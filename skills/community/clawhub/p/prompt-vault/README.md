# PromptVault — Team Prompt Library

**Organize, rate, and share prompts with your team. Never lose a great prompt again.**

Author: Shadow Rose  
License: MIT  
Quality: quality-verified

---

## What It Does

You've discovered a prompt that works perfectly. Your teammate found one that saves hours. Someone else rated a prompt 5 stars. **Where do you keep all of this knowledge?**

Random text files? Scattered notes? Lost in chat history?

**PromptVault solves this:**

- 📚 Central library for all your prompts
- ⭐ Rate prompts (1-5 stars) with performance notes
- 🏷️ Organize by categories and tags
- 🔍 Fast search across everything
- 📊 Usage tracking (know which prompts work)
- 🔄 Export/import for team sharing
- 🌐 Beautiful HTML browse interface (no server needed)
- 📝 Changelog tracking (who changed what, when)
- 🚀 Command-line first (scriptable, automation-friendly)

**One vault. Entire team. All the prompts that matter.**

---

## Quick Start

```bash
# Add your first prompt
python prompt_vault.py add "Helpful Assistant" \
  --text "You are a helpful, friendly assistant." \
  --category system

# Search for prompts
python prompt_vault.py search "assistant"

# Rate a prompt
python prompt_vault.py rate abc123def456 --rating 5 --notes "Perfect for customer support"

# Generate HTML browse interface
python prompt_browse.py -o browse.html

# Export for team sharing
python prompt_sync.py export prompt_vault.json -o team_export.json
```

---

## Features

### 📚 Organized Library

**Categories:**
- System prompts (personas, behaviors)
- Task prompts (specific jobs)
- Templates (reusable structures)
- Snippets (prompt fragments)
- Chains (multi-step sequences)

**Tags:** Add as many as you want. Search by any tag.

**Metadata:** Author, model compatibility, creation date, last modified

### ⭐ Rating System

Rate prompts 1-5 stars with notes:

```bash
python prompt_vault.py rate abc123def456 --rating 5 --notes "Works great with GPT-4"
```

Search by minimum rating:

```bash
python prompt_vault.py search --min-rating 4
```

Know which prompts are team favorites.

### 📊 Usage Tracking

Every time you use a prompt, track it:

```bash
python prompt_vault.py get abc123def456 --use
```

See most-used prompts:

```bash
python prompt_vault.py stats
```

**Data-driven prompt management.**

### 🔍 Powerful Search

Search by:
- Keywords (in name, text, notes)
- Category
- Tags (any tag matches)
- Author
- Minimum rating

```bash
# Find all code review prompts rated 4+
python prompt_vault.py search "code review" --category task --min-rating 4

# Find all prompts by Alice
python prompt_vault.py search --author Alice

# Find prompts tagged "python" or "coding"
python prompt_vault.py search --tags python,coding
```

### 🔄 Team Sharing

**Export prompts:**

```bash
# Export high-rated prompts for team
python prompt_sync.py export prompt_vault.json -o team_best.json --min-rating 4

# Export specific categories
python prompt_sync.py export prompt_vault.json -o system_prompts.json --categories system
```

**Import prompts:**

```bash
# Import with skip duplicates (default)
python prompt_sync.py import my_vault.json --from team_best.json

# Import and replace duplicates
python prompt_sync.py import my_vault.json --from team_best.json --strategy replace

# Import and merge (combine tags, keep highest rating)
python prompt_sync.py import my_vault.json --from team_best.json --strategy merge
```

**Compare vaults:**

```bash
python prompt_sync.py diff my_vault.json coworker_vault.json
```

### 🌐 HTML Browse Interface

Generate a static HTML page for easy browsing:

```bash
python prompt_browse.py -o browse.html
```

**Features:**
- Search bar (live filtering)
- Category filters
- Click to copy prompt to clipboard
- No server needed (open in browser)
- Works offline
- Share with team (just send the HTML file)

**Perfect for teams who want a simple, visual way to explore prompts.**

### 📝 Changelog Tracking

Every update is logged:

```bash
python prompt_vault.py update abc123def456 --text "Updated prompt text"
```

The vault automatically tracks:
- What changed
- When it changed
- Full history per prompt

### 🔒 Safe & Git-Friendly

- **JSON storage** — plain text, easy to diff
- **Automatic backups** — creates .bak before saves
- **No lock files** — safe for shared drives
- **Merge-friendly** — resolve conflicts easily

**Works great with Git, Dropbox, Google Drive, network shares.**

---

## Usage Examples

### Example 1: Build a System Prompt Library

