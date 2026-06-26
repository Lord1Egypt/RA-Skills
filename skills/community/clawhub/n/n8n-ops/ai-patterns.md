# n8n AI Workflow Patterns

## Pattern 1: Simple LLM Call (No Agent)

Use when: Single prompt -> single response, no tool calling.

```
[Trigger] -> [Basic LLM Chain] -> [Next Step]
                   |
         [OpenAI Chat Model] (ai_languageModel)
         [Output Parser]     (ai_outputParser) [optional]
```

## Pattern 2: AI Agent with Tools

Use when: LLM needs to decide which tools to call, iterate.

```
[Trigger] -> [AI Agent] -> [Response]
                |
    [LLM Model]      (ai_languageModel)
    [Memory]          (ai_memory)
    [Tool 1]          (ai_tool index 0)
    [Tool 2]          (ai_tool index 1)
```

Agent types: `toolsAgent`, `conversationalAgent`, `openAiFunctionsAgent`, `reActAgent`

## Pattern 3: RAG Document Ingestion

```
[Trigger] -> [Fetch Docs] -> [Document Loader] -> [Vector Store (insert)]
                                   |                      |
                         [Text Splitter]          [Embeddings Model]
                         (ai_textSplitter)        (ai_embedding)
```

## Pattern 4: RAG Query/Retrieval

```
[Trigger] -> [Retrieval QA Chain] -> [Response]
                    |
      [LLM Model]           (ai_languageModel)
      [Vector Store]         (ai_vectorStore)
            |
      [Embeddings]           (ai_embedding)
```

## Pattern 5: Webhook Chat -> AI Agent -> Respond

```json
{
  "connections": {
    "Webhook": {
      "main": [[{"node": "AI Agent", "type": "main", "index": 0}]]
    },
    "OpenAI Chat Model": {
      "ai_languageModel": [[{"node": "AI Agent", "type": "ai_languageModel", "index": 0}]]
    },
    "Simple Memory": {
      "ai_memory": [[{"node": "AI Agent", "type": "ai_memory", "index": 0}]]
    },
    "Calculator": {
      "ai_tool": [[{"node": "AI Agent", "type": "ai_tool", "index": 0}]]
    },
    "Wikipedia": {
      "ai_tool": [[{"node": "AI Agent", "type": "ai_tool", "index": 1}]]
    },
    "AI Agent": {
      "main": [[{"node": "Respond to Webhook", "type": "main", "index": 0}]]
    }
  }
}
```

## Anti-Patterns

- NEVER chain LLM nodes via `main` — use `ai_languageModel`
- NEVER use Agent for simple prompts — use Basic LLM Chain
- NEVER forget memory session keys — always pass sessionId
- NEVER use Function node — use Code node (Function is deprecated)
- NEVER put long prompts directly in parameters — use Set node first

## Output Data Reference

| Node | Output field |
|------|-------------|
| Basic LLM Chain | `$json.text` |
| AI Agent | `$json.output` |
| Summarization Chain | `$json.response.text` |
| Retrieval QA Chain | `$json.response.text` |
| Structured Output Parser | `$json.fieldName` (per schema) |
