-- Gemini / Generative Language / Vertex AI only, by model name parsed from the SKU.
SELECT
  REGEXP_EXTRACT(LOWER(sku.description), r'(gemini[ -][0-9][a-z0-9. -]*)') AS model,
  sku.description AS sku,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS credits_usd
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND REGEXP_CONTAINS(LOWER(service.description), r'gemini|generative language|vertex')
GROUP BY model, sku
HAVING gross_usd > 0
ORDER BY gross_usd DESC
LIMIT 50
