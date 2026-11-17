# Local cover rendering

Default to one typographic cover per requested post. Choose colors and copy from
the topic yourself. The user does not need to select a renderer or supply JSON.
Do not turn a cover task into a presentation, install a toolchain, or reverse-
engineer slidep. A PPT-to-image service is unnecessary for a flat PNG cover.

## Preferred route

Use [the bundled renderer](../scripts/render-cover.cjs) with an existing Node
runtime. It loads an already installed `canvas` module through normal resolution
or WorkBuddy's local runtime directories. It does not download packages, upload
content, contact a rendering service, or consume image-generation credits.

Resolve `<skill-root>` from the actual loaded Skill directory and use absolute
paths in tool calls. First run:

```text
node <skill-root>/scripts/render-cover.cjs --check
```

If `node` is absent from PATH on WorkBuddy Windows, list the existing
`%USERPROFILE%\.workbuddy\binaries\node\versions\` directories once and use
an actual `node.exe` there by absolute path. Do not ask the user to find it.
If a native module fails to load under a system Node, try the matching bundled
Node once; retain the original error if it still fails. `--canvas-module` can
select a verified installed module, but must not trigger a package install.

Write a data-only JSON spec yourself, in the user's language, for example:

```json
{
  "label": "HARDWARE BASICS",
  "title": "Connect your development board",
  "subtitle": "Check the cable, driver, and serial settings",
  "points": ["Use a data cable", "Verify the board's pinout", "Match the baud rate"],
  "accent": "#2563EB"
}
```

Then render to a new filename:

```text
node <skill-root>/scripts/render-cover.cjs --input <run-dir>/cover-spec.json --output <run-dir>/covers/cover-01.png
```

`title` is required. Optional fields are `label`, `subtitle`, up to four `points`,
six-digit hex `accent`, and `fontFamily`. Defaults include common Chinese system
fonts. Export is 1080 by 1440. Text is measured and wrapped; excessive text fails
instead of being truncated. The script refuses to overwrite an existing output.
For a justified correction use a revision filename and update `cover-index.md`.

Inspect the actual PNG once for legible Chinese glyphs, wrapping, contrast, and
agreement with the post. Module availability alone does not prove font coverage.
Allow at most two corrections for visible defects. Read a new revision once;
do not loop over copied images or guessed cache problems. Keep only necessary
paths and observations in context, not repeated image data or tool source code.

## Fallback and handoff

If the local renderer is unavailable or the requested art needs another tool,
use an already authorized host image/graphic renderer with a known schema or a
documented browser screenshot route. Validate one minimal export first, within
the task discovery budget. A paid/cloud generation route still needs any missing
cost and data-transfer consent; do not ask about it when local output suffices.

A transient failure gets at most one retry before switching route. Do not add
repeated sleeps, attempt unrelated formats, or inspect minified tool bundles.
If no route can export a usable image, preserve the text and return PARTIAL with
the rendering cause; before any useful work exists, use BLOCKED. Never claim a
prompt, blank image, uninspected preview, or inaccessible URL is a finished cover.
