# linkedin-skills

LinkedIn automation Skills — directly uses your logged-in browser and real account, operating LinkedIn as an ordinary user.

Supports OpenClaw and all AI Agent platforms compatible with the `SKILL.md` format (e.g. Claude Code).

> **⚠️ Usage advice**: Although this project uses your real browser and account, you should still **control operation frequency** and avoid mass actions in a short time. Aggressive automation may trigger LinkedIn's rate limits or account restrictions.

## Features

| Skill | Description | Core Capabilities |
|-------|-------------|-------------------|
| **linkedin-auth** | Authentication | Login check, session management |
| **linkedin-publish** | Content Publishing | Text post / image post submission |
| **linkedin-explore** | Discovery | Search (posts, people, companies), feed browsing, post details, user profiles, company pages |
| **linkedin-interact** | Social Interaction | Like, comment, send connection request, send message |
| **linkedin-content-ops** | Compound Ops | Competitor analysis, trend tracking, engagement campaigns |
| **linkedin-lead-gen** | Lead Generation | Find prospects, build lead lists, outreach targeting |

Supports **chained operations** — you can give compound natural-language instructions and the Agent will automatically chain multiple skills. For example:

> "Search LinkedIn for people who work in DevOps at Series B startups, get their profiles, and draft a connection message for each"

The Agent will execute: search → filter → get profiles → draft messages → confirm → send.

## Installation

### Prerequisites

