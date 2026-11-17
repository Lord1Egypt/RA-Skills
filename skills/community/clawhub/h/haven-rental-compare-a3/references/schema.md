# Input and interpretation

The input is a JSON array. Each entry can contain:

| Field | Meaning |
|---|---|
| name | Listing label |
| rent | Monthly rent, nonnegative number/numeric string; null if unknown |
| monthly_fees | Sum of known mandatory recurring fees; 0 only when explicitly known to be zero; null if unknown |
| deposit | Refundable upfront deposit; null if unknown |
| laundry | Supplied amenity fact, such as in-unit or shared |
| source_url | Public source URL, or a fixture: URI for synthetic examples |
| retrieved_at | Actual retrieval timestamp; preserve missing values rather than inventing one |
| synthetic | true for invented test data; false only for genuine sourced listings |

Use the same currency and monthly period for all amounts and the budget. The script does not convert currencies or weekly rents. It rejects negative/nonfinite costs. Preserve other supplied fields as reference data.

Output is ranked by known monthly total, with unknown totals last. known_monthly_total is rent + monthly_fees only when both are known. within_budget is unknown if that total is unknown. known_upfront_deposit is reported separately and does not include first-month rent, application fees or other move-in charges. missing identifies absent cost/provenance fields. Preference judgments remain explicit explanations based on the supplied facts.

The bundled synthetic example should produce Maple 2035 monthly, Cedar 2175 monthly, and Oak unknown because its recurring fees are unknown. The refundable deposits do not affect those monthly totals. A 2200 budget fits Maple and Cedar on known mandatory costs; preferences can still favor Cedar for in-unit laundry.
