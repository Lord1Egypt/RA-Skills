# Look — Core Workflow

## Procedure

- [ ] 1. Ingest image(s) with EXIF if available
- [ ] 2. Merge extraction evidence (OCR, entities, context)
- [ ] 3. Infer context and likely intent
- [ ] 4. Route to appropriate domain
- [ ] 5. Research and validate externally
- [ ] 6. Filter by constraints (dietary, preferences, permissions)
- [ ] 7. Reduce options before asking questions
- [ ] 8. Generate 1–3 decision-ready ActionDrafts
- [ ] 9. Emit Signal files for extracted entities (places, events, products). Signal schema: see `references/schemas.md`.
- [ ] 10. Write journal via `look.journal`

Clarification happens only after option reduction, not before.

## I/O Example

```
Input:  User provides /path/to/flyer.jpg (event flyer)
Output: ActionDraft {draft_type: "calendar_event", fields: {venue: "Greek Theater", date: "2026-08-15", time: "19:00"}}
        + DecisionRecord(type: "draft", summary: "Outdoor concert, Aug 15 7pm")

Input:  User provides meal photo (close-up plate)
        + context: vegetarian user
Output: ActionDraft {draft_type: "health_macros", fields: {protein: "15-22g", carbs: "45-60g", confidence: "medium"}}
```

## Validation Step

Before executing any action, verify:
1. All required fields in the ActionDraft are non-empty
2. Risk tier is correctly classified
3. User confirmation token exists (for high-risk)
4. External research results (if any) are documented in evidence_refs

If validation fails, list the missing fields to the user before attempting execution.

## Error Handling

| Failure | Detection | Response |
|---------|-----------|----------|
| Image unreadable / corrupt | `vision_analyze` returns error or empty | Report to user, request re-upload |
| Domain routing ambiguous | Low confidence across all domains | Present top 2 domain options, ask user |
| Reverse search returns empty | No results from Yandex or Google | Note "no external validation found" in draft, proceed with extracted data |
| Draft generation fails | Missing required fields (date, amount, etc.) | Mark draft as incomplete, list missing fields, ask user |
| Execution blocked (permissions) | Tool returns auth/permission error | Report blocked execution, save draft for manual action |
| API rate limit (Imgur, Yandex) | HTTP 429 or similar | Wait 30s, retry once. If still failing, report and continue without reverse search |
