# SEO Requirements

Travel-specific SEO checklist for UniqueStaysUSA journal posts. Applied during Phase 4 (SEO optimization).

## Keyword Placement Checklist

Every post must pass all of these:

- [ ] Primary keyword in the title
- [ ] Primary keyword in `metaTitle` (under 60 chars)
- [ ] Primary keyword in the first 100 words of body
- [ ] Primary keyword in at least one H2
- [ ] Primary keyword in `metaDescription` (under 160 chars)
- [ ] Primary keyword in `excerpt`
- [ ] 2-3 long-tail keyword variations woven into body paragraphs naturally
- [ ] Location keywords in `city`, `state` fields (for destination dispatches)
- [ ] Stay names used as natural anchor text in internal links

## Travel Keyword Patterns

These patterns drive the highest-intent traffic for UniqueStaysUSA. Target them based on article type:

| Pattern | Example | Article Type |
|---|---|---|
| `"[stay type] rentals [state]"` | "treehouse rentals Oregon" | Curated Roundup |
| `"best [stay type] near [landmark]"` | "best unique stays near Joshua Tree" | Destination Dispatch |
| `"[stay type] with [amenity] [state]"` | "cabins with hot tub Colorado" | Activity-Based Guide |
| `"[season] [stay type] [region]"` | "winter cabin getaways Pacific Northwest" | Seasonal Guide |
| `"[stay type] for [audience]"` | "treehouses for remote workers" | Activity-Based Guide |
| `"[stay type] vs hotel [state]"` | "treehouse vs hotel cost Colorado" | Comparison content |
| `"[stay type] near [national park]"` | "cabins near Yellowstone Montana" | Destination Dispatch |
| `"unique stays [state]"` | "unique stays Vermont" | Curated Roundup |

## AI Citation Optimization

Structure content so AI systems (ChatGPT, Perplexity, AI Overviews) can extract and cite it:

### Definition blocks
Include 1-2 clear, self-contained definition sentences early in the article. These should answer "what is X?" directly.

**Example:**
> A treehouse stay is a rental property built into or suspended from living trees, typically elevated 10-50 feet above ground, offering an immersive forest experience that conventional cabins cannot replicate.

### FAQ section
Include 3-5 questions that match common queries for the topic. Place after the main content, before closing.

**Format:**
```
## Frequently Asked Questions

### Can you actually rent a treehouse in [State]?
[2-3 sentence answer with specific example]

### How much does a [stay type] rental cost?
[2-3 sentence answer with price range]

### What's the best time to visit [destination] for [activity]?
[2-3 sentence answer with specific months]
```

### Sourced statistics
Cite 2-3 statistics with real attribution. Do not fabricate numbers. If a stat cannot be verified, rephrase as an observation or remove it.

**Good:** "According to Airbnb's 2025 travel report, treehouse listings saw a 45% increase in bookings year-over-year."
**Bad:** "Treehouses are becoming increasingly popular." (vague, unsourceable)

### Comparison tables
Where applicable, include a structured comparison that AI can extract:

| Factor | [Stay Type] | Hotel |
|---|---|---|
| Average cost/night | $X-$Y | $X-$Y |
| Privacy | [rating] | [rating] |
| Unique experience | [rating] | [rating] |

### Structured lists
Use ordered or unordered lists for "best of" content. AI systems extract these reliably.

## Internal Linking Rules

- Every journal post must link to at least 2 other journal posts (use contextual inline links, not "Related posts" blocks)
- Link to relevant spoke pages when the article covers a spoke topic (`/work-friendly`, `/pet-friendly`, etc.)
- Link to state-specific pages when geographic overlap exists
- Use descriptive anchor text — never "click here" or "read more"
- Cross-link between posts that share stays, regions, or themes

**How to find related posts:**
```bash
# Query Payload for posts in the same state or with overlapping stays
GET /api/blog-posts?where[state][equals]={state}&where[status][equals]=published&depth=0&limit=10
```

## External Linking Rules

- 2-3 authoritative external sources per post
- Link to specific pages, not homepages
- Attribution must be real — no "according to experts" without naming the source
- Prefer: official tourism sites, National Park Service, established travel publications, academic research

## Meta Requirements

| Field | Constraint |
|---|---|
| `metaTitle` | Under 60 chars, includes primary keyword, reads like editorial |
| `metaDescription` | Under 160 chars, includes keyword + one specific detail (number, name, price), ends with implicit invitation |
| `slug` | kebab-case, no dates in path, year suffix only for listicles |
| `excerpt` | 2-3 sentences, includes keyword, specific and compelling |

### Meta title patterns by article type

| Type | Pattern | Example |
|---|---|---|
| Destination Dispatch | `"Best Unique Stays in {City} \| {Subtypes}"` | `"Best Unique Stays in Joshua Tree \| Airstreams, Domes & Glass Villas"` |
| Curated Roundup | `"{Number} Most {Adjective} {Category} in America"` | `"10 Most Extraordinary Treehouses in America"` |
| Seasonal Guide | `"Best {Category} for {Season} Travel \| {Region}"` | `"Best Snow Globe Stays for Winter Travel \| US"` |
| Activity-Based Guide | `"Best {Category} for {Activity} \| {Region}"` | `"Best Cabins for Stargazing \| Western US"` |
| Stay Spotlight | `"{Stay Name} Review \| {City} Unique Stay"` | `"Fox A-Frame Review \| Skagit Valley Unique Stay"` |

## Cannibalization Check

Before finalizing, verify the new post does not compete with existing content:

1. Query Payload for all published posts: `GET /api/blog-posts?where[status][equals]=published&depth=0&limit=50`
2. Check for overlapping target keywords
3. If overlap exists, either: differentiate the angle, or consolidate into one stronger post
4. The calendar should prevent this, but verify anyway

## Structured Data

The frontend handles `BlogPosting` schema rendering. The skill must ensure these fields are populated so the schema renders correctly:

- `title` (required)
- `excerpt` (required — becomes description)
- `publishedAt` (required)
- `heroImage` (recommended — becomes image)
- `metaTitle` and `metaDescription` (recommended)

No additional markup is needed in the content itself.
