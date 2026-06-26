# Promptfoo config patterns

These patterns are aligned to Promptfoo's example repo style:

- include the schema header
- use top-level `description`
- prefer `vars` under `tests`
- use `defaultTest` for shared assertions
- use `file://...` when prompts, docs, tools, or agents live in files

Adapt the pattern to the repo. Do not invent a different abstraction unless the repo truly needs it.

## 1. Getting-started pattern

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Getting started

prompts:
  - 'Convert the following English text to {{language}}: {{input}}'

providers:
  - openai:gpt-5.2
  - openai:gpt-5-mini

tests:
  - vars:
      language: French
      input: Hello world
    assert:
      - type: contains
        value: 'Bonjour le monde'
  - vars:
      language: Spanish
      input: Where is the library?
    assert:
      - type: icontains
        value: 'Dónde está la biblioteca'
```

Use when building a basic side-by-side prompt/provider harness.

## 2. Self-grading pattern with file-backed prompts

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Automatic response evaluation using LLM rubric scoring

prompts:
  - file://prompts.txt

providers:
  - openai:chat:gpt-5.2

defaultTest:
  assert:
    - type: llm-rubric
      value: Do not mention that you are an AI or chat assistant
    - type: javascript
      value: Math.max(0, Math.min(1, 1 - (output.length - 100) / 900));

tests:
  - vars:
      name: Bob
      question: Can you help me find a specific product on your website?
```

Use when many tests share the same grading logic.

## 3. Provider comparison with operational guardrails

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Comparing provider performance on a shared task

prompts:
  - 'Solve this riddle: {{riddle}}'

providers:
  - openai:gpt-5.4
  - openai:gpt-5.3-chat-latest

defaultTest:
  assert:
    - type: cost
      threshold: 0.01
    - type: latency
      threshold: 10000

tests:
  - vars:
      riddle: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'
    assert:
      - type: contains
        value: echo
      - type: llm-rubric
        value: Do not apologize
```

Use when model choice depends on quality, latency, and cost together.

## 4. RAG eval pattern using context metrics

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Evaluating RAG responses using multiple quality metrics

prompts:
  - |
    You are an internal corporate chatbot.
    Respond to this query: {{query}}
    Here is some context that you can use to write your response: {{context}}

providers:
  - openai:gpt-4.1-mini

tests:
  - vars:
      query: What is the max purchase that doesn't require approval?
      context: file://docs/reimbursement.md
    assert:
      - type: contains
        value: '$500'
      - type: factuality
        value: the employee's manager is responsible for approvals
      - type: answer-relevance
        threshold: 0.9
      - type: context-recall
        threshold: 0.9
        value: max purchase price without approval is $500
      - type: context-relevance
        threshold: 0.9
      - type: context-faithfulness
        threshold: 0.9
```

Use when you need groundedness checks, not just output style checks.

## 5. Agent provider object pattern

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Evaluate a tool-using agent workflow

prompts:
  - '{{query}}'

providers:
  - id: openai:agents:my-agent
    config:
      agent: file://./agents/my-agent.ts
      tools: file://./tools/my-tools.ts
      maxTurns: 20

tests:
  - description: Requests inventory status
    vars:
      query: 'What tools do I have available?'
    assert:
      - type: contains-any
        value: ['inventory', 'tools']
```

Use when evaluating agent orchestration instead of a plain text prompt.

## 6. HTTP target for app-level evals

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Evaluate a live API-backed assistant

prompts:
  - '{{prompt}}'

targets:
  - id: https
    label: support-api
    config:
      url: 'https://example.com/api/chat'
      method: POST
      headers:
        Content-Type: application/json
      body:
        message: '{{prompt}}'

tests:
  - vars:
      prompt: 'What is your refund window?'
    assert:
      - type: contains
        value: '30'
```

Use when the real API path matters more than an isolated prompt template.

## 7. Red-team target skeleton

```yaml
purpose: 'Customer support assistant for an ecommerce platform. Users may ask about their own orders, but must not access other users\' personal or payment data.'

targets:
  - id: https
    label: ecommerce-support
    config:
      url: 'https://example.com/api/chat'
      method: POST
      headers:
        Content-Type: application/json
      body:
        message: '{{prompt}}'
```

Then add plugins and strategies via Promptfoo's setup flow or by refining the generated config.

## Pattern selection heuristics

Choose a pattern by the actual goal:

- basic eval harness → getting-started pattern
- shared grading logic → self-grading pattern
- provider decision → comparison with cost/latency guardrails
- groundedness → RAG pattern
- tool-using system → agent provider object pattern
- real app behavior → HTTP target pattern
- abuse resistance → red-team skeleton

## Anti-patterns

Avoid these:

- skipping the schema header in new configs
- using one huge rubric to judge everything
- only happy-path tests
- swapping prompts, providers, and datasets at the same time
- using synthetic tests only when production failure examples already exist
- treating red-team output as a one-off audit instead of a regression source
