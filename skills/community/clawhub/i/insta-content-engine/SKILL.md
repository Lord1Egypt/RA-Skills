---
name: social-search
description: Find trending topics, create editorial-style social media graphics, and post to X/Twitter and Instagram. Includes image generation with photographic backgrounds, dark gradient overlays, and bold typography. No paid social APIs needed.
---

# Social Search & Content Creator

Find → Create → Post pipeline for X/Twitter and Instagram content.

## Prerequisites

- **X/Twitter**: `bird` CLI installed and authenticated via browser cookies
- **Instagram Search**: Brave Search API key (set `BRAVE_API_KEY` or configure in OpenClaw)
- **Image Generation**: OpenAI API key (set `OPENAI_API_KEY`) — uses gpt-image-1
- **Instagram Posting**: `pip3 install instagrapi pillow` + IG_USERNAME/IG_PASSWORD env vars

## 1. FIND — Research Trending Topics

### X/Twitter (bird CLI)
```bash
bird search "query" -n 10          # Search tweets
bird read <url-or-id>              # Read a specific tweet
bird thread <url-or-id>            # Full thread
bird mentions                      # Check mentions
bird user-tweets <username>        # User's tweets
```

### Instagram (Brave-powered scraper)
```bash
node {baseDir}/scripts/instagram-search.js "query" [--limit 10] [--type posts|profiles|reels|all]
```

Types: `posts` (inurl:/p/), `profiles` (user pages), `reels` (inurl:/reel/), `all` (default)

### Viral/Trending Search (recommended starting point)
```bash
# Find viral content about a topic (sorted by engagement)
node {baseDir}/scripts/viral-search.js "query" [options]

# Options:
#   --platform x|instagram|both    (default: both)
#   --min-likes N                  Min likes to include (default: 50)
#   --min-retweets N               Min retweets (default: 10)
#   --sort engagement|recent       (default: engagement)
#   --limit N                      Results per platform (default: 10)
#   --trending                     What's blowing up RIGHT NOW on X
#   --days N                       Only last N days (default: 7)
```

Examples:
```bash
# What's viral about AI trading this week
node {baseDir}/scripts/viral-search.js "AI trading" --min-likes 100 --days 7

# What's trending across crypto right now (no query needed)
node {baseDir}/scripts/viral-search.js --trending

# Instagram-only viral search
node {baseDir}/scripts/viral-search.js "DeFi" --platform instagram --limit 10

# Lower the bar for niche topics
node {baseDir}/scripts/viral-search.js "delta neutral farming" --min-likes 10 --min-retweets 3
```

**How engagement scoring works:**
- Score = likes × 1 + retweets × 3 + replies × 2
- Retweets weighted highest (distribution signal)
- Replies weighted over likes (conversation signal)
- Results sorted by score descending

## 2. CREATE — Generate Editorial Graphics

### The System: Photographic Background + Dark Gradient + Bold Typography

**This is what makes the images look professional, not just text on a background.**

The approach:
- **Top 60%**: Cinematic photographic scene (real subjects, dramatic lighting)
- **Bottom 40%**: Heavy dark gradient overlay (95% black → transparent)
- **Text**: Bold condensed typography (Anton-style) sitting on the gradient
- **Result**: Looks like Bloomberg/Kalshi editorial cards

### Generate Images
```bash
OPENAI_API_KEY="your-key" python3 {baseDir}/scripts/gen_image.py "prompt" output.png [1024x1536]
```

Sizes: `1024x1024` (square), `1024x1536` (portrait/Instagram), `1536x1024` (landscape/Twitter)

### ⚠️ CRITICAL IMAGE RULES (learned the hard way)

1. **NEVER just put text on a solid dark background** — it looks flat and amateur
2. **ALWAYS use a photographic/cinematic background** — real scenes, real subjects
3. **ALWAYS use dark gradient overlay** on the lower 40% for text readability
4. **Keep subject visible** in the top 60% — face, setting, context
5. **Text lives in the bottom 40% only** — never cover the subject
6. **Use bold condensed typography** (Anton-style) — not regular weight fonts
7. **Include branded elements** — badge, branding URL, slide counter
8. **Cinematic lighting** — moody, dramatic, not flat studio lighting

### Master Prompt Template

Copy this template exactly. Only change the parts in [BRACKETS].

