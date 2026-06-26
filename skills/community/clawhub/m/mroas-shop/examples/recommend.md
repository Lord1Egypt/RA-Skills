# Example · Recommend by intent

## User
> 我侄子下周三岁生日，帮我挑个礼物吧，预算 $30 以内。

## Agent action
```bash
CONTEXT='{"region":"US","budget_range":{"max":30,"currency":"USD"},"recipient":{"relationship":"nephew","age_band":"3"},"occasion":"birthday","positive_preferences":["safe toy","giftable"],"privacy_scope":"ephemeral"}'

curl -G 'https://selltoai.ai/v1/recommend' \
  -H 'X-Moras-Skill: moras-shop' \
  --data-urlencode 'intent=birthday gift for 3-year-old kid under $30' \
  --data-urlencode "personal_agent_context=$CONTEXT" \
  --data-urlencode 'limit=3' \
  --data-urlencode 'channel=openclaw' \
  --data-urlencode 'format=openclaw'
```

## Response / agent reply

OpenClaw should render `cards[]` as 3 product cards:

- image, title, price, and discount
- one-line pitch
- "Why this pick" reason bullets and Moras score
- `personalization_trace` explaining which local preferences were used
- `understanding_trace` confirming consumer, creator, and commerce-agent fit
- top creator/video proof
- Buy and More Videos actions

If Canvas/A2UI is available, push `a2ui.jsonl`. Only use
`fallback_markdown` if no structured card surface is available. Do not print raw
trace JSON to the shopper.
