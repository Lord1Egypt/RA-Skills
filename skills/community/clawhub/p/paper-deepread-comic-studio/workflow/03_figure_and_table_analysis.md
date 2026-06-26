# Step 3: Figure And Table Analysis

For important architecture or model figures, extract:

- purpose
- layout
- block inventory
- flow logic
- figure-to-claim mapping
- what remains unclear or potentially misleading
- reusable design blueprint
- text-to-image prompt blueprint
- multi-image storyboard split plan: which claims belong in separate images rather than one compressed image
- camera/style/logic continuity plan for later continuous cartoon generation
- source-grounding check for every paper-specific visual element

If a LaTeX source is available, also inspect figure environments, captions, labels, nearby explanatory text, and included image paths. Reconstruct the role of important figures even when rendered page images are unavailable. Do not silently skip figures just because the source is `.tex`.

If a PDF source is available, explicitly interpret important figures from the rendered pages as well. Do not stop at saying that a figure exists. Explain the visual structure, how the arrows/blocks/curves should be read, which claim the figure supports, and what remains ambiguous, visually weak, or possibly misleading.

For important tables and charts, extract:

- what question the visual answers
- what the axes / legends / compared conditions mean when applicable
- which claim the table/chart is supposed to support
- whether the data really supports that claim, only partially supports it, or conflicts with it
- likely reasons for any mismatch, anomaly, or controversy
- why the layout is persuasive or potentially misleading
- what can be borrowed later

If page images, LaTeX figure metadata, or visual manifests are missing, return to Step 1 and request them.
