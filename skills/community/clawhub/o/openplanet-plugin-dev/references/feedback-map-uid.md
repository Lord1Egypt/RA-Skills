# ManiaPlanet Feedback Page — Map UID Extraction

The ManiaPlanet feedback page at `https://feedback.prod.live.maniaplanet.com/votes/display/{ID}` displays maps with their UIDs embedded in thumbnail image URLs.

## URL Pattern

Thumbnail images follow the format:
```
https://files-v4.live.maniaplanet.com/maps/{hash}/{UID}.jpg
```

The UID is a base64-like string (e.g., `pdHcfgrPuzYKYG84amT6KREpj97`).

## JavaScript Extraction

Run in browser console while on the feedback page to extract all UID-name pairs:

```javascript
(() => {
  const imgs = document.querySelectorAll('img');
  const h6s = document.querySelectorAll('h6');
  const items = [];
  const mapNames = [];
  h6s.forEach(h => {
    const t = h.textContent.trim();
    if (t && t !== 'YES/NO' && t !== '5 STARS')
      mapNames.push(t);
  });
  imgs.forEach(img => {
    const src = img.src || '';
    const m = src.match(/\/maps\/[a-f0-9]+\/([a-zA-Z0-9_\-]+)\.(jpg|png)/);
    if (m) items.push({uid: m[1], name: ''});
  });
  for (let i = 0; i < items.length && i < mapNames.length; i++)
    items[i].name = mapNames[i];
  return JSON.stringify(items);
})()
```

Returns JSON: `[{"uid": "...", "name": "..."}, ...]`

## Notes

- Number of img elements with `/maps/` in src = number of maps on the page.
- Map names are in h6 elements. Skip "YES/NO" and "5 STARS" headers.
- UID order matches map name h6 order.
- UIDs can construct direct thumbnail URLs or lookup maps on other platforms.

### Reference: plugin-cleanup-workflow

