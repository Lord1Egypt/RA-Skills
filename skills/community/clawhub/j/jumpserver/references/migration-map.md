# 能力映射与缺口清单

## 当前结构摘要

- 维持 3 个正式业务入口的分域心智模型：`query / diagnose / report`。
- 把底层执行统一收口到 `scripts/jumpserver_api/`，不让请求入口散落在顶层或依赖临时 SDK 包装。
- 把“查询类能力”组织成 `capability` 能力单元，便于技能路由、意图识别和跨环境复用。
- 把运行时、能力元数据、统计聚合、对象查询、权限回看分层拆开，避免把 CLI 入口、业务逻辑和底层请求耦合在一起。
- `SKILL.md` 负责路由、边界和输入输出风格；`README.md` 负责整体使用说明；`references/*.md` 负责分域规则和能力清单；`references/metadata/*.json` 负责运行时结构化元数据；`jms_capabilities.py` 负责加载和导出能力事实。

## 目录与职责

| 目录 / 文件 | 当前职责 | 说明 |
|---|---|---|
| `scripts/jumpserver_api/jms_runtime.py` | 环境加载、组织上下文、客户端构建、公共 CLI 行为 | 所有正式入口共享 |
| `scripts/jumpserver_api/jms_query.py` | 资产、平台、节点、账号、账号模板、用户、用户组、组织、标签、网域查询 | 按对象域集中只读查询 |
| `scripts/jumpserver_api/jms_query.py` | 授权规则、ACL、RBAC 与资产授权用户查询 | 不承担授权写入 |
| `scripts/jumpserver_api/jms_query.py` | 审计列表、详情、terminal 会话、命令存储提示、能力分析 | 统一承接调查类意图 |
| `scripts/jumpserver_api/jms_diagnose.py` | 预检、连通性、对象解析、设置/许可证/报表/工单/存储查询、治理/巡检查询 | 统一承接治理和环境查询能力 |
| `scripts/jumpserver_api/jms_analytics.py` | 多接口聚合、统计、排行、巡检逻辑 | 避免在 CLI 入口里复制逻辑 |
| `scripts/jumpserver_api/jms_capabilities.py` | 能力单元元数据加载与导出 | 从 `references/metadata/capabilities.json` 读取每个能力的标准描述 |

## 能力域 -> 当前能力 -> 脚本实现 -> 触发描述

| 能力域 | 当前能力 / 子命令 | 脚本实现 | 触发描述 |
|---|---|---|---|
| 资产列表、精确查询 | `asset-list-query`、`jms_query.py object-list/object-get` | `jms_diagnose.py inspect`、`jms_query.py` | 适用于按名称、地址、节点、平台、启用状态查询资产清单或读取单个资产详情 |
| 账号列表、账号与资产关系 | `account-list-query`、`account-asset-bindings`、`jms_query.py object-list --resource account` | `jms_diagnose.py inspect`、`jms_query.py` | 适用于按账号名、资产、特权属性、模板线索查看资产账号与绑定关系 |
| 用户、用户组、组织查询 | `jms_query.py object-list/object-get` | `jms_query.py` | 适用于读取 JumpServer 用户、用户组和组织对象 |
| 账号模板、标签、网域查询 | `jms_query.py object-list/object-get` | `jms_query.py` | 适用于读取账号模板、标签、网域对象，以及配合治理查询回看原始对象 |
| 平台、节点、资产查询 | `jms_query.py object-list/object-get` | `jms_query.py` | 适用于平台、节点、资产对象的只读查询和详情回看 |
| 授权查询 | `jms_query.py permission-list/permission-get`、`asset-perm-users` | `jms_query.py` | 适用于查看资产授权规则、ACL、RBAC、主体范围、资源范围和资产当前授权用户 |
| 命令审计 | `command-record-query`、`high-risk-command-audit`、`jms_query.py audit-list --audit-type command` | `jms_query.py audit-analyze`、`jms_query.py` | 适用于按用户、资产、关键字、时间范围调查命令执行和高危命令 |
| 会话审计 | `session-record-query`、`session-behavior-statistics`、`user-session-analysis`、`asset-session-analysis`、`jms_query.py terminal-sessions` | `jms_query.py audit-analyze`、`jms_query.py` | 适用于查看登录会话、terminal 会话、在线会话、历史会话、会话时长、异常中断、用户/资产维度会话行为 |
| 文件传输审计 | `file-transfer-log-query`、`file-transfer-risk-audit` | `jms_query.py audit-analyze` | 适用于排查上传/下载记录、风险文件、异常传输方向和高频主体 |
| 登录安全调查 | `abnormal-hours-login-query`、`abnormal-source-ip-login-query`、`failed-login-statistics` | `jms_query.py audit-analyze` | 适用于异常时间段、异常来源 IP、失败登录排行调查 |
| 特权与共享账号治理 | `privileged-account-usage-audit`、`high-privilege-account-list`、`privileged-account-activity`、`shared-account-usage` | `jms_query.py audit-analyze`、`jms_diagnose.py inspect` | 适用于特权账号使用审计、高权限账号盘点、特权账号活跃情况和共享账号治理 |
| 资产活跃与热度分析 | `asset-activity-overview`、`asset-login-ranking`、`hot-assets-ranking`、`cold-assets-ranking`、`asset-login-trend` | `jms_diagnose.py inspect` | 适用于查看热门资产、冷门资产、最近活跃资产和登录趋势 |
| 账号活跃分析 | `account-activity-overview`、`long-time-unused-accounts`、`frequent-operation-user-ranking` | `jms_diagnose.py inspect`、`jms_query.py audit-analyze` | 适用于查看账号使用热度、长期未使用账号、高频操作用户和最近活跃线索 |
| 资产治理 | `uncategorized-assets-query`、`assets-without-valid-account-template`、`duplicate-asset-name-query`、`offline-disabled-assets-statistics`、`long-time-unlogged-assets`、`long-time-unused-assets`、`node-asset-distribution` | `jms_diagnose.py inspect` | 适用于资产分类治理、模板治理、离线禁用统计、未使用资产和节点分布分析 |
| 账号治理 | `account-list-query`、`expired-account-query`、`accounts-without-template`、`account-asset-bindings`、`account-template-list` | `jms_diagnose.py inspect` | 适用于账号清单查询、失效账号排查、未绑定模板账号治理、账号-资产绑定关系查看和模板清单查看 |
| 对象解析与访问分析 | `resolve`、`resolve-platform`、`user-assets`、`user-nodes`、`user-asset-access` | `jms_diagnose.py` | 适用于名称歧义消解、平台解析、用户有效访问范围分析 |
| 系统设置与配置巡检 | `system-settings-overview`、`security-policy-check`、`login-auth-config-check`、`mfa-config-check`、`auth-source-config-check`、`notification-config-check`、`ticket-approval-config-check`、`audit-retention-check`、`terminal-access-policy-check`、`settings-category`、`license-detail` | `jms_diagnose.py inspect`、`jms_diagnose.py` | 适用于查看系统总览、安全策略、认证源、MFA、通知、审批、审计保留、终端接入配置和许可证详情 |
| 工单、终端组件与存储查询 | `tickets`、`terminals`、`command-storages`、`replay-storages` | `jms_diagnose.py` | 适用于直接读取工单、终端组件、命令存储、录像存储原始记录 |
| 报表与账号自动化查询 | `reports`、`report-query`、`account-automation-overview` | `jms_diagnose.py`、`jms_diagnose.py inspect` | 适用于读取报表接口、dashboard 数据以及账号备份/改密/风险/检测任务概览 |
| 组织与授权关系统计 | `org-resource-overview`、`role-binding-overview`、`endpoint-inventory`、`endpoint-verify` | `jms_diagnose.py inspect`、`jms_diagnose.py` | 适用于组织资源盘点、节点数量、RBAC 绑定关系、核心端点 inventory 与按路径验证 |
| 可疑行为聚合调查 | `suspicious-operation-summary` | `jms_query.py audit-analyze` | 适用于跨命令、登录、会话、文件传输多接口汇总可疑行为 |

