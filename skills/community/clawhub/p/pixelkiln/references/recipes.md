# Versioned recipes

Use a recipe when it matches the requested provider and asset family. Inspect
it before installation and prefer an exact version selector in a committed
project.

```bash
pixelkiln recipe inspect comfyui/pixel-art-xl-environment@1.0.0
pixelkiln recipe install comfyui/pixel-art-xl-environment@1.0.0
pixelkiln recipe verify \
  pixelkiln-recipes/comfyui/pixel-art-xl-environment/1.0.0
```

For a square image-to-image revision, use
`comfyui/pixel-art-xl-img2img@1.0.0` and read [Controlled revisions](revisions.md).
Its graph and binding contract are tested; its visual quality still needs a
broader benchmark. The first live fortress smoke preserved shape but missed
the requested winter treatment and lost alpha.

If the ComfyUI model root is known, pass it to `recipe verify`. Report missing
or mismatched models; do not download or replace them without the user's
request. Without `--model-root`, say that the recipe and workflow were verified
but workstation models remain unchecked.

Use the style entry printed by `recipe install`. Do not remove its versioned
workflow path, change a model or workflow silently, or call a
`composition-source` recipe production-ready. After an upgrade, compare the new
quality contract and run representative prompts before changing the manifest.

Recipe installation refuses locally changed declared files. Inspect those
changes before considering `--force`. Recipe commands are offline and do not
authorize generation.
