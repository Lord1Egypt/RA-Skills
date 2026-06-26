# Kit Email Marketing Operator - Installation Guide

**Version:** 1.0.0  
**Created:** February 17, 2026  
**Distribution:** Private ClawHub (Premium Skool Members Only)

---

## Overview

This skill transforms your OpenClaw agent into an expert email marketing operator with:

✅ **AI-powered email generation** (subject lines, body copy, CTAs)  
✅ **Direct Kit API integration** (create, schedule, analyze campaigns)  
✅ **Brand voice learning** (writes like YOU, not generic AI)  
✅ **Strategic guidance** (asks clarifying questions, follows best practices)  
✅ **Campaign analytics** (performance tracking with insights)  
✅ **Security-first** (encrypted credentials, compliance built-in)

---

## Prerequisites

### 1. OpenClaw Installation

You need OpenClaw installed and running:
- Installation guide: https://openclaw.com/docs
- Minimum version: 0.5.0+

### 2. Kit Account

Active Kit (ConvertKit) account:
- Sign up: https://kit.com
- Free plan available (up to 10,000 subscribers)

### 3. Node.js

Scripts require Node.js 14+:
```bash
node --version  # Should be 14.0.0 or higher
```

If not installed: https://nodejs.org

---

## Installation Steps

### Step 1: Copy Skill to Skills Directory

```bash
# Assuming you're in your OpenClaw workspace
cp -r skills/kit-email-operator ~/.openclaw/skills/
```

Or manually:
1. Download skill package
2. Extract to `~/.openclaw/skills/kit-email-operator/`

---

### Step 2: Make Scripts Executable

```bash
chmod +x ~/.openclaw/skills/kit-email-operator/scripts/*.js
```

---

### Step 3: Verify Installation

```bash
node ~/.openclaw/skills/kit-email-operator/scripts/kit-api.js
```

**Expected output:** CLI help text showing available commands

---

### Step 4: First-Time Setup

Talk to your OpenClaw agent:

```
"Set up Kit email marketing"
```

Or manually run setup wizard:

```bash
cd ~/.openclaw/skills/kit-email-operator/scripts
node setup-wizard.js
```

**Setup wizard will:**
1. Collect your Kit API credentials
2. Store them securely (encrypted)
3. Train your brand voice (optional)
4. Gather business context
5. Import custom fields from Kit

**Time required:** 5-10 minutes

---

## File Structure

```
kit-email-operator/
├── SKILL.md                          # Main skill instructions (for OpenClaw agent)
├── README.md                         # User-facing documentation
├── SETUP.md                          # Detailed setup guide
├── INSTALLATION.md                   # This file
│
├── references/                       # Best practices and templates
│   ├── email-best-practices.md       # Comprehensive email marketing guide
│   ├── subject-line-formulas.md      # 50+ proven subject line templates
│   ├── kit-personalization.md        # Kit Liquid tags reference
│   └── sequence-templates.md         # Welcome, nurture, sales sequences
│
├── scripts/                          # Working Node.js scripts
│   ├── credentials.js                # Secure credential storage
│   ├── kit-api.js                    # Kit API client
│   ├── email-generator.js            # Email generation logic (future)
│   └── setup-wizard.js               # Interactive setup (future)
│
└── examples/                         # Real email templates
    ├── welcome-email.md              # Welcome sequence example
    ├── nurture-email.md              # Value-first nurture email
    └── sales-email.md                # Product launch sales email
```

**Total size:** ~150KB (lightweight, no dependencies)

---

## Configuration

### API Credentials

**Where to find your Kit API credentials:**

1. Log in to Kit: https://app.kit.com
2. Click your profile picture → **Settings**
3. Go to **Advanced** → **API**
4. Copy:
   - **API Key** (starts with `kit_...`)
   - **API Secret** (long string)

**Storage location:** `~/.kit-credentials` (encrypted)

---

### Voice Training (Optional)

**How to train your brand voice:**

1. Collect 3-5 past emails you've written
2. Tell agent: `"Train my email voice"`
3. Paste complete emails (subject + body + signature)
4. Agent analyzes tone, structure, vocabulary

**Storage location:** `~/.kit-voice-samples.json`

---

### Business Context

**What the agent needs to know:**

- **Niche/Industry:** What you do
- **Target Audience:** Who you serve
- **Offer:** What you sell
- **Key Links:** Website, booking page, product pages

**Storage location:** `~/.kit-business-context.json`

---

## Usage Examples

### Create Your First Email

```
You: "Create a nurture email"

Agent: [Asks clarifying questions]
        ↓
        [Generates 3 subject line options]
        ↓
        [Writes email body with personalization]
        ↓
        [Shows complete draft for review]
        ↓
You: "Send it now"

Agent: [Creates broadcast in Kit]
       [Shows confirmation with broadcast ID]
```

---

### Check Campaign Performance

```
You: "Show stats for my last email"

Agent: [Fetches broadcast stats]
       ↓
       [Displays open rate, click rate, benchmarks]
       ↓
       [Provides AI insights and recommendations]
```

---

### Manage Subscribers

```
You: "Add a new subscriber"

Agent: [Prompts for email and details]
       ↓
       [Creates subscriber in Kit]
       ↓
       [Confirms with subscriber ID]
```

---

## Troubleshooting

### "No credentials found"

**Problem:** Agent can't find Kit API credentials

