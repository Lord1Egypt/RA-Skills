---
name: Appointment Confirmation
type: notification
channel: whatsapp
priority: high
---
Hi {{recipient_name}}! ✅

Your appointment is confirmed:

📅 Date: {{date}}
🕐 Time: {{time}}
📍 Location: {{location}}
{{#if service}}🔧 Service: {{service}}{{/if}}

We'll see you then! Reply STOP to unsubscribe.
