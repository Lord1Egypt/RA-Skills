# Article Templates

Five travel editorial formats for UniqueStaysUSA journal posts. Each type has a proven section structure, word count target, and a reference post that models the quality standard.

## Quick-Reference Selection Table

| Signal | Article Type |
|---|---|
| Topic names a specific city/region | Destination Dispatch |
| Topic names a stay category (treehouses, domes, cabins) | Curated Roundup |
| Topic names a season or month | Seasonal Guide |
| Topic names an activity (stargazing, fishing, hiking) | Activity-Based Guide |
| Topic focuses on a single property | Stay Spotlight |

---

## Type 1: Destination Dispatch

**3-5 stays in one location.** The reader is already interested in this place — give them the best stays and the reason each one matters.

**Reference post:** `best-unique-stays-joshua-tree`

### Structure

1. **Opening dispatch** (2-3 paragraphs)
   - Scene-setting: what does this place feel like at a specific time of day?
   - The sensory anchor: one detail that puts the reader there (light, sound, texture)
   - Why this place rewards the kind of traveler who reads UniqueStaysUSA

2. **The thesis** (1 paragraph)
   - What makes the stays here worth knowing about
   - Sets up the selections that follow — not "here are some options" but "these are the ones that earn their place"

3. **Stay sections** (one per stay, ~200-300 words each)
   - `## [Evocative section title — feeling or moment, not the stay name]`
   - 2-4 paragraphs of editorial prose
   - `[EMBED: stay-slug]` placed after the first paragraph
   - Price and rating woven into the prose naturally (not in a separate callout)
   - One specific detail that passes the Irish Storytelling Test

4. **"When to Go"** (1-2 paragraphs)
   - Seasonal guide tied to search queries (e.g., "spring wildflowers peak March-April")
   - Practical booking window advice
   - What to pack or prepare for

5. **Closing** (1 paragraph)
   - Opens the door to the broader directory without hard-selling
   - Ends with an action or open question

### Payload field mapping

| Field | Value |
|---|---|
| `city` | Populated (e.g., "Joshua Tree") |
| `state` | Populated (e.g., "California") |
| `latitude` / `longitude` | Populated |
| `linkedStays` | All 3-5 stay IDs |
| `metaTitle` | `"Best Unique Stays in {City} \| {Subtypes}"` (under 60 chars) |

**Word count:** 1,400-2,000

---

## Type 2: Curated Roundup

**8-12 stays across multiple regions.** The reader is browsing a category — give them a curated journey, not a ranked list.

**Reference post:** `most-extraordinary-treehouses-america`

### Structure

1. **Opening** (2-3 paragraphs)
   - The primal/emotional appeal of this category
   - Why the reader should care (not "treehouses are popular" but "there's a specific kind of quiet you only find 40 feet up")
   - What the reader will find below: a curated journey, not an exhaustive list

2. **Stay sections** (one per stay, ~150-200 words each)
   - `## [Evocative section title — feeling, not geography]`
   - `[EMBED: stay-slug]` placed after the first paragraph
   - 2-3 paragraphs of editorial prose
   - Organized by feeling/mood/arc — NOT by geography or ranking
   - Each stay description must feel distinct (no two sound alike)

3. **"How to Choose Your {Category}"** (2-3 paragraphs)
   - Practical subsections: For romance, For groups, For budget, For solitude
   - Decision framework, not just descriptions
   - Cross-references to stays above

4. **Closing** (1 paragraph)
   - The bigger picture — why these stays matter
   - Open door to directory

### Payload field mapping

| Field | Value |
|---|---|
| `city` | Empty (national scope) |
| `state` | Empty |
| `latitude` / `longitude` | Empty |
| `linkedStays` | All 8-12 stay IDs |
| `metaTitle` | `"{Number} Most {Adjective} {Category} in America"` (under 60 chars) |

**Word count:** 1,800-2,500

---

## Type 3: Seasonal Guide

**5-8 stays organized around a season or event.** The reader is planning — give them the right stays at the right time.

