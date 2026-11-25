-- Spend by SKU (model-level detail lives in sku.description) for the trailing 30 days.
SELECT
  service.description AS service,
  sku.description AS sku,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM(cost) + SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS net_usd
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY service, sku
HAVING gross_usd > 0
ORDER BY gross_usd DESC
LIMIT 50
