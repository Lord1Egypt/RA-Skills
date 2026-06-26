# SETUP-PROMPT.md - Email Assistant Setup Guide

**AGENT INSTRUCTIONS: Read and follow this file sequentially to set up the Email Assistant skill for the user.**

## 1. Locate the Skill Package

Find the skill package in the workspace. Run from the workspace root:

```bash
set -euo pipefail
IFS=$'\n\t'

# Verification: skill files installed by clawhub install
if [ "${#SKILL_PATHS[@]}" -eq 0 ]; then
  echo "ERROR: Could not find email-assistant skill package. Ensure it exists under a skills/ directory."
  exit 1
fi
if [ "${#SKILL_PATHS[@]}" -gt 1 ]; then
  echo "ERROR: Multiple email-assistant skill packages found. Keep only one to avoid copying untrusted files."
  printf '  - %s\n' "${SKILL_PATHS[@]}"
  exit 1
fi

SKILL_DIR=$(dirname "${SKILL_PATHS[0]}")
if [ ! -f "$SKILL_DIR/config/email-config.json" ] || [ ! -f "$SKILL_DIR/scripts/email-health-check.sh" ]; then
  echo "ERROR: Skill package is incomplete or unexpected: $SKILL_DIR"
  exit 1
fi

echo "Found skill at: $SKILL_DIR"
```

## 2. Create the Directory Structure

Create the data and config directories for storing email triage data. Use RELATIVE paths from the workspace root.

```bash
mkdir -p email-assistant/data/digests
chmod 700 email-assistant
chmod 700 email-assistant/data
chmod 700 email-assistant/data/digests
```

## 3. Initialize Data Files

Create the initial data files with secure permissions.

```bash
cat << 'EOF' > email-assistant/data/writing-style.json
{
  "tone": null,
  "avg_length": null,
  "greeting": null,
  "signoff": null,
  "uses_emoji": false,
  "sample_phrases": []
}
EOF
chmod 600 email-assistant/data/writing-style.json
```

## 4. Copy Configuration from Skill Package

Copy the default configuration file from the skill package to the user's data directory.

```bash
cp "$SKILL_DIR/config/email-config.json" email-assistant/data/email-config.json
chmod 600 email-assistant/data/email-config.json
```

## 5. Copy Health Check Script

```bash
mkdir -p email-assistant/scripts
chmod 700 email-assistant/scripts

cp "$SKILL_DIR/scripts/email-health-check.sh" email-assistant/scripts/email-health-check.sh
chmod 600 email-assistant/scripts/email-health-check.sh
```

## 6. Verify Email Tool Availability

Check that the user has an email access tool configured:

```bash
# Check for himalaya (recommended)
if command -v himalaya &> /dev/null; then
  echo "✅ himalaya CLI found"
  himalaya account list 2>/dev/null && echo "✅ himalaya accounts configured" || echo "⚠️ himalaya installed but no accounts configured"
# Check for gog (Google Workspace)
elif command -v gog &> /dev/null; then
  echo "✅ gog CLI found (Google Workspace)"
# Check for common IMAP tools
elif command -v neomutt &> /dev/null || command -v mutt &> /dev/null; then
  echo "✅ mutt/neomutt found (IMAP capable)"
else
  echo "⚠️ No email tool detected. You'll need to install one."
  echo "Recommended: himalaya (https://github.com/pimalaya/himalaya)"
  echo "Alternative: gog (for Google Workspace users)"
fi
```

## 7. Verify Setup

Confirm all files and directories exist with correct permissions:

```bash
echo "=== Email Assistant Setup Verification ==="
echo ""

# Check directories
for dir in email-assistant email-assistant/data email-assistant/data/digests email-assistant/scripts; do
  if [ -d "$dir" ]; then
    perms=$(stat -f "%Lp" "$dir" 2>/dev/null || stat -c "%a" "$dir" 2>/dev/null)
    echo "✅ $dir (permissions: $perms)"
  else
    echo "❌ MISSING: $dir"
  fi
done

# Check files
for file in email-assistant/data/writing-style.json email-assistant/data/email-config.json email-assistant/scripts/email-health-check.sh; do
  if [ -f "$file" ]; then
    perms=$(stat -f "%Lp" "$file" 2>/dev/null || stat -c "%a" "$file" 2>/dev/null)
    echo "✅ $file (permissions: $perms)"
  else
    echo "❌ MISSING: $file"
  fi
done

echo ""
echo "=== Verification Complete ==="
```

## 8. Introduce the Skill to the User

Send the following message to the user:

"✅ **Email Assistant is set up and secure!**

I've created your `email-assistant/` directory with `chmod 700/600` permissions to protect your email data.

You can now:
1. **Check your inbox:** 'What's in my inbox?' or 'Give me an email briefing.'
2. **Draft replies:** 'Draft a reply to the email from Sarah.'
3. **Set VIPs:** 'Add boss@company.com as a VIP sender.'
4. **Get digests:** 'Generate my daily email digest.'
5. **Configure cadence:** 'Check my email every morning at 8 AM.'

*Tip: Try 'What's in my inbox?' right now to see it in action!*"
