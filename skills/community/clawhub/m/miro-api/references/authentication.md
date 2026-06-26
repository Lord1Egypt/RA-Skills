# Miro REST API - Authentication Guide

## Authentication Methods

Miro supports two primary authentication approaches:

1. **OAuth 2.0** (Recommended for production applications)
2. **Personal Access Tokens** (Recommended for development/automation)

---

## Personal Access Tokens (PAT)

### When to Use
- Internal automation scripts
- Development and testing
- CLI tools
- Server-to-server communication
- Webhooks and cron jobs

### Creating a PAT

1. **Go to App Settings:**
   - Visit https://miro.com/app/settings/user-profile/apps
   - Or: Click Profile → Settings → Apps & Integrations

2. **Create Personal Access Token:**
   - Click "Create new personal access token"
   - Enter a descriptive name
   - Select required scopes (see below)
   - Click "Create"

3. **Copy the Token:**
   - Token is displayed only once
   - Copy immediately and store securely
   - Never share or commit to version control

### Token Format
```
miro_pat_<random-alphanumeric-string>
```

### Using PAT in Requests

**cURL:**
```bash
curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer YOUR_PAT"
```

**HTTP Header:**
```
Authorization: Bearer miro_pat_abc123xyz...
Content-Type: application/json
```

**Environment Variable (Recommended):**
```bash
export MIRO_TOKEN="miro_pat_abc123xyz..."

curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer $MIRO_TOKEN"
```

### Token Rotation
- No automatic expiration for PATs
- Rotate regularly (quarterly recommended)
- Delete old tokens immediately
- Revoke compromised tokens

### Scopes for PATs

Scopes define what your token can do:

| Scope | Permission |
|-------|-----------|
| `boards:read` | Read board metadata |
| `boards:write` | Create, update, delete boards |
| `items:read` | Read board items |
| `items:write` | Create, update, delete items |
| `comments:read` | Read comments |
| `comments:write` | Create, update, delete comments |
| `users:read` | Read team members |
| `users:write` | Invite, remove team members |
| `webhooks:read` | Read webhooks |
| `webhooks:write` | Create, update, delete webhooks |
| `team:read` | Read team information |
| `files:write` | Upload files/images |

**Example: Minimal Scopes**
For a read-only board inspector, request only:
- `boards:read`
- `items:read`

---

## OAuth 2.0

### When to Use
- Web applications
- User-facing integrations
- Third-party applications
- SaaS integrations
- Multi-user scenarios

### OAuth 2.0 Flow

#### 1. Register Your Application
1. Visit https://miro.com/app/settings/user-profile/apps
2. Click "Create new app"
3. Enter app name and description
4. Set **Redirect URI** (callback URL):
   ```
   https://yourapp.com/auth/miro/callback
   ```
5. Save and note your **Client ID** and **Client Secret**

#### 2. Redirect User to Authorization
Build authorization URL:
```
https://miro.com/oauth/authorize
  ?response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/auth/miro/callback
  &state=random-state-string
  &scope=boards:read items:read comments:read
```

**Example (JavaScript):**
```javascript
const clientId = "YOUR_CLIENT_ID";
const redirectUri = encodeURIComponent("https://yourapp.com/auth/miro/callback");
const scopes = encodeURIComponent("boards:read items:read");
const state = Math.random().toString(36).substring(7);

const authUrl = `https://miro.com/oauth/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&state=${state}&scope=${scopes}`;

window.location.href = authUrl;
```

#### 3. User Authorizes Your App
- User sees Miro authorization screen
- Clicks "Allow" or "Deny"
- Redirected back to your callback URI with `code`

#### 4. Exchange Code for Access Token
Your backend exchanges the code for tokens:

**Request:**
```http
POST https://miro.com/oauth/token
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&grant_type=authorization_code
&code=AUTHORIZATION_CODE
&redirect_uri=https://yourapp.com/auth/miro/callback
```

**Response:**
```json
{
  "access_token": "miro_oa2_...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "miro_oa2_refresh_...",
  "scope": "boards:read items:read comments:read"
}
```

#### 5. Use Access Token
```bash
curl -X GET https://api.miro.com/v2/boards \
  -H "Authorization: Bearer miro_oa2_..."
```

#### 6. Refresh Token When Expired
Access tokens expire after 3600 seconds (1 hour).

**Refresh Request:**
```http
POST https://miro.com/oauth/token
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID
&client_secret=YOUR_CLIENT_SECRET
&grant_type=refresh_token
&refresh_token=miro_oa2_refresh_...
```

**Response:**
```json
{
  "access_token": "miro_oa2_new_token",
  "expires_in": 3600
}
```

### OAuth Best Practices

1. **Secure Storage**
   - Store tokens in encrypted database
   - Never log tokens
   - Never embed in client-side code

2. **Redirect URI Validation**
   - Always verify redirect URI matches registered URL
   - Use HTTPS in production
   - Validate state parameter to prevent CSRF

3. **Token Management**
   - Implement token refresh before expiration
   - Handle 401 responses with token refresh
   - Delete tokens when user revokes access

4. **Scopes**
   - Request minimal required scopes
   - Inform user what data you're accessing
   - Document why each scope is needed

5. **Error Handling**
   - Handle user denial gracefully
   - Provide helpful error messages
   - Implement retry logic for network errors

### OAuth Endpoints

| Endpoint | Purpose |
|----------|---------|
| `https://miro.com/oauth/authorize` | Authorization endpoint |
| `https://miro.com/oauth/token` | Token endpoint |

---

## Security Considerations

### Secret Management

**DO:**
- Store tokens in environment variables
- Use secure credential management (HashiCorp Vault, AWS Secrets Manager)
- Rotate tokens regularly
- Use encrypted connections (HTTPS)
- Implement token expiration

**DON'T:**
- Commit tokens to Git
- Store tokens in config files
- Share tokens via email/chat
- Log tokens to console
- Use weak random number generators for state

### Network Security
- Always use HTTPS (TLS 1.2+)
- Validate SSL certificates
- Implement request signing if needed
- Monitor for suspicious API usage

### Rate Limiting Protection
- Implement exponential backoff
- Cache responses locally
- Batch requests when possible
- Monitor X-RateLimit headers

### Webhook Security
- Verify webhook signatures
- Use HTTPS for webhook endpoints
- Validate request source
- Implement request timeouts

---

## Troubleshooting

### 401 Unauthorized
**Cause:** Invalid or missing token
**Solution:**
- Check token format
- Verify token hasn't expired
- Refresh OAuth token if using OAuth
- Check Authorization header spelling

### 403 Forbidden
**Cause:** Insufficient permissions
**Solution:**
- Add required scopes to token
- Verify user has board access
- Check if board/item was deleted

### Invalid Scope
**Cause:** Requested scope not available
**Solution:**
- Check scope spelling
- Verify scope is supported
- See scope list above

### Token Expired (OAuth)
**Cause:** Access token older than 1 hour
**Solution:**
- Refresh token using refresh token
- Implement automatic refresh before expiration

