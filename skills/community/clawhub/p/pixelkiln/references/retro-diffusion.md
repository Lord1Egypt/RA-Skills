# Retro Diffusion

Read this reference when a manifest selects `retrodiffusion`, when evaluating
large scene work, or when using native animation and tileset output.

## Operational boundary

- Credential: `RD_API_KEY` in `.env.local` beside the manifest or in the
  process environment. Never print or commit it.
- Status: experimental adapter. RD Fast and RD Plus single-candidate stills are
  live-tested through quote, submit, download, provenance, and recovery.
  Multi-candidate, tileset, GIF, and spritesheet paths remain mock-tested.
- Cost unit: USD. PixelKiln enforces the offline plan, then checks Retro
  Diffusion's free authoritative quote before submission.
- Account operations: balance is supported. Listing, adopt, salvage, tagging,
  and deletion are not exposed by the current adapter.
- Recovery identity: the lock stores a durable `retrodiffusion://` reference,
  never a temporary signed storage URL or inline image. Do not replace that
  reference with the current download URL. Recovery uses the local content
  cache first and needs `RD_API_KEY` to refresh a missing result.

## When to use it

- `rd_plus__environment` for one-point-perspective scenic backgrounds.
- `rd_plus__topdown_map` for 3/4 top-down maps.
- `rd_tile__scene_object` for 64–384px objects placed on tile maps.
- `rd_plus__topdown_asset` or `rd_plus__isometric_asset` for isolated assets.
- `rd_animation__*` and `rd_advanced_animation__*` for GIF or PNG spritesheet
  output.

The useful environment styles currently top out at 384×384. PixelLab's `map`
route reaches 400×400, so Retro Diffusion is not the higher-resolution option
through PixelKiln today. Choose it for its scene styles, cleaner transparent
cutouts, smaller palettes, cinematic framing, or native animation. Build truly
large scenes from separately generated terrain, backdrop, landmark, building,
and foreground layers, then integer-upscale with nearest-neighbor filtering.

The committed 384px benchmark produced larger isometric
buildings than the earlier 256px brief while retaining 52% to 75%
transparency and 49 to 55 colors. Its volcanic backgrounds made the pass and
lava path clear, but dropped a requested fortress and favored close canyon
framing over separable distant planes. Use a representative large asset before
assuming prompt details or layerability will survive a batch.

For setup, selectors, and option constraints, use
<https://pixelkiln.griffen.codes/docs/retro-diffusion>. The matched visual
evidence is at <https://pixelkiln.griffen.codes/docs/provider-benchmark>. When
working in the PixelKiln repository, the same canonical sources are
`docs/RETRO_DIFFUSION.md` and `docs/PROVIDER_BENCHMARK.md`. The provider sources
are <https://www.retrodiffusion.ai/> and
<https://www.retrodiffusion.ai/app/guide/api>.
