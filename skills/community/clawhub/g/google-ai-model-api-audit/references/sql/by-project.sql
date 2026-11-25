-- Spend by project: separates experiments from production.
SELECT
  project.id AS project_id,
  project.name AS project_name,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM(cost) + SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS net_usd
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY project_id, project_name
HAVING gross_usd > 0
ORDER BY gross_usd DESC
