---
name: modelslab-account-management
description: Manage ModelsLab accounts programmatically — signup, login, token management, profile updates, API key CRUD, and team member management. Uses the Agent Control Plane API with bearer token auth.
---

# ModelsLab Account Management

Manage the full ModelsLab account lifecycle via the Agent Control Plane API — authentication, tokens, profile, API keys, and teams.

## When to Use This Skill

- Sign up or log in to ModelsLab programmatically
- Create and manage API keys for generation endpoints
- Update user profile, password, or social links
- Manage access tokens (list, revoke, switch team accounts)
- Invite, update, or remove team members
- Build agent workflows that need account bootstrapping

## Authentication

The Agent Control Plane uses **bearer tokens** (not API keys). Some endpoints (signup, login, forgot-password) work without a token.

```
Base URL: https://modelslab.com/api/agents/v1
Authorization: Bearer <agent_access_token>
```

## Auth: Signup & Login

### Sign Up

```python
import requests

def signup(email, password, name=None):
    """Create a new ModelsLab account."""
    response = requests.post(
        "https://modelslab.com/api/agents/v1/auth/signup",
        json={
            "email": email,
            "password": password,
            "name": name or ""
        }
    )
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])
    return data["data"]  # Contains access_token

# Usage
result = signup("agent@example.com", "securepass123", "My Agent")
token = result["access_token"]
print(f"Signed up! Token: {token}")
```

### Log In

```python
def login(email, password, token_expiry="1_month"):
    """Log in and get a bearer token.

    Args:
        token_expiry: "1_week", "1_month" (default), "3_months", "never"
    """
    response = requests.post(
        "https://modelslab.com/api/agents/v1/auth/login",
        json={
            "email": email,
            "password": password,
            "device_name": "my-agent",
            "token_expiry": token_expiry
        }
    )
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])
    return data["data"]["access_token"]

# Usage
token = login("agent@example.com", "securepass123")
```

### Logout

```python
def logout(token):
    """Revoke current token."""
    requests.post(
        "https://modelslab.com/api/agents/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )

def logout_all(token):
    """Revoke all tokens for this account."""
    requests.post(
        "https://modelslab.com/api/agents/v1/auth/logout-all",
        headers={"Authorization": f"Bearer {token}"}
    )
```

### Verify Email (Headless)

After signup, the user receives a `verification_code` via email. Verify without a browser:

```python
def verify_email(verification_code):
    """Verify email with the code from the verification email.

    Returns an access_token and api_key — no browser required.
    """
    response = requests.post(
        "https://modelslab.com/api/agents/v1/auth/verify-email",
        json={"verification_code": verification_code}
    )
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])
    return data["data"]

# Usage — complete headless signup flow
result = verify_email("the_code_from_email")
token = result["access_token"]
api_key = result["api_key"]
print(f"Verified! Token: {token}, API Key: {api_key}")
```

### Refresh Token

Rotate the current bearer token without re-authenticating:

```python
def refresh_token(token, token_expiry="1_month"):
    """Refresh/rotate the current access token.

    The old token is revoked and a new one is issued.

    Args:
        token_expiry: "1_week", "1_month" (default), "3_months", "never"
    """
    response = requests.post(
        "https://modelslab.com/api/agents/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"},
        json={"token_expiry": token_expiry}
    )
    data = response.json()
    if "error" in data:
        raise Exception(data["error"])
    return data["data"]["access_token"]

# Usage — rotate token before it expires
new_token = refresh_token(old_token, token_expiry="1_month")
```

### Password Reset

```python
def forgot_password(email):
    """Request a password reset email."""
    requests.post(
        "https://modelslab.com/api/agents/v1/auth/forgot-password",
        json={"email": email}
    )

def reset_password(email, token, new_password):
    """Reset password using the reset token from email."""
    requests.post(
        "https://modelslab.com/api/agents/v1/auth/reset-password",
        json={
            "email": email,
            "token": token,
            "password": new_password,
            "password_confirmation": new_password
        }
    )
```

## Token Management

```python
def make_headers(token):
    return {"Authorization": f"Bearer {token}"}

def list_tokens(token):
    """List all active tokens."""
    resp = requests.get(
        "https://modelslab.com/api/agents/v1/auth/tokens",
        headers=make_headers(token)
    )
    return resp.json()["data"]

def revoke_token(token, token_id):
    """Revoke a specific token by ID."""
    requests.delete(
        f"https://modelslab.com/api/agents/v1/auth/tokens/{token_id}",
        headers=make_headers(token)
    )

def revoke_other_tokens(token):
    """Revoke all tokens except the current one."""
    requests.post(
        "https://modelslab.com/api/agents/v1/auth/tokens/revoke-others",
        headers=make_headers(token)
    )

def switch_account(token, team_username):
    """Switch to a team account context. Returns new token."""
    resp = requests.post(
        "https://modelslab.com/api/agents/v1/auth/switch-account",
        headers=make_headers(token),
        json={"account_username": team_username}
    )
    return resp.json()["data"]["access_token"]
```

