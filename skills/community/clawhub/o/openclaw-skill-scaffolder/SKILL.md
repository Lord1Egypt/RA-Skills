---
name: openclaw-skill-scaffolder
description: Generate complete OpenClaw skill projects with SkillPay.me billing pre-wired. Describe what you want, get deployable code.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - SKILLPAY_API_KEY
    emoji: "🔧"
---

# OpenClaw Skill Scaffolder

Generate complete, deployable OpenClaw skills with SkillPay.me billing already wired up.

## How to Use This Skill

### Step 1: Charge billing and get templates

POST to the skill endpoint with your skill configuration:

```
POST https://openclaw-skill-scaffolder.swmengappdev.workers.dev/scaffold
Content-Type: application/json

{
  "user_id": "<user_id>",
  "name": "my-cool-skill",
  "description": "A skill that does something cool",
  "price_usdt": 0.01,
  "env_vars": ["SOME_API_KEY"]
}
```

The endpoint charges billing and returns scaffold templates:
- `SKILL.md` template
- `wrangler.toml` template
- `src/index.ts` worker template with SkillPay billing pre-wired
- `src/billing.ts` billing types
- Deploy commands

### Step 2: Generate custom logic

Using your own capabilities, generate the custom skill logic based on the user's description. The scaffold provides the boilerplate — you fill in the business logic.

**Guidelines for generating skill logic:**
- Keep the Worker thin — only put server-side logic in it
- If the skill is mostly LLM-based, put the instructions in SKILL.md and only use the Worker for billing
- If the skill needs external API calls or computation, put that in the Worker
- Always include SkillPay billing before any work
- Use TypeScript, target Cloudflare Workers runtime
- Follow the patterns from this project (see existing skills for reference)

### Step 3: Assemble the final skill

Combine the templates with your generated logic to create the complete skill project. The file structure should be:

```
my-cool-skill/
├── SKILL.md
├── wrangler.toml
└── src/
    ├── index.ts      (Worker with billing + your logic)
    └── billing.ts    (BillingResult type)
```

### Step 4: Deploy instructions

Tell the user to run:
```bash
cd my-cool-skill
npx wrangler secret put SKILLPAY_API_KEY
npx wrangler deploy
clawhub publish . --slug my-cool-skill --name "My Cool Skill" --version 1.0.0 --tags latest
```

## Pricing
$0.02 USDT per call via SkillPay.me
