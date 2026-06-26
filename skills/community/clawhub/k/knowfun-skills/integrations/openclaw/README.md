# Knowfun Skills for OpenClaw

English | [简体中文](README_CN.md)

Integration guide for using Knowfun.io content generation with OpenClaw AI assistant.

## What is OpenClaw?

[OpenClaw](https://openclaw.ai/) is an open-source personal AI assistant that runs locally on your machine. It provides:

- 🤖 Autonomous agent capabilities with persistent memory
- 💬 Access via chat apps (WhatsApp, Telegram, Discord, Slack)
- 🖥️ Full system control (file access, shell commands)
- 🌐 Browser automation
- 🔧 Extensible skill system
- 🏠 Local-first (your data stays on your machine)

## What Does This Integration Do?

This integration enables OpenClaw to generate educational content using Knowfun.io:

- 📚 **Courses** - Interactive presentations with narration
- 🎨 **Posters** - Visual infographics and marketing materials
- 🎮 **Games** - Interactive learning experiences
- 🎬 **Films** - Educational videos and documentaries

## Installation

### Step 1: Install the Knowfun CLI Tool

```bash
# Install from npm (recommended)
npm install -g knowfun-skills

# Or clone the repository and link manually
git clone https://github.com/MindStarAI/KnowFun-Skills.git
cd KnowFun-Skills
sudo ln -s $(pwd)/scripts/knowfun-cli.sh /usr/local/bin/knowfun
chmod +x scripts/knowfun-cli.sh
```

### Step 2: Configure API Key

Get your API key from [Knowfun.io API Platform](https://www.knowfun.io/api-platform):

```bash
# Set environment variable (temporary)
export KNOWFUN_API_KEY="kf_your_api_key_here"

# Or add to shell profile (permanent)
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Verify Installation

```bash
# Test CLI tool
knowfun credits

# Expected output:
# ✅ Available: 1,000 credits
# 📊 Total Earned: 1,500 credits
# 📉 Total Used: 500 credits
```

### Step 4: Configure OpenClaw (Optional)

If OpenClaw supports custom skill definitions, you can add this integration:

```bash
# Copy skill definition to OpenClaw's skill directory
# (Adjust path based on your OpenClaw installation)
cp integrations/openclaw/knowfun-skill.json ~/.openclaw/skills/
```

## Usage

### Method 1: Direct CLI Commands

Execute CLI commands directly through OpenClaw:

```bash
# Create a course
knowfun create course "Introduction to Python Programming"

# Check status
knowfun status <taskId>

# Get results
knowfun detail <taskId>
```

### Method 2: Natural Language (Recommended)

Ask OpenClaw in natural language:

```
You: "Create a Knowfun course about machine learning basics"

OpenClaw: *executes knowfun create course "Machine Learning Basics"*
          *monitors task status*
          *returns result URL when complete*
```

### Method 3: Remote Access via Chat Apps

Use OpenClaw through Telegram, WhatsApp, or other chat apps:

**Via Telegram:**
```
You: @openclaw Create a Knowfun poster about climate change

OpenClaw: 🎨 Creating poster...
          📊 Task ID: abc-123
          ⏳ Processing...
          ✅ Complete! https://r2.knowfun.io/posters/xxx.html
```

## Examples

### Example 1: Create and Monitor a Course

```bash
# Create the course
TASK_ID=$(knowfun create course "JavaScript Fundamentals: Variables, Functions, and Objects" | grep -o 'Task ID: [^"]*' | cut -d' ' -f3)

# Wait and check status
sleep 180  # Wait 3 minutes
knowfun status $TASK_ID

# Get full details
knowfun detail $TASK_ID
```

### Example 2: Batch Content Creation

```bash
# Create multiple pieces of content
knowfun create course "Python Basics"
knowfun create poster "Web Development Stack"
knowfun create game "Learn Git Commands"

# List all tasks
knowfun list
```

### Example 3: Natural Language Workflow

```
You: "Create a Knowfun course about Docker, wait for it to complete, and share the URL"

OpenClaw:
- Executes: knowfun create course "Docker Containers and Orchestration"
- Monitors status every 30 seconds
- When complete, fetches detail
- Responds: "✅ Course ready! https://r2.knowfun.io/courses/xxx.html"
```

### Example 4: Automated Content Pipeline

Ask OpenClaw to create a complete content series:

```
You: "Create a series of Knowfun content about React:
      1. A course on React basics
      2. A poster showing React component lifecycle
      3. A game for practicing hooks"

OpenClaw:
- Creates all three pieces of content
- Monitors each task
- Reports progress
- Delivers all URLs when complete
```

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Generate content | `knowfun create course "Topic"` |
| `status` | Check task status | `knowfun status <taskId>` |
| `detail` | Get task details | `knowfun detail <taskId>` |
| `list` | List recent tasks | `knowfun list 10` |
| `credits` | Check credit balance | `knowfun credits` |
| `schema` | Get config options | `knowfun schema` |

## Content Types

| Type | Description | Processing Time | Cost |
|------|-------------|-----------------|------|
| **course** | Interactive presentations | 2-5 minutes | 100 credits |
| **poster** | Visual infographics | 1-3 minutes | 100 credits |
| **game** | Interactive learning | 3-7 minutes | 100 credits |
| **film** | Educational videos | 5-10 minutes | 100 credits |

## Error Handling

OpenClaw can handle errors gracefully:

- **401 Unauthorized**: Check API key configuration
- **402 Insufficient Credits**: Visit [API Platform](https://www.knowfun.io/api-platform) to get more
- **429 Rate Limited**: Wait 60 seconds before retry
- **404 Not Found**: Verify taskId is correct

## Tips & Best Practices

### For OpenClaw Users

1. **Use Natural Language**: Let OpenClaw interpret your intent
   ```
   ✅ "Create a course about Python"
   ❌ knowfun create course "Python"
   ```

2. **Automate Workflows**: Chain operations together
   ```
   "Create a course, wait for completion, then create a related poster"
   ```

3. **Remote Content Creation**: Use chat apps for on-the-go content generation
   ```
   Telegram: "Create a Knowfun game about SQL queries"
   ```

4. **Batch Operations**: Check credits first
   ```
   "Check my Knowfun credits, then create 3 courses"
   ```

### Content Creation Tips

- **Be Specific**: Detailed descriptions yield better results
- **Structure Content**: For courses, outline key concepts
- **Visual Preferences**: For posters, mention style preferences
- **Learning Objectives**: For games, specify what to teach
- **Narrative Structure**: For films, outline the story

## Troubleshooting

### Issue: "Command not found: knowfun"

**Solution:**
```bash
# Check if CLI is in PATH
which knowfun

# If not found, create symlink
sudo ln -s /path/to/knowfun-skills/scripts/knowfun-cli.sh /usr/local/bin/knowfun
```

### Issue: "API Key not found"

**Solution:**
```bash
# Check if set
echo $KNOWFUN_API_KEY

# Set it
export KNOWFUN_API_KEY="kf_your_key"
```

### Issue: "Insufficient credits"

**Solution:**
Visit https://www.knowfun.io/api-platform to manage your account

## Advanced Usage

### Custom Skill Integration

If OpenClaw supports custom skills, you can define automation rules:

```json
{
  "trigger": "create knowfun content",
  "action": "execute CLI command",
  "monitor": "poll status until complete",
  "notify": "send result URL"
}
```

### Webhook Integration

Set up webhooks for task completion notifications (if OpenClaw supports):

```bash
# In API call, include callbackUrl
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -d '{"callbackUrl": "http://your-openclaw-instance/webhook"}'
```

## Resources

- **Knowfun Skills Documentation**: [README.md](../../README.md)
- **API Reference**: [api-reference.md](../../api-reference.md)
- **Examples**: [examples.md](../../examples.md)
- **OpenClaw Website**: https://openclaw.ai/
- **Knowfun.io**: https://www.knowfun.io

## Support

- **Issues**: [GitHub Issues](https://github.com/MindStarAI/KnowFun-Skills/issues)
- **API Platform**: https://www.knowfun.io/api-platform
- **Documentation**: https://www.knowfun.io/docs

---

