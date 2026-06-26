# PromptGit — Local Prompt Version Control

**Git for your prompts. Track every change, diff versions, rollback mistakes, never lose a good prompt again.**

PromptGit gives you version control for AI prompts — system prompts, task prompts, templates, snippets. Save versions with notes, compare changes, tag your best ones, rollback bad edits, and search your entire prompt library. All local, zero dependencies, works offline.

---

## The Problem

You're refining an AI prompt. You change a few words. Suddenly it doesn't work as well. What did you change? Can you get the old version back? You have no idea because you just overwrote it.

Or you have 47 variations of "good system prompt" scattered across text files, Google Docs, and Notion. Which one actually works? When was it last updated? Who knows.

## What PromptGit Does

### Version Control for Prompts
- Save versions with timestamps and notes
- Never lose a good prompt again
- See exactly what changed between versions
- Rollback to any previous version instantly

### Organization & Search
- Categories (system, task, template, snippet)
- Tags (best, testing, production, deprecated)
- Search by keyword, tag, date range, or regex
- Find similar prompts automatically

### Diff & Compare
- Side-by-side diffs between any two versions
- See exactly what changed (unified diff format)
- A/B comparison mode with notes field for results

### Export & Share
- Export prompts as portable JSON
- Share with version history or current version only
- Import prompts from others
- Export to markdown for documentation

---

## Quick Start

```bash
# Save your first prompt
echo "You are a helpful assistant..." | python3 prompt_git.py save assistant-v1 --note "First version"

# Make changes and save a new version
echo "You are a helpful and friendly assistant..." | python3 prompt_git.py save assistant-v1 --note "Added 'friendly'"

# See version history
python3 prompt_git.py versions assistant-v1

# Compare versions
python3 prompt_git.py diff assistant-v1 abc123 def456

# Rollback to a previous version
python3 prompt_git.py rollback assistant-v1 abc123
```

---

## Usage Guide

### Save a Prompt

```bash
# From stdin
echo "Your prompt here" | python3 prompt_git.py save my-prompt --note "Initial version"

# From file
python3 prompt_git.py save my-prompt --file prompt.txt --note "v2 with examples"

# With category and tags
python3 prompt_git.py save system-prompt \
  --category system \
  --tag best \
  --tag production \
  --note "Production system prompt"
```

### View Prompts

```bash
# List all prompts
python3 prompt_git.py list

# Filter by category
python3 prompt_git.py list --category system

# Filter by tag
python3 prompt_git.py list --tag best

# Get current version
python3 prompt_git.py get my-prompt

# Get specific version
python3 prompt_git.py get my-prompt --version abc123
```

### Version History

```bash
# See all versions
python3 prompt_git.py versions my-prompt

# Output:
→ def456 — 2026-02-21T15:30:00 — Added examples [production]
  abc123 — 2026-02-21T10:00:00 — Initial version []

# The arrow (→) marks the current version
```

### Diff Versions

```bash
# Compare two versions
python3 prompt_git.py diff my-prompt abc123 def456

# Output shows unified diff:
--- my-prompt (abc123)
+++ my-prompt (def456)
@@ -1,2 +1,3 @@
 You are a helpful assistant.
+Please provide examples.
```

### Rollback

```bash
# Rollback to a previous version
python3 prompt_git.py rollback my-prompt abc123

# This makes abc123 the current version
# The newer version (def456) is not deleted, just not current
```

### Tag Versions

```bash
# Tag a version
python3 prompt_git.py tag my-prompt abc123 best

# Tag meanings are up to you:
# - best: Best-performing version
# - testing: Under testing
# - production: Currently in production
# - deprecated: Don't use this
# - experimental: Risky/untested
```

### Search

```bash
# Search content by keyword
python3 prompt_search.py search "helpful assistant"

# Search by tag
python3 prompt_search.py tag best

# Search by date range
python3 prompt_search.py date --start 2026-02-01 --end 2026-02-21

# Regex search
python3 prompt_search.py regex "assistant|helper"

# Find recent prompts
python3 prompt_search.py recent --limit 10

# Find similar prompts
python3 prompt_search.py similar my-prompt --threshold 0.6

# Repository stats
python3 prompt_search.py stats
```

### Export & Import

```bash
# Export a prompt (current version only)
python3 prompt_export.py export my-prompt output.json

# Export with full history
python3 prompt_export.py export my-prompt output.json --history

# Export as markdown
python3 prompt_export.py export my-prompt output.md --markdown

# Export multiple prompts
python3 prompt_export.py export-multi bundle.json --names prompt1 prompt2 prompt3 --history

# Import a prompt
python3 prompt_export.py import shared-prompt.json

# Import and overwrite existing
python3 prompt_export.py import shared-prompt.json --overwrite
```

---

## Use Cases

### 1. **Prompt Engineering Iteration**
Save every version as you refine your prompt. See what changed. Rollback if something breaks. Never lose a good version.

### 2. **A/B Testing Prompts**
Save version A, save version B, tag with results. Compare diffs to see exactly what changed between the winner and loser.

