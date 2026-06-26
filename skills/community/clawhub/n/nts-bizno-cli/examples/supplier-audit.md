# Example — Supplier list audit

Goal: take a CSV of vendor business numbers, find which ones are still
operating, classify their tax type, and flag the closed (폐업) ones.

## Setup

```bash
export NTS_API_KEY='<encoded-serviceKey>'
```

Input file `vendors.csv`:

```
vendor_id,b_no,name
v01,124-81-00998,Samsung Electronics
v02,220-81-62517,NAVER
v03,120-81-47521,Kakao
v04,123-45-67890,bogus typo
v05,2208147230,unknown
```

## Step 1 — Local checksum sweep (no API)

```bash
tail -n +2 vendors.csv \
  | awk -F, '{print $2}' \
  | scripts/format.sh - \
  | jq -c 'select(.valid_checksum==false) | {input, formatted}'
# → flags v04 (123-45-67890) instantly without burning quota.
```

## Step 2 — Bulk status check

```bash
tail -n +2 vendors.csv \
  | awk -F, '{print $2}' \
  | scripts/bulk.sh - \
  | tee /tmp/vendor-audit.jsonl
```

## Step 3 — Slice the result

```bash
# Closed vendors → review for offboarding
jq -c 'select(.b_stt_cd=="03") | {b_no, b_no_formatted, end_dt}' /tmp/vendor-audit.jsonl

# Tax-type breakdown for finance
jq -r '.tax_type' /tmp/vendor-audit.jsonl \
  | sort | uniq -c | sort -rn

# Vendors that are 면세사업자 (cannot issue VAT-deductible invoices)
jq -c 'select(.tax_type_cd=="03") | {b_no_formatted, tax_type}' /tmp/vendor-audit.jsonl
```

## Step 4 — Strict authenticity for new payments

For any vendor about to receive a payment > ₩1M, run a full `validate` against
the contract sheet to make sure the rep name + opening date match NTS:

```bash
scripts/validate.sh \
  --b-no   124-81-00998 \
  --start-dt 19690113 \
  --p-nm   "한종희" \
  | jq -e '.valid' >/dev/null \
  && echo "ok" \
  || { echo "MISMATCH — block payment"; exit 1; }
```

## Why split the steps

`status.sh` counts as **1 request per call** (regardless of how many b_no's
you pass), but `validate.sh` counts as **N requests** (one per record).
Run `status` for cheap mass screening, then `validate` only on the rows
you actually need to gate on.
