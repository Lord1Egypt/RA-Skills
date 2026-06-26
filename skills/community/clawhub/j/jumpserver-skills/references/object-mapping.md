# Object Map

## 自然语言到对象映射

| 用户输入 | 推荐资源 | 常用命令 |
|---|---|---|
| 资产、主机、数据库、设备、云资产、Web 资产 | `asset` | `jms_assets.py list/get` |
| 节点、目录节点 | `node` | `jms_assets.py list/get` 或 `jms_diagnose.py resolve` |
| 平台、系统平台 | `platform` | `jms_assets.py list/get` 或 `resolve-platform` |
| 账号、系统账号 | `account` | `jms_assets.py list/get` |
| 用户 | `user` | `jms_assets.py list/get` |
| 用户组 | `user-group` | `jms_assets.py list/get` |
| 组织 | `organization` | `jms_assets.py list/get` 或 `select-org` |
| 授权、权限规则 | permission | `jms_permissions.py list/get` |
| 登录/操作/会话/命令日志 | audit | `jms_audit.py list/get` |

## 查询字段建议

| 场景 | 优先字段 |
|---|---|
| 用户 | `username`，其次 `name` |
| 账号 | `username` |
| 节点 | `value` |
| 平台 | 精确平台名或平台 ID |
| 权限 | `id` 最稳妥，列表时再配合 `limit` |
