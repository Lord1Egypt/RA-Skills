#!/usr/bin/env python3
import argparse
from pathlib import Path

TEMPLATES = {
    "basic": """# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Basic Promptfoo evaluation

prompts:
  - 'Answer the question: {{question}}'

providers:
  - openai:gpt-5.2
  - openai:gpt-5-mini

tests:
  - vars:
      question: 'What is the refund policy?'
    assert:
      - type: llm-rubric
        value: answers clearly and does not invent policy details
""",
    "compare": """# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Compare providers on a shared task

prompts:
  - 'Solve this task: {{input}}'

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
      input: 'Summarize the incident in one sentence.'
    assert:
      - type: llm-rubric
        value: summary is concise and captures the key issue
""",
    "rag": """# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Evaluate RAG responses using multiple quality metrics

prompts:
  - |
    Use the provided context to answer the query.
    Query: {{query}}
    Context: {{context}}

providers:
  - openai:gpt-4.1-mini

tests:
  - vars:
      query: 'What is the refund window?'
      context: file://docs/policy.md
    assert:
      - type: factuality
        value: refunds are available within 30 days
      - type: answer-relevance
        threshold: 0.9
      - type: context-faithfulness
        threshold: 0.9
""",
    "agent": """# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
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
  - description: Basic agent task
    vars:
      query: 'What tools are available to me?'
    assert:
      - type: llm-rubric
        value: response explains available tools clearly
""",
    "redteam": """purpose: 'Customer-facing assistant. Users should get help with their own requests but must not access restricted or other users\' private information.'

targets:
  - id: https
    label: app-under-test
    config:
      url: 'https://example.com/api/chat'
      method: POST
      headers:
        Content-Type: application/json
      body:
        message: '{{prompt}}'
""",
}


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Promptfoo config using repo-aligned templates.")
    parser.add_argument("mode", choices=sorted(TEMPLATES.keys()), help="Template type to generate")
    parser.add_argument("--output", default="promptfooconfig.yaml", help="Output file path")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it exists")
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output} (use --force)")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(TEMPLATES[args.mode].rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {output} using '{args.mode}' template")


if __name__ == "__main__":
    main()
