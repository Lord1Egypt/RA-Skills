# Pixmind image model routing

Use this routing order only when the user has not selected a model. An explicit model choice always wins.

## Preferred models

| Task | First choice | Why | Next choice |
| --- | --- | --- | --- |
| General text-to-image | `gpt-image-2` | Strong instruction following and reliable composition | `seedream-5.0-pro` |
| Text, poster, card, infographic, UI mockup | `gpt-image-2` | Best fit for readable text and structured layouts | `nano-banana-pro` |
| Reference edit, identity, product consistency | `nano-banana-pro` | Strong reference understanding and iterative editing | `gpt-image-2` |
| Cinematic photo, commercial key visual, material and lighting | `seedream-5.0-pro` | Polished realism and Asian commercial aesthetics | `gpt-image-2` |
| Chinese cultural or lifestyle scene | `seedream-5.0-pro` | Strong Chinese scene understanding | `nano-banana-pro` |
| Complex edit with many precise instructions | `gpt-image-2` | Strong constraint following | `nano-banana-pro` |

## Compatibility fallback

`seedream-4.5` is a compatibility model, not the default. Select it only when the user requests it or the preferred models are absent from the live catalog before a task is submitted.

Never retry a failed paid generation on another model automatically. Report the failure and obtain approval for a new task.
