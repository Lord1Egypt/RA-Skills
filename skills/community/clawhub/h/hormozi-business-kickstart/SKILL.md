---
name: hormozi-business-kickstart
description: "Generate comprehensive 28-page A4 landscape business kickstart manuals based on Alex Hormozi's $100M trilogy ($100M Offers, $100M Leads, $100M Money Models). Produces a complete strategy document with Grand Slam Offer, 36 problems→solutions matrix, 3 guarantees, 4-stage Money Model, lead generation plan, 30/60/90 execution roadmap, and equipment/marketing budget. Outputs PDF, DOCX, and Markdown. Triggers: business kickstart manual, hormozi business plan, $100M business plan, build kickstart manual, grand slam offer, money model, lead generation plan, business strategy based on hormozi, full business strategy."
metadata:
  builtin_skill_version: "1.5.6"
  openclaw_native: true
  triggers:
    - "generate a business kickstart manual"
    - "business kickstart"
    - "hormozi business plan"
    - "create a $100M business plan"
    - "build a kickstart manual"
    - "I need a business strategy based on Hormozi"
    - "make me a Grand Slam Offer"
    - "build me a lead generation plan"
    - "help me get more customers"
    - "I need more leads"
    - "build me a money model"
    - "stack my offers"
    - "I need a full business strategy"
---

# Business Kickstart Manual Generator Skill ($100M TRILOGY)

## Activation

Trigger this skill when the user says any of:
- "Generate a business kickstart manual"
- "Business kickstart"
- "Hormozi business plan"
- "Create a $100M business plan"
- "Build a kickstart manual for [business]"
- "I need a business strategy based on Hormozi"
- "Make me a Grand Slam Offer for [business]"
- "Build a lead generation plan for [business]"
- "Help me get more customers"
- "I need more leads"
- "Build me a money model"
- "Stack my offers for me"
- "I need a full business strategy"

## Companion Files
- `SKILL_PROMPT.md` — load this ENTIRE file as the system prompt when activating the skill
- `QUESTIONNAIRE.md` — ask these questions to the user BEFORE generating the manual
- `scripts/md_to_pdf.py` — generic Markdown→PDF converter with full CLI (page size, colors, branding, TOC)
- `scripts/md_to_docx.py` — generic Markdown→DOCX converter with full CLI (page size, colors, branding, TOC)

## Output Formats

The skill produces manuals in 3 formats (ask the user which they want; default to PDF).

### Default design (locked in from user feedback)
- **A4 landscape** is the default page size for BOTH PDF and DOCX
- **All text is centered**: H1, H2, H3, H4 headings, body paragraphs, list items, table cells, blockquotes
- **Color theme**: primary navy `#1A3A52` (H1/H2/H4 + table headers), accent orange `#D35400` (H3 + blockquotes + bullets)
- **Table style**: navy header row with white bold text, alternating row backgrounds, all cells centered
- No title page, no auto-TOC (intentional — the user prefers clean content with header/footer only)

### 1. PDF — `scripts/md_to_pdf.py`
- Built with **reportlab + NotoSans** (supports Cyrillic + Latin + most scripts)
- A4 landscape by default, supports A2/A3, landscape or portrait
- All headings + body + lists + table cells centered
- Primary + accent colors configurable via hex codes
- Header (business + location) and footer (title + page numbers) on every page
- Markdown features: headings, tables, bold, italic, code, lists, blockquotes, code fences

**Usage:**
```bash
python3 scripts/md_to_pdf.py <input.md> <output.pdf> [options]

Options:
  --title "TITLE"          Document title (defaults to first H1)
  --author "NAME"          Author name
  --business "NAME"        Business name (shown in header)
  --tagline "TEXT"         Tagline (shown in subtitle)
  --location "PLACE"       Location (shown in header)
  --primary "#1A3A52"      Primary color hex (default navy)
  --accent "#D35400"       Accent color hex (default orange)
  --size a4|a3|a2          Page size (default a4)
  --portrait               Portrait orientation (default landscape)
  --no-header              Skip the page header
  --no-footer              Skip the page footer
```

**Example:**
```bash
python3 scripts/md_to_pdf.py manual.md manual.pdf \
  --business "Ponovo Novo" \
  --location "Šremčica, Belgrade" \
  --primary "#1A3A52" --accent "#D35400"
```

