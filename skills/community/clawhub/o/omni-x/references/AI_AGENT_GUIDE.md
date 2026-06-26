# AI Agent Integration Guide

## Overview

This document provides instructions for AI agents to integrate and use the Omni-X Twitter Skills.

## Quick Start

```python
from scripts import TwitterSkillInterface

# Method 1: Initialize with auth_token (RECOMMENDED)
interface = TwitterSkillInterface(auth_token="your_auth_token_here")

# Method 2: Initialize without token (guest session)
interface = TwitterSkillInterface()

# Method 3: Set token after initialization
interface = TwitterSkillInterface()
interface.set_auth_token("your_auth_token_here")

# Discover available skills
skills = interface.get_available_skills()

# Execute a skill
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)
```

## Available Skills

### 1. get_user_profile
Extract user profile information.

**Parameters:**
- `username` (str, required): Twitter username without @

**Returns:**
```python
{
    "success": True,
    "data": {...},  # User profile data
    "skill_name": "get_user_profile",
    "parameters": {"username": "elonmusk"}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_profile",
    parameters={"username": "elonmusk"}
)
```

---

### 2. get_user_tweets
Extract user's recent tweets.

**Parameters:**
- `username` (str, required): Twitter username without @
- `count` (int, optional): Number of tweets to retrieve (default: 10)

**Returns:**
```python
{
    "success": True,
    "data": [...],  # List of tweets
    "count": 5,
    "has_next_page": True,
    "cursor": "...",
    "skill_name": "get_user_tweets",
    "parameters": {"username": "elonmusk", "count": 5}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 10}
)
```

---

### 3. get_user_followers
Extract user's followers list. **Requires login.**

**Parameters:**
- `username` (str, required): Twitter username without @
- `count` (int, optional): Number of followers to retrieve (default: 20)

**Returns:**
```python
{
    "success": True,
    "data": [...],  # List of followers
    "count": 20,
    "has_next_page": True,
    "cursor": "...",
    "skill_name": "get_user_followers",
    "parameters": {"username": "elonmusk", "count": 20}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_followers",
    parameters={"username": "elonmusk", "count": 20}
)
```

---

### 4. get_user_followings
Extract user's following list. **Requires login.**

**Parameters:**
- `username` (str, required): Twitter username without @
- `count` (int, optional): Number of followings to retrieve (default: 20)

**Returns:**
```python
{
    "success": True,
    "data": [...],  # List of followings
    "count": 20,
    "has_next_page": True,
    "cursor": "...",
    "skill_name": "get_user_followings",
    "parameters": {"username": "elonmusk", "count": 20}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_followings",
    parameters={"username": "elonmusk", "count": 20}
)
```

---

### 5. get_user_media
Extract media from user's tweets. **Requires login.**

**Parameters:**
- `username` (str, required): Twitter username without @
- `count` (int, optional): Number of media items to retrieve (default: 10)

**Returns:**
```python
{
    "success": True,
    "data": [...],  # List of media items
    "count": 10,
    "has_next_page": True,
    "cursor": "...",
    "skill_name": "get_user_media",
    "parameters": {"username": "elonmusk", "count": 10}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_media",
    parameters={"username": "elonmusk", "count": 10}
)
```

---

### 6. search_tweets
Search tweets by query. **Requires login.**

**Parameters:**
- `query` (str, required): Search query string
- `count` (int, optional): Number of tweets to retrieve (default: 10)
- `search_filter` (str, optional): Filter type - "Latest", "Top", "People", "Photos", "Videos" (default: "Top")

**Returns:**
```python
{
    "success": True,
    "data": [...],  # List of tweets
    "count": 10,
    "has_next_page": True,
    "cursor": "...",
    "skill_name": "search_tweets",
    "parameters": {"query": "AI technology", "count": 10, "search_filter": "Top"}
}
```

**Example:**
```python
result = interface.execute_skill(
    skill_name="search_tweets",
    parameters={
        "query": "AI technology",
        "count": 10,
        "search_filter": "Latest"
    }
)
```

---

## Dynamic Skill Discovery

AI agents can discover available skills at runtime:

```python
# Get all available skills
skills = interface.get_available_skills()

# Iterate through skills
for skill_name, skill_info in skills.items():
    print(f"Skill: {skill_name}")
    print(f"Description: {skill_info['description']}")
    print(f"Parameters: {skill_info['parameters']}")
    print(f"Returns: {skill_info['returns']}")
```

## Error Handling

All skills return a standardized response format:

**Success Response:**
```python
{
    "success": True,
    "data": [...],
    "count": 10,
    "skill_name": "...",
    "parameters": {...}
}
```