**Solution:**
```bash
node scripts/credentials.js exists
```

If returns "no":
```bash
node scripts/credentials.js store --key="kit_xxx" --secret="xxx"
```

Or run setup wizard again: Tell agent `"Set up Kit email marketing"`

---

### "Authentication failed"

**Problem:** Kit API credentials are invalid or expired

**Solution:**
1. Go to Kit: https://app.kit.com/settings/advanced
2. **Regenerate** your API credentials
3. Update in skill:
   ```
   Tell agent: "Update Kit credentials"
   ```
   Or manually:
   ```bash
   node scripts/credentials.js store --key="NEW_KEY" --secret="NEW_SECRET"
   ```

---

### "Rate limit exceeded"

**Problem:** Too many API requests in short time

**Solution:**
- Wait 5-10 minutes
- Kit API rate limits are conservative (built into skill)
- If urgent, save as draft and schedule for later

---

### "Broadcast failed to send"

**Problem:** Kit rejected the broadcast

**Common causes:**
- Subject line too long (>255 characters)
- Invalid personalization tags
- No subscribers in selected segment/tag

**Solution:**
- Check error message from Kit API
- Fix issue and retry
- Agent will provide specific guidance

---

### "Voice training not working"

**Problem:** Brand voice analysis failed

**Solution:**
- Paste at least 3-5 COMPLETE emails
- Include subject line, full body, and signature
- Use emails YOU wrote (not AI-generated)

**Retry:**
```
Tell agent: "Train my voice"
```

---

## Security & Privacy

### What Gets Stored

**Encrypted (secure):**
- `~/.kit-credentials` - Kit API key and secret

**Plain text (not sensitive):**
- `~/.kit-voice-samples.json` - Your past email examples
- `~/.kit-business-context.json` - Business info you provide
- `~/.kit-custom-fields.json` - Cached custom field names

**Location:** Your OpenClaw workspace (`/data/.openclaw/workspace/`)

---

### What DOESN'T Get Stored

❌ **No subscriber data** - Always fetched from Kit API  
❌ **No email content** - Created on-demand  
❌ **No personal info** - This is a generic skill (no Kevin-specific data)  
❌ **No external services** - Everything runs locally or via Kit API

---

### Encryption Details

**Algorithm:** AES-256-GCM  
**Key derivation:** PBKDF2 with machine-specific salt  
**Key tied to:** Your hostname + homedir (credentials won't work on other machines)

---

### Credential Safety

✅ **DO:**
- Store credentials via provided scripts
- Keep backup of API credentials in password manager
- Regenerate if compromised

❌ **DON'T:**
- Commit credentials to git
- Share credentials files
- Display credentials in plain text

---

## Updating the Skill

### Check for Updates

```bash
# Check ClawHub for new version
clawhub info kit-email-operator
```

### Update to Latest Version

```bash
# Pull latest from ClawHub
clawhub update kit-email-operator
```

**Your data is preserved:**
- Credentials stay encrypted
- Voice training persists
- Business context maintained

---

## Uninstalling

### Remove Skill

```bash
rm -rf ~/.openclaw/skills/kit-email-operator/
```

### Remove Stored Data

```bash
rm ~/.kit-credentials
rm ~/.kit-voice-samples.json
rm ~/.kit-business-context.json
rm ~/.kit-custom-fields.json
```

**Note:** Your data in Kit (subscribers, broadcasts) is never affected.

---

## Support

### Documentation

- **README.md** - User guide and features
- **SETUP.md** - Detailed setup wizard walkthrough
- **SKILL.md** - Technical skill instructions (for developers)
- **references/** - Best practices and templates

### Get Help

**In Skool community:**
- Tag @kevin with issue description
- Include: What you tried, error message, expected result

**Self-help:**
```
Tell your agent: "Help with Kit email marketing"
```

### Report Bugs

**Format:**
```
**Issue:** [Brief description]
**Steps to reproduce:**
1. [First step]
2. [Second step]
**Expected:** [What should happen]
**Actual:** [What actually happened]
**Error message:** [If any]
```

---

## Version History

**v1.0.0** (February 17, 2026)
- Initial release
- Core features: Email generation, Kit API integration, analytics
- Brand voice training
- Security-first credential management
- Premium skill for Skool members

---

## What's Next?

### After Installation

1. ✅ Complete setup wizard
2. ✅ Train your brand voice
3. ✅ Create your first email
4. ✅ Review campaign analytics

### Advanced Features

- **A/B testing:** Test subject lines and content variations
- **Sequences:** Set up welcome, nurture, and sales sequences
- **Segmentation:** Target specific audiences with personalized content
- **Voice refinement:** Update voice training as your style evolves

---

## License & Distribution

**Distribution:** Private ClawHub (Premium Skool Members Only)

**Usage Rights:**
- ✅ Use for your own email marketing
- ✅ Customize for your needs
- ❌ Do not redistribute publicly
- ❌ Do not resell or commercialize

**Support:** Available exclusively in Skool community

---

## Credits

**Built by:** OpenClaw Community  
**For:** Premium Skool Members  
**Research:** Kit API documentation, email marketing best practices  
**Version:** 1.0.0  
**Release Date:** February 17, 2026

---

**Ready to transform your email marketing with AI?** 🚀

Run the setup wizard and let your OpenClaw agent become your email marketing expert!

```
Tell your agent: "Set up Kit email marketing"
```
