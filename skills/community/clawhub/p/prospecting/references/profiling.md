# Customer Profiling — 8-Step Fixed Process

## Input

| Field | Required | Notes |
|-------|----------|-------|
| Company name | ✅ | Core search term |
| Location (city/state) | ✅ | Search area |
| Product purchased | ❌ | Helps profiling |
| Other info | ❌ | Any detail useful |

Even "name + location" is enough to start.

---

## Step 1: Identify Tier

Before enrichment, determine how deep to search:

| Tier | Criteria | Enrichment depth |
|------|----------|-----------------|
| 🔴 Chain/large | Chain name markers OR >200 reviews | Full: Maps + FB + LinkedIn + Website + News |
| 🟡 Mid-tier | Has website, 50-200 reviews | Medium: Maps + FB + Website |
| 🟢 Small | No website, <50 reviews | Minimal: Maps only |

Tier can be preliminary at this stage and refined after Maps data.

---

## Step 2: Google Maps Deep Dive

**Search**: `[company name] [location]`

**Required fields**:

| Field | Purpose |
|-------|---------|
| Exact address | Distance, similar-area matching |
| Phone | Primary contact |
| Rating | Business quality |
| Review count | Scale/activity indicator |
| Review content (sampled) | Business type, equipment, expansion signals |
| Business type tags | Industry matching |
| Hours | Scale indicator |
| Website link | Tier indicator |
| Photo count | Activity indicator |
| Chain/multi-location | Scale indicator |
| Opening date/years | Stability indicator |

**Review sampling rules** (NOT all reviews):

| Total reviews | Strategy | Sample size |
|---------------|----------|-------------|
| <50 | Read all | All |
| 50-200 | Latest 50 + keyword filter | ~60-70 |
| 200-1000 | Latest 30 + keyword filter | ~40-50 |
| >1000 | Latest 20 + keyword filter | ~30 |

**Keyword filter** — search all reviews for these, read when hit:
- `new / expand / expansion / moved / bigger / grand opening` (expansion)
- Generic equipment keywords: `new, expand, equipment, upgrade, install` — add industry-specific keywords based on the product
  - Auto body example: `paint booth, spray booth, insurance, fleet, dealer`
  - Manufacturing example: `CNC, machining, production line, automation`
  - HVAC example: `HVAC, furnace, ductwork, installation`
- Business type mentioned (industry-specific)
- `insurance / fleet / dealer / commercial` (client composition)
- `recommend / best / love / terrible / worst` (polarity reviews)

**Extract signals**:
- Business type mentioned (industry-specific)
- Equipment/bays mentioned
- Expansion / new service / relocation signals
- Client composition (insurance vs retail vs dealer)

---

## Step 3: Social Media & Website (Tier-gated)

**❌ No undifferentiated social search. Gate by tier.**

| Tier | Strategy | Time limit |
|------|----------|-----------|
| 🔴 Chain | FB + LinkedIn + Website full scan | 5 min |
| 🟡 Mid-tier | FB + Website | 3 min |
| 🟢 Small | **Skip** — not worth finding | 0 min |

**Reason**: Target clients are mostly small businesses with low social media coverage (FB 30-40%, IG/LinkedIn <20%).

**Facebook** (chain/mid-tier only):
- Followers/following count
- Last 3-5 posts (business focus, expansion signals)
- About description
- Email/website (may not be on Maps)

**LinkedIn** (chain only):
- Company size, employee count
- Purchasing decision makers
- Recent activity

---

## Step 4: Website Deep Dive (if has website)

**Search**: Open website from Maps/FB link

**Extract**:

| Page | Data |
|------|------|
| Services | Exact service offerings |
| About | Years, scale, philosophy |
| Team/Staff | Employee count, org structure |
| Equipment | Current equipment types & brands |
| Contact | Email, forms, multi-channel |
| Portfolio/Cases | Client types, capabilities |
| News/Blog | Expansion, awards, milestones |

---

## Step 5: Industry Directory & News Supplement

**Search**: `"[company name]" review/news/rating`

