# Google Visual And Video Module Rules

## 1. Module Scope

Use this module for Google images, Lens visual search, and videos.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Images and Lens
3. Videos

## 2. Images and Lens

- Documentation: `https://docs.keyapi.ai/en/google/images.md`
- Documentation: `https://docs.keyapi.ai/en/google/lens.md`
- Purpose: Retrieve image search results or visually similar Lens results.

### Best Suited For

- image research
- reverse-image-style lookup
- visual product/source discovery

### Routing Rules

- Use images for text-query image search.
- Use Lens when the starting point is an image URL or visual lookup.
- Extract selected result pages only when deeper source content is required.

## 3. Videos

- Documentation: `https://docs.keyapi.ai/en/google/videos.md`
- Purpose: Retrieve Google video search results.

### Best Suited For

- video result collection
- topic video research
- source discovery through video results

### Routing Rules

- Use for video results, not YouTube-specific channel/video details.
- Route selected webpages through webpage extraction if page content is needed.

## 4. Common Workflows

- Visual workflow: images or Lens -> selected result -> webpage extraction if needed.
- Video workflow: videos -> selected URL/page extraction if needed.
