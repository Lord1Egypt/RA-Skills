# OpenClaw Command Cheatsheet

## Basic Commands

### Status and Help
```bash
# View OpenClaw status
openclaw status

# View all available commands
openclaw help

# View command help
openclaw [command] --help
```

### Version Information
```bash
# View version
openclaw version

# Check for updates
openclaw update check

# Execute update
openclaw update run
```

## Agent Management

### List and Manage
```bash
# List all agents
openclaw agents list

# Create new agent
openclaw agents create [name] [--model MODEL] [--thinking THINKING]

# View agent details
openclaw agents get [id]

# Remove agent
openclaw agents remove [id]

# Update agent configuration
openclaw agents update [id] [--model MODEL] [--thinking THINKING]
```

### Agent Sessions
```bash
# Start agent session
openclaw agents session [id]

# List active sessions
openclaw agents sessions

# End session
openclaw agents kill [session-id]
```

## Cron Jobs

### Basic Operations
```bash
# List all cron jobs
openclaw cron list

# View cron job details
openclaw cron get [id]

# Add cron job
openclaw cron add --name "Task Name" --schedule "0 8 * * *" --command "echo hello"

# Remove cron job
openclaw cron remove [id]

# Run cron job immediately
openclaw cron run [id]

# Disable/Enable cron job
openclaw cron disable [id]
openclaw cron enable [id]
```

### Scheduling Expression
```
*    *    *    *    *
┬    ┬    ┬    ┬    ┬
│    │    │    │    │
│    │    │    │    └── Day of week (0-7, 0 and 7 both represent Sunday)
│    │    │    └───── Month (1-12)
│    │    └────────── Day of month (1-31)
│    └─────────────── Hour (0-23)
└──────────────────── Minute (0-59)
```

## Skills Management

### Install and Update
```bash
# List installed skills
openclaw skills list

# Search skills
openclaw skills search [keyword]

# Install skill
openclaw skills install [skill-name] [--version VERSION]

# Update skill
openclaw skills update [skill-name]

# Uninstall skill
openclaw skills uninstall [skill-name]

# View skill details
openclaw skills info [skill-name]
```

### Local Skills
```bash
# Install from local directory
openclaw skills install-local [path]

# Package skill
openclaw skills package [skill-directory]
```

## Gateway Management

### Service Control
```bash
# Start gateway
openclaw gateway start

# Stop gateway
openclaw gateway stop

# Restart gateway
openclaw gateway restart

# View status
openclaw gateway status

# View logs
openclaw gateway logs [--follow]
```

### Configuration Management
```bash
# View configuration
openclaw config get [key]

# Set configuration
openclaw config set [key] [value]

# Delete configuration
openclaw config delete [key]

# List all configurations
openclaw config list

# Interactive configuration
openclaw configure
```

## Tools and Integrations

### Web Search
```bash
# Configure Brave API key
openclaw configure --section web

# Test search
openclaw web search "search query"
```

### Message Channels
```bash
# List message channels
openclaw channels list

# Test channel
openclaw channels test [channel-name]

# Send message
openclaw channels send [channel-name] --message "Message content"
```

### Node Management
```bash
# List nodes
openclaw nodes list

# Pair node
openclaw nodes pair

# View node details
openclaw nodes get [node-id]
```

## Workspace Management

### File Operations
```bash
# List workspace files
openclaw workspace ls [path]

# Read file
openclaw workspace read [file-path]

# Write file
openclaw workspace write [file-path] --content "Content"

# Edit file
openclaw workspace edit [file-path] --old "Old Text" --new "New Text"
```

### Project Management
```bash
# Initialize project
openclaw workspace init [project-name]

# Switch project
openclaw workspace use [project-name]

# List projects
openclaw workspace projects
```

## Diagnostics and Debugging

### System Diagnostics
```bash
# Run diagnostics
openclaw doctor

# View system information
openclaw system info

# View resource usage
openclaw system resources

# View processes
openclaw system processes
```

### Log Management
```bash
# View logs
openclaw logs [--follow] [--tail LINES]

# Clear logs
openclaw logs clear

# Set log level
openclaw logs level [DEBUG|INFO|WARN|ERROR]
```

## Advanced Features

### Subcommand Combinations
```bash
# Create cron job to run agent
openclaw cron add --name "Daily Report" --schedule "0 9 * * *" --command "openclaw agents session report-agent"

# Batch operations
openclaw agents list | grep "test-" | xargs -I {} openclaw agents remove {}
```

### Environment Variables
```bash
# Common environment variables
export OPENCLAW_CONFIG_PATH="~/.openclaw/config.yaml"
export OPENCLAW_LOG_LEVEL="INFO"
export OPENCLAW_WORKSPACE="/path/to/workspace"
```

## Example Workflows

### 1. Create Scheduled Report Task
```bash
# Create report agent
openclaw agents create daily-reporter --model "gpt-4" --thinking "detailed"

# Add scheduled task
openclaw cron add \
  --name "Daily 9 AM Report" \
  --schedule "0 9 * * *" \
  --command "openclaw agents session daily-reporter --task 'Generate daily report'"
```

### 2. Install and Configure Skill
```bash
# Search skill
openclaw skills search "weather"

# Install skill
openclaw skills install weather-skill

# Configure API key
openclaw config set weather.api_key "YOUR_API_KEY"

# Test skill
openclaw agents session main --task "What's the weather today?"
```

### 3. Troubleshooting Flow
```bash
# 1. Check status
openclaw status

# 2. View logs
openclaw logs --tail 50

# 3. Check configuration
openclaw config list

# 4. Restart service
openclaw gateway restart

# 5. Run diagnostics
openclaw doctor
```

## Shortcuts and Aliases

### Common Aliases (add to ~/.bashrc or ~/.zshrc)
```bash
alias oc='openclaw'
alias oc-status='openclaw status'
alias oc-logs='openclaw logs --tail 100'
alias oc-restart='openclaw gateway restart'
alias oc-agents='openclaw agents list'
alias oc-cron='openclaw cron list'
alias oc-skills='openclaw skills list'
```

### Quick Commands
```bash
# Quick status view
oc-status

# Quick log view
oc-logs

# Quick restart
oc-restart
```

---

**Last Updated**: 2026-03-15  
**Version**: 1.0  
**Compatible With**: OpenClaw v2.0+
