# Maintaining the shared reader

Read only for renderer/Skill maintenance, demonstrated defects or special export work. Ordinary map generation reuses the bundled runtime without rebuilding the site or inspecting implementation.

## One document and renderer

`src/player.template.html` is the injection template. `src/player.html` and `dist/skill-examples/reader.html` are built previews. Skill and site share the assembler, layouts, SVG, depth policy, fonts and reader. Rebuild runtime copies and resource manifest after canonical changes; do not patch only one generated artifact.

`assets/runtime/manifest.json` fingerprints resources, detects drift and is not a security signature or proof of pixel quality. Tests compare all 16 presets against canonical output.

## HTML-first maintenance

Markdown is initial content/interchange. After editing, the latest saved HTML is authoritative: `document` contains a versioned canonical tree with stable IDs; `source` holds derived Markdown plus preserved source notes. Validate the tree rather than silently falling back to old text. Old HTML with source only remains supported.

Use `--input latest.html --extract` to read current content without loading the complete page. Direct restyling preserves the tree and saved view. For same-topic AI edits, extract the latest HTML, revise its complete Markdown, then use `--input map.html --revise revised.md` to replace that same file. Fence-only revisions retain existing source notes; when supplying new notes, include the prior notes you still need. An explicit different `--output` creates a separate copy. The agent decides topic continuity from the conversation; the renderer does not guess it. The old paired Markdown is a snapshot and must not replace newer HTML edits.

The reader reuses one editor for every preset. Double-click/F2 renames, Tab adds a child, Enter adds a sibling (child at root), Delete removes a subtree, and Ctrl/Command Z undoes. Root deletion and invalid changes are rejected. Escape cancels text editing. Keep IME confirmation separate from Enter-to-commit. No import or CRUD toolbar.

Save the result through the existing Save HTML action or Ctrl/Command S. Save includes tree, notes, selected style, Markdown editing view/draft, collapsed IDs and view. Saving downloads an updated file; there is no silent overwrite, background autosave or persisted undo history. Undo/redo history is bounded to the current session. Image exports use the latest tree, not the old source snapshot. CLI extraction returns a pending Markdown draft when present, otherwise the current canonical Markdown.

## Delivery and validation

One offline HTML embeds fonts and code. No account, key, CDN or service. Selected style plus a Markdown editing view. The same content model validates and applies bulk edits, preserving surviving IDs and source notes. Invalid Markdown keeps the last valid map and stays editable; Save HTML retains its draft. Map-to-Markdown switches reflect the latest direct node edits. Markdown-to-map switches require valid content. Both node and bulk edits share undo/redo. The full Markdown editor replaces notes/metadata as authored, including deletion; CLI fence-only patches separately retain context. Generate according to content complexity without a node quota; source-size, label-size and depth guards remain technical protections, not generation targets. Drafts are embedded in the saved HTML, never executed. Toolbar has reading tour then export. Export menu contains PNG and animated WebP only; Save HTML remains separate. PNG covers the full tree and ignores screen magnification. `imagePlan` chooses at least2x sampling and targets28px for the smallest node font, bounded by32760px and64MP; `limited` and `minTextPx` report the achieved result. Warn when the pixel budget reduces sampling. PNG encoding is lossless; readability still depends on pixel size.

`animationPlan` derives reading groups, parent context, frame aspect and dimensions from target text and bounds. It targets24px focused text within2560px/4MP; small maps use smaller frames, tall labels can use taller frames. First/last frames show the full overview, not a promise that all tiny text is legible simultaneously. Each focus camera is freshly rasterized from vectors, with250/950ms highlights and a breadcrumb. WebP remains raster animation, not guaranteed lossless or vector video. Encoding failure is reported without disguising formats.

The screen percentage represents actual design scale:100% equals the original style font sizes. Fit produces the true percentage instead of resetting the label to100%. Zoom limits use the smallest authored font and viewport to allow detailed reading (32–64px text), not a fixed2000% claim. The percentage button restores original size; wheel zoom anchors to the pointer. Saved views include absolute `scale` plus legacy fit-relative `zoom`; old views remain compatible. Folding preserves actual scale. One policy serves all16 styles and five layouts.

