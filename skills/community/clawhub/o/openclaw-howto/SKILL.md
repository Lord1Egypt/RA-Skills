---
name: openclaw-howto
description: OpenClaw HowTo skill — the accurate, reliable guide for using OpenClaw. Provides authoritative answers on OpenClaw features, configurations, CLI commands, troubleshooting, and best practices. Supports dual modes: 1) Web Search mode (using OpenClaw built-in or user-configured web_search tool for online queries); 2) Local mode (obtaining information via CLI/config/knowledge base). Will remember user configuration after first use and no longer ask repeatedly.
metadata:
  requires:
    bins: ["openclaw"]
    tools: ["read", "exec"]
  optional:
    tools: ["web_search", "web_fetch", "browser"]
  features:
    - auto_memory_cache
    - graceful_degradation
    - dual_mode_search
  keywords: ["openclaw", "configuration", "agents", "cron", "skills", "cli", "troubleshooting"]
---

# OpenClaw HowTo - OpenClaw HowTo Skill

Use this skill to become an OpenClaw expert, accurately understanding OpenClaw's capabilities, configurations, environment requirements, and the latest information to provide users with the most intuitive and effective answers.

## 🔍 Intelligent Dual-Mode Search Strategy

### **Core Mechanism: Auto Memory + Graceful Degradation**

- ✅ **One-time Configuration, Permanent Recall** → Saved to `memory/openclaw-env-info.md`
- ⏰ **7-Day Validity** → Prompt re-validation when expired
- 🔄 **Cache Priority** → No repeated questions
- 🛡️ **Automatic Fallback** → Switches to local mode when web_search is unavailable

---

## 🚀 Step 1: Runtime Detection Flow

```python
def get_websearch_tool():
    """
    Logic for obtaining web_search tool:
    1. First check cache (memory/openclaw-env-info.md)
    2. If cache invalid/missing, detect current environment
    3. If new tool detected, save to cache
    4. If none available, return None (fallback to local mode)
    """
    
    # Step 1: Check cache
    cached = read_cached_config("memory/openclaw-env-info.md")
    if cached and is_cache_valid(cached, days=7):
        return {"source": "cached", **cached}
    
    # Step 2: Attempt environment detection
    env_tools = detect_env_tools()
    if env_tools:
        save_new_config(env_tools)
        return {"source": "auto-detected", **env_tools}
    
    # Step 3: Only prompt on first use with no available tools
    if not has_asked_before():
        prompt_user_for_config()
        return None  # Let user decide whether to continue
    
    # Step 4: Fallback to local mode
    return None
```

---

## 📁 Cache File Format

`memory/openclaw-env-info.md` (auto-maintained):

```markdown
## Environment Info
- **Detection Time**: 2026-03-28 23:59
- **OpenClaw Version**: 2026.3.8

### Web Search Tool Configuration (Cached)
- **Source**: auto-detected / user-provided / cached
- **Tool Name**: MiniMax.web_search
- **Call Format**: mcporter call [tool_name] query:"[query]"
- **Success Example**: mcporter call MiniMax.web_search query:"OpenClaw cron help"
- **Saved At**: 2026-03-28 23:59
- **Last Verified**: 2026-03-28 23:59
- **Status**: ✅ Active / ❌ Disabled

---

## How to Configure/Update web_search Tool

```bash
# Run the following command to start configuration
openclaw configure web-search --setup
```

---

**Note**: 
- Config file will be auto-saved as skill updates
- Will prompt re-test if not verified for more than 7 days
- Deleting this file will reset to first-time state
```

---

## 🔄 Complete Workflow

### Scenario A: Cache Exists (After First Use)

```
User Question → Read Cache → Validate Validity (<7 days)
   ↓              ↓          ↓
Use Cached Tool ←         ✅ Valid → Use Directly
                          ↓
                         ❌ Expired → Prompt Re-verification
```

**Output Example**:

```markdown
💡 Using configured web_search tool to search...

Tool: MiniMax.web_search  
Last Verified: Yesterday

Searching: "OpenClaw Cron Job Configuration"
```

---

### Scenario B: First Time (No Cache)

```
User Question → Detect Environment → Found No web_search
   ↓               ↓           ↓
First Prompt   ←      ❌         ✅ Has Tool
                       ↓       ↓
                    Ask User → Wait for Choice
                     ↓       ↓
                  Option A  Option B
                   ↓       ↓
                Collect Config  Direct Fallback
                   ↓       ↓
                Save to Memory
```

**Output Example**:

```markdown
⚠️ No available web_search tool detected

To obtain the latest information, you can choose:

**Option A: Provide Existing Configuration**  
If you have other web_search tools, please share the following:
- Tool Name (e.g., "MiniMax.web_search")
- Call Method (e.g., "mcporter call [name] query:'[text]'")
- A Success Example

**Option B: Use Local Mode**  
Skip web_search, answer only via CLI and existing knowledge base

Please choose A or B 👇
```

---

### Scenario C: After User Provides Configuration

```
Receive User Input → Parse Config → Verify Availability → Save to Memory
   ↓              ↓         ↓          ↓
Format Validation  Extract Fields    Test Once  memory/openclaw-env-info.md
   ↓              ↓         ↓          ↓
❌ Invalid Format → Prompt Correction  ✅ Success  Record Timestamp
                            ↓
                      Confirm Save and Continue
```

