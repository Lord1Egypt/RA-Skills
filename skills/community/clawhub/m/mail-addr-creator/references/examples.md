# Example Prompts

## Natural Language

- `Create the mailbox t2@suilong.online`
- `Create a mailbox with name=t2, domain=suilong.online, enablePrefix=true`
- `Batch-create alice,bob,charlie on suilong.online`
- `Use the backend API to create 10 mailboxes in my Cloudflare temp mail system`

## Script Examples

Single address:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --name t2 `
  --domain suilong.online
```

Batch from CLI:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names alice,bob,charlie `
  --domain suilong.online `
  --enable-prefix true
```

Batch from file:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names-file .\names.txt `
  --domain suilong.online
```

Batch to CSV:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names alice,bob,charlie `
  --domain suilong.online `
  --output-format csv `
  --output-file .\created-addresses.csv
```

## Example Success Output

```json
{
  "status": "created",
  "address": "t2@suilong.online",
  "jwt": "xxx",
  "password": null,
  "error": null
}
```

## Example Batch Output

```json
{
  "summary": {
    "requested": 3,
    "created": 2,
    "already_exists": 1,
    "failed": 0
  },
  "results": [
    {
      "name": "alice",
      "status": "created",
      "address": "alice@suilong.online",
      "jwt": "xxx",
      "password": null,
      "error": null
    },
    {
      "name": "bob",
      "status": "already_exists",
      "address": "bob@suilong.online",
      "jwt": null,
      "password": null,
      "error": "address already exists"
    }
  ]
}
```
