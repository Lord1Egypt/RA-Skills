---
name: Broadcast
type: broadcast
channel: telegram
priority: low
parse_mode: Markdown
---
📢 <b>{{sender_name}}</b>

{{message}}

{{#if cta_url}}👉 [Learn More]({{cta_url}}){{/if}}

/unsubscribe to opt out.
