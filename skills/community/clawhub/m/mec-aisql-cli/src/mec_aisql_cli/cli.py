"""mec-aisql-cli 主入口模块

本模块定义了 CLI 的全部顶级命令，供人类用户和 AI Bot 共同使用。

== AI Bot 使用指南 ==

所有命令均支持 ``--json`` 输出模式和 ``--url`` 自定义 API 地址。
Token 存储在 ``~/.minglue/tokens.json``，配置存储在 ``~/.minglue/aisql_config.json``。

命令分类:
  - 自动化流程: ``run`` (交互式) / ``bot`` (全自动) / ``batch`` (批量)
  - 结果查询:   ``result`` (结果+下载+导出)
  - 系统:       ``login`` / ``logout`` / ``config`` / ``config-set`` / ``config-reset`` / ``version``

典型 Bot 生命周期:
  1. login       — 获取 Token
  2. config-set  — 预设 client/brand/datafrom 等默认值
  3. bot --json  — 全自动生成 SQL → 守卫 → 校验 → 创建 → 执行 → 监控 → 结果
  4. result      — 查询历史任务结果

退出码约定:
  0   成功
  1   一般错误 (API 失败、参数缺失、SQL 校验不通过等)
  2   任务已停止 (watch 检测到 Stopped)
  3   需要人工审核 (watch 检测到 NeedHumanReview)
  124 watch 超时
"""
import json
import sys

import typer

from mec_aisql_cli.commands.aisql import app as aisql_app
from mec_aisql_cli.commands.agent import run_agent, run_bot
from mec_aisql_cli.config import Config
from mec_aisql_cli.api_client import AisqlApiClient

# 确保 Windows 终端 UTF-8 输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

app = typer.Typer(
    help="mec-aisql-cli - AI SQL generation, validation, and task management for MEC platform",
    add_completion=True,
)

# 注册 aisql 子命令组 (16 个子命令: gen/translate/create/perform/status/watch/validate/agree/check-agreement/models/retry/stop/list/detail/sql/error)
app.add_typer(aisql_app, name="aisql", help="AISQL 管理命令 (gen/translate/create/perform/status/watch/validate/list/detail/sql/error/...)")
# sql 别名 — 与 aisql 完全相同，提供更短的调用路径
app.add_typer(aisql_app, name="sql", help="AISQL 别名命令", hidden=False)


