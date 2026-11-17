# Acceptance Criteria

Issue #58 — 只读的华为云 AOM 资源名称列表查询 Skill.

## Functional

- [x] **12 类名称列表查询**: `alarm-rules` 告警规则 / `alarm-rule-templates`
      告警规则模板 / `metric-or-event-alarm-rules` 指标·事件告警规则 /
      `event2alarm-rules` 事件告警规则 / `action-rules` 行动规则 /
      `mute-rules` 静默规则 / `dashboards` 仪表盘 / `dashboard-folders`
      仪表盘分组 / `notification-templates` 通知模板 / `prom-instances`
      Prometheus 实例 / `access-codes` 接入码 / `service-discovery-rules`
      服务发现规则.
- [x] **名称列表输出**: 默认表格（名称字段排第一列）、`--json` 完整字段、
      `--names-only` 仅名称；仅写 stdout.
- [x] **自然语言触发**: `--query "<中文/英文意图>"` 路由到对应类别；
      `--list-categories` 列出全部 12 类；未知意图明确报错.
      **对外触发词一律带 AOM 限定前缀**（如 查询AOM告警规则 / AOM 监控看板列表），
      与同目录兄弟 skill 的“告警规则 / 仪表盘”词面解耦，避免 Agent 路由混淆；
      `--query` 内部仍接受裸词（告警规则 / 仪表盘 / 看板 / dashboard）。
- [x] **CLI 参数口径**: `ListPromInstance` 必填 `Enterprise-Project-Id` 且不接受
      `--limit`；`ListNotificationTemplates` 不接受 `--limit`；仅 `alarm-rules` /
      `metric-or-event-alarm-rules` 支持 `--limit`（脚本会丢弃类别不支持的参数）.
      企业项目参数在 AOM API 中是 **header**，KooCLI 只接受 header 形式
      `--Enterprise-Project-Id`（传 snake_case `--enterprise_project_id` 会被
      KooCLI 以 `[USE_ERROR]Invalid parameter` 拒绝）；脚本按类别
      `cli_param_names` 映射输出 `--Enterprise-Project-Id`，凡声明该参数的类别
      （`alarm-rule-templates` / `metric-or-event-alarm-rules` / `dashboards` /
      `dashboard-folders` / `notification-templates` / `prom-instances`）一律如此.
      未显式传 `--enterprise-project-id` 时，`prom-instances` 默认补 `0`
      （默认企业项目），保证自然语言查询走 CLI `ListPromInstance` 路径；
      若 SDK 路径返回权限类 `403`（`aom:metric:list` / `AOM.0403`），
      自动降级重试只读 CLI 路径，避免单一凭据权限缺口导致整类查询不可用.
- [x] **环境准备优先**: Workflow 第 1 步要求先跑 `scripts/ensure_env.py`
      （幂等安装 `huaweicloudsdkaom`），避免 SDK 兜底缺失导致自然语言用例被跳过.
- [x] **三级回退**: CLI (`hcloud AOM <Operation>`) → SDK
      (`huaweicloudsdkaom` v2) → token REST GET.
- [x] **只读守卫**: 写操作意图（create/delete/update/enable/disable/batch-*
      及中文 创建/删除/修改/更新/启用/停用/升级 等）在执行任何命令之前被
      `GuardError` 拦截.
- [x] **异常分类**: `ConfigError`（凭据/CLI/SDK 缺失）/ `AuthError`（401/403）
      / `ApiError`（网络/API 失败）/ `GuardError`（写意图），空结果有明确提示.
- [x] **新增离线单元测试全部通过** — `python3 -m unittest discover -s tests`.

## Explicitly out of scope (never executed)

- [x] 原始指标数据点：`ListMetricItems` / `ShowMetricsData` / Prometheus
      `query` / `query_range`.
- [x] 日志数据：`ListLogItems`.
- [x] AOM CMDB 详情查询：`ShowAppByName` / `ShowComponentByName` /
      `ShowEnvByName`（无列表接口，非“名称列表”语义）.
- [x] 任何写操作：create / update / delete / batch-*.

## Quality

- [x] SKILL.md 结构符合 华为云Skill检查规范（`validate-skill.sh`），≤500 行.
- [x] 文件数 ≤ 30，扩展名在白名单内，references 为 kebab-case.
- [x] 无硬编码 AK/SK，无 in-session 凭据录入形式.
- [x] 质量 CLI 集成：`scripts/ensure_cli.sh` / `install_cli.sh` 存在，
      SKILL.md 含强制包裹与 4 点嵌入.