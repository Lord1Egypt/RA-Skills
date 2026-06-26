# Natural Language Intent Mapping (Retouch)

Objective: Map overseas user prompts for "Ghost Mannequin" or "Cleanup" into technical parameters.

| User Input (Natural Language) | Target Technical Parameter | Purpose (Logic) |
| :--- | :--- | :--- |
| **"Remove the ghost mannequin"** | `model_version: "v2.0"`, `correction_intensity: "high"` | Enable maximum reconstruction for dense occlusions. |
| **"Make it look natural, not over-processed"** | `correction_intensity: "low"` | Preserve subtle shadows and lighting for realist look. |
| **"High res for my Shopify store"** | `resolution: "2K"`, `model_version: "v2.0"` | Standard web-high resolution. |
| **"Remove the background tourists"** | `target_task: "passerby-removal"` | Switch to passerby-specific logic. |

## Rules
1. **Background Complexity**: If the background is very busy, default `correction_intensity` to "medium" or "high".
2. **Model Limitation**: 2K/4K resolution is only available in `v2.0` model.
