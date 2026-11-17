---
name: oo-linkfox
description: "LinkFox (linkfox.com). Use this skill for ANY LinkFox request — reading, creating, and updating data. Whenever a task involves LinkFox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "LinkFox"
  author: "OOMOL"
  version: "1.0.5"
  services: ["linkfox"]
  icon: "https://static.oomol.com/logo/third-party/linkfox.svg"
---

# LinkFox

Operate **LinkFox** through your OOMOL-connected account. This skill calls the `linkfox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected LinkFox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "linkfox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "linkfox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ask_amazon_alexa` — Ask the Amazon Alexa shopping assistant a product discovery question through LinkFox.
- `check_copyright_risk` — Check a product image for copyright risk through LinkFox and Ruiguan.
- `check_design_patent_risk` — Check a product image for design-patent risk through LinkFox and Ruiguan.
- `check_graphic_trademark_risk` — Check a product image for graphic trademark risk through LinkFox and Ruiguan.
- `check_image_policy_compliance` — Check a product image against policy-violating product imagery through LinkFox and Ruiguan.
- `check_product_tro_risk` — Check product images and text for TRO, trademark, copyright, and patent risk through LinkFox and Maidalv.
- `check_text_trademark_risk` — Check product text for trademark risk through LinkFox and Ruiguan.
- `check_utility_patent_risk` — Check product text for utility and invention patent risk through LinkFox and Ruiguan.
- `create_chuhaijiang_image_upload_url` — Create a temporary upload URL for a JPG, JPEG or PNG image through LinkFox and Chuhaijiang. [write]
- `get_1688_product` — Get public product, SKU, price, inventory, media, shipping, and supplier details from 1688 through LinkFox.
- `get_amazon_ads_authorization_url` — Create an Amazon Ads authorization URL through LinkFox.
- `get_amazon_ads_report` — Create or resume an Amazon Ads report and wait for a download URL. [write]
- `get_amazon_opportunity_report` — Generate a LinkFox Amazon commercial opportunity report for a keyword.
- `get_amazon_policy_update` — Get the full content of an Amazon policy or compliance news record through LinkFox.
- `get_amazon_product` — Get detailed Amazon product data for up to forty ASINs through LinkFox.
- `get_amazon_store_authorization_url` — Create an Amazon Selling Partner authorization URL through LinkFox.
- `get_amazon_store_report` — Create or resume an Amazon Selling Partner report and wait for a download URL. [write]
- `get_chuhaijiang_ad` — Get TikTok ad details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_creative` — Get TikTok creative details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_creator` — Get TikTok creator details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_live` — Get TikTok live stream details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_product` — Get TikTok product details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_shop` — Get TikTok shop details through LinkFox and Chuhaijiang.
- `get_chuhaijiang_video` — Get TikTok video details through LinkFox and Chuhaijiang.
- `get_current_account` — Get the current LinkFox account without exposing personal contact data.
- `get_echotik_products` — Get EchoTik details for a batch of TikTok products through LinkFox.
- `get_echotik_seller` — Get detailed public analytics for a TikTok Shop seller through LinkFox and EchoTik.
- `get_echotik_video_download` — Get available playback and download URLs for a TikTok video through LinkFox and EchoTik.
- `get_echotik_videos` — Get EchoTik details for a batch of TikTok videos through LinkFox.
- `get_etsy_product` — Get current public details for one Etsy listing through LinkFox.
- `get_kalodata_product` — Get Kalodata details for a TikTok product through LinkFox.
- `get_mercado_account_usage` — Get the connected supplier account package and usage information through LinkFox.
- `get_mercado_catalog` — Get Mercado Libre catalog product details through LinkFox.
- `get_mercado_catalog_history` — Get Mercado Libre catalog product sales history through LinkFox.
- `get_mercado_category_inventory_types` — Get warehouse type distribution in a Mercado Libre category through LinkFox.
- `get_mercado_category_price_distribution` — Get the price distribution in a Mercado Libre category through LinkFox.
- `get_mercado_category_sales_distribution` — Get the sales distribution in a Mercado Libre category through LinkFox.
- `get_mercado_category_sales_history` — Get sales history for a Mercado Libre category through LinkFox.
- `get_mercado_category_statistics` — Get summary statistics for a Mercado Libre category through LinkFox.
- `get_mercado_exchange_rate` — Get the exchange rate for a Mercado Libre market through LinkFox.
- `get_mercado_item` — Get Mercado Libre product details through LinkFox.
- `get_mercado_item_history` — Get Mercado Libre product sales history through LinkFox.
- `get_mercado_new_item_opportunities` — Get new product opportunities in a Mercado Libre category through LinkFox.
- `get_ozon_product` — Get analytics for one Ozon product through LinkFox and MPSTATS.
- `get_ozon_product_trend` — Get daily analytics trends for one Ozon product through LinkFox and MPSTATS.
- `get_seerfar_ozon_product` — Get an Ozon product snapshot and sales history through LinkFox and Seerfar.
- `get_sif_asin_traffic_summary` — Summarize natural, advertising, and recommendation traffic sources for up to ten Amazon ASINs through LinkFox and SIF.
- `get_sif_keyword_overview` — Get SIF search demand, supply-demand ratio, and advertising or recommendation competition for one Amazon keyword through LinkFox.
- `get_sif_keyword_traffic_summary` — Analyze competitor ASIN traffic shares and natural, advertising, or recommendation exposure for one Amazon keyword through LinkFox and SIF.
- `get_tiktok_shop_product` — Get public details for one TikTok Shop product through LinkFox.
- `get_zhihuiya_patent_abstract_images` — Get patent abstract image URLs through LinkFox and Patsnap.
- `get_zhihuiya_patent_bibliography` — Get detailed patent bibliographic records through LinkFox and Patsnap.
- `get_zhihuiya_patent_citations` — Get patent and non-patent documents cited by the specified patents through LinkFox and Patsnap.
- `get_zhihuiya_patent_cited_by` — Get patents that cite the specified patents and citation counts through LinkFox and Patsnap.
- `get_zhihuiya_patent_claims` — Get original patent claims through LinkFox and Patsnap.
- `get_zhihuiya_patent_descriptions` — Get original patent description sections through LinkFox and Patsnap.
- `get_zhihuiya_patent_families` — Get simple, INPADOC, and Patsnap patent families through LinkFox.
- `get_zhihuiya_patent_fulltext_images` — Get patent full-text image URLs through LinkFox and Patsnap.
- `get_zhihuiya_patent_legal_status` — Get patent legal statuses and events through LinkFox and Patsnap.
- `get_zhihuiya_patent_pdfs` — Get patent PDF download URLs through LinkFox and Patsnap.
- `get_zhihuiya_patent_simple_bibliography` — Get compact patent bibliographic records through LinkFox and Patsnap.
- `list_1688_hot_products` — List high-performing 1688 products from LinkFox rankings.
- `list_amazon_ads_profiles` — List or refresh Amazon Ads profiles through LinkFox.
- `list_amazon_policy_updates` — List recent Amazon policy, regulation, compliance, and marketplace news through LinkFox.
- `list_amazon_product_reviews` — Retrieve Amazon product reviews through LinkFox.
- `list_authorized_amazon_ads_accounts` — List Amazon Ads accounts authorized through LinkFox.
- `list_authorized_amazon_stores` — List Amazon stores authorized through LinkFox.
- `list_chuhaijiang_ad_products` — List products associated with a TikTok ad through LinkFox and Chuhaijiang.
- `list_chuhaijiang_commercial_creators` — List commercial TikTok creator rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_creator_agencies` — List TikTok creator agencies ranked by performance through LinkFox and Chuhaijiang.
- `list_chuhaijiang_creator_lives` — List live streams associated with a TikTok creator through LinkFox and Chuhaijiang.
- `list_chuhaijiang_creator_products` — List products associated with a TikTok creator through LinkFox and Chuhaijiang.
- `list_chuhaijiang_creator_videos` — List videos associated with a TikTok creator through LinkFox and Chuhaijiang.
- `list_chuhaijiang_growing_creators` — List TikTok creator follower-growth rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_live_products` — List products associated with a TikTok live stream through LinkFox and Chuhaijiang.
- `list_chuhaijiang_most_promoted_products` — List most-promoted TikTok product rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_most_promoted_shops` — List most-promoted TikTok shop rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_new_products` — List newly listed TikTok product rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_product_creators` — List creators associated with a TikTok product through LinkFox and Chuhaijiang.
- `list_chuhaijiang_product_lives` — List live streams associated with a TikTok product through LinkFox and Chuhaijiang.
- `list_chuhaijiang_product_reviews` — List TikTok product reviews through LinkFox and Chuhaijiang.
- `list_chuhaijiang_product_videos` — List videos associated with a TikTok product through LinkFox and Chuhaijiang.
- `list_chuhaijiang_shop_creators` — List creators associated with a TikTok shop through LinkFox and Chuhaijiang.
- `list_chuhaijiang_shop_products` — List products associated with a TikTok shop through LinkFox and Chuhaijiang.
- `list_chuhaijiang_shop_videos` — List videos associated with a TikTok shop through LinkFox and Chuhaijiang.
- `list_chuhaijiang_top_selling_products` — List top-selling TikTok product rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_top_selling_shops` — List top-selling TikTok shop rankings through LinkFox and Chuhaijiang.
- `list_chuhaijiang_video_products` — List products associated with a TikTok video through LinkFox and Chuhaijiang.
- `list_chuhaijiang_video_reviews` — List TikTok video comments through LinkFox and Chuhaijiang.
- `list_echotik_new_products` — List newly ranked TikTok Shop products from EchoTik through LinkFox.
- `list_echotik_product_videos` — List TikTok videos associated with a product through LinkFox and EchoTik.
- `list_echotik_seller_products` — List products belonging to a TikTok Shop seller through LinkFox and EchoTik.
- `list_echotik_video_rankings` — List daily, weekly, or monthly TikTok video rankings through LinkFox and EchoTik.
- `list_fastmoss_top_selling_products` — List top-selling TikTok products from FastMoss through LinkFox.
- `list_kalodata_products` — Browse Kalodata TikTok product rankings through LinkFox.
- `list_mercado_item_reviews` — Get reviews for a Mercado Libre product through LinkFox.
- `list_mercado_top_brands` — Get top brands in a Mercado Libre category through LinkFox.
- `list_mercado_top_items` — Get top products in a Mercado Libre category through LinkFox.
- `list_mercado_top_sellers` — Get top sellers in a Mercado Libre category through LinkFox.
- `list_ozon_brand_products` — List Ozon products for a brand through LinkFox and MPSTATS.
- `list_ozon_category_products` — List Ozon products in a category through LinkFox and MPSTATS.
- `list_ozon_seller_products` — List Ozon products for a seller through LinkFox and MPSTATS.
- `list_seerfar_ozon_category_products` — List Ozon category products and aggregate statistics through LinkFox and Seerfar.
- `list_seerfar_ozon_shop_products` — List Ozon shop products and aggregate statistics through LinkFox and Seerfar.
- `list_sif_asin_keywords` — Reverse-search one Amazon ASIN's SIF traffic keywords, ranks, traffic shares, and conversion markers through LinkFox.
- `list_sp_campaigns` — List Sponsored Products campaigns through the LinkFox Amazon Ads gateway.
- `mine_seerfar_ozon_keywords` — Mine Ozon keywords from a seed keyword through LinkFox and Seerfar.
- `query_amazon_aba` — Run a natural-language Amazon Brand Analytics query through LinkFox.
- `reverse_search_mercado_item_keywords` — Find keywords driving traffic to a Mercado Libre product through LinkFox.
- `reverse_search_seerfar_ozon_keywords` — Reverse-search Ozon keywords for SKU IDs through LinkFox and Seerfar.
- `search_1688_by_image` — Find visually similar 1688 products through LinkFox.
- `search_1688_products` — Search the LinkFox 1688 sourcing database.
- `search_amazon_by_image` — Find visually similar Amazon products through LinkFox.
- `search_amazon_opportunities` — Screen Amazon commercial opportunities with LinkFox market metrics.
- `search_amazon_products` — Search Amazon storefront products through LinkFox.
- `search_amazon_store_orders` — Search orders for an authorized Amazon store through LinkFox.
- `search_chuhaijiang_ads` — Search TikTok ads through LinkFox and Chuhaijiang.
- `search_chuhaijiang_creatives` — Search TikTok creatives through LinkFox and Chuhaijiang.
- `search_chuhaijiang_creators` — Search TikTok creators through LinkFox and Chuhaijiang.
- `search_chuhaijiang_lives` — Search TikTok live streams through LinkFox and Chuhaijiang.
- `search_chuhaijiang_products` — Search TikTok products through LinkFox and Chuhaijiang.
- `search_chuhaijiang_products_by_image` — Find visually similar TikTok products using an image URL or an uploaded object key through LinkFox and Chuhaijiang. [write]
- `search_chuhaijiang_shops` — Search TikTok shops through LinkFox and Chuhaijiang.
- `search_chuhaijiang_videos` — Search TikTok videos through LinkFox and Chuhaijiang.
- `search_ebay_products` — Search public eBay listings through LinkFox.
- `search_echotik_products` — Search EchoTik TikTok products through LinkFox.
- `search_echotik_sellers` — Search TikTok Shop sellers with EchoTik analytics through LinkFox.
- `search_echotik_videos` — Search TikTok videos with EchoTik analytics through LinkFox.
- `search_etsy_categories` — Search synchronized Etsy categories through LinkFox.
- `search_etsy_products` — Search Etsy products using commercial and listing filters through LinkFox.
- `search_etsy_stores` — Search Etsy shops using commercial and profile filters through LinkFox.
- `search_fastmoss_products` — Search FastMoss TikTok products through LinkFox.
- `search_mercado_catalogs` — Search Mercado Libre catalog products with commercial filters through LinkFox.
- `search_mercado_categories` — Search Mercado Libre categories through LinkFox.
- `search_mercado_daily_keywords` — Search daily Mercado Libre trending keywords through LinkFox.
- `search_mercado_items` — Search Mercado Libre products with commercial filters through LinkFox.
- `search_mercado_leaf_categories` — Search Mercado Libre leaf categories through LinkFox.
- `search_mercado_monthly_keywords` — Search monthly Mercado Libre trending keywords through LinkFox.
- `search_mercado_sellers` — Search Mercado Libre sellers by type and reputation through LinkFox.
- `search_ozon_products` — Search Ozon products by keyword or SKU through LinkFox and MPSTATS.
- `search_seerfar_ozon_market_keywords` — Search Ozon market keywords through LinkFox and Seerfar.
- `search_seerfar_ozon_product_reports` — Search Ozon product reports with commercial filters through LinkFox and Seerfar.
- `search_zhihuiya_patents` — Search patents with Analytics expressions, deduplication, sorting, and pagination through LinkFox and Patsnap.
- `search_zhihuiya_patents_by_image` — Search design and utility patents by image with filters and pagination through LinkFox and Patsnap.
- `translate_zhihuiya_patent_abstracts` — Get translated patent titles and abstracts through LinkFox and Patsnap.
- `translate_zhihuiya_patent_claims` — Get translated patent claims through LinkFox and Patsnap.
- `translate_zhihuiya_patent_descriptions` — Get translated patent descriptions through LinkFox and Patsnap.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change LinkFox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — LinkFox is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/linkfox
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- LinkFox homepage: https://www.linkfox.com/
