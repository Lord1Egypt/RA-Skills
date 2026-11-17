# Google Search Console use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/google-search-console

## Analyze Organic Search Performance

Understand which search queries and pages generate visibility, clicks, and opportunities for improving organic traffic.

- Apps: Google Search Console, Google Analytics, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

> Analyze my Google Search Console performance for the last 28 days and compare it with the previous 28 days. Report clicks, impressions, click-through rate, and average position. Break down the results by query, page, country, device, and search appearance where supported. Identify queries gaining or losing visibility, high-impression queries with relatively low CTR, and pages with meaningful changes in clicks. Compare the findings with Google Analytics organic landing-page behavior and Shopify sales where the data can be reliably matched. Rank the top ten SEO opportunities and explain the evidence behind each recommendation. Present metric cards, comparison tables, and a prioritized action plan.

## Find and Fix Indexing Problems

Inspect important Shopify product and collection URLs to identify indexing issues and prioritize pages that deserve attention.

- Apps: Google Search Console, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP`

> Review important URLs from my Shopify store using Google Search Console. Start with product and collection pages that have strong impressions, meaningful sales, or suspected indexing problems. Inspect their indexing status and summarize the reported reasons for any exclusions or errors. Compare the findings with sitemap information and relevant Shopify URL details where available. Separate confirmed Search Console findings from possible causes that require further investigation. Prioritize pages based on business importance rather than treating every unindexed URL as an error. Recommend specific next steps, but do not claim that an indexing request guarantees inclusion in Google Search.

## Improve Low-CTR Search Pages

Identify pages that appear in search results frequently but attract relatively few clicks, then recommend better search snippets and page alignment.

- Apps: Google Search Console, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

> Analyze Google Search Console queries and pages for the last 28 days. Identify high-impression pages and queries with relatively low click-through rates, taking average position and query intent into account. For each opportunity, identify the relevant Shopify product or collection page and review its available title, description, and content. Propose improved title and meta-description drafts that accurately represent the page and use relevant search language naturally. Avoid unsupported claims, keyword stuffing, or promises of ranking improvements. Show the original issue, supporting metrics, proposed changes, and reasoning. Do not publish any changes automatically.

## Discover Valuable SEO Keywords

Find search queries that could support product-page optimization, collection improvements, and new content opportunities.

- Apps: Google Search Console, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

> Analyze my Search Console query data to identify valuable organic search opportunities for my Shopify store. Find queries with growing impressions, meaningful clicks, relatively strong positions, or potential relevance to products that currently receive limited organic traffic. Group queries by product, collection, informational intent, and purchase intent where the data supports those categories. Compare query opportunities with my Shopify catalog to avoid recommending content for products I do not sell. Identify pages that already rank for related queries and suggest where existing content should be improved before creating new pages. Provide a prioritized keyword-to-page mapping with evidence and recommendations.

## Monitor Sitemap Health

Review submitted sitemaps, submission status, reported errors, warnings, and indexed URL counts to identify issues affecting discoverability.

- Apps: Google Search Console
- Tools: `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`, `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP`

> Review the sitemaps registered for my Shopify store in Google Search Console. Report each sitemap's URL, submission details, indexed and submitted URL counts, latest available timestamps, errors, and warnings where supported. Identify sitemaps with reported problems and explain which issues require investigation. Compare the reported URL counts with the expected product and collection catalog where relevant information is available. Distinguish normal differences between submitted and indexed URLs from confirmed errors. Recommend the exact checks needed before resubmission. Do not delete sitemaps or submit a new sitemap until I approve the intended URL and action.

## Connect SEO Traffic With Shopify Sales

Identify which organic landing pages attract visitors and which appear to contribute to ecommerce performance.

- Apps: Google Search Console, Google Analytics, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`

> Combine Google Search Console query and landing-page data with Google Analytics organic traffic and Shopify sales information where available. Identify pages that generate strong search visibility, clicks, product engagement, and purchases. Highlight pages that receive impressions but few clicks, pages with clicks but weak shopping activity, and products with promising sales but limited organic visibility. Match URLs to products carefully and explain any gaps in the available data. Do not assume Search Console clicks directly equal Analytics sessions or attribute revenue without supporting evidence. Provide a ranked list of SEO and conversion opportunities with the relevant metrics and recommended actions.

## Investigate Organic Traffic Declines

Find which queries, pages, devices, or countries may explain a decline in search clicks and recommend evidence-based investigations.

- Apps: Google Search Console, Google Analytics
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`

> Investigate any decline in Google Search Console clicks or impressions over the last 28 days compared with the previous 28 days. Identify the pages, queries, devices, and countries contributing most to the change where the data supports the comparison. Examine changes in impressions, CTR, and average position to distinguish visibility changes from click-through changes. Inspect important affected URLs for indexing issues and compare organic landing-page behavior in Google Analytics where available. Do not assume a Google algorithm update or technical error without evidence. Provide the largest contributing changes, likely explanations with confidence levels, and a prioritized diagnostic plan.

## Improve Product and Collection SEO

Use search performance and Shopify catalog information to prioritize product and collection pages for better search relevance.

- Apps: Google Search Console, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`

> Review Google Search Console performance for my Shopify product and collection pages. Identify pages with weak visibility, declining clicks, high impressions but low CTR, or queries that do not closely match the page's apparent purpose. Compare these findings with available Shopify product titles, descriptions, collection information, and inventory status. Recommend improvements to titles, meta descriptions, product copy, collection copy, and internal links where appropriate. Use only supported product details and natural language. Prioritize pages by their business importance and the evidence available. Prepare proposed content changes for review, but do not edit or publish Shopify pages automatically.

## Validate Important URL Changes

Check the Search Console status of important URLs after product launches, page changes, or SEO updates.

- Apps: Google Search Console, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_INSPECT_URL`, `GOOGLE_SEARCH_CONSOLE_GET_SITEMAP`

> Help me validate important Shopify URLs after a product launch or SEO update. Inspect the specified URLs in Google Search Console and summarize their indexing status and available inspection details. Review relevant sitemap information and compare current search performance with the available historical period. Flag pages with indexing issues, unexpected visibility changes, or possible inconsistencies that need further investigation. If a page is not indexed, explain the reported status and recommend the next diagnostic step. Do not claim that inspection or sitemap submission guarantees indexing. Do not delete site properties or change unrelated Search Console settings.

## Generate a Weekly SEO Performance Report

Combine search visibility, indexing health, Analytics behavior, and Shopify sales information into a concise weekly SEO report.

- Apps: Google Search Console, Google Analytics, Shopify
- Tools: `GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, `GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS`

> Prepare a weekly SEO report for my Shopify store using Google Search Console data for the latest seven days and an appropriate comparison period. Include clicks, impressions, CTR, average position, important query changes, top landing pages, indexing issues, and sitemap errors or warnings where available. Compare organic landing-page engagement and Shopify orders or revenue when Google Analytics and store data can be reliably matched. Highlight important product and collection opportunities, traffic declines, and unresolved technical issues. Rank the three most important actions for the coming week and explain the supporting evidence. Clearly distinguish measured results from estimates and recommendations. Format the report with metric cards, compact tables, and a prioritized action list. Do not modify pages, delete site properties, or submit sitemaps automatically.
