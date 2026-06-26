# 资产、用户与账号

## 快速概览

- 开始前先到 [runtime.md](runtime.md) 判断本次是“首次全量校验”还是“后续轻量校验”。
- 主入口：`python3 scripts/jumpserver_api/jms_query.py <subcommand> ...`
- 组织对象也走这个入口：`--resource organization`
- 这个入口只提供查询：`object-list` 与 `object-get`
- 所有列表型读取入口默认自动翻页拉全量；只有在 filters 里显式传 `limit` / `offset` 时才按分页结果返回。

## 子命令与资源

### 子命令表

| 子命令 | 用途 | 风险 |
|---|---|---|
| `object-list` | 列出对象或按条件筛选 | 低 |
| `object-get` | 读取单个对象详情 | 低 |

### 资源表

| 资源 | 说明 | 常见定位字段 |
|---|---|---|
| `asset` | 主机、数据库、设备、云、Web 资产 | `id`、`name`、`address` |
| `node` | 资产树节点 | `id`、`value` |
| `platform` | 平台模板 | `id`、`name` |
| `account` | 资产账号 | `id`、`username` |
| `account-template` | 账号模板 | `id`、`name` |
| `user` | JumpServer 用户 | `id`、`username` |
| `user-group` | 用户组 | `id`、`name` |
| `organization` | JumpServer 组织 | `id`、`name` |
| `label` | 标签 | `id`、`name` |
| `zone` | 网域 | `id`、`name` |

### `asset --kind` 表

| `--kind` | 实际列表路径 |
|---|---|
| 省略 / `generic` | `/api/v1/assets/assets/` |
| `host` | `/api/v1/assets/hosts/` |
| `database` | `/api/v1/assets/databases/` |
| `device` | `/api/v1/assets/devices/` |
| `cloud` | `/api/v1/assets/clouds/` |
| `web` / `website` | `/api/v1/assets/webs/` |
| `custom` / `customs` | `/api/v1/assets/customs/` |
| `directory` / `directories` | `/api/v1/assets/directories/` |

## 关键约束

| 条件 | 规则 |
|---|---|
| `--kind` | 只适用于 `--resource asset` |
| 资产详情读取 | `object-get --resource asset` 统一走通用资产详情路径 |
| 平台 ID | 不要硬编码 `Linux -> 1`、`MySQL -> 17` 这类映射 |
| 平台条件不确定 | 先 `resolve-platform`，再回到 `object-list/object-get` |
| `account` 名称查询 | 实际常用筛选字段是 `username` |
| 名称不唯一 | 先用 `resolve` 或更精确 filters 缩小范围 |
| 资产 `address` 可能共享 | `object-list` 会返回 `summary.ambiguous=true` 与候选摘要，需再用 `id/name/platform` 消歧 |
| 节点 `full_value` 过滤不稳定 | CLI 会做一次本地 exact-first 收敛；若仍多条，改用 `id` |
| 业务写请求 | 本入口不提供创建、更新、删除、解锁等动作 |

## 高频命令

精确查询用户：

```bash
python3 scripts/jumpserver_api/jms_query.py object-list --resource user --filters '{"username":"openclaw"}'
```

查询某类资产：

```bash
python3 scripts/jumpserver_api/jms_query.py object-list --resource asset --kind host --filters '{"name":"prod","is_active":true}'
python3 scripts/jumpserver_api/jms_query.py object-list --resource asset --kind database --filters '{"address":"10.0.0.12"}'
```

读取对象详情：

```bash
python3 scripts/jumpserver_api/jms_query.py object-get --resource asset --id <asset-id>
python3 scripts/jumpserver_api/jms_query.py object-get --resource platform --id <platform-id>
python3 scripts/jumpserver_api/jms_query.py object-get --resource user --id <user-id>
```

读取组织与用户组：

```bash
python3 scripts/jumpserver_api/jms_query.py object-list --resource organization --filters '{"name":"Default"}'
python3 scripts/jumpserver_api/jms_query.py object-list --resource user-group --filters '{"name":"运维组"}'
```
