# Runbook — Your Infrastructure Map

> ⚠️ **This is a template.** If you see `<!--` placeholder comments below, this file has not been filled in yet. Before using this skill in a real incident, populate this file with your actual services, endpoints, dashboards, and on-call contacts. Tell the user to fill it in now if it's still empty.

Fill this in with your services, endpoints, and tools. The triage framework references
this during Step 4 (Investigate) to know where to look.

## Services

<!-- List your services and their key details -->

| Service | Health Endpoint | Dashboard | Log Location |
|---------|----------------|-----------|-------------|
| <!-- api --> | <!-- https://api.example.com/health --> | <!-- Datadog/Grafana link --> | <!-- CloudWatch log group or log tool --> |
| <!-- web --> | <!-- https://app.example.com --> | <!-- link --> | <!-- link --> |
| <!-- worker --> | <!-- N/A (background) --> | <!-- link --> | <!-- link --> |

## Environments

| Environment | URL | Account/Project | Region |
|-------------|-----|-----------------|--------|
| Production | <!-- https://app.example.com --> | <!-- prod account --> | <!-- us-east-1 --> |
| Staging | <!-- https://staging.example.com --> | <!-- staging account --> | <!-- us-east-1 --> |

## Key Dependencies

<!-- External services your system depends on -->

| Dependency | Status Page | What Breaks If Down |
|-----------|------------|---------------------|
| <!-- Database (RDS/Cloud SQL) --> | <!-- AWS Health Dashboard --> | <!-- All API calls --> |
| <!-- Redis/Cache --> | <!-- link --> | <!-- Session management, rate limiting --> |
| <!-- Third-party API --> | <!-- status.example.com --> | <!-- Feature X --> |

## Deployment

| Component | CI/CD | Deploy Command | Rollback |
|-----------|-------|---------------|----------|
| <!-- API --> | <!-- GitHub Actions --> | <!-- Merges to main auto-deploy --> | <!-- Revert PR + merge --> |
| <!-- Web --> | <!-- GitHub Actions --> | <!-- Same --> | <!-- Same --> |

## On-Call

<!-- Fill in your rotation -->

| Role | Contact | Schedule |
|------|---------|----------|
| Primary | <!-- @person or phone --> | <!-- rotation link --> |
| Secondary | <!-- @person --> | <!-- rotation link --> |
| Engineering Lead | <!-- @person --> | <!-- N/A --> |

## Common Fixes

<!-- Quick fixes for recurring issues -->

| Symptom | Likely Cause | Quick Fix |
|---------|-------------|-----------|
| <!-- 502 errors --> | <!-- Container OOM --> | <!-- Scale up task memory, check for memory leak --> |
| <!-- Slow queries --> | <!-- Missing index --> | <!-- Check pg_stat_statements, add index --> |
| <!-- Connection refused --> | <!-- Security group change --> | <!-- Check recent Terraform applies --> |

## Customize

Delete the HTML comments and fill in your actual infrastructure.
Add or remove sections as needed — this is your team's reference.