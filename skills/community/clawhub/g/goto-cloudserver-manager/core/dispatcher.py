"""根据 provider + os_type + database 路由到对应适配器并执行操作。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from core.config_loader import ConfigLoader, ServerConfig
from core.policy_engine import PolicyEngine, PolicyViolationError, ConfirmationRequiredError

logger = structlog.get_logger(__name__)


@dataclass
class ActionResult:
    success: bool
    action: str
    server_id: str
    output: str = ""
    error: str = ""
    data: dict = field(default_factory=dict)

    def __bool__(self) -> bool:
        return self.success


class CloudServerManagerDispatcher:
    def __init__(
        self,
        config_loader: ConfigLoader | None = None,
        policy_engine: PolicyEngine | None = None,
    ) -> None:
        self._config = config_loader or ConfigLoader()
        self._policy = policy_engine or PolicyEngine()

    # ── 主入口 ────────────────────────────────────────────────────────────────

    def dispatch(
        self,
        server_id: str,
        action: str,
        params: dict[str, Any] | None = None,
        confirmed: bool = False,
    ) -> ActionResult:
        """
        执行一个运维动作。

        confirmed=True 表示上层已展示计划并收到用户确认，跳过 ConfirmationRequiredError。
        """
        params = params or {}
        server = self._config.get_server(server_id)
        log = logger.bind(server_id=server_id, action=action, environment=server.environment)

        # 策略检查
        try:
            self._policy.check(
                action=action,
                environment=server.environment,
                plan={"server": server_id, "params": params},
            )
        except PolicyViolationError as e:
            log.warning("action_forbidden", reason=str(e))
            return ActionResult(success=False, action=action, server_id=server_id, error=str(e))
        except ConfirmationRequiredError as e:
            if not confirmed:
                log.info("awaiting_confirmation", plan=e.plan)
                return ActionResult(
                    success=False,
                    action=action,
                    server_id=server_id,
                    error="需要用户确认后才能执行。",
                    data={"requires_confirmation": True, "plan": e.plan},
                )

        log.info("executing_action")
        try:
            result = self._execute(server, action, params)
            log.info("action_completed", success=result.success)
            return result
        except Exception as e:
            log.error("action_failed", error=str(e))
            return ActionResult(success=False, action=action, server_id=server_id, error=str(e))

    # ── 路由 ─────────────────────────────────────────────────────────────────

    # 这些 action 直接调用云厂商控制台 API（AK/SK），不需要 SSH/WinRM/云助手连接
    _PROVIDER_ONLY_ACTIONS = frozenset({
        "list_instances", "get_instance", "describe_security_groups",
        "modify_security_group", "reboot_instance",
    })

    def _execute(self, server: ServerConfig, action: str, params: dict) -> ActionResult:
        if action in self._PROVIDER_ONLY_ACTIONS:
            return self._route_action(server, None, action, params)
        executor = self._get_executor(server)
        server = self._ensure_host_ip(server, executor)
        try:
            executor.connect(server)
            result = self._route_action(server, executor, action, params)
        finally:
            executor.close()
        return result

    def _ensure_host_ip(self, server: ServerConfig, executor: Any) -> ServerConfig:
        """SSH/WinRM 直连需要真实 IP；servers.yaml 未配置时，实时查云厂商 API 补全。

        cloud_assistant/TAT 通道按 instance_id 派发命令，不需要 IP，因此只在
        真正落到 SSH/WinRM 执行器时才查询，避免给不需要的请求增加额外 API 调用。
        """
        from executor.ssh_executor import SSHExecutor
        from executor.winrm_executor import WinRMExecutor
        if not isinstance(executor, (SSHExecutor, WinRMExecutor)):
            return server
        if server.public_ip or server.private_ip:
            return server
        instance = self._get_provider(server).get_instance(server.instance_id, server.region)
        return server.model_copy(update={"public_ip": instance.public_ip, "private_ip": instance.private_ip})

    def _route_action(self, server: ServerConfig, executor: Any, action: str, params: dict) -> ActionResult:
        """根据 action 名称路由到对应处理方法。"""
        if action in ("check_server_status", "check_disk", "check_memory", "check_cpu", "check_network"):
            return self._check_server(server, executor, action, params)
        elif action == "install_database":
            return self._install_database(server, executor, params)
        elif action == "create_database":
            return self._create_database(server, executor, params)
        elif action == "apply_schema":
            return self._apply_schema(server, executor, params)
        elif action == "create_index":
            return self._create_index(server, executor, params)
        elif action in ("health_check", "check_database_status", "check_database_connections"):
            return self._database_health_check(server, executor, params)
        elif action == "read_recent_logs":
            return self._read_logs(server, executor, params)
        elif action == "generate_report":
            return self._generate_report(server, executor, params)
        elif action == "restart_service":
            return self._restart_service(server, executor, params)
        elif action == "backup_database":
            return self._backup_database(server, executor, params)
        elif action == "restore_database":
            return self._restore_database(server, executor, params)
        elif action == "create_user":
            return self._create_user(server, executor, params)
        elif action == "seed_data":
            return self._seed_data(server, executor, params)
        elif action in ("configure_firewall", "modify_firewall"):
            return self._configure_firewall(server, executor, params)
        elif action == "configure_winrm":
            return self._configure_winrm(server, executor, params)
        elif action in ("install_monitoring_agent", "install_windows_exporter", "install_node_exporter"):
            return self._install_monitoring_agent(server, executor, params)
        elif action == "list_instances":
            return self._list_instances(server, params)
        elif action == "get_instance":
            return self._get_instance(server, params)
        elif action == "describe_security_groups":
            return self._describe_security_groups(server, params)
        elif action == "modify_security_group":
            return self._modify_security_group(server, params)
        elif action == "reboot_instance":
            return self._reboot_instance(server, params)
        else:
            return ActionResult(
                success=False,
                action=action,
                server_id=server.id,
                error=f"未知操作：'{action}'",
            )

    # ── 执行器工厂 ────────────────────────────────────────────────────────────

    def _get_executor(self, server: ServerConfig):
        conn = server.connection
        provider_cfg = self._config.get_provider_config(server.provider)
        creds = self._config.get_server_credentials(server.id)

        primary = conn.type
        if primary == "cloud_assistant" and server.provider == "aliyun":
            from executor.cloud_command_executor import CloudCommandExecutor
            return CloudCommandExecutor(
                provider="aliyun",
                provider_config=provider_cfg,
                credentials=self._config.get_provider_credentials(server.provider),
            )
        if primary == "tat" and server.provider in ("tencent", "tencent-lighthouse"):
            from executor.cloud_command_executor import CloudCommandExecutor
            return CloudCommandExecutor(
                provider=server.provider,
                provider_config=provider_cfg,
                credentials=self._config.get_provider_credentials(server.provider),
            )
        if primary == "winrm" or (primary in ("cloud_assistant", "tat") and conn.fallback == "winrm"):
            from executor.winrm_executor import WinRMExecutor
            winrm_creds = creds.get("winrm", {})
            return WinRMExecutor(
                username=winrm_creds.get("username", conn.winrm.username),
                password=winrm_creds.get("password", conn.winrm.password),
                port=conn.winrm.port,
                use_ssl=conn.winrm.use_ssl,
            )
        if primary == "ssh" or conn.fallback == "ssh":
            from executor.ssh_executor import SSHExecutor
            ssh_creds = creds.get("ssh", {})
            return SSHExecutor(
                username=ssh_creds.get("username", conn.ssh.username),
                key_path=ssh_creds.get("key_path", conn.ssh.key_path),
                password=ssh_creds.get("password", conn.ssh.password),
                port=conn.ssh.port,
            )
        from executor.local_executor import LocalExecutor
        return LocalExecutor()

    # ── 云厂商 Provider 工厂 ──────────────────────────────────────────────────

    def _get_provider(self, server: ServerConfig):
        creds = self._config.get_provider_credentials(server.provider)
        if server.provider == "aliyun":
            from providers.aliyun.ecs import AliyunECS
            return AliyunECS(
                access_key_id=creds.get("access_key_id", ""),
                access_key_secret=creds.get("access_key_secret", ""),
                default_region=server.region,
            )
        if server.provider == "tencent":
            from providers.tencent.cvm import TencentCVM
            return TencentCVM(
                secret_id=creds.get("secret_id", ""),
                secret_key=creds.get("secret_key", ""),
                default_region=server.region,
            )
        if server.provider == "tencent-lighthouse":
            from providers.tencent.lighthouse import TencentLighthouse
            return TencentLighthouse(
                secret_id=creds.get("secret_id", ""),
                secret_key=creds.get("secret_key", ""),
                default_region=server.region,
            )
        if server.provider == "huawei":
            from providers.huawei.ecs import HuaweiECS
            return HuaweiECS(
                access_key_id=creds.get("access_key_id", ""),
                secret_access_key=creds.get("secret_access_key", ""),
                project_id=creds.get("project_id", ""),
                default_region=server.region,
            )
        raise ValueError(f"未知的云厂商：'{server.provider}'")

    # ── 动作实现 ──────────────────────────────────────────────────────────────

    def _upload_script(self, executor: Any, server: ServerConfig, local_script: Any) -> str:
        """把本地脚本文件上传到目标服务器的临时目录，返回远端路径。

        os_adapters/databases 下的脚本只存在于运行 Skill 的本机，必须先通过执行器
        （SSH/WinRM/云助手）传到目标服务器，才能在远端引用其路径执行——不能把本机路径
        直接拼进远端命令。
        """
        remote_path = (
            f"C:\\Windows\\Temp\\{local_script.name}"
            if server.os_type == "windows"
            else f"/tmp/{local_script.name}"
        )
        executor.upload_file(str(local_script), remote_path)
        return remote_path

    def _check_server(self, server: ServerConfig, executor: Any, action: str, params: dict) -> ActionResult:
        from pathlib import Path
        if server.os_type == "windows":
            local_script = Path(__file__).parent.parent / "os_adapters" / "windows" / "check_server.ps1"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}'"
        else:
            local_script = Path(__file__).parent.parent / "os_adapters" / "linux" / "check_server.sh"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"bash '{remote_script}'"
        result = executor.execute(cmd)
        return ActionResult(
            success=result.exit_code == 0,
            action=action,
            server_id=server.id,
            output=result.stdout,
            error=result.stderr,
        )

    def _install_database(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        db_type = params.get("database", "")
        from pathlib import Path
        base = Path(__file__).parent.parent / "databases" / db_type
        if server.os_type == "windows":
            remote_script = self._upload_script(executor, server, base / "install.ps1")
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}'"
        else:
            remote_script = self._upload_script(executor, server, base / "install.sh")
            cmd = f"bash '{remote_script}'"
        result = executor.execute(cmd, timeout=1800)
        return ActionResult(
            success=result.exit_code == 0,
            action="install_database",
            server_id=server.id,
            output=result.stdout,
            error=result.stderr,
        )

    def _create_database(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        db_type = params.get("database", self._infer_db_type(server))
        db_name = params.get("name", "")
        from pathlib import Path
        from jinja2 import Template
        tpl_path = Path(__file__).parent.parent / "databases" / db_type / "create_database.sql.j2"
        sql = Template(tpl_path.read_text(encoding="utf-8")).render(database_name=db_name)
        result = executor.execute_sql(db_type, sql)
        return ActionResult(
            success=result.exit_code == 0,
            action="create_database",
            server_id=server.id,
            output=result.stdout,
            error=result.stderr,
        )

    def _apply_schema(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        import yaml as _yaml
        from core.schema_compiler import SchemaCompiler, UnifiedSchema
        db_type = params.get("database", self._infer_db_type(server))
        schema_data = params.get("schema") or {}
        schema = UnifiedSchema.from_dict(schema_data) if schema_data else None
        if not schema:
            return ActionResult(success=False, action="apply_schema", server_id=server.id, error="缺少 schema 参数")
        ddl = SchemaCompiler().compile(schema, db_type)  # type: ignore[arg-type]
        result = executor.execute_sql(db_type, ddl)
        return ActionResult(
            success=result.exit_code == 0,
            action="apply_schema",
            server_id=server.id,
            output=ddl,
            error=result.stderr,
        )

    def _create_index(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        from core.schema_compiler import SchemaCompiler
        db_type = params.get("database", self._infer_db_type(server))
        table = params.get("table", "")
        columns = params.get("columns", [])
        if not table or not columns:
            return ActionResult(success=False, action="create_index", server_id=server.id, error="缺少 table 或 columns 参数")
        sql = SchemaCompiler().compile_create_index(
            table, columns, db_type,  # type: ignore[arg-type]
            database=params.get("name", ""),
            index_name=params.get("index_name", ""),
            unique=params.get("unique", False),
        )
        result = executor.execute_sql(db_type, sql)
        return ActionResult(success=result.exit_code == 0, action="create_index", server_id=server.id, output=sql, error=result.stderr)

    def _database_health_check(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        db_type = params.get("database", self._infer_db_type(server))
        from pathlib import Path
        sql_path = Path(__file__).parent.parent / "databases" / db_type / "health_check.sql"
        sql = sql_path.read_text(encoding="utf-8")
        result = executor.execute_sql(db_type, sql)
        return ActionResult(
            success=result.exit_code == 0,
            action="check_database_status",
            server_id=server.id,
            output=result.stdout,
        )

    def _read_logs(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        lines = params.get("lines", 100)
        if server.os_type == "windows":
            cmd = f"powershell -Command \"Get-EventLog -LogName Application -Newest {lines} | Format-List\""
        else:
            cmd = f"journalctl -n {lines} --no-pager"
        result = executor.execute(cmd)
        return ActionResult(success=result.exit_code == 0, action="read_recent_logs", server_id=server.id, output=result.stdout)

    def _generate_report(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        from core.report_generator import ReportGenerator
        report_type = params.get("type", "server_health_report")
        report = ReportGenerator().generate(report_type, server=server, params=params)
        return ActionResult(success=True, action="generate_report", server_id=server.id, output=report)

    def _restart_service(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        service = params.get("service", "")
        if server.os_type == "windows":
            cmd = f"Restart-Service -Name '{service}' -Force"
        else:
            cmd = f"systemctl restart {service}"
        result = executor.execute(cmd)
        return ActionResult(success=result.exit_code == 0, action="restart_service", server_id=server.id, output=result.stdout)

    def _backup_database(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        db_type = params.get("database", self._infer_db_type(server))
        from pathlib import Path
        db_name = params.get("name", "")
        if server.os_type == "windows":
            local_script = Path(__file__).parent.parent / "databases" / db_type / "backup.ps1"
            remote_script = self._upload_script(executor, server, local_script)
            dest = params.get("dest", "C:\\Backup")
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}' -DatabaseName '{db_name}' -Dest '{dest}'"
        else:
            dest = params.get("dest", "/backup")
            local_script = Path(__file__).parent.parent / "databases" / db_type / "backup.sh"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"bash '{remote_script}' {db_name} {dest}"
        result = executor.execute(cmd, timeout=3600)
        return ActionResult(success=result.exit_code == 0, action="backup_database", server_id=server.id, output=result.stdout)

    def _restore_database(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        db_type = params.get("database", self._infer_db_type(server))
        from pathlib import Path
        db_name = params.get("name", "")
        source = params.get("source", "")
        if not source:
            return ActionResult(success=False, action="restore_database", server_id=server.id, error="缺少 source 参数（备份文件路径）")
        if server.os_type == "windows":
            local_script = Path(__file__).parent.parent / "databases" / db_type / "restore.ps1"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}' -DatabaseName '{db_name}' -Source '{source}'"
        else:
            local_script = Path(__file__).parent.parent / "databases" / db_type / "restore.sh"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"bash '{remote_script}' {db_name} {source}"
        result = executor.execute(cmd, timeout=3600)
        return ActionResult(success=result.exit_code == 0, action="restore_database", server_id=server.id, output=result.stdout, error=result.stderr)

    def _create_user(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        # 注意：此处 params["database"] 表示目标数据库名（与 tasks.yaml 的 create_user 步骤一致），
        # 数据库引擎类型始终通过 _infer_db_type 推断，与 _create_database/_apply_schema 里
        # "database" 表示引擎类型的语义不同——这是 tasks.yaml 既有的命名歧义，不在本次改动范围内。
        db_type = self._infer_db_type(server)
        db_name = params.get("database", "")
        username = params.get("username", "")
        password = params.get("password", "")
        if not username:
            return ActionResult(success=False, action="create_user", server_id=server.id, error="缺少 username 参数")
        from pathlib import Path
        from jinja2 import Template
        tpl_path = Path(__file__).parent.parent / "databases" / db_type / "create_user.sql.j2"
        sql = Template(tpl_path.read_text(encoding="utf-8")).render(
            database_name=db_name, app_username=username, app_password=password,
        )
        result = executor.execute_sql(db_type, sql)
        return ActionResult(success=result.exit_code == 0, action="create_user", server_id=server.id, output=result.stdout, error=result.stderr)

    def _seed_data(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        from core.schema_compiler import SchemaCompiler
        db_type = params.get("database", self._infer_db_type(server))
        table = params.get("table", "")
        rows = params.get("rows", [])
        database_name = params.get("name", "")
        if not table or not rows:
            return ActionResult(success=False, action="seed_data", server_id=server.id, error="缺少 table 或 rows 参数")
        sql = SchemaCompiler().compile_insert(table, rows, db_type, database_name)  # type: ignore[arg-type]
        result = executor.execute_sql(db_type, sql)
        return ActionResult(success=result.exit_code == 0, action="seed_data", server_id=server.id, output=result.stdout, error=result.stderr)

    def _configure_firewall(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        from pathlib import Path
        ports = params.get("open_ports") or params.get("ports") or []
        source_cidr = params.get("source_cidr", "10.0.0.0/8")
        if not ports:
            return ActionResult(success=False, action="configure_firewall", server_id=server.id, error="缺少 open_ports 参数")
        if server.os_type == "windows":
            local_script = Path(__file__).parent.parent / "os_adapters" / "windows" / "configure_firewall.ps1"
            remote_script = self._upload_script(executor, server, local_script)
            port_args = " ".join(str(p) for p in ports)
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}' -Ports {port_args} -SourceCIDR '{source_cidr}'"
        else:
            local_script = Path(__file__).parent.parent / "os_adapters" / "linux" / "configure_firewall.sh"
            remote_script = self._upload_script(executor, server, local_script)
            ports_csv = ",".join(str(p) for p in ports)
            cmd = f"bash '{remote_script}' '{ports_csv}' '{source_cidr}'"
        result = executor.execute(cmd)
        return ActionResult(success=result.exit_code == 0, action="configure_firewall", server_id=server.id, output=result.stdout, error=result.stderr)

    def _configure_winrm(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        if server.os_type != "windows":
            return ActionResult(success=False, action="configure_winrm", server_id=server.id, error="WinRM 仅适用于 Windows 服务器")
        from pathlib import Path
        local_script = Path(__file__).parent.parent / "os_adapters" / "windows" / "configure_winrm.ps1"
        remote_script = self._upload_script(executor, server, local_script)
        port = params.get("port", 5986)
        cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}' -Port {port}"
        result = executor.execute(cmd)
        return ActionResult(success=result.exit_code == 0, action="configure_winrm", server_id=server.id, output=result.stdout, error=result.stderr)

    def _install_monitoring_agent(self, server: ServerConfig, executor: Any, params: dict) -> ActionResult:
        from pathlib import Path
        if server.os_type == "windows":
            local_script = Path(__file__).parent.parent / "os_adapters" / "windows" / "install_windows_exporter.ps1"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"powershell -ExecutionPolicy Bypass -File '{remote_script}'"
        else:
            local_script = Path(__file__).parent.parent / "os_adapters" / "linux" / "install_node_exporter.sh"
            remote_script = self._upload_script(executor, server, local_script)
            cmd = f"bash '{remote_script}'"
        result = executor.execute(cmd, timeout=600)
        return ActionResult(success=result.exit_code == 0, action="install_monitoring_agent", server_id=server.id, output=result.stdout, error=result.stderr)

    def _list_instances(self, server: ServerConfig, params: dict) -> ActionResult:
        provider = self._get_provider(server)
        region = params.get("region") or server.region
        instances = provider.list_instances(region)
        return ActionResult(
            success=True, action="list_instances", server_id=server.id,
            data={"instances": [vars(i) for i in instances]},
        )

    def _get_instance(self, server: ServerConfig, params: dict) -> ActionResult:
        provider = self._get_provider(server)
        instance = provider.get_instance(server.instance_id, server.region)
        return ActionResult(success=True, action="get_instance", server_id=server.id, data={"instance": vars(instance)})

    def _describe_security_groups(self, server: ServerConfig, params: dict) -> ActionResult:
        provider = self._get_provider(server)
        groups = provider.describe_security_groups(server.instance_id, server.region)
        return ActionResult(success=True, action="describe_security_groups", server_id=server.id, data={"security_groups": groups})

    def _modify_security_group(self, server: ServerConfig, params: dict) -> ActionResult:
        provider = self._get_provider(server)
        port = params.get("port")
        if not port:
            return ActionResult(success=False, action="modify_security_group", server_id=server.id, error="缺少 port 参数")
        security_group_id = params.get("security_group_id")
        if not security_group_id:
            groups = provider.describe_security_groups(server.instance_id, server.region)
            if not groups:
                return ActionResult(success=False, action="modify_security_group", server_id=server.id, error="未找到该实例关联的安全组")
            security_group_id = groups[0]["id"]
        ok = provider.update_security_group_rule(
            security_group_id=security_group_id,
            port=port,
            protocol=params.get("protocol", "TCP"),
            source_cidr=params.get("source_cidr", "10.0.0.0/8"),
            action=params.get("action", "accept"),
            region=server.region,
        )
        return ActionResult(success=ok, action="modify_security_group", server_id=server.id, data={"security_group_id": security_group_id})

    def _reboot_instance(self, server: ServerConfig, params: dict) -> ActionResult:
        provider = self._get_provider(server)
        ok = provider.reboot_instance(server.instance_id, server.region)
        return ActionResult(success=ok, action="reboot_instance", server_id=server.id)

    def _infer_db_type(self, server: ServerConfig) -> str:
        if server.databases:
            return server.databases[0].type
        return "mysql" if server.os_type == "linux" else "sqlserver"