## 缺口清单

| 项目 | 当前状态 | 说明 |
|---|---|---|
| 对象创建、更新、删除、解锁 | 不提供 | 本仓库不提供对象写操作 |
| 授权追加、移除、删除 | 不提供 | 本仓库不承担权限写操作 |
| 资产账号失效状态统一查询 | 待确认 | inventory 未给出统一可依赖的失效字段语义；当前 `expired-account-query` 以 JumpServer 用户账号维度输出 |
| `/api/v1/perms/asset-permissions/` 在所有环境的可用性 | 待环境验证 | `permissions`、`user-assets`、`user-nodes`、`user-asset-access` 依赖该接口或其等价接口 |
| 设置项键名跨环境差异 | 已做降级处理 | 巡检能力统一保留原始键值，必要时提示人工复核 |
| “高风险资产” 的统一标签来源 | 待确认 | 当前以资产名称、地址、关键字过滤为主，不臆造平台未提供的风险标签字段 |

## README 一致性维护策略

- 保持当前 README 的章节骨架，不把它改写成开发设计文档。
- 使用场景与命令示例继续保持示例驱动写法。
- 把实现差异压缩到技术栈、目录说明和扩展维护小节，不让实现细节成为主叙事。
- 能力扩展通过 `references/capabilities.md` 和 `references/migration-map.md` 补充，不打断主 README 的使用者阅读路径。
- README 与 references 不保留 preview/confirm 写流程描述。

## SKILL / README / references 分工

| 文件 | 负责内容 | 不负责内容 |
|---|---|---|
| `SKILL.md` | 何时适用、如何路由、什么场景要停下、输出模板 | 细颗粒度 API 映射和实现细节 |
| `README.md` | 整体定位、目录结构、使用方式、常见场景、维护约定 | 每个能力的逐条元数据 |
| `references/*.md` | 分域规则、能力目录、映射关系、排障路径、验证结论 | 运行时公共实现细节 |
| `references/metadata/capabilities.json` + `jms_capabilities.py` | 能力单元的结构化事实定义与加载 | 面向使用者的叙述性教程 |

## 为什么当前结构更容易维护

- 入口少而稳定：固定为 3 个正式 CLI 入口。
- 公共逻辑集中：运行时、请求签名、组织选择不在多个脚本里复制。
- 查询能力模块化：统计类、审计类、巡检类都通过 handler + metadata 组合扩展。
- 文档与代码一一对应：`capability_id -> handler -> endpoint -> reference` 关系是显式的。
- 对 inventory 未确认的接口保持克制：统一标记“待确认”，不把猜测写进交付物。
- 只读对象域减少了重复 payload 构造、diff、确认和写后回读维护成本。