**Error Response:**
```python
{
    "success": False,
    "error": "Error message",
    "skill_name": "...",
    "parameters": {...}
}
```

**Invalid Skill Response:**
```python
{
    "success": False,
    "error": "Unknown skill: invalid_skill",
    "available_skills": ["get_user_profile", "get_user_tweets", ...]
}
```

## Authentication

### ⚠️ Important: Token Usage Recommendation

**By default, TweeterPy uses a Guest Session** which has limited access. For AI agents calling these skills:

**BEST PRACTICE: Always provide an auth_token when possible**

```python
from scripts import TwitterSkillInterface

interface = TwitterSkillInterface()

# RECOMMENDED: Provide auth_token for full access
interface.skills.twitter.generate_session(auth_token="your_auth_token_here")
```

### Authentication Methods

TweeterPy supports multiple authentication methods. **Use only ONE of the following:**

#### Method 1: Auth Token (Recommended)
```python
interface.skills.twitter.generate_session(auth_token="your_auth_token_here")
```

#### Method 2: Username/Password Login
```python
interface.skills.twitter.login(
    username="your_username",
    password="your_password",
    email="your_email",  # optional
    phone="your_phone"   # optional
)
```

#### Method 3: Load Saved Session
```python
# If you previously saved a session with twitter.save_session()
interface.skills.twitter.load_session()
```

### Skill Access Levels

**Skills that work without login (Guest Session):**
- get_user_profile
- get_user_tweets

**Skills that require login (Auth Token needed):**
- get_user_followers
- get_user_followings
- get_user_media
- search_tweets

### Authentication Workflow

```python
from scripts import TwitterSkillInterface

interface = TwitterSkillInterface()

# Step 1: Try with guest session first (default)
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

# Step 2: If you need restricted features, provide auth_token
if not result["success"]:
    interface.skills.twitter.generate_session(auth_token="your_token")
    result = interface.execute_skill(
        skill_name="get_user_followers",
        parameters={"username": "elonmusk", "count": 10}
    )
```

### Getting Your Auth Token

The `auth_token` is a **cookie parameter** from Twitter/X. To get it:

**Quick Steps:**
1. Log in to Twitter/X in your browser
2. Open Developer Tools (F12)
3. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
4. Navigate to **Cookies** → `https://twitter.com` or `https://x.com`
5. Find the cookie named **`auth_token`**
6. Copy its **Value**

See [LOGIN_GUIDE.md](LOGIN_GUIDE.md) for detailed instructions with alternative methods.

## Best Practices for AI Agents

1. **Provide auth_token when calling skills** - For best results, always provide an auth_token to access all features
2. **Try guest session first** - For basic features (profile, tweets), try without login first, then use auth_token if needed
3. **Use only ONE authentication method** - Don't mix auth_token, login(), and load_session() - choose one
4. **Always check the success field** in the response before processing data
5. **Use dynamic skill discovery** to adapt to new skills automatically
6. **Handle errors gracefully** and provide meaningful feedback to users
7. **Cache skill metadata** to avoid repeated discovery calls
8. **Respect rate limits** by implementing delays between requests
9. **Use pagination** for large datasets via the cursor field

## Example: Complete AI Agent Workflow

```python
from scripts import TwitterSkillInterface

class TwitterAgent:
    def __init__(self):
        self.interface = TwitterSkillInterface()
        self.skills = self.interface.get_available_skills()
    
    def execute_task(self, task_description):
        # Parse task and determine which skill to use
        if "profile" in task_description.lower():
            skill_name = "get_user_profile"
        elif "tweets" in task_description.lower():
            skill_name = "get_user_tweets"
        else:
            return {"error": "Cannot determine skill from task"}
        
        # Extract parameters from task
        # (simplified - real implementation would use NLP)
        username = "elonmusk"  # extracted from task
        
        # Execute skill
        result = self.interface.execute_skill(
            skill_name=skill_name,
            parameters={"username": username}
        )
        
        # Process result
        if result["success"]:
            return self.format_response(result)
        else:
            return {"error": result["error"]}
    
    def format_response(self, result):
        # Format the response for the user
        return {
            "status": "completed",
            "skill_used": result["skill_name"],
            "data_count": result.get("count", 0),
            "summary": f"Retrieved {result.get('count', 0)} items"
        }

# Usage
agent = TwitterAgent()
response = agent.execute_task("Get tweets from elonmusk")
print(response)
```

## Support

For issues or questions:
- Check [README.md](README.md) for general usage
- Check [LOGIN_GUIDE.md](LOGIN_GUIDE.md) for authentication
- Review [agent_example.py](agent_example.py) for code examples
