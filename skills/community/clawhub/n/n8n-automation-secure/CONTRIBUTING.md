# Contributing to N8N Automation Secure

Thank you for considering contributing to **N8N Automation Secure**! This project prioritizes security above all else.

## 🤝 Code of Conduct

- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards other community members

## 🎯 Contribution Guidelines

### Security is Non-Negotiable

**EVERY contribution must maintain security guarantees:**

1. **Credential Isolation** - Never store credentials in files
2. **Input Validation** - Always validate and sanitize inputs
3. **Audit Logging** - Log all actions with timestamps
4. **Permissions** - Respect permission levels
5. **HTTPS Only** - Enforce encrypted connections
6. **Confirmation Required** - Dangerous operations need approval

### What We Accept

- ✅ Bug fixes (with security analysis)
- ✅ Security improvements
- ✅ Documentation improvements
- ✅ Test cases
- ✅ Performance optimizations (without compromising security)
- ✅ New features (with security review)

### What We Reject

- ❌ Features that bypass security validations
- ❌ Removal of audit logging
- ❌ Hardcoded credentials or URLs
- ❌ Weakening of permission systems
- ❌ Removal of confirmation requirements
- ❌ Insecure defaults

## 🔧 Development Setup

### Prerequisites

- Node.js >= 18.0.0
- Git
- An n8n instance (for testing)

### Setup

```bash
# Clone repository
git clone https://github.com/nelson-mazonzika/openclaw-n8n-automation-secure.git
cd openclaw-n8n-automation-secure

# Set up test environment
export N8N_URL="https://your-test-n8n.com"
export N8N_API_KEY="your-test-api-key"

# Validate setup
./scripts/validate-setup.sh
```

### Testing

```bash
# Run validation script
./scripts/validate-setup.sh

# Test API connectivity
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# Test audit logging
# Check that logs are created in /data/.openclaw/logs/n8n-audit.log
```

## 📝 Submitting Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/security-issue-123
```

### 2. Make Your Changes

- Follow existing code style
- Add/update documentation
- Include security analysis for changes
- Test thoroughly

### 3. Commit

```bash
git add .
git commit -m "feat: add XYZ feature with security validation

- Added input validation for XYZ
- Updated audit logging
- Added test cases
- Updated SKILL.md

Security: No credentials stored, HTTPS enforced"
```

### 4. Push

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- Clear description of changes
- Security analysis section
- Testing steps
- Related issue numbers

## 🔐 Security Review Checklist

Before submitting, verify:

- [ ] No credentials stored in files
- [ ] All inputs validated and sanitized
- [ ] Audit logging added/updated
- [ ] HTTPS enforced
- [ ] Permissions respected
- [ ] Confirmation required for dangerous ops
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No hardcoded URLs
- [ ] No eval() or unsafe functions

## 🐛 Bug Reports

### Template

```markdown
**Description:** Clear description of the bug

**Reproduction Steps:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:**
- OS: [Linux/macOS/Windows]
- Node version: [v18.x.x]
- N8N version: [x.x.x]
- Permission mode: [readonly/restricted/full]

**Security Impact:** [Low/Medium/High/Critical]
**Proposed Fix:** [Your suggestion]

**Logs:** [Relevant audit logs]
```

## ✨ Feature Requests

### Template

```markdown
**Problem Statement:** What problem does this solve?

**Proposed Solution:** How should it work?

**Security Considerations:**
- How does this affect security?
- What validations are needed?
- What should be logged?

**Alternatives Considered:** Other approaches you thought of

**Additional Context:** Any other relevant info
```

## 📚 Documentation

All changes must include:

1. **SKILL.md** - Main documentation update
2. **README.md** - User-facing documentation (if user-visible)
3. **security.md** - Security architecture update (if security changes)
4. **Changelog** - Version history update

### Documentation Style

- Clear and concise
- Security-first perspective
- Examples for every feature
- Security warnings for dangerous operations
- DO/DON'T sections for common pitfalls

## 🧪 Testing

### Test Categories

1. **Security Tests** - Credential handling, validation, sanitization
2. **Functional Tests** - Core functionality works
3. **Edge Cases** - Invalid inputs, network failures
4. **Permission Tests** - Each permission level works correctly
5. **Audit Tests** - Logs are created correctly

### Test Cases

For every feature, provide:

```bash
# Test case 1: Valid input
export N8N_URL="https://valid-n8n.com"
./scripts/validate-setup.sh
# Expected: Success

# Test case 2: Invalid URL
export N8N_URL="http://insecure.com"
./scripts/validate-setup.sh
# Expected: Error - must use HTTPS

# Test case 3: Missing credentials
unset N8N_API_KEY
./scripts/validate-setup.sh
# Expected: Error - N8N_API_KEY not set
```

## 🔄 Release Process

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking security changes or API changes
- **MINOR:** New features (backwards compatible)
- **PATCH:** Bug fixes or documentation updates

### Release Checklist

- [ ] All tests passing
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] SKILL.md version bumped
- [ ] _meta.json updated
- [ ] Tagged release: `git tag -a v1.x.x -m "Release notes"`
- [ ] Pushed to ClawHub: `clawhub publish .`

### Release Template

```markdown
## Release v1.x.x

### Added
- New feature 1
- New feature 2

### Fixed
- Bug fix 1
- Bug fix 2

### Security
- Security improvement 1
- Security improvement 2

### Changed
- Breaking change (if any)

### Docs
- Documentation updates
```

## 🎓 Getting Help

- **Documentation:** `references/security.md`, `SKILL.md`
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions (if enabled)
- **Security Issues:** Use private channels only

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

---

**Remember:** Security is not a feature, it's a mindset. Every line of code you write should be reviewed through this security lens.

Thank you for contributing to secure n8n automation! 🔒
