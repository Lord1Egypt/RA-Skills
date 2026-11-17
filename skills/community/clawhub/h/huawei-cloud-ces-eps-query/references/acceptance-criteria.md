# Acceptance Criteria

Issue #32 — 只读的华为云 CES/EPS 管理面查询 Skill（自然语言触发）.

## Functional

- [x] **CES 7 类查询**: `alarm-rules` 告警规则 / `alarm-histories` 告警历史 /
      `alarm-templates` 告警模板 / `dashboards` 仪表盘 / `notification-masks`
      通知掩码 / `resource-groups` 资源分组 / `one-click-alarms` 一键告警.
- [x] **EPS 5 类查询**: `eps-projects` 企业项目列表 / `eps-project-detail`
      企业项目详情 / `eps-quotas` 企业项目配额 / `eps-resources` 企业项目绑定
      资源 / `eps-migration-records` 迁移记录.
- [x] **自然语言触发**: `--query "<中文/英文意图>"` 路由到对应类别；
      `--list-categories` 列出全部 12 类；未知意图明确报错.
- [x] **三级回退**: CLI (`hcloud CES|EPS <Operation>`) → SDK
      (`huaweicloudsdkces` v2 / `huaweicloudsdkeps` v1) → token REST GET.
- [x] **只读守卫**: 写操作意图（create/delete/update/enable/disable/migrate/
      batch-* 及中文 创建/删除/修改/更新/启用/停用/迁移资源 等）在执行任何命令
      之前被 `GuardError` 拦截.
- [x] **新增离线单元测试全部通过** — `python3 -m unittest discover -s tests`.

## Explicitly out of scope (never executed)

- [x] 原始指标数据点：`ShowMetricData` / `ListMetrics` / `BatchListMetricData`.
- [x] 服务级别指标值：RDS / DCS / DMS / EVS / ELB 等.
- [x] 任何写操作：create / update / delete / enable / disable / migrate /
      batch-*.

## Quality

- [x] SKILL.md 结构符合 华为云Skill检查规范（`validate-skill.sh`），≤500 行.
- [x] 文件数 ≤ 30，扩展名在白名单内，references 为 kebab-case.
- [x] 无硬编码 AK/SK，无 in-session 凭据录入形式.
- [x] 质量 CLI 集成：`scripts/ensure_cli.sh` / `install_cli.sh` 存在，
      SKILL.md 含强制包裹与 4 点嵌入.
- [x] **脚本执行路径强制包裹**: `scripts/ces_eps_query.py` 的 CLI 路径把每次
      `hcloud` 调用构造为 `skill-quality-cli run --skill-name
      huawei-cloud-ces-eps-query -- hcloud ...`（缺失 CLI 或
      `SKILL_QUALITY_REPORT=0` 时回退裸 `hcloud`），与 SKILL.md 口径一致.
- [x] **辅助脚本离线单测**: `tests/test_ensure_env.py` /
      `tests/test_yaml_check_frontmatter.py` 覆盖两个脚本的成功与失败路径.