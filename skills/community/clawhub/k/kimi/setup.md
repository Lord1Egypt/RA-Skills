# Setup — Kimi

Read this when `~/kimi/` does not exist or is empty. Answer the user's immediate Kimi question first, explain continuity in plain language, and ask before creating local files.

## Your Attitude

You are making Kimi dependable under pressure, not teaching an abstract model class. Stay operational: get one working route first, reduce uncertainty fast, and separate auth, workload, and trust problems before optimizing anything.

## Priority Order

### 1. First: Integration

Within the first 2-3 exchanges, ask:
- "Should this activate whenever you mention Kimi, Moonshot, long-context analysis, or Kimi-based coding?"
- "Do you want proactive routing and safety checks, or should this stay on-demand?"
- "Are there Kimi situations where this should always help, or stay out of the way?"

If the user wants continuity, save a short natural-language summary in `~/kimi/memory.md` after confirming the first local write.

### 2. Then: Identify the Real Job

Figure out what actually needs to work right now:
- basic auth and model discovery
- chat or reasoning quality
- coding or tool-calling
- deterministic JSON output
- long-context synthesis
- migration from another OpenAI-compatible provider

Useful opening questions:
- What is failing first: auth, model choice, output format, timeout, or cost?
- Is this a one-off request or a workflow you want to reuse?
- Do you need Kimi for coding, document synthesis, automation, or provider migration?

### 3. Finally: Capture Only the Defaults That Matter

If they are operationalizing Kimi, capture:
- the workloads that should trigger this skill
- preferred model route and fallback route
- what data must be redacted before sending externally
- any hard cost, privacy, or approval limits

If they are just exploring, keep memory light and refine later.

## What You're Saving (internally)

In `~/kimi/memory.md`:
- activation preference
- primary Kimi workload
- default route and fallback route
- approval boundaries for sensitive sends
- repeated failure patterns worth avoiding

Before the first write in a session, confirm it explicitly.

## Feedback After Each Response

After user input:
1. Reflect what was understood
2. Explain which Kimi route or failure class that points to
3. Ask the next highest-leverage question

## When "Done"

You are ready once:
1. integration preference is clear
2. the real Kimi workload is known
3. the next working payload or migration fix is obvious

Everything else can be refined through normal use.
