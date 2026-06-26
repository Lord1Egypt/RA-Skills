# OpenClaw Best Practices Guide

## Table of Contents
1. [Configuration Management](#configuration-management)
2. [Agent Design](#agent-design)
3. [Cron Job Optimization](#cron-job-optimization)
4. [Skills Usage](#skills-usage)
5. [Workspace Organization](#workspace-organization)
6. [Performance Optimization](#performance-optimization)
7. [Security Practices](#security-practices)
8. [Troubleshooting](#troubleshooting)

## Configuration Management

### Layered Configuration Strategy
```yaml
# 1. System-level config (~/.openclaw/config.yaml)
system:
  log_level: INFO
  workspace: /opt/openclaw/workspace

# 2. Project-level config (workspace/.openclaw/config.yaml)
project:
  agents:
    default_model: gpt-4
  tools:
    web_search:
      enabled: true

# 3. Environment variable overrides
export OPENCLAW_LOG_LEVEL=DEBUG
export OPENCLAW_MODEL=gpt-4-turbo
```

### Configuration Validation
```bash
# Validate configuration syntax
openclaw config validate

# Test configuration
openclaw config test

# Backup configuration
cp ~/.openclaw/config.yaml ~/.openclaw/config.yaml.backup.$(date +%Y%m%d)
```

### Configuration Version Control
```bash
# Add config to version control
git add ~/.openclaw/config.yaml
git commit -m "Update OpenClaw configuration"

# Use environment-specific configs
ln -sf ~/.openclaw/config.${ENV}.yaml ~/.openclaw/config.yaml
```

## Agent Design

### Agent Type Selection
| Type | Use Case | Recommended Model |
|------|----------|-------------------|
| **General** | Daily conversations, Q&A | GPT-4, Claude-3 |
| **Specialized** | Code development, data analysis | Codex, Claude-Code |
| **Task-oriented** | Cron jobs, automation | GPT-3.5-turbo |
| **Memory-based** | Long-term conversation, context retention | GPT-4-128k |

### Agent Configuration Optimization
```yaml
# Optimization example
agent:
  name: "code-reviewer"
  model: "claude-3-opus"
  thinking: "detailed"  # Enable deep thinking
  temperature: 0.2      # Low randomness, high consistency
  max_tokens: 4000      # Reasonable output length limit
  tools:                # Enable only necessary tools
    - read
    - edit
    - exec
  memory:
    enabled: true       # Enable memory
    retention_days: 30  # Retain for 30 days
```

### Agent Lifecycle Management
```bash
# 1. Create with purpose
openclaw agents create code-helper --model "claude-3-sonnet" --description "Code assistant"

# 2. Regular performance evaluation
openclaw agents evaluate [agent-id] --metrics "accuracy,speed,cost"

# 3. Adjust based on usage
openclaw agents update [agent-id] --model "gpt-4" --thinking "fast"

# 4. Archive inactive agents
openclaw agents archive [agent-id]
```

## Cron Job Optimization

### Scheduling Strategy
```bash
# Avoid peak hours
# ❌ Bad: Runs at exact hour (may conflict with other services)
openclaw cron add --schedule "0 * * * *" --command "..."

# ✅ Good: Random offset
openclaw cron add --schedule "17 * * * *" --command "..."

# Distributed scheduling
# Multiple tasks staggered in time
openclaw cron add --name "task-1" --schedule "0 8 * * *" --command "..."
openclaw cron add --name "task-2" --schedule "30 8 * * *" --command "..."
openclaw cron add --name "task-3" --schedule "0 9 * * *" --command "..."
```

### Task Design Principles
1. **Single Responsibility**: Each task does one thing
2. **Idempotency**: Task can be re-executed with consistent results
3. **Timeout Control**: Set reasonable timeouts to prevent hanging
4. **Error Handling**: Log errors, graceful degradation
5. **Resource Limits**: Control CPU/memory usage

### Monitoring and Alerting
```bash
# Add health check job
openclaw cron add \
  --name "health-check" \
  --schedule "*/5 * * * *" \
  --command "openclaw status | grep -q 'healthy' || echo 'System abnormal'"

# Job execution logging
openclaw cron add \
  --name "daily-report" \
  --schedule "0 9 * * *" \
  --command "openclaw agents session reporter --task 'Generate report' >> /var/log/openclaw/report.log 2>&1"
```

## Skills Usage

### Skill Selection Criteria
1. **Official Certified**: Prefer official or community-validated skills
2. **Maintenance Status**: Check last update time, issue count
3. **Clear Dependencies**: Explicit dependencies and system requirements
4. **Complete Documentation**: Includes usage examples and troubleshooting
5. **Performance Impact**: Evaluate effect on system performance

### Skill Installation Flow
```bash
# 1. Search skill
openclaw skills search "weather"

# 2. View details
openclaw skills info weather-skill

# 3. Test environment
openclaw skills test weather-skill --dry-run

# 4. Install
openclaw skills install weather-skill --version "1.2.0"

# 5. Verify
openclaw skills verify weather-skill
```

### Skill Development Standards
```markdown
# Skill Structure
skill-name/
├── SKILL.md          # Main documentation
├── scripts/          # Executable scripts
├── references/       # Reference documents
├── assets/           # Resource files
└── tests/            # Test files

# Version Management
- Use semantic versioning (semver)
- Changelog for each version
- Backward compatibility guarantee
```

## Workspace Organization

### Directory Structure
```
workspace/
├── agents/           # Agent configurations
│   ├── general/      # General-purpose agents
│   ├── specialized/  # Specialized agents
│   └── archived/     # Archived agents
├── projects/         # Project files
│   ├── project-a/
│   ├── project-b/
│   └── templates/
├── skills/           # Local skills
│   ├── installed/    # Installed
│   └── custom/       # Custom
├── logs/             # Log files
│   ├── agents/
│   ├── cron/
│   └── system/
├── config/           # Configuration files
│   ├── environments/ # Environment configs
│   └── backups/      # Config backups
└── memory/           # Memory storage
    ├── daily/        # Daily records
    ├── projects/     # Project memories
    └── knowledge/    # Knowledge base
```

### File Naming Conventions
```bash
# Use meaningful names
✅ project-specification-v1.2.md
❌ doc1.md

# Include date version
✅ daily-report-2026-03-15.md
✅ meeting-notes-2026-03-15-10-30.md

# Use standard extensions
✅ script.py, data.json, config.yaml
❌ script, data.txt, config
```

### Version Control Integration
```bash
# .gitignore example
.openclaw/cache/
.openclaw/logs/*.log
workspace/logs/
workspace/memory/temp/
*.swp
*.tmp
```

## Performance Optimization

### Resource Monitoring
```bash
# Monitor commands
openclaw system resources --watch
openclaw system processes --sort memory
openclaw logs --grep "slow" --tail 100

# Performance benchmark
openclaw benchmark agents --count 10
openclaw benchmark tools --tool web_search
```

### Cache Strategy
```yaml
# Configure cache
cache:
  enabled: true
  ttl: 3600  # 1 hour
  max_size: 100MB
  
  # Cache types
  types:
    - web_search
    - api_calls
    - file_reads
```

### Concurrency Control
```bash
# Limit concurrency
openclaw config set system.max_concurrent_agents 5
openclaw config set system.max_concurrent_tools 10

# Queue management
openclaw queue list
openclaw queue stats
openclaw queue clear --older-than 1h
```

## Security Practices

### Access Control
```bash
# Use principle of least privilege
openclaw config set security.default_permission "readonly"

# Enable authentication
openclaw config set security.authentication true
openclaw config set security.allowed_users "user1,user2"

# API key management
openclaw secrets set brave_api_key "xxx"
openclaw secrets list
openclaw secrets rotate brave_api_key
```

### Audit Logs
```bash
# Enable detailed logging
openclaw config set audit.enabled true
openclaw config set audit.level "detailed"

# Regular review
openclaw audit review --days 7
openclaw audit export --format csv --output audit-report.csv
```

### Data Protection
```yaml
# Privacy configuration
privacy:
  # Exclude sensitive information
  exclude_patterns:
    - "password"
    - "api_key"
    - "token"
    - "secret"
  
  # Auto cleanup
  retention_days: 30
  auto_clean: true
  
  # Encrypted storage
  encryption:
    enabled: true
    algorithm: aes-256-gcm
```

## Troubleshooting

### Diagnosis Flow
```bash
# 1. Quick check
openclaw status
openclaw doctor

# 2. View logs
openclaw logs --tail 100 --level ERROR
openclaw logs --grep "exception" --tail 50

# 3. Check configuration
openclaw config validate
openclaw config test --section agents

# 4. Test components
openclaw test agents
openclaw test tools
openclaw test network

# 5. Resource check
openclaw system resources
df -h /  # Disk space
free -h  # Memory usage
```

### Common Issues and Solutions

#### Agent Unresponsive
```bash
# Check agent status
openclaw agents get [agent-id] --verbose

# Restart agent
openclaw agents restart [agent-id]

# Check model availability
openclaw test model [model-name]
```

#### Cron Job Failure
```bash
# View job logs
openclaw cron logs [task-id]

# Manually test job
openclaw cron run [task-id] --dry-run

# Check scheduler
openclaw cron status
```

#### Skill Installation Failure
```bash
# Check dependencies
openclaw skills info [skill-name] --dependencies

# Check permissions
ls -la ~/.openclaw/skills/

# Clean cache
openclaw skills clean-cache
```

### Recovery Strategies
```bash
# Create backup point
openclaw backup create --name "before-update"

# List backups
openclaw backup list

# Restore backup
openclaw backup restore [backup-id]

# Emergency recovery
openclaw emergency-reset --keep-data
```

---

**Best Practices Summary**:
1. **Config as Code**: Version control all configurations
2. **Monitor First**: Establish monitoring before deployment
3. **Gradual Deployment**: Test first, then small scale, finally full-scale
4. **Documentation Driven**: Write docs first, implement second
5. **Secure by Default**: Use most secure settings by default

**Last Updated**: 2026-03-15  
**Version**: 1.0
