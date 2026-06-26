# Contributing to HKO Weather Skill

Thank you for your interest in contributing! This guide will help you get started.

## How to Contribute

### 1. Report Issues

Found a bug or have a feature request? Please open an issue on GitHub:

- **Bug Reports:** Include steps to reproduce, expected vs actual behavior, and environment details
- **Feature Requests:** Describe the use case and expected functionality
- **Documentation Issues:** Note what's unclear, missing, or incorrect

### 2. Submit Pull Requests

We welcome PRs! Here's the process:

1. **Fork the repository** on GitHub
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-123
   ```
3. **Make your changes** following our code style guidelines
4. **Test your changes** (see Testing section below)
5. **Commit with clear messages** (see Commit Guidelines)
6. **Push and open a PR** against the `main` branch

### 3. Code Review

All PRs require review. Be prepared to:
- Address feedback from reviewers
- Make additional changes if requested
- Wait for approval before merging

## Code Style Guidelines

### Shell Scripts

```bash
#!/bin/bash

# Use descriptive variable names
weather_data=""
api_endpoint="https://www.hko.gov.hk"

# Use functions for reusable logic
fetch_weather() {
    local location="$1"
    curl -s "${api_endpoint}/weather/${location}"
}

# Always check return codes
if ! fetch_weather "hong-kong"; then
    echo "Failed to fetch weather" >&2
    exit 1
fi
```

**Guidelines:**
- Use `shellcheck` to lint scripts: `shellcheck scripts/*.sh`
- Quote all variables: `"$var"` not `$var`
- Use `local` for function variables
- Add comments for complex logic
- Keep functions small and focused

### JSON Configuration

```json
{
  "key": "value",
  "nested": {
    "object": true
  }
}
```

**Guidelines:**
- Use 2-space indentation
- Alphabetize keys when practical
- No trailing commas
- Validate with `jq`: `jq . config.json`

### Documentation (Markdown)

**Guidelines:**
- Use ATX-style headers (`# Header`)
- Keep lines under 100 characters when possible
- Use code blocks for commands and examples
- Include descriptions for all configuration options

## Testing Requirements

### Manual Testing

Before submitting a PR, test:

1. **Installation**
   ```bash
   ./install.sh
   openclaw skills list | grep hko-weather
   ```

2. **Basic Functionality**
   ```bash
   # Test weather fetch
   bash scripts/fetch-weather.sh
   
   # Test API connectivity
   bash scripts/test-hko.sh
   ```

3. **Uninstall**
   ```bash
   ./install.sh --uninstall
   ```

### Automated Testing

If adding new features, include tests:

```bash
#!/bin/bash
# scripts/test-feature.sh

test_feature_name() {
    local result
    result=$(your_command)
    
    if [[ "$result" == "expected" ]]; then
        echo "✓ test_feature_name passed"
        return 0
    else
        echo "✗ test_feature_name failed"
        return 1
    fi
}

# Run all tests
test_feature_name
```

### CI/CD

We use GitHub Actions for continuous integration. Your PR will automatically:
- Run shellcheck on all scripts
- Validate JSON files
- Test installation process
- Verify API connectivity

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add support for 9-day forecast

Extended forecast from 7 to 9 days using new HKO API endpoint.

Closes #42
```

```
fix(installer): handle missing jq dependency

Added proper error message when jq is not installed.
```

### Before You Commit

```bash
# Run linting
shellcheck scripts/*.sh install.sh

# Validate JSON
jq . clawhub.json > /dev/null

# Test installation
./install.sh --verbose
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if adding features
   - Update CHANGELOG if applicable
   - Ensure all configuration options are documented

2. **Verify Tests Pass**
   - All existing tests must pass
   - New features should include tests

3. **Request Review**
   - Tag relevant maintainers
   - Describe what changed and why
   - Link to related issues

4. **Address Feedback**
   - Respond to all comments
   - Make requested changes
   - Re-request review when ready

5. **Merge**
   - PR must be approved by at least one maintainer
   - All CI checks must pass
   - Squash commits if appropriate

## Development Setup

### Prerequisites

- Bash 4.0+
- curl
- jq
- shellcheck (for linting)
- OpenClaw (for integration testing)

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hko-weather-skill.git
cd hko-weather-skill

# Create a branch
git checkout -b feature/my-feature

# Make changes and test
# ...

# Commit and push
git commit -m "feat: add my feature"
git push origin feature/my-feature
```

## Questions?

- **General questions:** Open a discussion on GitHub
- **Bug reports:** Create an issue with reproduction steps
- **Security issues:** Email security@openclaw.dev (do not open public issue)

## License Compliance Requirements

### HKO Data Terms

**All contributors must preserve HKO data license terms:**

1. **Attribution Required**: Any output displaying HKO weather data must include:
   - Source attribution: "資料來源：香港天文台 (https://www.hko.gov.hk)"
   - Copyright notice: "© Government of the Hong Kong Special Administrative Region"

2. **Disclaimer Required**: All weather outputs must include or reference the HKO disclaimer (see LICENSE file for full text)

3. **Non-Commercial Use**: HKO data is for non-commercial use only. Do not add features that:
   - Sell or monetize HKO data
   - Enable commercial exploitation without written permission
   - Remove or obscure required attribution/disclaimer

4. **No IP Claims**: Do not claim intellectual property rights in HKO data

### Code vs Data Licensing

- **Skill code** (your contributions): Can be MIT or other permissive license
- **HKO weather data**: Must remain under HKO terms (CC BY-NC 4.0 / non-commercial)

Make this distinction clear in any new documentation or features you add.

### Before Submitting a PR

Verify license compliance:
```bash
# Check that attribution is present in output scripts
grep -r "hko.gov.hk" scripts/

# Check that disclaimer is included
grep -r "免責聲明\|disclaimer" scripts/
```

## Code of Conduct

Please be respectful and constructive in all interactions. We're building something together!

---

**Thank you for contributing to the HKO Weather Skill!** 🌦️
