---
name: Payment Received
type: notification
channel: whatsapp
priority: high
---
Hi {{recipient_name}}! 💰

Payment received - thank you!

{{#if amount}}Amount: ${{amount}}{{/if}}
{{#if invoice_id}}Invoice: {{invoice_id}}{{/if}}
{{#if service}}Service: {{service}}{{/if}}

{{#if delivery_date}}Your order will be delivered by {{delivery_date}}.{{/if}}

Reply STOP to unsubscribe.
