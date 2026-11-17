# Google Ads use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/google-ads

## Analyze Campaign Performance and ROI

Review advertising performance across campaigns, keywords, search terms, and ads. Identify high-cost campaigns, inefficient spending, and opportunities to improve conversions using available reporting data and Shopify sales information.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_GET_RMF_REPORT`, `GOOGLEADS_SEARCH_STREAM_GAQL`

> Analyze my Google Ads performance for the last 30 days. Review campaign, ad group, ad, keyword, and search-term performance wherever the available reporting supports it. Identify the strongest and weakest performers based on spend, clicks, conversions, conversion rate, and cost per conversion. Compare the results with relevant Shopify product and sales data if available. Rank the top five optimization opportunities and explain the reasoning behind each recommendation. Clearly distinguish reported conversions from verified Shopify orders. Do not change live campaigns; provide a prioritized report with tables and concise recommendations.

## Optimize Budgets Across Ad Campaigns

Identify campaigns that may deserve more or less budget based on performance, conversion costs, product availability, and business priorities.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_GET_RMF_REPORT`, `GOOGLEADS_MUTATE_CAMPAIGN_BUDGETS`

> Review my Google Ads campaigns from the last 30 days and recommend how to allocate my current advertising budget more effectively. Identify campaigns that appear suitable for scaling, campaigns that need further investigation, and campaigns that may be candidates for budget reduction. Consider conversion volume, cost per conversion, search-term relevance, and Shopify inventory and sales data where available. Recommend specific budget amounts and explain the assumptions behind them. Do not change any live budgets until I approve the proposed changes. Present the current budget, recommended budget, expected rationale, and risks in a comparison table.

## Create High-Converting Search Ads

Generate relevant search ad variations using Shopify product information, campaign performance, customer benefits, and existing marketing messages.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_MUTATE_AD_GROUP_ADS`, `GOOGLEADS_GET_RMF_REPORT`

> Help me create new Google Search ads for my Shopify products. Identify products with good sales performance and sufficient inventory, then review relevant existing campaign and keyword data. For each selected product, prepare three responsive search ad concepts with headlines and descriptions, along with suggested keywords and landing pages. Use only product features, prices, discounts, and claims supported by my store data. Check the current Google Ads format requirements where possible. Avoid unsupported promises and misleading claims. Show the proposed ads in a table and wait for my approval before creating or publishing anything in my account.

## Discover Wasteful Search Terms

Find irrelevant or expensive search terms and prepare a negative-keyword plan to improve campaign relevance and reduce wasted spending.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_GET_RMF_REPORT`, `GOOGLEADS_MUTATE_AD_GROUP_CRITERIA`

> Analyze search-term and keyword performance for my Google Ads campaigns over the last 30 days. Identify irrelevant queries, expensive terms with weak results, and search terms that may not match the products sold in my Shopify store. Group your findings into clearly irrelevant terms, terms requiring more data, and potentially valuable terms. Recommend negative keywords with the campaign or ad group where each should apply. Check for possible conflicts with valuable keywords before suggesting exclusions. Show the evidence and expected benefit for each recommendation. Do not add or remove any keywords until I approve the final list.

## Launch Product-Specific Campaigns

