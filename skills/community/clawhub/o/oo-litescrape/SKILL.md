---
name: oo-litescrape
description: "Litescrape (litescrape.com). Use this skill for ANY Litescrape request — reading, creating, updating, and deleting data. Whenever a task involves Litescrape, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Litescrape"
  author: "OOMOL"
  version: "1.0.2"
  services: ["litescrape"]
  icon: "https://static.oomol.com/logo/third-party/litescrape.svg"
---

# Litescrape

Operate **Litescrape** through your OOMOL-connected account. This skill calls the `litescrape` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Litescrape. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "litescrape" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "litescrape" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `airbnb_search` — Search Airbnb stays by destination and dates.
- `aliexpress_product` — Get an AliExpress product's details and price. This upstream API is Alpha.
- `aliexpress_search` — Search AliExpress products with prices. This upstream API is Alpha.
- `amazon_autocomplete` — Get Amazon search suggestions for a prefix and department. This upstream API is Alpha.
- `amazon_featured_reviews` — Get the featured reviews for an Amazon product. This upstream API is Alpha.
- `amazon_media_reviews` — Get Amazon reviews that include photos or videos. This upstream API is Alpha.
- `amazon_product` — Get an Amazon product page, with optional seller offers. This upstream API is Alpha.
- `amazon_search` — Search Amazon products. This upstream API is Alpha.
- `apartments_property` — Get an Apartments.com property by URL. This upstream API is Alpha.
- `apartments_search` — Search Apartments.com listings from a search URL. This upstream API is Alpha.
- `apple_app_store_product` — Get an App Store app's details, ratings and version history.
- `apple_app_store_reviews` — Get reviews for an App Store app.
- `apple_app_store_search` — Search the App Store for iPhone, iPad and Mac apps.
- `apple_maps_places` — Search Apple Maps places.
- `apple_maps_reviews` — Get Apple ratings and reviews for an Apple Maps place.
- `ashby_search` — Search jobs on a company's Ashby job board.
- `baidu_search` — Get Baidu search results as JSON.
- `bestbuy_product` — Get a Best Buy product's details, price and availability. This upstream API is Alpha.
- `bestbuy_search` — Search Best Buy products with prices and availability. This upstream API is Alpha.
- `bing_images` — Search Bing Images with size, color, date and license filters.
- `bing_maps` — Search Bing Maps places, or get one place by ID.
- `bing_product` — Get a Bing Shopping product's details using its product token.
- `bing_search` — Get Bing web search results.
- `bing_shopping` — Search Bing Shopping products.
- `brave_ai_mode` — Get Brave AI answers with citations.
- `brave_search` — Get Brave web search results.
- `copilot_chat_completions` — Text completions through Microsoft Copilot. This upstream API is Alpha.
- `create_checkout` — Create a credit-purchase checkout URL. Payment completes only after opening and completing checkout. [write]
- `disable_auto_top_up` — Disable automatic credit charges. [destructive]
- `duckduckgo_maps` — Search DuckDuckGo Maps places within a map area.
- `duckduckgo_search` — Get DuckDuckGo web search results.
- `ebay_product` — Get an eBay listing by item ID.
- `ebay_search` — Search eBay listings by keyword or category.
- `ebay_seller` — Get an eBay seller's profile and listings.
- `etsy_product` — Get an Etsy listing's details and price. This upstream API is Alpha.
- `etsy_search` — Search Etsy listings with prices. This upstream API is Alpha.
- `eventbrite_search` — Search Eventbrite events by location and keyword.
- `facebook_hashtag_posts` — Get public Facebook posts for a hashtag. This upstream API is Alpha.
- `facebook_marketplace_browse` — Browse or search Facebook Marketplace listings by city. This upstream API is Alpha.
- `facebook_page_posts` — Get recent public posts from a Facebook Page. This upstream API is Alpha.
- `facebook_post` — Get a public Facebook post by its URL. This upstream API is Alpha.
- `facebook_reel` — Get a public Facebook reel by its URL. This upstream API is Alpha.
- `facebook_search_pages` — Search public Facebook Pages by name. This upstream API is Alpha.
- `facebook_search_profiles` — Search public Facebook profiles by name. This upstream API is Alpha.
- `find_tools` — Find relevant data tools or retrieve their input schemas by name.
- `get_auto_top_up` — Read automatic top-up settings.
- `get_email_bonus` — Read email bonus eligibility and claim status; this does not claim the bonus.
- `get_job` — Read asynchronous job state and its retained response. Failed jobs return their original status_code and error response.
- `get_key_status` — Read key status, balance, concurrency and retention settings without a paid search.
- `get_usage` — Read account usage for a time range and timezone.
- `glassdoor_search` — Search Glassdoor jobs by keyword and location, with salary, seniority and remote filters.
- `google_ads` — Get the ads shown on a Google search results page. This upstream API is Alpha.
- `google_ai_mode` — Get Google AI Mode answers with cited sources.
- `google_ai_overview` — Get Google's AI Overview for a query, with cited sources.
- `google_contributor_reviews` — Get reviews written by a Google Maps contributor.
- `google_gemini` — Get a completed text reply from Gemini.
- `google_images` — Search Google Images.
- `google_jobs` — Search Google Jobs listings by query and location.
- `google_local` — Get Google local results for a query and location.
- `google_maps` — Search Google Maps places, or get one place by ID.
- `google_maps_photo_meta` — Get the place, contributor, and date of a Maps photo.
- `google_maps_popular_times` — See how busy a place is right now.
- `google_maps_posts` — Read the posts published by a business.
- `google_play_apps` — Search and browse Google Play apps.
- `google_play_books` — Search and browse Google Play ebooks and audiobooks.
- `google_play_games` — Browse Google Play games by category and chart.
- `google_play_movies` — Search and browse Google Play movies and TV shows.
- `google_play_product` — Get a Google Play app, book, movie or show by ID.
- `google_play_reviews` — Get reviews for a Google Play app.
- `google_reviews` — Get reviews for a Google Maps place.
- `google_search` — Get Google search results, including the AI Overview and People also ask.
- `google_shopping` — Search Google Shopping products.
- `google_shopping_merchant_urls` — Get direct merchant URLs for Google Shopping offers.
- `google_shopping_product` — Get every merchant offer for a Google Shopping product.
- `homedepot_product` — Get a Home Depot product's details, price and availability. This upstream API is Alpha.
- `homedepot_search` — Search Home Depot products with prices and availability. This upstream API is Alpha.
- `homes_property` — Get a Homes.com property by URL. This upstream API is Alpha.
- `homes_search` — Search Homes.com listings from a search URL. This upstream API is Alpha.
- `ikea_product` — Get an IKEA product's details, price and availability. This upstream API is Alpha.
- `ikea_search` — Search IKEA products with prices and availability. This upstream API is Alpha.
- `indeed_search` — Search Indeed jobs by keyword and location, with salary, experience and remote filters.
- `instagram_embed` — Retrieve public Instagram embed data. This upstream API is Alpha.
- `instagram_post` — Retrieve public Instagram post data. This upstream API is Alpha.
- `instagram_posts` — Retrieve public Instagram posts data. This upstream API is Alpha.
- `instagram_profile` — Retrieve public Instagram profile data. This upstream API is Alpha.
- `instagram_profile_post_count` — Retrieve public Instagram profile post count data. This upstream API is Alpha.
- `instagram_search_popular` — Get popular Instagram posts for a search topic. This upstream API is Alpha.
- `kroger_product` — Get a Kroger product's details, price and availability. This upstream API is Alpha.
- `kroger_search` — Search Kroger products with prices and availability. This upstream API is Alpha.
- `levels_search` — Search Levels.fyi jobs by company, location, level and pay.
- `naver_ai_overview` — Get Naver AI Briefing answers with citations.
- `naver_search` — Search Naver web, news, video and image results.
- `realtor_property` — Get a Realtor.com property by URL. This upstream API is Alpha.
- `realtor_search` — Search Realtor.com listings from a search URL. This upstream API is Alpha.
- `redfin_property` — Get a Redfin property by listing URL.
- `redfin_search` — Search Redfin homes for sale or recently sold.
- `rotate_key` — Replace the API key and immediately invalidate the current key. Save the returned key and reconnect before making another request. [destructive]
- `set_zero_data_retention` — Enable or disable zero data retention. Enabling it deletes completed batch results and disables new asynchronous jobs and screenshots. Active batch jobs must finish first. [destructive]
- `setup_auto_top_up` — Create a checkout URL to authorize automatic top-ups. Complete card authorization at the returned URL. [write]
- `sprouts_product` — Get a Sprouts product's details, price and availability. This upstream API is Alpha.
- `sprouts_search` — Search Sprouts products with prices and availability. This upstream API is Alpha.
- `submit_airbnb_search` — Submit asynchronously: Search Airbnb stays by destination and dates. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_aliexpress_product` — Submit asynchronously: Get an AliExpress product's details and price. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_aliexpress_search` — Submit asynchronously: Search AliExpress products with prices. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_amazon_autocomplete` — Submit asynchronously: Get Amazon search suggestions for a prefix and department. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_amazon_featured_reviews` — Submit asynchronously: Get the featured reviews for an Amazon product. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_amazon_media_reviews` — Submit asynchronously: Get Amazon reviews that include photos or videos. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_amazon_product` — Submit asynchronously: Get an Amazon product page, with optional seller offers. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_amazon_search` — Submit asynchronously: Search Amazon products. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apartments_property` — Submit asynchronously: Get an Apartments.com property by URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apartments_search` — Submit asynchronously: Search Apartments.com listings from a search URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apple_app_store_product` — Submit asynchronously: Get an App Store app's details, ratings and version history. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apple_app_store_reviews` — Submit asynchronously: Get reviews for an App Store app. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apple_app_store_search` — Submit asynchronously: Search the App Store for iPhone, iPad and Mac apps. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apple_maps_places` — Submit asynchronously: Search Apple Maps places. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_apple_maps_reviews` — Submit asynchronously: Get Apple ratings and reviews for an Apple Maps place. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ashby_search` — Submit asynchronously: Search jobs on a company's Ashby job board. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_baidu_search` — Submit asynchronously: Get Baidu search results as JSON. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bestbuy_product` — Submit asynchronously: Get a Best Buy product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bestbuy_search` — Submit asynchronously: Search Best Buy products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bing_images` — Submit asynchronously: Search Bing Images with size, color, date and license filters. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bing_maps` — Submit asynchronously: Search Bing Maps places, or get one place by ID. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bing_product` — Submit asynchronously: Get a Bing Shopping product's details using its product token. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bing_search` — Submit asynchronously: Get Bing web search results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_bing_shopping` — Submit asynchronously: Search Bing Shopping products. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_brave_ai_mode` — Submit asynchronously: Get Brave AI answers with citations. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_brave_search` — Submit asynchronously: Get Brave web search results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_copilot_chat_completions` — Submit asynchronously: Text completions through Microsoft Copilot. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_duckduckgo_maps` — Submit asynchronously: Search DuckDuckGo Maps places within a map area. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_duckduckgo_search` — Submit asynchronously: Get DuckDuckGo web search results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ebay_product` — Submit asynchronously: Get an eBay listing by item ID. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ebay_search` — Submit asynchronously: Search eBay listings by keyword or category. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ebay_seller` — Submit asynchronously: Get an eBay seller's profile and listings. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_etsy_product` — Submit asynchronously: Get an Etsy listing's details and price. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_etsy_search` — Submit asynchronously: Search Etsy listings with prices. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_eventbrite_search` — Submit asynchronously: Search Eventbrite events by location and keyword. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_hashtag_posts` — Submit asynchronously: Get public Facebook posts for a hashtag. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_marketplace_browse` — Submit asynchronously: Browse or search Facebook Marketplace listings by city. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_page_posts` — Submit asynchronously: Get recent public posts from a Facebook Page. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_post` — Submit asynchronously: Get a public Facebook post by its URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_reel` — Submit asynchronously: Get a public Facebook reel by its URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_search_pages` — Submit asynchronously: Search public Facebook Pages by name. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_facebook_search_profiles` — Submit asynchronously: Search public Facebook profiles by name. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_feedback` — Submit an explicitly requested rating about a previous result. Each feedback token expires after seven days and accepts one rating. [write]
- `submit_glassdoor_search` — Submit asynchronously: Search Glassdoor jobs by keyword and location, with salary, seniority and remote filters. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_ads` — Submit asynchronously: Get the ads shown on a Google search results page. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_ai_mode` — Submit asynchronously: Get Google AI Mode answers with cited sources. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_ai_overview` — Submit asynchronously: Get Google's AI Overview for a query, with cited sources. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_contributor_reviews` — Submit asynchronously: Get reviews written by a Google Maps contributor. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_gemini` — Submit asynchronously: Get a completed text reply from Gemini. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_images` — Submit asynchronously: Search Google Images. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_jobs` — Submit asynchronously: Search Google Jobs listings by query and location. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_local` — Submit asynchronously: Get Google local results for a query and location. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_maps` — Submit asynchronously: Search Google Maps places, or get one place by ID. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_maps_photo_meta` — Submit asynchronously: Get the place, contributor, and date of a Maps photo. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_maps_popular_times` — Submit asynchronously: See how busy a place is right now. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_maps_posts` — Submit asynchronously: Read the posts published by a business. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_apps` — Submit asynchronously: Search and browse Google Play apps. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_books` — Submit asynchronously: Search and browse Google Play ebooks and audiobooks. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_games` — Submit asynchronously: Browse Google Play games by category and chart. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_movies` — Submit asynchronously: Search and browse Google Play movies and TV shows. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_product` — Submit asynchronously: Get a Google Play app, book, movie or show by ID. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_play_reviews` — Submit asynchronously: Get reviews for a Google Play app. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_reviews` — Submit asynchronously: Get reviews for a Google Maps place. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_search` — Submit asynchronously: Get Google search results, including the AI Overview and People also ask. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_shopping` — Submit asynchronously: Search Google Shopping products. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_shopping_merchant_urls` — Submit asynchronously: Get direct merchant URLs for Google Shopping offers. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_google_shopping_product` — Submit asynchronously: Get every merchant offer for a Google Shopping product. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_homedepot_product` — Submit asynchronously: Get a Home Depot product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_homedepot_search` — Submit asynchronously: Search Home Depot products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_homes_property` — Submit asynchronously: Get a Homes.com property by URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_homes_search` — Submit asynchronously: Search Homes.com listings from a search URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ikea_product` — Submit asynchronously: Get an IKEA product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ikea_search` — Submit asynchronously: Search IKEA products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_indeed_search` — Submit asynchronously: Search Indeed jobs by keyword and location, with salary, experience and remote filters. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_embed` — Submit asynchronously: Retrieve public Instagram embed data. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_post` — Submit asynchronously: Retrieve public Instagram post data. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_posts` — Submit asynchronously: Retrieve public Instagram posts data. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_profile` — Submit asynchronously: Retrieve public Instagram profile data. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_profile_post_count` — Submit asynchronously: Retrieve public Instagram profile post count data. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_instagram_search_popular` — Submit asynchronously: Get popular Instagram posts for a search topic. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_kroger_product` — Submit asynchronously: Get a Kroger product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_kroger_search` — Submit asynchronously: Search Kroger products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_levels_search` — Submit asynchronously: Search Levels.fyi jobs by company, location, level and pay. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_naver_ai_overview` — Submit asynchronously: Get Naver AI Briefing answers with citations. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_naver_search` — Submit asynchronously: Search Naver web, news, video and image results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_realtor_property` — Submit asynchronously: Get a Realtor.com property by URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_realtor_search` — Submit asynchronously: Search Realtor.com listings from a search URL. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_redfin_property` — Submit asynchronously: Get a Redfin property by listing URL. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_redfin_search` — Submit asynchronously: Search Redfin homes for sale or recently sold. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_sprouts_product` — Submit asynchronously: Get a Sprouts product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_sprouts_search` — Submit asynchronously: Search Sprouts products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_target_product` — Submit asynchronously: Get a product sold by the US retailer Target, with its details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_target_search` — Submit asynchronously: Search products sold by the US retailer Target, with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_collection_videos` — Submit asynchronously: Page through posts saved in a public TikTok collection. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_comment_replies` — Submit asynchronously: Page through replies to a TikTok comment. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_comments` — Submit asynchronously: Page through public comments on a TikTok post. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_followers` — Submit asynchronously: Page through public followers of a TikTok user. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_following` — Submit asynchronously: Page through the public accounts a TikTok user follows. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_live` — Submit asynchronously: Get a TikTok live room's status and metrics. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_profile` — Submit asynchronously: Get public TikTok profile fields and statistics by handle or numeric user ID. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_profile_videos` — Submit asynchronously: Page through posts from a public TikTok profile by handle or numeric user ID. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_search_hashtag` — Submit asynchronously: Resolve a public hashtag and page through its posts. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_search_keyword` — Submit asynchronously: Search public TikTok posts by keyword with pagination and search-session IDs. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_search_suggestions` — Submit asynchronously: Get public TikTok autocomplete suggestions in order. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_search_top` — Submit asynchronously: Get TikTok's top search results. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_song` — Submit asynchronously: Get a TikTok sound's details and usage count. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_song_videos` — Submit asynchronously: Page through TikTok posts that use a sound. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_transcript` — Submit asynchronously: Get public TikTok captions with timed segments. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_trending_feed` — Submit asynchronously: Get TikTok's trending feed. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_user_live` — Submit asynchronously: Get a TikTok user's live status and room metadata. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tiktok_video` — Submit asynchronously: Get a TikTok video or photo post with its media and metrics. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tripadvisor_place` — Submit asynchronously: Get a Tripadvisor place by ID. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tripadvisor_reviews` — Submit asynchronously: Get reviews for a Tripadvisor place. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_tripadvisor_search` — Submit asynchronously: Search Tripadvisor hotels, restaurants and attractions. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_walmart_product` — Submit asynchronously: Get a Walmart product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_walmart_search` — Submit asynchronously: Search Walmart products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_wayfair_product` — Submit asynchronously: Get a Wayfair product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_wayfair_search` — Submit asynchronously: Search Wayfair products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_web_fetch` — Submit asynchronously: Get a web page as Markdown, HTML or plain text. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [destructive]
- `submit_web_screenshot` — Submit asynchronously: Take a screenshot of a web page. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [destructive]
- `submit_wholefoods_product` — Submit asynchronously: Get a Whole Foods product's details, price and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_wholefoods_search` — Submit asynchronously: Search Whole Foods products with prices and availability. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_x_community` — Submit asynchronously: Get X community details, including its creator, member count and rules. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_x_community_posts` — Submit asynchronously: Get posts from an X community, including authors, engagement and media. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_x_post` — Submit asynchronously: Get an X post with its text, author, engagement counts and media. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_x_profile` — Submit asynchronously: Get a public X profile, including its bio, follower counts and profile images. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_x_user_posts` — Submit asynchronously: Get posts from an X user. This upstream API is Alpha. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yahoo_images` — Submit asynchronously: Search Yahoo Images. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yahoo_search` — Submit asynchronously: Get Yahoo web search results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yandex_images` — Submit asynchronously: Search Yandex Images, including reverse image search. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yandex_search` — Submit asynchronously: Get Yandex web search results. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yelp_place` — Submit asynchronously: Get a Yelp business's details and menu. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yelp_reviews` — Submit asynchronously: Get reviews for a Yelp business. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_yelp_search` — Submit asynchronously: Search Yelp businesses by location and category. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_youtube_channel` — Submit asynchronously: Get a YouTube channel's profile, videos, Shorts, playlists and posts. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_youtube_search` — Submit asynchronously: Search YouTube videos, channels, playlists and Shorts. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_zillow_locations` — Submit asynchronously: Get Zillow region and address suggestions. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_zillow_property` — Submit asynchronously: Get a Zillow property by ID or URL. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_zillow_search` — Submit asynchronously: Search Zillow homes for sale, for rent or recently sold. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `submit_ziprecruiter_search` — Submit asynchronously: Search ZipRecruiter jobs in the US and Canada by keyword and location. Reuse idempotencyKey for retries. Results expire after 24 hours; zero data retention accounts cannot submit or poll retained jobs. [write]
- `target_product` — Get a product sold by the US retailer Target, with its details, price and availability. This upstream API is Alpha.
- `target_search` — Search products sold by the US retailer Target, with prices and availability. This upstream API is Alpha.
- `tiktok_collection_videos` — Page through posts saved in a public TikTok collection. This upstream API is Alpha.
- `tiktok_comment_replies` — Page through replies to a TikTok comment. This upstream API is Alpha.
- `tiktok_comments` — Page through public comments on a TikTok post. This upstream API is Alpha.
- `tiktok_followers` — Page through public followers of a TikTok user. This upstream API is Alpha.
- `tiktok_following` — Page through the public accounts a TikTok user follows. This upstream API is Alpha.
- `tiktok_live` — Get a TikTok live room's status and metrics. This upstream API is Alpha.
- `tiktok_profile` — Get public TikTok profile fields and statistics by handle or numeric user ID. This upstream API is Alpha.
- `tiktok_profile_videos` — Page through posts from a public TikTok profile by handle or numeric user ID. This upstream API is Alpha.
- `tiktok_search_hashtag` — Resolve a public hashtag and page through its posts. This upstream API is Alpha.
- `tiktok_search_keyword` — Search public TikTok posts by keyword with pagination and search-session IDs. This upstream API is Alpha.
- `tiktok_search_suggestions` — Get public TikTok autocomplete suggestions in order. This upstream API is Alpha.
- `tiktok_search_top` — Get TikTok's top search results. This upstream API is Alpha.
- `tiktok_song` — Get a TikTok sound's details and usage count. This upstream API is Alpha.
- `tiktok_song_videos` — Page through TikTok posts that use a sound. This upstream API is Alpha.
- `tiktok_transcript` — Get public TikTok captions with timed segments. This upstream API is Alpha.
- `tiktok_trending_feed` — Get TikTok's trending feed. This upstream API is Alpha.
- `tiktok_user_live` — Get a TikTok user's live status and room metadata. This upstream API is Alpha.
- `tiktok_video` — Get a TikTok video or photo post with its media and metrics. This upstream API is Alpha.
- `tripadvisor_place` — Get a Tripadvisor place by ID.
- `tripadvisor_reviews` — Get reviews for a Tripadvisor place.
- `tripadvisor_search` — Search Tripadvisor hotels, restaurants and attractions.
- `walmart_product` — Get a Walmart product's details, price and availability. This upstream API is Alpha.
- `walmart_search` — Search Walmart products with prices and availability. This upstream API is Alpha.
- `wayfair_product` — Get a Wayfair product's details, price and availability. This upstream API is Alpha.
- `wayfair_search` — Search Wayfair products with prices and availability. This upstream API is Alpha.
- `web_fetch` — Get a web page as Markdown, HTML or plain text. This upstream API is Alpha. [destructive]
- `web_screenshot` — Take a screenshot of a web page. This upstream API is Alpha. [destructive]
- `wholefoods_product` — Get a Whole Foods product's details, price and availability. This upstream API is Alpha.
- `wholefoods_search` — Search Whole Foods products with prices and availability. This upstream API is Alpha.
- `x_community` — Get X community details, including its creator, member count and rules. This upstream API is Alpha.
- `x_community_posts` — Get posts from an X community, including authors, engagement and media. This upstream API is Alpha.
- `x_post` — Get an X post with its text, author, engagement counts and media. This upstream API is Alpha.
- `x_profile` — Get a public X profile, including its bio, follower counts and profile images. This upstream API is Alpha.
- `x_user_posts` — Get posts from an X user. This upstream API is Alpha.
- `yahoo_images` — Search Yahoo Images.
- `yahoo_search` — Get Yahoo web search results.
- `yandex_images` — Search Yandex Images, including reverse image search.
- `yandex_search` — Get Yandex web search results.
- `yelp_place` — Get a Yelp business's details and menu.
- `yelp_reviews` — Get reviews for a Yelp business.
- `yelp_search` — Search Yelp businesses by location and category.
- `youtube_channel` — Get a YouTube channel's profile, videos, Shorts, playlists and posts.
- `youtube_search` — Search YouTube videos, channels, playlists and Shorts.
- `zillow_locations` — Get Zillow region and address suggestions.
- `zillow_property` — Get a Zillow property by ID or URL.
- `zillow_search` — Search Zillow homes for sale, for rent or recently sold.
- `ziprecruiter_search` — Search ZipRecruiter jobs in the US and Canada by keyword and location.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Litescrape state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Litescrape is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/litescrape
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Litescrape homepage: https://litescrape.com
- API documentation: https://litescrape.com/docs/reference
