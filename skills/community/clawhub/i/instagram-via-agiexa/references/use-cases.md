# Instagram use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/instagram

## Analyze Instagram Content Performance

Identify top-performing Reels, carousels, and posts using reach, engagement, and account insights. Turn the results into actionable content recommendations.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_USER_INSIGHTS`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`

> Analyze my Instagram account's performance using available account-level insights and recent media metrics. Identify my top-performing posts, Reels, and carousels by reach, interactions, and other available metrics. Compare performance across content types where the data supports a fair comparison. Explain which patterns may be contributing to engagement, identify underperforming content, and recommend five experiments for the next week. Clearly distinguish observed data from assumptions, account for missing metrics, and do not claim that engagement directly caused sales unless verified through Shopify or other available conversion data.

## Generate Product Promotion Content Ideas

Turn Shopify products, customer questions, and successful Instagram content into relevant Reel, carousel, and Story ideas.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`

> Review my Shopify product catalog and recent Instagram content. Generate ten Instagram content ideas that promote relevant products without repeating the same concept. For each idea, provide a 5-6-word title, target audience, content format, opening hook, key message, suggested visual sequence, caption draft, CTA, and relevant hashtags. Prioritize ideas inspired by products and content that have demonstrated strong engagement, but do not assume that engagement guarantees sales. Use only verified product features and pricing, and flag any information that needs confirmation.

## Prepare Instagram Posts for Publishing

Create publication-ready captions and media plans for product launches, promotions, and brand updates, with approval before publishing.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_POST_IG_USER_MEDIA`, `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`, `INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT`

> Prepare an Instagram post for my Shopify store using the product and campaign information I provide. Create a suitable caption, opening hook, CTA, hashtags, and a suggested visual concept. If I request a Reel, provide a short scene-by-scene script and on-screen text. Verify product details, pricing, discount terms, campaign dates, and destination URLs against available information. If any essential information is missing, ask me rather than inventing it. Prepare the media container or publishing draft only when the required asset and details are available. Show me the final content and obtain my approval before publishing.

## Respond to Customer Comments Effectively

Understand product-related comments, prioritize purchase questions, and prepare relevant replies that match the brand's tone.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_IG_MEDIA_COMMENTS`, `INSTAGRAM_POST_IG_COMMENT_REPLIES`, `INSTAGRAM_POST_IG_MEDIA_COMMENTS`

> Review recent comments on my Instagram posts and identify comments that need a response. Categorize them as product questions, purchase intent, positive feedback, complaints, spam, or other relevant categories. Draft a concise, friendly, brand-appropriate reply for each comment. Use Shopify product data and verified store policies when answering questions about prices, availability, shipping, and returns. Flag complaints and sensitive cases for human review. Do not delete comments or publish replies without my approval. If a comment is abusive or spam-like, explain why it may need moderation instead of automatically deleting it.

## Manage Instagram Direct Messages Efficiently

Review customer conversations, identify unanswered questions, and prepare personalized replies based on verified store information.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_LIST_ALL_CONVERSATIONS`, `INSTAGRAM_LIST_ALL_MESSAGES`, `INSTAGRAM_SEND_TEXT_MESSAGE`, `INSTAGRAM_MARK_SEEN`

> Review my available Instagram DM conversations and identify messages that need a response. Summarize each conversation, identify the customer's main question, assess purchase intent, and prioritize urgent or high-intent inquiries. Where appropriate, match the customer's question to relevant Shopify products and verify the information before drafting a reply. Prepare personalized responses for product availability, pricing, shipping, order-related questions, and bulk purchases. Do not expose private customer information, invent order status or policies, or send messages without my approval. Highlight conversations that require human support.

## Compare Instagram Engagement With Sales

Connect social content performance with Shopify sales data to investigate which content may be contributing to store visits and purchases.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`, `INSTAGRAM_GET_USER_INSIGHTS`

> Analyze my available Instagram media insights alongside Shopify sales and product data. Identify posts that may be associated with increased interest in relevant products. Compare post dates, product references, engagement, and available store performance metrics. Use campaign links, attribution data, or other reliable evidence if available. Separate verified correlations from possible explanations, and do not claim that a specific post generated an order without supporting attribution. Recommend which content to repeat, which products deserve more promotion, and what tracking improvements would help measure Instagram-driven revenue more accurately.

## Turn Customer Questions Into Content

Use recurring Instagram comments and DMs to identify common customer concerns and create useful content that answers them.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_IG_MEDIA_COMMENTS`, `INSTAGRAM_LIST_ALL_MESSAGES`

> Analyze recent Instagram comments and DM conversations to find recurring customer questions, objections, and product information gaps. Group similar questions into themes, count them where the available data allows, and identify which themes appear most frequently. Match each theme to relevant Shopify products when possible. Recommend five educational posts, Reels, or carousels that answer these questions. For each recommendation, include a hook, key points, suggested visual format, caption draft, and CTA. Protect customer privacy by excluding names and personal details. Do not invent trends from a small or incomplete sample.

## Monitor Instagram Account Performance

Track account insights and recent content performance to identify meaningful changes and recommend practical adjustments.

- Apps: Instagram
- Tools: `INSTAGRAM_GET_USER_INSIGHTS`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`

> Review my Instagram account insights and recent media metrics for the available reporting period. Summarize changes in follower count, reach, profile activity, and engagement where those metrics are available. Identify notable increases or decreases, compare equivalent time periods when possible, and investigate which posts may explain the changes. Recommend specific actions for content creation and audience engagement. State the reporting period, missing data, and limitations clearly. Do not describe a metric as increasing or decreasing unless the comparison supports that conclusion, and do not assume that a change in followers directly translates into sales.

## Improve Instagram Profile Conversion

Identify opportunities to make the Instagram profile, messaging, and content more effective at guiding shoppers toward relevant Shopify products.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_USER_INFO`, `INSTAGRAM_LIST_ALL_CONVERSATIONS`, `INSTAGRAM_UPDATE_MESSENGER_PROFILE`

> Review the available information about my Instagram professional account, recent content, customer conversations, and Shopify store. Identify potential friction points between discovering a product and finding or purchasing it. Evaluate the clarity of the profile information, content CTAs, product links, common customer questions, and available profile-activity metrics. Recommend improvements to the bio, content messaging, product discovery flow, and DM responses. Distinguish directly observable issues from hypotheses that require testing. Do not change account settings, profile details, or published content without showing me the proposed changes and obtaining my approval.

## Create a Weekly Instagram Marketing Report

Combine account insights, post performance, customer conversations, and Shopify data into a concise weekly marketing report.

- Apps: Instagram, Shopify
- Tools: `INSTAGRAM_GET_USER_INSIGHTS`, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS`, `INSTAGRAM_LIST_ALL_CONVERSATIONS`

> Prepare a weekly Instagram marketing report for my Shopify business using the available account insights, recent media metrics, comments, DM conversations, and relevant Shopify data. Include key performance metrics, top-performing content, underperforming posts, recurring customer questions, potential purchase-intent signals, and recommended actions for the next week. Compare the current period with the previous equivalent period when data is available. Include a table of the top posts and explain why each may deserve further testing. Separate confirmed sales results from engagement metrics and unverified attribution. End with three prioritized actions, their rationale, and the additional data needed to measure their impact.
