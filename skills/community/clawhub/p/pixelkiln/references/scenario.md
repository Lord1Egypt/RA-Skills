# Scenario

Use Scenario when the project needs a hosted third-party model or a reusable
project-specific model. BFL Flux 2 Dev is live-tested through authentication,
CU preflight, paid generation, human review, and durable recovery. Other model
schemas remain unverified. Require a one-asset smoke before widening a batch.

## Safety boundary

- Require `SCENARIO_SDK_API_KEY` and `SCENARIO_SDK_API_SECRET`. Never print or
  commit either value.
- Require `providerOptions.scenario.modelId` and a positive per-asset
  `maxComputeUnits`.
- Run `doctor --dry-run` and `plan` before authenticated `doctor` or generation.
- Planning is offline. At submit, PixelKiln sends the identical request with
  `dryRun=true` and refuses missing, malformed, or over-ceiling CU quotes.
- Pass `--budget <compute-units>` for a Scenario-only run. In a mixed run, use
  `--budget scenario=<compute-units>` alongside every other provider ceiling.
- Leave `numOutputs` above one to the local `pick` workflow. Selection reuses an
  existing Scenario asset and must not trigger another generation.
- Treat `scenario://` job and asset references as the recovery contract.
  Temporary signed Scenario URLs must not remain in a settled lockfile.
- Verify the chosen model returns PNG. The adapter rejects other media
  formats, animation, and tiles.
- Style images and `image-to-image` revisions are uploaded once (free) and sent
  as the model's `referenceImages` input; set `referenceParameter` and
  `referenceArray` for a model that names it differently. Other revision modes
  and `strength` are refused.

Scenario model parameters vary. The adapter supplies prompt, 16–4096px dimensions
(each model has tighter bounds, reported by the free dry run), one to four outputs, and optional seed. Put only documented
model inputs in `parameters`; PixelKiln rejects attempts to override its prompt,
dimensions, seed, output count, project routing, or CU ceiling.

Chain models across styles with `revision.fromStyle`; put any `quality` profile
on the last style. For large or illustrative art, render at four times the
target size (GPT Image 2 `quality: medium` is a flat 11 CU, FLUX.2 Klein 9b
1 CU), then Pixelate, Birefnet cutout, and `pixelkiln refine`. Pixelate's
`pixelGridSize` is not literal on inputs wider than about 512 px (120 asked gave
a 240-cell grid on a 960 px image): check one image's blocks first. Do not use
the chain for small native-size sprites. The adapter handles images only;
sound effects (MM Audio 1 CU, ElevenLabs 30 CU) go through the API directly.
See `docs/SCENARIO.md` for settings and measurements.

PixelKiln validates the job, bytes, hashes, and recovery path. It does not prove
the output is good pixel art. Inspect one result at 1× before approving a batch.

When calling Scenario outside PixelKiln (audio, say), the free dry run is only the
query parameter `?dryRun=true`: a `dryRun: true` in the JSON body is ignored and
submits and bills a real job. LoRA models need the legacy `/generate/txt2img`
endpoint (10 CU, JPEG output, not callable by the adapter). The adapter cannot read
the CU balance; check the dashboard and budget with a margin (a hand tally ran about
5% under the dashboard). A reference image keeps an existing design (silhouette
overlap 0.93 to 1.00 against 0.39 to 0.66 from text alone), though some models shift
its colours; use it before a text-only prompt when the look must be kept.

See `docs/SCENARIO.md` for setup, manifest examples, unsupported account
operations, and the live validation checklist.
