# Speech Workflows - MiniMax

Use this file when the user needs narration, TTS previews, voice tuning, or delivery-format decisions.

## Core Rule

Treat speech work as a delivery pipeline, not just a prompt.
The output quality depends on:
- model tier
- language and script quality
- input length and chunking
- output format
- latency target

## Recommended Routing

- `speech-2.8-hd` for final narration, demos, polished voice output, and higher-quality speech delivery
- `speech-2.8-turbo` for faster previews, QA loops, and rapid iteration
- use the standard API endpoint first, then the lower-TTFA `api-uw` path only when faster first audio matters and the user accepts that endpoint

## Workflow Order

1. Confirm the text is final enough to synthesize.
2. Confirm language, pronunciation sensitivity, and delivery style.
3. Choose HD or turbo based on quality versus latency.
4. Decide whether one request is enough or whether the script should be chunked.
5. Verify the output format and playback target before generating.

## Consent and Rights

- Do not imitate or clone a real person's voice unless the user has the right and explicit permission to do that.
- Treat uploaded reference audio as sensitive media.
- Keep the approved use case explicit in the task notes if the workflow could be misused.

## Common Failures

- sending draft text to TTS too early -> repeated spend on avoidable revisions
- ignoring punctuation and pronunciation constraints -> naturalness drops even when the voice model is fine
- synthesizing one giant script without chunk strategy -> retries and re-renders become expensive
- optimizing only for audio quality while ignoring turnaround time -> workflow becomes unusable in preview loops
