# Hive Task Router - Configuration Guide

## Overview

This document provides detailed configuration information for the Hive Task Router system.

**Universal Model Support:** Works with any AI model provider (Bailian, OpenAI, Anthropic, Google, etc.) via environment variable configuration.

---

## System Architecture

The Hive Task Router uses a **three-layer architecture**:

```
┌─────────────────────────────────────┐
│  Layer 1: Task Routing              │
│  - Keyword recognition              │
│  - Model selection                  │
│  - Execution mode decision          │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Layer 2: Session Isolation         │
│  - Fixed sessions per task type     │
│  - Model specialization             │
│  - Context preservation             │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Layer 3: Subagent Elasticity       │
│  - Parallel execution               │
│  - Dynamic scaling                  │
│  - Auto cleanup                     │
└─────────────────────────────────────┘
```

---

## Model Configuration

### Required Models (Example: Bailian)

Ensure these models are available in your OpenClaw configuration:

| Model | Purpose | Task Types |
|-------|---------|------------|
| `bailian/qwen3.5-plus` | General purpose, cost-effective | chat, doc |
| `bailian/qwen3-max-2026-01-23` | Advanced reasoning, search | web |
| `bailian/qwen3-coder-plus` | Code specialization | code, data |

### Model Configuration for Different Providers

**Bailian (通义千问):**
```bash
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"
export HIVE_MODEL_DATA="bailian/qwen3-coder-plus"
```

**OpenAI:**
```bash
export HIVE_MODEL_CODE="openai/gpt-4"
export HIVE_MODEL_WEB="openai/gpt-4-turbo"
export HIVE_MODEL_CHAT="openai/gpt-3.5-turbo"
export HIVE_MODEL_DOC="openai/gpt-3.5-turbo"
export HIVE_MODEL_DATA="openai/gpt-4"
```

**Anthropic (Claude):**
```bash
export HIVE_MODEL_CODE="anthropic/claude-3-5-sonnet"
export HIVE_MODEL_WEB="anthropic/claude-3-opus"
export HIVE_MODEL_CHAT="anthropic/claude-3-haiku"
export HIVE_MODEL_DOC="anthropic/claude-3-haiku"
export HIVE_MODEL_DATA="anthropic/claude-3-5-sonnet"
```

**Google (Gemini):**
```bash
export HIVE_MODEL_CODE="google/gemini-pro"
export HIVE_MODEL_WEB="google/gemini-pro"
export HIVE_MODEL_CHAT="google/gemini-pro"
export HIVE_MODEL_DOC="google/gemini-pro"
export HIVE_MODEL_DATA="google/gemini-pro"
```

**Mixed Providers (Best-in-Class):**
```bash
# Use the best model for each task type
export HIVE_MODEL_CODE="anthropic/claude-3-5-sonnet"  # Best for code
export HIVE_MODEL_WEB="openai/gpt-4-turbo"           # Best for search
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"        # Cost-effective
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"         # Cost-effective
export HIVE_MODEL_DATA="anthropic/claude-3-5-sonnet" # Best for analysis
```

### Verify Models

```bash
# List available models
openclaw models list

# Filter for specific provider
openclaw models list | grep bailian

# Check specific model
openclaw models list | grep qwen3-coder-plus
```

---

## Environment Variables

### Required Variables

Set these before using the router:

```bash
# Minimum required
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"

# Optional (defaults to chat model)
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"
export HIVE_MODEL_DATA="bailian/qwen3-coder-plus"
```

### Optional Variables

```bash
# Custom session IDs
export HIVE_SESSION_CODE="custom:code:session"
export HIVE_SESSION_WEB="custom:web:session"
export HIVE_SESSION_CHAT="custom:chat:session"

# Concurrency limit
export HIVE_MAX_CONCURRENT=10

# Debug mode
export HIVE_DEBUG=1
```

