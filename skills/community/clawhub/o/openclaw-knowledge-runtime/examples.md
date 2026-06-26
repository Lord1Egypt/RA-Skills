# Examples

## Example 1: Retrieval For A New Run

Goal:
Select the most relevant knowledge before ranking tasks or building prompts.

Suggested flow:

```text
role/objective/signals
  -> query_builder
  -> retrieval_selector
  -> typed_link_expansion
  -> compact output bundle
```

Expected output shape:

```json
{
  "knowledge_hits": [
    {
      "knowledge_id": "knowledge_semantic_repo-memory",
      "title": "Agent memory retrieval patterns",
      "score": 0.91,
      "reason": "High overlap with current objective and linked topic"
    }
  ],
  "knowledge_bias_tags": ["memory", "retrieval", "agent-runtime"],
  "linked_entities": [
    {
      "entity_type": "topic",
      "name": "Agent Memory"
    }
  ],
  "linked_genes": [],
  "memory_layers": ["semantic", "procedural"],
  "knowledge_context_preview": "Use layered retrieval and typed links before prompt assembly."
}
```

## Example 2: Task Ranking With Knowledge Relevance

Goal:
Use selected knowledge to influence which task or action gets priority.

Suggested approach:

1. Tokenize task title, summary, tags, and metadata.
2. Compare them with `knowledge_bias_tags`.
3. Reward overlap with `linked_entities` and `linked_genes`.
4. Save a short explanation such as `matched prior memory pattern` or `overlaps with linked entity`.

Good scoring signal:

- task overlaps with the same repo, topic, or failure pattern as selected knowledge

Bad scoring signal:

- task only shares generic words such as `fix`, `update`, or `improve`

## Example 3: Prompt Context Injection

Goal:
Inject only the smallest useful knowledge block into a prompt.

Good prompt context:

```text
Knowledge:
- Prior finding: retrieval quality drops when entity extraction is noisy.
- Linked topic: Agent Memory
- Linked asset: memory-reviewer
- Current bias tags: memory, retrieval, typed-links
```

Bad prompt context:

```text
Knowledge:
- full JSON event dump
- raw logs
- unfiltered URLs
- duplicated notes from prior runs
```

## Example 4: Stable Write-Back

Goal:
Record durable findings after a successful run without polluting the store.

Write back:

- validated findings with evidence
- repeated failure or success patterns
- summaries that can help future retrieval

Do not write back:

- scratch notes
- speculative guesses
- transient debugging output
- prompt dumps
