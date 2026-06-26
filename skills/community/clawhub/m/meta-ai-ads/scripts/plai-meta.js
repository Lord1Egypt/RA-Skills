#!/usr/bin/env node
/**
 * plai-meta.js — CLI for Plai Meta Ads API
 *
 * Usage: node scripts/plai-meta.js <command> [--key value ...]
 *
 * Required env vars:
 *   PLAI_API_KEY   — Plai API key
 *   PLAI_USER_ID   — Plai user ID
 */

const BASE_URL = process.env.PLAI_BASE_URL || "https://public.plai.io";
const API_KEY = process.env.PLAI_API_KEY;
const USER_ID = process.env.PLAI_USER_ID;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function assertEnv() {
  if (!API_KEY) {
    console.error("Error: PLAI_API_KEY environment variable is not set.");
    process.exit(1);
  }
  if (!USER_ID) {
    console.error("Error: PLAI_USER_ID environment variable is not set.");
    process.exit(1);
  }
}

async function plai(endpoint, body = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY,
      "x-request-source": "clawhub-meta-ads-skill",
    },
    body: JSON.stringify({ ...body, userId: USER_ID }),
  });

  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }

  if (!res.ok) {
    console.error(`API error ${res.status}: ${JSON.stringify(data, null, 2)}`);
    process.exit(1);
  }

  console.log(JSON.stringify(data, null, 2));
}

/** Parse --key value pairs from process.argv */
function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const key = argv[i].slice(2);
      const val = argv[i + 1];
      if (val === undefined || val.startsWith("--")) {
        args[key] = true;
      } else {
        try {
          args[key] = JSON.parse(val);
        } catch {
          args[key] = val;
        }
        i++;
      }
    }
  }
  return args;
}

function requireArgs(args, ...keys) {
  for (const key of keys) {
    if (args[key] === undefined) {
      console.error(`Error: --${key} is required for this command.`);
      process.exit(1);
    }
  }
}

/**
 * Build ages object from minAge / maxAge.
 * MCP server wraps these in { ages: { minAge, maxAge } } before sending to the API.
 */
function buildAges(args) {
  if (args.minAge !== undefined && args.maxAge !== undefined) {
    return { ages: { minAge: Number(args.minAge), maxAge: Number(args.maxAge) } };
  }
  return {};
}

/**
 * Transform images: string[] → { url: string }[]
 * The MCP server performs this transformation before calling the API.
 */
function buildImages(images) {
  if (!images) return undefined;
  return images.map((imgUrl) => ({ url: imgUrl }));
}

// ---------------------------------------------------------------------------
// Command dispatch
// ---------------------------------------------------------------------------

const [, , command, ...rest] = process.argv;
const args = parseArgs(rest);

assertEnv();