### Persistent Configuration

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Hive Task Router Configuration
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
export HIVE_MODEL_DOC="bailian/qwen3.5-plus"
export HIVE_MODEL_DATA="bailian/qwen3-coder-plus"
export HIVE_MAX_CONCURRENT=10
```

---

## Task Type Configuration

### Keyword Customization

You can customize keywords in `router.sh` by modifying these variables:

```bash
CODE_KEYWORDS="代码 编程 脚本 函数 nodejs react vue ..."
WEB_KEYWORDS="搜索 查找 调研 研究 github 项目 趋势 ..."
CHAT_KEYWORDS="你好 谢谢 再见 今天 明天 安排 ..."
DOC_KEYWORDS="文档 说明 教程 指南 手册 readme ..."
DATA_KEYWORDS="数据 分析 统计 图表 可视化 excel ..."
```

### Priority Rules

The system uses this priority order when multiple keywords match:

1. **web** (Priority 1 - Highest)
2. **code** (Priority 2)
3. **data** (Priority 3)
4. **doc** (Priority 4)
5. **chat** (Priority 5 - Default)

**Example:**
```
Task: "搜索如何用 Node.js 写代码"
Matches: web (搜索), code (Node.js, 代码)
Result: web (higher priority wins)
```

---

## Session Configuration

### Fixed Sessions

Recommended session IDs for task type isolation:

| Session ID | Model | Purpose |
|------------|-------|---------|
| `agent:main:code` | qwen3-coder-plus | Code development tasks |
| `agent:main:web` | qwen3-max-2026-01-23 | Research and search tasks |
| `agent:main:chat` | qwen3.5-plus | Daily conversation |

### Create Fixed Sessions

```bash
# Code session
openclaw agent \
  --session-id agent:main:code \
  --model bailian/qwen3-coder-plus \
  --message "Initialize code session"

# Web session
openclaw agent \
  --session-id agent:main:web \
  --model bailian/qwen3-max-2026-01-23 \
  --message "Initialize web session"

# Chat session
openclaw agent \
  --session-id agent:main:chat \
  --model bailian/qwen3.5-plus \
  --message "Initialize chat session"
```

---

## Subagent Configuration

### Concurrency Limits

| Scenario | Recommended Max | Notes |
|----------|----------------|-------|
| Light workload | 3-5 subagents | Safe for most cases |
| Normal workload | 5-10 subagents | Recommended range |
| Heavy workload | 10-20 subagents | Monitor API quota |
| Batch processing | 20+ subagents | Execute in batches |

### Parallel Execution Pattern

```bash
# Start multiple subagents
for task in "Task A" "Task B" "Task C" "Task D" "Task E"; do
    openclaw sessions spawn \
        --mode run \
        --runtime subagent \
        --model bailian/qwen3-max-2026-01-23 \
        --task "$task" &
done

# Wait for all to complete
wait

# Collect results
echo "All tasks completed!"
```

### Timeout Configuration

For long-running tasks, consider setting timeouts:

```bash
# With timeout (if supported by your OpenClaw version)
openclaw sessions spawn \
    --mode run \
    --runtime subagent \
    --model bailian/qwen3-max-2026-01-23 \
    --task "Long research task" \
    --timeout 300  # 5 minutes
```

---

## Performance Tuning

### Optimization Tips

1. **Use appropriate models**
   - Don't use qwen3-max for simple chat tasks
   - Don't use qwen3.5-plus for complex code

2. **Batch similar tasks**
   - Group research tasks together
   - Process with same model for efficiency

3. **Monitor API usage**
   - Check quota regularly
   - Implement rate limiting if needed

4. **Clean up old sessions**
   - Archive completed sessions
   - Remove unused session data

5. **Use environment variables**
   - Set once in `.bashrc` or `.zshrc`
   - Different configs for different projects

### Performance Benchmarks

| Task | Traditional | Hive Router | Improvement |
|------|-------------|-------------|-------------|
| Single code task | 60s | 60s | Same |
| 3 research tasks (sequential) | 180s | 180s | Same |
| 3 research tasks (parallel) | 180s | 60s | **3x** ⚡ |
| Mixed workload (5 tasks) | 300s | 90s | **3.3x** ⚡ |

---

## Troubleshooting

### Common Issues

#### Issue: Router script not found
```bash
# Make sure script is executable
chmod +x router.sh

