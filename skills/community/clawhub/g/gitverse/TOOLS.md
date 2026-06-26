# GitVerse Skill - Tools Reference

This skill provides CLI commands for GitVerse API.

## Setup

1. Set environment variable:
   ```bash
   export GITVERSE_TOKEN=your_token_here
   ```

2. Build the skill:
   ```bash
   cd ~/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/skills/gitverse
   npm run build
   ```

## Commands

### repos list

List repositories for an organization or user.

```bash
node dist/index.js repos list --org <org>
node dist/index.js repos list --user <username>
```

### repos info

Get repository information.

```bash
node dist/index.js repos info --owner <owner> --repo <repo>
```

### issues list

List issues in a repository.

```bash
node dist/index.js issues list --owner <owner> --repo <repo>
node dist/index.js issues list --owner <owner> --repo <repo> --state open
```

Options:
- `--state` - Filter by state: `open`, `closed`, `all` (default: `all`)

### issues view

View a specific issue.

```bash
node dist/index.js issues view --owner <owner> --repo <repo> --number <number>
```

### issues create

Create a new issue.

```bash
node dist/index.js issues create --owner <owner> --repo <repo> --title "Title" --body "Body"
```

Options:
- `--title` - Issue title (required)
- `--body` - Issue body (optional)

### issues close

Close an issue.

```bash
node dist/index.js issues close --owner <owner> --repo <repo> --number <number>
```

### issues comment

Add a comment to an issue.

```bash
node dist/index.js issues comment --owner <owner> --repo <repo> --number <number> --body "Comment"
```

### pulls list

List pull requests in a repository.

```bash
node dist/index.js pulls list --owner <owner> --repo <repo>
node dist/index.js pulls list --owner <owner> --repo <repo> --state open
```

Options:
- `--state` - Filter by state: `open`, `closed`, `all` (default: `all`)

### pulls view

View a specific pull request.

```bash
node dist/index.js pulls view --owner <owner> --repo <repo> --number <number>
```

### pulls create

Create a new pull request.

```bash
node dist/index.js pulls create --owner <owner> --repo <repo> --title "Title" --head feature --base main
```

Options:
- `--title` - PR title (required)
- `--head` - Head branch (required)
- `--base` - Base branch (required)
- `--body` - PR body (optional)

### pulls merge

Merge a pull request.

```bash
node dist/index.js pulls merge --owner <owner> --repo <repo> --number <number>
```

## Output

All commands output JSON to stdout, which can be parsed or displayed.

## Error Handling

Commands exit with code 1 on error and print error message to stderr.

## Examples

```bash
# List repos for organization
node dist/index.js repos list --org ai-center

# List open issues
node dist/index.js issues list --owner ai-center --repo minister --state open

# Create issue
node dist/index.js issues create --owner ai-center --repo chatbot --title "Bug: API error" --body "Description..."

# Create PR
node dist/index.js pulls create --owner ai-center --repo office --title "Feature: new endpoint" --head feature/new-endpoint --base main
```
