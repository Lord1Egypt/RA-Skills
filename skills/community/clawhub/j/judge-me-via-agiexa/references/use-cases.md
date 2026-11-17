# Judge.me use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/judge-me

## Identify Products With Poor Ratings

Find the lowest-rated Shopify products and investigate the customer feedback behind their ratings.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_PRODUCT_RATING_SUMMARY`, `JUDGEME_COUNT_REVIEWS`, `JUDGEME_GET_PRODUCT`

> Analyze my Judge.me product rating summaries and review counts. Identify the lowest-rated products, prioritizing those with enough reviews to make the comparison meaningful. Retrieve the associated reviews for these products and summarize recurring positive and negative themes. Match each product to its Shopify product information where possible. Recommend which products need investigation first and explain the evidence behind each recommendation. Clearly distinguish low ratings from low review counts, flag small samples, and do not invent complaint themes or claim a product has a defect without supporting review evidence.

## Summarize Customer Review Sentiment

Turn customer reviews into a concise report of satisfaction levels, recurring complaints, and product strengths.

- Apps: Judge.me
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_COUNT_REVIEWS`

> Review my available Judge.me product and store reviews. Summarize the overall rating distribution, recurring positive themes, recurring negative themes, and common customer suggestions. Group similar feedback together and include representative review examples where useful. Report counts and percentages only when the available data supports the calculation. Separate product-specific issues from shipping, packaging, service, and other concerns. Identify limitations caused by pagination or incomplete review data. Do not treat a small sample as representative of all customers, and do not invent review content.

## Draft Responses to Negative Reviews

Prepare empathetic, professional replies that acknowledge customer concerns and suggest appropriate next steps.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_REPLY_TO_REVIEW`, `JUDGEME_SEND_PRIVATE_REPLY`

> Find recent one-star, two-star, and other negative Judge.me reviews that may need a response. Retrieve each review's details and draft a personalized, empathetic reply that addresses the customer's actual concern. Use verified Shopify product information and available store policies where relevant. Do not blame the customer, make unsupported promises, disclose private order information publicly, or offer refunds or compensation without authorization. Recommend a public reply for general acknowledgment and a private email for sensitive or order-specific troubleshooting. Show me the review, proposed response, and recommended response type. Do not publish or send anything until I approve it.

## Respond to Positive Customer Reviews

Recognize satisfied customers with authentic replies that reinforce the brand's relationship with its audience.

- Apps: Judge.me
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_GET_REVIEW`, `JUDGEME_REPLY_TO_REVIEW`

> Review recent positive Judge.me product and store reviews and identify those that would benefit from a personalized response. Draft short, friendly replies that reflect the specific feedback rather than using the same generic message everywhere. Where appropriate, mention the verified product name and acknowledge the customer's stated experience. Do not invent personal details, claim that the customer made a repeat purchase without evidence, or add promotional language that feels misleading. Present each review with its suggested response and ask for approval before publishing any public replies.

## Find Recurring Product Quality Issues

Detect repeated complaints across reviews to help prioritize product improvements and supplier investigations.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_PRODUCT_RATING_SUMMARY`, `JUDGEME_COUNT_REVIEWS`

> Analyze the available Judge.me reviews for recurring product complaints. Group feedback into themes such as durability, performance, fit, packaging, instructions, and other themes actually present in the reviews. For each theme, provide the affected products, supporting review examples, the number of matching reviews when reliably countable, and the severity suggested by the feedback. Prioritize issues based on frequency, rating, and potential customer impact. Distinguish reported experiences from confirmed product defects. Recommend which issues deserve supplier investigation, product-description changes, or support improvements, and identify where more evidence is needed.

## Find Products With Strong Reviews

Identify highly rated products and use genuine customer feedback to suggest better product merchandising.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_PRODUCT_RATING_SUMMARY`, `JUDGEME_LIST_REVIEWS`, `JUDGEME_GET_PRODUCT`

> Find my highest-rated Shopify products using Judge.me rating summaries and review counts. Prioritize products with both strong ratings and a meaningful number of reviews. Retrieve relevant positive reviews and identify specific, verifiable product benefits that customers mention repeatedly. Recommend improvements to product descriptions, merchandising, and content ideas based on these themes. Match reviews to the correct products and preserve the meaning of customer statements. Do not invent testimonials, imply that all customers share the same opinion, or treat a high rating with very few reviews as conclusive evidence of broad customer satisfaction.

## Investigate Rating Changes Over Time

Compare available review records to investigate whether recent feedback indicates a possible change in customer satisfaction.

- Apps: Judge.me
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_COUNT_REVIEWS`, `JUDGEME_PRODUCT_RATING_SUMMARY`

> Analyze the available Judge.me reviews and rating summaries to investigate potential changes in customer satisfaction. Compare reviews across time periods if reliable dates and sufficiently complete review data are available. Identify changes in rating distribution, recurring complaints, and feedback associated with specific products. Separate verified historical changes from conclusions that cannot be supported by the available records. If complete historical snapshots are unavailable, explain that limitation rather than assuming the current review list represents the full history. Recommend follow-up investigations for products showing meaningful negative patterns.

## Audit Review Visibility Decisions

Review hidden and published review records where available to support consistent, policy-based moderation.

- Apps: Judge.me
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_GET_REVIEW`, `JUDGEME_SET_REVIEW_VISIBILITY`

> Help me audit review moderation decisions using the available Judge.me review records and visibility controls. Identify reviews that may warrant investigation under my documented moderation policy, such as suspected spam, irrelevant content, or content that may violate applicable rules. Do not flag a review for removal solely because it is negative, criticizes a product, or gives a low rating. For each candidate, show the review details, the potential policy concern, and the recommended next step. Do not change visibility automatically. Ask me to approve each specific moderation action and preserve a clear rationale for the decision.

## Compare Ratings Across Products

Compare product ratings and review volumes to discover customer satisfaction differences across the catalog.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_PRODUCT_RATING_SUMMARY`, `JUDGEME_COUNT_REVIEWS`, `JUDGEME_GET_PRODUCT`

> Compare Judge.me ratings and review counts across my Shopify product catalog. Identify the highest-rated and lowest-rated products, products with substantial review volume, and products whose ratings may be unreliable because of small samples. Where useful, retrieve reviews to explain differences in customer feedback. Present the findings in a table with product name, rating, review count, key supported feedback themes, and recommended action. Avoid comparing ratings as if every product has an equivalent customer base or review volume. Explain missing data and do not invent ratings or review counts.

## Create a Weekly Review Insights Report

Prepare a recurring review report highlighting satisfaction trends, unresolved complaints, and product improvement priorities.

- Apps: Judge.me, Shopify
- Tools: `JUDGEME_LIST_REVIEWS`, `JUDGEME_COUNT_REVIEWS`, `JUDGEME_PRODUCT_RATING_SUMMARY`

> Prepare a weekly customer review report using my available Judge.me reviews, review counts, and product rating summaries. Include the number of reviews analyzed, rating distribution, notable positive feedback, recurring complaints, lowest-rated products, highest-rated products, and reviews that may need responses. Compare with the previous week only if comparable historical data is available. Identify three prioritized actions for product quality, customer support, or merchandising. Include supporting review examples and clearly state data limitations. Do not claim that a trend has changed without a valid comparison, and do not publish replies or modify review visibility without my approval.
