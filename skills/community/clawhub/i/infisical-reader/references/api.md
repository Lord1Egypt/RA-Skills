# Infisical API Reference

## Authentication

### Login with Universal Auth

```
POST https://app.infisical.com/api/v1/auth/universal-auth/login
Content-Type: application/json

{"clientId": "...", "clientSecret": "***"}
```

Response:

```json
{"accessToken": "***", "expiresIn": 7200, "tokenType": "Bearer"}
```

## Projects

### List Projects

```
GET https://app.infisical.com/api/v1/workspace
Authorization: Bearer <token>
```

Response: `{"workspaces": [{"id": "...", "slug": "...", "name": "...", "environments": [{"slug": "prod"}, {"slug": "dev"}]}]}`

## Secrets

### List Secrets

```
GET https://app.infisical.com/api/v3/secrets/raw?workspaceId=<id>&environment=<env>&secretPath=/
Authorization: Bearer <token>
```

Required: `workspaceId` + `environment`
Optional: `secretPath` (default `/`), `recursive`, `expandSecretReferences`

### Get Single Secret

```
GET https://app.infisical.com/api/v3/secrets/raw/<secretName>?workspaceId=<id>&environment=<env>&secretPath=/
Authorization: Bearer <token>
```

### Response Format

```json
{
  "secrets": [
    {
      "secretKey": "OPENAI_API_KEY",
      "secretValue": "sk-...",
      "secretComment": "",
      "type": "shared",
      "workspace": "...",
      "environment": "prod",
      "secretPath": "/"
    }
  ]
}
```

## Common Errors

- `401 Invalid credentials` — wrong Client ID/Secret or identity locked
- `400 You must provide projectSlug or workspaceId` — missing required param
- `403 jwt must be provided` — token missing or expired
- `401 This identity auth method is temporarily locked` — too many failed attempts, wait or unlock in dashboard

## SDKs

Official SDKs: Node.js (`@infisical/sdk`), Python (`infisical`), Go, Ruby, Java, .NET

```javascript
import { InfisicalClient } from "@infisical/sdk";
const client = new InfisicalClient({ clientId: "...", clientSecret: "***" });
const secret = await client.getSecret("OPENAI_API_KEY");
```

```python
from infisical import InfisicalClient
client = InfisicalClient(client_id="...", client_secret="***")
secret = client.get_secret("OPENAI_API_KEY")
```
