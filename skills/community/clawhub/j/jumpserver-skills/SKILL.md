---
name: jumpserver-skills
description: Use for JumpServer V4 preflight, `.env.local` initialization, org selection, and read-only asset, permission, audit, and access queries through the bundled `jms_*.py` CLIs. Not for business mutations.
---

# JumpServer Skills

JumpServer 查询型 skill：允许环境初始化写入（`.env.local` 与 `JMS_ORG_ID`），但不执行业务对象或权限的创建、更新、删除、追加或移除。

## Input / Output / 输入输出

| 类型 | 常见输入 | 返回 |
|---|---|---|
| 环境初始化 | `JMS_API_URL`、鉴权信息、可选 `org-id` | 配置完整性、`.env.local` 写入结果、连通性、组织写入结果 |
| 对象查询 | `resource`、`id`、`name`、`filters` | 列表、详情、解析结果 |
| 权限与审计 | `filters`、`audit-type`、时间范围、`command_storage_id` | 权限详情、审计详情、最近活动 |
| 访问分析 | `username`、可选 `asset-name` | 用户可访问资产/节点、单资产访问视图 |

## Route / 路由流程

```text
config-status --json
  -> complete=false ? collect env info -> config-write --confirm
  -> ping
  -> org missing/inaccessible ? select-org [--org-id] -> select-org --confirm
  -> read-only query
```

- 仅当可访问组织集合恰好是 `{0002}` 或 `{0002,0004}` 时，才允许自动写入 `0002`。

## Capability Matrix / 能力矩阵

| Intent | Must Use | Precheck | Output | Stop If |
|---|---|---|---|---|
| 初始化环境 | `jms_diagnose.py config-status/config-write/ping/select-org` | 无 | 配置状态、`.env.local` 写入结果、连通性、组织持久化结果 | 地址或鉴权缺失、地址不可达、组织不可访问 |
| 查资产与对象 | `jms_assets.py list/get`、`jms_diagnose.py resolve/resolve-platform` | `config-status --json` -> 必要时 `config-write --confirm` -> `ping` -> 必要时 `select-org --confirm` | 资产类列表、详情、对象解析结果 | 名称不唯一、对象不清楚、组织未准备好 |
| 查权限规则 | `jms_permissions.py list/get` | `config-status --json` -> 必要时 `config-write --confirm` -> `ping` -> 必要时 `select-org --confirm` | 权限列表、权限详情 | 组织未准备好 |
| 查审计记录 | `jms_audit.py list/get` | `config-status --json` -> 必要时 `config-write --confirm` -> `ping` -> 必要时 `select-org --confirm` | 登录、操作、会话、命令审计 | `audit-type=command` 缺 `command_storage_id` |
| 做访问分析 | `jms_diagnose.py user-assets/user-nodes/user-asset-access/recent-audit` | `config-status --json` -> 必要时 `config-write --confirm` -> `ping` -> 必要时 `select-org --confirm` | 用户可访问资产/节点、单资产访问、最近审计 | 用户不存在、候选过多、组织未准备好 |

## Core Rules / 核心规则

| Rule | Required Behavior |
|---|---|
| 预检顺序 | `config-status --json -> config-write --confirm（如需） -> ping -> select-org --confirm（如需） -> read-only query` |
| 环境写入 | 允许通过 `config-write --confirm` 生成或更新 `.env.local` |
| 组织写入 | 允许通过 `select-org --confirm` 持久化 `JMS_ORG_ID` |
| 保留组织特判 | 可访问组织集合仅在 `{0002}` 或 `{0002,0004}` 时才自动写入 `0002` |
| 范围边界 | 把这个 skill 当作查询型 skill，而不是通用运维执行器 |
| 审计默认窗口 | `date_from/date_to` 省略时默认最近 7 天 |
| 命令审计 | `audit-type=command` 时必须提供 `command_storage_id` |
| 非支持动作 | 遇到 create/update/delete/append/remove/unblock 时直接说明“业务动作只保留查询” |

## Canonical Commands / 命令骨架

配置检查与写入：

```bash
python3 scripts/jms_diagnose.py config-status --json
python3 scripts/jms_diagnose.py config-write --payload '{"JMS_API_URL":"https://jump.example.com","JMS_ACCESS_KEY_ID":"<ak>","JMS_ACCESS_KEY_SECRET":"<sk>","JMS_VERSION":"4"}' --confirm
python3 scripts/jms_diagnose.py ping
```

组织选择：

```bash
python3 scripts/jms_diagnose.py select-org
python3 scripts/jms_diagnose.py select-org --org-id <org-id>
python3 scripts/jms_diagnose.py select-org --org-id <org-id> --confirm
```

对象查询：

```bash
python3 scripts/jms_assets.py list --resource user --filters '{"username":"openclaw"}'
python3 scripts/jms_assets.py get --resource asset --id <asset-id>
python3 scripts/jms_diagnose.py resolve --resource node --name demo-node
python3 scripts/jms_diagnose.py resolve-platform --value Linux
```

权限与审计查询：

```bash
python3 scripts/jms_permissions.py list --filters '{"limit":20}'
python3 scripts/jms_permissions.py get --id <permission-id>
python3 scripts/jms_audit.py list --audit-type operate --filters '{"limit":30}'
python3 scripts/jms_audit.py get --audit-type command --id <command-id> --filters '{"command_storage_id":"<command-storage-id>"}'
```

## Success Criteria / 成功标准

- 先完成或明确阻塞在 `config-status -> ping -> select-org` 预检链路上，不跳步。
- 配置缺失时，能按字段收集用户回复并在确认后调用 `config-write --confirm`。
- 组织缺失时，能先返回候选组织，再在确认后调用 `select-org --confirm`。
- 查询请求走正式 `jms_*.py` 入口，返回结果或明确说明阻塞原因。
- 对业务写操作直接拒绝，不绕过正式入口另写临时 SDK/HTTP 脚本。

## Not For / 不适用

- 不适用于资产、平台、节点、账号、用户、用户组、组织、权限的创建、更新、删除。
- 不适用于追加关系、移除关系、解锁用户、改密、批量修改。
- 不适用于临时 SDK/HTTP 脚本绕过正式入口。