## Profile Management

### Get Profile

```python
def get_profile(token):
    """Get the authenticated user's profile."""
    resp = requests.get(
        "https://modelslab.com/api/agents/v1/me",
        headers=make_headers(token)
    )
    return resp.json()["data"]

# Usage
profile = get_profile(token)
print(f"Name: {profile['name']}, Email: {profile['email']}")
print(f"Wallet: ${profile.get('wallet_balance', 0)}")
```

### Update Profile

```python
def update_profile(token, name=None, username=None, about_me=None):
    """Update profile fields."""
    payload = {}
    if name: payload["name"] = name
    if username: payload["username"] = username
    if about_me: payload["about_me"] = about_me

    resp = requests.patch(
        "https://modelslab.com/api/agents/v1/me",
        headers=make_headers(token),
        json=payload
    )
    return resp.json()["data"]

def update_password(token, current_password, new_password):
    """Change account password."""
    requests.patch(
        "https://modelslab.com/api/agents/v1/me/password",
        headers=make_headers(token),
        json={
            "current_password": current_password,
            "password": new_password,
            "password_confirmation": new_password
        }
    )

def update_socials(token, github=None, twitter=None, discord=None):
    """Update social media links."""
    payload = {}
    if github: payload["github"] = github
    if twitter: payload["twitter"] = twitter
    if discord: payload["discord"] = discord

    requests.patch(
        "https://modelslab.com/api/agents/v1/me/socials",
        headers=make_headers(token),
        json=payload
    )

def update_preferences(token, nsfw_content=None, wallet_notification_enabled=None):
    """Update account preferences."""
    payload = {}
    if nsfw_content is not None: payload["nsfw_content"] = nsfw_content
    if wallet_notification_enabled is not None:
        payload["wallet_notification_enabled"] = wallet_notification_enabled

    requests.patch(
        "https://modelslab.com/api/agents/v1/me/preferences",
        headers=make_headers(token),
        json=payload
    )
```

## API Key Management

API keys are used for generation endpoints (`/api/v6`, `/api/v7`, `/api/v8`).

### List API Keys

```python
def list_api_keys(token):
    """List all API keys."""
    resp = requests.get(
        "https://modelslab.com/api/agents/v1/api-keys",
        headers=make_headers(token)
    )
    return resp.json()["data"]
```

### Create API Key

```python
def create_api_key(token, name, notes=None):
    """Create a new API key for generation endpoints.

    Returns the full key — store it securely, it won't be shown again.
    """
    payload = {"name": name}
    if notes: payload["notes"] = notes

    resp = requests.post(
        "https://modelslab.com/api/agents/v1/api-keys",
        headers=make_headers(token),
        json=payload
    )
    return resp.json()["data"]

# Usage
key_data = create_api_key(token, "production-key", notes="Used by CI/CD")
api_key = key_data["key"]
print(f"API Key: {api_key}")
```

### Get, Update, Delete API Key

```python
def get_api_key(token, key_id):
    """Get details of a specific API key."""
    resp = requests.get(
        f"https://modelslab.com/api/agents/v1/api-keys/{key_id}",
        headers=make_headers(token)
    )
    return resp.json()["data"]

def update_api_key(token, key_id, name=None, notes=None):
    """Update an API key's name or notes."""
    payload = {}
    if name: payload["name"] = name
    if notes: payload["notes"] = notes

    resp = requests.put(
        f"https://modelslab.com/api/agents/v1/api-keys/{key_id}",
        headers=make_headers(token),
        json=payload
    )
    return resp.json()["data"]

def delete_api_key(token, key_id):
    """Delete an API key."""
    requests.delete(
        f"https://modelslab.com/api/agents/v1/api-keys/{key_id}",
        headers=make_headers(token)
    )
```

## Team Management

### List Team Members

```python
def list_team_members(token):
    """List all team members and pending invites."""
    resp = requests.get(
        "https://modelslab.com/api/agents/v1/teams",
        headers=make_headers(token)
    )
    return resp.json()["data"]
```

### Invite Team Member

