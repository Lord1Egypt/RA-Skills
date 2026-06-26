# PromptVault — Limitations

This document outlines what PromptVault **does NOT do** and known constraints.

---

## What It Doesn't Do

### ❌ Not a Prompt Generator
PromptVault **stores and organizes** existing prompts. It does not:
- Generate prompts from descriptions
- Improve prompt quality automatically
- Suggest better wording
- A/B test prompts

**What to do instead:** Use your AI assistant or prompt engineering tools to create/improve prompts, then store them in PromptVault.

---

### ❌ Not a Real-Time Collaboration Platform
PromptVault does not:
- Show who's currently editing
- Lock files during edits
- Provide live sync between users
- Have built-in conflict resolution

**What it does:** File-based storage that works with Git, Dropbox, network drives. Use Git for proper version control and merging.

---

### ❌ Not an AI API Integration
PromptVault does not:
- Send prompts to AI APIs directly
- Execute prompts
- Store AI responses
- Track token usage
- Compare model performance

**What it does:** Store and organize prompts. You copy them to your AI tool of choice.

---

### ❌ Not a Prompt Engineering Tutor
PromptVault does not:
- Teach prompt engineering
- Analyze prompt quality beyond ratings
- Suggest improvements
- Explain why prompts work

**What it does:** Help you organize and track what works through ratings and usage data.

---

### ❌ Not a Cloud Service
PromptVault does not:
- Provide hosted storage
- Sync automatically across devices
- Require account registration
- Have a web dashboard

**What it does:** Local/network file storage. You control where vaults live. Use your own sync solution (Git, Dropbox, etc.)

---

## Known Constraints

### Concurrent Edits
- **No file locking** — If two people edit simultaneously, last write wins
- **No automatic merge** — Manual conflict resolution required
- **Workaround:** Use Git for version control, or coordinate edits

### Search Capabilities
- **Simple substring matching** — Not fuzzy search
- **No semantic search** — Doesn't understand meaning
- **No regex in search** — Plain text only
- **Workaround:** Use consistent naming and tagging

### Scale Limits
- **Not tested beyond 10,000 prompts** per vault
- **JSON parsing** gets slower with huge vaults
- **HTML browse** may be slow with 1,000+ prompts
- **Workaround:** Split into multiple vaults by category

### Validation
- **Basic validation only** — Checks length, required fields
- **No duplicate detection** (by text) — Only by ID
- **No spell check**
- **No format validation** — Doesn't verify prompt quality

### Backup
- **Manual backup** — Only creates .bak on save
- **No automatic retention** — Old backups must be managed manually
- **Workaround:** Use external backup solutions (Time Machine, cloud sync, Git)

### HTML Browse Interface
- **Static only** — Regenerate when vault changes
- **No editing** — View and copy only
- **No advanced filtering** — Basic category/search only
- **Client-side search** — All prompts loaded in browser

### Export/Import
- **JSON only** — No CSV, XML, or other formats
- **No schema migration** — Future versions may break compatibility
- **No partial import** — Can't cherry-pick prompts from export

### Model Compatibility
- **Free text field** — Not validated
- **No automatic testing** — Can't verify if prompts work with specified models
- **Workaround:** Test manually and update notes

---

## Security & Privacy

### No Encryption
- **Plain text JSON** — Vault files are readable by anyone
- **No password protection**
- **Workaround:** Use encrypted drives or folders if needed

### No Access Control
- **No user permissions** — Anyone with file access can edit
- **No audit log** — Beyond basic changelog
- **Workaround:** Use file system permissions or Git for access control

### No Sanitization
- **Prompts stored as-is** — No content filtering
- **Could contain sensitive data** — Your responsibility to review
- **No PII detection**

---

## Platform Limitations

### Command-Line Focused
- **No GUI** — Terminal/CLI only (except HTML browse)
- **Not beginner-friendly** — Requires comfort with command line
- **Workaround:** HTML browse interface for non-technical users

### Python Required
- **Python 3.7+** needed — Not standalone executable
- **No installer** — Manual setup
- **Workaround:** Bundle with PyInstaller if needed

### No Mobile Support
- **Desktop only** — No mobile app
- **HTML browse works on mobile** — View-only
- **Workaround:** Access vault files via mobile apps (editor apps can open JSON)

---

## Integration Limits

### No Native Integrations
- **No Slack/Discord bots** — Would require custom development
- **No API** — Command-line interface only
- **No webhooks** — (Config has placeholders, but not implemented)
- **Workaround:** Build custom integrations using CLI commands

### No Import from Other Tools
- **No import from Notion, Airtable, etc.** — Manual conversion needed
- **No prompt library imports** — Would need custom scripts
- **Workaround:** Write conversion scripts or manual entry

---

## Data Format

### JSON Only
- **Single JSON file** — Not a database
- **No indexing** — Linear search through all prompts
- **No transactions** — File-level atomicity only
- **Gets slower at scale**

### No Media Support
- **Text only** — No images, audio, or video
- **No attachments**
- **Workaround:** Link to external files in notes

---

## What We Might Add (Future Ideas)

These are **not promises**, just potential improvements:

- 🔍 Fuzzy search / semantic search
- 🔀 Better merge conflict handling
- 📊 Analytics dashboard (prompt performance over time)
- 🔌 Plugin system for integrations
- 📱 Mobile-friendly web UI
- 🗄️ SQLite storage option for better scale
- 🔐 Optional encryption
- 🌐 Import from popular prompt libraries
- 📈 Prompt effectiveness tracking (link to AI outputs)

**No timeline. Use the tool as-is.**

---

## Bottom Line

PromptVault is a **focused tool** for organizing and sharing prompts.

It's not:
- An AI platform
- A collaboration suite
- A prompt generator
- A quality analyzer

**It's a library system.** Like a bookshelf for prompts. You supply the books, it keeps them organized.

---

## Reporting Issues

Found a limitation not listed here?

1. Check if it's a config issue (see config_example.json)
2. See if it's solvable with a custom script
3. Document clearly with examples
4. Share with the community

**This is open-source. Contributions welcome.**

---

**Know the limits. Use the tool effectively.**
