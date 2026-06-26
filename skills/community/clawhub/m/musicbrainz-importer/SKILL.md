---
name: musicbrainz_importer
description: "Look up and add music metadata on MusicBrainz. Use when asked to check if an artist, album, or release exists on MusicBrainz, find MusicBrainz entries linked to Spotify URLs, or add/edit releases, artists, or other entities on MusicBrainz. Triggers on mentions of MusicBrainz, MB, music database, adding releases, music metadata, or linking Spotify to MusicBrainz."
homepage: https://github.com/its-clawdia/musicbrainz-importer
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["curl", "jq", "node"] },
        "install":
          [
            {
              "id": "playwright",
              "kind": "npm",
              "package": "playwright",
              "bins": [],
              "label": "Install Playwright (npm)",
            },
          ],
      },
  }
---

# MusicBrainz

## Browser Setup

All browser work uses **Playwright** via a Node.js script. Install once per session:

```bash
cd /tmp && npm ls playwright 2>/dev/null || npm install playwright
```

Launch pattern (use in every script):

```javascript
import { chromium } from 'playwright';
import { execSync } from 'child_process';

// Detect Playwright's bundled Chromium path dynamically
const chromiumPath = process.env.PLAYWRIGHT_CHROMIUM_PATH
  || execSync('find ~/.cache/ms-playwright -name chrome -path "*/chrome-linux*/chrome" 2>/dev/null | head -1', { encoding: 'utf-8' }).trim()
  || execSync('find ~/.cache/ms-playwright -name Chromium -path "*/Chromium.app/Contents/MacOS/Chromium" 2>/dev/null | head -1', { encoding: 'utf-8' }).trim();
if (!chromiumPath) throw new Error('Chromium not found. Run: npx playwright install chromium');

const browser = await chromium.launch({
  executablePath: chromiumPath,
  headless: true,
  args: ['--no-sandbox']
});
const page = await browser.newPage();
```

## Architecture: Isolated Steps

There are **four operations**. Each is a self-contained Playwright script. Never combine them into one script. Run them sequentially:

1. **Login** — authenticate the browser session
2. **Add Artist** — create a new artist entity
3. **Add Release** — create a release with tracks, metadata, and Spotify link
4. **Upload Cover Art** — attach album artwork to an existing release

Between steps, **close the browser** (`await browser.close()`). Each script launches fresh, logs in if needed, does its one job, and exits. This prevents state pollution between operations.

---

## Preflight — Credentials Check

**Run before any write operation.** Skip for read-only lookups.

```bash
bash scripts/preflight.sh
```

Credentials live in `.credentials.json` in the skill directory.

- **`MISSING_CREDENTIALS`**: Ask user for MusicBrainz username + password. Save:
  ```bash
  cat > ~/.openclaw/skills/musicbrainz/.credentials.json << 'EOF'
  {"username": "USER", "password": "PASS"}
  EOF
  ```
- **`INVALID_CREDENTIALS`**: Ask user to verify, update file, re-run.
- No account → https://musicbrainz.org/register

---

## Step 1: Login

Every Playwright script that writes to MB must start with login. Use this exact pattern:

```javascript
import { readFileSync } from 'fs';
const creds = JSON.parse(readFileSync(
  process.env.HOME + '/.openclaw/skills/musicbrainz/.credentials.json'
));

await page.goto('https://musicbrainz.org/login', { waitUntil: 'networkidle', timeout: 30000 });
await page.fill('#id-username', creds.username);
await page.fill('#id-password', creds.password);
// IMPORTANT: There are TWO submit buttons on the page (search + login).
// Must click the one with "Log in" text.
await page.evaluate(() => {
  Array.from(document.querySelectorAll('button[type="submit"]'))
    .find(b => b.textContent.includes('Log in'))?.click();
});
await page.waitForTimeout(5000);

// Verify: should redirect to /user/<username>
if (page.url().includes('/login')) {
  throw new Error('Login failed');
}
```

### Key gotcha
The MusicBrainz login page has **two forms**: a search form and the login form. Both have `button[type="submit"]`. Using `page.click('button[type="submit"]')` hits the search button. **Always** use the evaluate pattern above to find the button by text content.

---

## Step 2: Add Artist

**When:** Artist doesn't exist on MusicBrainz. Check first with `mb_lookup.sh` or the search API.

### Script structure