```bash
# Add system prompts
python prompt_vault.py add "Code Reviewer" \
  --text "You are an expert code reviewer..." \
  --category system \
  --tags "coding,reviews" \
  --author "Alice"

python prompt_vault.py add "Technical Writer" \
  --text "You are a technical writer who explains concepts clearly..." \
  --category system \
  --tags "writing,documentation" \
  --author "Bob"

# List all system prompts
python prompt_vault.py list --category system
```

### Example 2: Track Performance

```bash
# Use a prompt for a task
python prompt_vault.py get abc123def456 --use

# After testing, rate it
python prompt_vault.py rate abc123def456 --rating 5 --notes "Perfect results with GPT-4"

# Check usage stats
python prompt_vault.py stats
```

Output:
```
=== Vault Statistics ===
Total prompts: 15
Average rating: 4.2/5

By category:
  system: 5
  task: 8
  template: 2

Most used:
  Code Reviewer: 23 times
  Bug Fixer: 18 times
  Documentation Writer: 12 times
```

### Example 3: Team Workflow

**Person A (Curator):**
```bash
# Create initial vault with best prompts
python prompt_vault.py add "Sprint Planner" --text "..." --category task --rating 5
python prompt_vault.py add "Bug Analyzer" --text "..." --category task --rating 5

# Export for team
python prompt_sync.py export my_vault.json -o team_prompts.json --min-rating 4
```

**Person B (Team Member):**
```bash
# Import team prompts
python prompt_sync.py import my_vault.json --from team_prompts.json

# Add own prompts
python prompt_vault.py add "My Custom Prompt" --text "..." --category task

# Generate browse interface
python prompt_browse.py -o browse.html
```

**Person C (Contributor):**
```bash
# Import team prompts
python prompt_sync.py import my_vault.json --from team_prompts.json --strategy merge

# Rate and improve
python prompt_vault.py rate abc123def456 --rating 4 --notes "Works but could be more specific"
python prompt_vault.py update abc123def456 --text "Improved version..."

# Export updated version
python prompt_sync.py export my_vault.json -o my_improvements.json
```

### Example 4: Automation

```bash
# Script to find and use a prompt
#!/bin/bash
PROMPT_ID="abc123def456"

# Get prompt text
TEXT=$(python prompt_vault.py get $PROMPT_ID --use | grep -A 999 "text:" | tail -n +2)

# Use with AI API
curl -X POST https://api.example.com/chat \
  -d "{\"prompt\": \"$TEXT\"}"
```

---

## Command Reference

### Core Commands

#### Add a Prompt
```bash
prompt_vault.py add "NAME" --text "PROMPT TEXT" [OPTIONS]

Options:
  --category CATEGORY    system, task, template, snippet, chain
  --tags TAGS            Comma-separated tags
  --author AUTHOR        Prompt author
  --notes NOTES          Usage notes
  --models MODELS        Compatible models
  --rating RATING        Initial rating (1-5)
```

#### Search Prompts
```bash
prompt_vault.py search [QUERY] [OPTIONS]

Options:
  --category CATEGORY    Filter by category
  --tags TAGS            Filter by tags (any match)
  --author AUTHOR        Filter by author
  --min-rating N         Minimum rating
  -v, --verbose          Show full details
```

#### Get a Prompt
```bash
prompt_vault.py get PROMPT_ID [OPTIONS]

Options:
  -v, --verbose          Show full details including changelog
  --use                  Increment usage counter
```

#### Rate a Prompt
```bash
prompt_vault.py rate PROMPT_ID --rating N [OPTIONS]

Options:
  --rating N             Rating (1-5, required)
  --notes NOTES          Rating notes
```

#### Update a Prompt
```bash
prompt_vault.py update PROMPT_ID [OPTIONS]

Options:
  --name NAME            New name
  --text TEXT            New text
  --category CATEGORY    New category
  --tags TAGS            New tags
  --notes NOTES          New notes
```

#### Delete a Prompt
```bash
prompt_vault.py delete PROMPT_ID [--confirm]
```

#### List Prompts
```bash
prompt_vault.py list [OPTIONS]

Options:
  --category CATEGORY    Filter by category
  -v, --verbose          Show full details
```

#### Statistics
```bash
prompt_vault.py stats
```

#### List Categories/Tags
```bash
prompt_vault.py categories
prompt_vault.py tags
```

### Sync Commands

#### Export
```bash
prompt_sync.py export VAULT.json -o OUTPUT.json [OPTIONS]

Options:
  --categories CATS      Comma-separated categories to include
  --min-rating N         Minimum rating to include
  --include-private      Include notes and changelog
```

#### Import
```bash
prompt_sync.py import VAULT.json --from IMPORT.json [OPTIONS]

Options:
  --strategy STRATEGY    skip (default), replace, or merge
  --update-existing      Update existing prompts with newer data
```

#### Diff (Compare)
```bash
prompt_sync.py diff VAULT1.json VAULT2.json [-v]
```

