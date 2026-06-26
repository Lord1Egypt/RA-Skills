# Landing Page Review Rubric

> Fixed scoring rubric for consistent, comparable landing page reviews.
> Load with `read_file("references/review-rubric.md")` during Review mode.

---

## Scoring Categories

Seven categories, each scored 1-5. Every category includes automatic-fail conditions that cap the score at 1.

---

### 1. Clarity

**What it measures**: Can a visitor understand what this product does, who it's for, and why it matters within 5 seconds?

| Score | Criteria |
|-------|----------|
| **5** | Headline names a specific outcome for a specific audience. Subheadline adds detail. Value prop is unmistakable above the fold. |
| **4** | Headline is clear and benefit-led but slightly generic on audience. Subheadline compensates. |
| **3** | Headline is understandable but requires reading the subheadline to grasp the product. Audience is implied, not stated. |
| **2** | Headline is vague or jargon-heavy. Visitor needs to scroll to understand what this is. |
| **1** | Headline is generic, clever-but-unclear, or missing. No clear value proposition above the fold. |

**Automatic fail (cap at 1)**:
- Headline is generic ("Welcome to our platform", "The future of X")
- No subheadline present
- Value proposition is absent above the fold

---

### 2. Offer

**What it measures**: Is the offer clear, specific, and compelling? Does the visitor know exactly what they get and at what cost/commitment?

| Score | Criteria |
|-------|----------|
| **5** | Pricing is transparent, what-you-get is specific, risk reversal is present (guarantee, free trial, etc.), CTA matches the offer. |
| **4** | Offer is clear. Minor gap: risk reversal is weak, or pricing has minor ambiguity. |
| **3** | Offer is understandable but vague on details. "Contact us for pricing" without a reason why. |
| **2** | Offer is confusing or buried. CTA doesn't match the offer (e.g., "Buy now" but no pricing shown). |
| **1** | No clear offer. Visitor cannot determine what they'd receive by taking action. |

**Automatic fail (cap at 1)**:
- No CTA present on the page
- CTA text says "Submit" or "Click here"
- No risk reversal on a paid product (no guarantee, no trial, no refund mention)

---

### 3. Proof

**What it measures**: Is there credible evidence that this product works, that real people use it, or that the creator is qualified?

| Score | Criteria |
|-------|----------|
| **5** | Specific outcome-based testimonials with names/roles, real metrics ("saved 40 hours/month"), multiple proof types (testimonials + user count + logos). |
| **4** | Named testimonials with specific praise, or strong founder credibility section. At least 2 proof types. |
| **3** | Generic but real testimonials ("Great product!"), or user count without specifics, or logos without context. |
| **2** | Minimal proof — a single vague testimonial or "trusted by" without numbers. |
| **1** | No social proof at all, or proof that appears fabricated. |

**Automatic fail (cap at 1)**:
- Fabricated testimonials (stock photos, generic names like "John D.", clearly made-up quotes)
- Generic praise without any attribution ("Users love it!")

**Note on Tier 3 (Preview/Waitlist) pages**: Score of 3 is the maximum if page correctly omits proof (appropriate for pre-launch). Do not penalize a waitlist page for lacking testimonials.

---

### 4. Friction

**What it measures**: How easy is it for a motivated visitor to take action? Are there unnecessary barriers?

| Score | Criteria |
|-------|----------|
| **5** | Single-field form (or 2 fields max), CTA is immediately actionable, trust signals near the form, minimal steps to convert. |
| **4** | Form has 3 fields, CTA is clear, minor friction (e.g., no trust signal near form). |
| **3** | Form has 4-5 fields, or CTA requires scrolling to find, or competing CTAs create confusion. |
| **2** | Form has 6+ fields, CTA is ambiguous, or conversion requires multiple pages/steps. |
| **1** | Conversion path is broken, unclear, or excessively complex. |

**Automatic fail (cap at 1)**:
- Form has more than 5 fields for initial conversion
- Multiple competing primary CTAs (e.g., "Buy now", "Start trial", and "Book demo" all presented as primary)
- No trust signals on a payment page (no SSL indicator, no security badges, no guarantee)

---

### 5. Mobile Hierarchy

**What it measures**: Does the page work well on mobile devices? Is the layout, typography, and CTA placement optimized for small screens?