```javascript
// ... browser launch + login (Step 1) ...

await page.goto('https://musicbrainz.org/artist/create', {
  waitUntil: 'networkidle', timeout: 30000
});
await page.waitForTimeout(2000);

// Fill fields
await page.fill('#id-edit-artist\\.name', 'Artist Name');
await page.fill('#id-edit-artist\\.sort_name', 'Name, Artist'); // "Last, First" or "Name, The"
await page.selectOption('#id-edit-artist\\.type_id', '2'); // 1=Person, 2=Group, 4=Other
await page.fill('#id-edit-artist\\.edit_note',
  'Adding artist from Spotify: https://open.spotify.com/artist/<id>');

// Submit — use form.submit() to avoid button ambiguity
await page.evaluate(() => {
  document.getElementById('id-edit-artist.name')?.closest('form')?.submit();
});
await page.waitForTimeout(5000);

// Extract MBID from redirect URL
const artistUrl = page.url();
const artistMbid = artistUrl.match(/artist\/([a-f0-9-]{36})/)?.[1];
console.log('Artist MBID:', artistMbid);

await browser.close();
```

### After completion
Report the artist MBID and link to user. Store the MBID — needed for adding releases.

---

## Step 3: Add Release

**Every release follows this identical flow**, regardless of what happened before (login, artist creation, previous releases). Each is a fresh Playwright script.

### Form field IDs (for reference)

| Field | ID | Values |
|-------|----|--------|
| Title | `name` | text |
| Artist | `ac-source-single-artist` | text (autocomplete) |
| Release group | `release-group` | text (autocomplete) |
| Primary type | `primary-type` | `1`=Album, `2`=Single, `3`=EP |
| Status | `status` | `1`=Official |
| Language | `language` | `120`=English, `145`=German |
| Script | `script` | `28`=Latin, `12`=Cyrillic |
| Year | `event-date-0` | YYYY |
| Month | `.partial-date-month` | MM |
| Day | `.partial-date-day` | DD |
| Country | `country-0` | `240`=[Worldwide] |
| Label | `label-0` | text (autocomplete) |
| Barcode | `barcode` | text |
| No barcode | `no-barcode` | checkbox |
| Packaging | `packaging` | `7`=None |

### Known traps

1. **Release group autocomplete blocks the form.** After filling the title and selecting an artist, the release group field auto-searches and opens a popup dialog ("Add medium") that makes all other form fields invisible to Playwright (offsetParent = null, zero-size rects). You **must** dismiss this before interacting with other fields.

2. **Artist autocomplete can match wrong entity.** Typing "The Bride Wore Black" and pressing ArrowDown+Enter may select a similarly-named *release group* or a different artist. **Use the MBID** in the autocomplete field for exact matching.

3. **React selects don't respond to `page.selectOption()` when not visible.** Use `evaluate` with native setters instead.

4. **Track parser dialog vs Add Medium dialog.** The track parser opens in a jQuery UI dialog. There may be multiple dialogs open. Always target by dialog title text.

5. **Track parser may double tracks.** The parse can produce duplicate entries. Always verify track count after parsing.

### Script structure

