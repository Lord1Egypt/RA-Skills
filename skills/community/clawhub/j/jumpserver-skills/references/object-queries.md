# Assets

## 只读范围

| 命令 | 作用 |
|---|---|
| `jms_assets.py list` | 查询资产、节点、平台、账号、用户、用户组、组织列表 |
| `jms_assets.py get` | 按 ID 查询单个对象详情 |
| `jms_diagnose.py resolve` | 用名称或 ID 做只读解析 |
| `jms_diagnose.py resolve-platform` | 解析平台名或平台 ID |

## 环境要求

- 先 `config-status --json`
- 缺配置时用 `config-write --confirm`
- 缺组织时用 `select-org --confirm`

## 常用命令

```bash
python3 scripts/jms_assets.py list --resource user --filters '{"username":"demo-user"}'
python3 scripts/jms_assets.py get --resource user --id <user-id>
python3 scripts/jms_assets.py list --resource node --filters '{"value":"demo-node"}'
python3 scripts/jms_diagnose.py resolve-platform --value Linux
```

## 停止条件

| 场景 | 正确处理 |
|---|---|
| 同名对象命中多个结果 | 改用 `get --id` 或更精确过滤 |
| 当前没有组织上下文 | 先 `select-org --confirm` |
| 用户要求创建/更新/删除 | 明确说明业务动作只保留查询能力 |