# ============================================================
# 命令: run
# ============================================================
@app.command("run")
def run(
    comment: str = typer.Option(..., "--comment", "-c", help="需求描述 (如: 统计某品牌曝光量)"),
    client: str = typer.Option("", "--client", help="客户名称 (未填则从 config 读取或交互提示)"),
    brand: str = typer.Option("", "--brand", help="品牌名称 (未填则从 config 读取或交互提示)"),
    datafrom: str = typer.Option("", "--datafrom", help="数据来源: ADM/OTT-OM/OTT-PMO/TVM/BDID-MZID/BDID-IPV6"),
    contype: str = typer.Option("", "--contype", help="分析类型 (可选)"),
    datetimefw: str = typer.Option("", "--datetimefw", help="时间范围, 格式 '2026-03-01/2026-03-31' 或 '20260301-20260331'"),
    model: str = typer.Option("", "--model", "-m", help="AI 模型 (默认使用 config 中的 model 配置)"),
    task_name: str = typer.Option("", "--task-name", "-t", help="任务名称 (留空则自动生成)"),
    auto_create: bool = typer.Option(False, "--auto-create", help="自动创建任务, 跳过用户确认"),
    auto_perform: bool = typer.Option(False, "--auto-perform", help="自动执行任务(创建工单), 跳过用户确认"),
    watch: bool = typer.Option(False, "--watch", "-w", help="创建工单后自动轮询监控进度直到完成"),
    watch_timeout: int = typer.Option(1800, "--watch-timeout", help="监控最大等待秒数 (默认 1800 = 30 分钟)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过所有确认提示 (等同 --auto-create --auto-perform)"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL (默认使用 config 中的 base_url)"),
    debug: bool = typer.Option(False, "--debug", help="启用调试模式 (打印请求/响应详情)"),
):
    """一键运行 AI SQL 全流程 (交互式)

    AI Usage:
        - 适用于人工 CLI 操作, 可在缺失参数时交互提示
        - AI Bot 应优先使用 ``bot`` 命令 (全自动、无交互、JSON 输出)
        - 如需批量执行, 使用 ``batch`` 命令

    Pipeline (7 阶段):
        1. AI 生成 SQL (gensql API)
        2. SQL 类型守卫 (仅提示, 不阻断)
        3. 后端校验 (validate API: 表名/时间过滤/DDL 检查)
        4. 创建任务 (create API)
        5. 执行工单 (perform API)
        6. 监控进度 (watch, 可选 --watch)
        7. 查询结果 (result, 可选)

    Exit codes:
        0 — 全流程成功完成
        1 — 任一阶段失败 (生成失败/校验不通过/创建失败/执行失败/监控失败)

    示例::

        mec-aisql run -c "统计某品牌曝光量" --client "客户A" --brand "品牌B" \\
            --datafrom ADM --datetimefw "2026-03-01/2026-03-31"
        mec-aisql run -c "需求描述" --auto-create --auto-perform --watch
        mec-aisql run -c "需求描述" --yes --watch  # 跳过所有确认
    """
    run_agent(
        comment=comment,
        client_name=client,
        brand=brand,
        datafrom=datafrom,
        contype=contype,
        datetimefw=datetimefw,
        model=model,
        task_name=task_name,
        auto_create=auto_create,
        auto_perform=auto_perform,
        watch_after=watch,
        watch_timeout=watch_timeout,
        no_confirm=yes,
        base_url=base_url,
        debug=debug,
    )


# ============================================================
# 命令: bot
# ============================================================
@app.command("bot")
def bot(
    comment: str = typer.Option(..., "--comment", "-c", help="需求描述 (必填, 如: 统计曝光量)"),
    client: str = typer.Option(..., "--client", help="客户名称 (必填)"),
    brand: str = typer.Option(..., "--brand", help="品牌名称 (必填)"),
    datafrom: str = typer.Option(..., "--datafrom", help="数据来源 (必填: ADM/OTT-OM/OTT-PMO/TVM/BDID-MZID/BDID-IPV6)"),
    datetimefw: str = typer.Option("", "--datetimefw", help="时间范围, 格式 '2026-03-01/2026-03-31' 或 '20260301-20260331'"),
    contype: str = typer.Option("", "--contype", help="分析类型 (可选)"),
    model: str = typer.Option("", "--model", "-m", help="AI 模型 (可选, 默认使用 config 中的配置)"),
    task_name: str = typer.Option("", "--task-name", "-t", help="任务名称 (可选, 留空自动生成)"),
    clientid: str = typer.Option("", "--clientid", help="客户 ID (可选, 留空自动按 client 名查找)"),
    brandid: str = typer.Option("", "--brandid", help="品牌 ID (可选, 留空自动按 brand 名查找)"),
    watch_timeout: int = typer.Option(1800, "--watch-timeout", help="监控超时秒数 (默认 1800)"),
    max_regen: int = typer.Option(2, "--max-regen", help="SQL 非统计类时最大重新生成次数 (默认 2)"),
    json_output: bool = typer.Option(False, "--json", help="输出结构化 JSON 结果 (适合 Bot 程序消费)"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
    debug: bool = typer.Option(False, "--debug", help="启用调试模式"),
):
    """Bot 模式: 全自动非交互式执行, 仅允许统计类 SQL

    AI Usage:
        - 这是 AI Bot 自动化执行的**首选命令**
        - 前置条件: 需先 ``login`` 获取 Token
        - 全程无交互确认, 所有必填参数必须通过命令行传入
        - SQL 类型守卫强制启用: 仅允许统计类查询 (COUNT/SUM/AVG/GROUP BY/DISTINCT)
        - 非统计类 SQL 会自动重新生成 (最多 --max-regen 次), 超限则阻断

    Pipeline (7 阶段):
        1. AI 生成 SQL
        2. SQL 类型守卫 (强制阻断非统计类)
        3. 后端校验 (表名/时间过滤/DDL)
        4. 创建任务
        5. 执行工单
        6. 监控进度直到完成
        7. 查询最终结果

    JSON 输出 (``--json`` 模式):

        成功::

            {
              "success": true,
              "task_id": 123,
              "sql": "SELECT brand, COUNT(*) ...",
              "sql_type": "statistical",
              "aggregate_functions": ["COUNT"],
              "status": "Succeeded",
              "table_name": "result_table_xxx",
              "file_router": "/path/to/result.csv",
              "order_id": "ORD123",
              "dms_query_id": "DMS456"
            }

        失败::

            {
              "success": false,
              "error": "SQL_TYPE_BLOCKED",
              "message": "Bot 自动化仅允许统计类 SQL...",
              "sql_type": "select_only",
              "sql": "SELECT name FROM ..."
            }

    Error codes:
        MISSING_PARAMS     — 缺少必要参数 (client/brand/datafrom/datetimefw)
        NOT_AUTHENTICATED  — 未登录或 Token 过期
        GEN_FAILED         — AI 生成 SQL 失败
        SQL_TYPE_BLOCKED   — SQL 类型守卫阻断 (重试后仍非统计类)
        VALIDATION_FAILED  — 后端校验失败
        CREATE_FAILED      — 创建任务失败
        PERFORM_FAILED     — 执行工单失败
        WATCH_FAILED       — 监控失败 (任务最终状态非 Succeeded)

    Exit codes:
        0 — 成功
        1 — 失败 (见 error 字段)

    示例::

        mec-aisql bot -c "统计曝光量" --client "客户A" --brand "品牌B" \\
            --datafrom ADM --datetimefw "2026-03-01/2026-03-31" --json
    """
    result = run_bot(
        comment=comment,
        client_name=client,
        brand=brand,
        datafrom=datafrom,
        datetimefw=datetimefw,
        contype=contype,
        model=model,
        task_name=task_name,
        clientid=clientid,
        brandid=brandid,
        watch_timeout=watch_timeout,
        max_regen_attempts=max_regen,
        base_url=base_url,
        debug=debug,
    )

    # --json 模式: 输出结构化 JSON 供程序消费
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0 if result.get("success") else 1)

    # 非 JSON 模式: 人类可读的失败提示
    if not result.get("success"):
        typer.echo(f"\n[BOT FAILED] {result.get('error', '')}: {result.get('message', '')}")
        raise typer.Exit(code=1)


# ============================================================
# 命令: result
# ============================================================
@app.command("result")
def result(
    id: int = typer.Option(..., "--id", help="任务 ID (必填)"),
    download: str = typer.Option("", "--download", help="下载结果文件到指定本地路径 (使用 fileRouter URL)"),
    export: str = typer.Option("", "--export", help="导出结果元数据到文件 (支持 .json 和 .csv 格式)"),
    json_output: bool = typer.Option(False, "--json", help="输出 JSON 格式结果"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
):
    """查询任务执行结果 (结果表名、文件路径、DMS ID 等)

    AI Usage:
        - 用于查询已完成或执行中任务的结果信息
        - 支持三种操作模式:
          1. 默认: 文本展示结果摘要
          2. ``--download``: 下载结果文件到本地
          3. ``--export``: 导出完整元数据 (JSON/CSV)
        - 可配合 ``bot`` 命令的输出 task_id 使用

    JSON 输出 (``--json`` 模式)::

        {
          "success": true,
          "task_id": 123,
          "status": "Succeeded",
          "table_name": "result_table_xxx",
          "file_router": "/path/to/result.csv",
          "order_id": "ORD123",
          "dms_query_id": "DMS456",
          "dms_export_id": "DMS789"
        }

    Export 格式 (``--export meta.json``):
        包含 15 个字段: task_id, status, progress, table_name, file_router,
        order_id, dms_query_id, dms_export_id, sql_content, create_time,
        order_date, sql_con_date, dms_task_time, error_code, error_message

    Exit codes:
        0 — 查询成功 (或下载/导出成功)
        1 — 查询失败 / 下载失败 / fileRouter 为空

    示例::

        mec-aisql result --id 123
        mec-aisql result --id 123 --json
        mec-aisql result --id 123 --download ./result.csv
        mec-aisql result --id 123 --export ./meta.json
        mec-aisql result --id 123 --export ./meta.csv
    """
    from mec_aisql_cli.commands.aisql import _build_client
    from mec_aisql_cli.output import print_result

    client = _build_client(base_url)
    status_result = client.get_aisql_agent_status({"id": id})
    success = status_result.get("success") or status_result.get("Success")
    data = status_result.get("data", {}) if success else {}

    # --- 模式 1: 导出元数据到文件 ---
    # 支持 .json (完整 JSON) 和 .csv (单行 CSV, 适合 Excel)
    if export:
        from pathlib import Path
        export_data = {
            "task_id": id,
            "status": data.get("agentStatus", ""),
            "progress": data.get("progress", 0),
            "table_name": data.get("tableName", ""),
            "file_router": data.get("fileRouter", ""),
            "order_id": data.get("orderid", ""),
            "dms_query_id": data.get("sqldmsid", ""),
            "dms_export_id": data.get("dmstaskid", ""),
            "sql_content": data.get("sqlcontent", ""),
            "create_time": str(data.get("createTime", "")),
            "order_date": str(data.get("orderdate", "")),
            "sql_con_date": str(data.get("sqlcondate", "")),
            "dms_task_time": str(data.get("dmstasktime", "")),
            "error_code": data.get("lastErrorCode", ""),
            "error_message": data.get("lastErrorMessage", ""),
        }
        export_path = Path(export)
        if export_path.suffix.lower() == ".csv":
            # CSV 格式: 使用 utf-8-sig (BOM) 确保 Excel 正确显示中文
            import csv
            with open(export_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(export_data.keys())
                writer.writerow(export_data.values())
        else:
            # 默认 JSON 格式
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
        typer.echo(f"结果元数据已导出到: {export}")
        raise typer.Exit(code=0 if success else 1)

    # --- 模式 2: 下载结果文件 ---
    # 从 fileRouter 字段获取 URL, 使用带 Token 的 HTTP 请求下载
    if download:
        file_router = data.get("fileRouter", "")
        if not file_router:
            typer.echo("该任务暂无结果文件可下载 (fileRouter 为空)。")
            raise typer.Exit(code=1)
        try:
            saved = client.download_result_file(file_router, download)
            typer.echo(f"结果文件已下载到: {saved}")
            raise typer.Exit(code=0)
        except Exception as e:
            typer.echo(f"下载失败: {e}")
            raise typer.Exit(code=1)

    # --- 模式 3: JSON 输出 ---
    if json_output:
        output = {
            "success": bool(success),
            "task_id": id,
            "status": data.get("agentStatus", ""),
            "table_name": data.get("tableName", ""),
            "file_router": data.get("fileRouter", ""),
            "order_id": data.get("orderid", ""),
            "dms_query_id": data.get("sqldmsid", ""),
            "dms_export_id": data.get("dmstaskid", ""),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        raise typer.Exit(code=0 if success else 1)

    # --- 模式 4: 文本展示 (默认) ---
    if not success:
        print_result(status_result, title="查询结果", as_json=False)
        return

    typer.echo(f"\n{'=' * 60}")
    typer.echo(f"  任务执行结果 (ID: {id})")
    typer.echo(f"{'=' * 60}")
    typer.echo(f"  状态:       {data.get('agentStatus', '-')}")
    typer.echo(f"  进度:       {data.get('progress', 0)}%")
    if data.get("aiTaskName"):
        typer.echo(f"  任务名:     {data['aiTaskName']}")
    if data.get("tableName"):
        typer.echo(f"  结果表名:   {data['tableName']}")
    if data.get("fileRouter"):
        typer.echo(f"  结果文件:   {data['fileRouter']}")
    if data.get("sqldmsid"):
        typer.echo(f"  DMS查询ID:  {data['sqldmsid']}")
    if data.get("dmstaskid"):
        typer.echo(f"  DMS导出ID:  {data['dmstaskid']}")
    if data.get("orderid"):
        typer.echo(f"  工单ID:     {data['orderid']}")
    if data.get("sqlcontent"):
        # SQL 内容通常很长, 截取前 200 字符展示
        typer.echo(f"  执行SQL:    {data['sqlcontent'][:200]}...")
    if data.get("lastErrorMessage"):
        typer.echo(f"  最后错误:   {data['lastErrorMessage']}")


# ============================================================
# 命令: login
# ============================================================
@app.command("login")
def login(
    account: str = typer.Option(..., "--account", "-a", help="登录账号 (必填)"),
    password: str = typer.Option(..., "--password", "-p", help="登录密码 (必填)"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL (默认使用 config 中的 base_url)"),
    debug: bool = typer.Option(False, "--debug", help="启用调试模式"),
):
    """登录 MEC 平台并保存 Token

    AI Usage:
        - Bot 启动时的**第一步操作**
        - Token 保存到 ``~/.minglue/tokens.json``, 后续所有命令自动读取
        - Token 过期后 API Client 会自动刷新, 无需重新登录
        - 如刷新失败, 需重新执行 login

    Exit codes:
        0 — 登录成功, Token 已保存
        1 — 登录失败 (账号/密码错误, 网络异常等)

    示例::

        mec-aisql login --account myuser --password mypass
        mec-aisql login -a myuser -p mypass --url https://example.com/api
    """
    config = Config()
    url = base_url or config.get("base_url", "https://mec.miaozhen.com/taskmng")
    client = AisqlApiClient(url, debug=debug)
    result = client.get_token(account, password)

    if result.get("success"):
        typer.echo("登录成功，Token 已保存。")
    else:
        typer.echo(f"登录失败: {result.get('message', '未知错误')}")
        raise typer.Exit(code=1)


# ============================================================
# 命令: batch
# ============================================================
@app.command("batch")
def batch(
    file: str = typer.Option(..., "--file", "-f", help="批量任务文件路径 (必填, 支持 .json 或 .csv)"),
    common_client: str = typer.Option("", "--client", help="全局客户名称 (覆盖文件中每条的 client 字段)"),
    common_brand: str = typer.Option("", "--brand", help="全局品牌名称 (覆盖文件中每条的 brand 字段)"),
    common_datafrom: str = typer.Option("", "--datafrom", help="全局数据来源 (覆盖文件中每条的 datafrom 字段)"),
    max_regen: int = typer.Option(2, "--max-regen", help="非统计 SQL 时最大重新生成次数 (默认 2)"),
    watch_timeout: int = typer.Option(1800, "--watch-timeout", help="每个任务的监控超时秒数 (默认 1800)"),
    continue_on_error: bool = typer.Option(True, "--continue-on-error/--stop-on-error", help="某条任务失败后是否继续执行下一条"),
    json_output: bool = typer.Option(False, "--json", help="输出 JSON 汇总结果 (包含每条任务的结果)"),
    base_url: str = typer.Option("", "--url", "-u", help="API base URL"),
    debug: bool = typer.Option(False, "--debug", help="启用调试模式"),
):
    """批量执行多个查询任务 (从文件读取需求列表)

    AI Usage:
        - 当需要一次性执行多个统计查询时使用
        - 每条任务走完整的 Bot 流程 (gen → guard → validate → create → perform → watch → result)
        - 全局参数 (--client/--brand/--datafrom) 会覆盖文件中的值, 便于批量设置公共参数
        - ``--continue-on-error`` (默认): 某条失败后继续执行下一条
        - ``--stop-on-error``: 某条失败后立即终止

    文件格式:

        JSON 格式::

            [
              {
                "comment": "统计曝光量",
                "client": "客户A",
                "brand": "品牌B",
                "datafrom": "ADM",
                "datetimefw": "2026-03-01/2026-03-31"
            },
            {
                "comment": "统计点击量",
                "client": "客户A",
                "brand": "品牌B",
                "datafrom": "ADM",
                "datetimefw": "2026-03-01/2026-03-31"
              }
            ]

        CSV 格式 (第一行为表头)::

            comment,client,brand,datafrom,datetimefw,contype
            统计曝光量,客户A,品牌B,ADM,2026-03-01/2026-03-31,
            统计点击量,客户A,品牌B,ADM,2026-03-01/2026-03-31,

    JSON 输出 (``--json`` 模式)::

        {
          "success": true,          // 所有任务成功为 true
          "total": 3,               // 总任务数
          "succeeded": 2,           // 成功数
          "failed": 1,               // 失败数
          "results": [              // 每条任务的结果 (结构同 bot 命令)
            {"success": true, "task_id": 123, ...},
            {"success": true, "task_id": 124, ...},
            {"success": false, "error": "...", ...}
          ]
        }

    Exit codes:
        0 — 所有任务成功
        1 — 至少一个任务失败

    示例::

        mec-aisql batch --file tasks.json --json
        mec-aisql batch --file tasks.csv --client "客户A" --brand "品牌B" --datafrom ADM
        mec-aisql batch --file tasks.json --stop-on-error  # 失败即停
    """
    from pathlib import Path
    from mec_aisql_cli.commands.agent import run_bot

    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"文件不存在: {file}")
        raise typer.Exit(code=1)

    # 根据文件扩展名选择解析方式
    tasks = []
    if file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    elif file_path.suffix.lower() == ".csv":
        import csv
        # utf-8-sig 兼容带 BOM 的 CSV (Excel 导出)
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            tasks = [dict(row) for row in reader]
    else:
        typer.echo(f"不支持的文件格式: {file_path.suffix} (请使用 .json 或 .csv)")
        raise typer.Exit(code=1)

    if not tasks:
        typer.echo("文件中没有任务数据。")
        raise typer.Exit(code=1)

    # 全局参数覆盖: 命令行传入的 --client/--brand/--datafrom 优先于文件中的值
    for task in tasks:
        if common_client:
            task["client"] = common_client
        if common_brand:
            task["brand"] = common_brand
        if common_datafrom:
            task["datafrom"] = common_datafrom

    results = []
    succeeded = 0
    failed = 0

    typer.echo(f"\n{'=' * 60}")
    typer.echo(f"  批量执行 ({len(tasks)} 个任务)")
    typer.echo(f"{'=' * 60}")

    # 逐条执行: 每条任务走完整的 run_bot 流程
    for i, task in enumerate(tasks, 1):
        comment = task.get("comment", "")
        client_name = task.get("client", "")
        brand = task.get("brand", "")
        datafrom = task.get("datafrom", "")
        datetimefw = task.get("datetimefw", "")
        contype = task.get("contype", "")

        typer.echo(f"\n[{i}/{len(tasks)}] {comment}")
        typer.echo(f"  客户={client_name}, 品牌={brand}, 来源={datafrom}, 时间={datetimefw}")

        result = run_bot(
            comment=comment,
            client_name=client_name,
            brand=brand,
            datafrom=datafrom,
            datetimefw=datetimefw,
            contype=contype,
            model="",
            task_name="",
            watch_timeout=watch_timeout,
            max_regen_attempts=max_regen,
            base_url=base_url,
            debug=debug,
        )

        results.append(result)

        if result.get("success"):
            succeeded += 1
            typer.echo(f"  [OK] task_id={result.get('task_id')} table={result.get('table_name', '')}")
        else:
            failed += 1
            typer.echo(f"  [FAIL] {result.get('error', '')}: {result.get('message', '')}")
            # --stop-on-error: 首条失败即终止
            if not continue_on_error:
                typer.echo("  --stop-on-error, 终止后续任务。")
                break

    # 汇总输出
    if json_output:
        summary = {
            "success": failed == 0,
            "total": len(tasks),
            "succeeded": succeeded,
            "failed": failed,
            "results": results,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        typer.echo(f"\n{'=' * 60}")
        typer.echo(f"  批量执行完成: {succeeded} 成功, {failed} 失败, 共 {len(tasks)} 个")
        typer.echo(f"{'=' * 60}")

    raise typer.Exit(code=0 if failed == 0 else 1)


# ============================================================
# 命令: logout
# ============================================================
@app.command("logout")
def logout():
    """清除已保存的 Token (登出)

    AI Usage:
        - 清除 ``~/.minglue/tokens.json`` 文件
        - 登出后所有需要认证的命令将失败, 需重新 ``login``
        - Bot 维护时可使用此命令清除旧 Token

    Exit codes:
        0 — 成功 (无论 Token 文件是否存在)

    示例::

        mec-aisql logout
    """
    from mec_aisql_cli.api_client import DEFAULT_TOKEN_PATH
    import os
    if os.path.exists(DEFAULT_TOKEN_PATH):
        os.remove(DEFAULT_TOKEN_PATH)
        typer.echo("已清除 Token。")
    else:
        typer.echo("没有已保存的 Token。")


# ============================================================
# 命令: config (查看配置)
# ============================================================
@app.command("config")
def config_show(
    key: str = typer.Option("", "--get", "-g", help="查看指定配置项的值 (不传则显示全部)"),
):
    """查看当前配置

    AI Usage:
        - Bot 启动时检查已保存的默认参数 (client/brand/datafrom 等)
        - 配置存储在 ``~/.minglue/aisql_config.json``
        - 可用 ``--get <key>`` 查询单个配置项, 不传则显示全部

    配置项列表:
        base_url     — API 地址 (默认: https://mec.miaozhen.com/taskmng)
        model        — AI 模型 (默认: mlamp/deepseek-v4-flash)
        client       — 默认客户
        brand        — 默认品牌
        datafrom     — 默认数据来源
        contype      — 默认分析类型
        datetimefw   — 默认时间范围
        timeout      — 请求超时秒数 (默认: 120)
        max_retries  — 最大重试次数 (默认: 2)

    示例::

        mec-aisql config            # 查看全部配置
        mec-aisql config --get client  # 查看 client 配置项
    """
    cfg = Config()
    if key:
        value = cfg.get(key, "<未设置>")
        typer.echo(f"{key} = {value}")
    else:
        typer.echo("当前配置:")
        for k, v in cfg.all().items():
            typer.echo(f"  {k}: {v}")


# ============================================================
# 命令: config-set (设置配置)
# ============================================================
@app.command("config-set")
def config_set(
    key: str = typer.Option(..., "--key", "-k", help="配置项名称 (如 client/brand/datafrom)"),
    value: str = typer.Option(..., "--value", "-v", help="配置值"),
):
    """设置配置项

    AI Usage:
        - Bot 预设默认参数, 避免每次命令都传入 --client/--brand 等参数
        - 设置后, 所有命令自动读取配置作为默认值
        - 命令行参数优先级 > 配置文件 > 内置默认值

    示例::

        mec-aisql config-set --key client --value "客户A"
        mec-aisql config-set --key brand --value "品牌B"
        mec-aisql config-set --key datafrom --value "ADM"
        mec-aisql config-set --key base_url --value "https://example.com/api"
    """
    cfg = Config()
    cfg.set(key, value)
    typer.echo(f"已设置 {key} = {value}")


# ============================================================
# 命令: config-reset (重置配置)
# ============================================================
@app.command("config-reset")
def config_reset(
    key: str = typer.Option("", "--key", "-k", help="要重置的配置项 (不传则重置全部)"),
):
    """重置配置为默认值

    AI Usage:
        - 传入 ``--key`` 重置单个配置项
        - 不传 ``--key`` 重置所有配置为默认值 (删除配置文件)

    示例::

        mec-aisql config-reset --key client    # 重置 client
        mec-aisql config-reset                 # 重置全部
    """
    cfg = Config()
    if key:
        cfg.unset(key)
        typer.echo(f"已重置 {key} 为默认值")
    else:
        import os
        if os.path.exists(cfg._path):
            os.remove(cfg._path)
        typer.echo("已重置所有配置为默认值")


# ============================================================
# 命令: version
# ============================================================
@app.command("version")
def version():
    """查看 CLI 版本号

    AI Usage:
        - Bot 可调用此命令检查当前使用的 CLI 版本
        - 输出为 JSON 格式, 便于程序解析

    输出::

        {"success": true, "message": "mec-aisql-cli version", "version": "0.3.1"}
    """
    output = {
        "success": True,
        "message": "mec-aisql-cli version",
        "version": "0.3.1",
    }
    print(json.dumps(output, ensure_ascii=False))


# ============================================================
# 命令: help
# ============================================================
@app.command("help")
def help_command():
    """显示帮助信息"""
    app(["--help"])


if __name__ == "__main__":
    app()