| Score | Criteria |
|-------|----------|
| **5** | CTA visible without scrolling on mobile, single-column stacking, 16px+ body text, thumb-zone CTA placement, full-width buttons. |
| **4** | Layout is responsive and usable. Minor issue: CTA requires one scroll, or touch targets are slightly small. |
| **3** | Page is responsive but not optimized. Text is readable but layout wastes space. CTA is below the fold on mobile. |
| **2** | Layout partially breaks on mobile. Text is too small in places. Horizontal scrolling on some elements. |
| **1** | Page is not mobile-responsive, or major layout issues make it unusable on mobile. |

**Automatic fail (cap at 1)**:
- CTA not visible without scrolling on mobile viewport (375px width)
- Body text below 16px on mobile
- Horizontal scrolling on mobile

---

### 6. Accessibility

**What it measures**: Does the page follow web accessibility standards? Can it be used by people with disabilities?

| Score | Criteria |
|-------|----------|
| **5** | Semantic HTML throughout (`<main>`, `<section>`, `<nav>`, `<footer>`), heading hierarchy is correct (h1→h2→h3, no skips), contrast ≥ 4.5:1, skip-nav link, keyboard-navigable CTAs, alt text on all images. |
| **4** | Semantic HTML, correct heading hierarchy, good contrast. Missing one minor element (e.g., no skip-nav, or one image without alt). |
| **3** | Basic semantic HTML but missing some elements. Heading hierarchy has a minor skip. Contrast is mostly adequate. |
| **2** | Minimal semantic HTML. Multiple heading skips. Some contrast issues. No skip-nav. |
| **1** | Non-semantic HTML (div soup). No heading hierarchy. Contrast failures. Keyboard navigation broken. |

**Automatic fail (cap at 1)**:
- No `<main>` element
- Heading levels skipped (e.g., h1 → h3, missing h2)
- Color contrast below 4.5:1 on body text or CTA buttons

---

### 7. SEO / Social

**What it measures**: Is the page discoverable by search engines and shareable on social media?

| Score | Criteria |
|-------|----------|
| **5** | Unique `<title>` (50-60 chars), meta description (150-160 chars), og:title, og:description, og:image, twitter:card, canonical URL. |
| **4** | Title, meta description, and OG tags present. Missing one element (e.g., no og:image or no twitter:card). |
| **3** | Title and meta description present but OG tags missing or incomplete. |
| **2** | Title present but generic or too long. Meta description missing. No OG tags. |
| **1** | Missing `<title>` or it contains placeholder text. No meta description. No OG tags. |

**Automatic fail (cap at 1)**:
- Missing `<title>` tag or title contains placeholder (e.g., `{{meta_title}}`)
- Missing `<meta name="description">`
- Missing `og:title` tag

---

## Overall Scoring

### Calculation

Sum of all 7 category scores: minimum 7, maximum 35.

### Grade Bands

| Score | Grade | Interpretation |
|-------|-------|----------------|
| **28-35** | Ship-ready | Page is ready to publish. Minor tweaks optional. |
| **21-27** | Needs polish | Solid foundation, but 2-3 areas need improvement before publishing. |
| **14-20** | Significant gaps | Multiple areas need rework. Iterate before publishing. |
| **7-13** | Rebuild recommended | Fundamental issues across most categories. Consider starting fresh. |

---

## Output Format

Present the review as a structured table:

```
LANDING PAGE REVIEW
====================

| Category          | Score | Notes                                    | Fail Conditions     |
|-------------------|-------|------------------------------------------|----------------------|
| Clarity           | 4/5   | Headline is clear, audience implied      | None                 |
| Offer             | 3/5   | Pricing unclear, risk reversal weak      | None                 |
| Proof             | 2/5   | Single generic testimonial               | None                 |
| Friction          | 5/5   | Single email field, clear CTA            | None                 |
| Mobile Hierarchy  | 4/5   | CTA requires one scroll on mobile        | None                 |
| Accessibility     | 3/5   | Missing skip-nav, one heading skip       | None                 |
| SEO/Social        | 4/5   | Missing og:image                         | None                 |

OVERALL: 25/35 — Needs polish

TOP 3 IMPROVEMENTS:
1. [Priority: High] Add specific testimonials or founder credibility section (Proof: 2→4)
2. [Priority: High] Add risk reversal — guarantee or free trial mention (Offer: 3→4)
3. [Priority: Medium] Add skip-nav link and fix heading hierarchy (Accessibility: 3→5)

EVIDENCE TIER: Tier 2 (Mechanism Proof) — founder credibility present, no customer results yet
```

---

*Reference for opc-landing-page-manager.*
