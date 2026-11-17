# Klaviyo tools via Agiexa (225)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects Klaviyo and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/klaviyo

| Tool | What it does |
| --- | --- |
| `KLAVIYO_ADD_PROFILE_TO_LIST` | Add profiles to a Klaviyo list by profile IDs or email addresses |
| `KLAVIYO_ASSIGN_CAMPAIGN_MESSAGE_TEMPLATE` | Creates a non-reusable version of the template and assigns it to the message.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `c |
| `KLAVIYO_BULK_CREATE_CLIENT_EVENTS` | Use the client-side endpoint with a public API key to track profile activity |
| `KLAVIYO_BULK_CREATE_EVENTS` | Bulk create events for multiple profiles in a single request |
| `KLAVIYO_CANCEL_CAMPAIGN_SEND` | Cancel or revert a campaign send job |
| `KLAVIYO_CREATE_BACK_IN_STOCK_SUBSCRIPTION` | Use the server-side endpoint to subscribe to restock alerts, following the Back in Stock API guide |
| `KLAVIYO_CREATE_CAMPAIGN` | Creates a campaign given a set of parameters, then returns it.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:write` |
| `KLAVIYO_CREATE_CAMPAIGN_CLONE` | Clones an existing campaign, returning a new campaign based on the original with a new ID and name.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: |
| `KLAVIYO_CREATE_CAMPAIGN_RECIPIENT_ESTIMATION_JOB` | Start an asynchronous task to estimate the number of recipients for a campaign |
| `KLAVIYO_CREATE_CAMPAIGN_SEND_JOB` | Trigger a campaign to send asynchronously<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:write` |
| `KLAVIYO_CREATE_CATALOG_CATEGORY` | Create a new catalog category.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_CREATE_CATALOG_CATEGORY_RELATIONSHIPS_ITEMS` | Create a new item relationship for the given category ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_CREATE_CATALOG_ITEM` | Create a new catalog item.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_CREATE_CATALOG_ITEM_RELATIONSHIPS_CATEGORIES` | Create a new catalog category relationship for the given item ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:writ |
| `KLAVIYO_CREATE_CATALOG_VARIANT` | Create a new variant for a related catalog item.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_CREATE_CLIENT_BACK_IN_STOCK_SUBSCRIPTION` | Use the endpoint for client-side back in stock notifications with a public API key |
| `KLAVIYO_CREATE_CLIENT_EVENT2` | Create a client-side event in Klaviyo to track user interactions |
| `KLAVIYO_CREATE_CLIENT_SUBSCRIPTION` | Endpoint manages email/SMS opt-ins using consent and requires public API key for client use |
| `KLAVIYO_CREATE_COUPON` | Creates a new coupon.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `coupons:write` |
| `KLAVIYO_CREATE_COUPON_CODE` | Synchronously creates a coupon code for the given coupon.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `coupon-codes:write` |
| `KLAVIYO_CREATE_EVENT` | Create or update a profile event with minimum identifiers and metric name |
| `KLAVIYO_CREATE_LIST` | Create a new list.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m`<br>Daily: `100/d` **Scopes:** `lists:write` |
| `KLAVIYO_CREATE_OR_UPDATE_CLIENT_PROFILE` | Update user profiles without tracking using a public client-side API; use a private server-side API for identifier changes |
| `KLAVIYO_CREATE_OR_UPDATE_CLIENT_PUSH_TOKEN` | This endpoint for mobile SDKs (iOS & Android) creates/updates push tokens using a public API key |
| `KLAVIYO_CREATE_OR_UPDATE_PROFILE` | Create or update a profile in Klaviyo with the given attributes |
| `KLAVIYO_CREATE_OR_UPDATE_PUSH_TOKEN` | Create or update a push token for mobile push notifications |
| `KLAVIYO_CREATE_PROFILE` | Create a new profile.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `profiles:write` |
| `KLAVIYO_CREATE_SEGMENT` | Create a segment.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m`<br>Daily: `100/d` **Scopes:** `segments:write` |
| `KLAVIYO_CREATE_TAG` | Summary: Instructions on creating a tag within an account's designated tag group with a maximum of 500 tags, with optional tag group specification |
| `KLAVIYO_CREATE_TAG_GROUP` | Create tag groups up to 50 per account, defaulting to non-exclusive unless specified |
| `KLAVIYO_CREATE_TAG_RELATIONSHIPS` | Associate a tag with other resources (flows, lists, segments, or campaigns) in Klaviyo |
| `KLAVIYO_CREATE_TEMPLATE` | Summary: Custom HTML templates can be created unless an account reaches 1,000 template limit |
| `KLAVIYO_CREATE_TEMPLATE_CLONE` | Clone a template by its ID, but cloning fails if account has 1,000+ templates |
| `KLAVIYO_CREATE_TEMPLATE_RENDER` | Render an email template with specific context and sparse fieldsets, then get HTML/plain text |
| `KLAVIYO_CREATE_WEBHOOK` | Create a new Webhook to receive real-time notifications when specific events occur in Klaviyo (e.g., email clicks, SMS sent) |
| `KLAVIYO_DELETE_CAMPAIGN` | Delete a campaign with the given campaign ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:write` |
| `KLAVIYO_DELETE_CATALOG_CATEGORY` | Delete a catalog category using the given category ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_DELETE_CATALOG_CATEGORY_RELATIONSHIPS_ITEMS` | Delete item relationships for the given category ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_DELETE_CATALOG_ITEM` | Delete a catalog item with the given item ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_DELETE_CATALOG_ITEM_RELATIONSHIPS_CATEGORIES` | Delete catalog category relationships for the given item ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_DELETE_CATALOG_VARIANT` | Delete a catalog item variant with the given variant ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_DELETE_COUPON` | Delete the coupon with the given coupon ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `coupons:write` |
| `KLAVIYO_DELETE_COUPON_CODE` | Deletes a coupon code specified by the given identifier synchronously |
| `KLAVIYO_DELETE_FLOW` | Delete a flow with the given flow ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:write` |
| `KLAVIYO_DELETE_LIST` | Delete a list with the given list ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `lists:write` |
| `KLAVIYO_DELETE_SEGMENT` | Delete a segment with the given segment ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `segments:write` |
| `KLAVIYO_DELETE_TAG` | Delete the tag with the given tag ID |
| `KLAVIYO_DELETE_TAG_GROUP` | Delete a specified tag group and its contents; associated resource links will be removed |
| `KLAVIYO_DELETE_TAG_RELATIONSHIPS` | Remove a tag's association with other resources like flows, campaigns, lists, or segments |
| `KLAVIYO_DELETE_TEMPLATE` | Permanently delete a template from your Klaviyo account using its unique template ID |
| `KLAVIYO_DELETE_WEBHOOK` | Permanently delete a webhook subscription from your Klaviyo account |
| `KLAVIYO_GET_ACCOUNT` | Retrieve a single account object by its account ID |
| `KLAVIYO_GET_ACCOUNTS` | Use a private API key to fetch an associated account's details like contact info, timezone, and currency, as well as validate the key |
| `KLAVIYO_GET_BULK_CREATE_COUPON_CODES_JOB` | Tool to get a coupon code bulk create job with the given job ID |
| `KLAVIYO_GET_BULK_DELETE_CATALOG_ITEMS_JOB` | Get a catalog item bulk delete job with the given job ID |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB` | Get a bulk profile import job with the given job ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `lists:read` `profiles:read |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB_ERRORS` | Get import errors for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `profiles:r |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB_LISTS` | Get list for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `lists:read` |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB_PROFILES` | Get profiles for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `profiles:read` |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB_RELATIONSHIPS_LISTS` | Get list relationship for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `lists: |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOB_RELATIONSHIPS_PROFILES` | Get profile relationships for the bulk profile import job with the given ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `pr |
| `KLAVIYO_GET_BULK_PROFILE_IMPORT_JOBS` | Get all bulk profile import jobs |
| `KLAVIYO_GET_BULK_UPDATE_CATALOG_ITEMS_JOB` | Get a catalog item bulk update job with the given job ID |
| `KLAVIYO_GET_BULK_UPDATE_CATEGORIES_JOB` | Retrieve a catalog category bulk update job by its ID from Klaviyo |
| `KLAVIYO_GET_BULK_UPDATE_VARIANTS_JOB` | Tool to retrieve a catalog variant bulk update job by its ID |
| `KLAVIYO_GET_CAMPAIGN` | Retrieve a specific campaign by its ID from Klaviyo |
| `KLAVIYO_GET_CAMPAIGN_CAMPAIGN_MESSAGES` | Return all messages that belong to the given campaign.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` |
| `KLAVIYO_GET_CAMPAIGN_MESSAGE` | Returns a specific message based on a required id.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` |
| `KLAVIYO_GET_CAMPAIGN_MESSAGE_CAMPAIGN` | Return the related campaign<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` |
| `KLAVIYO_GET_CAMPAIGN_MESSAGE_RELATIONSHIPS_CAMPAIGN` | Returns the ID of the related campaign<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` |
| `KLAVIYO_GET_CAMPAIGN_MESSAGE_RELATIONSHIPS_TEMPLATE` | Returns the ID of the related template<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` `templates:read` |
| `KLAVIYO_GET_CAMPAIGN_MESSAGE_TEMPLATE` | Return the related template<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` `templates:read` |
| `KLAVIYO_GET_CAMPAIGN_RECIPIENT_ESTIMATION` | Get estimated recipients for a given campaign ID using `Create Campaign Recipient Estimation Job` |
| `KLAVIYO_GET_CAMPAIGN_RECIPIENT_ESTIMATION_JOB` | Retrieve the status of a recipient estimation job triggered with the `Create Campaign Recipient Estimation Job` endpoint.<br><br>*Rate limits*:<br>Bur |
| `KLAVIYO_GET_CAMPAIGN_RELATIONSHIPS_CAMPAIGN_MESSAGES` | Returns the IDs of all messages associated with the given campaign.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:r |
| `KLAVIYO_GET_CAMPAIGN_RELATIONSHIPS_TAGS` | Returns the IDs of all tags associated with the given campaign.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `campaigns:read` ` |
| `KLAVIYO_GET_CAMPAIGNS` | Retrieve campaigns from your Klaviyo account |
| `KLAVIYO_GET_CAMPAIGN_SEND_JOB` | Get a campaign send job<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:read` |
| `KLAVIYO_GET_CAMPAIGN_TAGS` | Return all tags that belong to the given campaign.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `campaigns:read` `tags:read` |
| `KLAVIYO_GET_CATALOG_CATEGORIES` | Retrieve up to 100 account catalog categories, sortable by creation date |
| `KLAVIYO_GET_CATALOG_CATEGORY` | Get a catalog category with the given category ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `catalogs:read` |
| `KLAVIYO_GET_CATALOG_CATEGORY_ITEMS` | Retrieve up to 100 sorted items per request from a category using the category ID |
| `KLAVIYO_GET_CATALOG_CATEGORY_RELATIONSHIPS_ITEMS` | Get all items in the given category ID |
| `KLAVIYO_GET_CATALOG_ITEM` | Get a specific catalog item with the given item ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `catalogs:read` |
| `KLAVIYO_GET_CATALOG_ITEM_CATEGORIES` | Retrieve the catalog categories for an item by ID, sorted by 'created' date, with a 100-category maximum per request |
| `KLAVIYO_GET_CATALOG_ITEM_RELATIONSHIPS_CATEGORIES` | Get all catalog categories that a particular item is in |
| `KLAVIYO_GET_CATALOG_ITEMS` | Retrieve up to 100 sorted catalog items per account, with `$custom` integration and `$default` type |
| `KLAVIYO_GET_CATALOG_ITEM_VARIANTS` | Retrieve up to 100 variants per request for a specific item ID, sortable by creation date |
| `KLAVIYO_GET_CATALOG_VARIANT` | Get a catalog item variant with the given variant ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `catalogs:read` |
| `KLAVIYO_GET_CATALOG_VARIANTS` | Retrieve up to 100 account variants per request, sortable by creation date |
| `KLAVIYO_GET_COUPON` | Get a specific coupon with the given coupon ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `coupons:read` |
| `KLAVIYO_GET_COUPON_CODE` | Returns a Coupon Code specified by the given identifier.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `coupon-codes:read` |
| `KLAVIYO_GET_COUPON_CODE_BULK_CREATE_JOB` | Get a coupon code bulk create job with the given job ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `coupon-codes:read` |
| `KLAVIYO_GET_COUPON_CODE_BULK_CREATE_JOBS` | Get all coupon code bulk create jobs |
| `KLAVIYO_GET_COUPON_CODE_RELATIONSHIPS_COUPON` | Gets a list of coupon code relationships associated with the given coupon id<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `co |
| `KLAVIYO_GET_COUPON_CODES` | Obtains coupon codes using necessary coupon or profile filters |
| `KLAVIYO_GET_COUPON_CODES_FOR_COUPON` | Gets a list of coupon codes associated with the given coupon id<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `coupon-codes:re |
| `KLAVIYO_GET_COUPON_FOR_COUPON_CODE` | Get the coupon associated with a given coupon code ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `coupons:read` |
| `KLAVIYO_GET_COUPON_ID_FOR_COUPON_CODE` | Tool to get the coupon relationship associated with a given coupon code ID |
| `KLAVIYO_GET_COUPON_RELATIONSHIPS_COUPON_CODES` | Retrieves the coupon code relationships (resource identifiers) for a given coupon |
| `KLAVIYO_GET_COUPONS` | Get all coupons in an account |
| `KLAVIYO_GET_CREATE_CATEGORIES_JOB` | Get a catalog category bulk create job with the given job ID |
| `KLAVIYO_GET_CREATE_CATEGORIES_JOBS` | Get all catalog category bulk create jobs |
| `KLAVIYO_GET_CREATE_ITEMS_JOB` | Get a catalog item bulk create job with the given job ID |
| `KLAVIYO_GET_CREATE_ITEMS_JOBS` | Get all catalog item bulk create jobs |
| `KLAVIYO_GET_CREATE_VARIANTS_JOB` | Get a catalog variant bulk create job with the given job ID |
| `KLAVIYO_GET_CREATE_VARIANTS_JOBS` | Get all catalog variant bulk create jobs |
| `KLAVIYO_GET_DELETE_CATEGORIES_JOB` | Get a catalog category bulk delete job with the given job ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `catalogs:read` |
| `KLAVIYO_GET_DELETE_CATEGORIES_JOBS` | Get all catalog category bulk delete jobs |
| `KLAVIYO_GET_DELETE_ITEMS_JOBS` | Get all catalog item bulk delete jobs |
| `KLAVIYO_GET_DELETE_VARIANTS_JOB` | Get a catalog variant bulk delete job with the given job ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `catalogs:read` |
| `KLAVIYO_GET_DELETE_VARIANTS_JOBS` | Get all catalog variant bulk delete jobs |
| `KLAVIYO_GET_EVENT` | Get an event with the given event ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `events:read` |
| `KLAVIYO_GET_EVENT_METRIC` | Get the metric for an event with the given event ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `events:read` `metrics:re |
| `KLAVIYO_GET_EVENT_PROFILE` | Get the profile associated with an event with the given event ID.<br><br>*Rate limits*:<br>Burst: `350/s`<br>Steady: `3500/m` **Scopes:** `events:read |
| `KLAVIYO_GET_EVENT_RELATIONSHIPS` | Get metrics or profile relationships for a specific event |
| `KLAVIYO_GET_EVENTS` | Get all events in an account Requests can be sorted by the following fields: `datetime`, `timestamp` Returns a maximum of 200 events per page.<br><br> |
| `KLAVIYO_GET_FLOW` | Get a flow with the given flow ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` |
| `KLAVIYO_GET_FLOW_ACTION` | Get a flow action from a flow with the given flow action ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` |
| `KLAVIYO_GET_FLOW_ACTION_FOR_MESSAGE` | Get the flow action for a flow message with the given message ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` |
| `KLAVIYO_GET_FLOW_ACTION_MESSAGES` | Retrieve up to 50 flow messages per request by action ID, sortable by various fields, with ascending/descending options, and paginated using `page[siz |
| `KLAVIYO_GET_FLOW_ACTION_RELATIONSHIPS_FLOW` | Get the parent flow associated with a given flow action ID |
| `KLAVIYO_GET_FLOW_ACTION_RELATIONSHIPS_MESSAGES` | Retrieves up to 50 flow message relationships per request for a specified flow action ID, with cursor pagination |
| `KLAVIYO_GET_FLOW_FLOW_ACTIONS` | Get all flow actions associated with the given flow ID |
| `KLAVIYO_GET_FLOW_FOR_FLOW_ACTION` | Get the flow associated with the given action ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` |
| `KLAVIYO_GET_FLOW_MESSAGE` | Get the flow message of a flow with the given message ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` |
| `KLAVIYO_GET_FLOW_MESSAGE_RELATIONSHIPS_ACTION` | Get the flow action relationship for a specific flow message |
| `KLAVIYO_GET_FLOW_MESSAGE_RELATIONSHIPS_TEMPLATE` | Returns the ID of the related template<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `templates:read` |
| `KLAVIYO_GET_FLOW_MESSAGE_TEMPLATE` | Return the related template<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `templates:read` |
| `KLAVIYO_GET_FLOW_RELATIONSHIPS_FLOW_ACTIONS` | Retrieve all flow action relationships for a specific flow ID, sortable by `id`, `status`, `created`, `updated` |
| `KLAVIYO_GET_FLOW_RELATIONSHIPS_TAGS` | Return the tag IDs of all tags associated with the given flow.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` `tags: |
| `KLAVIYO_GET_FLOWS` | Get all flows in an account |
| `KLAVIYO_GET_FLOW_TAGS` | Return all tags associated with the given flow ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `flows:read` `tags:read` |
| `KLAVIYO_GET_FORM` | Get the form with the given ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_FORM_FOR_FORM_VERSION` | Get the form associated with the given form version.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_FORM_ID_FOR_FORM_VERSION` | Get the ID of the form associated with the given form version.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_FORMS` | Get all forms in an account.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_FORM_VERSION` | Retrieve detailed information about a specific form version by its ID |
| `KLAVIYO_GET_IMAGE` | Get the image with the given image ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `images:read` |
| `KLAVIYO_GET_IMAGES` | Get all images in an account.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `images:read` |
| `KLAVIYO_GET_LIST` | API allows 75 req/sec and 700 req/min, but with 'profile_count' param, it's 1 req/sec and 15 req/min |
| `KLAVIYO_GET_LIST_PROFILES` | Retrieve profiles in a list by ID, filterable by email/phone/push token/join date, sortable by join date |
| `KLAVIYO_GET_LIST_RELATIONSHIPS` | Get profile membership relationships for a Klaviyo list |
| `KLAVIYO_GET_LIST_RELATIONSHIPS_TAGS` | Returns the tag IDs of all tags associated with the given list.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `lists:read` `tags |
| `KLAVIYO_GET_LISTS` | Retrieve marketing lists from your Klaviyo account |
| `KLAVIYO_GET_LIST_TAGS` | Return all tags associated with the given list ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `lists:read` `tags:read` |
| `KLAVIYO_GET_METRIC` | Get a metric with the given metric ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `metrics:read` |
| `KLAVIYO_GET_METRICS` | Get all metrics in an account |
| `KLAVIYO_GET_PROFILE` | Get the profile with the given profile ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `profiles:read` |
| `KLAVIYO_GET_PROFILE_LISTS` | Get list memberships for a profile with the given profile ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `lists:read` `profil |
| `KLAVIYO_GET_PROFILE_RELATIONSHIPS` | Tool to get list membership or segment membership relationships for a profile with the given profile ID |
| `KLAVIYO_GET_PROFILES` | Retrieve profiles from your Klaviyo account |
| `KLAVIYO_GET_PROFILE_SEGMENTS` | Get segment memberships for a profile with the given profile ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `profiles:read` ` |
| `KLAVIYO_GET_SEGMENT` | Fetch a segment by ID with default rates of 75/s and 700/m, or with `additional-fields` at 1/s and 15/m |
| `KLAVIYO_GET_SEGMENT_PROFILES` | Retrieve profiles in a segment by ID, filtering by email, phone, token, or join date, and sorting by join date |
| `KLAVIYO_GET_SEGMENT_RELATIONSHIPS` | Get all profile membership or tag relationships for a segment |
| `KLAVIYO_GET_SEGMENTS` | Fetch segments from an account with filters like `name`, `created`, and `updated` |
| `KLAVIYO_GET_SEGMENT_TAGS` | Return all tags associated with the given segment ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `segments:read` `tags:read` |
| `KLAVIYO_GET_TAG` | Retrieve the tag with the given tag ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `tags:read` |
| `KLAVIYO_GET_TAG_GROUP` | Retrieve the tag group with the given tag group ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `tags:read` |
| `KLAVIYO_GET_TAG_GROUP_RELATIONSHIPS_TAGS` | Returns the tag IDs of all tags inside the given tag group.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `tags:read` |
| `KLAVIYO_GET_TAG_GROUPS` | Retrieve up to 25 tag groups per account, sortable/filterable by specific attributes |
| `KLAVIYO_GET_TAG_GROUP_TAGS` | Return the tags for a given tag group ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `tags:read` |
| `KLAVIYO_GET_TAG_RELATIONSHIPS` | Tool to retrieve relationship IDs for a tag |
| `KLAVIYO_GET_TAGS` | Retrieve up to 50 account tags at once, filterable/sortable by name or id, with cursor pagination |
| `KLAVIYO_GET_TAG_TAG_GROUP` | Returns the tag group resource for a given tag ID.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `tags:read` |
| `KLAVIYO_GET_TEMPLATE` | Get a template with the given template ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `templates:read` |
| `KLAVIYO_GET_TEMPLATES` | Retrieve account templates with sorting options (`id`, `name`, `created`, `updated`) |
| `KLAVIYO_GET_UPDATE_CATEGORIES_JOBS` | Get all catalog category bulk update jobs |
| `KLAVIYO_GET_UPDATE_ITEMS_JOB` | Get a catalog item bulk update job with the given job ID |
| `KLAVIYO_GET_UPDATE_ITEMS_JOBS` | Get all catalog item bulk update jobs |
| `KLAVIYO_GET_UPDATE_VARIANTS_JOBS` | Get all catalog variant bulk update jobs |
| `KLAVIYO_GET_VARIANT_IDS_FOR_CATALOG_ITEM` | Tool to get all variant IDs related to a given catalog item ID |
| `KLAVIYO_GET_VERSION_IDS_FOR_FORM` | Get the IDs of the form versions for the given form.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_VERSIONS_FOR_FORM` | Get the form versions for the given form.<br><br>*Rate limits*:<br>Burst: `3/s`<br>Steady: `60/m` **Scopes:** `forms:read` |
| `KLAVIYO_GET_WEBHOOK` | Get the webhook with the given ID.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m` **Scopes:** `webhooks:read` |
| `KLAVIYO_GET_WEBHOOKS` | Get all webhooks in an account.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m` **Scopes:** `webhooks:read` |
| `KLAVIYO_GET_WEBHOOK_TOPIC` | Retrieve details of a specific webhook topic by its ID |
| `KLAVIYO_GET_WEBHOOK_TOPICS` | Get all webhook topics in a Klaviyo account.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m` **Scopes:** `webhooks:read` |
| `KLAVIYO_MERGE_PROFILES` | Merge one or more source profiles into a destination profile |
| `KLAVIYO_QUERY_CAMPAIGN_VALUES` | Returns the requested campaign analytics values data<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `2/m`<br>Daily: `225/d` **Scopes:** `campaigns:r |
| `KLAVIYO_QUERY_FLOW_SERIES` | Returns time-series analytics data for flows, enabling performance tracking over time intervals |
| `KLAVIYO_QUERY_FLOW_VALUES` | Returns the requested flow analytics values data<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `2/m`<br>Daily: `225/d` **Scopes:** `flows:read` |
| `KLAVIYO_QUERY_METRIC_AGGREGATES` | The Klaviyo endpoint fetches metric events, handling JSON requests for custom data queries, sorting, and filtering; offers grouping and time-based fil |
| `KLAVIYO_REMOVE_PROFILE_FROM_LIST` | Remove profiles from a Klaviyo list by profile IDs or email addresses |
| `KLAVIYO_REQUEST_PROFILE_DELETION` | To delete a profile, use only one identifier: email, phone number, or ID |
| `KLAVIYO_SPAWN_BULK_PROFILE_IMPORT_JOB` | Initiate a job to create/update a batch of profiles, up to 10,000 with a max size of 5MB per request |
| `KLAVIYO_SPAWN_COUPON_CODE_BULK_CREATE_JOB` | Create a coupon-code-bulk-create-job to bulk create a list of coupon codes |
| `KLAVIYO_SPAWN_CREATE_CATEGORIES_JOB` | Create bulk job for up to 100 catalog categories with a 5MB size limit and a max of 500 concurrent jobs |
| `KLAVIYO_SPAWN_CREATE_ITEMS_JOB` | Create batches of up to 100 catalog items with a 5MB size limit using the bulk job, which allows 500 concurrent jobs |
| `KLAVIYO_SPAWN_CREATE_VARIANTS_JOB` | Initiate a job to bulk create up to 100 catalog variants, with a 5MB payload size limit |
| `KLAVIYO_SPAWN_DELETE_CATEGORIES_JOB` | Delete multiple catalog categories in bulk, with a limit of 100 per request and a 5MB payload size |
| `KLAVIYO_SPAWN_DELETE_ITEMS_JOB` | Delete batches of catalog items with a bulk job, max 100 items/request, 5MB size limit, and up to 500 concurrent jobs |
| `KLAVIYO_SPAWN_DELETE_VARIANTS_JOB` | Delete multiple catalog variants with a bulk job, max 100 per request, 5MB size limit |
| `KLAVIYO_SPAWN_UPDATE_CATEGORIES_JOB` | Create a job to bulk update up to 100 categories, with a 5MB size limit and a maximum of 500 concurrent jobs |
| `KLAVIYO_SPAWN_UPDATE_ITEMS_JOB` | You can bulk update up to 100 catalog items with a 5MB payload limit |
| `KLAVIYO_SPAWN_UPDATE_VARIANTS_JOB` | Create a job to bulk update up to 100 catalog variants with a 5MB payload limit |
| `KLAVIYO_SUBSCRIBE_PROFILES` | The API supports double opt-in for marketing, with 'historical_import' bypassing consent |
| `KLAVIYO_SUPPRESS_PROFILES` | Suppress profiles by email, segment, or list ID to stop email marketing, regardless of consent |
| `KLAVIYO_UNREGISTER_CLIENT_PUSH_TOKEN` | This endpoint unsubscribes a push token, for use with Klaviyo's mobile SDKs and a public API key |
| `KLAVIYO_UNSUBSCRIBE_PROFILES` | Opt-out profiles from email or SMS marketing |
| `KLAVIYO_UNSUBSCRIBE_PROFILES_BULK` | Tool to unsubscribe one or more profiles from a Klaviyo list |
| `KLAVIYO_UNSUPPRESS_PROFILES` | Remove 'USER_SUPPRESSED' blocks on profiles manually via email, segment, or list ID |
| `KLAVIYO_UNSUPPRESS_PROFILES_BULK` | Tool to unsuppress one or more profiles from email marketing by email address |
| `KLAVIYO_UPDATE_CAMPAIGN` | Update a campaign with the specified attributes |
| `KLAVIYO_UPDATE_CAMPAIGN_MESSAGE` | Update a campaign message<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `campaigns:write` |
| `KLAVIYO_UPDATE_CATALOG_CATEGORY` | Update a catalog category with the given category ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_UPDATE_CATALOG_CATEGORY_RELATIONSHIPS` | Tool to update item relationships for a catalog category |
| `KLAVIYO_UPDATE_CATALOG_CATEGORY_RELATIONSHIPS_ITEMS` | Update item relationships for the given category ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_UPDATE_CATALOG_ITEM` | Update a catalog item with the given item ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_UPDATE_CATALOG_ITEM_RELATIONSHIPS_CATEGORIES` | Update catalog category relationships for the given item ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_UPDATE_CATALOG_VARIANT` | Update a catalog item variant with the given variant ID.<br><br>*Rate limits*:<br>Burst: `75/s`<br>Steady: `700/m` **Scopes:** `catalogs:write` |
| `KLAVIYO_UPDATE_COUPON` | Update an existing coupon's properties |
| `KLAVIYO_UPDATE_COUPON_CODE` | Updates a coupon code specified by the given identifier synchronously |
| `KLAVIYO_UPDATE_FLOW_STATUS` | Update the status of a flow with the given flow ID, and all actions in that flow |
| `KLAVIYO_UPDATE_IMAGE` | Update the image with the given image ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `images:write` |
| `KLAVIYO_UPDATE_LIST` | Update the name of a list with the given list ID.<br><br>*Rate limits*:<br>Burst: `10/s`<br>Steady: `150/m` **Scopes:** `lists:write` |
| `KLAVIYO_UPDATE_PROFILE` | Update profiles with the provided ID |
| `KLAVIYO_UPDATE_SEGMENT` | Update a segment with the given segment ID.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m`<br>Daily: `100/d` **Scopes:** `segments:write` |
| `KLAVIYO_UPDATE_TAG` | Update the tag with the given tag ID |
| `KLAVIYO_UPDATE_TAG_GROUP` | Update the tag group with the given tag group ID |
| `KLAVIYO_UPDATE_TEMPLATE` | Update an existing email template by ID |
| `KLAVIYO_UPDATE_WEBHOOK` | Update the webhook with the given ID.<br><br>*Rate limits*:<br>Burst: `1/s`<br>Steady: `15/m` **Scopes:** `webhooks:write` |
| `KLAVIYO_UPLOAD_IMAGE_FROM_FILE` | Upload an image from a file |
| `KLAVIYO_UPLOAD_IMAGE_FROM_URL` | Import an image from a url or data uri |
