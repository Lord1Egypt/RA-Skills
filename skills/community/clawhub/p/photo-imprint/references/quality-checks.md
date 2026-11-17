# Quality and release gates

Automated style-consistency metrics are diagnostic leads; they never substitute for opening each final page at full size and at phone scale. Machine-verifiable facts are different: expected dimensions, plate readiness/validation, severe background/seam/frame diagnostics, current hashes, metadata absence, and QA-to-stage identity are non-overridable hard gates.

## Plate gate

For every model-rendered plate:

```bash
python3 bin/clean_plate.py normalize --input raw/02.png --config work/resolved-config.json \
  --output work/plates/02.png --report work/plates/02-normalization.json
python3 bin/clean_plate.py validate --input work/plates/02.png --config work/resolved-config.json \
  --report work/plates/02-validation.json
```

The active style profile determines whether cleanup is soft paper-keying, alpha-only validation, or disabled for intentionally opaque media. Blocking checks cover alpha, empty-area noise, corner contamination, rectangular seam risk, and hard border/frame risk. Texture belongs inside actual marks, not in empty background.

## Final QA generation

```bash
python3 bin/qa_images.py --input work/final --plates work/plates \
  --render-plan work/render-plan.json --config work/resolved-config.json --output work/qa
```

This creates color/grayscale contact sheets, long strip, per-page 360×640 phone previews, diagnostics, and `review-checklist.json`.

## Two independent acceptance dimensions

### Page-level compliance

Each page must independently pass:

- its production-plan subject priority and thumbnail read;
- identity anchors, material/depth cues, and structural-line operations;
- absence of forbidden inventions;
- background uniformity and clean subject-to-paper compositing;
- no rectangular seam or forbidden frame;
- full-size and phone-scale review.

### Set-level cohesion

The ordered set must independently pass:

- overall visual cohesion;
- shared paper consistency;
- style and mark consistency;
- typography consistency;
- order/dimensions;
- cross-page rhythm;
- enabled/disabled route and other optional-module integrity.

A page can comply while the set fails, or the set can look unified while one page violates its brief. Packaging is blocked in either case.

Record evidence with `review_checklist.py record`; then validate:

```bash
python3 bin/review_checklist.py validate --checklist work/qa/review-checklist.json
```

Every blocking check needs `status: pass` and evidence. A contact sheet alone is insufficient; full-size and phone evidence files must exist for every page.

## Verified staging and packaging

```bash
python3 bin/package_verified.py stage --input work/final --output work/staging-manifest.json
# Run QA and complete the checklist against this locked stage.
python3 bin/package_verified.py package --input work/final \
  --staging-manifest work/staging-manifest.json \
  --review-checklist work/qa/review-checklist.json \
  --state work/approval-state.json \
  --composition-manifest work/final/composition-manifest.json \
  --output dist/carousel.zip --manifest-output dist/release-manifest.json
python3 bin/package_verified.py verify --zip dist/carousel.zip --manifest dist/release-manifest.json
```

Packaging includes only hash-locked numbered images plus `release-manifest.json`. It requires the deterministic composition manifest and rejects changed/extra/missing stage files; source, caption, renderer-receipt, reference, plate, font, config, or render-plan drift; a mismatch between composed, QA-reviewed, and staged page hashes; incomplete page-level or set-level acceptance; changed QA evidence; unsafe ZIP members; checksum mismatches; EXIF/GPS/XMP metadata; and changed pages that a local revision promised to preserve. Manual `pass` entries cannot override objective failures. Release evidence stores hashes and basenames, not local filesystem paths.

Artifact delivery must copy the verified staged ZIP/images. It must not regenerate artwork.

## Repair rule

Fix the source layer that caused a defect, then rerun plate validation, composition, both QA dimensions, staging, and ZIP verification. Do not hide defects with patches that create seams or inconsistent paper.