### Browse Interface

#### Generate HTML
```bash
prompt_browse.py -o OUTPUT.html [OPTIONS]

Options:
  --vault VAULT.json     Source vault (default: prompt_vault.json)
  --title TITLE          Page title
```

---

## Configuration

See `config_example.json` for reference constants and example values

```python
# Vault location
VAULT_PATH = './prompt_vault.json'

# Categories
DEFAULT_CATEGORIES = ['system', 'task', 'template', 'snippet', 'chain']

# Team settings
TEAM_SETTINGS = {
    'default_author': 'Team',
    'require_category': True,
}

# Custom categories
CUSTOM_CATEGORIES = ['code_review', 'creative_writing']
```

See `config_example.json` for all available options.

---

## Use Cases

### For Solo Developers
- Keep all your favorite prompts in one place
- Rate what works, discard what doesn't
- Never lose a great prompt again

### For Teams
- Share best prompts across the team
- Track which prompts are most effective
- Standardize on high-quality prompts

### For Prompt Engineers
- Organize experiments by category
- Track performance with ratings
- Version control with changelog

### For Managers
- See what prompts teams use most
- Identify top contributors
- Export best practices

---

## File Structure

```
prompt-vault/
├── prompt_vault.py        # Main library engine
├── prompt_browse.py       # HTML interface generator
├── prompt_sync.py         # Export/import for sharing
├── config_example.json      # Configuration template
├── prompt_vault.json      # Your vault (created on first use)
├── README.md              # This file
├── LIMITATIONS.md         # What this tool doesn't do
└── LICENSE                # MIT License
```

---

## Requirements

**Python 3.7+** (standard library only — no external dependencies)

---

## Tips & Best Practices

### 1. Use Descriptive Names
**Bad:** "Prompt 1", "Test prompt"  
**Good:** "Bug Analyzer - Python", "Sprint Planning Assistant"

### 2. Tag Consistently
Agree on team tags: `coding`, `writing`, `analysis`, not `code`/`coding`/`dev`

### 3. Rate After Real Use
Don't rate on creation. Use it first, then rate based on actual results.

### 4. Add Performance Notes
When rating, note which model, what task, and results:
```
Rating 5/5: Perfect with GPT-4 for code reviews. Catches edge cases consistently.
```

### 5. Export Regularly
Share team exports weekly or monthly. Keep everyone aligned.

### 6. Use Categories Meaningfully
- **System:** Personas and behaviors
- **Task:** Specific job prompts
- **Template:** Reusable structures
- **Snippet:** Fragments for building
- **Chain:** Multi-step sequences

### 7. Track Usage
Use `--use` flag when grabbing prompts. Data shows what actually works.

### 8. HTML for Non-Technical Users
Generate HTML browse interface for team members who don't use CLI.

---

## Integration Ideas

### Git Workflow
```bash
# Commit vault changes
git add prompt_vault.json
git commit -m "Added new code review prompts"
git push

# Team pulls changes
git pull
```

### Automation Scripts
```bash
# Auto-export high-rated prompts nightly
0 2 * * * python prompt_sync.py export my_vault.json -o /shared/team_best.json --min-rating 4
```

### Backup Strategy
```bash
# Daily backup to cloud
0 1 * * * cp prompt_vault.json ~/Dropbox/backups/prompt_vault_$(date +\%Y\%m\%d).json
```

---

## Contributing

MIT License means you can:
- Fork and modify
- Share improvements
- Use commercially
- Customize for your team

---

## License

MIT License — see LICENSE file for details.

Free for personal and commercial use.

---

## Author

**Shadow Rose**


---

## FAQ

**Q: Can multiple people use the same vault file?**  
A: Yes! Store on a network drive, Dropbox, or Git repo. The format is merge-friendly.

**Q: What if two people edit at the same time?**  
A: Use Git for merging, or export/import to combine changes safely.

**Q: Does this work with any AI model?**  
A: Yes! Store prompts for any model (GPT, Claude, Gemini, local models, etc.)

**Q: Can I migrate from my current prompt system?**  
A: Yes. Write a quick script to convert your format to PromptVault JSON, then import.

**Q: How do I backup my vault?**  
A: It's just a JSON file. Copy it anywhere. Enable auto-backup in config.

**Q: Can I have multiple vaults?**  
A: Yes! Use `--vault` flag to specify different vault files.

**Q: Is there a GUI?**  
A: No built-in GUI, but the HTML browse interface works like one. Or build your own on top of the CLI.

**Q: Can I search by partial match?**  
A: Yes, search is substring-based by default.

---

**Never lose a great prompt again. Start building your vault today:**

```bash
python prompt_vault.py add "Your First Prompt" --text "Make it great" --category task
```


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
