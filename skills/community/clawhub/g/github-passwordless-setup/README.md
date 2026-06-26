# GitHub Passwordless Setup

**Never type passwords again for Git operations and GitHub API calls!**

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-blue.svg)]()

English | [简体中文](README.zh-CN.md)

## 🎯 What This Does

Configures **complete passwordless authentication** for GitHub using:
1. **SSH Keys** - Zero-password Git operations (push/pull/clone)
2. **Personal Access Token** - Zero-password repository management

**One-time setup, lifetime convenience!**

## ⚡ Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/happydog-intj/github-passwordless-setup/master/setup.sh | bash
```

## ✨ Before vs After

| Operation | Before | After |
|-----------|--------|-------|
| `git push` | ❌ Password required | ✅ Instant |
| `git clone` | ❌ Password required | ✅ Instant |
| `gh repo create` | ❌ Re-authentication | ✅ Instant |
| Token expiration | ❌ Breaks workflow | ✅ Never expires* |

*with "No expiration" token setting

## 📋 What You Get

### SSH Key Authentication
- ✅ Push code without passwords
- ✅ Pull updates instantly
- ✅ Clone repos seamlessly
- ✅ Works with all Git operations

### GitHub CLI (gh) with PAT
- ✅ Create repositories: `gh repo create`
- ✅ Manage issues: `gh issue create/list`
- ✅ Handle PRs: `gh pr create/merge`
- ✅ All GitHub operations

## 🚀 Manual Setup (5 minutes)

### Part 1: SSH Key (3 minutes)

```bash
# 1. Generate key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# 2. Copy public key
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub           # Linux (copy manually)

# 3. Add to GitHub
# Visit: https://github.com/settings/ssh/new
# Paste key and save

# 4. Test
ssh -T git@github.com
```

### Part 2: GitHub CLI Token (2 minutes)

```bash
# 1. Create token
# Visit: https://github.com/settings/tokens/new
# Scopes: ✅ repo (select all)
# Click "Generate token" and copy it

# 2. Install GitHub CLI
brew install gh  # macOS
# Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# 3. Configure token
gh auth login --with-token
# Paste your token

# 4. Set SSH protocol
gh config set git_protocol ssh
```

## 🧪 Verify Setup

```bash
# Test SSH
ssh -T git@github.com
# Expected: Hi username! You've successfully authenticated...

# Test GitHub CLI
gh auth status
# Expected: ✓ Logged in to github.com

# Test complete workflow
gh repo create test-$(date +%s) --public && gh repo delete --yes $(gh repo list --limit 1 --json name --jq '.[0].name')
# Expected: Creates and deletes repo without passwords
```

## 📖 Documentation

See [SKILL.md](./SKILL.md) for:
- Detailed setup instructions
- Troubleshooting guide
- Advanced configuration
- Security best practices
- Multiple accounts setup

## 🔒 Security

- SSH keys use ED25519 (most secure)
- Tokens can be scoped to minimum permissions
- Passphrase protection available
- Easy revocation if compromised

## 🌐 Platform Support

- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- ✅ Windows (WSL2, Git Bash)

## 🛠️ Tools Included

- `setup.sh` - Automated setup script
- `verify.sh` - Configuration verification
- Complete documentation

## 💡 Use Cases

Perfect for:
- OpenClaw automated workflows
- CI/CD pipelines
- Development teams
- Anyone tired of typing passwords

## 🤝 Contributing

Issues and pull requests welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🔗 Links

- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.ai)
- [GitHub SSH Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**Made with ❤️ for productivity enthusiasts**
