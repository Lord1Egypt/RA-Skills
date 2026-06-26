# Trending Meme Templates — Sources & Methods

How to get fresh, currently trending meme templates beyond the static classic catalog.

## 1. Imgflip API (Free, No Auth)

The Imgflip API returns ~100 popular templates. Not truly "trending" (ranked by all-time popularity), but a good general catalog.

```bash
curl -s "https://api.imgflip.com/get_memes" | python3 -c "
import sys, json
memes = json.load(sys.stdin)['data']['memes'][:20]
for m in memes:
    print(f\"{m['name']}: {m['url']}\")
"
```

Use with memegen.link's custom template:
```
https://api.memegen.link/images/custom/{top}/{bottom}.png?background={imgflip_url}&width=800
```

## 2. Imgflip Trending Scraper (No Auth)

For actually trending/new templates, scrape Imgflip's "Top New" page. See `scripts/imgflip-trending.py`.

```bash
python3 scripts/imgflip-trending.py
```

Outputs JSON array of `{id, name, url}` — the newest popular templates on Imgflip.

## 3. Reddit (Requires OAuth)

Reddit's `r/MemeTemplates` is the single best source for genuinely trending blank templates. Requires OAuth setup.

### Setup (one-time)

1. Go to https://www.reddit.com/prefs/apps and create a **script** type app
2. Note the **client ID** (under the app name) and **secret**
3. Set env vars:
   ```bash
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_secret"
   export REDDIT_USERNAME="your_username"
   export REDDIT_PASSWORD="your_password"
   ```

### Fetching Trending Templates

```bash
./scripts/reddit-trending.sh 20
```

Returns JSON array of `{title, url, score, created_utc}` from r/MemeTemplates/hot.

### Using Reddit Templates as Custom Backgrounds

```bash
# Get a trending template URL from the script output, then:
curl -s -o /tmp/meme.png \
  "https://api.memegen.link/images/custom/top_text/bottom_text.png?background=TEMPLATE_URL&width=800"
```

### Spanish/Latin Meme Subreddits (same OAuth setup)

| Subreddit | Focus | Content |
|-----------|-------|---------|
| **r/yo_elvr** | Spanish "me_irl" — relatable memes | Active, good quality |
| **r/memexico** | Mexican memes | Culture-specific, very active |
| **r/MemesEnEspanol** | General Spanish memes | Mixed quality |
| **r/LatinoPeopleTwitter** | Latino culture (mixed EN/ES) | Twitter screenshots, memes |

## 4. Giphy (Requires Free API Key)

Giphy returns finished reaction GIFs, not blank templates. Useful for GIF-based memes.

### Setup

1. Register at https://developers.giphy.com and create an app
2. Copy the **beta API key** (free: 100 calls/hour)
3. Set env var:
   ```bash
   export GIPHY_API_KEY="your_api_key"
   ```

### Endpoints

| Endpoint | URL |
|----------|-----|
| Search | `https://api.giphy.com/v1/gifs/search?api_key=KEY&q=QUERY&limit=10` |
| Trending | `https://api.giphy.com/v1/gifs/trending?api_key=KEY&limit=10` |
| Random | `https://api.giphy.com/v1/gifs/random?api_key=KEY&tag=TAG` |

### Quick Search

```bash
./scripts/giphy-search.sh "disappointed reaction"
```

Returns top 5 GIF URLs and downloads the best match to `/tmp/meme.gif`.

### Example: GIF Reaction Meme

```bash
# 1. Search for a reaction GIF
./scripts/giphy-search.sh "facepalm"

# 2. Verify the download
file /tmp/meme.gif       # Should say "GIF image data"
ls -la /tmp/meme.gif     # Should be >50KB

# 3. Use or deliver the GIF as needed
```

## 5. Spanish Language Support

All Spanish characters render correctly in memegen.link:
- Accented vowels (á, é, í, ó, ú) — work directly in URLs
- ñ (eñe) — works directly
- Inverted punctuation (¿, ¡) — work directly
- `?` uses `~q` encoding (same as English)

### Latin American-Specific Templates

Templates unique to Spanish-language meme culture (use as custom backgrounds):

| Template | Usage | Cultural Context |
|----------|-------|------------------|
| El Chavo del 8 characters | Ironic situations, nostalgia | Mexican TV show |
| Don Ramon | Sarcastic wisdom, poverty humor | El Chavo character |
| Chapulín Colorado | Ironic heroism | Mexican TV superhero |
| El Buki (Marco Antonio Solís) | Romantic/dramatic situations | Mexican singer |
| "No era penal" | Injustice, bad calls | Mexico football |
| "Dice mi mama que siempre no" | Cancelled plans | Mexican childhood |

None of these exist as built-in templates — use custom background URLs.

## Source Comparison

| Source | Auth Required | Cost | Content Type | Freshness |
|--------|--------------|------|-------------|-----------|
| Imgflip API | None | Free | Blank templates | Static (all-time popular) |
| Imgflip Scraper | None | Free | Blank templates | Trending (top new) |
| Reddit OAuth | Yes | Free | Blank templates | Genuinely trending |
| Giphy | Yes (free key) | Free (100/hr) | Reaction GIFs | Trending GIFs |
