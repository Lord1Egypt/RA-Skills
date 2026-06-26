# 🚀 Getting Started

## Quick Start Guide

Get OpenClaw Security Guard running in under 5 minutes.

---

## Step 1: Install

```bash
npm install -g openclaw-security-guard
```

Verify installation:

```bash
openclaw-guard --version
```

---

## Step 2: Run Your First Audit

Navigate to your OpenClaw directory and run:

```bash
cd ~/.openclaw
openclaw-guard audit
```

You'll see output like this:

```
🛡️ OpenClaw Security Guard v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Secrets Scanner............ ✅ No issues
🔧 Config Auditor............. ❌ 2 critical
💉 Injection Detector......... ✅ No issues
📦 Dependency Scanner......... ⚠️ 1 warning
🔌 MCP Server Auditor......... ✅ No issues
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Security Score: 65/100

🔴 Critical issues found!
   Run: openclaw-guard fix
```

---

## Step 3: Fix Issues

### Option A: Interactive Mode

```bash
openclaw-guard fix
```

You'll be prompted for each fix:

```
Found 2 fixable issue(s):

🔴 Sandbox mode is not set to 'always'
   Fix: Set sandbox.mode to 'always'

🟡 DM policy is set to 'open'
   Fix: Set dmPolicy to 'pairing'

? Apply these fixes? (y/N)
```

### Option B: Automatic Mode

```bash
openclaw-guard fix --auto
```

All fixes are applied automatically with backup.

---

## Step 4: Start the Dashboard

```bash
openclaw-guard dashboard
```

### First Time Setup

1. Browser opens to `http://localhost:18790`
2. You'll see the **Setup** page
3. Create a password (minimum 8 characters)
4. Click "Create Password"
5. You're in!

### Next Time

1. Run `openclaw-guard dashboard`
2. Enter your password
3. Access the dashboard

---

## Step 5: Set Up Pre-commit Hook (Optional)

Prevent accidentally committing secrets:

```bash
openclaw-guard hooks install
```

Now, every time you commit, secrets will be scanned automatically.

---

## What's Next?

- 📖 Read the [full documentation](./en/README.md)
- ⚙️ [Configure](./en/README.md#configuration) the tool to your needs
- 🔧 Learn about [all CLI commands](./api/cli.md)
- 🤝 [Contribute](../CONTRIBUTING.md) to the project

---

## Common Commands

```bash
# Full audit
openclaw-guard audit

# Deep audit (more thorough)
openclaw-guard audit --deep

# Quick audit (faster)
openclaw-guard audit --quick

# Fix issues interactively
openclaw-guard fix

# Fix automatically
openclaw-guard fix --auto

# Start dashboard
openclaw-guard dashboard

# Generate HTML report
openclaw-guard report -f html -o security-report.html

# Scan only for secrets
openclaw-guard scan secrets

# Check hook status
openclaw-guard hooks status

# Show help
openclaw-guard --help
```

---

## Troubleshooting

### Command not found?

```bash
# Use npx instead
npx openclaw-security-guard audit

# Or check your PATH
echo $PATH | grep npm
```

### Dashboard not opening?

```bash
# Check if port is in use
lsof -i :18790

# Try a different port
openclaw-guard dashboard --port 3000
```

### Forgot dashboard password?

```bash
# Delete auth file and restart
rm ~/.openclaw-security-guard/auth.json
openclaw-guard dashboard
```

---

## Need Help?

- 📖 [Documentation](https://github.com/2pidata/openclaw-security-guard/docs)
- 🐛 [Report Bug](https://github.com/2pidata/openclaw-security-guard/issues)
- 🌐 [2pidata.com](https://2pidata.com)

---

<div align="center">

**Made by [Miloud Belarebia](https://2pidata.com)** 🇲🇦

</div>
