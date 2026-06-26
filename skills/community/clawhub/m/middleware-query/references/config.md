# Configuration

## connections.json location

Default runtime path: `skills/middleware-query/scripts/connections.json`

Template file (safe to commit): `skills/middleware-query/scripts/connections.example.json`

First-time setup:

```bash
cp skills/middleware-query/scripts/connections.example.json \
   skills/middleware-query/scripts/connections.json
# then edit connections.json with real credentials
```

## Recommended format (middleware list + env/alias)

```json
{
  "redis": [
    {"env": "local", "alias": "main", "host": "127.0.0.1", "port": 6379, "username": "default", "password": "secret", "db": 0},
    {"env": "dev", "alias": "dev", "host": "10.0.0.2", "port": 6379, "username": "default", "password": "secret", "db": 0}
  ],
  "mongo": [
    {"env": "local", "alias": "main", "host": "127.0.0.1", "port": 27017, "username": "admin", "password": "secret", "database": "app_db", "authSource": "admin"}
  ],
  "mysql": [
    {"env": "local", "alias": "main", "host": "127.0.0.1", "port": 3306, "username": "root", "password": "secret", "database": "app_db"}
  ]
}
```

Use profile as `<middleware>.<env-or-alias>`:

- `redis.local` / `redis.main`
- `mysql.dev` / `mysql.main`
- `mongo.test` / `mongo.main`

The selector part (`<env-or-alias>`) matches either `env` or `alias`.

## Env vars

- MySQL: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
- Redis: `REDIS_HOST`, `REDIS_PORT`, `REDIS_USER`, `REDIS_PASSWORD`, `REDIS_DB`
- Mongo: `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_DATABASE`, `MONGO_AUTH_SOURCE`

CLI args override env vars, env vars override `connections.json`.

## Planner (v3)

- `OPENAI_API_KEY`: optional, enable LLM planner (`planner_llm.py`)
- `MW_PLANNER_MODEL`: optional, default `gpt-4o-mini`

Optional Python dependencies:

```bash
pip3 install openai jsonschema
```

If not installed/configured, planner falls back to rule-based router.