### 2. DOCX / Word — `scripts/md_to_docx.py`
- Built with **python-docx** (industry-standard .docx library)
- A4 landscape by default, supports A2/A3, landscape or portrait
- All headings + body + lists + table cells centered
- Section borders under H1 (12pt) and H2 (6pt) headings for visual structure
- H1=22pt navy, H2=16pt navy, H3=13pt accent orange, H4=11pt navy
- Table headers 9pt bold white on navy; cells 9pt centered
- Same color scheme + header/footer configuration as PDF
- Word fields for live page numbers in footer (Serbian "Stranica X")
- Fully editable in Word, Pages, LibreOffice, Google Docs

**Usage:** identical CLI to `md_to_pdf.py` — see above (the `--tagline` option is DOCX-specific and shows in the header center).

**Example:**
```bash
python3 scripts/md_to_docx.py manual.md manual.docx \
  --business "Ponovo Novo" \
  --tagline "Auto Servis · Šremčica" \
  --location "Belgrade, Srbija" \
  --primary "#1A3A52" --accent "#D35400"
```

### 3. Both
Run both scripts, deliver both files (PDF for reading/sharing, DOCX for editing).

### Requirements
- Python 3.8+
- `pip install python-docx reportlab`
- NotoSans fonts at `/tmp/NotoSans-Regular.ttf` and `/tmp/NotoSans-Bold.ttf` (for PDF Cyrillic support); falls back to Helvetica if missing.

### Known Issues & Workarounds (locked-in from production)

These are real bugs in python-docx and Word mobile that affect the DOCX output. The scripts already work around them, but if you ever touch the table code, read this first:

1. **`python-docx` `Table.width` setter is broken** — assigning `t.width = Cm(21.36)` does NOT update the underlying `<w:tblW>` element (it stays at `type="auto" w="0"`). **Workaround:** set `<w:tblW>` directly via XML:
   ```python
   tblW = t._tbl.tblPr.find(qn('w:tblW'))
   tblW.set(qn('w:type'), 'dxa')
   tblW.set(qn('w:w'), str(table_w_dxa))
   ```

2. **Word mobile ignores `<w:jc w:val="center"/>` for tables** — even when the XML is correct, Word mobile (iOS/Android) renders the table left-aligned. **Workaround:** use `<w:tblInd>` to physically push the table to the center. Compute the indent as half the leftover content-area space:
   ```python
   available_cm = page_w_cm - left_margin - right_margin
   table_w_cm = available_cm * 0.80
   indent_dxa = int((available_cm - table_w_cm) / 2 * 567)
   tblInd.set(qn('w:type'), 'dxa')
   tblInd.set(qn('w:w'), str(indent_dxa))
   ```
   This is geometrically identical to centering, but enforced by left-margin rather than relying on the `<w:jc>` renderer.

3. **Default cell paragraph keeps LEFT alignment** — `cell.text = ''` doesn't reliably clear the cell's default empty paragraph, which inherits the cell's default LEFT alignment. **Workaround:** explicitly remove all existing paragraphs from the cell BEFORE adding the fresh centered one:
   ```python
   for old_p in list(cell.paragraphs):
       old_p._element.getparent().remove(old_p._element)
   p = cell.add_paragraph()
   p.alignment = WD_ALIGN_PARAGRAPH.CENTER
   ```

**Verification before delivery:** Open the generated `.docx` as a zip, read `word/document.xml`, and check that every table has all three of these:
- `<w:tblW w:type="dxa" w:w="12111"/>` (or proportional — must be explicit dxa, not auto/0)
- `<w:jc w:val="center"/>` (kept as a fallback for Word desktop)
- `<w:tblInd w:type="dxa" w:w="1513"/>` (forces centering on Word mobile)

## Overview

This skill generates comprehensive business kickstart manuals grounded in **Alex Hormozi's complete $100M Trilogy** — combining all three books into a single, integrated lead-to-cash system:

1. **$100M Offers** — Build the Grand Slam Offer
2. **$100M Leads** — Get engaged leads to it
3. **$100M Money Models** — Stack offers so each customer pays 5-10× what the first offer cost

The skill walks the user through a 4-stage process: **Offer → Leads → Money Model → Scale.**

## The Complete Framework

The $100M trilogy is sequential. Skipping a stage breaks the system:

```
$100M Offers (Stage 1) ────────► What you sell
        ↓
$100M Leads  (Stage 2) ────────► Who you sell it to (and how to find them)
        ↓
$100M Money Models (Stage 3) ──► How to maximize revenue per customer
        ↓
Scaling (Stage 4) ─────────────► How to grow without breaking
```

**A business needs all 4 stages.** Most beginners stop at Stage 1 or 2. The complete system is what generates 5-10× returns.

---

