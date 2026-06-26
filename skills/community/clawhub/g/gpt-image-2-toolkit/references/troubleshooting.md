Use this file only when you need extra detail while working with the HNBC skill.

## Fast failure map

### 1. `No image-generation provider registered for hnbc`
Most likely causes:
- plugin is neither available under `~/.openclaw/extensions/hnbc` nor bundled under `/usr/lib/node_modules/openclaw/dist/extensions/hnbc`
- running gateway has not reloaded after plugin install
- tool-side runtime is still using an older provider registry

### 2. `hnbc generate does not support resolution overrides`
Cause:
- request passed `resolution`

Fix:
- remove `resolution`
- use only supported `size` or `aspectRatio`

### 3. HNBC visible in local runtime, invisible in `image_generate list`
Interpretation:
- disk files and plugin load path are fine
- running gateway likely needs restart

### 4. `HNBC API key missing`
Check one of:
- env: `HNBC_API_KEY`
- config: `models.providers.hnbc.apiKey`
- auth profile for provider `hnbc`

## Supported request geometry
- sizes:
  - `1024x1024`
  - `1024x1536`
  - `1536x1024`
- aspect ratios:
  - `1:1`
  - `2:3`
  - `3:2`
- edit mode: unsupported
