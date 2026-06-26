---
name: idle-web-developer
description: Make 100s of websites while you're idle. Builds, deploys lovable,v0, quality websites with built-in analytics to help you iterate toward breakout winner and hit product market fit. Note for best experience use with HEARTBEAT.md
version: 1.0.2
homepage: https://github.com/jaswirraghoe/idle-web-developer
metadata: {"openclaw":{"emoji":"🚀","requires":{"env":["VERCEL_TOKEN"],"bins":["vercel","npm"]},"primaryEnv":"VERCEL_TOKEN","files":["scripts/*"],"os":["darwin","linux"]}}
---

# Website Builder

Autonomously build and ship a polished web app.
The idea and design are determined automatically using a **dice-based system**.

---

# Workflow

## 0. First-Time Setup (Onboarding Wizard)

Before doing anything else, check whether the skill has been configured.

**Config file location:**
```
~/.openclaw/workspace/skills/idle-web-developer/.skill-config
```

If `.skill-config` **does not exist** (or the user explicitly asks to re-run setup with `--setup`), run the **interactive onboarding wizard** below.

---

### Onboarding Wizard

Ask the user each question in order. Collect the answers, then write them all to `.skill-config` at the end. Present each question clearly — one at a time, conversationally.

---

#### Step A — Vercel Token (required)

> "To deploy your sites, I need your Vercel token.  
> You can find it at: https://vercel.com/account/tokens  
> What is your Vercel token?"

Save as `VERCEL_TOKEN`.

---

#### Step B — Google Analytics (optional)

> "Would you like to enable Google Analytics on your sites? This is optional — it lets you track page views and user behaviour.  
> (yes / no)"

- If **no** → skip to Step C. Leave `GA_MEASUREMENT_ID` and `GOOGLE_APPLICATION_CREDENTIALS` blank.
- If **yes** → ask:

> "What is your Google Application Credentials JSON file path?  
> (e.g. /home/you/.config/gcloud/service-account.json)"

Save as `GOOGLE_APPLICATION_CREDENTIALS`.

> "What is your GA4 Measurement ID?  
> (e.g. G-XXXXXXXXXX — found in Google Analytics → Admin → Data Streams)"

Save as `GA_MEASUREMENT_ID`.

---

#### Step C — Supabase Waitlist (optional)

> "Every site includes a 'Join the Waitlist' section so visitors can sign up.  
> Would you like to connect this to Supabase so emails are actually saved? This is optional — the section always appears, but without credentials submissions won't be stored.  
> (yes / no)"

- If **no** → skip. Leave `SUPABASE_URL` and `SUPABASE_ANON_KEY` blank. The waitlist UI will still be included on every site.
- If **yes** → ask:

