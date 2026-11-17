# Google Analytics use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/google-analytics

## Analyze Store Traffic and Sales

Understand how visitors arrive at the store, which channels generate purchases, and how traffic quality relates to Shopify sales.

- Apps: Google Analytics, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`

> Analyze my Shopify store's Google Analytics data for the last 30 days. Report sessions, active users, engagement, product views, add-to-cart events, checkout starts, and purchases where available. Break down performance by traffic source, medium, campaign, landing page, device, and country where useful. Compare Analytics purchases with Shopify orders and revenue if the required data is available. Identify the strongest and weakest traffic sources, highlight meaningful changes, and recommend five improvements. Clearly distinguish measured results from estimates and explain any data limitations. Present the results using metric cards, comparison tables, and a prioritized action list.

## Find and Fix Shopping Funnel Drop-Offs

Identify where visitors abandon the purchase journey and investigate product-page, cart, and checkout opportunities.

- Apps: Google Analytics, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT`, `GOOGLE_ANALYTICS_RUN_REPORT`

> Analyze my GA4 ecommerce funnel for the last 30 days, from product views to add-to-cart, checkout starts, and purchases. Calculate stage-to-stage conversion rates and drop-off rates where the available events support them. Segment the funnel by device, traffic source, landing page, and product when possible. Compare the findings with Shopify orders and product information. Identify the largest drop-offs, but do not assume the cause without supporting evidence. Recommend specific investigations and improvements for product pages, cart usability, shipping information, and checkout. Present a funnel table with event counts, conversion rates, and recommended next steps.

## Compare Google Ads With Store Revenue

Evaluate paid campaign traffic against Analytics behavior and Shopify sales to identify campaigns that may be wasting spend.

- Apps: Google Analytics, Google Ads, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`

> Compare Google Ads campaign performance with Google Analytics traffic and Shopify sales for the last 30 days. Review spend, clicks, reported conversions, sessions, engagement, purchases, revenue, and cost per acquisition where available. Match campaign data using campaign identifiers and tracking parameters when possible. Identify campaigns that attract traffic but generate few purchases, campaigns with promising sales performance, and discrepancies between conversion reports. Do not treat Google Ads conversions, Analytics purchases, and Shopify orders as interchangeable. Explain attribution and tracking limitations, then provide a ranked list of campaign investigations and budget recommendations. Do not change live campaign settings.

## Identify High-Potential Products

Find products with strong customer interest, good sales performance, or promising engagement that could benefit from additional promotion.

- Apps: Google Analytics, Shopify, Google Ads
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_RUN_PIVOT_REPORT`

> Analyze my Shopify product catalog and available Google Analytics ecommerce reports. Rank products by product views, add-to-cart activity, purchases, revenue, and product conversion rate where the data supports these metrics. Identify products with strong engagement but weak purchases, products with high sales, and products showing improving demand. Compare these findings with Google Ads campaign performance and inventory levels where available. Recommend which products to promote, investigate, or deprioritize. Consider stock availability and margin data before suggesting increased advertising. Show the supporting metrics and clearly label any assumptions.

## Improve Landing Page Conversions

Discover landing pages that attract traffic but fail to move visitors toward purchases, and propose targeted improvements.

