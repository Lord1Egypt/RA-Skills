# Video Models

## Model ID Table

Use exact `model_id` values for the active task type.

| Friendly name | text-to-video | image-based video | Notes |
| --- | --- | --- | --- |
| Wan 2.6 | `wan2.6-t2v` | `wan2.6-i2v` | task-type-specific suffix |
| Seedance 2.0 | `ima-pro` | `ima-pro` | requires subscription |
| Seedance 2.0 Fast | `ima-pro-fast` | `ima-pro-fast` | no subscription required |
| Kling O1 | `kling-video-o1` | `kling-video-o1` | same ID across current video modes |
| Kling 2.6 | `kling-v2-6` | `kling-v2-6` | same ID across current video modes |
| Hailuo 2.3 | `MiniMax-Hailuo-2.3` | `MiniMax-Hailuo-2.3` | exact casing matters |
| Hailuo 2.0 | `MiniMax-Hailuo-02` | `MiniMax-Hailuo-02` | `02`, not `2.0` |
| Vidu Q2 | `viduq2` | `viduq2-pro` | image path can differ |
| Google Veo 3.1 | `veo-3.1-generate-preview` | `veo-3.1-generate-preview` | exact suffix matters |
| Sora 2 Pro | `sora-2-pro` | `sora-2-pro` | same ID across current video modes |
| Pixverse | `pixverse` | `pixverse` | version distinguished by product leaf / params |
| SeeDance 1.5 Pro | `doubao-seedance-1.5-pro` | `doubao-seedance-1.5-pro` | exact prefix matters |

## Alias Table

The shipped alias canonicalizer currently rewrites only:

| Alias input | Canonical model ID |
| --- | --- |
| `Seedance 2.0` | `ima-pro` |
| `Seedance 2.0-Fast` | `ima-pro-fast` |
| `Seedance 2.0 Fast` | `ima-pro-fast` |
| `Ima Sevio 1.0` | `ima-pro` |
| `Ima Sevio 1.0-Fast` | `ima-pro-fast` |
| `Ima Sevio 1.0 Fast` | `ima-pro-fast` |

`Seedance 2.0` / `Seedance 2.0 Fast` are the canonical operator-facing names in this repo.
`Ima Sevio 1.0` / `Ima Sevio 1.0 Fast` are treated as legacy-compatible aliases.

## Subscription Notes

- `Seedance 2.0` (`ima-pro`) requires subscription.
- `Seedance 2.0 Fast` (`ima-pro-fast`) does not require subscription.
