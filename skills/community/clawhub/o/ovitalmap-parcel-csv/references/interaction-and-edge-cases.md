# Interaction and Edge Cases

## Delivery

Send or link the actual files in their returned order:

```text
1. {first_parcel_filename}
2. {second_parcel_filename}
```

Give the import instruction once: open each boundary CSV in OvitalMap and choose `轨迹`. For vertex files, choose `标签`. If both modes were requested, distinguish them by the `_vertices` filename suffix.

## Archive model

- `{CC}_parcels.csv` is the country record.
- `master.csv` is the all-in-one cross-country record.
- New parcels update both in one locked commit.
- Archive hits are re-exported without another append.
- Corrections back up and update both records.

## Parcel codes

Prefer a confirmed official registration/cadastre/permit ID:

```text
{CC}-{OFFICIAL_ID}
```

Otherwise use:

```text
{CC}-{YYMMDD}-{SEQ}
```

The archive allocates sequence continuity. An existing official code is blocking and requires user review; do not silently fall back to a sequential code.

## Archive hits

- Reuse the archived parcel code and provider metadata.
- Export only that parcel as its own file in the requested export mode.
- Do not append it again.
- If a newly supplied official ID fills an empty cadastre field, update it during Step 3.
- If the user insists identical coordinates represent a different parcel, require explicit confirmation and set `allow_duplicate_coordinates: true` with a note naming the matched code.

For a mixed batch, preserve the original `parcel_ref` order across archive hits and new parcels. Export each parcel separately; do not group the delivered files by archive status.

## Multi-parcel batches

- Keep `parcel_ref` stable from intake through replies, CSV generation, and archive results. Numeric positions remain accepted only for backward-compatible input.
- Generate one file per parcel for the requested mode and return the files in `parcel_ref` order. If both modes were requested, keep each parcel's normal file immediately before its `_vertices` file.
- Use one country/region per pipeline run. If parcel-level country codes differ, split the batch and preserve each parcel's ref.
- Report all current parcel-specific problems together in the user's language.
- If two submitted parcels have identical boundaries, request `duplicate_resolutions.{parcel_ref}`:
  - `same`: skip the later duplicate.
  - `different`: keep both, record explicit confirmation, and allow the duplicate boundary during archive commit.
- Reject duplicate non-empty official IDs before code allocation. Use `official_id_resolutions.{parcel_ref}` to correct or clear the later value.
- Never drop an unresolved parcel from run state. No CSV or archive write may occur while a batch conflict remains.

## Provider matching

- Exact normalized match: reuse automatically.
- No match: keep the supplied provider.
- Never merge providers based on similarity alone.

## Corrections

Use `archive_manager.py` action `correct` with `country_code`, `parcel_code`, and `new_vertices`. The operation must:

1. Validate the corrected polygon.
2. Require the parcel in both country and master archives.
3. Reject coordinates already belonging to another parcel.
4. Back up both archives.
5. Update both rows atomically.
6. Regenerate the corrected boundary file by default, or the explicitly requested vertex/both mode.

Report the backup and generated file paths and ask the user to verify the corrected parcel.
