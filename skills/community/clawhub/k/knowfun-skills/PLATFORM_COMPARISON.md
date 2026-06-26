# Platform Comparison - Claude Code vs Cursor vs Cline vs OpenClaw

English | [简体中文](PLATFORM_COMPARISON_CN.md)

Detailed comparison of using Knowfun.io Skill across different AI coding platforms.

---

## 🎯 Quick Summary

| Platform | Best For | Experience | Setup Complexity |
|----------|----------|------------|------------------|
| **Claude Code** | Native integration | ⭐⭐⭐⭐⭐ Excellent | 🟢 Easy |
| **Cursor** | Terminal + AI | ⭐⭐⭐⭐ Very Good | 🟡 Moderate |
| **Cline** | Flexible workflows | ⭐⭐⭐⭐ Very Good | 🟡 Moderate |
| **OpenClaw** | Remote + Local AI | ⭐⭐⭐⭐ Very Good | 🟡 Moderate |

---

## 📊 Detailed Feature Comparison

### Command System

| Feature | Claude Code | Cursor | Cline | OpenClaw |
|---------|-------------|--------|-------|
| **Slash Commands** | ✅ `/knowfun` | ❌ No native support | ❌ No native support |
| **Natural Language** | ✅ "Create a course..." | ✅ "Use knowfun CLI..." | ✅ "Create a course..." |
| **CLI Access** | ✅ | ✅ | ✅ |
| **Auto-completion** | ✅ Built-in | ❌ | ❌ |

### Integration Level

| Aspect | Claude Code | Cursor | Cline | OpenClaw |
|--------|-------------|--------|-------|
| **Skill System** | ✅ Native SKILL.md | ⚠️ Rules file | ⚠️ Custom config |
| **Auto-invocation** | ✅ Description-based | ❌ Manual | ❌ Manual |
| **Permission Control** | ✅ Fine-grained | ❌ | ❌ |
| **Context Forking** | ✅ Supported | ❌ | ❌ |

### User Experience

| Aspect | Claude Code | Cursor | Cline | OpenClaw |
|--------|-------------|--------|-------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Learning Curve** | 🟢 Low | 🟡 Medium | 🟡 Medium |
| **Documentation** | ✅ Integrated | ⚠️ External | ⚠️ External |
| **Error Messages** | ✅ Clear | ✅ Clear | ✅ Clear |

---

## 🔍 Platform-Specific Details

### Claude Code

**Strengths:**
- ✅ **Native skill system** - First-class citizen
- ✅ **Slash commands** - `/knowfun create course "..."`
- ✅ **Auto-invocation** - Claude detects when to use skill
- ✅ **Tool restrictions** - Fine-grained permission control
- ✅ **Integrated docs** - Help built into skill
- ✅ **Version control** - Commit `.claude/skills/` to git

**Installation:**
```bash
mkdir -p ~/.claude/skills/knowfun
cp -r * ~/.claude/skills/knowfun/
```

**Usage:**
```bash
/knowfun create course "Python Basics"
```

**Best For:**
- Teams using Claude Code
- Projects needing fine-grained control
- Workflows requiring auto-invocation

---

### Cursor

**Strengths:**
- ✅ **CLI tool works great** - Full functionality
- ✅ **Natural language** - "Use knowfun to create..."
- ✅ **Terminal integration** - Direct CLI access
- ✅ **Rules file** - Guide Cursor's behavior
- ✅ **Fast execution** - Direct shell commands

**Limitations:**
- ❌ No native slash commands
- ❌ No auto-invocation
- ⚠️ Must ask Cursor to use CLI

**Installation:**
```bash
# Install CLI globally
sudo ln -s $(pwd)/scripts/knowfun-cli.sh /usr/local/bin/knowfun

# Add rules (optional)
cp integrations/cursor/.cursorrules .
```

**Usage:**

*Method 1: Terminal*
```bash
knowfun create course "Python Basics"
```

*Method 2: Ask Cursor*
```
Use knowfun CLI to create a course about "Python Basics"
```

