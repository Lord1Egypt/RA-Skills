# Locker Secrets Manager — CLI Reference

## Authentication

The CLI authenticates via environment variables or interactive login.

### Environment Variables (Preferred for Agents)

```bash
export LOCKER_ACCESS_KEY_ID="ak_xxxxxxxxxxxxxxxx"
export LOCKER_SECRET_ACCESS_KEY="sk_xxxxxxxxxxxxxxxx"
```

Access keys are created in the Locker dashboard:
`Project Settings → Access Keys → Create New`

### Interactive Login

```bash
locker login
```

Not suitable for agents — use environment variables.

---

## Secret Commands

### List All Secrets

```bash
locker secret list
```

Output: One key per line, or a formatted table depending on CLI version.

Export all secrets to .env file:
```bash
locker secret list > .env
```

### Get a Secret

```bash
locker secret get --name=SECRET_KEY
```

Returns only the value (stdout), suitable for piping:
```bash
locker secret get --name=MYSQL_PASSWORD | mysql -h db.example.com -u admin -p
```

### Create a Secret

```bash
# With explicit value
locker secret create --key=MY_SECRET --value=my-secret-value

# With random generated value
locker secret create --key=SESSION_TOKEN --random-value
```

### Set / Export as System Variables

```bash
# Loads all secrets as environment variables for the next command
locker secret set && node app.js
```

This exports secrets as system variables, making them available to the spawned process.

### Delete a Secret

```bash
locker secret delete --name=SECRET_KEY
```

---

## Common Patterns

### Use in CI/CD Pipeline

```bash
# In GitHub Actions, GitLab CI, etc.
export LOCKER_ACCESS_KEY_ID=${{ secrets.LOCKER_AK }}
export LOCKER_SECRET_ACCESS_KEY=${{ secrets.LOCKER_SK }}

# Get database URL for migration
DATABASE_URL=$(locker secret get --name=DATABASE_URL)
npx prisma migrate deploy
```

### Use in Docker

```dockerfile
# At runtime, not build time!
CMD ["sh", "-c", "locker secret set && node server.js"]
```

### Use in Cron Jobs

```bash
# crontab entry
0 */6 * * * LOCKER_ACCESS_KEY_ID=ak_xxx LOCKER_SECRET_ACCESS_KEY=sk_xxx locker secret get --name=API_TOKEN | xargs -I{} curl -H "Authorization: Bearer {}" https://api.example.com/sync
```

---

## Error Messages

| Message | Meaning |
|---------|---------|
| `Authentication failed` | Invalid access key pair |
| `Secret not found` | Key doesn't exist in the project |
| `Permission denied` | Access key doesn't have required permissions |
| `Rate limit exceeded` | Too many API calls, wait and retry |
| `Network error` | Can't reach Locker API |

---

## Installation

```bash
# macOS / Linux
curl -fsSL https://locker.io/secrets/install.sh | bash

# Verify
locker --version

# Update
locker update
```

### System Requirements
- Linux (x64, arm64) or macOS
- Network access to api.locker.io
- Node.js NOT required (CLI is standalone binary)
