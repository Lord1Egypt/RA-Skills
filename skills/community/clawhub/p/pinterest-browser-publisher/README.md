# Pinterest Browser Publisher (浏览器自动发布)

Use Playwright to automate Pinterest pin publishing via browser. No API key needed — simulates human interaction.

## Prerequisites

```bash
npm install -g playwright
playwright install chromium
```

## Authentication

### Option 1: Cookie Login (Recommended)

1. Log in to Pinterest manually in your browser
2. Export cookies (use browser extension like "EditThisCookie" or "cookie-editor")
3. Save to `~/.config/pinterest/cookies.json`

### Option 2: Email/Password Login

First run will require manual 2FA if enabled. Subsequent runs use saved session.

## Usage

### Single Pin

```bash
node publish-pin.js \
  --image "./pinterest/01-cover.png" \
  --title "Mercury Retrograde Survival Guide" \
  --description "Your pin description here..." \
  --board "Astrology & Spiritual Wellness" \
  --link "https://yourblog.com/mercury-retrograde"
```

### Carousel Pin (Multiple Images)

```bash
node publish-pin.js \
  --images "./pinterest/01.png,./pinterest/02.png,./pinterest/03.png" \
  --title "Mercury Retrograde Survival Guide" \
  --description "Your pin description here..." \
  --board "Mercury Retrograde Survival"
```

### Batch Publish from JSON

```bash
node publish-batch.js --input pins.json --delay 30000
```

`pins.json`:
```json
[
  {
    "images": ["./01.png", "./02.png", "./03.png"],
    "title": "Pin Title 1",
    "description": "Description 1",
    "board": "Board Name",
    "link": "https://..."
  }
]
```

## Configuration

Create `~/.config/pinterest/config.json`:

```json
{
  "email": "your@email.com",
  "password": "your-password",
  "headless": false,
  "slowMo": 100,
  "defaultBoard": "Astrology & Spiritual Wellness",
  "defaultLink": "https://yourblog.com",
  "postDelay": 30000
}
```

## Anti-Detection

| Technique | Implementation |
|-----------|----------------|
| Human-like delays | Random 2-5s between actions |
| Mouse movement | Bezier curve simulation |
| Viewport | Random 1920×1080 to 2560×1440 |
| User Agent | Rotating real browser UAs |
| Post timing | Randomize publish time ±15 min |
| Session reuse | Save cookies after first login |

## Rate Limits

| Action | Safe Limit |
|--------|------------|
| Pins per day | 25-50 |
| Pins per hour | 10 |
| Comments per day | 50 |
| Follows per day | 50 |

**Warning**: Exceeding limits may trigger account review.

## Error Handling

| Error | Recovery |
|-------|----------|
| Login failed | Clear cookies, retry with manual login |
| Board not found | Create board first or check name |
| Image upload timeout | Increase timeout, check file size |
| 2FA required | Complete manually, save session |

## Output

```
✓ Logged in as @yourhandle
✓ Created/Found board: "Mercury Retrograde Survival"
✓ Uploaded 3 images
✓ Set title and description
✓ Published pin: https://pinterest.com/pin/123456789
✓ Added to 3 boards (primary + 2 secondary)
⏳ Waiting 30s before next pin...
```

## Integration with aura-image-gen

```bash
# Generate images
aura-image-gen --topic "Mercury Retrograde" --platform pinterest --output ./pins/

# Publish
node publish-pin.js \
  --images "./pins/*.png" \
  --title "$(cat ./pins/title.txt)" \
  --description "$(cat ./pins/description.txt)" \
  --board "Astrology & Spiritual Wellness"
```

## Security Notes

- ⚠️ Never commit `cookies.json` to git
- ⚠️ Use environment variables for credentials in production
- ⚠️ Run in isolated environment if possible
- ⚠️ Monitor account health regularly

## Troubleshooting

### "Cannot read property 'click' of null"
Pinterest changed selector. Update `selectors.js` with current DOM.

### Login loop / CAPTCHA
- Clear cookies
- Use residential proxy if available
- Add longer delays between actions
- Complete CAPTCHA manually once

### Images fail to upload
- Check file size (<20MB per image)
- Use PNG or JPEG format
- Ensure file paths are absolute

## Files Structure

```
pinterest-publisher/
├── publish-pin.js       # Single pin publisher
├── publish-batch.js     # Batch publisher
├── login.js             # Manual login helper
├── selectors.js         # Pinterest DOM selectors (update when UI changes)
├── utils/
│   ├── cookies.js       # Cookie management
│   ├── mouse.js         # Human-like mouse movement
│   └── delays.js        # Random delay helpers
└── config/
    └── default.json     # Default configuration
```
