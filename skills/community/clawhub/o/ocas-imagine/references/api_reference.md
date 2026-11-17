# Generation Routing Reference

## Primary Generation Path: Current Active Model

Image generation must route through the **current active conversation model** when that model is text-to-image capable. For <operator>'s current setup, `ocas-imagine` maps to the active model session rather than to a separate image backend.

Do **not** call any of these as implementation fallbacks unless <operator> explicitly requests that backend:

- `image_generate`
- Pollinations / Pollination
- FAL
- direct provider HTTP endpoints
- ad-hoc scripts that download images from an external image service

## Prompt Contract

1. Retrieve or synthesize the **Style Prompt**.
2. Expand the user's request into a **Content Prompt** containing only scene content.
3. Concatenate Style first, Content second.
4. Submit the combined prompt to the active model as an image-generation request.
5. Record the returned image URL or file path in history, journal, and evidence when a file/URL is produced.

## Current-Model Request Shape

In this setup the active text-to-image path is the **GenTube browser bridge** (gentube.app via
the Hermes browser tool). The concrete execution path:

1. Ensure logged in (see gentube-mcp `references/browser-tool-login.md` — vault fill, not typing).
2. Navigate to `https://www.gentube.app/create` (use a named browser session — it persists across calls).
3. Set aspect ratio: click `aria-label="Change aspect ratio"` → choose `16:9 widescreen`.
4. Fill the `Type to Create ✨` textarea with **Style Prompt first, Content Prompt second**.
5. Click `aria-label="Create"`. Poll for an `<img>` whose `src` starts with `data:image` and
   `naturalWidth > 200` (alt="Generated image").
6. Extract the base64 data URI via `browser_console` (JS returning filtered img srcs), decode,
   resize to exact target with PIL LANCZOS (GenTube's "16:9" renders 1344×768 — always resize).
7. Verify: PIL opens the file, 1600×900, white-bright pixel fraction < 1% (text-leak check).

Use natural-language image output instructions, not a tool call:

```text
Use the current active text-to-image model to generate an image.

Style Prompt:
<full style prompt>

Content Prompt:
<pure scene content>

Output: image file/attachment, square aspect ratio unless the user requested otherwise.
```

## Recommendations

- Keep style instructions in the Style Prompt; keep subject/scene details in the Content Prompt.
- Do not add model/vendor-specific parameters unless the active model interface exposes them directly.
- Do not use hidden external endpoints as a fallback.
- For a series, reuse the exact same Style Prompt across all images and vary only the Content Prompt.
- If the active model cannot emit image bytes/attachments through the current surface, report that as an interface wiring problem; do not route around it.

## Failure Handling

If the active model image path returns an error or is not exposed in the current surface:

- Log `degraded: current_model_t2i_unavailable` in evidence.
- Return the error clearly.
- Do not fall back to `image_generate`, Pollinations/Pollination, FAL, or other direct provider calls.
