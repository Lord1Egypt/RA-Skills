# Request Schema

The Unity worker consumes one JSON request file.

Example:

```json
{
  "haunt_id": 1,
  "collateral": "ETH",
  "eye_shape": "Mythical",
  "eye_color": "High",
  "skin_id": 0,
  "background": "#806AFB",
  "pose": "idle",
  "wearables": {
    "body": 0,
    "face": 0,
    "eyes": 0,
    "head": 56,
    "pet": 0,
    "hand_left": 0,
    "hand_right": 58
  },
  "output": {
    "slug": "custom-gotchi",
    "full_png": "/absolute/path/to/full.png",
    "headshot_png": "/absolute/path/to/headshot.png",
    "manifest_json": "/absolute/path/to/manifest.json"
  }
}
```

Notes:

- wearable values are numeric wearable IDs
- `0` means empty slot
- output paths should be absolute when possible
- `background` can be a hex color like `#806AFB` or `transparent`