> "What is your Supabase project URL?  
> (e.g. https://abcdefgh.supabase.co)"

Save as `SUPABASE_URL`.

> "What is your Supabase anon/public key?  
> (found in Supabase → Project Settings → API → Project API Keys)"

Save as `SUPABASE_ANON_KEY`.

---

#### Saving the Config

After collecting all answers, write the config file:

```bash
CONFIG="~/.openclaw/workspace/skills/idle-web-developer/.skill-config"

cat > "$CONFIG" <<EOF
VERCEL_TOKEN="${VERCEL_TOKEN}"
GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"
GA_MEASUREMENT_ID="${GA_MEASUREMENT_ID}"
SUPABASE_URL="${SUPABASE_URL}"
SUPABASE_ANON_KEY="${SUPABASE_ANON_KEY}"
EOF
```

Confirm to the user:

> "✅ Setup complete! Your config has been saved.  
> You can re-run setup anytime by saying 'set up the website builder' or passing `--setup` to the script."

Then proceed with the rest of the workflow.

---

### If `.skill-config` already exists

Load it and continue. No questions needed.

```bash
source ~/.openclaw/workspace/skills/idle-web-developer/.skill-config
```

---

## 1. Check for Vercel Token

Verify that deployment is possible.

- Confirm `$VERCEL_TOKEN` is set (from config or environment).
- If not available: stop and inform the user to run setup.

Never deploy without authentication.

---

## 2. 🎲 Roll 1 — What to Build

Generate a number from **1–5**:

```bash
python3 -c "import random; print(random.randint(1,5))"
```

| Roll | What to build |
|-----|---------------|
| 1, 2 | 🤖 **AI Tool** |
| 3 | 🏗️ **OpenClaw Web Tool** |
| 4, 5 | 💰 **Niche Clone** |

---

### If Roll = 1 or 2 → AI Tool

Research current AI opportunities.

Search:

```
web_search "trending AI tools 2026"
```

Find something **original and useful** that can realistically be built as a web app.

Examples:
- AI workflow generators
- AI niche productivity tools
- AI dev utilities
- AI writing or research helpers

The result must be **practical and usable**, not just a landing page.

---

### If Roll = 3 → OpenClaw Tool

Research inspiration from the OpenClaw project.

Run:

```
gh issue list -R openclaw/openclaw --limit 20
```

Then build something that **extends or promotes the OpenClaw ecosystem**, such as:

- Interactive docs
- Prompt playground
- Demo tool
- Developer utility
- Visual onboarding experience

The result should help **developers understand or use OpenClaw faster**.

---

### If Roll = 4 or 5 → Niche Clone

**Do not use a predefined list.** Research what's actually making money right now.

Run multiple searches across these sources:

```
web_search "most profitable micro SaaS 2025 site:starterstory.com"
web_search "bootstrapped SaaS revenue 2025 site:starterstory.com"
web_search "fastest growing AI SaaS startups 2025 site:crunchbase.com"
web_search "profitable niche SaaS ideas 2025"
```

Look for:
- **StarterStory.com** — real founders sharing actual MRR, growth, and what's working
- **Crunchbase** — recently funded startups (seed/Series A) in AI/SaaS — funding = validated demand
- **Indie Hackers** — $10k–$100k MRR solo/small-team products
- **Product Hunt** — trending tools with strong upvote momentum

**Selection criteria:**
1. The product has **demonstrated revenue or traction** (not just hype)
2. A clear **underserved niche** exists (industry, role, geography, workflow)
3. The niche version can be **meaningfully differentiated** — not just a rebrand

**Then:**

1. Pick the most promising product with clear revenue signal
2. Identify a **specific underserved niche** — be precise:
   - ❌ "small businesses"
   - ✅ "independent veterinary clinics"
3. Build a **focused version targeting that niche exactly**

The **niche is the moat** — the narrower, the better.

**Example:**

Research finds → Otter.ai ($50M ARR, meeting transcription)

Instead of:
> AI meeting transcription

Build:
> AI meeting transcription **for real estate showings** — auto-generates buyer feedback summaries and follow-up emails for agents

---

## 3. 🎲 Roll 2 — Color Palette

Roll **two more times**.

### Primary Color

```bash
python3 -c "import random; print(random.randint(1,6))"
```

| Roll | Color | Hex | Vibe |
|-----|------|------|------|
| 1 | Electric Blue | #2563EB | Trustworthy, tech, precise |
| 2 | Deep Violet | #7C3AED | Creative, premium, mysterious |
| 3 | Emerald | #059669 | Growth, calm, fresh |
| 4 | Crimson Red | #DC2626 | Bold, urgent, powerful |
| 5 | Amber | #D97706 | Confident, warm, energetic |
| 6 | Cyan / Teal | #0891B2 | Clean, modern, sharp |

---

### Background Mode

```bash
python3 -c "import random; print(random.randint(1,6))"
```

| Roll | Mode | Style |
|-----|------|-------|
| 1, 2, 3 | ☀️ Light | White or `#FAFAFA` base, dark text |
| 4, 5, 6 | 🌙 Dark | `#070B14` or deep neutral base, light text |

Pair the primary with **1–2 derived accent colors** and a neutral set.
The palette should feel **curated and intentional** — never generic.

---

## 4. 🔨 Building Web Apps

Before building, check previous builds:

```
memory/side-hustle-builds.md
```

Do **not duplicate existing ideas**.

---

### Stack
- **React + TypeScript + Vite**
- **Tailwind CSS** (via npm)
- **Framer Motion** for animations
- **lucide-react** for icons
- **Pexels** for stock photos (link only, never download)

---

### Design Standards (non-negotiable)

- Full-viewport animated **Hero** — bold headline, subheadline, primary CTA
- Fixed **Nav** with smooth scroll and CTA button
- **Features / How It Works** with icons or a 3-step flow
- **Social Proof** — testimonials, logos, or user counts
- **Waitlist Signup Section** — **ALWAYS included, no exceptions** (see below)
- **CTA section** mid-page + bottom — urgent, outcome-focused copy
- **Footer** — links, legal, socials
- Optional: **Demo section** (interactive product simulation), **Pricing**, **FAQ**
- Apple/Stripe level polish — every page a bespoke masterpiece
- 8px grid, fluid responsive, mobile-first
- Scroll-triggered animations, hover states, microinteractions
- Benefit-driven copy — outcomes not features

---

### ✉️ Waitlist Signup Section (Required — Always)

**Every single site must include a waitlist signup section.** This is non-negotiable, regardless of whether Supabase credentials are configured.

The section should be visually prominent — a full-width band, typically placed between the main CTA and the footer. It should:

- Have a compelling headline (e.g. "Be the first to know", "Get early access", "Join the waitlist")
- Have a subheadline matching the product's value proposition
- Have an email input + submit button
- Show a success state after submission

**Placement:** Between the mid-page CTA and the Footer (or at the bottom of the hero if the page is short).

**Component file:** `src/components/Waitlist.tsx`

---

### Project Structure

```
apps/<app-name>/
  package.json
  vite.config.ts
  tailwind.config.ts
  tsconfig.json
  index.html
  src/
    main.tsx
    App.tsx
    components/
      Nav.tsx
      Hero.tsx
      Features.tsx
      Waitlist.tsx       ← always present
      Testimonials.tsx
      CTA.tsx
      Footer.tsx
      (+ Demo.tsx, Pricing.tsx, FAQ.tsx as needed)
```

---

#### Wiring: With Supabase Credentials

If `$SUPABASE_URL` and `$SUPABASE_ANON_KEY` are set, the form should POST to Supabase.

Assume the table is named `waitlist` with columns `email`, `app_name`, and `app_url`. The agent should note in the output that the user may need to create this table in Supabase if it doesn't exist.

SQL to create the table:
```sql
create table if not exists waitlist (
  id uuid default gen_random_uuid() primary key,
  email text not null unique,
  app_name text not null,
  app_url text,
  created_at timestamptz default now()
);
```

The fetch call in the component — **always include `app_name` and `app_url`**:
```typescript
const res = await fetch(`${SUPABASE_URL}/rest/v1/waitlist`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
    'Prefer': 'return=minimal',
  },
  body: JSON.stringify({ email, app_name: APP_NAME, app_url: window.location.origin }),
});
```

`APP_NAME` should be a constant at the top of the Waitlist component, set to the product name (e.g. `const APP_NAME = 'ErrorLens'`).

Inject the values at build time via Vite env vars — never hardcode in source:

In `vite.config.ts`, expose:
```typescript
define: {
  __SUPABASE_URL__: JSON.stringify(process.env.SUPABASE_URL ?? ''),
  __SUPABASE_ANON_KEY__: JSON.stringify(process.env.SUPABASE_ANON_KEY ?? ''),
}
```

Use `__SUPABASE_URL__` and `__SUPABASE_ANON_KEY__` in the component.

---

#### Wiring: Without Supabase Credentials

If credentials are absent, still include the full waitlist UI. The form should render and look identical, but on submit show:

> "✅ Thanks! We'll be in touch soon."

(The submission does nothing server-side — it's a polished placeholder.)

Log a note in build output:
```
⚠️  Waitlist is UI-only — set SUPABASE_URL and SUPABASE_ANON_KEY to enable real sign-ups
```

---

### Analytics (Optional)

Check for both conditions **before** adding any analytics code:

1. `$GA_MEASUREMENT_ID` is set
2. `$GOOGLE_APPLICATION_CREDENTIALS` is set or the file exists

**If either is missing → skip analytics entirely. Do not add any tracking code.**

Only when both are present, add the following to `index.html` before `</body>`, replacing `<MEASUREMENT_ID>` with the actual value:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=<MEASUREMENT_ID>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '<MEASUREMENT_ID>', { page_title: document.title, page_location: location.href });
  gtag('event', 'page_view', { product_id: location.hostname });
</script>
```

Check at build time:

```bash
if [ -n "$GA_MEASUREMENT_ID" ] && ([ -n "$GOOGLE_APPLICATION_CREDENTIALS" ] || [ -f "$HOME/.openclaw/workspace/secrets/ga-service-account.json" ]); then
  echo "✅ Analytics enabled — Measurement ID: $GA_MEASUREMENT_ID"
else
  echo "⚠️  Analytics skipped — set GA_MEASUREMENT_ID and GOOGLE_APPLICATION_CREDENTIALS to enable"
fi
```

---

## 5. Deploy

**Important:** Deploy the pre-built `dist/` folder, NOT the project root. Vercel rebuilds from source on their servers where your env vars don't exist — Supabase credentials and analytics would be baked in as empty strings. Deploying `dist/` sends the already-built static files with credentials properly baked in.

```bash
cd apps/<app-name>

# Load credentials from config
source ~/.openclaw/workspace/skills/idle-web-developer/.skill-config

# Export for Vite build (bakes values into the JS bundle locally)
export SUPABASE_URL SUPABASE_ANON_KEY GA_MEASUREMENT_ID GOOGLE_APPLICATION_CREDENTIALS

npm install
npm run build

# Tell Vercel: skip server-side build, serve static files as-is
cat > dist/vercel.json <<'EOF'
{ "buildCommand": "", "outputDirectory": "." }
EOF

# Deploy the LOCAL build output — NOT the source
vercel deploy dist/ --prod --yes --token "$VERCEL_TOKEN"
```

**Why this works:** `npm run build` runs locally where env vars are set, so Vite's `define` bakes Supabase/GA values into the JS bundle. The `vercel.json` in `dist/` tells Vercel to skip rebuilding and serve the files directly.

---

## 6. After Every Build

- Add to `memory/side-hustle-builds.md` (name, URL or path, idea, date)
- Log in `memory/YYYY-MM-DD.md`
- Update `lastBuild` in `memory/heartbeat-state.json`

---

## 7. After Deployment Return

- **Deployed URL**
- **Dice roll results**
- **The generated idea**
- **How the product works**
- **Why it could succeed**
- **Color palette used**
- **Analytics:** enabled or skipped (state which env var was missing if skipped)
- **Waitlist:** confirm the section is included; state whether Supabase is wired or placeholder mode. If wired, remind the user to create the `waitlist` table in Supabase if not already done. The table must include `app_name text not null` and `app_url text` columns.

---

## Commands

```bash
# Normal build + deploy
bash skills/idle-web-developer/scripts/build-and-deploy.sh --name "my-auto-saas"

# Re-run onboarding setup
bash skills/idle-web-developer/scripts/build-and-deploy.sh --setup

# Skip deploy (scaffold only)
bash skills/idle-web-developer/scripts/build-and-deploy.sh --name "my-site" --skip-deploy
```

---

## Notes

- **Onboarding runs once** — after setup, the config is reused automatically.
- **Re-setup:** say "set up the website builder" or pass `--setup` to the script.
- **Waitlist section is mandatory** on every site — no exceptions.
- Never hardcode secrets or tokens into source files.
- Never embed the Supabase anon key directly in JSX — always use Vite define injection.
- Prefer polished dark UI defaults unless user asks otherwise.
- For larger projects, scaffold first, then iterate in follow-up turns.

See `references/workflow.md` for detailed operational guidance.
