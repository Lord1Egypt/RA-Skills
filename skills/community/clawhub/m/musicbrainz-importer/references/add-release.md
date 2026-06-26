# Adding a Release — Reference

## Form Element IDs

| Field | Element ID | Type | Common Values |
|-------|-----------|------|---------------|
| Title | `name` | input text | Release title |
| Artist | `ac-source-single-artist` | input text (autocomplete) | Artist name or MBID |
| Release group | `release-group` | input text (autocomplete) | Auto-populates from title |
| Primary type | `primary-type` | select | `1`=Album, `2`=Single, `3`=EP |
| Secondary types | `secondary-types` | select-multiple | Compilation, Live, etc. |
| Status | `status` | select | `1`=Official |
| Language | `language` | select | `120`=English, `145`=German |
| Script | `script` | select | `28`=Latin, `12`=Cyrillic |
| Year | `event-date-0` | input text | YYYY format, placeholder "YYYY" |
| Month | `.partial-date-month` | input text (class) | MM format |
| Day | `.partial-date-day` | input text (class) | DD format |
| Country | `country-0` | select | `240`=[Worldwide], `81`=Germany |
| Label | `label-0` | input text (autocomplete) | Label name or MBID |
| Catalog number | `catno-0` | input text | |
| Barcode | `barcode` | input text | |
| No barcode checkbox | `no-barcode` | checkbox | |
| Packaging | `packaging` | select | `7`=None |
| Disambiguation | `comment` | input text | |
| Edit note | `edit-note-text` | textarea | |

## Tabs

The release editor uses jQuery UI tabs:

| Tab | Anchor text | Notes |
|-----|------------|-------|
| Release information | `Release information` | Main form fields |
| Release duplicates | `Release duplicates` | Auto-populated, may be disabled |
| Tracklist | `Tracklist` | Medium format, track parser |
| Recordings | `Recordings` | Auto-linked, may be disabled |
| Edit note | `Edit note` | Edit note + submit button |

Switch tabs:
```javascript
Array.from(document.querySelectorAll('.ui-tabs-anchor'))
  .find(t => t.textContent === 'Tracklist')?.click();
```

## Setting Form Values (Knockout.js)

MusicBrainz uses **Knockout.js** (not React). Form values must be set via native property setters to trigger Knockout's data binding:

### Select elements
```javascript
function setSelect(id, value) {
  const el = document.getElementById(id);
  if (!el || el.disabled) return;
  el.value = value;
  el.dispatchEvent(new Event('change', { bubbles: true }));
}
```

### Input elements
```javascript
function setInput(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
  ).set;
  setter.call(el, value);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
}
```

### Textarea elements
```javascript
function setTextarea(id, value) {
  const el = document.getElementById(id);
  if (!el) return;
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, 'value'
  ).set;
  setter.call(el, value);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## Track Parser

The track parser opens in a jQuery UI dialog. There may be **multiple dialogs** open simultaneously (Track parser + Add medium). Always target by title:

```javascript
for (const dialog of document.querySelectorAll('.ui-dialog')) {
  if (dialog.style.display === 'none') continue;
  const title = dialog.querySelector('.ui-dialog-title');
  if (!title?.textContent.includes('Track parser')) continue;
  // ... work with this dialog ...
}
```

### Track text format
```
1. Track Title (M:SS)
2. Another Track (M:SS)
```

### After parsing
- Close the dialog via `.ui-dialog-titlebar-close`
- Check for capitalization warning checkbox ("I confirm these titles are capitalized correctly")
- Verify track count matches expected

## Known Blockers

### Release group autocomplete + "Add medium" dialog
After entering a title and selecting an artist, MusicBrainz auto-searches for matching release groups and may open an "Add medium" dialog. These overlays make all form fields below them **invisible to Playwright** (zero bounding rect, null offsetParent).

**Fix:** Dismiss all blockers before touching any other field:
```javascript
await page.evaluate(() => {
  document.querySelectorAll('ul.ui-autocomplete')
    .forEach(ul => ul.style.display = 'none');
  document.querySelectorAll('.ui-dialog').forEach(d => {
    if (d.style.display !== 'none' && d.offsetParent !== null) {
      d.querySelector('.ui-dialog-titlebar-close')?.click();
    }
  });
  document.activeElement?.blur();
});
```

### `page.selectOption()` fails with "element is not visible"
When dialogs are covering form elements, Playwright's `selectOption()` and `click()` timeout. Use `evaluate()` instead — it operates on the DOM directly regardless of visual occlusion.

## Cover Art Upload

### URL
```
https://musicbrainz.org/release/<mbid>/add-cover-art
```

### Method
Download the image locally first, then use Playwright's `setInputFiles()`:

```javascript
// Before the script:
//   curl -sL "<cover-url>" -o /tmp/cover.jpg

await page.locator('input[type="file"]').setInputFiles('/tmp/cover.jpg');
```

### Spotify cover art URLs
- `ab67616d00001e02<hash>` = 300×300
- `ab67616d0000b273<hash>` = 640×640 (use this one)

### Submit button
- ID: `add-cover-art-submit`
- Starts disabled, enables after upload processing completes
- Poll until enabled, then click

### Duplicate entries
The jQuery uploader sometimes creates two file entries from one upload. Check and remove duplicates before submitting.

## Seeding (Alternative to Manual Form Fill)

POST form data to pre-fill the release editor. See `scripts/seed_release.mjs` for the JSON schema and field mapping.

**Caveat:** Seeding populates DOM values but Knockout.js bindings don't always pick them up. The form may show validation errors ("title required", "artist required") even though the fields appear filled. If seeding fails validation, fall back to the manual form fill approach in SKILL.md Step 3.

Seeding docs: https://musicbrainz.org/doc/Development/Seeding/Release_Editor
