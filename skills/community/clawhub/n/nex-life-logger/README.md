# Nex Life Logger

**AI-powered local activity tracker. Your agent remembers everything you did on your computer.**

Built by **Nex AI** - Digital transformation for Belgian SMEs.

## What It Does

- Silently tracks browser history (Chrome, Edge, Brave, Firefox) and active window focus
- Captures YouTube video transcripts so the AI knows what was discussed, not just what was watched
- Generates hierarchical AI summaries (daily, weekly, monthly, yearly) of your computer activity
- Provides a powerful CLI to search, query, and export your personal history
- All activity data stays local on your machine. No telemetry. You own your data.
- LLM-powered features (summaries, AI search) require you to explicitly configure a provider. No external API calls are made until you do.

## Quick Install

```bash
# Via ClawHub
clawhub install nex-life-logger

# Or manual
git clone <repo-url>
cd clawhub-skill
bash setup.sh
```

## Example Usage

Ask your AI agent natural questions about your computer activity:

```
You: What was I working on yesterday afternoon?
Agent: Yesterday afternoon you spent about 3 hours working on a Python API project.
       You were primarily in VS Code, researching FastAPI documentation and
       watching a tutorial on async database patterns...

You: What YouTube videos did I watch about Docker this week?
Agent: This week you watched 4 Docker-related videos...

You: Search my history for anything about Kubernetes
Agent: Found 23 activities related to Kubernetes across the last month...

You: Generate a summary of my week
Agent: Generating weekly summary... This week was focused on backend development...
```

## Configuration

After installation, configure your LLM provider for AI-powered features:

```bash
# Set your API key
nex-life-logger config set-api-key

# Choose a provider (openai, qwen, groq, ollama)
nex-life-logger config set-provider openai

# Or set a specific model
nex-life-logger config set-model gpt-4o

# View current config
nex-life-logger config show
```

Supported providers: any OpenAI-compatible API (OpenAI, Qwen/DashScope, Groq, Ollama, LM Studio, or custom endpoints).

## Supported Browsers

- Google Chrome
- Microsoft Edge
- Brave Browser
- Mozilla Firefox

## Supported Platforms

- Linux (Ubuntu 22.04+, any systemd-based distro)
- macOS 12+
- Windows 11 (via WSL2)

## Privacy

Nex Life Logger is built privacy-first:

- All activity data is stored locally in `~/.life-logger/` on your machine
- No external API calls are made unless you explicitly configure an LLM provider for summary generation
- No telemetry, no analytics, no tracking of any kind
- No default API endpoints: you must configure a provider before any LLM features work
- Chat/messaging apps are automatically filtered out (WhatsApp, Discord, Slack, etc.)
- Sensitive windows are never logged (password managers, banking, incognito mode)
- Browser history files are copied to temp and securely deleted (overwritten with random bytes)
- API keys are stored via OS credential stores where available (Windows Credential Manager / DPAPI), with owner-only permission file fallback on Linux/macOS. For maximum security, use the AI_API_KEY environment variable instead.

## How It Works

1. **Background Collector**: A lightweight process runs every 30 seconds, reading browser history and tracking the active window. It classifies content as productive or not, fetches YouTube transcripts for productive videos, and stores everything in a local SQLite database.

2. **AI Summaries**: On a schedule (or on demand), the summarizer generates hierarchical summaries using your configured LLM. Daily summaries build from raw activities, weekly from dailies, monthly from weeklies, yearly from monthlies.

3. **CLI Interface**: The `nex-life-logger` command gives your AI agent (and you) full access to search, query, and export your data. The agent reads the output and presents it naturally.

4. **Keyword Extraction**: The system automatically extracts tools, languages, topics, and projects from your activity data using pattern matching, making it easy to track trends.

## CLI Reference

```
nex-life-logger search <query>          Search all tracked data
nex-life-logger summary <period>        View AI summaries
nex-life-logger activities [options]    View raw activities
nex-life-logger keywords [options]      View extracted keywords
nex-life-logger transcript <video_id>   Get a YouTube transcript
nex-life-logger transcripts             List recent transcripts
nex-life-logger stats                   Database statistics
nex-life-logger generate <period>       Generate AI summary
nex-life-logger export <format>         Export data (json/csv/html)
nex-life-logger service <action>        Manage collector service
nex-life-logger config <action>         View/set configuration
```

## Credits

- **Built by**: Nex AI (https://nex-ai.be)
- **Author**: Kevin Blancaflor
- **License**: MIT-0

## License

MIT No Attribution (MIT-0). See [LICENSE](LICENSE) for details.