## STAGE 1: $100M OFFERS — Build the Grand Slam Offer

### The Value Equation (lens for every decision)

```
            Dream Outcome × Perceived Likelihood of Achievement
Value   =  ─────────────────────────────────────────────────────
                  Time Delay × Perceived Effort & Sacrifice
```

- **MAXIMIZE:** Dream Outcome + Perceived Likelihood
- **MINIMIZE:** Time Delay + Perceived Effort & Sacrifice
- **Hormozi's rule:** "Get the bottom to zero." Beginner marketers push the top. Pros dominate by crushing the bottom.

### The 4-Step Grand Slam Offer Process

1. **Dream Outcome** — Specific, time-bound, emotionally charged transformation. "Sell the vacation, not the plane flight."
2. **List ALL Problems** (aim for 32-64) — categorize by Value Equation driver (Dream Outcome, Likelihood, Time Delay, Effort)
3. **Convert Problems → Solutions** — turn each problem into a "How to..." statement
4. **Pick Delivery Vehicles** ("The How") — Live, Recorded, Done-for-you, Community, Software/Tools, Templates/SOPs, 1:1 Access

The set of delivery vehicles IS the offer.

### Sales-to-Fulfillment Continuum

- Start: over-deliver (high fulfillment, easy sales, low margin) → validate demand
- Optimize: lower fulfillment, systemize, higher margin
- Friction: raise prices, tighten terms, reduce bonuses
- **Mantra:** "Create flow. Monetize flow. Then add friction."

### Pricing

- **Cost-to-price ratio:** 1:100, not 1:3
- **Niche specificity multiplier:** General 1x, Industry 5x, Role 10-25x, Ultra-specific 50-100x
- "Charge as much as humanly possible."

### Enhancement Layers

- **Scarcity (3):** Limited seats, Limited bonuses, Never again
- **Urgency (4):** Cohort rolling, Seasonal rolling, Pricing/bonus, Exploding opportunity
- **Bonuses** — name, stack, time-limit
- **Guarantees** — named, specific, generous
- **Naming** — give the offer its own identity

**Mantras:** "When demand increases, cut supply." "Deadlines drive decisions."

---

## STAGE 2: $100M LEADS — Get Engaged Leads to the Offer

### The Goal: Engaged Leads

Engaged leads are prospects who *show* interest in your stuff (follow, give contact info, reply). Moving them from "cold audience" to "warm audience" through consuming content or a lead magnet.

### Lead Magnets

A complete solution to a narrow problem. When solved, reveals another problem solved by your core offer.

**3 Types:**
1. **Reveal Their Problem** ("diagnosis") — speed test, posture analysis, audit
2. **Samples and Trials** — free trial, single-use, fun-sized sample
3. **One Step of a Multi-Step Process** — free chapter, first template, sample step

**7 Steps to Create a Lead Magnet:**
1. Pick the problem and who to solve it for
2. Figure out how to solve it (which of the 3 types)
3. Figure out how to deliver it (the vehicle)
4. Test what to name it (named lead magnets convert better)
5. Make it easy to consume (low friction)
6. Make it darn good (Grand Slam Offer standard applies to free)
7. Make it easy to tell you they want more (clear next step)

**Doctrine:** "Grand Slam Offers work for free stuff as much or better than paid stuff."

### The Core Four Channels (2x2)

|             | **Warm Audience**      | **Cold Audience**       |
| ----------- | ---------------------- | ----------------------- |
| **1-to-1**  | Warm Outreach          | Cold Outreach           |
| **1-to-many** | Post Free Content    | Run Paid Ads            |

**Always start with Warm Outreach.** Add free content. Layer cold outreach. Run paid ads when ready.

### The Content Unit (Hook → Retain → Reward)

Every piece of content must do all 3:
1. **Hook attention** — beat every alternative
2. **Retain attention** — keep them consuming
3. **Reward attention** — satisfy the reason they consumed

### 5 Topic Categories

1. **Far Past** — important life lessons
2. **Recent Past** — stuff you did, meetings, conversations
3. **Present** — ideas you have right now
4. **Trending** — go where attention is, apply your expertise
5. **Manufactured** — turn ideas into reality (live on $100 for a month)

### 6 Levels of Advertising

Where to start, when to scale, when to hire:
- **Level 1:** Find one method that gets a customer profitably. Do it yourself.
- **Level 2:** Optimize. Max personal capacity.
- **Level 3:** Hire employees/contractors.
- **Level 4:** 25%+ from referrals. Build goodwill.
- **Level 5:** Advertise in more places, more ways.
- **Level 6:** Hire executives.

