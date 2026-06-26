---
description: Slash-command entry point to tidy a workflow template's node positions. Invoke as /n8n-evol-I:tidyup with a workflow key; delegates to tidy-workflow.md for full option details.
---

# tidyup

Apply the canvas-layout algorithm to a workflow template. Runs the `@n8n/workflow-sdk` dagre layouter (auto-installed on first use); falls back to pure-Python BFS if Node is unavailable. Sticky notes are never moved.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/tidy_workflow.py --workspace <ws> --workflow-key <key> --in-place
```

See full options, side effects, idempotence, and auto-tidy hook details in [`skills/tidy-workflow.md`](tidy-workflow.md).
