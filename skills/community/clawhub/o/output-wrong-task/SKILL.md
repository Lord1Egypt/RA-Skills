---
name: output-wrong-task
description: The model produces correct-looking output that addresses a different task than the one requested — typically a related but distinct interpretation of an ambiguous prompt.
emoji: 🎯
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# output-wrong-task

The output is well-formed and internally coherent but answers the wrong question. The model resolved an ambiguous prompt toward the most common interpretation rather than the one the user intended, or it latched onto a salient keyword and addressed that instead of the full request. The result can look convincing enough to pass a quick read.

## Symptoms

- The deliverable matches the topic of the request but misses its purpose — e.g., "explain this function" gets documentation instead of the debugging analysis asked for.
- A code task produces something runnable but solving a simpler or adjacent problem than specified.
- The model answers the first clause of a multi-part question and silently drops the rest.
- The output would be correct for a different, more common prompt that shares keywords with this one.
- Asking the model to verify what it just did reveals that it believed it was solving a different problem.

## What to do

- Restate the concrete deliverable, not just the topic. Instead of "help me with authentication," say "write a middleware function that checks for a valid JWT in the Authorization header and returns 401 if missing or invalid — nothing else."
- Break compound tasks apart. If the prompt has multiple independent requirements, submit them one at a time and verify each before continuing.
- Anchor the output format explicitly. Specifying the expected structure (function signature, JSON schema, number of steps, file to modify) gives the model less room to substitute a related but wrong output.
- Before accepting the output, map it back to the original requirement: does this output satisfy the stated goal, not just a plausible-sounding version of it?
- If the wrong-task output keeps recurring on the same prompt, the prompt likely has a latent ambiguity. Identify which interpretation the model chose and add a clause that explicitly rules it out.