**Rule:** Don't go to Level 3 before Level 1 is profitable.

### 4 Organic Channels

1. **Customer Referrals** — target 25%+ of customers
2. **Employees** — incentivize with revenue share
3. **Agencies** — outsource what you can't do in-house
4. **Affiliates and Partners** — commission per customer

**Referral Growth Equation:** Referrals (in) − Churn (out) = Net Growth. If positive, you grow without advertising.

---

## STAGE 3: $100M MONEY MODELS — Stack Offers for 5-10× LTV

> "A Money Model is a sequence of offers. At their core, we find every opportunity to solve a customer's problem...and then offer to solve it."

### The 4 Types of Offers

| Type | Purpose | When |
|------|---------|------|
| **Attraction Offers** | Turn strangers into customers | First contact |
| **Upsell Offers** | Get people to spend more cash | Right after attraction |
| **Downsell Offers** | Get people to say yes when they'd have said no | Right after upsell-no |
| **Continuity Offers** | Keep people buying | Recurring |

### Stage I: ATTRACTION OFFERS (5 types)

The free-ish thing that gets a stranger to become a customer. Goal: **cover customer acquisition cost and start the relationship.**

1. **Win Your Money Back** — "If you do X within Y time within Z rules, you get it free." Customers put money down, get it back if they achieve the result.
2. **Giveaways** — Free product/service in exchange for applications, lead info, or referral.
3. **Decoy Offer** — A "lesser" priced tier that makes the main offer look better. Three tiers, middle one is the goal.
4. **Buy X Get Y Free** — High perceived value through bundling. Stack bonuses around the core.
5. **Pay Less Now or Pay More Later** — Discount for paying in full up front, OR premium for ongoing.

**Rule:** Pick one. Make it work. Move on.

### Stage II: UPSELL OFFERS (4 types)

The first thing they buy creates new problems. Upsell offers solve those problems. Goal: **30-day profits well above cost of getting the customer.**

1. **The Classic Upsell** — "Do you want to add X?" Just one obvious add-on. Most people say yes.
2. **Menu Upsell** — "Choose one: A, B, C, D, E?" Each option has different price/value. Move them up the menu.
3. **Anchor Upsell** — "Look at this $5,000 option. Now look at this $2,000 option." (Note: the $5k option is rarely sold but reframes the $2k.)
4. **Rollover Upsell** — "Your 4-week program is almost done. Want to roll over to a 12-week for $X?"

**Rule:** Pick one that solves the natural next problem from your attraction offer. Make it at their time of greatest need.

### Stage III: DOWNSELL OFFERS (3 types)

Get the people who said no to your upsell to say yes to something. Goal: **sell more people from the same number of leads.**

1. **Payment Plan Downsell** — Same product, split the price. Total cash may be lower but conversion is way higher.
2. **Trial With Penalty** — Try it for $X. If you keep it, pay full price + the trial fee. If you return, pay restocking fee. Get the yes.
3. **Feature Downsell** — Less of the product, less of the price. The "good-better-best" pattern.

**Rule:** Alternate between them in the same sale. The more flexible, the more people buy.

### Stage IV: CONTINUITY OFFERS (3 types)

Recurring revenue. Goal: **stack recurring cash so each customer pays 5-10× what the first offer cost.**

1. **Continuity Bonus Offer** — "Get this bonus every month you stay." Adds value over time, makes them stay.
2. **Continuity Discount Offer** — "Get X% off everything you buy from us, forever, for $Y/month." Replaces transactional with subscription.
3. **Waived Fee Offer** — "We'll waive the setup/cancellation/processing fee if you stay." Removes friction.

**Note:** Sometimes the best time for continuity is after the first 30 days. Better to offer at the right time than force it at the wrong time.

### 4-Step "Make Your Money Model" Process

**Step 1) Start with an Attraction Offer.** Goal: turn strangers into customers and cover costs. Pick one. Advertise it. May take a year to find what works.

**Step 2) Pick an Upsell Offer.** Goal: 30-day profits well above cost. Solve the next problem your attraction offer creates. Make the offer at their time of greatest need.

**Step 3) Pick a Downsell Offer.** Goal: convert the upsell-noes into yeses. Change how they pay (Payment Plan) or what they get (Feature). Alternate in the same sale.

**Step 4) Pick a Continuity Offer.** Goal: stack recurring cash. Try Continuity Bonuses, Discounts, or Waived Fee.

**Important:** Perfect one offer at a time. Implement one stage fully before moving to the next. "You either build it right or you build it again."

