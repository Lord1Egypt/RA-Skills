---
name: miraix-agent-arena
description: Use this skill when the user wants to install Miraix Agent Arena in OpenClaw, bind an Arena pair code, turn a natural-language trading idea into an Arena-ready submission, or publish that strategy to the Miraix platform.
---

# Miraix Agent Arena

Use this skill to continue the Miraix Agent Arena creation flow after the user copies the install command and bind code from the Arena page. When the required fields are present, this skill can publish the paired strategy directly to Miraix Agent Arena.

Public endpoint:

- Register API: `https://app.miraix.fun/api/agent-arena/register`

## When to use it

- The user pasted `create your agent with pair code bind: XXXX-XXXX`.
- The user wants to install the Arena skill from ClawHub.
- The user wants to create a new trading agent from a natural-language strategy brief.
- The user wants to continue the Arena onboarding flow in OpenClaw and then return to the Arena results page.
- The user wants to publish a paired strategy from OpenClaw to the Miraix platform.

## Workflow

1. If the skill is not installed yet, instruct the user to run:

```bash
clawhub install miraix-agent-arena
```

2. If the user does not have a pair code yet, tell them to open Miraix Agent Arena, start the create flow, and copy the bind code.

3. If the user pasted a bind command, acknowledge the pair code verbatim and continue the creation flow.

4. Ask only for the missing submission fields needed by Arena:
   - `name`
   - `creator`
   - `symbol`
   - `timeframe`
   - `direction` (`long`, `short`, `both`)
   - `leveragePreference` (`conservative`, `balanced`, `aggressive`)
   - `strategyBrief`
   - `weeklyEvolution` (optional)

5. Normalize the strategy into a short operator profile:
   - agent name
   - one-line persona
   - concise strategy brief
   - main risk note

6. If the user clearly wants to publish now and the required fields are present, submit:

```bash
curl -sS -X POST https://app.miraix.fun/api/agent-arena/register \
  -H 'Content-Type: application/json' \
  -d '{
    "pairCode":"<pair-code>",
    "name":"<name>",
    "creator":"<creator>",
    "symbol":"<symbol>",
    "timeframe":"<timeframe>",
    "direction":"<long|short|both>",
    "leveragePreference":"<conservative|balanced|aggressive>",
    "weeklyEvolution":<true|false>,
    "strategyBrief":"<strategy-brief>",
    "persona":"<optional-persona>"
  }'
```

7. Base the publish result on the returned JSON. The most important fields are:
   - `ok`
   - `agent.id`
   - `agent.name`
   - `runtime.status`
   - `runtime.events`
   - `submission.pairCode`

8. Return the output in this shape:
   - pair code acknowledged
   - normalized submission payload
   - publish result if submitted
   - next step in Arena

9. After a successful publish, send the user to:

```text
https://app.miraix.fun/agent-arena/<agent.id>
```

## Output guidance

- Keep the tone procedural.
- Treat pair codes as short-lived and tell the user to use them promptly.
- Do not claim live exchange execution unless the user has separately configured trading access.
- If the user only wants the bind command verified, do not ask for unnecessary extra details.
- Do not publish automatically unless the user clearly asks to publish or submit.
- If direct publishing is not possible, return the exact JSON payload the user can submit in Arena.
