---
name: lark-openclaw-bridge
description: Personal memo assistant, triggered when the user message starts with `/private-secretary` or `/ps`. Features: 1. Automatically classifies and appends user input to the corresponding Markdown file in `~/.memo`. 2. Automatically re-classifies and reorganizes all memos under `~/.memo` when the input is "rearrange"
---
# Private Secretary

Analyzes input content, automatically identifies classification labels (e.g., Tech, Work, Life, Inspiration), and appends it to the corresponding Markdown file in the `~/.memo/` directory.

## Parameters

- `content`: (required) The raw text content that needs to be classified and recorded.

## Instructions

1. **Analyze and Classify**: Read the `content` provided by the user. Based on the semantic meaning, classify it into one of the following: [Tech, Work, Life, Inspiration, Others].
2. **Extract Tags**: If the content involves Kubernetes, Java, programming, etc., be sure to label it as "Tech".
3. **Format Output**: Prepare a Markdown entry including a timestamp, classification label, and the original content.
4. **Execute Write**: Use the `exec` tool to run shell commands and append the content to `~/.memo/{category}.md`. Please use English for filenames.

## Exec Command

```bash
# Ensure directory exists
mkdir -p ~/.memo

# Generate ISO 8601 timestamp (Local Time)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Write to file (Variables populated by Agent)
# {{category}} will be the English label identified (e.g., Tech, Work)
printf "\n---\n### Timestamp: $TIMESTAMP\nLabel: {{category}}\n\n{{content}}\n" >> ~/.memo/{{category}}.md
