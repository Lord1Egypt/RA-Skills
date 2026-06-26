# GAQL Examples

## Notes

- Customer IDs are 10-digit numbers without dashes.
- Cost fields are returned in micros. Divide by 1,000,000 for currency units.
- Start with read-only reporting queries before considering any operational change.

## Campaign performance, last 30 days

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Ad group performance

```sql
SELECT
    ad_group.id,
    ad_group.name,
    ad_group.status,
    campaign.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.ctr,
    metrics.average_cpc,
    metrics.conversions
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Keyword performance

```sql
SELECT
    ad_group_criterion.criterion_id,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    campaign.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.quality_score
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Search terms report

```sql
SELECT
    search_term_view.search_term,
    campaign.name,
    ad_group.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Zero-conversion keywords with meaningful spend

```sql
SELECT
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    campaign.name,
    metrics.cost_micros,
    metrics.clicks,
    metrics.impressions,
    metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.conversions = 0
  AND metrics.cost_micros > 5000000
ORDER BY metrics.cost_micros DESC
```

## Search terms with spend and no conversions

```sql
SELECT
    search_term_view.search_term,
    campaign.name,
    metrics.cost_micros,
    metrics.clicks,
    metrics.impressions,
    metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.conversions = 0
  AND metrics.cost_micros > 5000000
ORDER BY metrics.cost_micros DESC
```

## Conversion actions overview

```sql
SELECT
    conversion_action.name,
    conversion_action.category,
    conversion_action.status,
    conversion_action.primary_for_goal,
    conversion_action.type
FROM conversion_action
ORDER BY conversion_action.name
```

## Device performance

```sql
SELECT
    segments.device,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Geographic performance

```sql
SELECT
    geographic_view.country_criterion_id,
    geographic_view.location_name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

## Daily trend

```sql
SELECT
    segments.date,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY segments.date DESC
```

## Account overview

```sql
SELECT
    customer.id,
    customer.descriptive_name,
    customer.status,
    customer.currency_code,
    customer.time_zone
FROM customer
```
