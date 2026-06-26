# GitHub Installer Agent 🛡️

A security-first GitHub project cloning skill for OpenClaw with comprehensive safety checks, dependency analysis, and secure installation guidance.

## 📋 Overview

This skill provides secure GitHub repository cloning with multiple layers of safety checks:

1. **Input Validation** - Strict GitHub URL format validation
2. **Repository Safety Checks** - Size, stars, last update verification via GitHub API
3. **Safe Cloning** - Uses shallow cloning (`--depth 1`) to minimize risk
4. **Dependency Analysis** - Identifies and analyzes dependency files safely
5. **Security Recommendations** - Provides safe installation commands (never auto-executes)
6. **Transparent Reporting** - Detailed operation logs and security assessments

## 🚀 Quick Start

### Basic Usage
```bash
# Clone a repository with safety checks
github_installer_agent(
    repo_url="https://github.com/psf/requests",
    target_dir="./requests_analysis",
    safe_mode=true,
    depth=1
)
```

### Advanced Usage
```bash
# Clone with custom depth
github_installer_agent(
    repo_url="https://github.com/tensorflow/tensorflow",
    target_dir="/tmp/tensorflow_analysis",
    depth=3,
    safe_mode=true
)
```

## 🔒 Security Features

### Core Security
- ✅ **No Automatic Installation** - Never auto-executes `pip install` or `npm install`
- ✅ **Input Validation** - All inputs are strictly validated
- ✅ **Repository Verification** - Checks repository info via GitHub API
- ✅ **Shallow Cloning** - Uses `git clone --depth 1` by default
- ✅ **File Safety Scanning** - Checks for suspicious file types

### Safety Checks
- GitHub URL format validation
- Repository size verification (warns >100MB)
- Last update timestamp check
- Star count as reputation indicator
- Suspicious file type detection

### Best Practices
- Virtual environment recommendations
- Safe installation commands with `--user` flag
- Package mirror suggestions
- Security audit recommendations

## 📁 File Structure

```
github-installer-agent/
├── SKILL.md              # Main skill documentation
├── _meta.json           # Skill metadata
├── README.md            # This file
├── scripts/
│   ├── safe_clone.sh    # Main security script
│   ├── test_security.sh # Security test script
│   └── validate_skill.sh # Skill validation script
└── SECURITY_IMPROVEMENTS.md # Security improvements documentation
```

## 🧪 Testing

### Run Security Tests
```bash
cd scripts && ./test_security.sh
```

### Validate Skill Configuration
```bash
cd scripts && ./validate_skill.sh
```

### Test with Example Repository
```bash
./scripts/safe_clone.sh https://github.com/psf/requests
```

## 📊 Security Compliance

### OWASP Compliance
- Input Validation
- Output Encoding
- Authentication
- Session Management
- Access Control
- Cryptographic Practices
- Error Handling
- Logging
- Security Configuration

### GitHub Security Best Practices
- GitHub API for repository verification
- Rate limiting implementation
- Repository ownership validation
- Repository activity checking
- Commit signature verification (when available)

## ⚙️ Configuration

### Environment Variables
```bash
# Set temporary directory
export GITHUB_CLONE_TEMP="/tmp/github_clones"

# Set maximum repository size (MB)
export MAX_REPO_SIZE_MB=100

# Enable verbose logging
export GITHUB_CLONE_VERBOSE=1
```

### Skill Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `repo_url` | String | Required | GitHub repository URL |
| `target_dir` | String | Auto-generated | Local directory for clone |
| `safe_mode` | Boolean | true | Enable safety checks |
| `depth` | Number | 1 | Git clone depth |

## 🚨 Security Warnings

### High-Risk Operations to Avoid
1. **Never auto-execute installation commands** from unknown sources
2. **Always test in virtual environments** or containers
3. **Check package sources** in requirements.txt/package.json
4. **Avoid using root privileges** for installation
5. **Review all script files** before execution

### Recommended Security Practices
```bash
# Use virtual environments
python -m venv venv
source venv/bin/activate

# Use --user flag for pip
pip install --user -r requirements.txt

# Use trusted package mirrors
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Audit npm packages
npm audit
npm ci --ignore-scripts
```

## 📈 Performance

- **Shallow Cloning**: Uses `--depth 1` for faster downloads
- **API Rate Limiting**: Respects GitHub API rate limits
- **Memory Efficient**: Minimal memory usage for analysis
- **Parallel Safe**: Can run multiple instances safely

## 🔧 Requirements

### Required Binaries
- `git` - For repository cloning
- `ls` - For file listing
- `cat` - For file content viewing
- `curl` - For GitHub API calls
- `jq` - For JSON parsing

### Installation
```bash
# Ubuntu/Debian
sudo apt install git curl jq

# macOS
brew install git curl jq
```

## 📚 References

- [GitHub Security Best Practices](https://docs.github.com/en/security)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [npm Security Audit Guide](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)
- [Git Shallow Clone Documentation](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---depthltdepthgt)

## 🆘 Troubleshooting

### Common Issues

1. **URL Validation Failed**
   - Ensure URL starts with `https://github.com/`
   - Check for typos in repository name
   - Verify repository exists

2. **API Rate Limit Exceeded**
   - Wait before retrying
   - Consider using GitHub token for higher limits
   - Reduce frequency of checks

3. **Permission Denied**
   - Check directory permissions
   - Use temporary directory (`/tmp/`)
   - Ensure write permissions

### Debug Mode
```bash
export GITHUB_CLONE_VERBOSE=1
./scripts/safe_clone.sh https://github.com/psf/requests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with security in mind
4. Run security tests
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

- Issues: [GitHub Issues](https://github.com/openclaw/skills/issues)
- Documentation: [OpenClaw Docs](https://docs.openclaw.ai)
- Community: [Discord](https://discord.com/invite/clawd)

---

**Security First, Trust But Verify.** 🛡️

*Version: 2.0.1*
*Last Updated: 2026-03-22*