```python
def invite_team_member(token, email):
    """Send a team invite to an email address."""
    resp = requests.post(
        "https://modelslab.com/api/agents/v1/teams",
        headers=make_headers(token),
        json={"email": email}
    )
    return resp.json()["data"]

# Usage
invite_team_member(token, "colleague@example.com")
```

### Manage Members

```python
def get_team_member(token, member_id):
    """Get details of a team member."""
    resp = requests.get(
        f"https://modelslab.com/api/agents/v1/teams/{member_id}",
        headers=make_headers(token)
    )
    return resp.json()["data"]

def update_team_member(token, member_id, role=None, permissions=None):
    """Update a team member's role or permissions."""
    payload = {}
    if role: payload["role"] = role
    if permissions: payload["permissions"] = permissions

    resp = requests.put(
        f"https://modelslab.com/api/agents/v1/teams/{member_id}",
        headers=make_headers(token),
        json=payload
    )
    return resp.json()["data"]

def remove_team_member(token, member_id):
    """Remove a member from the team."""
    requests.delete(
        f"https://modelslab.com/api/agents/v1/teams/{member_id}",
        headers=make_headers(token)
    )

def resend_invite(token, member_id):
    """Resend a pending team invite."""
    requests.post(
        f"https://modelslab.com/api/agents/v1/teams/{member_id}/resend-invite",
        headers=make_headers(token)
    )

def accept_invite(token, invite_id):
    """Accept a team invitation."""
    requests.post(
        f"https://modelslab.com/api/agents/v1/teams/invitations/{invite_id}/accept",
        headers=make_headers(token)
    )
```

## Complete Agent Bootstrap Example

```python
import requests

class ModelsLabAgent:
    """Bootstrap a ModelsLab account for an AI agent."""

    BASE = "https://modelslab.com/api/agents/v1"

    def __init__(self):
        self.token = None
        self.api_key = None

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, email, password):
        """Step 1: Authenticate."""
        resp = requests.post(f"{self.BASE}/auth/login", json={
            "email": email,
            "password": password,
            "token_expiry": "1_month"
        })
        self.token = resp.json()["data"]["access_token"]
        return self

    def get_or_create_api_key(self, name="agent-key"):
        """Step 2: Get existing key or create one."""
        keys = requests.get(
            f"{self.BASE}/api-keys",
            headers=self._headers()
        ).json()["data"]

        for key in keys:
            if key["name"] == name:
                self.api_key = key["key"]
                return self.api_key

        new_key = requests.post(
            f"{self.BASE}/api-keys",
            headers=self._headers(),
            json={"name": name}
        ).json()["data"]

        self.api_key = new_key["key"]
        return self.api_key

    def check_ready(self):
        """Step 3: Verify account is ready for generation."""
        profile = requests.get(
            f"{self.BASE}/me",
            headers=self._headers()
        ).json()["data"]

        print(f"Account: {profile['name']} ({profile['email']})")
        print(f"API Key: {self.api_key[:8]}...")
        return True

# Usage
agent = ModelsLabAgent()
agent.login("agent@example.com", "password")
agent.get_or_create_api_key("production")
agent.check_ready()

# Now use agent.api_key with generation endpoints
```

## Headless Agent Flow (No Browser Required)

The complete flow for agents that need to sign up, verify, add payment, subscribe, and generate content without any browser interaction. See `modelslab-billing-subscriptions` for all three payment paths (headless, setup intent, human-assisted).

```python
import requests

BASE = "https://modelslab.com/api/agents/v1"

# Fetch Stripe publishable key dynamically
config_resp = requests.get(f"{BASE}/billing/stripe-config",
    headers={"Authorization": f"Bearer {token}"})
STRIPE_PK = config_resp.json()["publishable_key"]

# 1. Sign up
signup_resp = requests.post(f"{BASE}/auth/signup", json={
    "email": "agent@example.com",
    "password": "securepass123",
    "name": "My Agent"
})
# -> User receives verification_code in email

# 2. Verify email with code from email (no browser needed)
verify_resp = requests.post(f"{BASE}/auth/verify-email", json={
    "verification_code": "the_code_from_email"
})
token = verify_resp.json()["data"]["access_token"]
api_key = verify_resp.json()["data"]["api_key"]
hdrs = {"Authorization": f"Bearer {token}"}

# 3a. Option A: Headless card tokenization via Stripe API (recommended)
# Or fetch key dynamically: GET /billing/stripe-config
pm_resp = requests.post(
    "https://api.stripe.com/v1/payment_methods",
    auth=(STRIPE_PK, ""),
    data={
        "type": "card",
        "card[number]": "4242424242424242",
        "card[exp_month]": 12,
        "card[exp_year]": 2027,
        "card[cvc]": "123",
    }
)
pm_id = pm_resp.json()["id"]

# 3b. Option B: Setup Intent flow (save card for future use)
# setup_resp = requests.post(f"{BASE}/billing/setup-intent", headers=hdrs)
# -> Confirm with Stripe API, then use the resulting pm_id

# 3c. Option C: Human-assisted payment link
# link = requests.post(f"{BASE}/billing/payment-link", headers=hdrs, json={
#     "purpose": "subscribe", "plan_id": 123
# }).json()["data"]
# -> Forward link["payment_url"] to human, then confirm-checkout

# 4. Attach the payment method
requests.post(f"{BASE}/billing/payment-methods", headers=hdrs, json={
    "payment_method_id": pm_id,
    "make_default": True
})

# 5. Subscribe headlessly with payment_method_id (no Checkout redirect)
sub_resp = requests.post(f"{BASE}/subscriptions", headers=hdrs, json={
    "plan_id": 123,
    "payment_method_id": pm_id
})

# 6. Generate content using existing APIs with the api_key from step 2
gen_resp = requests.post("https://modelslab.com/api/v6/images/text2img", json={
    "key": api_key,
    "model_id": "flux-dev",
    "prompt": "A sunset over mountains",
    "width": 1024,
    "height": 1024
})
```

