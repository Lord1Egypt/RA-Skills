# Omni-X Installation and Usage Guide

## 🤖 How AI Agents Can Use This Project

AI Agents can use Omni-X Twitter Skills in three ways:

---

## Method 1: Direct Use (Recommended for Development and Testing)

### Step 1: Clone or Download the Project
```bash
cd /path/to/your/workspace
git clone <repository-url>
cd Omni-X
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Import and Use in Code
```python
import sys
sys.path.append('/path/to/Omni-X')

from scripts import TwitterSkillInterface

# Initialize with auth_token
interface = TwitterSkillInterface(auth_token="your_auth_token")

# Execute a skill
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

print(result)
```

---

## Method 2: Install as Python Package (Recommended for Production)

### Step 1: Install the Package
```bash
# Install from local directory
cd /path/to/Omni-X
pip install -e .

# Or install directly from Git (if published)
pip install git+https://github.com/yourusername/Omni-X.git
```

### Step 2: Use Anywhere
```python
from scripts import TwitterSkillInterface

# Initialize and use
interface = TwitterSkillInterface(auth_token="your_auth_token")
result = interface.execute_skill(
    skill_name="get_user_profile",
    parameters={"username": "elonmusk"}
)
```

---

## Method 3: Integrate as Git Submodule

### Step 1: Add as Git Submodule
```bash
cd /path/to/your/project
git submodule add <repository-url> omni-x
git submodule update --init --recursive
```

### Step 2: Install Dependencies
```bash
pip install -r omni-x/requirements.txt
```

### Step 3: Use in Your Project
```python
from omni_x.scripts import TwitterSkillInterface

interface = TwitterSkillInterface(auth_token="your_token")
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 10}
)
```

---

## 🚀 Quick Start Example

### Simplest Usage

```python
from scripts import TwitterSkillInterface

# 1. Initialize (with token for full access)
interface = TwitterSkillInterface(auth_token="your_auth_token_here")

# 2. View available skills
skills = interface.get_available_skills()
print("Available skills:", list(skills.keys()))

# 3. Execute a skill
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

# 4. Process results
if result["success"]:
    print(f"Retrieved {result['count']} tweets")
    for tweet in result["data"]:
        print(f"- {tweet}")
else:
    print(f"Error: {result['error']}")
```

---

## 📋 AI Agent Integration Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Obtain Twitter auth_token (see LOGIN_GUIDE.md)
- [ ] Import TwitterSkillInterface
- [ ] Initialize interface with auth_token
- [ ] Call execute_skill() to execute skills
- [ ] Check the success field in returned results
- [ ] Process the returned data

---

## 🔑 Authentication Guide

### Getting Auth Token

The `auth_token` is a cookie parameter from Twitter/X:

1. Log in to Twitter/X in your browser
2. Open browser developer tools (F12)
3. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
4. Navigate to **Cookies** → `https://twitter.com` or `https://x.com`
5. Find the cookie named **`auth_token`**
6. Copy its **Value** (this is your auth_token)

**Alternative method via Network tab:**
1. Open developer tools (F12) → **Network** tab
2. Refresh the page
3. Find any Twitter API request
4. Look in **Request Headers** for `Cookie:` header
5. Find `auth_token=...` in the cookie string
6. Copy the value after `auth_token=`

See [LOGIN_GUIDE.md](LOGIN_GUIDE.md) for detailed instructions with screenshots

### Using Token

```python
# Method 1: Pass during initialization (Recommended)
interface = TwitterSkillInterface(auth_token="your_token")

# Method 2: Set later
interface = TwitterSkillInterface()
interface.set_auth_token("your_token")

# Method 3: No token (limited features)
interface = TwitterSkillInterface()  # Only supports profile and tweets
```

---

## 📚 Complete Documentation

- **[README.md](README.md)** - Project overview
- **[AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)** - Complete AI Agent integration guide
- **[LOGIN_GUIDE.md](LOGIN_GUIDE.md)** - Authentication details
- **[STATUS.md](STATUS.md)** - Project status

---

## 🧪 Test Installation

Run test scripts to verify installation:

```bash
# Test basic functionality
python test.py

# Test token authentication
python test_with_token.py

# Test AI Agent interface
python agent_example.py
```

---

## ❓ FAQ

### Q: Must AI Agents provide auth_token?
A: Not required, but strongly recommended. Without token, only basic features (profile, tweets) are available. Cannot access followers, followings, media, search features.

### Q: How to store token in AI Agent?
A: Recommended to use environment variables or config files:
```python
import os
auth_token = os.getenv("TWITTER_AUTH_TOKEN")
interface = TwitterSkillInterface(auth_token=auth_token)
```

### Q: Can I use multiple tokens simultaneously?
A: Yes, create separate TwitterSkillInterface instances for each token:
```python
interface1 = TwitterSkillInterface(auth_token="token1")
interface2 = TwitterSkillInterface(auth_token="token2")
```

### Q: What are the project dependencies?
A: Main dependency is `tweeterpy`, which automatically installs other required packages.

---

## 💡 AI Agent Best Practices

1. **Always provide auth_token** - Ensures full feature access
2. **Check success field** - Verify request success before processing data
3. **Handle errors** - Gracefully handle API errors and rate limits
4. **Use skill discovery** - Call `get_available_skills()` to dynamically get available features
5. **Cache results** - Avoid repeated requests for same data
6. **Respect rate limits** - Add appropriate delays between requests

---

## 📞 Support

For questions, check:
- Project documentation (README.md, AI_AGENT_GUIDE.md)
- Example code (agent_example.py, test.py)
- TweeterPy documentation: https://github.com/iSarabjitDhiman/TweeterPy
