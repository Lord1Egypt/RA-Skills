
# GitHub Push - Auto-Push Tool 🚀

> **Production-grade GitHub push automation with zero manual setup**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)

Push to GitHub with confidence! This skill implements enterprise-grade safety mechanisms following GitHub's automation guidelines, perfect for CI/CD pipelines, batch processing, and professional automated workflows.

## When to Use ✅

- **Automated deployments** - Push code to GitHub without manual configuration
- **SSH key management** - Auto-detects and loads SSH keys automatically  
- **Conflict resolution** - Handles git merge conflicts intelligently
- **Batch file uploads** - Safely upload hundreds of files in one operation
- **CI/CD integration** - Reliable automated workflows for production environments

## When Not to Use ❌

- **GitHub platform operations** - Creating issues, PRs, or managing repository settings
- **Code review tasks** - Reviewing pull requests or analyzing code changes  
- **Read-only operations** - Simply viewing GitHub content or fetching data
- **Non-GitHub repositories** - GitLab, Bitbucket, or self-hosted Git servers

## Quick Start

### Basic Usage (Fully Automatic)
```bash
# Auto-configures SSH, remote, and pushes everything
python scripts/github_upload.py --repo owner/repo --path ./files --message "Update"
```

### Safe Testing
```bash
# Dry run - shows what would be uploaded without actual push
python scripts/github_upload.py --repo owner/repo --path ./files --dry-run
```

### Conflict Handling
```bash
# Force push with intelligent conflict resolution
python scripts/github_upload.py --repo owner/repo --path ./files --force
```

### Version Information
```bash
# Check installed version
python scripts/github_upload.py --version
```

## Prerequisites

### SSH Key Setup
The script auto-detects SSH keys but requires initial key generation:

```bash
# Check existing SSH keys
ls ~/.ssh/id_*

# Generate new key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start ssh-agent and load key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to your GitHub account
cat ~/.ssh/id_ed25519.pub
```

### Git Configuration
User information is auto-configured if missing, but you can set it manually:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

## Smart Features

### Zero-Setup Automation
- **Auto SSH Loading**: Detects and loads `~/.ssh/id_*` keys automatically
- **Auto Remote Config**: Sets up `git@github.com:owner/repo.git` when missing
- **Auto Repository Init**: Initializes git repository for new projects
- **Auto User Setup**: Configures name/email if not already set

### Intelligent Safety
- **Smart File Filtering**: Automatically excludes sensitive files:
  - Git files: `.git/`, `.gitignore`
  - System files: `.DS_Store`, `__pycache__/`, `Thumbs.db`
  - Secrets: `id_rsa`, `*.pem`, `*.key`, `.env*`, `*.secret`
  - Binaries: `*.zip`, `*.tar`, `*.exe`, `*.dll`, `*.so`
- **Conflict Resolution Workflow**: 
  1. Normal push → Success? Done!
  2. Pull + rebase → Auto-resolve conflicts
  3. Force push → Last resort for stubborn cases
- **Progress Tracking**: Real-time `[1/16]` upload progress display
- **Rate Limiting**: 3-5 second delays following GitHub best practices

## File Structure

```
github-push/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # User guide (this file)
├── scripts/
│   └── github_upload.py  # Main automation script
├── references/
│   ├── api.md            # API documentation
│   ├── configuration.md  # Configuration guide  
│   └── examples.md       # Usage examples
└── CONTRIBUTING.md       # Contribution guidelines
```

## Troubleshooting

### Common Issues & Solutions
- **"Push too frequent"**: Wait 3+ minutes between operations, then retry
- **"Validation failed"**: Check file sizes (<100MB) and ensure no sensitive files are included
- **"Repository not found"**: Verify the repository exists and you have push permissions
- **"SSH key not loaded"**: Manually run `ssh-add ~/.ssh/id_ed25519` if auto-loading fails

### Advanced Options
- `--no-safe`: Disable safety features for maximum speed (use with caution)
- `--delay N`: Set custom delay between operations (seconds)
- `--config PATH`: Use custom configuration file

## Documentation

For detailed information, see the reference guides:
- `references/api.md` - Complete API reference
- `references/configuration.md` - Advanced configuration options  
- `references/examples.md` - Practical usage examples
- `references/anti-patterns.md` - Common mistakes to avoid

## Contributing

Contributions welcome! Please read `CONTRIBUTING.md` for guidelines on:
- Adding new file filtering patterns
- Enhancing conflict resolution strategies
- Improving authentication methods
- Expanding progress reporting features

## License

MIT - OpenClaw Skill Standard
>>>>>>> 3b3fe1a (Add all project files [2026-03-06 23:22:50])
