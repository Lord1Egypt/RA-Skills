# 安全规则

## 快速概览

- 本仓库默认用于查询、审计、分析与巡检。
- 业务对象和权限对象只保留读取、审计、分析、巡检能力。
- 歧义未消除、对象无法精确定位、组织不明确时，拒绝继续执行。
- 本地仅允许 `config-write --confirm` 与 `select-org --confirm` 两类运行时准备写入。

## 风险等级

| 风险等级 | 场景 |
|---|---|
| 低 | 只读查询、审计查询、故障排查查询 |
| 中 | 本地配置写入、组织上下文确认 |
| 高 | 业务对象变更、权限变更、批量调整 |

## 动作边界矩阵

| 动作 | 当前是否支持 | 处理方式 |
|---|---|---|
| `jms_query.py object-list/object-get` | 支持 | 直接执行 |
| `jms_query.py permission-list/permission-get` | 支持 | 直接执行 |
| `jms_query.py audit-list/audit-get/audit-analyze` | 支持 | 直接执行 |
| `jms_diagnose.py inspect/resolve/user-assets/...` | 支持 | 直接执行 |
| `config-write --confirm` | 支持 | 仅写本地 `.env` |
| `select-org --confirm` | 支持 | 仅写本地 `JMS_ORG_ID` |
| 对象创建、更新、删除、解锁 | 不支持 | 阻塞并说明本仓库不提供对象写操作 |
| 授权创建、更新、追加、移除、删除 | 不支持 | 阻塞并说明本仓库不承担权限写操作 |

## 阻塞规则

| 条件 | 要求 |
|---|---|
| 未选组织 | 先 `select-org` |
| 多个候选对象 | 拒绝继续执行 |
| 名称存在歧义 | 拒绝继续执行 |
| 当前组织是 A，目标对象在 B | 拒绝跨组织继续执行 |
| 请求对象写操作 | 直接说明超出本仓库范围 |
| 想用临时脚本绕过正式入口 | 拒绝并回到 `scripts/jumpserver_api/jms_*.py` |

## 推荐阻塞模板

```text
本仓库范围：查询、审计、治理分析、本地运行时预检。
目标动作：<create / update / delete / unblock / append / remove>
阻塞原因：该动作属于业务对象或权限对象写操作，本仓库不提供此类写能力。

建议下一步：
1. 先执行相关查询，确认对象和范围。
2. 如确需恢复写能力，请在正式 wrapper 中补充并单独评审。
```
