---
name: gumroad-launcher
description: Research a digital product niche, generate the product (ebook, template, script, checklist, or skill), write high-converting Gumroad sales copy, and publish the product listing. Use when asked to "launch a product on Gumroad", "create a digital product", "publish to Gumroad", "make something to sell", or "create a passive income product". Handles the full pipeline from niche research to live listing.
---

# Gumroad Launcher

Full pipeline: niche research → product creation → copy → publish.

## Step 1: Niche Research

Use `web_search` to validate the product idea:
- Search: `"[topic] template gumroad"` — check how many exist and what they sell for
- Search: `"[topic] cheatsheet filetype:pdf"` — gauge free competition
- Search: `site:gumroad.com "[topic]"` — see real listings and prices

**Green lights:** < 20 competitors, clear pain point, people pay $9–$49 for similar things.

## Step 2: Create the Product

Based on product type:

**Skill (.skill file):** Build using skill-creator workflow. Package with `package_skill.py`.

**Markdown ebook/guide:** Write directly, save as `product/[slug].md`. Convert to PDF if needed.

**HTML template:** Build the file(s), zip into `product/[slug].zip`.

**Checklist/cheatsheet:** Create as a clean single-page HTML or Markdown file.

**Prompt pack:** Write 10–25 tested prompts, save as `product/[slug].md`.

Save everything to: `~/workspace/products/[slug]/`

## Step 3: Write Sales Copy

Use this structure for the Gumroad description:

```
**[HEADLINE — outcome-focused, under 10 words]**

[1-2 sentence hook — the pain this solves]

**What you get:**
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

**Who this is for:**
[2-3 sentences describing the ideal buyer]

**Why it works:**
[1 paragraph — the mechanism / why this approach is different]

**[Price justification — what they'd pay otherwise or time saved]**

[CTA: "Get instant access →"]
```

See references/copy-examples.md for real examples.

## Step 4: Set Pricing

| Product Type | Suggested Price |
|---|---|
| Single skill / template | $9–$19 |
| Workflow / system | $19–$29 |
| Bundle (3–5 items) | $37–$57 |
| Course / deep guide | $49–$97 |

Default: price at $19 for first launch, raise after 10 sales.

## Step 5: Publish to Gumroad

Use `web_fetch` or `exec` to interact with Gumroad API.

**Gumroad credentials:** dawn@marathondm.com account (Dawn's store — do NOT use for MJW products)
**MJW Gumroad:** Use MJ's account for all MJW Design Studio products.

Gumroad API base: `https://api.gumroad.com/v2`

Create product:
```powershell
$body = @{
  name = "[Product Name]"
  description = "[Sales copy from Step 3]"
  price = 1900  # in cents
  url = "https://mjwdesignstudio.com"
} | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.gumroad.com/v2/products" -Method POST -Body $body -Headers @{ Authorization = "Bearer [ACCESS_TOKEN]" }
```

After creating, upload the product file via the Gumroad dashboard or API.

## Output

Always report:
- ✅ Product file location
- ✅ Gumroad listing URL
- ✅ Suggested price
- ✅ Sales copy (full text, ready to paste)
