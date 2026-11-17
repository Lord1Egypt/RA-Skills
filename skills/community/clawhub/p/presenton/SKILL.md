---
name: presenton
description: "Skill for creating new PPTX, PDF, and PNG files with Presenton. Use this skill whenever a user asks for a PowerPoint, presentation, slide deck, pitch deck, report deck, PDF, presentation PDF, PNG slide, slide image, or exported deck, even when Presenton is not mentioned. Use a concrete design brief from the user when provided; otherwise search Presenton designs, upload user-provided images, search Presenton icons, generate 1280x720 HTML with HTTPS asset URLs, export requested formats—or all three formats when none is specified—and return download URLs plus a shareable presentation-preview link."
---

# Create PPTX, PDF, and PNG Files with Presenton

Use Presenton's design search when a user-provided design brief is absent, then use its HTML exporter instead of constructing binary formats directly.

## Operating constraints

- Read [references/api.md](references/api.md) before making API calls and [references/html-format.md](references/html-format.md) before writing HTML.
- Use the public `https://api.presenton.ai` endpoints through the provided helper; no API key or authorization header is required.
- Follow the design-resolution, export, reporting, and cleanup workflow below. Print concise status updates throughout, including periodic heartbeats during long waits.
- Treat every non-empty `message` in a successful design-search, export, or preview-creation response as user-facing. Relay it verbatim in the next commentary update and include it in the final response's `Notes`.

## Creation workflow

1. Determine the requested formats, title, audience, purpose, slide count, and content. If no format is named, export PPTX, PDF, and PNG. Make reasonable content assumptions when details are absent.
2. Resolve the visual direction from the user prompt. A concrete design brief (palette, typography, layout, aesthetic, brand, imagery, or composition) is used directly and skips search. Otherwise search designs, ask the user to choose only when the options require a human preference, or select the best result automatically. Retain the searched design ID for export.
3. Resolve slide assets before writing HTML:

   - For every user-provided image that will appear in the presentation, upload the file exactly once and retain the returned HTTPS URL. Reuse that URL wherever the image appears. Never embed image bytes, base64, or any `data:` URL in the HTML.

     ```bash
     python3 scripts/presenton_artifacts.py upload-image --file <image-path>
     ```

   - For every icon concept used in the presentation, search Presenton's icon endpoint and choose a returned HTTPS URL that matches the concept and visual weight. Use `--icon-type` to match the design. Do not draw, inline, or invent substitute icons with SVG, emoji, Unicode glyphs, icon fonts, or CSS shapes.

     ```bash
     python3 scripts/presenton_artifacts.py search-icons \
       --query "revenue growth" \
       --limit 5 \
       --icon-type thin
     ```

4. Translate the resolved brief into design rules, then create a private OS temporary directory with `presenton_artifacts.py create-temp` and write the complete HTML document from scratch at `<temporary-directory>/presentation.html`. Follow [references/html-format.md](references/html-format.md) for dimensions, Tailwind, charts, fonts, assets, and PPTX compatibility. Use the retained HTTPS image and icon URLs in `<img>` elements. Do not copy a reference presentation or store HTML in the workspace.
5. Confirm the HTML reflects the resolved design, has direct 1280×720 slide children under `#presentation-slides-wrapper`, contains no `data:` URLs, and passes the preflight validator:

   ```bash
   python3 scripts/validate_html.py "$presenton_temp_dir/presentation.html"
   ```

   The validator also checks that custom fonts used by slide markup have a matching import in the document head.

6. Export each requested format exactly once, separately. The endpoint accepts only one `format` per call. Add `--design-id` only when the visual brief came from a searched design; omit it for user-provided design briefs:

   ```bash
   presenton_temp_dir=$(python3 scripts/presenton_artifacts.py create-temp)
   # Generate fresh HTML at "$presenton_temp_dir/presentation.html", then export it.
   python3 scripts/presenton_artifacts.py export \
     --html "$presenton_temp_dir/presentation.html" \
     --format pptx \
     --title "Presentation title" \
     --json
   ```

