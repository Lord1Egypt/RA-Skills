# Troubleshooting

## 常见问题

| 错误或现象 | 原因 | 第一步 |
|---|---|---|
| `python3: command not found` | 没有可用的 Python 3 | 先安装或确认 `python3` |
| `No module named jms_client` | 当前解释器缺依赖 | `python3 -m pip install -r requirements.txt` |
| `JMS_API_URL is required.` | 没有地址配置 | 先 `config-status --json`，再用 `config-write --confirm` |
| `Provide either JMS_ACCESS_KEY_ID/... or JMS_USERNAME/...` | 鉴权配置不完整 | 用完整 payload 重跑 `config-write --confirm` |
| `This action requires --confirm after the change preview is reviewed.` | 环境写入少了确认 | 给 `config-write` 或 `select-org` 补 `--confirm` |
| `selection_required=true` | 当前没有 `JMS_ORG_ID` | 先 `select-org`，再 `select-org --confirm` |
| `audit-type=command requires ... command_storage_id` | 命令审计缺必需参数 | 给 `--filters` 补 `command_storage_id` |
| 找到多个同名对象 | 名称不唯一 | 改用 `get --id` 或更精确过滤 |
| 用户要求写业务对象 | 当前 skill 仍只读 | 直接说明不支持业务写操作 |

## 最小排查顺序

```text
检查 Python 3
  -> 检查依赖
  -> config-status --json
  -> config-write --confirm（如需）
  -> ping
  -> select-org --confirm（如需）
  -> resolve / list / get
  -> 如需调查再查 audit
```
