# Nex Changelog

**Changelog & Version Notes Generator for client-facing release communication**

Generate professional changelogs and version notes. Import from git commits, organize by type and audience, format as Keep a Changelog, client emails, or Telegram updates.

Built by [Nex AI](https://nex-ai.be) for digital transformation of Belgian SMEs.

## Features

- **Multi-project support** - Manage changelogs for multiple projects
- **Git integration** - Automatically parse commits and conventional commits
- **Flexible audiences** - Organize entries for internal, client, or public audiences
- **Professional formatting** - Export as Keep a Changelog, emails, or Telegram messages
- **Local storage** - All data stored in `~/.nex-changelog/` - no cloud dependencies
- **Rich categorization** - Organize changes by type: Added, Fixed, Changed, Removed, Security, Deprecated, Performance

## Installation

### Prerequisites

- Python 3.9+
- Git (for git import functionality)
- Bash

### Quick Start

```bash
# Run the setup script
bash setup.sh

# Test the installation
nex-changelog --help
```

## Usage

### Add a Project

```bash
nex-changelog project add \
  --name "Ribbens Airco Website" \
  --repo-path /path/to/repo \
  --client-name "Ribbens Airco" \
  --client-email "contact@ribbens-airco.be" \
  --description "Corporate website with contact form"
```

### Add Changelog Entries

Manually add entries:

```bash
nex-changelog add \
  --project "Ribbens Airco Website" \
  --type added \
  --description "Contact form with email notification" \
  --audience client
```

Or import from git commits:

```bash
nex-changelog git /path/to/repo \
  --project "My App" \
  --version 1.3.0
```

### Create a Release

```bash
nex-changelog release \
  --project "Ribbens Airco Website" \
  --version 1.3.0 \
  --summary "Mobile fixes and contact form"
```

### Generate Client Email

```bash
nex-changelog email \
  --project "Ribbens Airco Website" \
  --version 1.3.0
```

### Show Changelog

```bash
# Keep a Changelog format
nex-changelog show --project "My App" --format keepachangelog

# Simple bullet list
nex-changelog show --project "My App" --format simple

# Markdown table
nex-changelog show --project "My App" --format table

# JSON export
nex-changelog show --project "My App" --format json
```

### Generate Telegram Message

```bash
nex-changelog telegram \
  --project "Ribbens Airco Website" \
  --version 1.3.0
```

### List and Search

```bash
# List all entries
nex-changelog list

# List by project
nex-changelog list --project "My App"

# Filter by type and audience
nex-changelog list --type fixed --audience client

# Search entries
nex-changelog search --query "security"
```

### View Statistics

```bash
nex-changelog stats
```

## Data Organization

### Change Types

- `ADDED` - New features
- `CHANGED` - Changes to existing functionality
- `FIXED` - Bug fixes
- `REMOVED` - Removed functionality (breaking changes)
- `SECURITY` - Security vulnerability fixes
- `DEPRECATED` - Features marked for removal
- `PERFORMANCE` - Performance improvements

### Audiences

- `INTERNAL` - Development team only
- `CLIENT` - Client-facing announcements
- `PUBLIC` - Public/marketing announcements

### Conventional Commits

The tool automatically parses conventional commits:

```
feat: add login system              → ADDED, CLIENT
fix: resolve password bug           → FIXED, CLIENT
perf: optimize image loading        → PERFORMANCE, CLIENT
security: patch XSS vulnerability   → SECURITY, CLIENT
docs: update API docs              → CHANGED, INTERNAL
refactor: simplify auth module     → CHANGED, INTERNAL
chore: update dependencies         → CHANGED, INTERNAL
```

Breaking changes (using `!:` or marked in body) are flagged and categorized as REMOVED.

## Database

All data is stored locally in SQLite:

```
~/.nex-changelog/
├── changelog.db          # Main database
└── exports/              # Generated exports
```

### Database Schema

**projects**
- `id` - Project ID
- `name` - Project name (unique)
- `repo_path` - Git repository path
- `current_version` - Latest version
- `client_name` - Client contact name
- `client_email` - Client email address
- `description` - Project description
- `created_at` - Creation timestamp

**changelog_entries**
- `id` - Entry ID
- `project_id` - Link to project
- `version` - Version number (optional, for unreleased entries)
- `change_type` - Type of change (ADDED, FIXED, etc.)
- `description` - Entry description
- `audience` - Target audience
- `details` - Additional details
- `author` - Git author or creator
- `commit_hash` - Git commit hash (if from git)
- `breaking` - Boolean: is breaking change
- `created_at` - Creation timestamp

**releases**
- `id` - Release ID
- `project_id` - Link to project
- `version` - Version number
- `release_date` - Release date
- `summary` - Release summary
- `client_notes` - Notes for clients
- `internal_notes` - Internal notes
- `telegram_sent` - Boolean: message sent to Telegram
- `email_sent` - Boolean: email sent to client
- `created_at` - Creation timestamp

## Examples

### Scenario: Release for Ribbens Airco Website

```bash
# 1. Create project
nex-changelog project add \
  --name "Ribbens Airco Website" \
  --client-name "Ribbens Airco" \
  --description "Corporate website"

# 2. Import recent git commits
nex-changelog git /path/to/ribbens-repo \
  --project "Ribbens Airco Website" \
  --version 1.3.0

# 3. Add any manual entries
nex-changelog add \
  --project "Ribbens Airco Website" \
  --type added \
  --description "Customer testimonials section" \
  --audience client \
  --version 1.3.0

# 4. Create formal release
nex-changelog release \
  --project "Ribbens Airco Website" \
  --version 1.3.0 \
  --summary "New testimonials section and performance improvements"

# 5. Generate client email
nex-changelog email \
  --project "Ribbens Airco Website" \
  --version 1.3.0

# 6. Generate Telegram announcement
nex-changelog telegram \
  --project "Ribbens Airco Website" \
  --version 1.3.0

# 7. Export full changelog
nex-changelog export \
  --project "Ribbens Airco Website" \
  --output CHANGELOG.md
```

## Development

### Project Structure

```
nex-changelog/
├── lib/
│   ├── config.py          # Configuration and constants
│   ├── storage.py         # SQLite database operations
│   ├── git_parser.py      # Git commit parsing
│   └── formatter.py       # Output formatting
├── nex-changelog.py       # CLI entry point
├── SKILL.md               # Skill documentation
├── README.md              # This file
├── setup.sh               # Installation script
└── LICENSE.txt            # MIT-0 License
```

### Adding New Features

1. Add command handler in `nex-changelog.py` (e.g., `cmd_*` function)
2. Add subparser in `main()` function
3. Document in `SKILL.md` and `README.md`

### Adding New Output Formats

1. Add formatter function in `lib/formatter.py`
2. Call formatter in appropriate command
3. Update help text and documentation

## License

MIT-0 License - Use freely, no attribution required.

## Support

For issues or questions:
- Check the [Nex AI website](https://nex-ai.be)
- Review the [SKILL.md](SKILL.md) documentation
- Run `nex-changelog --help` for command reference

## Author

Built by Nex AI - Digital transformation for Belgian SMEs
