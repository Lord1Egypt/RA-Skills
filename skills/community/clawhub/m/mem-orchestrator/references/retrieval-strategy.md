# Retrieval Strategy

## Goal

Load the minimum useful memory needed to answer well.

## Retrieval Order

1. Domain and intent classification
2. Topic-card recall
3. Object-summary recall
4. Conditional detail expansion
5. Optional associative expansion

## Recall Budgets

Default budget:
- topics: 1-2
- object summaries: 3-5
- full detail reads: 1-2
- associative expansions: 0-2

These budgets are guardrails. Do not exceed them unless the user explicitly asks for deep historical analysis.

## Ranking Inputs

Use a weighted score combining:
- semantic similarity
- domain match
- recency
- relation proximity
- user preference match
- stability

Fallback if embeddings are unavailable:
- keyword overlap score
- explicit domain score
- tags overlap
- recency decay
- relation count bonus

## Expansion Rules

Expand full object details only when:
- the user asks for mechanism, evidence, implementation details, or chronology
- the current answer would otherwise be vague or risky
- multiple summaries conflict and need resolution

Do not expand details just because they exist.

## Associative Recall Rules

Use associative recall only when one of these holds:
- a strongly linked object clarifies the current answer
- the user is comparing alternatives
- the current topic naturally extends to a neighboring domain

Examples:
- research method discussion → related framework in technology
- investing risk question → prior user risk preference object
- career tradeoff → old decision object about autonomy vs stability

## Suppression Rules

Suppress recalled items when:
- they are stale and low-stability
- they are semantically weak matches
- they would distract from the current topic
- they duplicate stronger recalled items

## Output Shape

Return compact JSON from retrieval:

```json
{
  "query": "...",
  "intent": "compare",
  "domains": ["research"],
  "topics": [
    {"id": "research", "summary": "..."}
  ],
  "objects": [
    {"id": "paper/constitutional-ai", "summary": "...", "score": 0.84}
  ],
  "expanded": [
    {"id": "paper/constitutional-ai", "why": "needs mechanism detail"}
  ],
  "associations": []
}
```

Keep the payload small enough to insert into the answer-generation prompt without bloating context.