**Output Example**:

```markdown
✅ Configuration successfully remembered!

📝 **Saved Information:**
- Tool Name: MiniMax.web_search
- Call Format: mcporter call [tool_name] query:"[query]"
- Status: ✅ Active
- Saved At: 2026-03-28 23:59

💡 Will load automatically next time, no need to ask again.

Now continuing with your request...
```

---

## 💬 Interaction Templates

### 1. Prompt When Using Cache

```markdown
💡 **Web Search Mode** (Configured)

Using saved web_search tool to find latest information:

**Tool**: `MiniMax.web_search`  
**Last Verified**: Today  
**Search Scope**: OpenClaw Official Docs + GitHub + Discord

Please wait...
```

---

### 2. Prompt When Configuration Expires

```markdown
⚠️ **Web Search Configuration Needs Re-verification**

Last verification was `X` days ago (>7 days), to ensure accuracy:

(A) Re-verify tool configuration  
(B) Temporarily fallback to local mode

Or do you want to update to a different tool?
```

---

### 3. Fallback to Local Mode

```markdown
⚠️ **Currently in Local Mode** (web_search unavailable)

Will provide assistance through:
- Reading OpenClaw CLI commands
- Analyzing configuration files
- Consulting local knowledge base (`memory/openclaw-knowledge.md`)

💡 **Hint**: For latest information, configure web_search tool and try again.

Here is the answer based on existing knowledge:
```

---

## 🛠️ Automation Script Recommendations

### save-websearch-config.py

```python
#!/usr/bin/env python3
"""Auto-save web_search config to memory/openclaw-env-info.md"""

from datetime import datetime

def save_config(tool_name, call_format, example=None):
    config = {
        "tool_name": tool_name,
        "call_format": call_format,
        "example": example or f"mcporter call {tool_name} query:'test'",
        "saved_at": datetime.now().isoformat(),
        "last_verified": datetime.now().isoformat(),
        "status": "active"
    }
    
    with open("memory/openclaw-env-info.md", "a") as f:
        f.write("\n### Web Search Tool Configuration\n")
        for k, v in config.items():
            f.write(f"- **{k}**: {v}\n")
    
    print("✅ Configuration saved to memory/openclaw-env-info.md")
```

---

### validate-websearch.sh

```bash
#!/bin/bash
# Verify if cached configuration is valid

ENV_FILE="memory/openclaw-env-info.md"
LAST_VERIFIED=$(grep "Last Verified" $ENV_FILE | awk '{print $3" "$4}')
CURRENT_DATE=$(date +"%Y-%m-%d %H:%M")

DAYS_OLD=$(( ($(date -d "$CURRENT_DATE" +%s) - $(date -d "$LAST_VERIFIED" +%s)) / 86400 ))

if [ $DAYS_OLD -gt 7 ]; then
    echo "⚠️ Web Search configuration expired ($DAYS_OLD days ago)"
    exit 1
else
    echo "✅ Web Search configuration valid (${DAYS_OLD}days ago verified)"
    exit 0
fi
```

---

## 🎯 Trigger Scenarios

Use this skill when users ask about:

- "Does openclaw support..."
- "Help me use openclaw to do/find/accomplish..."
- "Let me see how openclaw does..."
- "How to configure openclaw..."
- "How to set up openclaw cron jobs"
- "How to create a new agent"
- "How to manage openclaw skills"
- Any implied questions about OpenClaw-related information

---

## 📚 Knowledge Base Structure

Maintain the following files under `memory/` directory:

### `memory/openclaw-knowledge.md`
OpenClaw Core Knowledge Base (command reference, configuration options, best practices)

### `memory/openclaw-env-info.md` **(New)**
Environment Info Recording (web_search tool config, version info, special configs)

### `memory/openclaw-commands.md`
OpenClaw Command Quick Reference

---

## 📖 Common Command Reference

### Basic Commands
```bash
# View OpenClaw status
openclaw status

# View all available commands
openclaw help

# View help for specific command
openclaw [command] --help
```

### Agent Management
```bash
# List all agents
openclaw config get agents.list --json

# View agent details
openclaw config get agents.list | jq '.[] | select(.id == "agent-name")'
```

### Skills Management
```bash
# List all skills
openclaw skills list

# Install skill
openclaw skills install [skill-name]

# Publish skill
cd ~/my-skill
clawhub publish . \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --changelog "Initial release"
```

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| Asking about web_search every time | Check if `memory/openclaw-env-info.md` is saved correctly |
| Cache config invalid | Manually delete this file to restart configuration |
| web_search tool call fails | Run `mcporter list` to check if tool is in list |
| Network timeout | Check network connection, configure HTTP_PROXY |

---

## 🔄 Configuration Management Commands

```bash
# View current web_search config
cat memory/openclaw-env-info.md | grep -A10 "Web Search"

# Clear cache (reconfigure)
rm memory/openclaw-env-info.md

# Re-run skill trigger config flow
openclaw run openclaw-howto --setup
```

---

**Last Updated**: 2026-03-28  
**Maintainer**: OpenClaw HowTo Skill  
**Goal**: One-time configuration, permanent recall, intelligent fallback  
**Version**: 2.1 (With Cached Memory)