### 4 Critical Money Model Principles

1. **Perfect One Offer At A Time.** Don't implement the whole Money Model at once. Pick one. Try it. Keep doing it until it works reliably. Then go to the next stage.
2. **Raise Price In Stages.** Make new offers cheap at first. Get yeses, get feedback. Then raise price. Keep raising until you can't make up for the nos with the extra cash.
3. **Simple Scales. Fancy Fails.** It's not about 100 products. It's about 100 ways to offer the same product. (One product → one, two, three, four sessions per week.)
4. **Affiliate Products Can Fill Money Model Gaps.** You can always offer somebody else's stuff in your Money Model — at any stage, any size, any time. No extra operational headache.

### Bootstrapped vs Funded

> "Unless you get outside investors, start with a fortune, or have an endless source of free customers, achieving a Money Model is the only way you can profitably scale."

The Money Model is what makes a bootstrapped business scale profitably. It costs money to get customers; you need to recover that cost plus make profit from the first 30 days. Without a Money Model, you run out of cash and go out of business.

---

## STAGE 4: SCALING — How to Grow Without Breaking

This is integrated into the books as principles:

- **Over-deliver at first**, then optimize, then add friction (Sales-to-Fulfillment)
- **Charge as much as possible** (1:100 ratio)
- **Niche specificity** multiplies pricing power (1x to 100x)
- **Use all 4 organic channels** (Referrals → Employees → Agencies → Affiliates)
- **Don't go to Level 3 advertising before Level 1 is profitable**
- **Make it harder to become a customer** (limit supply when demand rises)

---

## Putting It All Together: The Manual Structure

The complete manual includes:

**Part A: The Offer** (from $100M Offers)
1. Title page with offer name
2. Executive Summary
3. The Value Equation Analysis
4. Dream Outcome
5. Problem List (32-64, categorized)
6. Solutions & Delivery Vehicles
7. The Value Stack
8. The Trim & The Stack
9. The Money Model (sequencing — placeholder filled in Part B)
10. Enhancements: Scarcity, Urgency, Bonuses, Guarantee, Name

**Part B: The Money Model** (from $100M Money Models)
11. **Stage I: Attraction Offer** — pick 1 of 5 types, define mechanics
12. **Stage II: Upsell Offer** — pick 1 of 4 types, define mechanics
13. **Stage III: Downsell Offer** — pick 1 of 3 types, define mechanics
14. **Stage IV: Continuity Offer** — pick 1 of 3 types, define mechanics
15. **The Full Money Model** — sequence diagram, value stack, LTV target
16. **Affiliate Products** — if any gaps to fill

**Part C: The Leads** (from $100M Leads)
17. **Lead Magnet** — 1 of 3 types, named, valuable
18. **The Core Four Channels** — pick 1-2 to start, 1-2 to layer
19. **Content Unit Plan** — 5 topics, 10 pieces of content
20. **Paid Ads Strategy** — only if applicable, 6 Levels framework
21. **Organic Channels Roadmap** — Referrals (25%), Employees, Agencies, Affiliates

**Part D: The Plan**
22. **30/60/90 Implementation Plan** — phased rollout (one stage at a time)
23. **Key Metrics & Targets** — LTV, CAC, take rate, retention
24. **First 3 Actions This Week** — always end here

---

## Key Hormozi Principles to Internalize

From $100M Offers:
- "Make an offer so good people feel stupid saying no"
- "Get the bottom of the Value Equation to zero"
- "When demand increases, cut supply"
- "Deadlines drive decisions"
- "Create flow. Monetize flow. Then add friction."
- "If you don't know who your customer is, you don't have a business — you have a hobby"

From $100M Leads:
- "Quantity has a quality all of its own"
- "Content is just a free good that gets you paid goods"
- "Your best free content = your best paid ads"
- "Don't go to Level 3 before Level 1 is profitable"
- "If referrals > churn, you grow without any other advertising"

From $100M Money Models:
- "A Money Model is a sequence of offers"
- "Get the result, take the actions, get the money back" (Win Your Money Back)
- "More and better free stuff" (the secret to attraction)
- "Perfect one offer at a time"
- "Raise price in stages"
- "Simple scales, fancy fails"
- "Affiliate products can fill Money Model gaps"
- "If you don't have a Money Model, you have a hobby that's bleeding cash"

---

## When NOT to use this skill

- The user has neither an offer nor any customer
- The user is selling a commodity with no differentiation
- The user wants pure execution tactics (this is strategy + system)
- The user wants to remain at the same level — this skill is for scaling
