---
name: ping-echotest
description: A tiny smoke-test skill that echoes back any text you send it. Useful for verifying skill ingestion, publishing, and end-to-end load in a registry. Not for production use.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎯",
        "category": "testing",
        "tags": ["smoke-test", "echo", "regression"],
      },
  }
---

# ping-echotest

Takes any input text and returns the same text prefixed with `pong:`.
Designed as a deterministic, side-effect-free probe for tooling that
ingests skills from a registry.

## Usage

Invoke the skill and pass it a piece of text. It will reply with:

    pong: <your text>

## Example

Input: `hello resource-center`
Output: `pong: hello resource-center`

## Why it exists

- Deterministic output makes it perfect for CI/integration checks.
- No external network or credentials required.
- Safe to publish publicly; it carries no user data.