**Best For:**
- Cursor users who prefer terminal workflows
- Projects already using Cursor
- Users comfortable with CLI tools

---

### Cline

**Strengths:**
- ✅ **CLI tool support** - Full API access
- ✅ **Flexible** - Can integrate various ways
- ✅ **Natural language** - Intuitive interaction
- ✅ **Config file** - Structured configuration
- ✅ **Extensible** - Custom tool definitions

**Limitations:**
- ❌ No native slash commands
- ❌ No auto-invocation
- ⚠️ Must configure manually

**Installation:**
```bash
# Install CLI
sudo ln -s $(pwd)/scripts/knowfun-cli.sh /usr/local/bin/knowfun

# Add config
mkdir -p .cline
cp integrations/cline/knowfun.json .cline/
```

**Usage:**

*Method 1: Terminal*
```bash
knowfun create course "Python Basics"
```

*Method 2: Ask Cline*
```
Create a Knowfun course about "Python Basics"
```

**Best For:**
- Cline/OpenClaw users
- Custom workflow integration
- Projects needing flexibility

---

## 🎯 Recommendation by Use Case

### Use Case: Personal Projects

**Recommended: Claude Code**
- Easiest setup
- Best integration
- Native experience

### Use Case: Team Collaboration

**Recommended: Claude Code**
- Version controllable (`.claude/skills/`)
- Consistent across team
- Fine-grained permissions

### Use Case: Already Using Cursor

**Recommended: Stay with Cursor**
- CLI tool works great
- No need to switch
- Same functionality

### Use Case: Already Using Cline

**Recommended: Stay with Cline**
- CLI tool integrates well
- Maintains workflow
- Full feature access

---

## 📈 Migration Path

### From Cursor to Claude Code

1. Keep CLI tool installed
2. Install Claude Code skill
3. Use `/knowfun` commands instead of CLI
4. Gradually adopt Claude Code features

### From Cline to Claude Code

1. Same as Cursor migration
2. Remove `.cline/` config if desired
3. Adopt native skill system

### From Claude Code to Others

1. CLI tool already works
2. Add platform-specific config
3. Use natural language or direct CLI

---

## 🔧 Technical Differences

### File Structure

**Claude Code:**
```
.claude/skills/knowfun/
├── SKILL.md              # Main definition
├── api-reference.md      # API docs
├── examples.md           # Examples
└── scripts/
    └── knowfun-cli.sh    # CLI tool
```

**Cursor:**
```
.cursorrules              # Rules file (optional)
/usr/local/bin/knowfun    # Global CLI link
```

**Cline:**
```
.cline/knowfun.json       # Config (optional)
/usr/local/bin/knowfun    # Global CLI link
```

### Configuration Format

**Claude Code:**
```yaml
---
name: knowfun
description: Create courses, posters, games, films
user-invocable: true
allowed-tools: Bash(curl *), Read, Write
---
```

**Cursor:**
```
# .cursorrules (plain text)
You have access to knowfun CLI...
[Instructions in natural language]
```

**Cline:**
```json
{
  "name": "Knowfun.io Integration",
  "commands": { ... },
  "environment": { ... }
}
```

---

## 💡 Tips by Platform

### Claude Code Tips

1. Use `/knowfun` for commands
2. Let Claude auto-invoke when relevant
3. Check help with `/help knowfun`
4. Commit skill to `.claude/` for team sharing

### Cursor Tips

1. Set up global CLI link for convenience
2. Add `.cursorrules` for better AI guidance
3. Use terminal for quick commands
4. Ask Cursor to use CLI for complex workflows

### Cline Tips

1. Configure `.cline/knowfun.json` for consistency
2. Use natural language for task delegation
3. Terminal access for direct control
4. Keep config in version control

---

## 🆚 Head-to-Head Example

**Task: Create a course about Python**

