# Memory Architecture Reference

Detailed comparison of agent memory architectures based on 2026 research survey.

## CMA vs RAG vs Temporal KG

### Benchmark Evidence

From arXiv:2603.07670 (CMA survey) and arXiv:2601.09913 (RAG comparison):

| Architecture | LongMemEval Score | Latency | Infrastructure |
|---|---|---|---|
| CMA (flat files) | Baseline | Low | None |
| Semantic RAG | +12-15% recall | Medium | Embedder |
| Temporal KG (Zep) | +18.5% | High (ingestion) | Neo4j + LLM |

**Key finding**: Temporal KG wins on long-horizon recall but requires async ingestion. CMA wins on simplicity and zero-infra.

### Mem0 vs Zep/Graphiti

From arXiv:2504.19413 (Mem0) and arXiv:2501.13956 (Zep):

**Mem0** (breadth-first):
- 91% latency reduction vs naive
- 90% token cost reduction
- User-level memory profiles
- OpenAI-compatible API

**Zep/Graphiti** (temporal KG-native):
- `valid_at`/`invalid_at` on every fact edge
- Entity deduplication across episodes
- Handles "what was true at time T?" correctly
- Requires Neo4j; ingestion is LLM-heavy

**When to choose Zep**: agents with months of state where fact supersession matters (e.g., "what's the current config?" may have changed many times).

**When to choose Mem0**: agents that need fast, breadth-first recall across many user/session profiles.

## OpenClaw-Specific Integration Notes

### OpenClaw /v1 Endpoint

OpenClaw exposes an OpenAI-compatible API at `http://127.0.0.1:<port>/v1`:
- `/v1/chat/completions` — LLM inference
- `/v1/embeddings` — embedding (768-dim, model name: `"openclaw"`)
- Auth: `Authorization: Bearer $OPENCLAW_GATEWAY_TOKEN`

This endpoint can back Graphiti, Mem0, and other libraries expecting OpenAI-compatible APIs.

### Graphiti + OpenClaw: Required Patches

Claude via Bedrock ignores `response_format: json_object`. Graphiti depends on structured JSON responses. Required fixes:

```python
class OpenClawLLMClient(OpenAIGenericClient):
    """Subclass that injects JSON schema into prompts since Bedrock ignores response_format."""

    async def _generate_response(self, messages, response_model=None,
                                  max_tokens=None, model_size=None, **kwargs):
        openai_messages = []
        for m in messages:
            m.content = self._clean_input(m.content)
            if m.role == 'user':
                openai_messages.append({'role': 'user', 'content': m.content})
            elif m.role == 'system':
                extra = '\n\nCRITICAL: Respond with ONLY valid raw JSON. No markdown, no fences. Start with {'
                if response_model is not None:
                    schema = response_model.model_json_schema()
                    import json
                    extra += f'\n\nJSON must match schema:\n{json.dumps(schema, indent=2)}'
                openai_messages.append({'role': 'system', 'content': m.content + extra})

        import re, json
        def strip_fences(text):
            match = re.match(r'^```(?:json)?\s*\n?(.*?)\n?```\s*$', text.strip(), re.DOTALL)
            return match.group(1).strip() if match else text.strip()

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={'type': 'json_object'},
            )
            raw = response.choices[0].message.content or ''
            return json.loads(strip_fences(raw))
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f'LLM error: {e}')
```

Also set `embedding_model="openclaw"` in `OpenAIEmbedderConfig`.

## Compression Architecture

### How OpenClaw Compacts Context

lossless-claw (LCM) creates a DAG of summaries from session history. When context pressure rises:
1. Oldest leaf messages are summarized into `sum_xxx` nodes
2. Summaries are stored and recalled via `lcm_grep` / `lcm_expand_query`
3. Detail is preserved in summary DAG, not raw transcript

**Implication**: Facts in raw messages are safe long-term via LCM. Facts in memory FILES are safer (not subject to LCM compression). Write important facts to memory files.

### Healthy Compression Posture

1. Memory files for durable facts (not just transcripts)
2. Short HEARTBEAT.md (< 40 lines) — long heartbeats get truncated
3. Timestamps on all facts in memory
4. Use `lcm_expand_query` to recover compacted history before answering questions about past work
5. Prefer `memory_search` over `read` for memory files (token-efficient)