* Python >= 3.11
* [uv](https://docs.astral.sh/uv/) package manager
* Google Chrome browser

### Step 1: Install the project

**Option A: Download ZIP (recommended)**

Download from GitHub and extract to your Agent skills directory:

```
# OpenClaw
<openclaw-project>/skills/linkedin-skills/

# Claude Code
<your-project>/.claude/skills/linkedin-skills/
```

**Option B: Git Clone**

```bash
cd <your-agent-project>/skills/
git clone https://github.com/ceoqveda/linkedin-skills.git
```

Then install Python dependencies:

```bash
cd linkedin-skills
uv sync
```

### Step 2: Install the browser extension

The extension lets the AI operate LinkedIn in your browser using your real login session.

1. Open Chrome, navigate to `chrome://extensions/`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked**, select this project's `extension/` directory
4. Confirm the **LinkedIn Bridge** extension is enabled

Once installed, you're ready to go — all actions happen in your own browser, using your real account.

## Usage

### As an AI Agent skill (recommended)

After installing to a skills directory, just talk to the Agent in natural language. It will route your intent to the right skill automatically.

**Authentication:**

> "Check if I'm logged in to LinkedIn" / "Log out of LinkedIn"

**Search & Browse:**

> "Search LinkedIn for posts about AI agents" / "Show me the top posts on machine learning"

**Manage content:**

> "Post this update to my LinkedIn feed: ..."

**Interact:**

> "Like this post" / "Comment on this post: Great write-up!" / "Send a connection request to this person"

**Lead generation:**

> "Find people who work in sales at fintech companies in London"

**Compound operations:**

> "Analyze top posts in my feed this week and summarize the common themes"

### As a CLI tool

All features can be called directly from the command line, with JSON output for scripting.

```bash
# Check login
python scripts/cli.py check-login

# Browse home feed
python scripts/cli.py home-feed

# Search for people
python scripts/cli.py search --query "machine learning engineer" --type people

# Search for posts
python scripts/cli.py search --query "AI agents" --type content

# Search for companies
python scripts/cli.py search --query "fintech startup" --type companies

# Get a user profile
python scripts/cli.py user-profile --username "satyanadella"

# Get a company page
python scripts/cli.py company-profile --company-slug "microsoft"

# Get post detail
python scripts/cli.py get-post-detail --url "https://www.linkedin.com/feed/update/urn:li:activity:..."

# Submit a text post (content in a file)
python scripts/cli.py submit-post --content-file post.txt

# Submit an image post
python scripts/cli.py submit-image --content-file caption.txt --images /path/to/image.jpg

# Like a post
python scripts/cli.py like-post --url "https://www.linkedin.com/feed/update/urn:li:activity:..."

# Comment on a post
python scripts/cli.py comment-post --url "..." --content "Great insight!"

# Send a connection request
python scripts/cli.py send-connection --url "https://www.linkedin.com/in/username/"

# Send a connection request with a note
python scripts/cli.py send-connection --url "https://www.linkedin.com/in/username/" --note-file note.txt

# Send a direct message
python scripts/cli.py send-message --url "https://www.linkedin.com/in/username/" --content-file message.txt
```

> On first run, if Chrome is not open, the CLI will auto-launch it.

## CLI Command Reference

| Subcommand | Description |
|------------|-------------|
| `check-login` | Check login status, return username if logged in |
| `delete-cookies` | Log out (UI-based logout) |
| `home-feed` | Get home feed posts |
| `search` | Search LinkedIn (supports `--type people/content/companies`) |
| `get-post-detail` | Get full post content and comments |
| `user-profile` | Get user profile and recent activity |
| `company-profile` | Get company page info and posts |
| `submit-post` | Submit a text post |
| `submit-image` | Submit an image post |
| `like-post` | Like a post |
| `comment-post` | Comment on a post |
| `send-connection` | Send a connection request (optional `--note-file`) |
| `send-message` | Send a direct message to a connection |

Exit codes: `0` success · `1` not logged in · `2` error

## Project Structure

```
linkedin-skills/
├── extension/                  # Chrome Extension (MV3)
│   ├── manifest.json
│   └── background.js
├── scripts/                    # Python automation engine
│   ├── linkedin/               # Core automation library
│   │   ├── bridge.py           # Extension bridge client
│   │   ├── selectors.py        # CSS selectors (centralized)
│   │   ├── login.py            # Login check + logout
│   │   ├── feed.py             # Home feed
│   │   ├── search.py           # Search + filters
│   │   ├── post_detail.py      # Post detail + comment loading
│   │   ├── profile.py          # User + company profiles
│   │   ├── interact.py         # Like, comment, connect, message
│   │   ├── publish.py          # Post submission
│   │   ├── types.py            # Data types
│   │   ├── errors.py           # Exception hierarchy
│   │   ├── urls.py             # URL constants
│   │   └── human.py            # Behavior simulation
│   ├── cli.py                  # Unified CLI entry point
│   ├── bridge_server.py        # Local WebSocket bridge
│   └── image_downloader.py     # Image download with local cache
├── skills/                     # AI Agent skill definitions
│   ├── linkedin-auth/SKILL.md
│   ├── linkedin-publish/SKILL.md
│   ├── linkedin-explore/SKILL.md
│   ├── linkedin-interact/SKILL.md
│   ├── linkedin-content-ops/SKILL.md
│   └── linkedin-lead-gen/SKILL.md
├── SKILL.md                    # Skill router (routes to sub-skills)
├── pyproject.toml
└── README.md
```

## Architecture

```
AI Agent (natural language)
      ↓
scripts/cli.py              ← single entry point for all commands
      ↓
scripts/bridge_server.py    ← local WebSocket server (ws://localhost:9335)
      ↓
extension/ (Chrome)         ← reads/writes LinkedIn DOM in your browser
      ↓
LinkedIn.com (your real account)
```

## Security

- **No API keys required** — uses your existing browser session
- **Local only** — bridge server binds to `127.0.0.1:9335` only
- **No telemetry** — no data sent to third-party servers
- **Scoped permissions** — extension only has access to `linkedin.com` pages
- **Publish/interact requires confirmation** — destructive actions need explicit user approval

## Development

```bash
uv sync                    # Install dependencies
uv run ruff check .        # Lint
uv run ruff format .       # Format
uv run pytest              # Run tests
```

## License

MIT
