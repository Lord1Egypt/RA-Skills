---
name: omni-x-data-extractor
description: |
  Extract X (Twitter) data including user profiles, posts, followers, followings, media, and search results.
  This skill provides comprehensive Twitter data extraction capabilities using the tweeterpy library.
  
  Trigger scenarios:
  - When user asks to get Twitter user information or profile
  - When user wants to extract tweets from a specific user
  - When user needs to analyze Twitter followers or followings
  - When user wants to search for tweets by keywords
  - When user needs to extract media from Twitter posts
  
  Authentication levels:
  - Guest session (no auth): get_user_profile, get_user_tweets
  - Authenticated session (auth_token required): get_user_followers, get_user_followings, get_user_media, search_tweets

version: 1.0.0
author: Omni-X
category: social-media
tags: [twitter, x, social-media, data-extraction, api]
---

# X (Twitter) Data Extractor Skill

## Overview

This skill provides AI agents with the ability to extract various types of data from X (Twitter) platform, including user profiles, posts, followers, followings, media content, and search results.

## Prerequisites
- Python 3.7+ installed
- Dependencies installed (see `references/INSTALLATION.md`)


## Workflow

### Step 1: Initialize the Skill Interface

```python
from scripts import TwitterSkillInterface

# Method 1: Initialize with auth_token (RECOMMENDED for full access)
interface = TwitterSkillInterface(auth_token="your_auth_token_here")

# Method 2: Initialize without token (guest session - limited features)
interface = TwitterSkillInterface()

# Method 3: Set token after initialization
interface = TwitterSkillInterface()
interface.set_auth_token("your_auth_token_here")
```

### Step 2: Discover Available Skills

```python
# Get all available skills and their metadata
skills = interface.get_available_skills()

# Each skill contains:
# - description: What the skill does
# - parameters: Required and optional parameters
# - returns: Expected return format
# - requires_auth: Whether authentication is needed
```

### Step 3: Execute Skills

```python
# Execute a skill with parameters
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 10}
)

# Check result
if result["success"]:
    data = result["data"]
    print(f"Retrieved {result['count']} items")
else:
    print(f"Error: {result['error']}")
```

### Step 4: Handle Results

All skills return a standardized response format:

**Success Response:**
```python
{
    "success": True,
    "data": [...],           # The actual data
    "count": 10,             # Number of items (if applicable)
    "has_next_page": True,   # Pagination info (if applicable)
    "cursor": "...",         # Cursor for next page (if applicable)
    "skill_name": "...",     # Name of executed skill
    "parameters": {...}      # Parameters used
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

## Available Skills

### 1. get_user_profile
**Description:** Extract detailed user profile information.

**Authentication:** Not required (works with guest session)

**Parameters:**
- `username` (str, required): Twitter username without @ symbol

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_profile",
    parameters={"username": "elonmusk"}
)
```

**Returns:** User profile data including name, bio, followers count, following count, etc.

---

### 2. get_user_tweets
**Description:** Extract recent tweets from a specific user.

**Authentication:** Not required (works with guest session)

**Parameters:**
- `username` (str, required): Twitter username without @ symbol
- `count` (int, optional): Number of tweets to retrieve (default: 10)

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 20}
)
```

**Returns:** List of tweets with text, timestamp, engagement metrics, etc.

---

### 3. get_user_followers
**Description:** Extract list of users following the specified account.

**Authentication:** Required (auth_token needed)

**Parameters:**
- `username` (str, required): Twitter username without @ symbol
- `count` (int, optional): Number of followers to retrieve (default: 20)

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_followers",
    parameters={"username": "elonmusk", "count": 50}
)
```

**Returns:** List of follower profiles with pagination support.

---

### 4. get_user_followings
**Description:** Extract list of users that the specified account follows.

**Authentication:** Required (auth_token needed)

**Parameters:**
- `username` (str, required): Twitter username without @ symbol
- `count` (int, optional): Number of followings to retrieve (default: 20)

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_followings",
    parameters={"username": "elonmusk", "count": 50}
)
```

**Returns:** List of following profiles with pagination support.

---

### 5. get_user_media
**Description:** Extract media content (photos/videos) from user's tweets.

**Authentication:** Required (auth_token needed)

**Parameters:**
- `username` (str, required): Twitter username without @ symbol
- `count` (int, optional): Number of media items to retrieve (default: 10)

**Example:**
```python
result = interface.execute_skill(
    skill_name="get_user_media",
    parameters={"username": "elonmusk", "count": 15}
)
```

**Returns:** List of media items with URLs and metadata.

---

### 6. search_tweets
**Description:** Search for tweets matching a query string.

**Authentication:** Required (auth_token needed)

**Parameters:**
- `query` (str, required): Search query string
- `count` (int, optional): Number of tweets to retrieve (default: 10)
- `search_filter` (str, optional): Filter type - "Latest", "Top", "People", "Photos", "Videos" (default: "Top")

**Example:**
```python
result = interface.execute_skill(
    skill_name="search_tweets",
    parameters={
        "query": "AI technology",
        "count": 20,
        "search_filter": "Latest"
    }
)
```

**Returns:** List of tweets matching the search query.

---

## Tool Usage Instructions

### For AI Agents

When using this skill, follow these steps:

1. **Determine the task**: Analyze user request to identify which skill is needed
   - Profile info → `get_user_profile`
   - Recent tweets → `get_user_tweets`
   - Follower analysis → `get_user_followers`
   - Following analysis → `get_user_followings`
   - Media extraction → `get_user_media`
   - Search tweets → `search_tweets`

2. **Check authentication requirements**: 
   - If skill requires auth and no token is set, inform user to provide auth_token
   - Guest session works for: `get_user_profile`, `get_user_tweets`
   - Auth required for: `get_user_followers`, `get_user_followings`, `get_user_media`, `search_tweets`

3. **Extract parameters from user request**:
   - Username (remove @ if present)
   - Count/limit for results
   - Search filters (for search_tweets)

4. **Execute the skill**:
   ```python
   result = interface.execute_skill(skill_name="...", parameters={...})
   ```

5. **Process and present results**:
   - Check `result["success"]` first
   - If successful, format and present `result["data"]`
   - If failed, explain `result["error"]` to user
   - Mention pagination if `result["has_next_page"]` is True

### Error Handling

```python
result = interface.execute_skill(skill_name="...", parameters={...})

