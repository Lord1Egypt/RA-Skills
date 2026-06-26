# npm-supply-chain-security

## Description
Protect your JavaScript projects from npm supply chain attacks. Learn to identify malicious packages, implement trusted publishing, and use security heuristics to detect compromised dependencies.

## Implementation

NPM supply chain attacks have become increasingly common, with recent incidents affecting packages with millions of weekly downloads. The Axios attack in March 2026 demonstrated how leaked long-lived npm tokens can be exploited to publish malicious dependencies.

### Key Security Practices:
- **Trusted Publishing**: Configure GitHub Actions workflows as the only authorized publishers to npm
- **Release Verification**: Check for accompanying GitHub releases when new package versions are published
- **Dependency Monitoring**: Watch for newly published dependencies in established packages
- **Token Management**: Use short-lived, scoped tokens instead of long-lived global tokens

### Red Flags for Malicious Packages:
- New dependencies added to established packages
- Versions published without corresponding GitHub releases
- Freshly published dependency packages with suspicious names
- Unusual code patterns or obfuscated implementations

## Code Examples

### Example 1: Configure Trusted Publishing
```json
{
  "name": "your-package",
  "version": "1.0.0",
  "publishConfig": {
    "registry": "https://registry.npmjs.org/",
    "provenance": true
  },
  "scripts": {
    "release": "npm publish --provenance"
  }
}
```

### Example 2: GitHub Actions Workflow for Trusted Publishing
```yaml
name: Publish Package
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Required for trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Example 3: Security Heuristic Checker
```python
import requests
import json

def check_package_release_heuristic(package_name, version):
    """Check if package version has corresponding GitHub release"""
    # Get package info from npm registry
    npm_url = f"https://registry.npmjs.org/{package_name}/{version}"
    npm_response = requests.get(npm_url)
    
    if npm_response.status_code != 200:
        return False, "Package version not found"
    
    npm_data = npm_response.json()
    repository = npm_data.get('repository', {}).get('url', '')
    
    if 'github.com' not in repository:
        return True, "Non-GitHub repository"  # Can't verify
    
    # Extract GitHub repo info
    repo_parts = repository.replace('https://github.com/', '').replace('.git', '').split('/')
    if len(repo_parts) != 2:
        return True, "Invalid repository format"
    
    owner, repo = repo_parts
    github_release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/v{version}"
    github_response = requests.get(github_release_url)
    
    if github_response.status_code == 200:
        return True, "GitHub release found"
    else:
        return False, "No corresponding GitHub release - potential red flag!"

# Usage
safe, message = check_package_release_heuristic("axios", "1.14.1")
print(f"Security check: {safe} - {message}")
```

### Example 4: Dependency Audit Script
```javascript
const fs = require('fs');
const path = require('path');

function auditDependencies(packageJsonPath) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const dependencies = {...packageJson.dependencies, ...packageJson.devDependencies};
    
    // Check for recently published packages (simplified)
    const suspiciousPatterns = [
        'crypto-js', 'plain-', 'simple-', 'basic-', 'core-'
    ];
    
    const suspiciousDeps = [];
    for (const [dep, version] of Object.entries(dependencies)) {
        // Check if dependency name matches suspicious patterns
        if (suspiciousPatterns.some(pattern => dep.includes(pattern))) {
            suspiciousDeps.push(dep);
        }
    }
    
    return suspiciousDeps;
}

// Usage
const suspicious = auditDependencies('./package.json');
if (suspicious.length > 0) {
    console.warn('Suspicious dependencies detected:', suspicious);
}
```

## Dependencies
- Python 3.8+ (for security scripts)
- requests library
- Node.js 18+ (for npm workflows)
- GitHub CLI (optional, for automated verification)