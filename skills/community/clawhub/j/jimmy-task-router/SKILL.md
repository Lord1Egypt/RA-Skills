---
name: task-router
version: 1.0.0
description: Automatically route tasks to the appropriate tool, agent, or workflow. Analyzes task intent and complexity to route to coding, research, trading, system, or content workflows.
---

# AI Task Router

Automatically route tasks to the appropriate tool, agent, or workflow based on keywords and complexity analysis.

## Usage

```bash
bash scripts/route-task.sh "write a python script to sort a list"
bash scripts/route-task.sh "what is the weather in Valencia?"
bash scripts/route-task.sh "analyze this wallet: 0x81ac..."
```

## How It Works

1. Analyzes task description for intent and complexity
2. Matches against known patterns:
   - **coding**: code writing, refactoring, debugging
   - **research**: web search, data gathering, analysis  
   - **trading**: crypto ops, wallet checks, DeFi
   - **content**: writing, summarization, translation
   - **system**: file ops, cron, monitoring
   - **general**: conversation, Q&A

3. Returns routing decision with confidence score

## Configuration

Edit `scripts/config.sh` to add custom patterns or change routing logic.

## Integration

Can be used as a pre-processor for incoming tasks to route them to specialized agents or tools.
