---
name: ootd
description: Your personal AI stylist. Suggests an Outfit Of The Day based on real-time weather and your personal style.
author: heytedward
metadata:
  openclaw:
    emoji: 🧥
    requires:
      skills: ["weather"]
---

# OOTD (Outfit Of The Day)

A smart outfit recommender that adapts to the weather and your specific style profile.

## Usage

```bash
# Check outfit for current location
ootd

# Check outfit for a specific city
ootd "New York"
```

## How It Works

1.  **Weather Analysis:** Fetches current conditions (Temperature, Sky, Wind) using the `weather` skill.
2.  **User Context:** Reads `USER.md` to understand your persona and style preferences (e.g., "Streetwear", "Techwear", "Classic").
3.  **Wardrobe Lookup (Optional):** Checks for a `wardrobe.json` file in the workspace to recommend specific items you own.
4.  **Recommendation:** Generates a natural language suggestion.

## Configuration

### 1. The Digital Wardrobe (Optional)

Create a file named `wardrobe.json` in your workspace (`~/.openclaw/workspace/`) to define your clothes. If this file doesn't exist, the skill will give general advice based on your style.

**Example Format:**
```json
{
  "items": [
    {
      "name": "Heavyweight Hoodie",
      "type": "top",
      "tags": ["heavy", "streetwear", "cotton"],
      "min_temp": 40,
      "max_temp": 65
    },
    {
      "name": "Vintage Denim Jacket",
      "type": "outerwear",
      "tags": ["casual", "layer"],
      "min_temp": 50,
      "max_temp": 65
    }
  ]
}
```

### 2. Style Profile

Ensure your `USER.md` contains a note about your style.
*   *Example:* "I prefer minimalist streetwear and dark colors."

## Output Format

The output is formatted as a clean summary:

*   **Temperature:** [Current Temp]
*   **Sky:** [Condition]
*   **Vibe:** [Short mood description]
*   **Recommendation:** [Conversational advice]
