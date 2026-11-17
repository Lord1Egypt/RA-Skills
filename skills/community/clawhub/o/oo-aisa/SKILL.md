---
name: oo-aisa
description: "AIsa (aisa.one). Use this skill for ANY AIsa request — reading, creating, updating, and deleting data. Whenever a task involves AIsa, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AIsa"
  author: "OOMOL"
  version: "1.0.5"
  services: ["aisa"]
  icon: "https://static.oomol.com/logo/third-party/aisa.svg"
---

# AIsa

Operate **AIsa** through your OOMOL-connected account. This skill calls the `aisa` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AIsa. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "aisa" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "aisa" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `answer_exa` — Answer a question using Exa web retrieval with source citations and optional structured output.
- `cancel_firecrawl_batch_scrape` — Request cancellation of a Firecrawl task. Work already performed may still be charged; poll the task for final state and pricing. [destructive]
- `cancel_firecrawl_crawl` — Request cancellation of a Firecrawl task. Work already performed may still be charged; poll the task for final state and pricing. [destructive]
- `compare_semrush_domains` — Compare organic or paid keyword portfolios across domains.
- `crawl_tavily` — Synchronously crawl a website through Tavily and return page content. Set limit, depth and breadth to bound the crawl; this does not create a background job.
- `enrich_akta_company` — Retrieve Akta company profile sections, including firmographics, management, products, and financial estimates.
- `enrich_apollo_organization` — Enrich one organization from its domain using Apollo's global database.
- `enrich_apollo_organizations` — Enrich multiple organizations from their domains in one Apollo request.
- `enrich_apollo_people` — Enrich up to ten people from known identifiers in one Apollo request.
- `enrich_apollo_person` — Enrich one person from known identifiers using Apollo's global database.
- `extract_tavily` — Extract content from known URLs through Tavily. Inspect failed_results for per-URL failures; use crawl_tavily to discover and retrieve pages from a website.
- `find_foreplay_brands` — Find candidate advertising brands associated with a domain.
- `find_similar_creators` — Find creators similar to a seed account with optional audience filters.
- `get_ahrefs_domain_rating` — Get Ahrefs Domain Rating and Ahrefs Rank for a domain on a specified date.
- `get_ahrefs_site_metrics` — Get Ahrefs organic and paid keyword counts, traffic, and traffic value for a domain.
- `get_analyst_estimates` — Get analyst estimates for a ticker and reporting period.
- `get_apollo_job_postings` — List live job postings for an Apollo organization.
- `get_apollo_organization` — Get one complete organization record from Apollo's global database.
- `get_balance_sheets` — Get standardized balance sheets for a company.
- `get_cash_flow_statements` — Get standardized cash-flow statements for a company.
- `get_company_facts` — Get standardized SEC company facts by ticker or CIK.
- `get_company_news` — Get recent financial news, optionally filtered by ticker.
- `get_credits_balance` — Get the current AIsa account, key, and go-to-market credit balances.
- `get_crypto_coin` — Get metadata, market data, and community signals for one coin.
- `get_crypto_market_chart` — Get price, market-cap, and volume history for a coin over a Unix-time range.
- `get_crypto_news` — Get recent cryptocurrency news with optional coin and language filters.
- `get_crypto_ohlc` — Get open, high, low, and close price candles for one coin.
- `get_crypto_prices` — Get current prices and optional market metrics for multiple coins.
- `get_dataforseo_ai_gemini_search` — Get Gemini search answers through DataForSEO.
- `get_dataforseo_ai_keyword_volume` — Get AI-search volume estimates for up to 1,000 keywords.
- `get_dataforseo_ai_mentions_top_brands` — Get AI mentioned brands through DataForSEO.
- `get_dataforseo_ai_mentions_top_pages` — Get AI cited pages through DataForSEO.
- `get_dataforseo_amazon_asin` — Get Amazon product details through DataForSEO.
- `get_dataforseo_amazon_products` — Get Amazon product search results through DataForSEO.
- `get_dataforseo_amazon_sellers` — Get Amazon product sellers through DataForSEO.
- `get_dataforseo_app_store_listings` — Get App Store listings through DataForSEO.
- `get_dataforseo_backlinks_bulk_spam_score` — Get bulk backlink spam scores through DataForSEO.
- `get_dataforseo_backlinks_domain_pages_summary` — Get page backlink summaries through DataForSEO.
- `get_dataforseo_backlinks_page_intersection` — Get referring page intersections through DataForSEO.
- `get_dataforseo_backlinks_referring_domains` — Get referring domains through DataForSEO.
- `get_dataforseo_content_category_trends` — Get content category trends through DataForSEO.
- `get_dataforseo_content_phrase_trends` — Get content mention trends through DataForSEO.
- `get_dataforseo_content_sentiment` — Get content sentiment through DataForSEO.
- `get_dataforseo_google_business_info` — Get Google Business profiles through DataForSEO.
- `get_dataforseo_google_business_questions` — Get Google Business questions and answers through DataForSEO.
- `get_dataforseo_keyword_trends` — Compare popularity over time for up to five keywords using DataForSEO Trends for Google Search, News, or Shopping. These are DataForSEO estimates, not original Google Trends data or absolute search volumes.
- `get_dataforseo_keywords_bing_keywords_for_site` — Get Bing keywords for a website through DataForSEO.
- `get_dataforseo_labs_amazon_bulk_search_volume` — Get Amazon search volumes through DataForSEO.
- `get_dataforseo_labs_amazon_product_competitors` — Get Amazon product competitors through DataForSEO.
- `get_dataforseo_labs_amazon_product_keyword_intersections` — Get Amazon keyword intersections through DataForSEO.
- `get_dataforseo_labs_amazon_product_rank_overview` — Get Amazon product rank overview through DataForSEO.
- `get_dataforseo_labs_amazon_ranked_keywords` — Get Amazon ranked keywords through DataForSEO.
- `get_dataforseo_labs_amazon_related_keywords` — Get Amazon related keywords through DataForSEO.
- `get_dataforseo_labs_app_store_app_competitors` — Get App Store competitors through DataForSEO.
- `get_dataforseo_labs_app_store_bulk_app_metrics` — Get App Store app metrics through DataForSEO.
- `get_dataforseo_labs_app_store_keywords_for_app` — Get App Store app keywords through DataForSEO.
- `get_dataforseo_labs_bulk_keyword_difficulty` — Get Google keyword difficulty through DataForSEO.
- `get_dataforseo_labs_competitors_domain` — Get Google domain competitors through DataForSEO.
- `get_dataforseo_labs_domain_metrics_by_categories` — Get Google domain metrics by category through DataForSEO.
- `get_dataforseo_labs_google_play_app_competitors` — Get Google Play competitors through DataForSEO.
- `get_dataforseo_labs_google_play_app_intersection` — Get Google Play keyword intersections through DataForSEO.
- `get_dataforseo_labs_keyword_ideas` — Get Google keyword ideas through DataForSEO.
- `get_dataforseo_labs_keyword_overview` — Get Google keyword overview through DataForSEO.
- `get_dataforseo_labs_keywords_for_categories` — Get Google category keywords through DataForSEO.
- `get_dataforseo_llm_mention_metrics` — Aggregate LLM mention metrics for domains and keyword entities.
- `get_dataforseo_llm_mention_top_domains` — Get domains cited most often in LLM responses matching target entities.
- `get_dataforseo_onpage_lighthouse` — Get Lighthouse audits through DataForSEO.
- `get_dataforseo_reference_data` — Look up DataForSEO model names, location codes, categories, or supported filter fields before a research query.
- `get_dataforseo_serp_google_ai_mode` — Get Google AI Mode answers through DataForSEO.
- `get_dataforseo_serp_google_finance_markets` — Get Google Finance markets through DataForSEO.
- `get_dataforseo_serp_google_finance_quote` — Get Google Finance quotes through DataForSEO.
- `get_dataforseo_serp_google_images` — Get Google image search results through DataForSEO.
- `get_dataforseo_serp_google_local_finder` — Get Google local search results through DataForSEO.
- `get_dataforseo_serp_google_news` — Get Google news results through DataForSEO.
- `get_dataforseo_serp_youtube_comments` — Get YouTube comments through DataForSEO.
- `get_dataforseo_serp_youtube_organic` — Get YouTube search results through DataForSEO.
- `get_dataforseo_serp_youtube_subtitles` — Get YouTube subtitles through DataForSEO.
- `get_dataforseo_serp_youtube_video_info` — Get YouTube video details through DataForSEO.
- `get_exa_contents` — Retrieve text and metadata for known URLs through Exa. Inspect statuses for per-URL failures, including when other URLs succeed.
- `get_filing_items` — Get selected sections and exhibits from a company filing.
- `get_financial_metrics` — Get historical valuation, profitability, growth, and leverage metrics.
- `get_financial_metrics_snapshot` — Get the latest available financial metrics for a company.
- `get_firecrawl_batch_scrape` — Get a Firecrawl task state and results. Check outputExpired and job errors even when the task has finished.
- `get_firecrawl_crawl` — Get a Firecrawl task state and results. Check outputExpired and job errors even when the task has finished.
- `get_foreplay_brand_ads` — List ads for one or more known Foreplay brand IDs.
- `get_foreplay_brand_analytics` — Get daily running-ad distribution and creative velocity for a brand page.
- `get_income_statements` — Get standardized income statements for a company.
- `get_insider_trades` — List reported insider transactions for a ticker.
- `get_kalshi_markets` — List Kalshi prediction markets with live quotes, settlement rules, and pagination.
- `get_kalshi_trades` — List executed Kalshi trades with prices, size, side, and pagination.
- `get_polymarket_activity` — Get one wallet's Polymarket split, merge, and redemption activity.
- `get_polymarket_events` — List Polymarket events and their related prediction markets.
- `get_polymarket_markets` — List Polymarket questions with outcome prices, liquidity, volume, and date filters.
- `get_semrush_backlink_anchors` — Get backlink anchor text and backlink counts for a domain or URL.
- `get_semrush_backlink_competitors` — Find domains competing with a target for backlinks.
- `get_semrush_backlinks` — List backlinks pointing to a domain or URL.
- `get_semrush_backlinks_overview` — Get authority, backlink, referring-domain, URL, and IP totals for a root domain.
- `get_semrush_broad_match_keywords` — Find broad-match keyword ideas for a seed phrase.
- `get_semrush_domain_organic_keywords` — List a domain's Google organic keywords with positions, search volume, CPC, and ranking URLs.
- `get_semrush_domain_overview` — Get current Semrush rank, organic keyword, traffic, cost, and paid keyword totals for a domain.
- `get_semrush_domain_rank_history` — Get historical Semrush rank and search-visibility metrics for a domain.
- `get_semrush_indexed_pages` — List pages with backlinks and their backlink counts; this report does not verify Google indexation or live HTTP status.
- `get_semrush_keyword_difficulty` — Get keyword-difficulty scores for up to 20 keywords.
- `get_semrush_keyword_overview` — Get volume, CPC, competition, and result counts for a keyword.
- `get_semrush_organic_competitors` — Find Google organic search competitors with relevance and shared keyword counts.
- `get_semrush_organic_results` — List domains, URLs, and raw SERP feature codes for a keyword in Google organic search.
- `get_semrush_question_keywords` — Find question-form keyword ideas for a seed phrase.
- `get_semrush_referring_domains` — List domains linking to a target domain or URL.
- `get_semrush_url_organic_keywords` — List a landing page's Google organic keywords with positions, search volume, and CPC.
- `get_similarweb_ad_networks` — List display-ad networks associated with a website.
- `get_similarweb_audience_interests` — List topics and categories that interest a website's audience.
- `get_similarweb_audience_overlap` — Compare duplicated and exclusive audiences across two to five websites.
- `get_similarweb_deduplicated_audience` — Get deduplicated desktop and mobile-web audience measurements.
- `get_similarweb_demographics` — Get age and gender distributions for a website's audience in one month.
- `get_similarweb_keyword_competitors` — List domains competing with a website for organic and paid search clicks.
- `get_similarweb_landing_pages` — List pages receiving organic or paid search traffic for a website.
- `get_similarweb_marketing_channels` — Get direct, search, social, referral, mail, and display traffic shares.
- `get_similarweb_popular_pages` — List the pages that receive the most traffic on a website.
- `get_similarweb_ppc_spend` — Get estimated monthly paid-search spending for a website.
- `get_similarweb_ranking` — Get monthly global, country, and category rankings for a website.
- `get_similarweb_referrals` — List websites that send referral traffic to the target domain.
- `get_similarweb_serp_players_aggregated` — Compare domains capturing the most search clicks for a keyword.
- `get_similarweb_serp_players_timeseries` — Track how search clicks shift among domains competing for a keyword over time.
- `get_similarweb_similar_sites` — List websites whose audience and traffic profile resemble a target website.
- `get_similarweb_subdomains` — List the subdomains that receive traffic for a website.
- `get_similarweb_technologies` — List technologies detected on a website for the latest available month.
- `get_similarweb_top_geographies` — Get the top countries by share of a website's traffic for the latest month.
- `get_similarweb_top_sites` — List the highest-ranked websites in an industry category.
- `get_similarweb_traffic_engagement` — Get monthly visits and engagement metrics for a website from Similarweb.
- `get_similarweb_traffic_snapshot` — Get the latest visits and engagement snapshot for a website.
- `get_similarweb_traffic_trend` — Get the recent monthly traffic trend for a website.
- `get_similarweb_website_keywords` — List organic and paid keywords that send search traffic to a website.
- `get_stock_earnings` — Get the most recent earnings snapshot for a ticker.
- `get_stock_price_snapshot` — Get the latest available market-price snapshot for a ticker.
- `get_stock_prices` — Get historical market prices for a ticker and date range.
- `get_token_data` — Get CoinGecko metadata and market data for a token contract.
- `get_token_prices` — Get current prices for token contracts on one asset platform.
- `get_trending_crypto` — Get coins, NFTs, and categories currently trending on CoinGecko.
- `get_twitter_mentions` — Get public posts mentioning a Twitter username in an optional time window.
- `get_twitter_post_replies` — List public replies to a Twitter post.
- `get_twitter_posts` — Get public Twitter posts by their IDs.
- `get_twitter_thread` — Get the public conversation context surrounding a Twitter post.
- `get_twitter_trends` — Get public Twitter trends for a Where On Earth location.
- `get_twitter_user` — Get a public Twitter profile by username through AIsa.
- `get_twitter_user_recent_posts` — Get a public Twitter user's most recent posts by ID or username.
- `get_twitter_user_timeline` — Get a public Twitter user's post timeline.
- `get_twitter_users` — Get public Twitter profiles for multiple user IDs.
- `get_usage` — Get AIsa request, token, value, and charged usage in daily buckets.
- `list_company_filings` — List SEC filings by ticker, CIK, and filing type.
- `list_crypto_categories` — List cryptocurrency categories and their aggregate market performance.
- `list_crypto_exchanges` — List exchanges ranked by trust score and trading volume.
- `list_crypto_markets` — List coin markets with price, capitalization, volume, and change metrics.
- `lookup_creator_email` — Look up the public contact email for one creator profile; not-found results are billed.
- `map_firecrawl` — Discover website links through Firecrawl. Set limit to bound discovery and usage before retrieving individual pages.
- `query_dataforseo_chatgpt` — Run a live ChatGPT response query for GEO research through DataForSEO.
- `query_dataforseo_claude` — Run a live Claude response query for GEO research through DataForSEO.
- `query_dataforseo_gemini` — Run a live Gemini response query for GEO research through DataForSEO.
- `query_dataforseo_perplexity` — Run a live Perplexity response query for GEO research through DataForSEO.
- `scrape_firecrawl` — Retrieve one HTTPS web page as Markdown through Firecrawl. The AIsa route supports basic proxy mode and excludes PDF URLs.
- `search_akta_companies` — Find Akta companies by name, website, or UUID.
- `search_akta_company_list` — Search an Akta company list using natural language or structured filters, with optional enrichment and pagination.
- `search_akta_industries` — Resolve industry terms to ranked Akta industry codes.
- `search_apollo_company_news` — Search Apollo news articles for known organizations and event categories.
- `search_apollo_organizations` — Search Apollo's global organization database by domain, location, size, and name.
- `search_apollo_people` — Search Apollo's global people database by role, location, employer, and seniority.
- `search_creators` — Find creators from a natural-language brief and optional audience filters.
- `search_dataforseo_llm_mentions` — Search individual LLM mention records for domains and keywords.
- `search_exa` — Search the web semantically through Exa. Request contents to include page text, or retrieve selected URLs with get_exa_contents.
- `search_firecrawl` — Search the web through Firecrawl and return ranked URLs, titles, and snippets.
- `search_foreplay_ads` — Search the Foreplay ad index by text, platform, format, niche, and activity.
- `search_twitter_posts` — Search public Twitter posts using X query syntax and cursor pagination.
- `submit_firecrawl_batch_scrape` — Start a background batch scrape of known URLs through AIsa Firecrawl. Poll the returned task ID for results. [write]
- `submit_firecrawl_crawl` — Start a background website crawl through AIsa Firecrawl. Poll the returned task ID for results. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AIsa state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AIsa is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/aisa
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- AIsa homepage: https://aisa.one
- API documentation: https://aisa.one/docs/zh/api-reference
