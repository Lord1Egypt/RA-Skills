---
name: prescription-price-research
description: Compare public GoodRx pharmacy price snapshots using Crawlora drug and option discovery. Use to compare posted prices for a specified medication, form, strength, quantity, and US location; excludes diagnosis, dosing advice, medication changes, and purchases.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Prescription price research

## Access and contract

Use only the three read-only GoodRx price routes listed in
[reference/endpoints.md](reference/endpoints.md). The optional bundled helper
is the only shell command this skill asks to run; its allowlist rejects every
other route and it accepts GET requests only. When invoked, it reads
`CRAWLORA_API_KEY` and sends it as an `x-api-key` header over HTTPS to
`api.crawlora.net`; it reads `TMPDIR` only to choose a temporary config
location. The key is not sent to GoodRx. The helper writes a mode-600 curl
config under `TMPDIR` and removes it when the command exits. It does not
enumerate environment variables or files, install software, or run with
elevated privileges. Run it only for a requested price comparison; successful
requests can consume credits. Check application `code` as well as HTTP status,
stop on authentication errors, back off on `429`, and retry a transient
upstream failure once. Preserve source URLs, identifiers, and collection times.

GoodRx can return a retained price response when the upstream refuses a live
fetch. The standard helper prints the JSON body but not `X-Availability` headers,
so keep the Crawlora retrieval time separate from any source timestamp and do
not call the result a live checkout quote.

Compare posted pharmacy prices for the user's specified medication and package.
A price comparison does not select a medication, dose, or clinical substitute.

## Resolve the exact priced product

1. Use the drug directory's initial-letter route only to resolve a slug for the
   medication the user named, or use a slug supplied by a verified GoodRx
   source. Read `goodrx_drug_options` before using the exact label
   (brand/generic), form, strength, and package quantity. Valid option values
   form combinations; do not build an arbitrary cross-product or equate
   similarly named formulations.
2. Keep the medication and product choices fixed to the user's request. The
   `dosage` API parameter is a GoodRx product-option identifier; it is not a
   dosing instruction or recommendation. Do not select a medication, dose,
   formulation, or substitute for the user.
3. Query prices with those resolved choices and explicit US location. Coordinate
   queries require latitude and longitude together; retain state/ZIP evidence
   rather than inventing coordinates from an approximate city. Missing choices
   can select source defaults, so inspect and report the resolved product before
   treating two quoted prices as comparable.
4. Record quantity, units, brand/generic label, strength, form, location,
   pharmacy, coupon or other eligibility conditions, source URL, and timestamp.

```sh
scripts/crawlora.sh /goodrx/drugs letter=a
# Select the requested drug slug, then discover its exact options:
# scripts/crawlora.sh /goodrx/drug-options slug="$DRUG_SLUG"
# scripts/crawlora.sh /goodrx/drug-prices slug="$DRUG_SLUG" form="$FORM" dosage="$DOSAGE" quantity="$QUANTITY" zip_code="$ZIP"
```

## Compare costs and limitations

Keep cash/list prices, discounted coupon prices, membership prices, and insurance
copays separate; do not assume a coupon combines with insurance. Calculate unit
cost only for the same unit and formulation, and show the package total alongside
it. A snapshot is not guaranteed pharmacy stock, a final checkout price, or an
insurer's benefit determination. Missing prices remain unknown; do not substitute
zero or assume a drug is unavailable. Return a comparable pharmacy-price table,
resolved-option ledger, source/time, and eligibility questions to confirm.
Price alone does not establish clinical suitability. Questions about changing
medicines, doses, or clinical suitability require a qualified
clinician/pharmacist. Do not redeem a coupon, buy medication, or transmit
medical or prescription data from this research.
