# Gmail use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/gmail

## Prioritize Important Store Emails

Identify customer inquiries, supplier issues, and order-related emails, then organize your inbox around the actions that matter most to your Shopify business.

- Apps: Gmail, Shopify
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`

> Act as my Shopify business email assistant. Review my recent Gmail messages and identify customer inquiries, supplier communications, order-related issues, and other important store emails. Group them by category and urgency. Summarize the sender, subject, key information, required action, and any relevant deadline. When an email refers to a Shopify order or product, retrieve the corresponding store information where possible. Identify emails that need replies and recommend which ones I should handle first. Do not send replies or delete emails without my approval.

## Answer Customer Emails Using Shopify Data

Prepare accurate, personalized email replies using current Shopify order, product, and inventory information.

- Apps: Gmail, Shopify
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_REPLY_TO_THREAD`, `GMAIL_SEND_EMAIL`

> Act as my Shopify customer support assistant. Review customer emails asking about orders, product prices, availability, or other store-related questions. Match each inquiry to the relevant Shopify order or product using reliable identifiers. Retrieve the necessary information and draft a concise, friendly email response. Use verified information only, and flag any missing details or ambiguous matches. Show me the complete draft before sending it. Never invent delivery dates, promise stock availability without checking, or send a customer email without my approval.

## Match Supplier Emails With Inventory Risks

Connect supplier delivery updates and backorder notifications with Shopify inventory to identify products at risk of running out of stock.

- Apps: Gmail, Shopify
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_CREATE_EMAIL_DRAFT`

> Act as my Shopify supplier and inventory assistant. Review recent supplier emails for shipment delays, backorders, stock shortages, dispatch updates, and revised delivery dates. Identify the products mentioned in those emails and match them to my Shopify catalog where possible. Check current inventory quantities and highlight products that are out of stock or running low. Summarize the supplier, affected products, current stock, expected delivery information, and recommended next action. Distinguish confirmed supplier information from assumptions. Draft supplier follow-up emails when needed, but do not send them without my approval or change inventory quantities based solely on an email.

## Organize Emails With Smart Labels

Automatically categorize business emails using Gmail labels and filtering rules so customer support, supplier communications, and order issues stay organized.

- Apps: Gmail
- Tools: `GMAIL_LIST_LABELS`, `GMAIL_CREATE_LABEL`, `GMAIL_CREATE_FILTER`

> Act as my Gmail inbox organizer for my Shopify business. Review my existing labels, filters, and recent emails. Recommend a clear labeling system for customer inquiries, suppliers, order issues, refunds, inventory, and urgent follow-ups. Identify messages that match each category and explain your proposed organization. Before creating labels, applying labels in bulk, or creating filters, show me the exact changes for approval. Ensure that filter criteria are specific enough to avoid incorrectly categorizing unrelated emails. Do not permanently delete messages or remove existing labels without my explicit confirmation.

## Manage Shopify Delivery Support Emails

Combine customer emails with Shopify orders and shipment tracking information to investigate delivery complaints and prepare informed responses.

- Apps: Gmail, Shopify, AfterShip
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`, `GMAIL_REPLY_TO_THREAD`

> Act as my Shopify delivery support assistant. Find customer emails reporting late deliveries, missing packages, or shipment problems. Match each email to the corresponding Shopify order and retrieve available fulfillment and tracking information. If AfterShip is connected, also retrieve the latest shipment checkpoints, delivery exceptions, and estimated delivery dates. Summarize what is confirmed, what remains unknown, and the recommended next step. Draft a personalized reply explaining the verified status and any necessary follow-up. Never invent tracking updates, promise unsupported delivery dates, or send the email without my approval.

## Handle Return and Refund Email Requests

Review return and refund requests from Gmail, investigate the associated Shopify order, and prepare appropriate responses using verified order information.

- Apps: Gmail, Shopify, AfterShip
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_REPLY_TO_THREAD`

> Act as my Shopify returns and refund assistant. Identify customer emails requesting returns, refunds, exchanges, or help with damaged or incorrect products. Retrieve the relevant Shopify order details and, if AfterShip returns are connected, check the associated return request, items, reasons, and available refund information. Summarize the customer's request, order status, existing return status, and recommended next step. Draft a professional response for my review. Never approve or reject a return, issue a refund, promise a refund amount, or send a customer email without the required verification and my explicit approval.

## Draft Supplier Follow-Ups Automatically

Prepare professional supplier emails about delayed shipments, missing stock, purchase-related questions, and outstanding delivery commitments.

- Apps: Gmail, Shopify
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_CREATE_EMAIL_DRAFT`

> Act as my Shopify supplier communication assistant. Review supplier emails and identify unresolved issues involving delayed shipments, backorders, stock availability, and missing delivery updates. Connect the affected products to my Shopify inventory where possible. Draft a professional follow-up that references the relevant supplier email, product, outstanding issue, and specific information needed from the supplier. Prioritize urgent cases where stock is depleted or customer orders may be affected. Create an email draft for my review rather than sending it automatically. Never invent supplier commitments, purchase order numbers, or delivery dates.

## Turn New Orders Into Email Workflows

Use incoming Gmail messages and Shopify order information to identify new order-related requests and prepare the appropriate follow-up actions.

- Apps: Gmail, Shopify
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_CREATE_EMAIL_DRAFT`

> Act as my Shopify order email assistant. When a new Gmail message arrives, determine whether it concerns a Shopify order, product inquiry, order change, cancellation request, or delivery issue. Retrieve the relevant Shopify order details when sufficient identifying information is available. Summarize the customer's request, the current order status, and the next action required. Draft an appropriate response for my approval. If an order modification or cancellation is requested, explain the implications and ask for confirmation before taking action. Do not assume that an email alone authorizes a financial or order-status change.

## Follow Up on Unanswered Customer Emails

Find customer conversations that may need a response and prepare follow-ups to help prevent important inquiries from being overlooked.

- Apps: Gmail, Shopify
- Tools: `GMAIL_LIST_THREADS`, `GMAIL_FETCH_MESSAGE_BY_THREAD_ID`

> Act as my Shopify customer follow-up assistant. Review recent Gmail threads involving customer inquiries and identify conversations that appear to require a response. Consider the latest message, existing replies, and available timestamps before deciding whether a conversation is unanswered. Where relevant, check Shopify order or product information to understand the customer's issue. Prepare a prioritized list with the customer, subject, last message date, outstanding question, and suggested response. Draft follow-up emails for my review. Do not send repetitive messages, assume a response is overdue without considering its context, or send follow-ups without my approval.

## Generate Daily Shopify Business Email Reports

Combine Gmail communications with Shopify order and inventory information to produce a daily report of customer issues, supplier risks, and outstanding business actions.

- Apps: Gmail, Shopify, AfterShip
- Tools: `GMAIL_FETCH_EMAILS`, `GMAIL_LIST_THREADS`

> Act as my daily Shopify business operations assistant. Review relevant Gmail messages for the specified period and summarize customer inquiries, supplier updates, order-related issues, return requests, and outstanding follow-ups. Connect messages to Shopify orders, products, inventory, and fulfillment information where possible. If AfterShip is connected, include relevant shipment exceptions and return information. Organize the report into urgent customer issues, inventory and supplier risks, delivery and return problems, and routine follow-ups. Include sender, subject, relevant identifiers, and recommended next steps. Distinguish verified information from assumptions and avoid double-counting messages from the same conversation. Do not send emails or modify store records as part of reporting.
