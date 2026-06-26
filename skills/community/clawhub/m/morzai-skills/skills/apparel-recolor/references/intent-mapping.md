# Natural Language Intent Mapping (Recolor)

This reference document defines the technical mapping logic from common user prompts to API parameters.

| User Input (Natural Language) | Target Technical Parameter | Purpose (Logic) |
| :--- | :--- | :--- |
| **"Recolor the shirt only"** | `target_parts: ['upper_body']` | Limit recolor scope to the requested garment part. |
| **"Make it look like the sample"** | `extract_color -> confirm hex_color` | Extract a candidate color from the sample first, then recolor with the confirmed target color. |
| **"Match the dress to the first image"** | `extract_color -> confirm hex_color`, `target_parts: ['full_body']` | Use sample-assisted color picking, then apply it to the full garment. |
| **"Don't touch my logo/stripes"** | `pattern_behavior: keep` | Keep existing logos, stripes, and printed patterns unchanged. |
| **"Recolor the logo/print too"** | `pattern_behavior: recolor` | Recolor printed elements together with the garment. |
| **"Remove the printed text/pattern while recoloring"** | `pattern_behavior: remove` | Remove printed pattern/text during the recolor workflow. |
| **"I need 4K resolution for my store"** | `model: "pro"`, `output_mode: "4k"` | Enable high-resolution output via the pro model. |
| **"Recolor the hat and the scarf"** | `target_parts: ['hat', 'scarf']` | Apply one recolor request to multiple garment parts. |
| **"Make it slightly darker"** | `confirm a darker hex_color before execution` | Current runtime changes the target color, not a separate brightness slider. |

## Recognition Rules
1. **Multi-Selection**: If the user mentions multiple garments (e.g., "pants and socks"), include every requested part in `target_parts`.
2. **Sample-Assisted Flow**: If the user mentions a reference/sample photo, do not assume direct reference recolor. Extract a candidate color first and ask for confirmation.
3. **Pattern / Logo Handling**: If the prompt mentions logo, print, text, or stripes, always choose and confirm one explicit `pattern_behavior`: `keep`, `recolor`, or `remove`.
4. **Model Constraints**: High-res (2K/4K) requests must always switch to the pro model.
