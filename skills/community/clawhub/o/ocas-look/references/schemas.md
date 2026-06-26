# Look Schemas

## ImageEvidence
```json
{"image_id":"string","ingest_source":"string","exif":{"gps":"object|null","timezone":"string|null","capture_time":"string|null"},"device_preparse":"object|null","extracted_entities":{"dates":[],"times":[],"addresses":[],"phones":[],"urls":[],"place_names":[],"product_strings":[]}}
```

## ActionDraft
```json
{"draft_id":"string","draft_type":"string — calendar_hold|calendar_event|ticket_purchase|health_macros|maps_to_try|product_pricing|product_order|civic_report_311|expense_entry|drive_file_document","risk":"string — low|medium|high","confidence":"string","summary":"string","fields":"object","evidence_refs":["string"],"next_step":"string"}
```

## ExecutionReceipt
```json
{"execution_id":"string","draft_id":"string","status":"string — executed|rolled_back|failed","external_refs":"object|null","timestamp":"string"}
```

## DecisionRecord
Extends shared DecisionRecord. Look-specific types: ingest, context, route, research, reduce, draft, execute, rollback, safety.
