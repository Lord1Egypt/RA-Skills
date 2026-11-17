# API Tester Toolbox

## 何时使用

用 `scripts/toolbox/api_tester.py` 在写 n8n HTTP Request 节点前快速验证一个接口：方法、URL、headers、query、JSON body、raw body、timeout。它适合做轻量 Postman，不适合做压测、OAuth 浏览器授权或长期接口监控。

## 示例命令

```bash
python3 scripts/toolbox/api_tester.py \
  --method POST \
  --url "https://example.com/api/items" \
  --headers '{"Authorization":"Bearer token_here","Content-Type":"application/json"}' \
  --query '{"limit":10}' \
  --body-json '{"name":"demo"}' \
  --print-n8n-config
```

只检查参数、不发网络请求：

```bash
python3 scripts/toolbox/api_tester.py \
  --method GET \
  --url "https://example.com/api/items" \
  --query '{"q":"n8n"}' \
  --dry-run
```

从文件读取 JSON：

```bash
python3 scripts/toolbox/api_tester.py \
  --method POST \
  --url "https://example.com/webhook" \
  --headers @headers.json \
  --body-json @payload.json \
  --n8n-config-out /tmp/http-request-node.json
```

## 输出与 n8n 草稿

`--print-n8n-config` 或 `--n8n-config-out` 会生成 n8n `HTTP Request` 节点的 `parameters` 草稿。草稿会保留 method、url、headers、query、body 结构，但敏感值会被替换为 `<redacted>`，导入或手工复制到 n8n 前要改成 n8n credential、环境变量或表达式。

## 安全边界

- 默认会脱敏 key 名包含 `authorization`、`cookie`、`token`、`secret`、`password`、`api_key` 等字段的值。
- 脱敏是启发式保护，不保证能识别藏在普通字段里的密钥；不要把真实 token 放进要提交到仓库的命令或输出文件。
- `--dry-run` 不发请求，适合先给其他 agent 或用户审查请求形态。
- 脚本只使用 Python 标准库，不保存请求历史。
