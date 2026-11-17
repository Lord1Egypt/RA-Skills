# Onimi Slides creation

Onimi Slides use the original Bento canvas, editor behavior and document model through a reviewed Onimi
adapter. Creator supplies content and an exact compatible author document. Do not make a replacement
canvas, a browser-side AI generator, or an invented JSON schema.

## Pick content and theme separately

Use one narrative template:

- work report: period, goals, evidence, variance, decisions and next steps;
- proposal: problem, audience, approach, proof, scope, tradeoffs and ask;
- product introduction: user problem, workflow, differentiated capabilities, proof and next action;
- lesson: outcomes, concept sequence, worked example, practice and recap;
- research defense: question, related work, method, evidence, limitations and conclusion;
- portfolio: context, role, process, selected work, outcome and reflection.

Each template requires its own visible composition within the selected theme. Preserve and adapt the
acquired document's structure rather than substituting titles into a shared cover or repeating one
layout across six narratives:

| Template | Cover composition and supporting layouts |
| --- | --- |
| Work report | Lead with a period and result scorecard; use goal/result comparisons, variance evidence and owner/action rows. |
| Proposal | Frame the problem beside a proposed direction and decision ask; use alternatives, scope and tradeoff comparisons. |
| Product introduction | Pair the value claim with a product or workflow panel; use capability demonstrations and a clear next action. |
| Lesson | Present the learning goal with a sequenced learning path; use worked examples, practice prompts and recap checks. |
| Research defense | Organize the research question, method and evidence as a research brief; use results, limitations and conclusion layouts. |
| Portfolio | Give selected work a prominent showcase area with role and context; use project/process/outcome stories and reflection. |

Changing only the title, subtitle or colors does not satisfy template adaptation. Keep the same theme
while arranging content blocks, emphasis, grouping and visual hierarchy for the chosen narrative.
Use compatible elements already present in the acquired document; do not add a schema or require
additional questions to obtain these distinctions.

Use one Bento theme—Signal, Terra, Orbital or Pixel Picnic—as the visual system. The current
visual profiles combine typography, composition and decorative surfaces:

| Theme | Typography and composition | Surface |
| --- | --- | --- |
| Signal | Precise sans headings and body, aligned grids, coral rules | Clear light canvas |
| Terra | Serif headings with sans body, generous editorial spacing | Warm paper gradient |
| Orbital | Mono headings and labels with sans body, orbit geometry | Dark blue radial gradient |
| Pixel Picnic | Bold playful headings, rounded or mono fallback, pastel blocks and stepped shapes | Pastel composition |

A theme changes presentation, not the narrative template. Use the exact acquired profile;
do not recreate it by changing only colors. Fonts use local fallback stacks: check Chinese wrapping
and readability when a preferred font is unavailable, and do not promise identical typography across
operating systems. Theme gradients are bounded embedded PNG image elements in the acquired document;
retain them and their placement. `background`, `fill` and other color fields still require compatible
color values, never CSS gradient strings. Do not invent a gradient element or expand the document schema.
The optional theme `visualStyle` is one of `signal-grid`, `terra-editorial`, `orbital-tech` or
`pixel-playful`; preserve the acquired value. Existing earlier revisions without it remain valid. Keep one main claim per slide and vary layouts for explanation,
evidence, comparison, sequence and conclusion. Chinese needs intentional wrapping and spacing rather
than an English title stretched to fit.

Ask only useful optional questions: audience, decision or purpose, duration, key claims, supporting
material and style. Reuse existing answers. When absent, create a short editable outline and state
assumptions. Label all sample metrics.

Bundled example decks demonstrate a complete narrative rather than a three-slide wireframe. Treat
their people, organizations, research, quotes and metrics as synthetic examples. Preserve the visible
example label until every claim has been replaced with verified user material. Rework the sequence,
tables and charts for the user's evidence; changing only the title or theme does not make an example
factually ready to present.

## Discover and acquire the exact template

1. Select the existing Onimi project first. A valid explicit project UUID is a hard precondition for
   `onimi_list_templates` and `onimi_get_template`. If the user has not identified an existing project,
   ask once which project to use; do not probe with `null`, an empty value, a nil UUID or a placeholder,
   and do not create a project. Preserve the selected template/theme and local editable outline while
   waiting for that answer. Call `onimi_list_templates` with the resolved `projectId` and the locale.
   Public listing returns metadata, compatibility and effective availability, never source.
2. Select one exact advertised `templateKey` and `version`. Discover the visual theme separately in
   the resource catalog and select its exact `themeKey` and `themeVersion`. Do not guess a key,
   substitute `latest`, or combine multiple template sources.
3. Call `onimi_get_template` with a fresh UUID and exact
   `{templateKey, projectId, locale, version, themeKey, themeVersion}` when applying a theme. It
   requires `template:read`; premium source additionally requires current effective entitlement.
   Retry an uncertain acquisition with the same UUID and body. The returned themed `source.document`
   already carries the applied theme and exact `onimi.themeRevision` identity; retain its theme
   derivation and license receipt.