- Apps: Google Analytics, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`

> Review my GA4 landing-page performance for the last 30 days. Compare sessions, engagement, product interactions, add-to-cart events, purchases, and revenue where available. Segment results by source, medium, campaign, and device. Identify high-traffic pages with weak purchase performance and pages that convert particularly well. For each underperforming page, inspect the relevant Shopify product or collection information and recommend improvements to content relevance, product information, navigation, calls to action, or campaign alignment. Do not claim a page causes poor conversion without evidence. Provide a prioritized table with page, observed issue, supporting metrics, and proposed improvement.

## Build Useful Remarketing Audiences

Define audiences based on shopping behavior and prepare eligible segments for potential remarketing campaigns.

- Apps: Google Analytics, Google Ads
- Tools: `GOOGLE_ANALYTICS_LIST_AUDIENCES`, `GOOGLE_ANALYTICS_CREATE_AUDIENCE_LIST`, `GOOGLE_ANALYTICS_LIST_GOOGLE_ADS_LINKS`

> Review my GA4 audience configurations and ecommerce events. Propose audiences for product viewers, add-to-cart users who have not purchased, repeat purchasers, and other useful customer segments supported by the available data. For each audience, specify inclusion rules, exclusion rules, membership duration, business purpose, and relevant campaign ideas. Verify that the required events and dimensions are available before recommending a segment. Check existing audiences and Google Ads linking configuration where accessible to avoid unnecessary duplication. Respect consent, privacy requirements, and platform policies. Do not export audience data, create audiences, or change advertising settings until I approve the proposed definitions.

## Investigate Tracking and Conversion Issues

Audit available Analytics events, conversion settings, data streams, and Google Ads links to help identify unreliable reporting.

- Apps: Google Analytics, Google Ads, Shopify
- Tools: `GOOGLE_ANALYTICS_LIST_KEY_EVENTS`, `GOOGLE_ANALYTICS_LIST_CONVERSION_EVENTS`, `GOOGLE_ANALYTICS_VALIDATE_EVENTS`

> Review my GA4 property configuration for ecommerce measurement and conversion reporting. Inspect available data streams, key events, conversion events, event creation rules, attribution settings, and Google Ads links. Identify missing purchase-related events, questionable event configurations, and potential inconsistencies between Analytics purchases, Google Ads conversions, and Shopify orders. Check dimension and metric compatibility before running reports. Where event implementation changes are needed, prepare a validation plan and use event validation capabilities before recommending production submissions. Distinguish confirmed configuration issues from suspected tracking problems. Do not modify property settings or send production events without approval.

## Measure Marketing Campaign Effectiveness

Determine which campaigns and acquisition channels contribute to meaningful customer activity and purchases.

- Apps: Google Analytics, Google Ads, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_LIST_CHANNEL_GROUPS`

> Evaluate my marketing campaigns using GA4 acquisition reports and available Google Ads data. Compare campaign traffic, engagement, product interactions, purchases, and revenue where supported. Identify campaigns that attract visitors but have weak shopping activity, campaigns that generate purchases, and campaigns that need better tracking. Review campaign names, source and medium values, and available attribution settings. Compare the results with Shopify orders and revenue where a reliable match exists. Recommend improvements to campaign targeting, landing pages, and measurement. Explain the limits of attributing revenue to individual campaigns, and do not modify live campaigns.

## Understand Customer Behavior by Device

Compare shopping behavior across mobile, desktop, and tablet devices to uncover usability and conversion opportunities.

- Apps: Google Analytics, Shopify
- Tools: `GOOGLE_ANALYTICS_RUN_REPORT`, `GOOGLE_ANALYTICS_RUN_PIVOT_REPORT`

> Analyze my GA4 ecommerce performance by device category for the last 30 days. Compare sessions, engagement, product views, add-to-cart events, checkout starts, purchases, and conversion rates where available. Identify devices with large traffic volumes but weaker purchase performance. Compare traffic sources and landing pages to determine whether the difference may be related to visitor intent or page experience. Use Shopify order data where possible to validate the purchase patterns. Recommend specific mobile and desktop improvements, but separate evidence from hypotheses. Present a device comparison table and a prioritized list of next investigations.

## Generate a Complete Ecommerce Performance Brief

Combine Analytics, Google Ads, and Shopify data into a concise report that highlights performance, risks, and the next best actions.

- Apps: Google Analytics, Google Ads, Shopify
- Tools: `GOOGLE_ANALYTICS_BATCH_RUN_REPORTS`, `GOOGLE_ANALYTICS_RUN_FUNNEL_REPORT`

> Prepare an ecommerce performance brief for my Shopify store covering the last 7 days and comparing it with the previous 7 days. Use GA4 reports for acquisition, engagement, ecommerce funnels, landing pages, and product performance. Include Google Ads spend, clicks, and reported conversions where available, and compare these with Shopify orders and revenue when the data can be reliably matched. Highlight the biggest improvements, declines, conversion drop-offs, tracking discrepancies, and product opportunities. Rank the three most important actions for the next week and explain the supporting evidence. Clearly distinguish actual measurements from estimates and recommendations. Format the report using metric cards, compact tables, and a short executive summary. Do not make campaign or property changes automatically.
