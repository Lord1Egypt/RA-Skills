---
name: nex-changelog
description: Professional changelog and release notes generator for client-facing software releases and updates. Automatically parse git commit history using conventional commit format (feat:, fix:, security:, etc.) and categorize changes into changelog entries (ADDED, CHANGED, FIXED, REMOVED, SECURITY, DEPRECATED, PERFORMANCE). Organize changes by target audience (internal team, client-facing, public) so you can create separate release notes for different stakeholders. Support multiple output formats including standard Keep a Changelog markdown format, simple text summaries, HTML reports, and JSON structured data. Generate professional client-facing email announcements highlighting new features and improvements while hiding technical details and internal refactoring. Create compact Telegram-friendly release announcements with emoji indicators for easy social media sharing. Track releases with semantic versioning, generate release summaries, and manage unreleased entries. Import git commits automatically from project repositories or manually add changelog entries for documentation or non-code releases. Perfect for web agencies, software companies, and development teams who need to communicate changes professionally with clients and stakeholders.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "📜"
    requires:
      bins:
        - python3
        - git
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-changelog.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Changelog

Changelog & Version Notes Generator for client-facing release communication. Organize code changes by type and audience, import from git commits, and export professional release notes in multiple formats (Keep a Changelog, client emails, Telegram).

## When to Use

Use this skill when the user asks about:

- Generating changelogs or release notes for a project
- Creating version updates or "what's new" summaries
- Writing client-facing release announcements
- Documenting breaking changes or security updates
- Organizing code changes by type (features, fixes, breaking changes)
- Importing commit messages from git as changelog entries
- Tracking changes across multiple projects
- Creating Telegram or email updates about new releases
- Managing different audience types (internal, client, public)
- Exporting changelogs in standard formats

Trigger phrases: "changelog", "release notes", "version update", "what changed", "client email", "release announcement", "breaking changes", "new features", "fixed issues", "generate changelog", "import commits", "what's new"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies, and initializes the database.

## Available Commands

The CLI tool is `nex-changelog`. All commands output plain text.

### Add Entry

Manually add a changelog entry:

```bash
nex-changelog add --project "Ribbens Airco Website" --type added --description "Contact form with email notification" --audience client

nex-changelog add --project "My App" --description "Fixed the header menu on mobile" --type fixed --author "John Doe"

nex-changelog add --project "API Service" --type security --description "Patched SQL injection vulnerability" --breaking
```

Supported types: `ADDED`, `CHANGED`, `FIXED`, `REMOVED`, `SECURITY`, `DEPRECATED`, `PERFORMANCE`

Supported audiences: `INTERNAL`, `CLIENT`, `PUBLIC`

### Import from Git

Import commits from a git repository as changelog entries:

```bash
nex-changelog git /path/to/repo --project "My App" --version 1.3.0

nex-changelog git /path/to/repo --since v1.2.0 --project "My App"

nex-changelog git /path/to/repo --project "API" --description "REST API service"
```

The tool automatically:
- Parses conventional commits (feat:, fix:, chore:, security:, etc.)
- Categorizes commits into change types
- Determines audience (internal vs client-facing)
- Extracts author and commit hash

### Create Release

Create a formal release for a version:

```bash
nex-changelog release --project "Ribbens Airco Website" --version 1.3.0 --summary "Mobile fixes and contact form"

nex-changelog release --project "My App" --version 2.0.0 \
  --summary "Major rewrite" \
  --client-notes "New dashboard and improved performance" \
  --internal-notes "API v2, deprecated v1 endpoints"
```

### Show Changelog

Display the changelog for a project:

```bash
nex-changelog show --project "Ribbens Airco Website" --format keepachangelog

nex-changelog show --project "My App" --version 1.3.0 --format simple

nex-changelog show --project "API Service" --type fixed --format table

nex-changelog show --project "My App" --audience client --format json
```

Supported formats: `keepachangelog`, `simple`, `table`, `json`

### List Entries

List all changelog entries with filters:

```bash
nex-changelog list --project "My App"

nex-changelog list --type fixed --audience client

nex-changelog list --version 1.3.0

nex-changelog list --project "API" --type security
```

### Unreleased Entries

Show entries that haven't been assigned to a release yet:

```bash
nex-changelog unreleased --project "Ribbens Airco Website"
```

### Generate Client Email

Create a professional client-facing email for a release:

