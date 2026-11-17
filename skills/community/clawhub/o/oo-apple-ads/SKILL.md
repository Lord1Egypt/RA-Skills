---
name: oo-apple-ads
description: "Apple Ads (ads.apple.com). Use this skill for ANY Apple Ads request — reading, creating, updating, and deleting data. Whenever a task involves Apple Ads, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Apple Ads"
  author: "OOMOL"
  version: "1.0.5"
  services: ["apple_ads"]
  icon: "https://static.oomol.com/logo/third-party/apple_ads.svg"
---

# Apple Ads

Operate **Apple Ads** through your OOMOL-connected account. This skill calls the `apple_ads` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Apple Ads. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "apple_ads" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "apple_ads" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `apply_daily_budget_recommendations` — Accept one or more daily budget recommendations. Apple Ads raises each campaign's daily budget and moves the recommendation to the terminal APPLIED state. [destructive]
- `apply_target_cpa_recommendations` — Accept one or more target CPA recommendations. Apple Ads changes the target the campaign's Maximize Conversions bidding optimizes toward and moves each recommendation to the terminal APPLIED state. [destructive]
- `bulk_create_keywords` — Create many keywords in one request, spanning as many ad groups as you like. The whole batch counts as a single call against the rate limit, which makes it the way to seed a keyword list. [write]
- `bulk_create_negative_keywords` — Create many negative keywords in one request, mixing campaign-level and ad-group-level exclusions freely. The whole batch counts as a single call against the rate limit. Each outcome carries the zero-based index of the payload it belongs to. [write]
- `bulk_update_keywords` — Change the bid or the status of many keywords in one request, for example to reprice a set of high performers or pause a set of weak ones. Apple Ads accepts nothing else on an update. [destructive]
- `bulk_update_negative_keywords` — Pause or resume many negative keywords in one request. status is the only field Apple Ads allows changing, and every payload identifies its record by id. Each outcome carries the zero-based index of the payload it belongs to. [destructive]
- `create_ad` — Create an ad that links an existing ad creative to an ad group. adGroupId and creativeId are fixed at creation: serve a different ad creative by creating another ad and deleting this one. The ad creative must have a systemStatus of VALID, and only one ad per ad group can be ENABLED at a time. [write]
- `create_ad_account` — Create an ad account under the organization the access token is bound to. The currency, time zone and payment model are inherited from the organization, and productFeatures is fixed at creation: an account authorized for the App Store can never run Apple Maps campaigns, or the other way around. [write]
- `create_ad_group` — Create an ad group inside an existing campaign. campaignId, pricingModel and automatedKeywordsRequired are fixed at creation. Keywords and negative keywords cannot be created inline: add them afterwards with the keyword actions. [write]
- `create_budget_order` — Create a budget order for the ad account this request is scoped to, then cap the total spend of a group of campaigns by assigning them to it. The ad account must be on the LOC (Line of Credit) payment model, which is why invoice details are required. [write]
- `create_campaign` — Create a campaign. promotedObjectType, promotedObjectId and billingEvent are fixed at creation: promote a different app or brand by creating another campaign. [write]
- `create_creative` — Create an ad creative at the ad account level. It is not tied to a campaign or ad group, so several ads can reference the same one. creativeType and destination are fixed at creation. Pass the returned identifier as creativeId when creating an ad. [write]
- `create_keyword` — Add one keyword to an ad group. adGroupId, text and matchType are fixed at creation: to change them, delete the keyword and create a new one. [write]
- `create_location_group` — Create a location group, a named set of the advertiser's business locations that an ad group can target. brandId and the owning ad account are fixed at creation: move a group to another brand by deleting it and creating a new one. A STATIC group becomes usable immediately, while a DYNAMIC group stays PENDING until Apple Ads finishes evaluating its rules. [write]
- `create_negative_keyword` — Create one negative keyword. Scope it either to a campaign, by passing campaignId alone, or to a single ad group, by passing adGroupId alone: Apple Ads rejects a payload that carries both or neither. text and matchType are fixed at creation, so changing them means deleting this record and creating another. [write]
- `delete_ad` — Soft-delete one ad. Delivery stops immediately and query results exclude it, but Apple Ads keeps the record and still returns it from a read. The referenced ad creative is untouched and stays available to other ads. [destructive]
- `delete_ad_group` — Soft-delete one ad group. Apple Ads keeps the record but stops delivery and cascades the deletion to the ad group's ads, keywords and negative keywords. It cannot be undone. [destructive]
- `delete_asset` — Soft-delete one creative asset. Only assets uploaded through the Apple Ads API can be deleted, deleting an already deleted asset fails with 404, and get_asset keeps returning the record with deleted set to true. [destructive]
- `delete_budget_order` — Soft-delete one budget order. Apple Ads rejects the deletion with 400 while any campaign is still assigned to the budget order, and also once it has started, expired, been exhausted or been canceled. A soft-deleted budget order cannot be restored; create a new one instead. [destructive]
- `delete_campaign` — Soft-delete one campaign. Apple Ads keeps the record but stops delivery and cascades the deletion to the campaign's ad groups, keywords and ads. [destructive]
- `delete_creative` — Soft-delete one ad creative. It cannot be undone or reused for new ads, and every ad already referencing it drops to systemStatus NOT_RUNNING without being deleted. Deleting an already deleted ad creative returns 404. [destructive]
- `delete_keyword` — Soft-delete one keyword. Apple Ads keeps the record and stops bidding on the term, and leaves the parent ad group and campaign untouched. To pause the term temporarily, update its status to PAUSED instead. [destructive]
- `delete_location_group` — Soft-delete one location group. Deletion is permanent and there is no restore: ad groups targeting the group lose that constraint immediately and keep serving only if they target another location group. A group whose systemStatus is INVALID or PENDING cannot be deleted. [destructive]
- `delete_negative_keyword` — Soft-delete one negative keyword. The excluded term stops being suppressed right away, across every ad group of the campaign for a campaign-level record. Use update_negative_keyword with status PAUSED instead when the exclusion should come back later. [destructive]
- `dismiss_daily_budget_recommendations` — Reject one or more daily budget recommendations. Each campaign keeps its current daily budget, but the recommendation moves to the terminal DISMISSED state and never returns to AVAILABLE. [destructive]
- `dismiss_target_cpa_recommendations` — Reject one or more target CPA recommendations. The campaign keeps its current target, but each recommendation moves to the terminal DISMISSED state and never returns to AVAILABLE. [destructive]
- `get_ad` — Read one ad by identifier, including systemStatus, displayStatus and the reason arrays that explain why it is not delivering. Apple Ads still returns a soft-deleted ad with deleted set to true.
- `get_ad_account` — Read the full record of one ad account, including its delegated advertiser resources and the reasons it is not operational.
- `get_ad_group` — Read one ad group by identifier, including its full targeting and bid strategy. Apple Ads returns the ad group regardless of its deleted state.
- `get_ad_group_report` — Retrieve App Store ad group performance, one row per ad group with metrics aggregated over the date range and optionally broken out by granularity and dimension. Every App Store report request must carry a filter on campaignId; this action rejects a request without one before it reaches Apple Ads. Add an adGroupId filter to narrow the report further.
- `get_ad_report` — Retrieve App Store ad performance, one row per ad with metrics aggregated over the date range. Every App Store report request must carry a filter on campaignId; this action rejects a request without one before it reaches Apple Ads. Ad-level reports do not support HOURLY granularity or the demographic dimensions.
- `get_advertiser_resources` — List the advertiser resources of one type that the organization can delegate to an ad account. Use the returned resourceId values in the delegations of create_ad_account and update_ad_account.
- `get_app` — Read the App Store metadata of one app by its Adam ID, including its genres, supported device classes and the countries or regions it is available in. Apple Ads answers with 404 when no app matches the Adam ID.
- `get_app_rejection_reasons` — Read one ad creative rejection reason by identifier, including its reason code, the level it applies at and the reviewer comment.
- `get_asset` — Read one creative asset by identifier, including its eligibility status. Apple Ads returns the asset regardless of its deleted state, and this is the only way to read a variant crop, which query_assets omits.
- `get_brand` — Read one brand by identifier, including its categories and its current ad serving eligibility.
- `get_brand_ad_group_report` — Retrieve Apple Maps ad group performance, one row per ad group with spend, engagement and Apple Maps action metrics aggregated over the date range. Filter on campaignId or adGroupId to scope the report.
- `get_brand_ad_report` — Retrieve Apple Maps ad performance, one row per ad with its creative snapshot and metrics aggregated over the date range. Filter on campaignId or adGroupId to scope the report. Ad-level reports do not support HOURLY granularity.
- `get_brand_campaign_report` — Retrieve Apple Maps campaign performance, one row per campaign with spend, engagement and Apple Maps action metrics aggregated over the date range. Filter on campaignId to scope the report to specific campaigns.
- `get_brand_keyword_report` — Retrieve Apple Maps keyword performance, one row per keyword with metrics aggregated over the date range and an optional bid recommendation. Always filter on campaignId or adGroupId so the report does not span every keyword in the ad account.
- `get_brand_search_term_report` — Retrieve the Apple Maps search terms that matched a keyword and produced an impression on the Search Results placement, one row per search term with the keyword it matched. Always filter on campaignId or adGroupId. Apple Ads suppresses or aggregates low-volume terms to protect user privacy.
- `get_budget_order` — Read one budget order by identifier, including its amount, active date range, assigned ad account and invoice details.
- `get_business_category` — Read one Apple Maps business category by its MUID, including its qualifiedId taxonomy path and eligibility status.
- `get_campaign` — Read one campaign by identifier. Apple Ads returns the campaign regardless of its deleted state.
- `get_campaign_limited_status_details` — Read why a legacy app campaign delivers below its potential in each country or region, as a map of country or region code to limiting reason.
- `get_campaign_report` — Retrieve App Store campaign performance, one row per campaign with metrics aggregated over the date range and optionally broken out by granularity and dimension. Every App Store report request must carry a filter on campaignId; this action rejects a request without one before it reaches Apple Ads.
- `get_change_history_detail` — Read the field-level before and after values of one entity change, addressed by the composite detailId that query_change_history returns in each row's metas entries when metadata is latest or snapshot.
- `get_creative` — Read one ad creative by identifier, including its creative spec, destination, system status and per-placement eligibility. A soft-deleted ad creative returns 404: read it back through query_creatives with a deleted filter instead.
- `get_keyword` — Read one keyword by identifier. Apple Ads returns a soft-deleted keyword with deleted set to true rather than 404.
- `get_keyword_report` — Retrieve App Store keyword performance, one row per keyword with metrics aggregated over the date range and an optional bid recommendation. Every App Store report request must carry a filter on campaignId; this action rejects a request without one before it reaches Apple Ads. Add an adGroupId filter to keep the report to a single ad group.
- `get_location` — Read one business location by identifier. Use it to confirm the address, coordinates, operational status and eligibility of a store before adding it to a location group.
- `get_location_group` — Read one location group by identifier, including its membership definition, systemStatus, location count and eligibility. A soft-deleted group is still readable and comes back with systemStatus DELETED.
- `get_me` — Read the user and organization the access token belongs to. It is the cheapest way to confirm the credential works and to learn the orgId the other account actions need.
- `get_negative_keyword` — Read one negative keyword by identifier. Apple Ads returns the record regardless of its deleted state, and an absent or null adGroupId marks it as a campaign-level exclusion.
- `get_org` — Read one organization by identifier, including the currency, time zone, payment model and system status its ad accounts inherit.
- `get_product_page` — Read one App Store product page by identifier. Use query_product_pages to discover the identifiers of an app's product pages first.
- `get_search_term_report` — Retrieve the App Store search terms that matched a keyword and produced an impression, one row per search term with the keyword it matched. Every App Store report request must carry a filter on campaignId; this action rejects a request without one before it reaches Apple Ads. Apple Ads suppresses or aggregates low-volume terms to protect user privacy.
- `get_user_acls` — List every ad account the access token can reach and the roles the API user holds on each. Start here to discover the adAccountId values the ad-account-scoped actions need.
- `query_ad_groups` — Search the ad groups of one ad account with filters, sorting and offset pagination. Filter on campaignId to scope the result to a single campaign. Soft-deleted ad groups are excluded unless a filter on deleted asks for them.
- `query_ads` — Search the ads of one ad account with filters, sorting and offset pagination. Filter on adGroupId to scope to one ad group or on campaignId for a whole campaign. Soft-deleted ads are excluded unless a deleted EQUALS true filter asks for them.
- `query_app_eligibilities` — Check whether apps are eligible to run App Store ads, one row per combination of app, supply placement, supply source, country or region and device class. Run it before creating a campaign in a new market, because an ineligible market delivers nothing. Apple Maps brand promotion is not covered here.
- `query_app_locale_details` — Read the localized content of one app's default product page, identified by the app's adamId. It returns every locale configured for the default product page unless a languageCode filter narrows it. Custom product pages are not covered here: use query_product_page_locale_details for those.
- `query_app_rejection_reasons` — Search the rejection reasons recorded for the App Store ad creatives of an app, explaining why each creative failed Apple review. Filter by adamId to scope the search to one app.
- `query_assets` — Search the creative assets of one ad account. Soft-deleted assets and variant crops are excluded from the results; filter on deleted to include soft-deleted assets, and read a variant with get_asset. Filter on promotedObjectId to scope the query to one app or brand, because an unfiltered query spans every promoted object in the ad account.
- `query_brand_rejection_reasons` — Search the policy assignments that explain why Apple Ads rejected a brand, one of its creatives or one of its assets. Filter on promotedObjectId to scope the results to a single brand.
- `query_brands` — Search the brands accessible to one ad account with filters, sorting and offset pagination. A brand must reach eligibility.status ELIGIBLE before an Apple Maps campaign can promote it.
- `query_budget_orders` — Search the budget orders of one ad account with filters, sorting and offset pagination. Soft-deleted budget orders are excluded unless a filter on deleted asks for them.
- `query_business_categories` — Search the Apple Maps business category taxonomy with filters, sorting and offset pagination. Only categories with eligibility.status ELIGIBLE can be used by an active Apple Maps campaign.
- `query_campaigns` — Search the campaigns of one ad account with filters, sorting and offset pagination. Soft-deleted campaigns are excluded unless a filter on deleted asks for them.
- `query_category_suggestions` — Discover the categories associated with one promoted object, or look up how popular known category names are. Pick exactly one route: SUGGESTION needs the promoted object, SEARCH needs categories or categoryLike.
- `query_change_history` — Search the change history of one ad account, returning one row per transaction, actor and entity type with a count of the entity changes it covers. A filter on eventTime is required and Apple Ads looks back at most 6 months. A summary row carries no entityId, so set metadata to latest or snapshot when you plan to expand rows with get_change_history_detail: each row's metas entries then include a ready-to-use detailId.
- `query_creatives` — Search the ad creatives of one ad account with filters, sorting and offset pagination. Soft-deleted ad creatives are excluded unless a deleted EQUALS true filter asks for them, which is the only way to read one back after deletion.
- `query_daily_budget_recommendations` — List the daily budget increases Apple Ads recommends for one promoted object, with the historical and projected performance behind each one. This is the only recommendation type available for Apple Maps brand campaigns.
- `query_geo_locations` — Look up geo targeting locations by identifier. Pass the geo location ids or pipe-delimited legacy ids you already have, and Apple Ads returns their metadata and eligibility scoped to one supply source. Use it to batch-validate targeting values before applying them to an ad group; this endpoint never filters soft-blocked geos out.
- `query_impression_share` — Measure what share of the available impressions one App Store app captured for each search term and country or region. Apple Maps brand campaigns have no impression share equivalent.
- `query_keyword_suggestions` — Discover keywords worth targeting for one promoted object, ranked by relative popularity. Suggestions are stateless: turn one into a live keyword with create_keyword.
- `query_keywords` — Search the keywords of one ad account with filters, sorting and offset pagination. Apple Ads requires a filter on adGroupId or campaignId unless you filter on id, and soft-deleted keywords are excluded unless a filter on deleted asks for them.
- `query_location_groups` — Search the location groups of one ad account with filters, sorting and offset pagination. Soft-deleted groups are excluded unless a filter on deleted asks for them.
- `query_locations` — Search the advertiser's business locations, the physical stores and venues an Apple Maps campaign promotes. Filter by brandId to scope results to one brand, and collect the returned ids to build a location group.
- `query_negative_keywords` — Search the negative keywords of one ad account with filters, sorting and offset pagination. Apple Ads requires an adGroupId filter on every query except one filtered by id: combine adGroupId IS_NULL with campaignId EQUALS to list a campaign's own exclusions, adGroupId IS_NOT_NULL with campaignId EQUALS to list the ad-group-level ones across that campaign, or adGroupId EQUALS or IN to scope the query to specific ad groups.
- `query_phrase_suggestions` — Discover natural-language search phrases for one promoted object, or look up how popular known phrases are. Pick exactly one route: SUGGESTION needs the promoted object, SEARCH needs phrases or phraseLike.
- `query_product_page_locale_details` — Read the localized content of one custom product page: the localized app name, subtitle, promotional text and the screenshots and preview videos grouped by device type. A filter on productPageId is required; without a languageCode filter Apple Ads returns every locale configured for the page.
- `query_product_pages` — Search the App Store product pages available to one ad account, covering default product pages, custom product pages and product page optimization variants. Filter on adamId to list the pages of a single app, because an unfiltered query spans every app the ad account can reach. Product pages come from App Store Connect and appear here after a short propagation delay.
- `query_search_term_popularity` — Rank App Store search terms by relative search volume within a country or region and genre, to discover high-volume terms worth targeting.
- `query_supported_app_languages` — List the App Store countries or regions along with the languages that Apple Ads supports in each market. Use it to validate a locale before setting it on an ad group or a creative. An empty query returns every market.
- `query_target_cpa_recommendations` — List the target CPA adjustments Apple Ads recommends for one promoted object. Only campaigns on a Maximize Conversions bid strategy receive them, and a target CPA is a goal the auto-bidder optimizes toward rather than a bid.
- `query_target_cpa_suggestion` — Read the target CPA Apple Ads suggests as the starting point for a new Maximize Conversions campaign, computed from the app's tap-install CPI over the last 28 days. It applies to App Store apps only, so the request always asks for promotedObjectType APPSTORE_APP.
- `search_apps` — Search the App Store for apps by name or content provider, or list the apps the organization owns. Supply at least one of query, cpids or returnOwnedApps set to true. Campaigns can only promote apps the ad account owns, so use returnOwnedApps to find a usable promotedObjectId.
- `search_geo_locations` — Search geo targeting locations by name. Use it to discover the geo location ids to put in an ad group's country, adminArea, locality or postalCode targeting dimension. Soft-blocked geos are returned with their eligibility data unless eligible is true.
- `update_ad` — Change the name or status of one ad. They are the only mutable fields; adGroupId, creativeId, campaignId and adAccountId are locked at creation. Only the fields you pass are changed. Updating a soft-deleted ad returns 404. [destructive]
- `update_ad_account` — Change the name or the delegated advertiser resources of one ad account. Only the fields you pass are changed, and the delegations array you pass replaces the stored one entirely. The currency, time zone, payment model, organization and productFeatures are fixed and cannot be updated. [destructive]
- `update_ad_group` — Change the mutable fields of one ad group. Only the fields you pass are changed, and targeting is merged dimension by dimension: a dimension you pass replaces the stored one, and a dimension you omit is left alone. campaignId, pricingModel and automatedKeywordsRequired cannot be changed. [destructive]
- `update_budget_order` — Change the mutable fields of one budget order. Only the fields you pass are changed. On a budget order that is already active, an end date can only be shortened, never extended, and passing endTime as null removes the expiration date entirely. [destructive]
- `update_campaign` — Change the mutable fields of one campaign. Only the fields you pass are changed, but an array you pass replaces the stored array entirely. [destructive]
- `update_creative` — Change the name or creative spec of one ad creative. They are the only mutable fields; creativeType and destination are locked at creation. Changing creativeSpec can send the ad creative back to PENDING for re-review, which stops the ads referencing it from delivering until it is VALID again. [destructive]
- `update_keyword` — Change the bid or the status of one keyword. Apple Ads accepts nothing else on an update, and returns 404 for a keyword that has already been deleted. [destructive]
- `update_location_group` — Change the mutable fields of one location group. Only the fields you pass are changed, but locationIds and rules replace the stored array entirely rather than merging into it. Changing rules sends a DYNAMIC group back to PENDING while Apple Ads re-evaluates membership. A group whose systemStatus is INVALID or PENDING cannot be updated. [destructive]
- `update_negative_keyword` — Pause or resume one negative keyword. status is the only field Apple Ads allows changing: PAUSED lets the excluded term reach the auction again, ENABLED restores the exclusion. Apple Ads answers a request for a deleted negative keyword with 404. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Apple Ads state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Apple Ads is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/apple_ads
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Apple Ads homepage: https://ads.apple.com/
- API documentation: https://developer.apple.com/documentation/apple-ads-platform-api
