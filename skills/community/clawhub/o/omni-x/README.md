# Omni-X - X (Twitter) Skills

> A skill project for agents to extract X (Twitter) data including posts, followers, followings, profile details, and media.

[![中文文档](https://img.shields.io/badge/docs-%E4%B8%AD%E6%96%87-0F766E?style=flat-square)](./README_CN.md)

## 🙏 Acknowledgments

This project is built on top of [TweeterPy](https://github.com/iSarabjitDhiman/TweeterPy) - an excellent Python library for Twitter/X data extraction without using the official API.

**Special thanks to [@iSarabjitDhiman](https://github.com/iSarabjitDhiman)** for creating and maintaining TweeterPy, which makes this project possible. TweeterPy provides the core functionality for:
- Extracting tweets and user profiles
- Accessing followers and followings data
- Searching tweets and extracting media
- Handling Twitter authentication

All the Twitter data extraction capabilities in Omni-X are powered by TweeterPy. We are grateful for the open-source community and the amazing work done by the TweeterPy team.

**TweeterPy Repository:** https://github.com/iSarabjitDhiman/TweeterPy

## Features

- Extract Tweets
- Extract User's Followers
- Extract User's Followings
- Extract User's Profile Details
- Extract Twitter Profile Media
- Search Tweets by Query

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### For Direct Use

```python
from scripts import TwitterSkills

# Initialize the skills
twitter = TwitterSkills()

# Extract user profile
profile = twitter.get_user_profile("username")

# Extract tweets
tweets = twitter.get_user_tweets("username", count=10)

# Extract followers
followers = twitter.get_user_followers("username", count=20)

# Extract followings
followings = twitter.get_user_followings("username", count=20)

# Extract media
media = twitter.get_user_media("username", count=10)
```

### For AI Agents (Recommended)

The `TwitterSkillInterface` provides a standardized interface that AI agents can use to discover and execute skills dynamically:

```python
from scripts import TwitterSkillInterface

# Initialize the interface
interface = TwitterSkillInterface()

# Discover available skills
skills = interface.get_available_skills()
# Returns: Dict with skill names, descriptions, parameters, and return types

# Execute a skill
result = interface.execute_skill(
    skill_name="get_user_tweets",
    parameters={"username": "elonmusk", "count": 5}
)

# Result format:
# {
#     "success": True/False,
#     "data": [...],
#     "count": 5,
#     "skill_name": "get_user_tweets",
#     "parameters": {"username": "elonmusk", "count": 5}
# }
```

### Available Skills for AI Agents

1. **get_user_profile** - Extract user profile information
2. **get_user_tweets** - Extract user's recent tweets
3. **get_user_followers** - Extract user's followers list
4. **get_user_followings** - Extract user's following list
5. **get_user_media** - Extract media from user's tweets
6. **search_tweets** - Search tweets by query

## Documentation

### For AI Agents
- **[SKILL.md](SKILL.md)** - Core skill definition and usage guide (entry point for AI agents)
- **[references/AI_AGENT_GUIDE.md](references/AI_AGENT_GUIDE.md)** - Complete API reference for AI agents
- **[agent_example.py](agent_example.py)** - Example code for AI agent integration

### General
- **[references/LOGIN_GUIDE.md](references/LOGIN_GUIDE.md)** - Authentication and login instructions
- **[references/INSTALLATION.md](references/INSTALLATION.md)** - Installation guide

## Examples

Run the example script:

```bash
# AI agent interface example
python agent_example.py
```

## Requirements

- Python 3.7+
- tweeterpy

## ⚠️ Disclaimer and Terms of Use

**This project is for educational and research purposes only.**

By using this tool, you agree to:

1. **Comply with X (Twitter) Terms of Service**: You are responsible for ensuring your use of this tool complies with [X (Twitter)'s Terms of Service](https://twitter.com/tos) and [Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement-and-policy).

2. **Respect Rate Limits**: Implement appropriate delays between requests to avoid overwhelming X (Twitter)'s servers. Excessive requests may result in temporary or permanent restrictions on your account.

3. **Use Responsibly**: 
   - Do not use this tool for spam, harassment, or any malicious activities
   - Respect user privacy and data protection regulations (GDPR, CCPA, etc.)
   - Only extract publicly available data
   - Do not redistribute or sell extracted data without proper authorization

4. **No Warranty**: This tool is provided "as is" without any warranties. The authors are not responsible for any consequences resulting from the use of this tool.

5. **Account Risk**: Using automated data extraction tools may violate X (Twitter)'s terms and could result in account suspension. Use at your own risk.

**Recommended Best Practices:**
- Implement rate limiting (e.g., 1-2 second delays between requests)
- Use reasonable request counts (start small, increase gradually)
- Cache results to minimize repeated requests
- Monitor your account for any warnings or restrictions

## Login Requirements

Some features require Twitter authentication:

**Works without login (Guest Session):**
- get_user_profile
- get_user_tweets

**Requires login:**
- get_user_followers
- get_user_followings
- get_user_media
- search_tweets

See [references/LOGIN_GUIDE.md](references/LOGIN_GUIDE.md) for detailed login instructions.

## Why Use the Skill Interface?

The `TwitterSkillInterface` is designed specifically for AI agents:

- **Dynamic Discovery**: Agents can query available skills and their parameters
- **Standardized Execution**: All skills use the same `execute_skill()` method
- **Structured Responses**: Consistent response format with metadata
- **Error Handling**: Graceful error handling with informative messages
- **Extensibility**: Easy to add new skills without changing the interface
