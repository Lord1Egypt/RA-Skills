# Mixed-provider projects

Read this reference when one game or repository needs assets from PixelLab,
Retro Diffusion, ComfyUI, or another combination of providers.

The top-level `provider` is the default. A style may override it with its own
`provider`; assets may not. Keep each style's output directory distinct and put
service settings under the matching `providerOptions` key.

Run `doctor --dry-run` and `plan` across the intended filters. Report every plan
group separately. Never add generation counts, USD, and `free` costs. Copy each
estimate into a named ceiling:

```bash
pixelkiln gen \
  --budget pixellab=<generations> \
  --budget retrodiffusion=<usd> \
  --budget comfyui=0
```

Do not replace those with one unkeyed total. PixelKiln should refuse the run if
a paid provider ceiling is missing, repeated, or unknown. A `free` provider may
be written explicitly as zero. Confirm that validation happens before any
provider receives a submission.

Use one lockfile for one manifest. Its entry-level provider is authoritative
when polling, selecting, fetching, restoring, or tagging existing work. A style
provider change makes prior work stale; do not use `accept` to relabel it.

For `balance`, `adopt`, `salvage`, or `purge`, pass the explicit account provider
when the manifest is mixed. Never assume that the top-level default covers all
styles. Provider-qualified workspace claims keep identical remote IDs from
different services separate.

Separate manifests remain valid when teams, credentials, or release schedules
need a harder boundary. Register them in the workspace catalog and never merge
their lockfiles by hand.

A tested split is PixelLab for prompt-sensitive buildings and mature account
recovery, then Retro Diffusion for environment-styled backdrops, clean cutouts,
or native animation. ComfyUI fits private work, local models, and custom graph
control when the user accepts a refinement pass and hands-on art review.
`pixelkiln refine` can apply the same native-grid, palette, audit, and approval
record to output from any provider. Start with a specialized hosted provider when
minimizing cleanup matters more than local control. The committed benchmark is
evidence for tendencies, not a guarantee. Run one representative asset before
expanding any batch, and test a ComfyUI graph on at least two scene families.
