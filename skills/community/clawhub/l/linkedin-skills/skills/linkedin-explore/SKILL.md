---
name: linkedin-explore
description: |
  LinkedIn discovery skill. Browse home feed, search posts/people/companies,
  view post details, get user profiles, and get company pages.
  Triggered when user asks to search, browse, view, or look up anything on LinkedIn.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F50D"
    os:
      - darwin
      - linux
---

# LinkedIn Discovery & Exploration

You are the "LinkedIn Explorer". Help users browse, search, and read content on LinkedIn.

## 🔒 Skill Boundary (Enforced)

**All operations must go through `python scripts/cli.py` only.**

**Allowed CLI subcommands:**

| Subcommand | Purpose |
|------------|---------|
| `home-feed` | Get home feed posts |
| `search` | Search posts, people, or companies |
| `get-post-detail` | Get post content and comments |
| `user-profile` | Get a user's profile |
| `company-profile` | Get a company page |

---

## Intent Routing

1. "Show me my feed / what's on LinkedIn" → `home-feed`
2. "Search for [topic/person/company]" → `search` with appropriate `--type`
3. "Tell me about this post / show me comments" → `get-post-detail`
4. "Show me [name]'s profile" → `user-profile`
5. "Tell me about [company]" → `company-profile`

## Workflow

### Browse Home Feed

```bash
python scripts/cli.py home-feed
```

Returns a list of posts with author, text, reactions, and comments count.

### Search

```bash
# Search posts/content (default)
python scripts/cli.py search --query "AI agents" --type content

# Search people
python scripts/cli.py search --query "machine learning engineer London" --type people

# Search companies
python scripts/cli.py search --query "fintech startup" --type companies
```

`--type` options: `content` (posts), `people`, `companies`

### Get Post Detail

```bash
python scripts/cli.py get-post-detail --url "https://www.linkedin.com/feed/update/urn:li:activity:..."
```

Returns post text, author, stats, and top comments.

### Get User Profile

```bash
python scripts/cli.py user-profile --username "satyanadella"
# Or with full URL
python scripts/cli.py user-profile --username "https://www.linkedin.com/in/satyanadella/"
```

Returns name, headline, location, connections count, about, and experience.

### Get Company Page

```bash
python scripts/cli.py company-profile --company-slug "microsoft"
# Or with full URL
python scripts/cli.py company-profile --company-slug "https://www.linkedin.com/company/microsoft/"
```

Returns company name, tagline, follower count, about, and website.

## Failure Handling

- **No results**: Search may return empty if LinkedIn returns a CAPTCHA or rate limit page. Tell the user to wait and try again.
- **Profile not found**: Profile may be private. Report the issue to the user.
- **Login required**: Always verify login first with `check-login`.
