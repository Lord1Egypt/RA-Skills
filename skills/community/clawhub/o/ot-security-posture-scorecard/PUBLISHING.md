# Publishing to ClawHub — Step by Step

## 1. Prerequisites

```bash
# Install the ClawHub CLI
npm install -g clawhub

# Login to ClawHub
clawhub login
```

## 2. Check for Name Collisions

```bash
clawhub search "ot-security"
clawhub search "scada security"
clawhub search "ics security posture"
```

If no conflicts, proceed with publishing.

## 3. Validate Your Skill

```bash
# Navigate to the skill directory
cd ot-security-posture-scorecard/

# Verify structure
ls -la
# Should show: SKILL.md, README.md, scripts/

# Check SKILL.md frontmatter is valid
head -20 SKILL.md
```

## 4. Publish

```bash
# First publish
clawhub publish

# This will:
# - Parse SKILL.md frontmatter
# - Upload all text-based files (SKILL.md, README.md, scripts/*.sh)
# - Create version 1.0.0
# - Tag as "latest"
# - Run VirusTotal security scan
```

## 5. Verify

```bash
# Search for your published skill
clawhub search "ot-security-posture-scorecard"

# Check the ClawHub page
# https://clawhub.ai/skills/ot-security-posture-scorecard
```

## 6. Promote

After publishing, promote your skill:

### On Moltbook (the agent social network)
Ask your OpenClaw agent:
> "Post on Moltbook about the new OT Security Posture Scorecard skill I published on ClawHub. Highlight that it's built by a CISSP/CISM professional and covers IEC 62443 and NIST CSF."

### On ToolWeb.in
Add a page for the OpenClaw skill on your platform with:
- Install instructions
- Demo video (YouTube)
- Link to ClawHub listing

### On YouTube
Create a demo video showing:
1. Installing the skill in OpenClaw
2. Sending a message via WhatsApp/Telegram
3. Getting the scorecard results
4. Music: "After Sunset - Alex Jones | Xander Jones"

### On RapidAPI
Cross-reference the OpenClaw skill in your existing RapidAPI listing description.

## 7. Updating

```bash
# Bump version in SKILL.md frontmatter to 1.1.0
# Then:
clawhub publish
```

## 8. Monitor

- Check install counts on ClawHub
- Monitor API usage on portal.toolweb.in dashboard
- Respond to comments/reviews on ClawHub