4. Write the returned structured object to a task cache outside the installed Skill and run:

   If the Agent host truncates a large tool result, call `onimi_get_template_chunk` with the
   **same** project, template, version, locale, theme pair and idempotency UUID, plus
   `compression: "br"` for smaller transfer and a SHA-256 per chunk. Start with
   `chunkIndex: 0`, then fetch every index through `chunkCount - 1` in order. Save each small
   JSON tool result as one line in a private task-cache `chunks.jsonl`; do not read a
   host-protected internal tool-result file or regenerate the source from a similar local example.
   The chunk tool replays the same authorized acquisition and does not accept task content.
   After each small group of chunks, validate the file before fetching more; a transcription error
   is identified by its `chunkIndex` and must be re-read from the native tool:

   ```sh
   node /absolute/path/to/onimi-pages-creator/scripts/assemble-template-chunks.mjs check /absolute/path/to/chunks.jsonl
   ```

   Assemble the exact response before using any source bytes:

   ```sh
   node /absolute/path/to/onimi-pages-creator/scripts/assemble-template-chunks.mjs /absolute/path/to/chunks.jsonl /absolute/path/to/template-response.json
   ```

   The helper checks every index, each compressed chunk digest, acquisition identity, transfer
   digest, total byte count, complete response digest and canonical source digest; it refuses
   to overwrite an existing output. If any chunk or digest
   differs, stop and retain the current editable outline. Do not combine chunks from different
   acquisitions or continue with a partial source.

   Then run:

   ```sh
   node /absolute/path/to/onimi-pages-creator/scripts/scenario.mjs verify /absolute/path/to/template-response.json <template-key> <exact-version> <locale>
   ```

   Require `canonical-json`, matching byte length and SHA-256. Keep the returned `license`, asset
   notices and `acquisition` receipt with the document. Removing Onimi branding never removes third-party
   license obligations.

An acquired template remains usable for an existing document, but do not treat that as permission to
acquire new premium bytes later. If acquisition is unavailable, preserve the user's content and use a
clearly identified local HTML presentation; do not call it editable Onimi Slides.

## Author and save

Use the acquired schema and compatible runtime exactly. The source for a Slides draft is:

```json
{"kind":"slides","document":{"...":"exact Bento-compatible author document"}}
```

For a Slides deck with no shared cloud data, its separate protocol manifest is **exactly**:

```json
{"protocolVersion":1,"kind":"slides","data":{"mode":"local"}}
```

`data` is required. Do not send a bare `{ "protocolVersion": 1, "kind": "slides" }` or a
manifest for a Page. Use `controlled-cloud` only after the user has explicitly chosen collaborative
data and the collection schema has been configured.

Start from the acquired themed `source.document` and replace its example content with the user's
content. Preserve the valid `document.onimi` fields: `runtimeVersion`, `sourceFormat`,
`templateKey`, `templateRevision` and `themeRevision` (including the exact theme source SHA-256
from the acquisition). `sourceFormat: "onimi"` is valid for an Onimi-authored document;
`"bento-html"` identifies an imported Bento HTML document. Changing the value or removing the
revision identities does not repair an invalid manifest. Keep claims, notes, hidden slides, theme
values and the resource provenance separate when editing the template. A style-only edit must retain
manual overrides, chart and table data, speaker notes, hidden slides and existing access permissions.
Use the catalog-advertised exact revisions; older acquired revisions remain valid and must not be
relabeled as the newer visual profile.

Before claiming the source is ready or calling `onimi_save_draft`, write the complete
`{kind, document, manifest}` object to a local JSON file and run the bundled preflight:

```sh
node /absolute/path/to/onimi-pages-creator/scripts/validate-slides.mjs /absolute/path/to/deck.slides.json <template-key> <template-version> <theme-key> <theme-version>
```

It rejects lost revision identities and colors that Bento would silently replace with defaults,
including unresolved `INK`/`ACCENT`/`BG` tokens. Repair the source and rerun it after every theme
change. This is a local preflight; the server still performs the authoritative schema, permission
and draft-revision checks when saving.

Speaker notes, hidden slides and author-only assets stay in private source. For a large Slides
document, use the staged file path so the full source need not be copied through the model. After
`onimi_get_draft`, prepare a private upload body and small begin request:

```sh
node /absolute/path/to/onimi-pages-creator/scripts/draft-payload.mjs prepare-upload-slides \
  /absolute/path/to/deck.slides.json /absolute/path/to/upload-body.json
node /absolute/path/to/onimi-pages-creator/scripts/draft-payload.mjs prepare-begin \
  /absolute/path/to/upload-body.json <project-uuid> <current-revision> \
  <new-mutation-uuid> /absolute/path/to/begin-request.json
```

Call `onimi_begin_draft_upload` with the complete small begin request, save its response in a
private file, then use `draft-payload.mjs send-upload` with the confirmed MCP resource URL as
described in the main Skill. The upload body contains only `{source:{kind:"slides",document},manifest}`;
keep the acquisition and license receipt separately. The server may normalize a Bento document
before calculating `sourceSha256`, so `sourceReadbackRequired: true` on the upload receipt means
**read and compare the saved draft**, not that the upload failed. Call `onimi_list_draft_revisions`
and `onimi_get_draft`; verify the revision ID, source hash, manifest, six-page content where
applicable, notes and exact template/theme identities. Do not finish the journal or publish until
that readback succeeds. A 409 means another save won; read and reconcile the new head. Never
change the body or expected revision while reusing an idempotency UUID.

For a small Slides source that the client can forward without truncation, `onimi_save_draft` is
also valid with the complete source, exact manifest, current revision and UUID. If saving returns
`INVALID_SOURCE`, inspect the actual source and manifest against the accepted schema; do not
silently drop resource provenance, create another project or claim that a local file is a saved
Slides draft.

Use `onimi_list_draft_revisions` for history. Restoration is an explicit new save: fetch the selected
revision, fetch the current head, then save the selected source and manifest with the current numeric
revision and a new UUID. It does not overwrite history.

Publication projects an audience document on the server. Notes, hidden slides and private assets must
be absent from audience bytes, including JSON and comments. Review keyboard navigation, slide position,
mobile layout, print-all, reduced motion, font failure, image failure and both supported UI languages.
Do not promise faithful PowerPoint round-trip export. Treat imported HTML as untrusted; only recognized
Bento JSON enters the adapter, and foreign scripts or collaboration endpoints are never reused.
