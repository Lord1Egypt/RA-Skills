# GitHub Manager CLI

A comprehensive GitHub repository management CLI tool. It provides repository management, code review, changelog generation, CI/CD setup, issue management, and project management automation.

## Features

- **Repository management**: List and create repositories
- **Code review**: PR review, file change analysis, and suggestions (tests, docs, large files, config changes)
- **Changelog generation**: Auto-generate changelogs from commit messages (feat, fix, breaking, etc.)
- **CI/CD setup**: One-shot generation of GitHub Actions workflows (CI and deploy)
- **Issue management**: List, create, and close issues with label support
- **Project management**: Project boards, milestones, and weekly reports (via `scripts/project-manager.js`)
- **Standalone scripts**: Code review and changelog scripts that can be run independently

## Requirements

- **Node.js**: >= 14.0.0
- **GitHub**: A [Personal Access Token](https://github.com/settings/tokens) with `repo` scope (recommended)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/github-manager.git
cd github-manager

# Install dependencies
npm install

# Optional: link globally to use the github command
npm link
```

## Configuration

Configure GitHub authentication before first use. The config file is saved as `.github-manager.json` in the current working directory.

```bash
# Configure token and username (required)
node github-cli.js config --token YOUR_GITHUB_TOKEN --username YOUR_USERNAME

# Optional: set default repo so you can omit --repo in later commands
node github-cli.js config --token YOUR_TOKEN --username YOUR_USERNAME --default-repo owner/repo-name
```

You can also copy `config-template.json` from the project root to `.github-manager.json` and fill in `github.token`, `github.username`, `github.defaultRepo`, etc.

**Security**: Do not commit `.github-manager.json` or any config containing real tokens to version control. Add it to `.gitignore`.

## Usage

### General

- If `defaultRepo` is not set, most commands (except `repos list` and `repos create`) require `--repo owner/repo`.
- After `npm link`, you can run `github` directly; otherwise use `node github-cli.js` or `npm start`.

### Repository management

```bash
# List all repositories for the authenticated user
github repos list

# Create a new repository (initializes Node gitignore and MIT license)
github repos create --name repo-name [--description "Description"] [--private true]
```

### Code review

```bash
# Review a specific PR (view changes and review suggestions)
github review pr --repo owner/repo --pr <PR_NUMBER>
```

### Changelog

```bash
# Generate changelog from commit history and print to terminal
github changelog generate --repo owner/repo [--since starting-tag]
```

### Issue management

```bash
# List open issues for a repository
github issues list --repo owner/repo

# Create an issue
github issues create --repo owner/repo --title "Title" [--body "Body"] [--labels "bug,enhancement"]

# Close an issue
github issues close --repo owner/repo --number <ISSUE_NUMBER>
```

### CI/CD setup

```bash
# Create .github/workflows/ locally and write ci.yml and deploy.yml templates
github ci setup --repo owner/repo
```

After generation, commit and push `.github/workflows/` to the target repository for the workflows to take effect on GitHub.

### Help

Running without a subcommand or with invalid arguments prints help:

```bash
node github-cli.js
```

## Project structure

```
.
├── github-cli.js          # Main entry and core logic (config, repos, review, changelog, issues, CI)
├── package.json
├── config-template.json   # Config template (token, environments, review/release/CI options)
├── README.md
├── SKILL.md               # Feature and usage notes (extended usage and best practices)
├── scripts/
│   ├── project-manager.js # Project management (Projects v2, boards, milestones, reports)
│   ├── code-review.js     # Standalone code review script
│   └── generate-changelog.js # Standalone changelog generator
├── templates/
│   └── github-actions/    # CI/CD workflow templates
│       ├── ci-workflow.yml
│       └── deploy-workflow.yml
└── .github/
    └── workflows/        # Example or generated workflow files
        ├── ci.yml
        └── deploy.yml
```

## Standalone scripts

These scripts can be run on their own. You must pass token/repo etc. yourself (or rely on config in the same or parent directory):

- **`scripts/project-manager.js`**: Project management (list/create projects, boards, milestones, reports).
- **`scripts/code-review.js`**: Run code review for a PR in a given repository.
- **`scripts/generate-changelog.js`**: Generate changelog from local git history.

See each script’s header comments or implementation for arguments and usage.

## Development

```bash
# Run the main CLI
npm start

# Lint and format
npm run lint
npm run format
```

## License

MIT License. See the LICENSE file in the repository if present.

---

**Note**: Run `config` to set your GitHub token and username before use, and ensure the token has the required repository permissions.
