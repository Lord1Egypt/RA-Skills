# Klaviyo use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/klaviyo

## Analyze Email Campaign Performance

Evaluate campaign engagement, conversions, and attributed revenue to identify opportunities for better email marketing.

- Apps: Klaviyo
- Tools: `KLAVIYO_GET_CAMPAIGNS`, `KLAVIYO_QUERY_CAMPAIGN_VALUES`, `KLAVIYO_GET_CAMPAIGN_CAMPAIGN_MESSAGES`

> Analyze my recent Klaviyo campaign analytics for the requested reporting period. Review available delivery, open, click, conversion, unsubscribe, and attributed-revenue metrics. Compare campaigns using equivalent periods and relevant audience characteristics where possible. Identify the strongest and weakest campaigns, explain the evidence behind the differences, and recommend five experiments involving subject lines, content, CTAs, or audience selection. Distinguish observed metrics from hypotheses, account for missing data, and avoid treating open rates as definitive evidence of purchase intent. Do not send, cancel, or modify campaigns without my approval.

## Build Valuable Customer Segments

Identify meaningful customer groups based on available profile attributes, purchase events, and engagement behavior.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_GET_SEGMENTS`, `KLAVIYO_GET_PROFILES`, `KLAVIYO_CREATE_SEGMENT`

> Analyze available Klaviyo profiles, lists, segments, and events alongside Shopify customer and order information where accessible. Recommend customer segments that could support acquisition, repeat purchases, retention, and re-engagement. For each segment, define its business purpose, eligibility conditions, relevant time window, exclusions, and recommended messaging. Check for overlap with existing segments and flows. Respect marketing consent and suppression status, and do not infer purchase history or engagement that is not supported by the data. Present the proposed segment definitions for approval before creating or modifying any segments.

## Improve Abandoned Cart Recovery

Design a recovery sequence that reminds shoppers about abandoned items and addresses barriers to checkout.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_GET_FLOWS`, `KLAVIYO_GET_EVENTS`, `KLAVIYO_UPDATE_FLOW_STATUS`

> Review my existing marketing flows and available cart-related events to evaluate abandoned-cart recovery. Identify whether a recovery flow already exists, how its messages are timed, and whether audience filters or exclusions may cause duplication. Propose a sequence with appropriate delays, useful product information, clear CTAs, and an optional final reminder. Use verified Shopify product details and available cart information. Do not invent discounts, stock scarcity, or shipping promises. Explain how to exclude customers who have already purchased and how to measure recovered orders. Present proposed changes for approval before creating or activating a flow.

## Create Personalized Email Campaigns

Draft relevant marketing emails using customer segments, product information, and campaign objectives.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_CREATE_CAMPAIGN`, `KLAVIYO_CREATE_CAMPAIGN_RECIPIENT_ESTIMATION_JOB`, `KLAVIYO_UPDATE_CAMPAIGN_MESSAGE`

> Create a Klaviyo email campaign for my Shopify store based on the campaign objective and audience I provide. Draft the subject line, preview text, email body, CTA, and suggested product or collection content. Use available customer attributes and catalog information for relevant personalization, with safe fallbacks when data is missing. Verify pricing, discounts, product availability, destination URLs, and campaign dates. Check the intended audience's eligibility and suppression rules, and estimate recipients where supported. Prepare the campaign and message for review, but do not schedule or send it until I approve the content, audience, and timing.

## Recover Inactive Customer Relationships

Identify eligible customers who have stopped engaging and prepare a targeted re-engagement campaign.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_GET_PROFILES`, `KLAVIYO_GET_SEGMENTS`, `KLAVIYO_GET_SEGMENT_PROFILES`

> Analyze available profile activity, campaign engagement, purchase events, and existing segments to identify potentially inactive customers. Define inactivity using an explicit time window and available evidence rather than assumptions. Exclude customers who have unsubscribed, are suppressed, or otherwise cannot receive the intended marketing messages. Recommend a re-engagement campaign with relevant product discovery, useful content, and a clear preference or unsubscribe path. Check whether an existing flow already targets the same audience. Present the segment definition, expected audience size, message drafts, and measurement plan before creating or sending anything.

## Encourage Repeat Customer Purchases