```javascript
// ... browser launch + login (Step 1) ...

// Navigate to empty add-release form
await page.goto('https://musicbrainz.org/release/add', {
  waitUntil: 'networkidle', timeout: 30000
});
await page.waitForTimeout(3000);

// === TITLE ===
// Use evaluate with native setter — keyboard typing is fragile
await page.evaluate((title) => {
  const el = document.getElementById('name');
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
  ).set;
  setter.call(el, title);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
}, 'Album Title');
await page.waitForTimeout(500);

// === ARTIST ===
// Paste the MBID for exact matching (avoids wrong autocomplete selections)
const artistInput = page.locator('#ac-source-single-artist');
await artistInput.click();
await page.keyboard.type('<artist-mbid>', { delay: 5 });
await page.waitForTimeout(4000);
await page.keyboard.press('ArrowDown');
await page.waitForTimeout(500);
await page.keyboard.press('Enter');
await page.waitForTimeout(3000);

// Verify artist matched (background turns green)
const artistOk = await page.evaluate(() => {
  const input = document.getElementById('ac-source-single-artist');
  return window.getComputedStyle(input).backgroundColor.includes('177'); // rgb(177,235,176)
});
if (!artistOk) throw new Error('Artist not matched');

// === DISMISS BLOCKERS ===
// The release-group autocomplete and "Add medium" dialog may have opened.
// Close everything before touching other fields.
await page.evaluate(() => {
  // Hide all autocomplete dropdowns
  document.querySelectorAll('ul.ui-autocomplete')
    .forEach(ul => ul.style.display = 'none');
  // Close any open dialogs (Add medium, search, etc.)
  document.querySelectorAll('.ui-dialog').forEach(d => {
    if (d.style.display !== 'none' && d.offsetParent !== null) {
      const close = d.querySelector('.ui-dialog-titlebar-close');
      if (close) close.click();
    }
  });
  // Blur active element
  document.activeElement?.blur();
});
await page.waitForTimeout(1000);

// === METADATA (all via evaluate — fields may not be "visible" to Playwright) ===
await page.evaluate(({ year, month, day }) => {
  function setSelect(id, val) {
    const el = document.getElementById(id);
    if (!el || el.disabled) return;
    el.value = val;
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }
  function setInput(id, val) {
    const el = document.getElementById(id);
    if (!el) return;
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    setter.call(el, val);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }

  setSelect('primary-type', '1');   // Album
  setSelect('status', '1');         // Official
  setSelect('language', '120');     // English
  setSelect('script', '28');        // Latin
  setSelect('packaging', '7');      // None
  setSelect('country-0', '240');    // [Worldwide]

  setInput('event-date-0', year);
  const dateContainer = document.getElementById('event-date-0')?.closest('.partial-date');
  if (dateContainer) {
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    const monthEl = dateContainer.querySelector('.partial-date-month');
    const dayEl = dateContainer.querySelector('.partial-date-day');
    if (monthEl) {
      setter.call(monthEl, month);
      monthEl.dispatchEvent(new Event('input', { bubbles: true }));
    }
    if (dayEl) {
      setter.call(dayEl, day);
      dayEl.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }

  // No barcode
  const cb = document.querySelector('#no-barcode');
  if (cb && !cb.checked) cb.click();
}, { year: '2007', month: '7', day: '10' });
await page.waitForTimeout(1000);

// === TRACKLIST ===
// Switch to Tracklist tab
await page.evaluate(() => {
  Array.from(document.querySelectorAll('.ui-tabs-anchor'))
    .find(t => t.textContent === 'Tracklist')?.click();
});
await page.waitForTimeout(2000);

// Set medium format to Digital Media
await page.evaluate(() => {
  const sel = document.querySelector('#tracklist select');
  if (sel) {
    const dm = Array.from(sel.options).find(o => o.text === 'Digital Media');
    if (dm) {
      sel.value = dm.value;
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
});

// Open track parser
await page.evaluate(() => {
  Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent === 'Track parser')?.click();
});
await page.waitForTimeout(1500);

// Fill track parser dialog — target by dialog title to avoid "Add medium" dialog
const trackText = '1. Track One (3:47)\n2. Track Two (2:50)'; // build from data
await page.evaluate((text) => {
  for (const dialog of document.querySelectorAll('.ui-dialog')) {
    if (dialog.style.display === 'none') continue;
    const title = dialog.querySelector('.ui-dialog-title');
    if (!title?.textContent.includes('Track parser')) continue;
    const ta = dialog.querySelector('textarea');
    if (ta) {
      const setter = Object.getOwnPropertyDescriptor(
        window.HTMLTextAreaElement.prototype, 'value'
      ).set;
      setter.call(ta, text);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    Array.from(dialog.querySelectorAll('button'))
      .find(b => b.textContent === 'Parse tracks')?.click();
    break;
  }
}, trackText);
await page.waitForTimeout(3000);

// Close track parser dialog
await page.evaluate(() => {
  for (const d of document.querySelectorAll('.ui-dialog')) {
    if (d.querySelector('.ui-dialog-title')?.textContent.includes('Track parser')) {
      d.querySelector('.ui-dialog-titlebar-close')?.click();
    }
  }
});
await page.waitForTimeout(1000);

// Confirm capitalization if warning appears
await page.evaluate(() => {
  document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
    const text = cb.closest('label')?.textContent || cb.parentElement?.textContent || '';
    if (text.includes('capitalized correctly') && !cb.checked) cb.click();
  });
});

// Verify track count
const trackCount = await page.evaluate(() =>
  document.querySelectorAll('tr.track').length
);

// === EXTERNAL LINKS (Spotify URL) ===
await page.evaluate(() => {
  Array.from(document.querySelectorAll('.ui-tabs-anchor'))
    .find(t => t.textContent === 'Release information')?.click();
});
await page.waitForTimeout(1000);

await page.evaluate((url) => {
  const input = document.querySelector('input[type="url"]');
  if (input) {
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    setter.call(input, url);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }
}, 'https://open.spotify.com/album/<id>');
await page.waitForTimeout(2000);

// === EDIT NOTE ===
await page.evaluate(() => {
  Array.from(document.querySelectorAll('.ui-tabs-anchor'))
    .find(t => t.textContent === 'Edit note')?.click();
});
await page.waitForTimeout(1000);

await page.evaluate((note) => {
  const ta = document.getElementById('edit-note-text');
  if (ta) {
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 'value'
    ).set;
    setter.call(ta, note);
    ta.dispatchEvent(new Event('input', { bubbles: true }));
  }
}, 'Added from Spotify: <url>');
await page.waitForTimeout(500);

// === SUBMIT ===
const canSubmit = await page.evaluate(() => {
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.includes('Enter edit'));
  return btn && !btn.disabled;
});

if (canSubmit) {
  await page.evaluate(() => {
    Array.from(document.querySelectorAll('button'))
      .find(b => b.textContent.includes('Enter edit'))?.click();
  });
  await page.waitForTimeout(15000);

  const mbid = page.url().match(/release\/([a-f0-9-]{36})/)?.[1];
  console.log('Release MBID:', mbid);
}

await browser.close();
```