**Reference post:** (new — calendar has entries like "Snow Globe Stays," "Fall Foliage Cabins")

### Structure

1. **Opening** (2 paragraphs)
   - What this season feels like in the places you're about to describe
   - Why now is the right time — urgency without hype

2. **The seasonal thesis** (1 paragraph)
   - Why the stays below are right for this exact moment
   - What ties them together beyond "they're nice in winter"

3. **Stay sections** (one per stay, ~150-250 words each)
   - `## [Evocative section title — seasonal moment]`
   - `[EMBED: stay-slug]` placed after the first paragraph
   - Seasonal context woven into the editorial prose
   - Organized by region or experience type

4. **"Planning Your {Season} Trip"** (2-3 paragraphs)
   - Booking windows and pricing trends
   - Weather realities (honest, not selling)
   - Packing tips specific to the season
   - "Book by [date]" if there's a genuine deadline

5. **Closing** (1 paragraph)

### Payload field mapping

| Field | Value |
|---|---|
| `city` / `state` | Empty unless regionally focused |
| `publishedAt` | Timed 4-6 weeks before target season |
| `linkedStays` | All 5-8 stay IDs |
| `metaTitle` | `"Best {Category} for {Season} Travel \| {Region}"` (under 60 chars) |

**Word count:** 1,500-2,200

---

## Type 4: Activity-Based Guide

**4-7 stays organized around an activity.** The reader knows what they want to do — give them the stays that amplify it.

**Reference post:** `workcation-manifesto-remote-work-treehouse`

### Structure

1. **Opening** (2 paragraphs)
   - The activity itself — what draws people to it, sensory detail
   - Why the right stay matters for this specific activity (not just "these places are nice")

2. **The thesis** (1 paragraph)
   - The connection between activity and accommodation
   - What makes a stay good for this activity (beyond "it's near trails")

3. **Stay sections** (one per stay, ~200-250 words each)
   - `## [Evocative section title — activity moment]`
   - `[EMBED: stay-slug]` placed after the first paragraph
   - Each section connects the property to the specific activity
   - Practical details: gear storage, proximity, conditions

4. **"What to Know Before You Go"** (2-3 paragraphs)
   - Activity-specific tips, gear, permits
   - Best conditions and when they occur
   - Beginner vs. advanced considerations

5. **Closing** (1 paragraph)

### Payload field mapping

| Field | Value |
|---|---|
| `city` / `state` | Empty if multi-region |
| `linkedStays` | All 4-7 stay IDs |
| `metaTitle` | `"Best {Category} for {Activity} \| {Region}"` (under 60 chars) |

**Word count:** 1,400-2,000

---

## Type 5: Stay Spotlight

**Deep dive on a single extraordinary property.** The reader is already intrigued — give them every reason to book.

### Structure

1. **Opening** (2-3 paragraphs)
   - The story of arriving at this place
   - First impressions — sensory, specific, immediate
   - Why this property earned a spotlight

2. **The space** (3-4 paragraphs)
   - Room-by-room or feature-by-feature walkthrough
   - Not a catalog — a narrative tour
   - Architectural or design details that distinguish it
   - The specific detail that passes the Irish Storytelling Test

3. **The surroundings** (2 paragraphs)
   - Area guide — what's nearby, what's worth doing
   - The neighborhood character, not tourist highlights
   - Distances and logistics

4. **Practical details** (1-2 paragraphs)
   - Pricing by season
   - Booking platform and direct link
   - Best time to visit
   - Getting there (nearest airport, drive time)

5. **Closing** (1 paragraph)
   - Who this stay is for (and who it isn't)
   - The final image that makes someone open the booking page

### Payload field mapping

| Field | Value |
|---|---|
| `city` | Populated |
| `state` | Populated |
| `latitude` / `longitude` | Populated |
| `linkedStays` | Single stay ID |
| `metaTitle` | `"{Stay Name} Review \| {City} Unique Stay"` (under 60 chars) |

**Word count:** 1,000-1,500