if not result["success"]:
    error_msg = result["error"]
    
    # Common errors and solutions:
    if "auth" in error_msg.lower() or "login" in error_msg.lower():
        # Inform user that authentication is required
        print("This feature requires authentication. Please provide auth_token.")
    elif "not found" in error_msg.lower():
        # Username doesn't exist
        print(f"User not found. Please check the username.")
    elif "rate limit" in error_msg.lower():
        # Rate limit exceeded
        print("Rate limit exceeded. Please wait before trying again.")
    else:
        # Generic error
        print(f"An error occurred: {error_msg}")
```

## Examples

### Example 1: Get User Profile and Recent Tweets

```python
from scripts import TwitterSkillInterface

# Initialize
interface = TwitterSkillInterface()

# Get profile
profile = interface.execute_skill(
    skill_name="get_user_profile",
    parameters={"username": "elonmusk"}
)

if profile["success"]:
    print(f"User: {profile['data']['name']}")
    print(f"Followers: {profile['data']['followers_count']}")

# Get recent tweets
tweets = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

if tweets["success"]:
    for tweet in tweets["data"]:
        print(f"Tweet: {tweet['text']}")
```

### Example 2: Search and Analyze Tweets (Requires Auth)

```python
from scripts import TwitterSkillInterface

# Initialize with auth token
interface = TwitterSkillInterface(auth_token="your_auth_token")

# Search for tweets
results = interface.execute_skill(
    skill_name="search_tweets",
    parameters={
        "query": "artificial intelligence",
        "count": 20,
        "search_filter": "Latest"
    }
)

if results["success"]:
    print(f"Found {results['count']} tweets")
    for tweet in results["data"]:
        print(f"- {tweet['text'][:100]}...")
```

### Example 3: Analyze User Network (Requires Auth)

```python
from scripts import TwitterSkillInterface

# Initialize with auth token
interface = TwitterSkillInterface(auth_token="your_auth_token")

username = "elonmusk"

# Get followers
followers = interface.execute_skill(
    skill_name="get_user_followers",
    parameters={"username": username, "count": 100}
)

# Get followings
followings = interface.execute_skill(
    skill_name="get_user_followings",
    parameters={"username": username, "count": 100}
)

if followers["success"] and followings["success"]:
    print(f"Followers: {followers['count']}")
    print(f"Following: {followings['count']}")
    print(f"Ratio: {followers['count'] / followings['count']:.2f}")
```

## Best Practices

1. **Always provide auth_token when possible** - Many features require authentication
2. **Check success field first** - Always verify `result["success"]` before accessing data
3. **Handle pagination** - Use `cursor` field for large datasets
4. **Respect rate limits** - **CRITICAL**: Implement delays between requests to avoid account restrictions
   - Recommended: 1-2 second delay between requests
   - For bulk operations: 2-3 second delay
   - Monitor for rate limit errors and back off exponentially if encountered
5. **Cache results** - Avoid repeated requests for the same data
6. **Validate usernames** - Remove @ symbol and validate format before calling
7. **Use appropriate count values** - Start with small counts (10-20) and increase gradually as needed
8. **Handle errors gracefully** - Provide meaningful feedback to users
9. **Comply with Terms of Service** - Ensure all usage complies with X (Twitter) Terms of Service
10. **Educational/Research Use Only** - This tool is intended for educational and research purposes only

## Authentication Guide

See `references/LOGIN_GUIDE.md` for detailed instructions on obtaining and using auth_token.

Quick steps:
1. Log in to Twitter/X in browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Find `auth_token` cookie
5. Copy its value
6. Use it to initialize: `TwitterSkillInterface(auth_token="...")`

## Troubleshooting

**Problem:** "Guest session has limited access"
- **Solution:** Provide auth_token for full feature access

**Problem:** "User not found"
- **Solution:** Verify username is correct (without @ symbol)

**Problem:** "Rate limit exceeded"
- **Solution:** Wait before making more requests, implement delays

**Problem:** "Authentication required"
- **Solution:** Provide valid auth_token for this feature

## References

- Full API documentation: `references/AI_AGENT_GUIDE.md`
- Authentication guide: `references/LOGIN_GUIDE.md`
- Installation instructions: `references/INSTALLATION.md`
- Example code: `agent_example.py`

## Support

For issues or questions, refer to the documentation in the `references/` directory or check the main README.md file.