### Claude Code
```bash
# Option 1: Slash command
/knowfun create course "Introduction to Python"

# Option 2: Natural language
"Create a Knowfun course about Python introduction"
# Claude automatically detects and uses /knowfun
```

### Cursor
```bash
# Option 1: Terminal
knowfun create course "Introduction to Python"

# Option 2: Ask Cursor
"Use knowfun CLI to create a course about Python introduction"
```

### Cline
```bash
# Option 1: Terminal
knowfun create course "Introduction to Python"

# Option 2: Ask Cline
"Create a Knowfun course about Python introduction"
```

**Result: All produce the same output!** ✨

---

## 📊 Performance Comparison

| Aspect | Claude Code | Cursor | Cline | OpenClaw |
|--------|-------------|--------|-------|
| **Command Response** | Instant | Instant | Instant |
| **API Call Speed** | Same | Same | Same |
| **Task Processing** | Same | Same | Same |
| **Setup Time** | 30 seconds | 2 minutes | 2 minutes |
| **Documentation Access** | Built-in | External | External |

**Conclusion:** API performance is identical across all platforms. Differences are in UX and integration depth.

---

## 🎓 Learning Resources

### Claude Code Users
- Read: [README.md](README.md)
- Start: [QUICKSTART.md](QUICKSTART.md)
- Install: [INSTALLATION.md](INSTALLATION.md#claude-code-installation)

### Cursor Users
- Read: [README.md](README.md)
- Start: [QUICKSTART.md](QUICKSTART.md)
- Install: [INSTALLATION.md](INSTALLATION.md#cursor-installation)

### Cline Users
- Read: [README.md](README.md)
- Start: [QUICKSTART.md](QUICKSTART.md)
- Install: [INSTALLATION.md](INSTALLATION.md#cline-installation)

---

## 🔄 Cross-Platform Compatibility

**Good News:** The CLI tool and API are **100% compatible** across all platforms!

This means:
- ✅ Same commands work everywhere
- ✅ Same API endpoints
- ✅ Same results
- ✅ Easy to switch platforms
- ✅ Can use multiple platforms simultaneously

---

## 🎯 Final Recommendation

**Choose based on your current setup:**

- **Already using Claude Code?** ➜ Use the native skill
- **Already using Cursor?** ➜ Use the CLI + rules
- **Already using Cline?** ➜ Use the CLI + config
- **Starting fresh?** ➜ Choose Claude Code for best experience

**Remember:** You can always switch later - the CLI tool works everywhere!

---


---

### OpenClaw

**Strengths:**
- ✅ **Local-first AI** - Data stays on your machine
- ✅ **Remote access** - Control via Telegram, WhatsApp, Discord, Slack
- ✅ **Autonomous workflows** - Self-directed task execution
- ✅ **Persistent memory** - Remembers context across sessions
- ✅ **Browser automation** - Can interact with web applications
- ✅ **System integration** - Full file access and shell control
- ✅ **Extensible** - Can write its own extensions

**Limitations:**
- ❌ No native slash commands
- ❌ No auto-invocation (but AI interprets intent)
- ⚠️ Requires local installation

**Installation:**
```bash
# Install CLI
sudo ln -s $(pwd)/scripts/knowfun-cli.sh /usr/local/bin/knowfun

# Add skill definition (optional)
cp integrations/openclaw/knowfun-skill.json ~/.openclaw/skills/
```

**Usage:**

*Method 1: Terminal*
```bash
knowfun create course "Python Basics"
```

*Method 2: Natural Language*
```
"Create a Knowfun course about Python basics"
```

*Method 3: Remote via Chat*
```
@openclaw Create a Knowfun course about Python
```

**Best For:**
- OpenClaw users
- Remote content creation needs
- Automated workflows
- Mobile/on-the-go access

**Unique Features:**
- 📱 **Mobile Access**: Create content from your phone via chat apps
- 🤖 **Autonomous Loops**: Can monitor and notify when tasks complete
- 🔒 **Privacy**: Data stays local, not in cloud
- 🔧 **Self-Improving**: Can write and install its own extensions

