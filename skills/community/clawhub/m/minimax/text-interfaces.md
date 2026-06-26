# Text Interfaces - MiniMax

Use this file when the task involves MiniMax text generation through raw HTTP, Anthropic-compatible SDKs, or OpenAI-compatible SDKs.

## Interface Choice

### Native MiniMax API
Use native MiniMax APIs when:
- the app is greenfield and you want the most direct behavior
- you need the clearest mapping between docs and payload
- you want to avoid SDK-compatibility ambiguity

### Anthropic-Compatible API
Use the Anthropic-compatible surface when:
- the application already uses the Anthropic SDK
- the supported MiniMax text model set is sufficient
- the team accepts that some Anthropic parameters are ignored

Current official caveats to remember:
- text support is currently limited to `MiniMax-M2.5`, `MiniMax-M2.5-highspeed`, `MiniMax-M2.1`, `MiniMax-M2.1-highspeed`, and `MiniMax-M2`
- `temperature` must stay in the documented `(0.0, 1.0]` range
- some Anthropic parameters are ignored, including `thinking`, `top_k`, `stop_sequences`, `service_tier`, `mcp_servers`, `context_management`, and `container`
- image and document inputs are not currently supported on that compatible surface

### OpenAI-Compatible API
Use the OpenAI-compatible surface when:
- the application is already wired around an OpenAI client
- the integration values lower migration cost over exact native semantics
- the current docs confirm the needed endpoint, payload, and model support

Treat official MiniMax docs as the source of truth for the exact base URL and supported OpenAI-compatible methods before shipping code.

## Decision Rule

Prefer this order:
1. Native MiniMax API for new builds or feature-complete control
2. Compatible interface only when the existing app architecture makes it worth the narrower surface
3. If the compatible interface starts hiding important behavior, switch back to native instead of stacking patches

## Payload Discipline

- Pin the exact text model in every request.
- Keep temperature conservative when the downstream step needs structured parsing.
- Record any compatible-interface caveat next to the integration code, not only in chat notes.
- When debugging, reduce the payload before changing models.

## Debug Sequence

When a MiniMax text call behaves strangely:
1. Confirm the chosen interface really supports the selected model.
2. Check whether a parameter is being ignored by the compatible layer.
3. Reproduce the issue with the smallest payload possible.
4. Only then escalate to prompt changes or model swaps.
