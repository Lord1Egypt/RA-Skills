# LLM Review Layer

Use a hybrid approach:

1. Run heuristics first.
2. If heuristic confidence is high, trust the rule.
3. If heuristic confidence falls inside a configured ambiguity band, run a lightweight LLM review.
4. Log whether the final decision came from heuristics only or heuristics + LLM review.

## Recommended confidence band

Example:

- below `0.68`: too weak — prefer no action or conservative handling
- `0.68` to `0.86`: ambiguous band — send to LLM review
- above `0.86`: trust heuristics unless a custom safeguard says otherwise

## Suggested LLM task

Return strict JSON only:

```json
{
  "category": "opportunity",
  "actionable": true,
  "confidence": 0.81,
  "archive": false,
  "star": true,
  "important": false,
  "notify": true,
  "reason": "Short explanation"
}
```

## Use cases for LLM review

- person vs organization ambiguity
- press release vs press opportunity
- ordinary receipt vs billing issue
- action required in Portuguese/Spanish nuance
- multilingual business inquiries with weak keyword coverage

## Safety

Do not let the LLM create arbitrary new labels.
The LLM must choose from an allowlisted category set.