| Source | Data | Priority |
|--------|------|----------|
| Yelp | Ratings, reviews, photos | 🟡 If available |
| BBB | Rating, complaints, years | 🟡 If available |
| Industry news | Expansion, acquisitions, partnerships | 🟢 Nice to have |
| Supply chain info | Vendor relationships | 🟢 Nice to have |

---

## Step 6: Synthesize Profile

Aggregate all collected data into characteristic tags:

| Dimension | Extract | Source priority |
|-----------|---------|----------------|
| Scale | Bays, employees, estimated revenue | Website > Maps reviews > FB |
| Business type | Paint, body, insurance, dealer work | Website > FB > Maps reviews |
| Client mix | Insurance vs retail vs dealer | Maps reviews > Website |
| Geography | Industrial/commercial/suburban | Maps address > Maps reviews |
| Years in business | Opening date | Maps > BBB > Website |
| Equipment | Current equipment, age | Website > Reviews |
| Expansion signals | New location, new service, new equipment | Reviews > FB > News |

---

## Step 7: Determine Product Tier

| Characteristics | Product tier | Search direction |
|----------------|-------------|-----------------|
| Chain/multi-location/large center/>200 reviews | 🔴 High-end | Same brand locations + similar-scale competitors |
| Has website, 3-5 bays, mid revenue | 🟡 Mid-range | Similar-scale independents |
| 1-2 bays, family-run, no website | 🟢 Entry-level | Similar small shops |

**Chain store tier note**: Chain stores (Crash Champions, Caliber Collision, Fix Auto, CARSTAR) are always treated as 🔴 or high-🟡 regardless of individual location size, because:
- One corporate deal can cover multiple locations
- Chain procurement volume justifies premium positioning
- EV/Premium lines (e.g., Crash Champions LUXE, EV Certified) have specialized requirements

**Tier labels include chain distinction**:
- Independent: "中高端-独立", "中端-独立", etc.
- Chain: "连锁-中高端", "连锁-高端", etc.
- This distinction affects opener strategy and follow-up approach

---

## Step 8: Output — Profile Card

Save as `prospect-data/{batch}/profile-{name}.json`:

```json
{
  "company_name": "ABC Auto Body",
  "location": "Orange, CA",
  "tier": "中高端",
  "phone": "(714) 555-0000",
  "address": "123 Main St, Orange, CA 92867",
  "website": "https://abcauto.com",
  "rating": 4.6,
  "reviews_count": 134,
  "business_type": ["auto body", "collision repair"],   // adjust per industry
  "scale": "5 bays, 12 employees",
  "years_in_business": 15,
  "client_mix": "Insurance-heavy (State Farm, Allstate DRP)",
  "equipment": "2 downdraft booths, 1 prep station",   // industry-specific
  "expansion_signals": ["Added paint services 2024", "New signage"],
  "certifications": ["I-CAR Gold", "ASA member"],
  "tags": ["industry keyword", "business type", "certification"],   // e.g., ["auto body", "collision", "I-CAR"]
  "search_keywords": ["auto body shop", "collision repair"],   // derived from profile
  "search_center": "Orange, CA",
  "search_radius_miles": 50,
  "source_notes": "Reviews mention expansion into new services. DRP with multiple insurers."   // industry-specific
}
```

---

## Key Rules

1. Every step must execute — skip only if data source has nothing
2. Review sampling with keyword filtering — never read all reviews for large counts
3. Search by company name, not "industry + location" — ensures data corresponds to correct business
4. Record all information found — don't discard subjectively
5. Output standardized profile card — fixed format for batch comparison and reuse

## Time Estimate

| Step | Time | Notes |
|------|------|-------|
| Maps deep dive | 3-5 min | Core, most complete source |
| FB/Social | 2-3 min | Mid-tier and above only |
| Website | 2-3 min | Only if website exists |
| Directory/News | 1-2 min | If available, skip if not |
| Synthesis | 2-3 min | Aggregate analysis |
| **Total** | **10-15 min/customer** | First one slower, can parallelize later |