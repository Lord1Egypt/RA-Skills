# Algorithm Profiles

## Selection policy

Inspect the image visually before invoking the script. Recommend a profile and state its advantage, disadvantage, and uncached download size. If the user does not choose, use `default`. Never enable generative face restoration silently.

| Profile | Model | Best use | Advantage | Limitation | Download |
| --- | --- | --- | --- | --- | ---: |
| `default` | high-fidelity-4x | Unknown or mixed images | Balanced and conservative | Does not maximize any one content type | ~32 MB |
| `fast` | upscayl-lite-4x | Preview and batch processing | Fastest and smallest | Less reconstructed detail | ~2.5 MB |
| `photo` | remacri-4x | Natural photographs | Smooth tonal transitions and natural texture | Softer than `sharp` on hard edges | ~32 MB |
| `portrait` | remacri-4x | Noisy, compressed, or rough natural portraits | Avoids generative face replacement and smooths transitions | Can remove skin and eyelash detail from clean AI portraits | Shared with `photo` |
| `digital-art` | digital-art-4x | Anime, illustration, icons | Clean synthetic edges, compact model | Can flatten photographic texture | ~8.6 MB |
| `sharp` | ultrasharp-4x | Architecture, products, game assets | Strongest apparent edge detail | Can amplify noise, halos, pores, and text artifacts | ~32 MB |

`auto` means the agent selects a profile after visual inspection. The standalone CLI has no bundled vision classifier; it uses explicit filename hints for digital art and otherwise falls back to `default`.

Do not route by subject alone. A same-size comparison on a clean AI portrait showed that `default` retained more eyelashes, eyebrows, and skin texture, while `portrait` produced smoother skin and a smaller output. Route clean AI and studio portraits to `default`; reserve `portrait` for degraded natural portraits.

## 8K behavior

The bundled models produce a native 4× result. Exact 1K/2K/4K/8K presets then resize that result to the requested long edge. If the requested 8K dimensions exceed native 4× output, the extra pixels are interpolation rather than newly recovered factual detail. Prefer a clearly labeled comparison crop when evaluating results.

## Heavy optional algorithms

Do not install these by default:

- SwinIR or HAT: transformer restoration with stronger benchmark reconstruction, but requires a substantially larger PyTorch environment and slower inference.
- CodeFormer or GFPGAN: face restoration that can improve damaged portraits, but may change identity. Require explicit user consent and expose fidelity controls.
- SUPIR: diffusion restoration with strong perceived detail, but high GPU-memory use, slow inference, generative hallucination risk, and non-commercial-use restrictions in the upstream project.

Keep heavy algorithms in separate optional adapters and report their complete environment, model, temporary-file, and output storage costs before installation.
