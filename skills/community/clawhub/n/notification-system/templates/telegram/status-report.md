---
name: Status Report
type: report
channel: telegram
priority: normal
parse_mode: Markdown
---
📊 <b>Status Report</b>

{{title}}

{{#each metrics}}
• {{name}}: {{value}}
{{/each}}

{{#if cta_url}}[View Dashboard]({{cta_url}}){{/if}}
