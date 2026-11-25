-- Input vs output vs cached token spend. Output tokens usually cost 4-8x input.
SELECT
  CASE
    WHEN REGEXP_CONTAINS(LOWER(sku.description), r'cached|context cach') THEN 'cached_input'
    WHEN REGEXP_CONTAINS(LOWER(sku.description), r'output|response|generated') THEN 'output'
    WHEN REGEXP_CONTAINS(LOWER(sku.description), r'input|prompt') THEN 'input'
    ELSE 'other'
  END AS token_class,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM(usage.amount), 0) AS units
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND REGEXP_CONTAINS(LOWER(service.description), r'gemini|generative|vertex')
GROUP BY token_class
ORDER BY gross_usd DESC
