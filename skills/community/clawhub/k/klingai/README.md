# Kling AI

Video generation, image generation, and subject management.

- **Command**: `node scripts/kling.mjs <video|image|element|voice|account> [options]`
- **Subcommands**:
  - `video`: video generation (text-to-video, image-to-video, omni-video, multi-shot)
  - `image`: image generation (text-to-image, image-to-image, omni-image, 4K/series)
  - `element`: subject CRUD
  - `voice`: voice library CRUD (public URL or video_id; not a local file)
  - `account`: quota query and credential bind/import
- Choose by user intent; if ambiguous, ask the user first.

See [SKILL.md](SKILL.md) for full routing/parameters and [reference.md](reference.md) for endpoint mapping.
Official docs: [CN](https://app.klingai.com/cn/dev/document-api) / [Global](https://kling.ai/document-api/quickStart/productIntroduction/overview).