### 3. **Team Prompt Sharing**
Export your best prompts. Share the JSON file. Team imports it. Everyone has the same version, with full history if you want.

### 4. **System Prompt Library**
Organize all your system prompts by category. Tag the ones that work best. Search across all of them when you need inspiration.

### 5. **Audit Trail**
See when a prompt was changed, what changed, and what note was left. Perfect for compliance or debugging "when did this break?"

### 6. **Template Management**
Save reusable templates (e.g., "email writer", "code reviewer"). Pull them when needed. Never rewrite from scratch.

---

## Storage Structure

```
~/.promptgit/
  index.json          # Prompt metadata (names, categories, tags, current versions)
  prompts/
    my-prompt/
      versions.json   # Version history for this prompt
      abc123.txt      # Content for version abc123
      def456.txt      # Content for version def456
    another-prompt/
      versions.json
      xyz789.txt
```

All human-readable, grep-friendly JSON and text files. No binary blobs.

---

## Configuration

See `config_example.json` for reference constants and example values

```python
# Change storage location
STORAGE_DIR = '/path/to/your/prompts'

# Define your own categories
DEFAULT_CATEGORIES = ['system', 'task', 'template', 'snippet', 'general']

# Suggested tags
SUGGESTED_TAGS = ['best', 'testing', 'production', 'deprecated']

# Similarity threshold for "find similar" search
SIMILARITY_THRESHOLD = 0.5
```

See `config_example.json` for all options.

---

## Examples

### Example 1: Refining a System Prompt

```bash
# Initial version
echo "You are a helpful assistant." | \
  python3 prompt_git.py save assistant --category system --note "v1"

# After testing, add more detail
echo "You are a helpful assistant. Provide concise answers." | \
  python3 prompt_git.py save assistant --note "v2: added conciseness"

# Hmm, too concise. Rollback
python3 prompt_git.py rollback assistant <v1-version-id>

# Try a different approach
echo "You are a helpful assistant. Provide detailed, thoughtful answers." | \
  python3 prompt_git.py save assistant --note "v3: detailed instead" --tag testing

# This one works! Tag it
python3 prompt_git.py tag assistant <v3-version-id> best
python3 prompt_git.py tag assistant <v3-version-id> production
```

### Example 2: Sharing Prompts with a Team

```bash
# Export your best system prompt
python3 prompt_export.py export my-system-prompt team-prompt.json --history

# Teammate imports it
python3 prompt_export.py import team-prompt.json

# Now they have the full history and can see how it evolved
python3 prompt_git.py versions my-system-prompt
```

### Example 3: Finding What Broke

```bash
# Prompt stopped working. When?
python3 prompt_git.py versions my-prompt

# Output shows versions with timestamps
# Pick two versions: one that worked, one that didn't
python3 prompt_git.py diff my-prompt <good-version> <broken-version>

# Diff shows exactly what changed
# Fix it and save a new version
```

---

## What's Included

| File | Purpose |
|------|---------|
| `prompt_git.py` | Main version control (save, get, diff, rollback, tag) |
| `prompt_search.py` | Search and browse (keyword, tag, date, regex, similar) |
| `prompt_export.py` | Export/import (JSON, markdown, bundles) |
| `config_example.json` | Configuration template |
| `README.md` | This file |
| `LIMITATIONS.md` | What it doesn't do |
| `LICENSE` | MIT License |

---

## Requirements

- Python 3.7+
- **Zero external dependencies** (stdlib only)
- Works on Linux, macOS, Windows

---

## Python API

Use PromptGit in your own scripts:

```python
from prompt_git import PromptRepository

# Initialize repo
repo = PromptRepository(storage_dir='~/.promptgit')

# Save a prompt
version_id = repo.save(
    'my-prompt',
    'You are a helpful assistant.',
    note='Initial version',
    category='system',
    tags=['testing']
)

# Get current version
version = repo.get_version('my-prompt')
print(version.content)

# List all prompts
prompts = repo.list_prompts(category='system')

# Diff two versions
diff = repo.diff('my-prompt', version_a_id, version_b_id)
print(diff)
```

---

## quality-verified


---

## FAQ

**Q: Does it sync across devices?**  
A: No. It's local-only. But you can export/import to share manually, or put `~/.promptgit` in a synced folder (Dropbox, Git, etc.).

**Q: Can I use it with Git?**  
A: Yes! The storage directory is just JSON and text files. You can version the whole thing with Git if you want meta-version-control.

**Q: What about collaborative editing?**  
A: Not built-in. Export/import is the collaboration model. For real-time collab, use a shared folder or Git.

**Q: Does it work with images or multimodal prompts?**  
A: Text only. If your multimodal prompt has a text component, you can save that.

**Q: How do I delete a prompt?**  
A: Currently, no delete command (by design — version control shouldn't delete easily). You can manually delete the folder in `~/.promptgit/prompts/`.

---

## License

MIT — See `LICENSE` file.

---

## Author

**Shadow Rose**

Built for AI users who are tired of losing good prompts to accidental overwrites and bad edits.


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