Find opportunities to encourage a second purchase through relevant product recommendations and post-purchase communication.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_GET_EVENTS`, `KLAVIYO_GET_PROFILES`, `KLAVIYO_GET_CATALOG_ITEMS`

> Analyze Shopify purchase information and available Klaviyo profiles and events to identify customer groups that may benefit from repeat-purchase campaigns. Distinguish first-time buyers, repeat buyers, and customers whose purchase history is incomplete. Recommend relevant post-purchase education, complementary products, or replenishment reminders only when supported by actual catalog relationships and reasonable product-use timing. Avoid assuming every product is consumable or that every customer needs another purchase. Draft the messaging, define audience eligibility and exclusions, and propose measurable success criteria. Check existing flows and obtain approval before activating any new communication.

## Generate Personalized Discount Campaigns

Plan targeted promotional offers while controlling discount usage and avoiding unnecessary margin erosion.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_CREATE_COUPON`, `KLAVIYO_CREATE_COUPON_CODE`, `KLAVIYO_CREATE_CAMPAIGN`

> Design a targeted promotional campaign for my Shopify store using available Klaviyo customer segments, campaign analytics, and catalog information. Identify which audience may benefit from an offer and consider a non-discount alternative. If a discount is justified, propose its value, eligibility, expiration, exclusions, and intended audience based on the information I provide. Verify product pricing and existing coupon rules before preparing any coupon codes. Do not invent margins, promise unauthorized discounts, or create overlapping offers without identifying the conflict. Present the campaign economics, draft content, and estimated recipient count for approval before creating codes or sending the campaign.

## Automate Back In Stock Notifications

Help interested shoppers receive restock notifications when products become available again.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_CREATE_BACK_IN_STOCK_SUBSCRIPTION`, `KLAVIYO_GET_EVENTS`, `KLAVIYO_GET_FLOWS`

> Review available Shopify catalog and inventory information alongside existing Klaviyo back-in-stock events, subscriptions, and flows. Identify products that may benefit from restock notifications and determine whether the necessary subscription and availability data are available. Recommend a process for collecting valid opt-ins, checking product or variant availability, and notifying eligible subscribers when the item returns. Avoid sending notifications for unavailable variants or to customers without the required consent. Check existing flows to prevent duplicate messages. Prepare the proposed setup and message content for review, and do not create subscriptions or activate a flow without the required authorization.

## Maintain Clean Customer Profiles

Detect duplicate profiles, inconsistent attributes, and list-quality issues that can undermine segmentation and reporting.

- Apps: Klaviyo
- Tools: `KLAVIYO_GET_PROFILES`, `KLAVIYO_GET_LIST_PROFILES`, `KLAVIYO_MERGE_PROFILES`

> Audit my available Klaviyo profiles, lists, segments, and profile attributes for potential data-quality issues. Identify likely duplicate profiles, missing or inconsistent fields, unexpected list memberships, and records that may affect campaign eligibility. Match profiles using reliable identifiers and explain the evidence for each suspected duplicate. Do not merge profiles merely because names are similar, and do not change consent or suppression status based on assumptions. Prepare a reconciliation report with recommended corrections and their potential impact. Obtain explicit approval before merging profiles, deleting data, changing list membership, or modifying marketing eligibility.

## Prepare Weekly Marketing Insights

Combine campaign, flow, profile, and event analytics into a concise report with prioritized marketing actions.

- Apps: Klaviyo, Shopify
- Tools: `KLAVIYO_QUERY_CAMPAIGN_VALUES`, `KLAVIYO_QUERY_FLOW_VALUES`, `KLAVIYO_GET_CAMPAIGNS`

> Prepare a weekly Klaviyo marketing report using available campaign analytics, flow performance, profile activity, segment membership, and relevant Shopify sales information. Include key engagement and conversion metrics, attributed revenue where available, top-performing campaigns, underperforming flows, audience changes, and customer-retention opportunities. Compare with the previous equivalent period only when comparable historical data exists. Identify three prioritized actions and explain their expected benefit and evidence. Separate Klaviyo-attributed revenue from total Shopify revenue, disclose data limitations, and avoid claiming causation without supporting evidence. Do not modify campaigns, customer profiles, flows, or consent settings while preparing the report.
