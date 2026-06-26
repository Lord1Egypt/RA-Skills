# Examples

## One-command (v4)

```bash
python3 skills/middleware-query/scripts/nl_query.py \
  --text "查一下 redis 里 user:1001 的 hash" \
  --redis-profile redis.local
```

可选：保留生成的 plan

```bash
python3 skills/middleware-query/scripts/nl_query.py \
  --text "查mongo collection:orders 最近20条" \
  --keep-plan /tmp/mw-plan.json
```

## NL -> Plan -> Execute (v3, 手动分步)

```bash
python3 skills/middleware-query/scripts/planner_llm.py \
  --text "查一下 redis 里 user:1001 的 hash" \
  --out /tmp/mw-plan.json

python3 skills/middleware-query/scripts/planner_guard.py --plan /tmp/mw-plan.json
python3 skills/middleware-query/scripts/execute_plan.py --plan /tmp/mw-plan.json
```

> 未配置 OPENAI_API_KEY 时，`planner_llm.py` 会自动回退到 `router_nl.py` 规则路由。

## SQL

```bash
python3 skills/middleware-query/scripts/query_sql.py \
  --profile mysql_main \
  --sql "SELECT id, name FROM users WHERE created_at >= '2026-01-01' ORDER BY id DESC LIMIT 20"
```

## Redis

```bash
python3 skills/middleware-query/scripts/query_redis.py \
  --profile redis.local \
  --command scan --pattern "user:*" --count 100
```

```bash
python3 skills/middleware-query/scripts/query_redis.py \
  --profile redis_main \
  --command hgetall --key "user:1001"
```

## Mongo

```bash
python3 skills/middleware-query/scripts/query_mongo.py \
  --profile mongo_main \
  --collection users \
  --filter '{"status":"active"}' \
  --limit 50
```

```bash
python3 skills/middleware-query/scripts/query_mongo.py \
  --profile mongo_main \
  --collection orders \
  --pipeline '[{"$match":{"status":"paid"}},{"$group":{"_id":"$user_id","total":{"$sum":"$amount"}}}]' \
  --limit 20
```
