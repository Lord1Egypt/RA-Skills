# HTML format for html-to-any

## Temporary-file policy

Create working HTML only inside the private OS temporary directory returned by `presenton_artifacts.py create-temp`. Never write generated HTML or exported PPTX, PDF, PNG, or ZIP files into the workspace, repository, home directory, or another persistent location. Submit the temporary HTML to the API and return the response URL without downloading it. After all requested exports complete—or after errors, exhausted retries, or interruption—run `presenton_artifacts.py cleanup-temp --path <exact-created-path>` in a `finally`-equivalent step. The helper refuses to remove the OS temporary root, symlinks, and directories it did not create.

When the entire workflow lives inside one Python process, `tempfile.TemporaryDirectory(prefix="presenton-")` is the preferred equivalent because its context manager performs the same cleanup automatically.

## Required document structure

Submit a complete HTML document. It must contain exactly one wrapper with the required ID, and every direct element child becomes one slide/page:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  </head>
  <body class="m-0 p-0">
    <main id="presentation-slides-wrapper" class="m-0 w-[1280px] p-0">
      <section class="relative h-[720px] w-[1280px] overflow-hidden" data-speaker-note="Optional note">...</section>
      <section class="relative h-[720px] w-[1280px] overflow-hidden">...</section>
    </main>
  </body>
</html>
```

Do not wrap slides in another container inside `#presentation-slides-wrapper`. A nested group counts as one slide because only direct children are exported.

## Dimensions and pagination

- Make every slide exactly 1280×720 px (16:9).
- Use `h-[720px] w-[1280px] overflow-hidden` on every slide and resolve overflow before export.
- Keep the wrapper at 1280 px wide and remove default document margins.
- Do not add margins or gaps between direct slide elements.
- Presenton injects print rules that page-break after each direct child for PDF and PNG generation.

## Tailwind styling

- Load Tailwind with `<script src="https://cdn.tailwindcss.com"></script>` in `<head>`.
- Express all visual styling with Tailwind utility classes, including arbitrary pixel values when required.
- Do not use inline `style` attributes or embedded `<style>` blocks.
- Keep the CDN script in the submitted HTML; the exporter waits for Tailwind to finish applying styles.

## Assets and fonts

- Use complete inline SVG only for non-chart, non-icon artwork.
- Use absolute HTTPS URLs for images, icons, and fonts. Never use `data:` URLs or base64 assets. Local and relative filesystem paths are not reachable by the exporter.
- Before writing HTML, upload every user-provided image with `presenton_artifacts.py upload-image --file <image-path>` and use the returned HTTPS URL in an `<img>` element. Upload each file once and reuse its returned URL.
- Search every icon with `presenton_artifacts.py search-icons --query <concept>`. Choose a returned HTTPS URL and use it in an `<img>` element. Do not substitute inline SVG, emoji, Unicode glyphs, icon fonts, or CSS-drawn shapes for icons.
- If the resolved user-provided or searched design names a font family, use that exact family in the slide markup and import its matching font resource in `<head>`. Do not replace it merely because another font is easier to load. If the exact font has no exporter-reachable source, do not substitute silently: tell the user which font is unavailable and obtain their approval before using a fallback.
- When using a non-system font, add its matching absolute HTTPS stylesheet `<link>` in `<head>` before using the font in slide markup. A font-family name without a head import is invalid for this workflow. Generic/system fallback families do not need an import.
- Include meaningful `alt` text on images.
- Use common fallback fonts. Web fonts may be used, but the exporter can only preserve what loads before stabilization and what the target format supports.
- Ensure every image has explicit dimensions and a deliberate `object-fit` value.

## Chart.js charts

- Use Chart.js for every data chart; do not hand-build charts with HTML, CSS, or SVG.
- Load it with `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>` in `<head>` whenever a chart is present.
- Give every canvas a unique ID and fixed `width` and `height` attributes.
- Initialize each canvas directly with `document.querySelector("#chart-unique-id")` and one `new Chart(...)` call.
- Set `responsive: false` and `animation: false` so the exporter sees a stable chart.
- Use the selected design's palette, typography, grid, and labeling rules in Chart.js options.
- Do not use delayed timers, loops over canvas classes, or interaction-dependent rendering.

## PPTX compatibility

Presenton reads the rendered DOM and computed styles to create PPTX elements. For the most editable result:

- Keep text as HTML text elements rather than baking it into images.
- Prefer Tailwind solid fills, borders, simple gradients, flexbox, grid, positioned boxes, `<img>`, and simple SVG.
- Avoid CSS filters, backdrop filters, masks, unusual blend modes, video, and animation.
- Chart.js canvases may be captured as screenshots and may not remain editable in PPTX.
- Avoid content that depends on interaction, hover state, delayed timers, or user input.

## Speaker notes

When notes are requested, place exactly one `data-speaker-note` attribute on each slide element and escape quotes correctly. Do not add separate note elements elsewhere in the wrapper; the exporter collects every matching attribute in DOM order.

## Applying a user-provided or searched design

Inspect the user prompt before searching. A concrete user-provided design brief—such as explicit palette, typography, layout, aesthetic, brand, imagery, or composition requirements—is the visual source of truth. Do not search designs in that case, and do not send a `design_id` during export.

If the user prompt does not contain a concrete design brief, search designs and select one automatically unless the options require a human preference. If human input is needed, present concise options with their titles, descriptions, and IDs and wait for the user's selection. For a searched design, use its title and description; for a user-provided brief, use the brief itself. Translate the resolved visual brief into a small design system before writing slides:

- background and surface colors
- text and accent colors with accessible contrast
- title, body, and numeric type scale
- spacing unit and safe content bounds
- corner, border, and shadow language
- image treatment and chart palette

Apply the resolved system consistently, but choose a content-appropriate layout per slide and generate the complete document from scratch. Do not use a reference presentation HTML or template. Pass a searched design's `id` as the optional `design_id` field when exporting; omit it when the visual brief came from the user.

## Preflight checklist

- Complete document with `<html>`, `<head>`, and `<body>`
- Tailwind CDN script present
- Exactly one `#presentation-slides-wrapper`
- At least one direct element child
- 1280×720 dimensions present and applied to every slide
- No overflow, clipping, accidental scrollbars, or off-canvas text
- No relative/local asset URLs
- No `data:` URLs or base64-embedded assets
- Every user-provided image uses the URL returned by the public image-upload endpoint
- Every icon uses a URL returned by the icon-search endpoint
- Every font family named by the resolved design is used exactly, or the user explicitly approved the reported fallback
- Custom fonts used by slide markup are imported or linked from `<head>`
- No inline `style` attributes or embedded `<style>` blocks
- Chart.js CDN, unique fixed-size canvas IDs, and non-animated initialization present for every chart
- Same final HTML used for PPTX, PDF, and PNG exports
- Final response includes the selected design/reference inputs, presentation details, exact font inventory, and one download URL per requested format
- Export only the formats requested by the user; when no format is specified, export PPTX, PDF, and PNG
