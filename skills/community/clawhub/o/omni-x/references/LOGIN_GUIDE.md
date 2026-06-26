# Login Guide for Omni-X Twitter Skills

## Overview

Some Twitter API features require authentication. TweeterPy supports multiple login methods.

## Login Methods

### Method 1: Guest Session (Default - No Login)
```python
from scripts import TwitterSkills

# Uses guest session by default
twitter = TwitterSkills()

# Works without login:
# - get_user_profile()
# - get_user_tweets()
```

### Method 2: Auth Token Login
```python
from scripts import TwitterSkills

twitter = TwitterSkills()
twitter.twitter.generate_session(auth_token="your_auth_token_here")
```

### Method 3: Credentials Login
```python
from scripts import TwitterSkills

twitter = TwitterSkills()
twitter.twitter.login(
    username="your_username",
    password="your_password",
    email="your_email",  # optional
    phone="your_phone"   # optional
)
```

### Method 4: Load Saved Session
```python
from scripts import TwitterSkills

twitter = TwitterSkills()
# Load previously saved session
twitter.twitter.load_session()
```

## Save Session for Future Use

```python
# After logging in, save the session
twitter.twitter.save_session()
```

## Features Requiring Login

- **get_user_followers()** - Requires login
- **get_user_followings()** - Requires login
- **get_user_media()** - Requires login
- **search_tweets()** - Requires login

## Features Working Without Login

- **get_user_profile()** - Works with guest session
- **get_user_tweets()** - Works with guest session

## Example with Login

```python
from scripts import TwitterSkillInterface

# Initialize
interface = TwitterSkillInterface()

# Login (choose one method)
interface.skills.twitter.generate_session(auth_token="your_token")

# Now you can use all features
result = interface.execute_skill(
    skill_name="get_user_followers",
    parameters={"username": "elonmusk", "count": 10}
)

# Save session for next time
interface.skills.twitter.save_session()
```

## How to Get Auth Token

The `auth_token` is a **cookie parameter** from Twitter/X:

### Method A: Via Application/Storage Tab (Easiest)

1. Open Twitter/X in your browser and log in
2. Open Developer Tools (F12 or Right-click → Inspect)
3. Go to **Application** tab (Chrome/Edge) or **Storage** tab (Firefox)
4. In the left sidebar, expand **Cookies**
5. Click on `https://twitter.com` or `https://x.com`
6. Find the cookie named **`auth_token`**
7. Copy its **Value** - this is your auth_token

### Method B: Via Network Tab

1. Open Developer Tools (F12) → **Network** tab
2. Refresh the page
3. Click on any request to Twitter's API
4. Go to **Headers** → **Request Headers**
5. Find the `Cookie:` header
6. Look for `auth_token=...` in the cookie string
7. Copy the value after `auth_token=` (up to the next semicolon)

**Example:**
```
Cookie: auth_token=a1b2c3d4e5f6...; ct0=xyz123...
```
Your auth_token is: `a1b2c3d4e5f6...`

## Important Notes

- Try guest session first for basic features
- Only login if you need followers/followings/media/search
- Save your session to avoid frequent logins
- Keep your auth token secure