# Run with full path
bash /path/to/router.sh "task"
```

#### Issue: Model not available
```bash
# Check available models
openclaw models list

# Update environment variables with available models
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
```

#### Issue: Wrong model used
```bash
# Verify environment variables are set
echo $HIVE_MODEL_CODE
echo $HIVE_MODEL_WEB

# Set them explicitly before running router.sh
export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
bash router.sh "task"
```

#### Issue: Subagent fails to start
```bash
# Check OpenClaw status
openclaw status

# Retry with different model
# Reduce concurrent subagent count
```

#### Issue: Task type misidentified
```bash
# Add more specific keywords to router.sh
# Edit identify_task_type() function
```

---

## Integration Examples

### CI/CD Pipeline

```yaml
# .github/workflows/task-router.yml
name: Task Router Test

on: [push]

jobs:
  test-router:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install OpenClaw
        run: npm install -g openclaw
      - name: Configure models
        run: |
          export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
          export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
          export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
      - name: Test router script
        run: |
          chmod +x router.sh
          ./router.sh "Test task"
```

### Shell Alias

Add to your `.bashrc` or `.zshrc`:

```bash
# Quick router access
alias hivert='bash /path/to/hive-task-router/router.sh'

# Usage
hivert "帮我写个脚本"
```

### VS Code Integration

```json
// .vscode/settings.json
{
  "terminal.integrated.profiles.osx": {
    "Hive Router": {
      "path": "bash",
      "args": ["-c", "bash /path/to/router.sh"]
    }
  }
}
```

### Project-Specific Config

Create `.hive-env` in your project root:

```bash
# .hive-env
HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
HIVE_MODEL_CHAT="bailian/qwen3.5-plus"
HIVE_MAX_CONCURRENT=5
```

Load it before using:

```bash
source .hive-env
bash router.sh "task"
```

---

## Security Considerations

1. **API Key Protection**
   - Never commit API keys to version control
   - Use environment variables for secrets
   - Add `.hive-env` to `.gitignore`

2. **Task Content**
   - Don't send sensitive data to subagents
   - Review subagent outputs before using

3. **Resource Limits**
   - Set reasonable concurrency limits
   - Monitor API quota usage
   - Implement rate limiting if needed

4. **Model Costs**
   - Track usage per model
   - Use cost-effective models for simple tasks
   - Set budget alerts if available

---

## Updates and Maintenance

### Check for Updates

```bash
# If installed via ClawHub
clawhub check-updates hive-task-router

# Manual check - compare with repository
```

### Update Procedure

```bash
# Backup current configuration
cp -r hive-task-router hive-task-router.backup

# Install update
clawhub update hive-task-router

# Verify configuration
bash hive-task-router/router.sh "test"

# Restore environment variables if needed
source ~/.hive-config
```

### Backup Configuration

```bash
# Export current configuration
echo "export HIVE_MODEL_CODE=\"$HIVE_MODEL_CODE\"" > ~/.hive-config
echo "export HIVE_MODEL_WEB=\"$HIVE_MODEL_WEB\"" >> ~/.hive-config
echo "export HIVE_MODEL_CHAT=\"$HIVE_MODEL_CHAT\"" >> ~/.hive-config
echo "export HIVE_MODEL_DOC=\"$HIVE_MODEL_DOC\"" >> ~/.hive-config
echo "export HIVE_MODEL_DATA=\"$HIVE_MODEL_DATA\"" >> ~/.hive-config
echo "export HIVE_MAX_CONCURRENT=\"$HIVE_MAX_CONCURRENT\"" >> ~/.hive-config

# Source it in .bashrc or .zshrc
echo "source ~/.hive-config" >> ~/.bashrc
```

---

## Support

- **Documentation:** See `SKILL.md` for usage examples
- **Issues:** Report bugs or feature requests
- **Contributions:** Pull requests welcome
- **Community:** Join OpenClaw Discord for discussions

---

*Version: 1.0.0*  
*Last Updated: 2026-03-12*  
*Author: qiongcao*  
*Universal Model Support: Yes*
