---
name: System Alert
type: alert
channel: telegram
priority: high
parse_mode: HTML
---
🔴 <b>SYSTEM ALERT</b>

<b>{{subject}}</b>

{{message}}

{{#if action_required}}<b>Action Required:</b> {{action_required}}{{/if}}

{{#if timestamp}}Occurred: {{timestamp}}{{/if}}
