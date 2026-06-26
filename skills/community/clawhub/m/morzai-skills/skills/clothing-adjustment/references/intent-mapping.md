# Natural Language Intent Mapping (Adjustment)

Map clothing-cleanup intents into one approved whole-garment preset direction.

| User Input (Natural Language) | Recommended Preset Direction | Purpose (Logic) |
| :--- | :--- | :--- |
| **"Iron this perfectly, no creases"** | `strong_flattening` | Use the strongest available whole-image wrinkle-cleanup preset. |
| **"Clean up the lint and pet hair"** | `surface_cleanup` | Prefer a preset that emphasizes overall surface cleanup. |
| **"Make it look cleaner and flatter overall"** | `balanced_cleanup` | Use a balanced preset that improves both wrinkles and overall neatness. |
| **"Just a quick touch-up for minor wrinkles"** | `light_cleanup` | Use the lightest available whole-image cleanup preset. |
| **"Make it look structured"** | `balanced_cleanup` or `strong_flattening` | Choose the nearest whole-image preset based on how aggressive the user wants the result to be. |
| **"Only smooth the sleeves"** | `unsupported -> confirm fallback` | Current support is not part-level; ask whether the user accepts a whole-garment cleanup preset instead. |
| **"Protect the buttons and zippers"** | `unsupported explicit switch -> confirm fallback` | Current support has no separate protection switch; confirm whether to proceed with a whole-garment preset. |

## Recognition Rules
1. **Preset-Level Only**: Current support is one whole-garment preset per request, not separate wrinkle / blemish / edge sliders.
2. **No Part Masks**: If the user asks for collar-only, sleeve-only, or local-area adjustment, explain the limitation and ask whether whole-image cleanup is acceptable.
3. **No Separate Protection Toggle**: Do not promise `objects_protection` or similar fine-grained switches unless the runtime actually adds them later.
4. **Compress Mixed Requests**: If the user asks for multiple detailed operations at once, compress them into the nearest approved preset direction and confirm before execution.