Reading traverses authored hierarchy; it does not invent causal relationships. Deep metrics are shared between measurement, rendering and export through `src/hierarchy.cjs`, keeping previous upper levels and progressively lighter details/annotations.

For reader changes: build and test, check actual rename/add/delete/undo/cancel, keyboard access, collapsed branches, save/reopen and CLI continuation. Download and decode media; verify frames as well as extensions. Test composition with a real IME before claiming it was exercised. Script checks do not prove every browser or aesthetic quality.

## Installed versions and updates

For version questions run `node "<skill-dir>/scripts/manage.cjs" --status`; `render.cjs --version` prints the installed version. `manage.cjs --check` explicitly checks the latest stable GitHub release; never run it during ordinary generation. No published release and network failures have distinct statuses.

Use the standard Skills CLI for lifecycle requests:

| Request | Global command |
| --- | --- |
| Install / reinstall | `npx skills add MarkingYang/mindbox -g` |
| List installations | `npx skills list -g` |
| Update / upgrade Mindbox | `npx skills update mindbox -g` |
| Uninstall Mindbox | `npx skills remove mindbox -g` |

Only update or remove when requested. Resolve the installation scope first: omit `-g` for a project install; use `-p` for project updates. Keep the explicit `mindbox` update/removal filter. Open a new host session after changing the Skill. Reinstallation prompts for assistants. Removal asks for confirmation and targets standard assistant directories unless filtered with `--agent`; generated HTML remains independent.

For a read-only release check use the installed `manage.cjs --check` command above. Do not substitute `npx skills check`: the tested Skills CLI 1.7.4 routes `check` to its updater. Report unavailable/unpublished states accurately. To pin or switch to a published release use `npx skills add https://github.com/MarkingYang/mindbox/tree/vX.Y.Z --skill mindbox -g`, replacing the version with an actual published tag. Updates retain a pin; ordinary reinstall returns to the default branch. Standard updates do not provide a saved previous package. For a prior bundled/local/ZIP install, ordinary reinstall is required once to record the GitHub source; do not assume the standard updater changes a local source to GitHub. Existing links to the same shared directory remain usable.

The optional multi-host installer remains for WorkBuddy and legacy recovery: `npx --yes --package=github:MarkingYang/mindbox mindbox-install --update` repairs its extra link and retains one prior complete package. Its `--rollback` only works when that backup exists; do not promise it for a standard CLI/manual ZIP install. Before removing a shared installation, remove only a WorkBuddy link confirmed to point to that package, preserving any independent copy. See the repository [installation guide](https://github.com/MarkingYang/mindbox/blob/main/docs/installation.md) and [version guide](https://github.com/MarkingYang/mindbox/blob/main/docs/versioning.md) for platform paths and recovery limits. Fingerprints detect drift, not publisher authenticity.

## Branch interaction

Click selects; double-click/F2 edits only. One screen-sized branch button appears on hover/selection: minus folds, plus with the hidden descendant count expands. Leaves have no branch control. Space toggles the selected branch; Left folds an expanded branch, otherwise visits its parent; Right opens a folded branch, otherwise visits its first child. Touch uses selection to expose a44px target. The saved view retains collapsed IDs. Node position is anchored during folds and actual scale is preserved within the zoom limits; Fit resets the overview. The control is transient reader UI and excluded from exports/saved transient state. One behavior serves all16 styles and five layouts.

## Exact artifact checks and website parity

Generation validates the canonical HTML, reads back staged/final bytes before removing recovery copies, and returns SHA-256 hashes of the exact HTML, normalized content and current source. Run `node "<skill-dir>/scripts/render.cjs" --input map.html --check` to inspect an existing artifact without executing its scripts. The receipt identifies structural validation and explicitly sets `browserChecked: false`; it is not a browser, security or source-fact audit. The website binds data into a canonical reader shell and prunes only unused font faces. All16 presets plus internal compositions are tested for byte parity. Do not clone the catalogue into a user deliverable. The public quality report covers geometry/readability models; keep those separate from actual browser evidence.
