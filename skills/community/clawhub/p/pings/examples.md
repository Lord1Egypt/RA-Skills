# 调用示例

将 `{BASE}` 换为 `https://wink.run`（本仓库与 CLI 约定）。

## HTTP

```http
GET {BASE}/api/pings/latest?lang=zh&limit=5
GET {BASE}/api/pings/latest?user_id=user%40example.com&lang=en&limit=10&freshness=24
```

## curl

```bash
curl -sS -G "{BASE}/api/pings/latest" \
  --data-urlencode "lang=zh" \
  --data-urlencode "limit=5"
```

```bash
curl -sS -G "{BASE}/api/pings/latest" \
  --data-urlencode "user_id=user@example.com" \
  --data-urlencode "lang=zh" \
  --data-urlencode "limit=10" \
  --data-urlencode "freshness=8"
```

## CLI（本仓库）

```bash
npx wink-pings --email you@example.com --freshness 4 --lang zh
npx wink-pings --lang en --json
```

完整参数见仓库根目录 `README.md` 或执行 `npx wink-pings --help`。