```bash
nex-changelog email --project "Ribbens Airco Website" --version 1.3.0

nex-changelog email --project "My App" --version 1.3.0 --client "Acme Corp"
```

Output is a professional email with:
- Friendly greeting
- Changes organized by type with emojis
- Client-focused language (no technical jargon)
- Signature

### Generate Telegram Message

Create a compact Telegram-friendly update:

```bash
nex-changelog telegram --project "Ribbens Airco Website" --version 1.3.0
```

Output is compact with emojis, suitable for posting to Telegram or Slack.

### Manage Projects

Add, list, or view projects:

```bash
nex-changelog project add \
  --name "Ribbens Airco Website" \
  --repo-path /path/to/repo \
  --client-name "Ribbens Airco" \
  --client-email "contact@ribbens-airco.be" \
  --description "Corporate website with contact form"

nex-changelog project list

nex-changelog project show --name "Ribbens Airco Website"
```

### Export Changelog

Export full changelog as markdown file:

```bash
nex-changelog export --project "My App" --output CHANGELOG.md
```

### Search Entries

Search across all entries:

```bash
nex-changelog search --query "security"

nex-changelog search --query "header menu" --project "Ribbens Airco Website"

nex-changelog search --query "performance" --project "API"
```

### Statistics

View statistics across projects:

```bash
nex-changelog stats
```

Shows:
- Total entries per project
- Total releases per project
- Latest version per project
- Overall statistics

## Example Interactions

**User:** "What changed in the latest release for Ribbens Airco?"
**Agent runs:** `nex-changelog show --project "Ribbens Airco Website" --format simple`
**Agent:** Displays the formatted changelog naturally.

**User:** "Generate a client email about version 1.3.0"
**Agent runs:** `nex-changelog email --project "Ribbens Airco Website" --version 1.3.0`
**Agent:** Shows the professional email ready to send.

**User:** "Import recent commits from the repo"
**Agent runs:** `nex-changelog git /path/to/repo --project "My App"`
**Agent:** Confirms imported entries and categorization.

**User:** "Add an entry: fixed the SSL redirect issue"
**Agent runs:** `nex-changelog add --project "My App" --description "Fixed the SSL redirect issue" --type fixed --audience client`
**Agent:** Confirms the entry was added.

**User:** "Create release 2.1.0 for ECHO Management website"
**Agent runs:** `nex-changelog release --project "ECHO Management" --version 2.1.0`
**Agent:** Confirms release created.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` separators
- List items prefixed with `- ` or `• `
- Timestamps in ISO-8601 format
- Every command output ends with `[Nex Changelog by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally.

## Data Storage

All changelog data is stored locally at `~/.nex-changelog/`:

- `changelog.db` - SQLite database with projects, entries, and releases
- `exports/` - Generated markdown and export files

No data is sent to external servers. The tool is fully local.

## Conventional Commits

The tool automatically parses conventional commit messages:

```
feat: add new feature          → ADDED, CLIENT audience
fix: resolve issue             → FIXED, CLIENT audience
docs: update documentation     → CHANGED, INTERNAL audience
style: formatting changes      → CHANGED, INTERNAL audience
refactor: code reorganization  → CHANGED, INTERNAL audience
perf: performance improvements → PERFORMANCE, CLIENT audience
test: add test coverage        → CHANGED, INTERNAL audience
chore: dependency update       → CHANGED, INTERNAL audience
security: fix vulnerability    → SECURITY, CLIENT audience
```

Breaking changes (feat!: or fix!:) are automatically marked.

## Important Notes

- All data is stored locally at `~/.nex-changelog/`. No telemetry or external API calls.
- The database supports multiple projects with separate changelogs.
- Entries can be filtered by type, audience, version, and project.
- Releases are automatically linked to entries via version number.
- Git commits are automatically categorized based on conventional commit format.
- Client emails are filtered to show only CLIENT and PUBLIC audience entries.
- Internal views show all entries regardless of audience.

## Troubleshooting

- **"Project not found"**: Use `nex-changelog project list` to see available projects, or `nex-changelog project add` to create a new one.
- **"No entries found"**: Use `nex-changelog list` to view all entries, or `nex-changelog add` to create one.
- **"Git import failed"**: Ensure the repository path is correct and the directory contains a `.git` folder.
- **Database errors**: The database is initialized automatically; check that `~/.nex-changelog/` directory exists and is writable.
- **Conventional commits not recognized**: Verify commit messages follow the format `type(scope): description`.

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
