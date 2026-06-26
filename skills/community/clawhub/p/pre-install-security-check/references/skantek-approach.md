# Skantek Approach (Adyen)

This document details Adyen's approach to securing npm dependencies, as implemented in their internal tool **Skantek**.

## Background

Adyen is a fintech company processing sensitive payment data. Before adopting Node.js, they needed automated dependency verification to secure npm packages.

## Core Problem: NPM is Insecure

**Key issues:**
1. **No enforced uniformity** in package.json (license, source link are optional)
2. **Source code not visible** on npm website
3. **Lifecycle scripts** (preinstall/postinstall) can execute shell commands
4. **Nested dependencies** ("sinister Matryoshka dolls") — any level can be malicious

**Famous example:** left-pad incident (2016) — small utility package broke thousands of projects when unpublished.

## Skantek's Solution

### Metrics Used

Skantek scans packages based on:

1. **Presence, location, and length of README**
2. **Link to source code** (GitHub URL in package.json)
3. **Vulnerability databases** (Snyk, npm audit)
4. **License presence** and type

### Risk Scoring

Similar to fraud detection:

- Not binary (safe/unsafe)
- Combination of data points
- Threshold determines if manual review needed
- **Risk score increases** with irregularities

### Workflow

1. **Fetch metadata** from npm
2. **Resolve dependency tree** (all nested dependencies)
3. **Traverse tree** and scan each package
4. **Assign risk score** to each
5. **If threshold exceeded** → flag for manual review
6. **If approved** → publish to private npm registry

### Key Features

- **Regular rescanning** — Catches new vulnerabilities
- **Delayed updates** — Reduces zero-day exploit risk
- **Private registry** — Only approved packages available
- **Manual approval team** — Reviews flagged packages

## Lessons Learned

### 1. Dependency Trees Are Deep

**Problem:** Some trees are massive, with hundreds of nested dependencies.

**Solution:** 
- Refactor to traverse tree only once
- Perform all checks in single pass
- More efficient, easier to maintain

### 2. License Detection Is Hard

**Problem:** Authors put license in README but not in package.json.

**Solution:**
- Parse README for license info
- Manual checks when needed
- Encourage developers to use package.json

### 3. Fewer Dependencies = Better

**Recommendation:** When choosing packages, prefer those with fewer dependencies.

**Rationale:**
- Easier to review code
- Less surface area for attacks
- Simpler to maintain

## Implementation Details

### Performance

**Current:**
- Traverses dependency tree **three times**
- Taxing on performance for large trees

**Planned:**
- Touch each dependency **once**
- Run all checks in single pass

### Automation

**Cron job** runs regularly:
- Rescans all packages
- Detects changes
- Flags new vulnerabilities
- Alerts security team

### Logging & Visualization

**Goal:** Security team can see at-a-glance:
- Which licenses changed
- New vulnerabilities discovered
- Packages needing review

## NPM Approval Team

**Responsibilities:**
1. Administer and support Skantek
2. Approve packages for internal registry
3. Develop protocols for vulnerabilities
4. Work with security on remediation:
   - Fork and patch
   - Submit pull requests
   - Remove if necessary

## Future Enhancements

### 1. Code Pattern Detection

**Current:** Scans metadata and structure.

**Planned:** Scan actual code for dangerous patterns:
- eval() usage
- child_process.exec()
- Suspicious network calls

### 2. Batch Scanning

**Goal:** Scan multiple packages simultaneously (after recursion optimization).

### 3. Open Source Release

**Plan:** Share Skantek with community once mature.

**Rationale:** Security is an arms race — community benefits from shared tools.

## Key Takeaway

> "Sometimes in tech, people rush into adapting new technologies to 'get things done' without considering the dangers. It's the equivalent of a driver saying 'We're going really fast in this car, no roof, no brakes, no seatbelt, but we're really getting places!'"

Skantek's approach: **Go far, go fast, arrive safely.**

## References

- Original article: [Skantek: Securing NodeJS at Adyen](https://medium.com/adyen/skantek-securing-nodejs-at-adyen-f944283ce7c9)
- Snyk: https://snyk.io
- npm audit: https://docs.npmjs.com/cli/audit
