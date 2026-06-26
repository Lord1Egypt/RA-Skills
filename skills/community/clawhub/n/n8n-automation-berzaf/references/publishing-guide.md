# Publishing to ClawHub — Step by Step

Follow these exact steps to publish your n8n Automation Skill
to ClawHub and start getting installs.

---

## Pre-Publishing Checklist

Before publishing, confirm everything is ready:

- [ ] SKILL.md is complete and tested locally
- [ ] README.md is written (appears on ClawHub listing page)
- [ ] All workflow templates documented in references/
- [ ] Skill works on your own OpenClaw — tested all 8 workflows
- [ ] No API keys or secrets anywhere in the files
- [ ] GitHub account is more than 1 week old
- [ ] Chosen a unique slug (check clawhub.com that it is not taken)

---

## Step 1 — Install the ClawHub CLI

```bash
npm i -g clawhub
```

Verify install:
```bash
clawhub --version
```

---

## Step 2 — Login with GitHub

```bash
clawhub login
```

This opens your browser. Authorize with GitHub. Done.

---

## Step 3 — Check Your Slug is Available

Before publishing, verify your chosen slug is not taken:

```bash
clawhub inspect n8n-automation-berzaf
```

If it returns "not found" — the slug is available. Good.

---

## Step 4 — Publish

From the parent folder of your skill:

```bash
clawhub publish ./n8n-automation-skill \
  --slug n8n-automation-berzaf \
  --name "n8n Workflow Automation" \
  --version 1.0.0 \
  --tags latest
```

You will see:
```
✅ Published n8n-automation-berzaf v1.0.0
   View at: clawhub.com/skills/n8n-automation-berzaf
```

---

## Step 5 — Verify Your Listing

Open `clawhub.com/skills/n8n-automation-berzaf`

Check that:
- Name shows correctly
- Description is visible
- README content renders
- SKILL.md is viewable (transparency builds trust)
- No credentials leaked

---

## How People Install Your Skill

Anyone can install with one command:
```bash
clawhub install n8n-automation-berzaf
```

Or they can tell their OpenClaw agent:
```
"Install the n8n automation skill by berzaf"
```

---

## Publishing Updates

When you add more workflows or fix bugs:

```bash
clawhub publish ./n8n-automation-skill \
  --slug n8n-automation-berzaf \
  --version 1.1.0 \
  --tags latest
```

Only you (the original publisher) can update your own slug.

---

## After Publishing — How to Promote

**Post on X/Twitter:**
```
Just published my n8n + OpenClaw skill on ClawHub 🔥

Trigger any n8n workflow from natural language:
- Lead nurture sequences
- Social media auto-post
- Meeting follow-ups
- CRM updates
- Invoice reminders
- Daily briefings

Install: clawhub install n8n-automation-berzaf

#OpenClaw #n8n #automation
```

**Post on Reddit:**
- r/openclaw
- r/n8n
- r/selfhosted
- r/automation

**Title:** "I built an n8n skill for OpenClaw — trigger any workflow with natural language"

**Post on Berzaf AI Automation YouTube:**
- Make a video showing it working
- Link to ClawHub in description
- Show the before (manually triggering) vs after (just talking)

---

## Monetization After Publishing

**Free skill → paid setup:**
- Skill is free on ClawHub
- Offer "$299 Full n8n + OpenClaw Setup" in your README
- Link to your YouTube channel
- People who install will become consulting leads

**Upsell to automation consulting:**
- Anyone who installs needs their n8n configured
- Your consulting rate: $500–$2,500 per setup
- Monthly retainer: $100–$300/month maintenance

**YouTube content:**
- Tutorial showing the skill working = views
- Views = channel growth = more consulting leads
- Position yourself as THE n8n + OpenClaw expert

---

## Tracking Your Installs

ClawHub shows install counts on your skill page.
Check it at: `clawhub.com/skills/n8n-automation-berzaf`

Every install = a potential consulting lead.
Consider adding a "Get Custom Setup Help" section in README
linking to a simple contact form or your YouTube community post.
