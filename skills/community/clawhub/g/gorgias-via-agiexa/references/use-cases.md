# Gorgias use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/gorgias

## Prioritize Urgent Customer Support Tickets

Review open support tickets, identify time-sensitive customer issues, and prepare a prioritized queue for the support team.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_GET_TICKET`

> Review my open Gorgias tickets and categorize them by issue type, urgency, ticket age, and available customer or order context. Identify delayed deliveries, refund requests, damaged products, payment concerns, and other cases that may need prompt attention. Use available Shopify order and fulfillment information where relevant. Explain why each ticket deserves its proposed priority, and distinguish verified facts from assumptions. Recommend the next action and responsible team for each case. Do not delete tickets, send replies, or change assignments without approval. Present a prioritized table and a concise support action plan.

## Resolve Shopify Order Support Requests

Combine support conversations with Shopify order details to prepare accurate responses to common order-related questions.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_GET_TICKET_MESSAGE`, `GORGIAS_SEND_TICKET_MESSAGE`

> Review Gorgias tickets related to Shopify orders. For each relevant ticket, identify the customer concern and retrieve the corresponding order details where the connected store data is available. Check order status, fulfillment information, available tracking details, and relevant product information. Prepare a customer-friendly reply that uses verified facts and avoids promising delivery dates, refunds, or other outcomes that have not been confirmed. Identify cases requiring human review. Do not send replies or modify orders unless I explicitly approve the action.

## Manage Returns and Refund Requests

Organize return and refund tickets, identify missing information, and prepare responses based on verified order details and store policies.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_ADD_TICKET_TAGS`

> Find Gorgias tickets related to returns, refunds, exchanges, and damaged products. Group them by request type and identify the order information, customer explanation, supporting evidence, and outstanding questions available in each case. Check relevant Shopify order details where accessible. Prepare a recommended next action and a customer reply for each ticket, distinguishing eligibility that has been verified from eligibility that still needs review. Apply appropriate existing tags only after approval. Do not issue refunds, promise replacements, or send external messages automatically.

## Automate Repetitive Support Responses

Create reusable response macros for frequent support questions while keeping customer-specific facts accurate.

- Apps: Gorgias
- Tools: `GORGIAS_LIST_MESSAGES`, `GORGIAS_CREATE_MACRO`

> Analyze recent Gorgias tickets and messages to identify repetitive customer questions, such as shipping delays, order status, return instructions, product availability, and address changes. Group similar cases and draft reusable response macros for the most common categories. Include placeholders for customer names, order numbers, verified status, and other variable information. Recommend any ticket tags or team actions associated with each macro. Review existing macros before proposing duplicates. Do not create or publish macros, send messages, or enable automatic customer communication until I approve the final content and actions.

## Classify Tickets With Consistent Tags

Standardize ticket categorization so support teams can filter, prioritize, and report on customer issues more effectively.

- Apps: Gorgias
- Tools: `GORGIAS_LIST_TAGS`, `GORGIAS_LIST_TICKET_TAGS`, `GORGIAS_SET_TICKET_TAGS`

> Review my existing Gorgias tags, teams, ticket fields, and open tickets. Identify inconsistent classifications, frequently used categories, and tickets that appear to lack useful tags. Propose a standardized tagging scheme for delivery issues, refunds, damaged products, product questions, order changes, and other recurring support topics. Reuse existing tags where appropriate and avoid creating duplicates. Prepare a mapping from each ticket category to its recommended tags and responsible team. Show proposed changes before applying them, and do not remove existing tags or overwrite ticket fields without approval.

## Identify Recurring Customer Complaints

Analyze support conversations to uncover repeated product, delivery, checkout, and service issues that may need operational improvements.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_LIST_MESSAGES`

> Analyze recent Gorgias tickets and messages to identify recurring customer complaints and support patterns. Group issues by category, affected product, order status, and available time period. Where Shopify data is available, compare complaints with product availability, fulfillment information, and relevant order details. Identify repeated delivery problems, product-quality concerns, confusing product information, and common return reasons where the evidence supports them. Rank the most important issues by frequency and customer impact. Recommend operational improvements and explain the evidence behind each recommendation. Do not assume that ticket volume alone proves a product or process is defective.

## Route Tickets to the Correct Team

Recommend ticket assignments based on the issue type, available teams, and the information required to resolve each case.

- Apps: Gorgias
- Tools: `GORGIAS_LIST_TEAMS`, `GORGIAS_LIST_USERS`, `GORGIAS_UPDATE_TICKET`

> Review my Gorgias teams, users, existing tags, and open tickets. Categorize tickets by the type of help required, such as shipping, returns, product questions, or order management. Recommend the most appropriate existing team for each ticket and explain any uncertain assignments. Identify tickets that need escalation or additional information before routing. Avoid creating duplicate teams or changing existing workspace configuration unnecessarily. Show the current classification and proposed assignment in a table. Do not reassign tickets, delete teams, or change permissions until I approve the proposed changes.

## Build Support Views and Workflow Rules

Organize support work into saved views and propose automation rules for repeatable ticket-handling processes.

- Apps: Gorgias
- Tools: `GORGIAS_LIST_VIEWS`, `GORGIAS_CREATE_VIEW`, `GORGIAS_LIST_RULES`, `GORGIAS_CREATE_RULE`

> Review my existing Gorgias views and automation rules. Identify opportunities to create useful saved views for urgent tickets, unresolved delivery issues, refund requests, damaged products, and tickets awaiting customer information. Propose rule conditions and actions that match the available workspace configuration. Use existing tags and teams where possible, and avoid overlapping rules that could cause conflicting actions. For each proposed workflow, explain its trigger, conditions, actions, and expected benefit. Do not create rules, change existing automation, or enable external message delivery until I approve the configuration.

## Improve Customer Support Efficiency

Summarize support workload, common issues, and opportunities to reduce repetitive manual work.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_LIST_EVENTS`, `GORGIAS_LIST_TAGS`

> Review available Gorgias ticket, message, tag, team, and event data for a specified period. Summarize ticket volume, issue categories, open-ticket backlog, repeated customer concerns, and team workload where the data supports these metrics. Identify frequent requests that could benefit from response macros, saved views, or consistent classification. Where Shopify order information is available, highlight recurring operational issues that appear connected to fulfillment, product availability, or order changes. Clearly state which performance metrics cannot be calculated from the available records. Recommend the five most useful support improvements and present the findings with metric cards, tables, and a prioritized action list.

## Create a Customer Support Operations Report

Produce a structured report combining ticket trends, unresolved cases, customer concerns, and recommended next actions.

- Apps: Gorgias, Shopify
- Tools: `GORGIAS_LIST_TICKETS`, `GORGIAS_LIST_MESSAGES`, `GORGIAS_LIST_VIEW_ITEMS`

> Prepare a customer support operations report using my available Gorgias tickets and messages for the selected period. Include ticket counts by category, open and unresolved cases, common customer questions, recurring complaints, and the tickets that need attention first. Summarize team and tag distribution where available. Use connected Shopify order information to contextualize delivery, refund, product, and fulfillment issues when reliable matching is possible. Highlight missing data and avoid inventing resolution times, satisfaction scores, or other unsupported metrics. End with three prioritized operational improvements and a list of cases requiring human review. Format the report using metric cards, compact tables, and concise recommendations.
