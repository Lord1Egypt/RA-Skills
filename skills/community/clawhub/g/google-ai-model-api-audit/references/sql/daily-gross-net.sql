-- Daily gross / credits / net for the trailing 30 days.
-- Replace <PROJ>, <DS>, <ACC>. <ACC> = billing account id with dashes -> underscores.
SELECT
  DATE(usage_start_time) AS day,
  ROUND(SUM(cost), 2) AS gross_usd,
  ROUND(SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS credits_usd,
  ROUND(SUM(cost) + SUM((SELECT IFNULL(SUM(c.amount), 0) FROM UNNEST(credits) c)), 2) AS net_usd
FROM `<PROJ>.<DS>.gcp_billing_export_v1_<ACC>`
WHERE cost_type = 'regular'
  AND DATE(usage_start_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY day
ORDER BY day DESC
