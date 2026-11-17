---
name: ovitalmap-parcel-csv
description: Convert parcel boundaries into OvitalMap-compatible CSV files, assign stable parcel codes, and maintain deduplicated country and master archives. Use for WGS84, DMS, or UTM coordinates supplied as text or images, including archive re-exports and coordinate corrections. Do not use it as cadastral or legal validation.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: OVITALMAP_WORKSPACE
        required: false
        description: Directory for generated exports and archives; defaults to the current working directory.
---

# OvitalMap Parcel CSV

Use the bundled Python scripts through JSON stdin/stdout. Do not recreate coordinate conversion, code allocation, CSV generation, or archive updates manually.

## Input

Set `OVITALMAP_WORKSPACE` to the directory where exports and archives should be stored. If it is unset, the scripts use the current working directory.

Each parcel is a JSON object:

```json
{"vertices":[[114.13472,22.50422],[114.13564,22.50411],[114.135,22.503]],"provider_name":"Survey Team","official_id":null,"altitude":[]}
```

Use WGS84 longitude, latitude order. For a batch, keep one country or region per pipeline run. The pipeline assigns stable `parcel_ref` values (`P01`, `P02`, and so on).

## Workflow

1. Extract and show the source coordinate text. When the source is an image, preserve the transcription for review.
2. Convert decimal, DMS, or UTM coordinates with `scripts/coordinate_converter.py`. Supply the coordinate `format`; for decimal input also supply `order`, and for UTM supply `zone` and `hemisphere`.
3. Show the resulting WGS84 vertices and obtain explicit confirmation of the coordinates and provider names. Do not write exports or archives before confirmation.
4. Obtain the ISO 3166-1 alpha-2 country or region code from explicit context. Ask when it is uncertain.
5. Run `python3 scripts/parcel_pipeline.py --step 1` with `parcels`, `country_code`, and optional `date` in `YYMMDD` form. Retain the returned `run_id`. On `needs_input`, request only the fields listed in `required_input`.
6. Continue with the same `run_id`: run Step `2b` to classify archive hits and new parcels, then Step `2` to assign codes to new parcels.
7. Show the proposed codes. After the user approves them, pass `confirmed_codes: true` to Step `3`.
8. Deliver every path in `result.exports` in its returned order. Boundary files import into OvitalMap as tracks (`轨迹`); vertex files import as labels (`标签`).

Use `--step all` only when the user has already confirmed the complete input and explicitly approved automatic code acceptance with `"confirmed": true` and `"auto_accept_codes": true`.

## Parcel codes

Prefer a confirmed official registration, cadastral, or permit identifier:

```text
{CC}-{OFFICIAL_ID}
```

When no official identifier is available, assign a stable archive code:

```text
{CC}-{YYMMDD}-{SEQ}
```

The archive determines the next three-digit sequence. Do not use `unknown`, invent a descriptive parcel name, or silently replace a generated code later.

## Export modes

- `boundary` is the default and produces one track CSV per parcel.
- `vertices` produces one label CSV per parcel only when explicitly requested.
- `both` produces both formats only when explicitly requested.

Preserve the chosen mode throughout a multi-step run.

## Safety and consistency

- Treat `error`, `blocked`, and `needs_input` as stopping conditions.
- Never guess the country, provider, altitude, official identifier, UTM zone, or hemisphere.
- Reuse an archive hit's parcel code and metadata; do not append it again.
- Resolve batch conflicts by `parcel_ref`; identical coordinates do not prove two submissions are the same parcel.
- Do not replace a non-empty cadastral identifier without explicit confirmation.
- Preserve vertex order; the scripts close polygons when needed.
- Export each parcel separately and preserve submitted order.
- The scripts own filenames, CSV headers, encoding, archive schemas, and defaults.

## Archive operations

Use `scripts/archive_manager.py` with one of these actions: `scan`, `check_duplicate`, `extract_single`, `update_cadastre`, `backup`, or `correct`.

## References

- Read [references/csv-contract.md](references/csv-contract.md) when checking or changing OvitalMap CSV compatibility.
- Read [references/workflow-contract.md](references/workflow-contract.md) when handling pipeline states, confirmations, or errors.
- Read [references/interaction-and-edge-cases.md](references/interaction-and-edge-cases.md) for duplicate submissions, archive hits, corrections, or multi-parcel batches.
