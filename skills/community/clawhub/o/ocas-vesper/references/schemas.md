# Vesper Schemas

## Briefing
```json
{"briefing_id":"string","type":"string — morning|evening|manual","timestamp":"string","location":"string","sections":["BriefingSection"],"delivery_status":"string"}
```

## BriefingSection
```json
{"section_type":"string — today|messages|logistics|markets|decisions|system","section_marker":"string — ▪|✉|⚑|◈|⟡|⚙","content_items":["ContentItem"]}
```

## ContentItem
```json
{"item_id":"string","source_skill":"string","summary":"string","inline_links":[{"text":"string","uri":"string","uri_type":"string — gcal|maps|gmail|status"}],"decision_request":"DecisionRequest|null"}
```

## DecisionRequest
```json
{"decision_id":"string","option":"string","benefit":"string","cost":"string|null","status":"string — pending|accepted|ignored|expired"}
```

## SignalEvaluation
```json
{"signal_id":"string","source":"string","relevance_score":"number","included":"boolean","exclusion_reason":"string|null"}
```

## VesperBriefingFile
Written to `briefings/YYYY-WXX/YYYY-MM-DD-{type}.json` after every briefing generation. Read by Dispatch for delivery.
```json
{"briefing_id":"string","type":"string — morning|evening|manual","date":"string — YYYY-MM-DD","week":"string — YYYY-WXX","generated_at":"string","content":"string — rendered briefing text","sections":["BriefingSection"]}
```
