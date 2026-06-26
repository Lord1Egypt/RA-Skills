# Input Schema

Canonical payload example:

```json
{
  "haunt_id": 1,
  "collateral": "ETH",
  "eye_shape": "Mythical",
  "eye_color": "High",
  "skin_id": 0,
  "wearables": {
    "body": 0,
    "face": 0,
    "eyes": 0,
    "head": 56,
    "pet": 0,
    "hand_left": 0,
    "hand_right": 58
  },
  "background": "#806AFB",
  "pose": "idle",
  "output": {
    "slug": "eth-mythical-custom",
    "full_png": "/tmp/openclaw/custom-gotchi-eth-mythical-custom-full.png",
    "headshot_png": "/tmp/openclaw/custom-gotchi-eth-mythical-custom-headshot.png",
    "manifest_json": "/tmp/openclaw/custom-gotchi-eth-mythical-custom-manifest.json"
  }
}
```

## Notes

- Wearable IDs default to `0` when empty.
- `pose` is reserved for later animation and turntable support.
- `background` can be a hex value or `transparent`.
- MVP validation checks structure and integer slot IDs first.
- A later pass should validate that requested wearables actually exist in the installed Unity SDK asset set.
