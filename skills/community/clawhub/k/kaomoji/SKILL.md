---
name: kaomoji
description: Light kaomoji selector based on context tags.
---

# Kaomoji

A fast and simple tool to select or store kaomojis.

## Pick a kaomoji

```bash
python pick_kaomoji.py <tag1> <tag2> ...
```

Example:
```bash
python pick_kaomoji.py encouragement positive
```

Example output: `(๑•̀ㅂ•́)و✧`

## List all kaomojis

```bash
python list_kaomojis.py
```

Save a new kaomoji

### Save a new kaomoji

Add a new kaomoji with metadata.

```bash
python save_kaomoji.py "<kaomoji>" "<meaning>" "<usage_tags>" "<tone_tags>"
```

Example:
```bash
python save_kaomoji.py "(๑•̀ㅂ•́)و✧" "cheering, encouragement, energetic" "encouragement,celebrating progress,casual chat,greeting" "positive,playful,cute"
```