7. Capture the positive integer `id` and HTTP or HTTPS `url` from each JSON object printed by the helper. Return every `url` as a clickable download link. The helper writes any response `message` to stderr as `API message: ...`; retain every such message for user reporting. Do not download or save exported files locally.
8. After every requested format for one presentation succeeds, create exactly one shareable preview using any one of that presentation's retained export creation IDs:

    ```bash
    python3 scripts/presenton_artifacts.py create-preview --id <creation-id>
    ```

    Capture the HTTP or HTTPS URL printed by the helper and return it as the presentation's clickable shareable-preview link. The preview link expires after 24 hours. When creating multiple distinct presentations, repeat this once for each presentation; do not create a separate preview for each format of the same presentation.
9. After all requested exports and the preview link succeed, list the fonts from the exact final HTML before cleanup:

    ```bash
    python3 scripts/presenton_artifacts.py list-fonts \
      --html "$presenton_temp_dir/presentation.html"
    ```

    Include the resulting font names in the final response, along with any web-font source URLs when present. State that the inventory applies to every requested PPTX, PDF, and PNG export from that HTML.
10. Return the result using this format:

    ```text
    Presentation
    - Title: <title>
    - Formats: <requested formats, or PPTX, PDF, and PNG when none was specified>
    - Slides: <slide count>
    - Design/reference used: <user-provided design brief, or searched design title and id>
    - References/assets used: <source URLs, user-provided references, image sources, or "None">
    - Notes: <every API response message verbatim, followed by other useful details; or "None">

    Shareable preview
    - [View presentation](<preview_url>) — expires after 24 hours

    Fonts
    - <font name> — <source URL when applicable>

    Download URLs
    - PPTX: [Download](<url>)
    - PDF: [Download](<url>)
    - PNG: [Download](<url>)
    ```

    Include only requested formats in `Download URLs`; when no format was specified, include PPTX, PDF, and PNG. Do not invent references, font sources, or URLs; use `None` when there is nothing to report.

11. In a `finally`-equivalent step that runs after success, exhausted retries, errors, or interruption, clean up the exact temporary directory:

   ```bash
   python3 scripts/presenton_artifacts.py cleanup-temp \
     --path "$presenton_temp_dir"
   ```

   Keep the directory only while active retries or additional requested formats still need the same HTML. Do not rely on eventual OS cleanup, and never delete the OS temporary root or any directory not created by `create-temp`.

Use the helper for design search:

```bash
python3 scripts/presenton_artifacts.py search-designs \
  --query "executive cybersecurity review, restrained dark blue, data-led"
```

If the helper cannot be used, follow the equivalent cURL contracts in [references/api.md](references/api.md).

## Quality rules

- Use the resolved visual direction consistently across all slides: palette, typography, spacing, imagery, and shape language.
- When the resolved design names a font family, use that exact font family in the presentation; do not silently substitute another font.
- Preserve recognizable details from the user-provided design brief or selected searched-design description; do not merely mention the design in notes or metadata.
- Vary layouts to fit the content while preserving a coherent system.
- Keep text readable at presentation distance and prevent all overflow.
- Use uploaded HTTPS URLs for every user-provided image and searched HTTPS URLs for every icon. Never use `data:` URLs or base64 assets in HTML.
- Keep text as HTML text for PPTX editability and use charts only for actual data visualizations.
- Add one `data-speaker-note` attribute per slide only when notes are requested.
- Export from the same final HTML for every requested format so the outputs match.

## Failure handling

- On `404`, confirm that the public v3 designs/export routes have been deployed; do not guess a legacy replacement route.
- On `400` wrapper/slide errors, re-run the validator and compare the HTML with the structural contract in [references/html-format.md](references/html-format.md).
- On `422`, correct the request shape or field limits.
- On `502`, keep the HTML only while retrying. After retries finish, run `cleanup-temp` before reporting failure. Never copy it to persistent storage.
- Do not claim success unless every requested export response contains a valid positive creation ID and HTTP or HTTPS URL, and every distinct presentation has a valid HTTP or HTTPS shareable-preview URL.
