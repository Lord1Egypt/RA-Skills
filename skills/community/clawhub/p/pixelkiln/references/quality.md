# Manifest quality profiles

Read this reference when a selected style declares `quality`, `plan` reports a
derived-art state, or `pack`/`mount` is blocked on approval.

## Keep raw generation separate

The style's normal `outDir` owns raw provider output. `quality.outDir` owns the
refined PNG and its `.pixelkiln.json` record. Palette, grid confidence,
transparency, fixer revision, interpreter, and final path are excluded from the
provider spec hash. Changing them must not trigger generation or add provider
cost. The interpreter is execution configuration and does not invalidate a
current refinement record by itself.

The source is `asset.source` when declared. Otherwise PixelKiln requires one
intact downloaded PNG from the lockfile. ComfyUI `frames` is the multi-output
exception: it requires every ordered, role-named PNG. Do not refine modified,
missing, GIF, provider-native animation, or tileset input through this contract.

## Run the gate

```bash
pixelkiln refine --style <style> --only <asset-ids>
pixelkiln refine approve --from <final.pixelkiln.json> --reviewer "<name>"
pixelkiln refine check --style <style>
pixelkiln plan --style <style> --check
```

Manifest mode reads output, palette, and thresholds from the manifest. Do not
pass `--out`, `--palette`, `--fixer-revision`, `--min-grid-confidence`, or
`--min-transparency` without `--from`.

Set `quality.fixerPython` to a manifest-relative project environment when the
default `python3` does not contain the fixer. A one-run `--fixer-python`
override wins, followed by the manifest setting,
`PIXELKILN_PIXEL_FIXER_PYTHON`, and `python3`.

`refine` skips current pending and approved records. Use `--force` only when the
user intends to rebuild current output; any rebuild resets approval. A changed
declared source or profile becomes `needs-refinement`. Provider output whose
generation spec is stale, missing, modified, or structurally unsupported is
`blocked`. Mechanical success becomes `needs-approval`, never approved.

Before recording approval, have the named reviewer inspect the exact native PNG
at 1× and integer zoom. Check prompt coverage, silhouette, clusters, contours,
single-pixel noise, palette separation, alpha, and seams. Do not infer approval
from a passing audit, a high-confidence grid, prior approval of different bytes,
or permission to generate.

`pack` and `mount` fail closed until every participating record is current and
approved. They then use the refined PNG and include its quality record in their
provenance. Do not bypass that gate with raw lock output or a copied file.

For `frames`, one record owns the whole set. Require matching native dimensions,
step, and phase; apply one palette; inspect the loop at 1×; and record one named
approval. Packaging uses every `asset/frame-XX` member or fails.