Prepare campaign structures for selected Shopify products or collections, including ad groups, targeting, assets, and initial budget recommendations.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_MUTATE_CAMPAIGNS`, `GOOGLEADS_MUTATE_AD_GROUPS`

> Review my Shopify catalog, collections, product availability, and recent sales performance. Identify up to three products or collections that may be suitable for dedicated Google Ads campaigns. For each opportunity, propose a campaign objective, campaign structure, ad groups, keyword themes, headlines, descriptions, relevant assets, targeting settings, and an initial daily budget. Review existing campaigns to avoid unnecessary duplication. Clearly label assumptions, and do not invent product claims or promotional offers. Prepare the proposed configuration for my review, but do not create, enable, or publish campaigns until I approve the complete setup.

## Fix Conversion Tracking Problems

Review conversion action configuration and ingestion status to help identify tracking gaps, misconfigured purchase events, or unreliable conversion reporting.

- Apps: Google Ads, Shopify
- Tools: `GOOGLEADS_LIST_DATA_MANAGER_CONVERSION_ACTIONS`, `GOOGLEADS_GET_CONVERSION_INGESTION_STATUS`, `GOOGLEADS_GET_CONVERSION_ACTION_TAG_SNIPPETS`

> Audit my Google Ads conversion tracking configuration. List the available conversion actions, identify the purchase-related actions, and review relevant conversion ingestion status where supported. Check for possible duplicate purchase conversions, missing configuration details, inactive actions, or inconsistencies between reported advertising conversions and Shopify order data. If website or call tracking snippets are available, retrieve them and explain where they belong without exposing secrets. Recommend a validation plan and distinguish confirmed issues from potential issues. Do not modify conversion actions or submit conversion events without my approval.

## Build Customer Remarketing Audiences

Organize eligible customer segments into advertising audiences using permitted customer data and appropriate consent and platform requirements.

- Apps: Google Ads, Shopify, Gmail
- Tools: `GOOGLEADS_GET_CUSTOMER_LISTS`, `GOOGLEADS_CREATE_CUSTOMER_LIST`, `GOOGLEADS_ADD_OR_REMOVE_TO_CUSTOMER_LIST`

> Help me plan customer remarketing audiences for my Shopify store. Review the customer lists currently available in Google Ads and identify opportunities for segments such as past purchasers, repeat customers, and eligible high-value customers. Use only customer data that I am authorized to process and that meets applicable consent, privacy, and platform requirements. Propose useful audience names, inclusion and exclusion rules, and suitable campaign objectives. If Gmail contains relevant campaign plans or customer-segmentation discussions, include those in the recommendation. Show the proposed audience structure and explain any data requirements. Do not upload, remove, or modify customer-list membership until I approve the exact changes.

## Coordinate Marketing With Gmail

Turn campaign reports, partner recommendations, supplier updates, and marketing requests into an organized advertising action plan.

- Apps: Google Ads, Gmail, Shopify
- Tools: `GOOGLEADS_GET_RMF_REPORT`

> Review my recent Gmail messages for Google Ads reports, marketing agency recommendations, promotional plans, tracking issues, and supplier updates relevant to my Shopify products. Compare the recommendations with actual Google Ads performance and available Shopify inventory and sales data. Identify which suggestions are supported by evidence, which require further investigation, and which may create stock or profitability risks. Prepare a prioritized action plan with the source email, relevant campaign or product, recommended action, and reason. Draft replies to relevant partners when useful, but do not send emails or change campaigns without my approval.

## Track Promotions and Product Availability

Coordinate advertising campaigns with Shopify stock levels, upcoming promotions, supplier replenishment, and campaign assets to reduce avoidable advertising and fulfillment problems.

- Apps: Google Ads, Shopify, Gmail
- Tools: `GOOGLEADS_GET_RMF_REPORT`, `GOOGLEADS_MUTATE_CAMPAIGN_ASSETS`

> Review my active Google Ads campaigns and identify the products they appear to promote. Compare them with current Shopify inventory, product availability, prices, and active promotional details. Check Gmail for upcoming discounts, supplier restock dates, and promotion deadlines. Flag campaigns promoting unavailable products, products with low inventory, or offers that may no longer be valid. Recommend whether each campaign should remain unchanged, be reviewed, or be prepared for a future update. Explain any uncertainty in matching campaigns to products. Do not pause campaigns, change budgets, modify ads, or publish promotional assets without my approval.

## Generate a Daily Advertising Brief

Create a concise marketing report combining advertising results, product performance, tracking status, and important email updates.

- Apps: Google Ads, Shopify, Gmail
- Tools: `GOOGLEADS_GET_RMF_REPORT`, `GOOGLEADS_SEARCH_STREAM_GAQL`

> Prepare a daily Google Ads and Shopify marketing brief using the latest available data. Include spend, impressions, clicks, conversions, cost per conversion, campaign-level highlights, significant keyword or search-term changes, and conversion tracking warnings where available. Compare advertising performance with Shopify orders, product sales, and inventory when the data can be reliably matched. Review Gmail for relevant marketing emails, partner updates, tracking notifications, and promotion deadlines. Highlight the three most important actions for today, with the reason and supporting evidence for each. Separate measured results from estimates and recommendations. Format the report with metric cards, compact tables, and a short prioritized action list. Do not make changes to campaigns or send emails automatically.
