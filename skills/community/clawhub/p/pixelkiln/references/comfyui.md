# ComfyUI

Read this reference before operating a PixelKiln manifest whose provider is
`comfyui`.

When the bundled environment recipe matches the task, install an exact version
and verify it first. Read [Versioned recipes](recipes.md) for the trust boundary.
A verified recipe pins the graph and models; it does not approve the art.

## Set expectations

The ComfyUI adapter automates a committed graph, candidate review, provenance,
and recovery. It does not make a general image model produce good pixel art.
Use it when local control, private inputs, or a custom graph justify manual art
direction. Do not call the current SDXL plus Pixel Art XL setup production-ready
or game-ready.

If the user mainly wants the shortest path to usable pixel art, compare the
specialized hosted providers first. Choose ComfyUI when owning the workflow is
worth the extra model testing and cleanup.

## Quality-first workflow

1. Generate two to four candidates on the model's normal working canvas.
2. Reject weak composition and missing prompt elements before post-processing.
3. For isolated art, remove the background at full resolution.
4. Run `pixelkiln refine` to recover one native pixel per detected cell and
   apply the project's final palette, usually 16–32 colors without dithering.
5. Review the native file at 1× and an integer zoom. Check silhouette, clusters,
   contours, single-pixel noise, palette separation, alpha, and seams.
6. Record the named review with `pixelkiln refine approve`, then require
   `pixelkiln refine check` before packaging.
7. If the project has a quality baseline, run `pixelkiln quality check --from
   <baseline>` to catch structural drift from its reviewed references.
8. Accept the smallest clear result. For the tested stack, start with 48–128px
   native components and compose larger scenes from reviewed parts.

Background removal stays in the ComfyUI graph. PixelKiln handles grid recovery,
the final palette, measurable checks, and the approval record. It cannot decide
whether the drawing is good. Do not present the generated
working canvas, a nearest-neighbor resize, an unreviewed grid recovery, or a
pending quality record as the finished asset.

`quality check` is deterministic and safe for CI. It measures dimensions,
palette, alpha, edges, and isolated pixels and can bind the refiner's record.
It cannot judge composition, prompt coverage, clusters, or readability; keep
the named 1× review separate.

Test a workflow on at least two different scene families before recommending
it. A prompt that reduced noise in the alpine benchmark increased noise in the
volcanic benchmark and still missed the requested fortress.

## Connection and workflow contract

ComfyUI is self-hosted and needs no provider credential. Never assume the
server is reachable. `pixelkiln doctor --dry-run` validates workflow bindings
offline; `pixelkiln doctor` checks the read-only system-stats route. The default
URL is `http://127.0.0.1:8188`; `COMFYUI_BASE_URL` overrides it. Keep an
unauthenticated server off public networks.

The style's `providerOptions.comfyui` must name a committed API-format workflow,
one image output node, the expected candidate count, and the inputs PixelKiln
may replace. Text-to-image needs prompt, width, and height; multiple candidates
need batch size; a declared seed needs seed. A revision needs `sourceImage`,
inpainting needs `maskImage`, and declared strength needs `strength`. Read
[Controlled revisions](revisions.md) before operating one. Node IDs and model
filenames are workflow-specific. Check the exported JSON instead of guessing.

Bindings may also use project-defined names. Match each name to the asset's
`providerInputs` entry instead of copying one workflow per pose, reference, or
strength. When a custom binding targets `LoadImage.image` or
`LoadImageMask.image`, its value is a manifest-relative PNG/JPEG. Keep that file
with the project: PixelKiln hashes it during planning, checks it again before
submission, uploads it under a content-addressed name, and records no local
path. Do not tell users to copy these inputs into ComfyUI by hand.

Other custom inputs must be string, finite number, or boolean values matching
the committed workflow placeholder. Treat an unknown binding, duplicate target,
reserved built-in name, missing file, or type mismatch as a manifest error.
Changing an input value or image bytes makes only the affected asset stale.

For `generator: frames`, `providerOptions.comfyui.frames.vary` names one custom
binding and the matching `providerInputs` value is an ordered 2–64 item array.
Keep `numImages: 1`. A nonzero `seedStep` also requires `style.seed` and a seed
binding. Review, fetch, refine, approve, and pack the set as one asset. Reject a
set when any frame changes grid dimensions, step, or phase; never keep only its
good-looking members.

Planning parses and hashes the workflow file without contacting ComfyUI. A
workflow content change makes affected assets stale. The adapter supports
`map` and ordered still-image `frames`, PNG output from one node, 1–16 map
candidates, 2–64 frames, and dimensions from 16–4096px. Manifest `styleImages`
and `palette` are unsupported; those
shared controls belong in the workflow. Per-asset ControlNet and reference
images belong in custom bindings plus `providerInputs`.

## Tested evidence, not a preset

The diagnostic stack uses SDXL Base 1.0 as
`sd_xl_base_1.0.safetensors` and Pixel Art XL as
`pixel-art-xl.safetensors`. The repository's
`benchmarks/provider-environments/comfyui/` project names both files and uses
core nodes only. Its workflows sample at 1024×1024, then use `ImageScale` with
`nearest-exact`; width and height bindings point to the scale node so the saved
PNG still matches the manifest dimensions. The isolated workflow uses LoRA
strength 1.0, while the environment workflow uses 0.85. Read
`docs/COMFYUI.md` for download links, checksums, licenses, and measured limits.

The cleanup experiment in
`benchmarks/provider-postprocessing/comfyui/` runs BiRefNet on the decoded
full-resolution image, quantizes RGB separately, joins the inverted background
mask as alpha, and scales last. It proves those nodes run; it is not the complete
recommended pipeline. Background removal belongs before grid recovery. Final
palette quantization belongs after grid recovery. Always audit the final native
file, because reconstruction can introduce averaged colors.

The boundary experiment in
`benchmarks/provider-hires/comfyui/` keeps generation canvas, native art grid,
and display size separate. Pixel Art XL can make a 1024px raster whose implied
cells resolve to a much smaller editable grid. Nearest-neighbor scaling
preserves those fake cells; it does not repair them. Run accepted output through
`pixelkiln refine` with the pinned local Retro Diffusion Pixel Art Fixer and an
explicit project palette. Its companion records the fixer revision, source and
output hashes, detected grid, confidence, dimensions, audit, and human-review
state.

Do not add `LatentUpscale` and a second sampling pass by default. The tested
1536px and 2048px variants blurred the output. Nearest-neighbor scaling preserves
existing cells but cannot repair them. Grid recovery proves structure, not good
clusters or prompt coverage.

## Operation and recovery

The plan reports `0 free` and generation uses `--budget 0`. Explain that this
means no metered API charge. Hardware, electricity, hosting, and model licenses
can still cost money.

The lockfile records a prompt ID, output node, workflow hash, and portable
`comfyui://` source. Restore from the validated content cache first. If the
cache is missing, the current ComfyUI server must still retain the history
output so PixelKiln can resolve the portable source.

For setup, the tested model stack, benchmarks, and troubleshooting, use
`docs/COMFYUI.md` or
<https://pixelkiln.griffen.codes/docs/comfyui>.
