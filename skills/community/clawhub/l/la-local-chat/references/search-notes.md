# Search Notes

## Current product direction
Search is the best candidate for AI-assisted improvement.

## Recommended pattern
1. Detect search intent.
2. Parse criteria.
3. Retrieve real candidates from source data.
4. Rank or rerank.
5. Return up to 5 strong matches.
6. Allow follow-up for technical sheet detail.

## Search rules
- Never invent locations.
- Weight location strongly when the query implies zone/city/sector.
- Use name, location, description, and architecture as meaningful signals.
- Avoid padding results with weak filler matches.
- Improve incrementally from real team queries.

## Open search questions
- Which real prompts recur most often?
- Which fields are most reliable for weighting?
- Should search stay on direct retrieval first or move toward an index layer later?