## MCP Server Access

These same capabilities are available via the Agent Control Plane MCP server:
- **URL**: `https://modelslab.com/mcp/agents`
- **Auth**: `Authorization: Bearer <token>`
- **Tools**: `agent-auth`, `agent-tokens`, `agent-profile`, `agent-api-keys`, `agent-teams`

See: https://docs.modelslab.com/mcp-web-api/agent-control-plane

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Create account |
| POST | `/auth/login` | Get bearer token |
| POST | `/auth/verify-email` | Verify email with code (headless) |
| POST | `/auth/refresh` | Refresh/rotate access token |
| POST | `/auth/logout` | Revoke current token |
| POST | `/auth/logout-all` | Revoke all tokens |
| POST | `/auth/forgot-password` | Request reset email |
| POST | `/auth/reset-password` | Reset with token |
| POST | `/auth/resend-verification` | Resend verification email |
| GET | `/auth/tokens` | List active tokens |
| DELETE | `/auth/tokens/{id}` | Revoke specific token |
| POST | `/auth/tokens/revoke-others` | Revoke other tokens |
| POST | `/auth/switch-account` | Switch team context |
| GET | `/me` | Get profile |
| PATCH | `/me` | Update profile |
| PATCH | `/me/password` | Change password |
| PATCH | `/me/socials` | Update social links |
| PATCH | `/me/preferences` | Update preferences |
| GET | `/api-keys` | List API keys |
| POST | `/api-keys` | Create API key |
| GET | `/api-keys/{id}` | Get API key |
| PUT | `/api-keys/{id}` | Update API key |
| DELETE | `/api-keys/{id}` | Delete API key |
| GET | `/teams` | List team members |
| POST | `/teams` | Invite member |
| GET | `/teams/{id}` | Get member details |
| PUT | `/teams/{id}` | Update member |
| DELETE | `/teams/{id}` | Remove member |
| POST | `/teams/{id}/resend-invite` | Resend invite |
| POST | `/teams/invitations/{id}/accept` | Accept invite |

## Best Practices

### 1. Store Tokens Securely
```python
import os
# Use environment variables, not hardcoded values
token = os.getenv("MODELSLAB_AGENT_TOKEN")
```

### 2. Use Token Expiry Wisely
```python
# Short-lived for CI/CD
login(email, password, token_expiry="1_week")

# Long-lived for persistent agents
login(email, password, token_expiry="never")
```

### 3. Create Descriptive API Keys
```python
create_api_key(token, "staging-backend", notes="Used by staging environment")
create_api_key(token, "ci-tests", notes="Used by GitHub Actions")
```

### 4. Clean Up Old Tokens
```python
# Revoke all other tokens when rotating
revoke_other_tokens(token)
```

## Resources

- **API Documentation**: https://docs.modelslab.com/agents-api/overview
- **MCP Server**: https://docs.modelslab.com/mcp-web-api/agent-control-plane
- **Dashboard**: https://modelslab.com/dashboard
- **Discord**: https://discord.gg/modelslab

## Related Skills

- `modelslab-billing-subscriptions` - Billing, wallet, and subscription management
- `modelslab-model-discovery` - Search models and check usage analytics
- `modelslab-training` - Model training and fine-tuning
- `modelslab-servers` - Deploy dedicated GPU servers
- `modelslab-image-generation` - Use API keys for image generation
