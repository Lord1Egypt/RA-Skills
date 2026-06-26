# KDP Publishing & Formatting Reference

Complete reference for Amazon KDP and IngramSpark publishing — formatting, metadata, categories, pricing, front/back matter, and upload preparation.

---

## TABLE OF CONTENTS
1. [Manuscript Formatting — Ebook](#ebook-formatting)
2. [Manuscript Formatting — Paperback](#paperback-formatting)
3. [Front Matter](#front-matter)
4. [Back Matter](#back-matter)
5. [KDP Metadata Package](#kdp-metadata-package)
6. [BISAC Categories & Browse Nodes](#bisac-categories--browse-nodes)
7. [Pricing Strategy](#pricing-strategy)
8. [KDP Select vs Wide Distribution](#kdp-select-vs-wide-distribution)
9. [IngramSpark](#ingram-spark)
10. [Cover Requirements](#cover-requirements)
11. [Pre-Upload Checklist](#pre-upload-checklist)
12. [Amazon Author Central](#amazon-author-central)

---

## Ebook Formatting

### File Format
- KDP accepts EPUB, DOCX, or KPF (Kindle Create output)
- EPUB is preferred for control — DOCX works but may introduce formatting artifacts
- If using pandoc: `pandoc manuscript.md -o manuscript.epub --toc --toc-depth=2`

### Formatting Standards
- **Chapter headings**: H1 for chapter titles, H2 for sections within chapters
- **Page breaks**: forced page break before every chapter heading
- **Font embedding**: embed fonts in EPUB to preserve design intent
- **Images**: 72 DPI minimum for ebook, JPG or PNG, max 5MB per image
- **Table of contents**: auto-generated from headings, all links must work
- **No headers/footers**: ebooks don't use page headers or footers
- **No page numbers**: Kindle generates its own location system
- **Hyperlinks**: internal links (TOC, cross-references) and external links (author website, resources) must work

### Common Ebook Mistakes to Avoid
- Hard page numbers left in from print formatting
- Manual line breaks instead of proper paragraph spacing
- Inconsistent heading styles (mixing H1/H2 randomly)
- Images that are too large (slow loading, file size rejection)
- Smart quotes that don't render properly (test on Kindle Previewer)

---

## Paperback Formatting

### Trim Sizes (Common for KDP)
| Genre | Recommended Trim | Notes |
|---|---|---|
| Non-fiction | 6" x 9" | Industry standard, professional feel |
| Fiction | 5.5" x 8.5" | Common for novels |
| Children's | 8.5" x 8.5" or 8" x 10" | Landscape or portrait depending on illustration style |
| Business/Self-help | 6" x 9" | Professional, shelf-compatible |
| Poetry | 5" x 8" | Compact, intimate feel |

### Margins (KDP Minimum Requirements)
For 6" x 9" trim with 200+ pages:
- **Inside margin (gutter)**: 0.75" minimum (increase for thicker books — 0.875" for 400+ pages)
- **Outside margin**: 0.5" minimum
- **Top margin**: 0.5" minimum
- **Bottom margin**: 0.5" minimum

### Bleed
- **No bleed needed** if no images/color touch the page edge
- **With bleed**: add 0.125" on top, bottom, and outside edge. Trim size becomes 6.25" x 9.25"
- Background images and full-page illustrations MUST use bleed

### Spine Width Calculation
Spine width depends on page count and paper type:
- **White paper**: page count x 0.002252"
- **Cream paper**: page count x 0.0025"
- Example: 250-page book on cream paper = 250 x 0.0025 = 0.625" spine

### Paper Color
- **White**: best for books with images, charts, or color content
- **Cream/off-white**: best for text-heavy fiction and non-fiction (easier on eyes, traditional feel)

### Page Numbering
- Front matter: lowercase Roman numerals (i, ii, iii...) or no numbers
- Body: Arabic numerals starting at 1 from Chapter 1
- Right-side (recto) pages are odd numbers
- Chapter opening pages: no page number displayed (standard convention)

---

## Front Matter

Required and optional elements, in order:

### Required
1. **Half-title page**: book title only, no subtitle or author name (recto page)
2. **Title page**: full title, subtitle, author name, optional publisher imprint (recto page)
3. **Copyright page** (verso page — back of title page):
   ```
   Copyright (c) [Year] {{AUTHOR_NAME}}
   All rights reserved.

   No part of this publication may be reproduced, distributed, or transmitted
   in any form or by any means without the prior written permission of the
   publisher, except in the case of brief quotations in reviews and certain
   other noncommercial uses permitted by copyright law.

   [Medical/legal disclaimer if applicable]

   ISBN: [Paperback ISBN]
   ISBN: [Ebook ISBN]

   First edition: [Month Year]

   [Publisher name or "Published by {{AUTHOR_NAME}}"]
   [City, State/Country]

   www.[author-website].com
   ```
4. **Table of contents**: auto-generated, linked in ebook

### Optional (in order, after copyright)
5. **Dedication**: brief, one page
6. **Epigraph**: opening quote, one page
7. **Foreword**: written by someone other than the author
8. **Preface/Introduction**: author's framing, why this book matters

### Medical Disclaimer (Required for Health Books)
```
The information in this book is intended for educational purposes only and
is not a substitute for professional medical advice, diagnosis, or treatment.
Always consult your physician or qualified healthcare provider before making
changes to your medications, diet, exercise routine, or health regimen.

The author and publisher disclaim any liability for adverse effects arising
from the use or application of the information contained herein.
```

---

## Back Matter

Elements in order:

1. **Acknowledgments** (optional)
2. **About the Author**: 150-200 words, third person, credibility + personality
3. **Also By {{AUTHOR_NAME}}**: list of other published titles with links
4. **Resources**: recommended tools, websites, organizations (for non-fiction)
5. **References/Bibliography**: sourced citations (for non-fiction)
6. **Discussion Questions**: for book clubs (optional, strong for non-fiction)
7. **Index** (optional, non-fiction only — rare in indie publishing)
8. **Call to Action**: newsletter signup, website, social media, next book preview

### CTA Best Practices
The last thing a reader sees should invite continued engagement:
- "Want the companion workbook? Visit [URL]"
- "Join [X] readers getting weekly [topic] insights: [newsletter URL]"
- "If this book helped you, a review on Amazon helps other readers find it too."

---

## KDP Metadata Package

For every book, produce a complete metadata document containing:

### Title & Subtitle
- **Title**: keyword-aware but not keyword-stuffed. Must sound like a real book title.
- **Subtitle**: can be more keyword-rich. This is where SEO lives.
- Example: Title: "The Complete Guide to [Topic]" / Subtitle: "A [Professional]'s [Timeframe] Plan to [Benefit 1], [Benefit 2], and [Benefit 3]"

### Book Description (4,000 character max)
Amazon allows basic HTML formatting. Use it:
```html
<b>Your [pain point]. Your [symptom]. Your doctor says "watch it."</b>

This book gives you the plan your 15-minute appointment couldn't.

<b>Inside you'll discover:</b>
<ul>
<li>Why [problem A] and [problem B] are the same conversation</li>
<li>Which [metrics] actually matter (and which are noise)</li>
<li>A [timeframe] plan you can follow without quitting your life</li>
<li>What your [current approach] helps — and what it misses</li>
</ul>

Written by {{AUTHOR_CREDENTIALS}} who has helped thousands of readers...
```

**Rules for book descriptions:**
- First line is the hook — must create emotional recognition or curiosity
- Bullet lists for scanability
- Benefits, not features — "you'll discover" not "this book contains"
- End with credibility statement and/or social proof
- Write to the reader's pain, not the book's contents
- Test against top 5 competitor descriptions in the niche

### 7 Backend Keywords
See `references/keyword-research.md` for full methodology.
- 7 keyword phrases (not single words)
- Each phrase max 50 characters
- No repetition of words already in title/subtitle
- Based on actual Amazon search behavior, not brainstorming

### Author Bio
- Third person, 150 words
- Lead with credibility relevant to the book topic
- Include personality — not just credentials
- End with location or personal detail that humanizes

### DRM Setting
- **Recommendation**: DRM OFF for most indie authors
- DRM does not prevent piracy but does limit legitimate reader flexibility
- Exception: if publisher or institutional requirements mandate DRM

---

## BISAC Categories & Browse Nodes

### How to Choose Categories
1. Search Amazon for your book's main keyword
2. Look at where top-selling comparable titles are categorized
3. Check the competitive density — how many reviews does the #1 book in that subcategory have?
4. **Target subcategories where #1 has fewer than 500 reviews** — your book can rank here
5. Choose one competitive category (where the readers are) and one niche category (where you can rank)

### Browse Node Strategy
- KDP allows 2 categories at upload
- Request up to 8 additional categories via KDP Support after publishing
- Always request additional categories — this is free ranking surface area

### BISAC Code Format
Example: `HEA039150` = Health, Fitness & Dieting > Diseases & Physical Ailments > Diabetes > Type 2
- Always provide the full browse path AND the BISAC code when documenting

### Category Research Process
1. Find 5 comparable titles on Amazon
2. Note their categories (visible on product page under "Product Details")
3. Check BSR in each category — lower BSR = more competitive
4. Choose categories where your book can realistically reach top 10-20

---

## Pricing Strategy

### Ebook Pricing
| Price Point | Best For | KDP Royalty Rate |
|---|---|---|
| $0.99 | Launch promotions, reader magnets, short content | 35% |
| $2.99 | Permanently low — acceptable for short books (<30K words) | 70% |
| $3.99-$4.99 | Non-fiction, genre fiction sweet spot | 70% |
| $5.99-$7.99 | Established authors, premium non-fiction | 70% |
| $8.99-$9.99 | Max 70% royalty tier — expert non-fiction only | 70% |
| $10.00+ | Drops to 35% royalty — rarely justified for indie | 35% |

**The 70% royalty tier requires**: price between $2.99-$9.99, enrolled in KDP Select OR price at least 20% below print price.

### Paperback Pricing
- **Formula**: (printing cost x 2.5) rounded to nearest $0.99
- **Minimum**: printing cost + $0.01 (but never price at minimum — signals low value)
- **Typical ranges**: $12.99-$16.99 for standard non-fiction, $14.99-$19.99 for premium

### Launch Pricing Strategy
1. **Pre-launch**: set ebook at $0.99 for first 5 days (volume + rank momentum)
2. **Week 2**: raise to $2.99 (still accessible, start building royalty base)
3. **Week 3+**: raise to full price ($4.99-$7.99 depending on genre)
4. **Paperback**: full price from day one — no discount on print

### Competitive Pricing Research
Before setting price:
1. Check the top 10 books in your target category
2. Note their ebook and paperback prices
3. Price within the range — never dramatically above without strong brand
4. If your book is shorter than competitors, price slightly below

---

## KDP Select vs Wide Distribution

### KDP Select (Exclusive to Amazon)
**Pros:**
- Kindle Unlimited (KU) page reads — significant revenue for fiction
- Kindle Countdown Deals (scheduled promotions with countdown timer)
- Free Book Promotions (5 days per 90-day enrollment period)
- Higher visibility in Amazon algorithm during promotions

**Cons:**
- Cannot sell ebook ANYWHERE else (Apple Books, Kobo, Barnes & Noble, Google Play)
- 90-day auto-renewing commitment
- Dependent on Amazon's KU page-read payout rate (fluctuates)

**Best for:** Fiction (especially romance, thriller, sci-fi/fantasy), books targeting heavy Kindle readers

### Wide Distribution (Non-Exclusive)
**Pros:**
- Sell on all platforms (Apple, Kobo, B&N, Google Play, libraries via OverDrive)
- Diversified income — not dependent on one platform
- Library distribution (growing market)
- International reach (Kobo strong in Canada, Australia)

**Cons:**
- Loses KU page reads (major revenue stream for fiction)
- No Kindle Countdown Deals
- Harder to build momentum — split across platforms

**Best for:** Non-fiction (readers buy, not borrow), established backlist, authors building long-term platform

### Decision Framework
| Factor | Choose KDP Select | Choose Wide |
|---|---|---|
| Genre is fiction (especially romance/thriller) | Yes | |
| Genre is non-fiction (health, business, self-help) | | Yes |
| First book, need visibility | Yes | |
| Building long-term backlist | | Yes |
| Heavy KU readership in your niche | Yes | |
| Want library distribution | | Yes |

Always document the decision with rationale. This can be changed every 90 days.

---

## IngramSpark

### When to Use IngramSpark
- Wide print distribution (bookstores, libraries, academic)
- Hardcover option (KDP does not offer hardcover in all markets)
- International distribution beyond Amazon
- Returns-eligible status for bookstore shelf placement

### Key Settings
- **Trim size**: match KDP paperback or choose standard bookstore sizes
- **Paper**: 50# white or 70# cream (standard trade)
- **Cover finish**: matte (literary/non-fiction) or gloss (commercial/genre)
- **Wholesale discount**: 55% is standard for bookstore returnability
- **Returns**: "Yes — Returnable" if you want bookstore placement (increases cost risk)
- **Distribution**: "Global Connect" for widest reach

### Spine Width (IngramSpark)
- **Black & white, white paper (50#)**: page count x 0.002252"
- **Black & white, cream paper (70#)**: page count x 0.0025"
- **Color, white paper (70#)**: page count x 0.002347"

### IngramSpark vs KDP Print
| Feature | KDP Print | IngramSpark |
|---|---|---|
| Amazon distribution | Automatic | Requires opt-in |
| Bookstore distribution | Limited | Excellent (with returns) |
| Hardcover | Limited markets | Available globally |
| Setup cost | Free | $49/title (watch for free promo codes) |
| Print quality | Good | Excellent |
| Expanded distribution | Available but limited | Industry standard |

**Recommendation**: Use both. KDP Print for Amazon sales (better royalty). IngramSpark for everywhere else (turn OFF Amazon distribution in IngramSpark to avoid conflict).

---

## Cover Requirements

### KDP Cover Specs
- **Front cover**: trim width + bleed (0.125") on each side
- **Full cover (paperback)**: front + spine + back, single PDF
- **Resolution**: 300 DPI minimum
- **Color space**: CMYK for print, RGB for ebook
- **File format**: PDF (print), JPG or TIFF (ebook)

### Cover Brief (What to Provide a Designer)
When writing a cover brief, include:
1. **Genre and tone**: what visual language does this category use?
2. **3-5 reference covers**: comparable titles with successful covers in the niche
3. **Title, subtitle, author name**: exact text for front cover
4. **Spine text**: title + author name (confirm spine width)
5. **Back cover elements**: description block, author bio, barcode placement, tagline
6. **Color palette guidance**: based on genre conventions and competitive analysis
7. **What to avoid**: specific visual cliches that signal amateur design in this genre

### Common Cover Mistakes
- Font choices that signal amateur (Comic Sans, Papyrus, overly decorative fonts)
- Too much text on the front cover
- Low-contrast text that's unreadable at thumbnail size
- Generic stock photos that look like every other book in the category
- Not testing at Amazon thumbnail size (the most common viewing context)

---

## Pre-Upload Checklist

Before uploading to KDP or IngramSpark:

### Content
- [ ] Full manuscript proofread (no typos, formatting errors, broken links)
- [ ] Front matter complete and correctly ordered
- [ ] Back matter complete with CTA
- [ ] Table of contents links work (ebook)
- [ ] Page numbers correct (print)
- [ ] All [NEEDS VERIFICATION] markers resolved or removed
- [ ] Medical/legal disclaimers included (if applicable)
- [ ] ISBN assigned and included on copyright page

### Metadata
- [ ] Title and subtitle finalized
- [ ] Book description written and HTML-formatted
- [ ] 7 backend keywords researched and documented
- [ ] 2 BISAC categories selected with browse node IDs
- [ ] Author bio written
- [ ] Pricing set (ebook + paperback separately)
- [ ] KDP Select decision documented
- [ ] DRM setting confirmed

### Files
- [ ] Ebook file (EPUB or DOCX) tested in Kindle Previewer
- [ ] Paperback interior PDF with correct margins, bleed, page count
- [ ] Cover file meets spec (resolution, dimensions, color space)
- [ ] Spine width calculated and verified
- [ ] All files named clearly: `[book-slug]-ebook.epub`, `[book-slug]-interior.pdf`, `[book-slug]-cover.pdf`

---

## Amazon Author Central

### Setup Requirements
- Create or claim Author Central profile at author.amazon.com
- Upload professional author photo
- Write "Biography" section (can differ from book bio — more personal)
- Add "From the Author" section on each book's product page
- Link all books under one author profile (critical for discoverability)

### Ongoing Maintenance
- Update bio when new books publish
- Add editorial reviews when available
- Monitor and respond to reader questions (if Amazon Q&A is active)
- Check that all books are properly linked to the author page
- Update "From the Author" sections seasonally or with new releases
