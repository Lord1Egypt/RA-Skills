# Base Mode Verification Runbook

## 1. Identify the Base target

```bash
mbs workbook inspect --target "$WORKBOOK"
mbs worksheet list --target "$WORKBOOK" --output json
mbs table inspect --target "$BASE_TABLE"
mbs table schema --target "$BASE_TABLE"
mbs table sample --target "$BASE_TABLE" --limit 10 --output table
```

Use `table sample` for a quick, representative, non-exhaustive check of Base
records and field values. Use bounded `table read` when verification needs a
specified result window or post-mutation readback.

Use a persistent Base table ID (`tid`) and stable field/record identities. A
worksheet name alone is insufficient for a Base record or field mutation.
For a Base target, canonical `table inspect` also returns matched worksheet
dimensions when available; use `table schema` and `table read` for fields and
records.

## 2. Insert or update records

```bash
mbs table insert --target "$BASE_TABLE" --frame-in rows.json --verify
mbs table update --target "$BASE_TABLE" --frame-in corrected_rows.json --key order_id --verify
mbs table read --target "$BASE_TABLE" --limit 100 --output table
```

`table update` is key-based. It does not imply an atomic full-table replacement,
delete missing records, or preserve all legacy replacement semantics. Stop and
report the capability gap when those semantics are required.

## 3. Fields and Formula fields

```bash
mbs column insert --target "$BASE_TABLE" --field gross_margin --field-type formula --verify
mbs column rename --target "$BASE_TABLE" --field gross_margin --new-name "Gross Margin" --verify
mbs column config --target "$BASE_TABLE" --field gross_margin --spec field-style.json --verify
mbs formula validate --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost'
mbs formula set --target "$BASE_TABLE" --field gross_margin --expression 'revenue - cost' --verify
mbs formula recalculate --target "$BASE_TABLE" --field gross_margin --verify
```

`column config` configures resource style; it is not a substitute for every
Base typed-field property. Use current parent/command help before changing a
field and report unsupported schema work instead of selecting a hidden command.

## 4. Verify SQL materialization

```bash
mbs sql materialize \
  --target "$WORKBOOK?table=S_orders" \
  --sql-file result.sql \
  --mode create \
  --schema schema.json \
  --verify
mbs table read --target "$WORKBOOK?table=S_orders" --limit 100 --output table
```

Verify the result schema, row count, representative values, and the target
identity returned by the mutation.

## 5. Reject Sheet-only misuse

Do not apply A1 range writes, merge/unmerge, Sheet cell notes, or Excel cell
formula assumptions to a Base table. Explain the mismatch and choose a public
Base record/field workflow instead.
