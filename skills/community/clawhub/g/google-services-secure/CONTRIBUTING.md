# Contributing to Google Services Secure

Thank you for considering contributing to **Google Services Secure**! This project prioritizes security above all else, especially OAuth token management and Google API security.

## 🤝 Code of Conduct

- Be respectful and constructive
- Focus on what is best for the community
- Show empathy towards other community members

## 🎯 Contribution Guidelines

### Security is Non-Negotiable

**EVERY contribution must maintain security guarantees:**

1. **OAuth Token Security** - Never store OAuth tokens in files
2. **Input Validation** - Always validate and sanitize inputs
3. **Audit Logging** - Log all actions with timestamps
4. **Permissions** - Respect permission levels
5. **OAuth Scopes** - Use minimal required scopes only
6. **HTTPS Only** - Enforce encrypted connections
7. **Confirmation Required** - Dangerous operations need approval

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
- ❌ Hardcoded OAuth tokens or secrets
- ❌ Weakening of permission systems
- ❌ Removal of confirmation requirements
- ❌ Insecure defaults
- ❌ Broad OAuth scopes without justification
- ❌ Token storage in files

## 🔧 Development Setup

### Prerequisites

- Node.js >= 18.0.0
- Git
- Google Cloud Project with APIs enabled
- OAuth 2.0 Client ID and Secret

### Setup

```bash
# Clone repository
git clone https://github.com/nelmaz/openclaw-google-services-secure.git
cd openclaw-google-services-secure

# Set up test environment
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:8080/callback"

# Validate setup
./scripts/validate-setup.sh

# Authenticate via OAuth
./scripts/auth-google.sh auth
```

### Testing

```bash
# Run validation script
./scripts/validate-setup.sh

# Test OAuth flow
./scripts/auth-google.sh auth
./scripts/auth-google.sh status

# Test API connectivity (after auth)
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  https://www.googleapis.com/oauth2/v3/tokeninfo
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
- Validate OAuth flow still works

### 3. Commit

```bash
git add .
git commit -m "feat: add XYZ feature with security validation

- Added input validation for XYZ
- Updated audit logging
- Added test cases
- Updated SKILL.md

Security: OAuth tokens stored in memory only, HTTPS enforced"
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

- [ ] No OAuth tokens or secrets stored in files
- [ ] All inputs validated and sanitized
- [ ] Audit logging added/updated
- [ ] HTTPS enforced
- [ ] Permissions respected
- [ ] OAuth scopes are minimal and justified
- [ ] Confirmation required for dangerous ops
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No hardcoded URLs or credentials
- [ ] No eval() or unsafe functions
- [ ] Input validation added
- [ ] OAuth flow tested end-to-end

## 🐛 Bug Reports

### Template

```markdown
**Description:** Clear description of bug

**Reproduction Steps:**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happened

**Environment:**
- OS: [Linux/macOS/Windows]
- Node version: [Run `node --version`]
- Google Cloud Project: [Your project ID]
- Permission mode: [readonly/restricted/full]
- Access token status: [Valid/Expired/Not set]

**OAuth Configuration:**
- Client ID: [From Google Cloud Console]
- Redirect URI: [Your redirect URI]
- Scopes: [List of OAuth scopes]

**Security Impact:** [Low/Medium/High/Critical]
**Proposed Fix:** [Your suggestion]

**Logs:** [Relevant audit logs]

**Error Messages:** [Full error output]
```

## ✨ Feature Requests

### Template

```markdown
**Problem Statement:** What problem does this solve?

**Proposed Solution:** How should it work?

**OAuth Considerations:**
- What OAuth scopes are needed?
- How does this affect token security?
- What validations are needed?
- What should be logged?

**Alternatives Considered:** Other approaches you thought of

**Additional Context:** Any other relevant info
```

## 🧪 Testing

### Test Categories

1. **Security Tests** - OAuth token handling, validation, sanitization
2. **OAuth Flow Tests** - Complete authentication flow
3. **Functional Tests** - Core functionality works
4. **Edge Cases** - Invalid inputs, network failures
5. **Permission Tests** - Each permission level works correctly
6. **Audit Tests** - Logs are created correctly
7. **Google API Tests** - Each service API works correctly

### Test Cases

For every feature, provide:

```bash
# Test case 1: Valid OAuth credentials
export GOOGLE_CLIENT_ID="valid-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="valid-secret"
./scripts/auth-google.sh auth
# Expected: Success, authorization URL generated

# Test case 2: Invalid client secret
export GOOGLE_CLIENT_SECRET="invalid"
./scripts/auth-google.sh auth
# Expected: Error - invalid credentials

# Test case 3: Missing access token
unset ACCESS_TOKEN
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages"
# Expected: 401 Unauthorized

# Test case 4: Valid API call (after auth)
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages"
# Expected: 200 OK with messages data
```

## 🔄 Release Process

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR:** Breaking security changes or OAuth flow changes
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
- [ ] Pushed to GitHub: `git push origin v1.x.x`
- [ ] Published to ClawHub: `clawhub publish . --version 1.x.y`

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
- **Google Cloud Docs:** https://developers.google.com/apis

## ⚖️ License

By contributing, you agree that your contributions will be licensed under **MIT License**.

---

**Remember:** Security is not a feature, it's a mindset. Every line of code you write should be reviewed through this security lens, especially for OAuth token management and Google API integration.

Thank you for contributing to secure Google services integration! 🔒