---

## Step 4: Upload Cover Art

**Run as a separate script after the release exists.**

```javascript
// ... browser launch + login (Step 1) ...

// Download cover image locally first (avoids CORS issues in-page)
// Do this via exec before the Playwright script:
//   curl -sL "<spotify-640px-url>" -o /tmp/cover.jpg

await page.goto(
  'https://musicbrainz.org/release/<mbid>/add-cover-art',
  { waitUntil: 'networkidle', timeout: 30000 }
);
await page.waitForTimeout(3000);

// Upload via Playwright's setInputFiles (works with jQuery File Upload)
await page.locator('input[type="file"]').setInputFiles('/tmp/cover.jpg');
await page.waitForTimeout(3000);

// Wait for upload processing — poll until submit button enables
for (let i = 0; i < 15; i++) {
  const enabled = await page.evaluate(() => {
    const btn = document.getElementById('add-cover-art-submit');
    return btn && !btn.disabled;
  });
  if (enabled) break;
  await page.waitForTimeout(2000);
}

// Check "Front" type
await page.evaluate(() => {
  document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
    const label = cb.closest('label')?.textContent || '';
    if (label.includes('Front') && !cb.checked) cb.click();
  });
});

// Submit
await page.locator('#add-cover-art-submit').click();
await page.waitForTimeout(10000);

// Success = redirect to /release/<mbid>/cover-art
console.log('Final URL:', page.url());

await browser.close();
```

### Cover art URL from Spotify
Find the image hash on the album page (prefix `ab67616d00001e02` = 300px). Replace with `ab67616d0000b273` for 640×640:
```
https://i.scdn.co/image/ab67616d0000b273<hash>
```

### Download before upload
Always download the image locally first with `curl`, then use `setInputFiles()`. Do NOT use in-page `fetch()` — it can hit CORS issues and the jQuery uploader's signature flow doesn't reliably trigger.

---

## Lookups (API — no login needed)

```bash
bash scripts/mb_lookup.sh <spotify-url>
```

Returns MB entity ID or "NOT FOUND". For other queries see `references/api.md`.

### Search by name (no Spotify link)

```bash
# Build User-Agent: use bot name + MB username from .credentials.json if available
MB_USER=$(jq -r '.username // empty' ~/.openclaw/skills/musicbrainz/.credentials.json 2>/dev/null || true)
UA="${OPENCLAW_BOT_NAME:-OpenClawBot}/1.0 (${MB_USER:-anonymous}@users.noreply.musicbrainz.org)"

curl -s "https://musicbrainz.org/ws/2/artist/?query=<name>&fmt=json&limit=5" \
  -H "User-Agent: $UA" | jq '.artists[] | {id, name, score}'
```

---

## Scraping Spotify

Use the oembed endpoint to get the artist/album name without a browser:

```bash
curl -s "https://open.spotify.com/oembed?url=<spotify-url>" | jq '.title'
```

For full discography scraping, use Playwright on `/artist/<id>/discography/all` and expand the viewport incrementally until all lazy-loaded content renders (see the expand loop pattern in `references/api.md`).

---

## Progress Reporting (MANDATORY)

**Message the user after EACH discrete operation completes:**
- Artist created → name + MBID + link
- Release submitted → title + MBID + link
- Cover art uploaded → confirmation

Never go silent for more than a few minutes during multi-release work.

---

## Key Facts

- New accounts are "Beginner" — edits queue for 7-day vote
- Digital releases: Packaging=None, Country=[Worldwide], no barcode
- MusicBrainz uses Knockout.js (not React) for forms — native property setters + `dispatchEvent` are required
- `page.selectOption()` only works when the select element is visible in the viewport; use `evaluate` when elements may be hidden behind dialogs
- Seeding docs: https://musicbrainz.org/doc/Development/Seeding/Release_Editor