```
Instagram carousel post design. EXACTLY 1080 pixels wide by 1350 pixels tall (4:5 vertical ratio).

Background: [DESCRIBE THE SCENE - who/what is shown, setting, lighting, mood]. Keep subject clearly visible in top 60% of image. Cinematic lighting, dramatic.

Overlay: Heavy dark gradient ONLY on bottom 40% of image - solid black (95% opacity) at very bottom, fading to transparent at 60% height. Top portion stays clear.

Text positioning (bottom area):
- 65% from top: Small rectangular badge with [COLOR] background and [TEXT COLOR] bold text: [BADGE TEXT]
- 70-90% from top: Huge white bold text in Anton font, uppercase, centered:
[MAIN HEADLINE
SPLIT ACROSS
2-3 LINES]
- [Optional: Below headline in smaller white text, any supporting details]
- Bottom right corner (95% from top): [X/Y] in white, small
- Bottom left corner (95% from top): [brand.url] in white, Montserrat Bold, small, lowercase

Font: Anton for headline. Montserrat Bold for branding.

Style: Clean Instagram carousel slide, vertical format, text at bottom like Kalshi/Bloomberg editorial style. Cinematic, high contrast, professional.
```

### Badge Color System
- 🔵 Cyan (#00D4FF): "EXPLAINED", "GUIDE", educational content
- 🟠 Orange (#FF6B00): "HOW IT WORKS", "DEEP DIVE", breakdowns
- 🟢 Green (#22c55e): "THE SHIFT", "SOLUTION", "REAL CASE", positive takes
- 🔴 Red (#e63946): "WARNING", "UNFAIR", "MYTH", negative/urgent
- ⚫ Black (#000000): "TRENDING", "BREAKING", news

### Background Scene Ideas by Topic

**Crypto/Trading**: Trader at multiple monitors, trading floor, candlestick charts on screens
**Tech/AI**: Neural network visualizations, server rooms, holographic displays
**Finance**: City skyline at night, office with Bloomberg terminals, stock exchange
**Startup**: Founder at whiteboard, team in modern office, product on screen
**Education**: Person studying, lecture hall, books with highlighted text

### Carousel Structure (3 slides)
- **Slide 1 — The Hook**: Sets the scene, asks the question (e.g., "What is X?")
- **Slide 2 — The Breakdown**: How it works, the layers, the details
- **Slide 3 — The Shift**: Why it matters, the bigger picture, call to action

### Example: Crypto Educational Carousel

**Slide 1 prompt background**: "A young male trader in a dark room lit by multiple monitors showing crypto charts. Blue and green screen glow on his face. Hoodie, leaning forward, focused."

**Slide 2 prompt background**: "Close-up of an AI neural network visualization on a large curved monitor in a dark trading room. Neon blue data streams flowing across the screen."

**Slide 3 prompt background**: "Aerial view of a massive trading floor with hundreds of screens running autonomously, seats empty. No humans present. Dramatic overhead shot, neon blue glow."

## 3. POST — Publish Content

### X/Twitter (bird CLI)
```bash
bird tweet "Your tweet text"                         # Text only
bird tweet "Text" --media image.jpg                  # With image
bird tweet "Text" --media img1.jpg --media img2.jpg  # Multiple
bird reply <tweet-id-or-url> "Reply text"            # Reply
```

### Instagram (instagrapi)
```bash
# Photo post
node {baseDir}/scripts/instagram-post.js --action photo --caption "Caption" image.jpg

# Reel
node {baseDir}/scripts/instagram-post.js --action reel --caption "Caption" video.mp4

# Story
node {baseDir}/scripts/instagram-post.js --action story --caption "Caption" image.jpg

# Carousel
node {baseDir}/scripts/instagram-post.js --action carousel --caption "Caption" img1.jpg img2.jpg img3.jpg
```

Instagram auth: Set `IG_USERNAME` and `IG_PASSWORD` env vars. Google sign-in won't work — need a password set on the account.

## Full Workflow Example

```bash
# 1. Research what's trending
bird search "agentic trading crypto" -n 10
node {baseDir}/scripts/instagram-search.js "AI crypto trading" --limit 10

# 2. Generate 3-slide carousel
OPENAI_API_KEY="key" python3 {baseDir}/scripts/gen_image.py "slide 1 prompt..." slide1.png 1024x1536
OPENAI_API_KEY="key" python3 {baseDir}/scripts/gen_image.py "slide 2 prompt..." slide2.png 1024x1536
OPENAI_API_KEY="key" python3 {baseDir}/scripts/gen_image.py "slide 3 prompt..." slide3.png 1024x1536

# 3. Post to X
bird tweet "your caption" --media slide1.png --media slide2.png --media slide3.png

# 4. Post to Instagram
node {baseDir}/scripts/instagram-post.js --action carousel --caption "your caption" slide1.png slide2.png slide3.png
```