switch (command) {

  // ── Campaigns ──────────────────────────────────────────────────────────────

  /**
   * meta_get_campaigns_list
   * No input params.
   */
  case "list-campaigns":
    plai("/meta/get_campaigns_list");
    break;

  /**
   * meta_create_campaign
   *
   * Required: campaignName, campaignType, budget, locations
   * Required for LEAD_GENERATION:      leadsFormId
   * Required for CONVERSIONS/OUTCOME_SALES: pixelId, conversionGoal
   * Optional: url, primaryText, headlines, images, videos, interests,
   *           gender, minAge+maxAge, targetLocales, audienceId
   *
   * Notes:
   *  - images are passed as URL strings; transformed to {url} objects here.
   *  - minAge + maxAge are wrapped into ages:{minAge,maxAge} for the API.
   *  - callToAction is always LEARN_MORE (matches MCP server behaviour).
   */
  case "create-campaign":
    requireArgs(args, "campaignName", "campaignType", "budget", "locations");
    {
      const body = {
        campaignName: args.campaignName,
        campaignType: args.campaignType,
        budget: Number(args.budget),
        callToAction: "LEARN_MORE",
        locations: args.locations,
        primaryText: args.primaryText || [],
        ...buildAges(args),
      };

      if (args.url)           body.url = args.url;
      if (args.headlines)     body.headlines = args.headlines;
      if (args.images)        body.images = buildImages(args.images);
      if (args.videos)        body.videos = args.videos;
      if (args.interests)     body.interests = args.interests;
      if (args.gender)        body.gender = args.gender;
      if (args.targetLocales) body.targetLocales = args.targetLocales;
      if (args.audienceId)    body.audienceId = args.audienceId;
      if (args.pixelId)       body.pixelId = args.pixelId;
      if (args.conversionGoal) body.conversionGoal = args.conversionGoal;

      // LEAD_GENERATION: leadsFormId required
      if (args.campaignType === "LEAD_GENERATION") {
        requireArgs(args, "leadsFormId");
        body.leadsFormId = args.leadsFormId;
      }

      // CONVERSIONS / OUTCOME_SALES: pixelId + conversionGoal required
      if (args.campaignType === "CONVERSIONS" || args.campaignType === "OUTCOME_SALES") {
        requireArgs(args, "pixelId", "conversionGoal");
      }

      plai("/meta/create_campaign", body);
    }
    break;

  /**
   * meta_create_message_engagement_campaign
   *
   * Required: campaignName, budget, url, locations, messagingApps, multipleCreatives
   * Optional: interests, gender, minAge+maxAge, targetLocales, audienceId
   *
   * multipleCreatives: JSON array of 1–10 creative objects, each with:
   *   Required: url, primaryText, greetingText, conversations
   *   Optional: headlines, phoneNumber, image, video:{video_id,thumbnail_url}
   *
   * messagingApps: JSON array of MESSENGER | INSTAGRAM | WHATSAPP
   *
   * Note: campaignType is hardcoded to OUTCOME_ENGAGEMENT by the MCP server.
   */
  case "create-message-engagement":
    requireArgs(args, "campaignName", "budget", "url", "locations", "messagingApps", "multipleCreatives");
    {
      const body = {
        campaignName: args.campaignName,
        budget: Number(args.budget),
        url: args.url,
        locations: args.locations,
        campaignType: "OUTCOME_ENGAGEMENT",
        messagingApps: args.messagingApps,
        multipleCreatives: args.multipleCreatives.map((creative) => ({
          ...creative,
          callToAction: "LEARN_MORE",
        })),
        ...buildAges(args),
      };

      if (args.interests)     body.interests = args.interests;
      if (args.gender)        body.gender = args.gender;
      if (args.targetLocales) body.targetLocales = args.targetLocales;
      if (args.audienceId)    body.audienceId = args.audienceId;

      plai("/meta/create_campaign", body);
    }
    break;

  /**
   * meta_get_campaign_insights
   *
   * Required: campaignId
   * Optional: startDate (YYYY-MM-DD), endDate (YYYY-MM-DD),
   *           currencySymbol (default $), clientCostAdjustmentPercentage (default 100)
   */
  case "get-insights":
    requireArgs(args, "campaignId");
    plai("/meta/get_campaign_insights", {
      campaignId: args.campaignId,
      ...(args.startDate ? { startDate: args.startDate } : {}),
      ...(args.endDate   ? { endDate:   args.endDate   } : {}),
      currencySymbol: args.currencySymbol || "$",
      clientCostAdjustment: {
        percentage: args.clientCostAdjustmentPercentage
          ? Number(args.clientCostAdjustmentPercentage)
          : 100,
      },
    });
    break;

  /**
   * meta_update_campaign_status
   *
   * Required: campaignId, status
   * status: PAUSED | ACTIVE | DELETE
   */
  case "update-status":
    requireArgs(args, "campaignId", "status");
    if (!["PAUSED", "ACTIVE", "DELETE"].includes(args.status)) {
      console.error("Error: --status must be one of PAUSED, ACTIVE, DELETE");
      process.exit(1);
    }
    plai("/meta/update_campaign_status", {
      campaignId: args.campaignId,
      status: args.status,
    });
    break;

  /**
   * meta_update_campaign_budget
   *
   * Required: campaignId, amount
   * Optional: editLevel (default BUDGET — only supported value)
   */
  case "update-budget":
    requireArgs(args, "campaignId", "amount");
    plai("/meta/edit_campaign", {
      campaignId: args.campaignId,
      editLevel: args.editLevel || "BUDGET",
      amount: Number(args.amount),
    });
    break;

  // ── Lead Forms ─────────────────────────────────────────────────────────────

  /**
   * meta_check_leadform_tos
   * No input params. Run before creating a lead form.
   */
  case "check-leadform-tos":
    plai("/meta/check_leadform_tos");
    break;

  /**
   * meta_get_leadform_list
   * No input params.
   */
  case "list-leadforms":
    plai("/meta/get_leadform_list");
    break;

  /**
   * meta_create_leadform
   *
   * Required: leadsFormName, privacyPolicyUrl, privacyPolicyName,
   *           website_url, questionPageCustomHeadline
   * All fields must come from the user — never assume values.
   */
  case "create-leadform":
    requireArgs(
      args,
      "leadsFormName",
      "privacyPolicyUrl",
      "privacyPolicyName",
      "website_url",
      "questionPageCustomHeadline"
    );
    plai("/meta/create_leadform", {
      leadsFormName: args.leadsFormName,
      privacyPolicyUrl: args.privacyPolicyUrl,
      privacyPolicyName: args.privacyPolicyName,
      questionPageCustomHeadline: args.questionPageCustomHeadline,
      leadFormQuestions: [{ type: "EMAIL" }, { type: "FULL_NAME" }],
      thankYouPage: {
        title: "Thanks, you're all set",
        body: "We'll be in touch soon.",
        button_text: "Visit Website",
        button_type: "VIEW_WEBSITE",
        website_url: args.website_url,
      },
      language: args.language || "EN_US",
      form_type: "MORE_VOLUME",
    });
    break;

  // ── Targeting ──────────────────────────────────────────────────────────────

  /**
   * meta_search_targeting_locations
   * Required: query
   * Returns {id, type, countryCode} objects — pass directly to create-campaign --locations.
   */
  case "search-locations":
    requireArgs(args, "query");
    plai("/meta/search_targeting_locations", { query: args.query });
    break;

  /**
   * meta_search_targeting_interests
   * Required: query
   * Optional: specialAdCategories (HOUSING | FINANCIAL_PRODUCTS_SERVICES | EMPLOYMENT)
   *           specialAdCountries (ISO 3166-1 alpha-2 codes, e.g. ["US","GB"])
   */
  case "search-interests":
    requireArgs(args, "query");
    plai("/meta/search_targeting_interests", {
      query: args.query,
      ...(args.specialAdCategories ? { specialAdCategories: args.specialAdCategories } : {}),
      ...(args.specialAdCountries  ? { specialAdCountries:  args.specialAdCountries  } : {}),
    });
    break;

  /**
   * meta_get_targeting_locales
   * No input params. Returns numeric locale IDs for language targeting.
   */
  case "get-locales":
    plai("/meta/get_targeting_locales_lookup");
    break;

  // ── Audiences ──────────────────────────────────────────────────────────────

  /**
   * meta_get_custom_audiences
   * Optional: pagination
   */
  case "list-audiences":
    plai("/meta/get_custom_audiences", {
      ...(args.pagination ? { pagination: args.pagination } : {}),
    });
    break;

  /**
   * meta_create_page_audience
   * Required: name, type (FACEBOOK | INSTAGRAM)
   */
  case "create-page-audience":
    requireArgs(args, "name", "type");
    if (!["FACEBOOK", "INSTAGRAM"].includes(args.type)) {
      console.error("Error: --type must be FACEBOOK or INSTAGRAM");
      process.exit(1);
    }
    plai("/meta/create_page_audience", {
      name: args.name,
      type: args.type,
    });
    break;

  /**
   * meta_create_leadform_audience
   * Required: name, description, type (open | close | submit), leadFormIds
   * Note: description is required (not optional).
   */
  case "create-leadform-audience":
    requireArgs(args, "name", "description", "type", "leadFormIds");
    if (!["open", "close", "submit"].includes(args.type)) {
      console.error("Error: --type must be open, close, or submit");
      process.exit(1);
    }
    plai("/meta/create_leadform_audience", {
      name: args.name,
      description: args.description,
      type: args.type,
      leadFormIds: args.leadFormIds,
    });
    break;

  /**
   * meta_create_lookalike_audience
   * Required: sourceType (AUDIENCE | PAGE), audienceName, countryCode (2-letter ISO)
   * Required when sourceType=AUDIENCE: sourceId
   */
  case "create-lookalike":
    requireArgs(args, "sourceType", "audienceName", "countryCode");
    if (!["AUDIENCE", "PAGE"].includes(args.sourceType)) {
      console.error("Error: --sourceType must be AUDIENCE or PAGE");
      process.exit(1);
    }
    if (args.sourceType === "AUDIENCE") {
      requireArgs(args, "sourceId");
    }
    plai("/meta/create_lookalike_audience", {
      sourceType: args.sourceType,
      ...(args.sourceId ? { sourceId: args.sourceId } : {}),
      audienceName: args.audienceName,
      countryCode: args.countryCode,
    });
    break;

  // ── Pixels & Conversions ───────────────────────────────────────────────────

  /**
   * meta_get_pixels_list
   * No input params.
   */
  case "list-pixels":
    plai("/meta/get_pixels_list");
    break;

  /**
   * meta_get_custom_conversions
   * Required: pixelId, campaignType (CONVERSIONS | OUTCOME_SALES)
   */
  case "list-conversions":
    requireArgs(args, "pixelId", "campaignType");
    if (!["CONVERSIONS", "OUTCOME_SALES"].includes(args.campaignType)) {
      console.error("Error: --campaignType must be CONVERSIONS or OUTCOME_SALES");
      process.exit(1);
    }
    plai("/meta/get_custom_conversions", {
      pixelId: args.pixelId,
      campaignType: args.campaignType,
    });
    break;

  // ── Media ──────────────────────────────────────────────────────────────────

  /**
   * meta_get_ad_account_media
   * Required: type (IMAGE | VIDEO)
   * Optional: pagination
   */
  case "list-media":
    requireArgs(args, "type");
    if (!["IMAGE", "VIDEO"].includes(args.type)) {
      console.error("Error: --type must be IMAGE or VIDEO");
      process.exit(1);
    }
    plai("/meta/get_ad_account_media", {
      type: args.type,
      ...(args.pagination ? { pagination: args.pagination } : {}),
    });
    break;

  /**
   * meta_get_fb_page_media (via get_fb_page_media endpoint)
   * Required: type (IMAGE | VIDEO)
   * Optional: pagination
   */
  case "list-fb-media":
    requireArgs(args, "type");
    if (!["IMAGE", "VIDEO"].includes(args.type)) {
      console.error("Error: --type must be IMAGE or VIDEO");
      process.exit(1);
    }
    plai("/meta/get_fb_page_media", {
      type: args.type,
      ...(args.pagination ? { pagination: args.pagination } : {}),
    });
    break;

  /**
   * meta_get_ig_page_media (via get_ig_page_media endpoint)
   * Optional: pagination
   */
  case "list-ig-media":
    plai("/meta/get_ig_page_media", {
      ...(args.pagination ? { pagination: args.pagination } : {}),
    });
    break;

  /**
   * meta_upload_video
   * Required: videoUrl (publicly accessible URL)
   */
  case "upload-video":
    requireArgs(args, "videoUrl");
    plai("/meta/upload_video", { videoUrl: args.videoUrl });
    break;

  /**
   * meta_get_video_info
   * Required: videoId
   * Poll until status is READY before using the video in a campaign.
   */
  case "get-video-info":
    requireArgs(args, "videoId");
    plai("/meta/get_video_info", { videoId: args.videoId });
    break;

  // ── Product Catalogs ───────────────────────────────────────────────────────

  /**
   * meta_get_catalog_list
   * No input params.
   */
  case "list-catalogs":
    plai("/meta/get_catalog_list");
    break;

  /**
   * meta_create_catalog
   * Required: name
   */
  case "create-catalog":
    requireArgs(args, "name");
    plai("/meta/create_catalog", { name: args.name });
    break;

  /**
   * meta_create_catalog_products_feed
   * Required: catalogId, name, fileUrl (CSV/XML), currencyCode (3-letter ISO), timezone (IANA)
   * Optional: interval (HOURLY|DAILY|WEEKLY|MONTHLY, default DAILY),
   *           minute (default "0"), hour (default "0"),
   *           dayOfWeek (default MONDAY), dayOfMonth (default "1")
   */
  case "create-catalog-feed":
    requireArgs(args, "catalogId", "name", "fileUrl", "currencyCode", "timezone");
    plai("/meta/create_catalog_products_feed", {
      catalogId: args.catalogId,
      name: args.name,
      fileUrl: args.fileUrl,
      currencyCode: args.currencyCode,
      timezone: args.timezone,
      interval:    args.interval    || "DAILY",
      minute:      args.minute      || "0",
      hour:        args.hour        || "0",
      dayOfWeek:   args.dayOfWeek   || "MONDAY",
      dayOfMonth:  args.dayOfMonth  || "1",
    });
    break;

  /**
   * meta_get_catalog_products_feed
   * Required: catalogFeedId
   */
  case "get-catalog-feed":
    requireArgs(args, "catalogFeedId");
    plai("/meta/get_catalog_products_feed", {
      catalogFeedId: args.catalogFeedId,
    });
    break;

  /**
   * meta_get_catalog_products_list
   * Required: productSetId
   */
  case "list-catalog-products":
    requireArgs(args, "productSetId");
    plai("/meta/get_catalog_products_list", {
      productSetId: args.productSetId,
    });
    break;

  /**
   * meta_create_catalog_product_set
   * Required: catalogId, name, productIds (string array, min 1)
   */
  case "create-product-set":
    requireArgs(args, "catalogId", "name", "productIds");
    plai("/meta/create_catalog_product_set", {
      catalogId:  args.catalogId,
      name:       args.name,
      productIds: args.productIds,
    });
    break;

  /**
   * meta_edit_catalog_product_set
   * Required: productSetId, name, productIds (string array, min 1)
   */
  case "edit-product-set":
    requireArgs(args, "productSetId", "name", "productIds");
    plai("/meta/edit_catalog_product_set", {
      productSetId: args.productSetId,
      name:         args.name,
      productIds:   args.productIds,
    });
    break;

  // ── Account Connection ────────────────────────────────────────────────────

  /**
   * create_account_connection_link
   *
   * Generates a link the user opens in their browser to connect their
   * Facebook/Instagram or Google Ads account to Plai.
   *
   * Always run this (and share the link with the user) when any ad tool
   * returns "User has no connected Facebook account" or similar.
   *
   * Required: platform (FACEBOOK | GOOGLE)
   * Optional: redirectUri — URL to redirect after successful connection
   */
  case "create-connection-link":
    requireArgs(args, "platform");
    if (!["FACEBOOK", "GOOGLE"].includes(args.platform)) {
      console.error("Error: --platform must be FACEBOOK or GOOGLE");
      process.exit(1);
    }
    plai("/auth/create_link", {
      platform: args.platform,
      ...(args.redirectUri ? { redirectUri: args.redirectUri } : {}),
    });
    break;

  // ── Page Posts ─────────────────────────────────────────────────────────────

  /**
   * meta_get_page_posts (via get_page_posts endpoint)
   * Required: platform (FACEBOOK | INSTAGRAM)
   * Optional: pagination
   */
  case "list-page-posts":
    requireArgs(args, "platform");
    if (!["FACEBOOK", "INSTAGRAM"].includes(args.platform)) {
      console.error("Error: --platform must be FACEBOOK or INSTAGRAM");
      process.exit(1);
    }
    plai("/meta/get_page_posts", {
      platform: args.platform,
      ...(args.pagination ? { pagination: args.pagination } : {}),
    });
    break;

  // ── Help ───────────────────────────────────────────────────────────────────

  default:
    console.log(`
Plai Meta Ads CLI

Usage: node scripts/plai-meta.js <command> [--key value ...]

Pass JSON arrays/objects as quoted strings: --locations '[{"id":"2537","type":"city","countryCode":"AE"}]'

Campaign Management:
  list-campaigns
  create-campaign
      Required: --campaignName --campaignType --budget --locations
      Required (LEAD_GENERATION):          --leadsFormId
      Required (CONVERSIONS/OUTCOME_SALES): --pixelId --conversionGoal
      Optional: --url --primaryText --headlines --images --videos
                --interests --gender --minAge --maxAge --targetLocales --audienceId
      campaignType: LEAD_GENERATION | LINK_CLICKS | CONVERSIONS | OUTCOME_SALES

  create-message-engagement
      Required: --campaignName --budget --url --locations --messagingApps --multipleCreatives
      Optional: --interests --gender --minAge --maxAge --targetLocales --audienceId
      messagingApps: JSON array of MESSENGER | INSTAGRAM | WHATSAPP
      multipleCreatives: JSON array (1-10) each with:
        Required: url, primaryText, greetingText, conversations:[{title}]
        Optional: headlines, phoneNumber, image, video:{video_id,thumbnail_url}

  get-insights       --campaignId [--startDate YYYY-MM-DD --endDate YYYY-MM-DD --currencySymbol]
  update-status      --campaignId --status (PAUSED|ACTIVE|DELETE)
  update-budget      --campaignId --amount

Lead Forms:
  check-leadform-tos
  list-leadforms
  create-leadform
      Required: --leadsFormName --privacyPolicyUrl --privacyPolicyName
                --website_url --questionPageCustomHeadline

Targeting:
  search-locations   --query
  search-interests   --query [--specialAdCategories --specialAdCountries]
                     specialAdCategories: HOUSING | FINANCIAL_PRODUCTS_SERVICES | EMPLOYMENT
  get-locales

Audiences:
  list-audiences     [--pagination]
  create-page-audience    --name --type (FACEBOOK|INSTAGRAM)
  create-leadform-audience --name --description --type (open|close|submit) --leadFormIds
  create-lookalike   --sourceType (AUDIENCE|PAGE) --audienceName --countryCode
                     (add --sourceId when sourceType=AUDIENCE)

Pixels & Conversions:
  list-pixels
  list-conversions   --pixelId --campaignType (CONVERSIONS|OUTCOME_SALES)

Media:
  list-media         --type (IMAGE|VIDEO) [--pagination]
  list-fb-media      --type (IMAGE|VIDEO) [--pagination]
  list-ig-media      [--pagination]
  upload-video       --videoUrl
  get-video-info     --videoId

Catalogs:
  list-catalogs
  create-catalog         --name
  create-catalog-feed    --catalogId --name --fileUrl --currencyCode --timezone
                         [--interval HOURLY|DAILY|WEEKLY|MONTHLY --hour --minute --dayOfWeek --dayOfMonth]
  get-catalog-feed       --catalogFeedId
  list-catalog-products  --productSetId
  create-product-set     --catalogId --name --productIds
  edit-product-set       --productSetId --name --productIds

Page Posts:
  list-page-posts    --platform (FACEBOOK|INSTAGRAM) [--pagination]

Account Connection:
  create-connection-link  --platform (FACEBOOK|GOOGLE) [--redirectUri]
    Run this when a Meta or Google Ads account is not yet connected.
    Share the returned link with the user to complete OAuth connection.

Environment:
  PLAI_API_KEY    (required)
  PLAI_USER_ID    (required)
  PLAI_BASE_URL   (optional, default: https://public.plai.io)
`);
    process.exit(0);
}
