# Configuration Options Reference

## Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `project_dir` | (required) | Target project directory |
| `--name` | (required) | Project name (used in configs and docs) |
| `--dev-port` | 8020 | Development server port |
| `--test-port` | 8010 | Testing server port |
| `--prod-port` | 8000 | Production server port |
| `--dev-user` | "" | Developer name (shown in startup message) |
| `--test-user` | "" | QA tester name (shown in startup message) |
| `--db-type` | sqlite | Database type: `sqlite` or `postgres` |
| `--app-module` | server.main:app | Uvicorn app module path |
| `--dev-db` | (auto) | Custom dev database URL |
| `--test-db` | (auto) | Custom test database URL |
| `--prod-db` | (auto) | Custom prod database URL |

## Generated Environment Variables

### Per-Environment Settings

| Variable | Dev | Test | Prod |
|----------|-----|------|------|
| `APP_ENV` | development | testing | production |
| `DEBUG` | True | True | False |
| `LOG_LEVEL` | DEBUG | INFO | WARNING |
| `CORS_ORIGINS` | ["*"] | ["*"] | restricted |
| `RATE_LIMIT_ENABLED` | False | True | True |

### Shared Settings (customizable per env)

| Variable | Description |
|----------|-------------|
| `HOST` | Bind address (default: 127.0.0.1) |
| `PORT` | Server port |
| `DATABASE_URL` | Database connection string |
| `STORAGE_TYPE` | File storage type (local) |
| `MEDIA_STORAGE_PATH` | Media upload directory |
| `JWT_SECRET` | JWT signing secret |
| `JWT_ALGORITHM` | JWT algorithm (HS256) |
| `JWT_EXPIRE_MINUTES` | Token expiry (1440 = 24h) |

## Database URL Formats

### SQLite (default)
```
sqlite+aiosqlite:///./data/{env}/{project}.db
```

### PostgreSQL
```
postgresql://user:pass@localhost:5432/{project}_{env}
```

## Security Checklist

### Production Environment
- [ ] Change `JWT_SECRET` to a strong random value
- [ ] Restrict `CORS_ORIGINS` to actual domains
- [ ] Enable `RATE_LIMIT_ENABLED=True`
- [ ] Set `DEBUG=False`
- [ ] Set `LOG_LEVEL=WARNING`
- [ ] Set up database backups for `data/prod/`

### Development Environment
- [ ] Never use production API keys
- [ ] Use isolated `data/dev/` database
- [ ] Development data is safe to delete/recreate

## Troubleshooting

### Port conflicts
```bash
# Find process using a port
lsof -i :<port>
# Kill it
kill -9 <PID>
```

### Database locked
```bash
# Stop all environments first
pkill -f "uvicorn"
# Then restart the one you need
./scripts/start-dev.sh
```

### Environment not loading
```bash
# Verify ENV_FILE is set
echo $ENV_FILE
# Should point to the correct .env.{env} file
```
