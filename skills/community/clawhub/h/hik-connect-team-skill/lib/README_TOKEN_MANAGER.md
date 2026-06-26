# HCT Global Token Manager

🔐 Provides unified Token cache management for all HCT skills.

## 📁 Location

```
/Users/jony/.openclaw/workspace/skills/Hik-Connect Team Skills/lib/token_manager.py
```

## ✨ Features

- **Global Cache**: All skills share the same Token, avoiding repeated acquisition
- **Smart Reuse**: Use cache directly during Token validity period, no API calls
- **Safe Buffer**: Auto-refresh 5 minutes before expiration to avoid boundary issues
- **Multi-Account Support**: Identify different accounts based on md5(appKey:appSecret)
- **Atomic Write**: Write to temporary file first then replace, ensuring data safety
- **Permission Protection**: Cache file permission set to 600 (owner read/write only)

## 🔐 Credential Configuration

**Credentials only need to be configured ONCE. The system will automatically find and use them.**

**Priority order (highest to lowest):**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Environment Variables (if set)                           │
│    ├─ HIK_CONNECT_TEAM_OPENAPI_APP_KEY                      │
│    └─ HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY                   │
├─────────────────────────────────────────────────────────────┤
│ 2. OpenClaw Config Files (if env vars not set)              │
│    ├─ ~/.openclaw/config.json                               │
│    ├─ ~/.openclaw/gateway/config.json                        │
│    └─ ~/.openclaw/channels.json ⭐ Recommended                       │
└─────────────────────────────────────────────────────────────┘
```

### OpenClaw Config File Format

Config file format (same for all three files):

```json
{
  "channels": {
    "hik_connect_team_openapi": {
      "appKey": "Your Hik-Connect Team OpenAPI AppKey",
      "secretKey": "Your Hik-Connect Team OpenAPI SecretKey",
      "enabled": true
    }
  }
}
```

**Recommended: Save to `~/.openclaw/channels.json`** — This is the dedicated file for channel credentials.

**⚠️ Security Note**: Before saving credentials to a config file, ask the user for confirmation. Storing credentials on disk is convenient but introduces some risk. Always inform the user of this option and let them choose.

---

## 🚀 Usage

### Method 1: Import and use in Python skills

```python
# Add lib directory to path
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.join(script_dir, "..", "..")
lib_dir = os.path.abspath(os.path.join(workspace_dir, "Hik-Connect Team Skills", "lib"))
if os.path.exists(lib_dir) and lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from token_manager import get_cached_token

# Get Token (prefer cache, auto-refresh if expired)
token_result = get_cached_token(app_key, app_secret, use_cache=True)
if token_result["success"]:
    access_token = token_result["access_token"]
    print(f"Token: {access_token}")
    print(f"From Cache: {token_result['from_cache']}")
```

### Method 2: Command Line Tool

```bash
cd /Users/jony/.openclaw/workspace/skills/Hik-Connect Team Skills

# Get Token (use cache)
python lib/token_manager.py get --app-key "your_key" --app-secret "your_secret"

# Force refresh Token (no cache)
python lib/token_manager.py refresh --app-key "your_key" --app-secret "your_secret"

# View cache list
python lib/token_manager.py list

# Clear specific account cache
python lib/token_manager.py clear --app-key "your_key" --app-secret "your_secret"

# Clear all cache
python lib/token_manager.py clear
```

## 📊 Cache Location

```
/var/folders/xx/xxxx/T/hctopen_global_token_cache/global_token_cache.json
```

Cache file format:
```json
{
  "3aa746c5ea5329ab...": {
    "cache_key": "3aa746c5ea5329ab...",
    "access_token": "at.ay4x6ris6kl61uao6a3qcjpa1ww...",
    "area_domain": "https://ieu-team.hikcentralconnect.com",
    "expire_time": 1774419637518,
    "created_at": 1773816338280,
    "app_key_prefix": "26810f3a..."
  }
}
```

## 🔄 Workflow

```
Skill Startup
    ↓
Call get_cached_token(app_key, app_secret)
    ↓
Check cache file
    ├─ Cache exists and not expired → Return cached Token directly ✅
    └─ Cache doesn't exist or expired → Call API to get new Token
                                      ↓
                                Save to cache file
                                      ↓
                                Return new Token
```

## 🎯 Integrated Skills

| Skill                         | Status       | File                       |
|-------------------------------|--------------|----------------------------|
| Device List (device_list)     | ✅ Integrated | `scripts/list_devices.py`  |
| Device Detail (device_detail) | ✅ Integrated | `scripts/device_detail.py` |

## 🧪 Test Examples

```bash
# 1. Clear cache
python lib/token_manager.py clear

# 2. First acquisition (from API)
python lib/token_manager.py get --app-key "26810f3acd794862b608b6cfbc32a6b8" --app-secret "3155063e93f09f377eaf5ba9f321f8c2"
# Output: From Cache: False

# 3. Get again (from cache)
python lib/token_manager.py get --app-key "26810f3acd794862b608b6cfbc32a6b8" --app-secret "3155063e93f09f377eaf5ba9f321f8c2"
# Output: From Cache: True

# 4. View cache
python lib/token_manager.py list
```

## ⚠️ Notes

1. **Token Validity**: 7 days, auto-refresh 5 minutes before expiration
2. **Cache Cleanup**: System temp directory may be periodically cleaned
3. **Multi-Account**: Each appKey:appSecret combination has independent cache
4. **Security**: Cache file permission 600, owner read/write only
5. **Concurrency**: Supports multi-process simultaneous reading, atomic operation during writing

## 📝 API Functions

### get_cached_token(app_key, app_secret, use_cache=True)
Get Token, prefer using cache.

**Returns**:
```json
{
    "success": True,
    "access_token": "at.xxx",
    "area_domain": "https://hpc-sgp-uat-5.hik-partner.com",
    "expire_time": 1774419637518,
    "from_cache": True
}
```

### refresh_token(app_key, app_secret, cache_key=None)
Force refresh Token, do not use cache.

### clear_token_cache(app_key=None, app_secret=None)
Clear cache (can specify account or clear all).

### list_cached_tokens()
List all cached Token information.

---

**Error Codes**:

| Return Code | Return Message    | Description                   |
|-------------|-------------------|-------------------------------|
| OPEN000001  | AK does not exist | Please check if AK is correct |
| OPEN000002  | SK error          | SK does not match current AK  |