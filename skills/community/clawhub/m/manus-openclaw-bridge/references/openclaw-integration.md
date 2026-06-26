# OpenClaw integration

## Direct-message trigger pattern

Use the Manus bridge when the user clearly intends to hand work to Manus, for example:
- `Manus, generate an image of a beach sunset`
- `manus: research AI hardware`

Flow:
1. Strip the Manus prefix.
2. Submit the cleaned prompt with `scripts/manus_prompt.sh`.
3. Parse the returned task id.
4. Wait and collect with `scripts/manus_wait_and_collect.py`.
5. Return text/files to the current conversation.

## Group trigger pattern

Use a stricter rule in groups:
- require an @mention
- require the message to start with `Manus,` or `manus:`

This prevents accidental Manus invocations during normal conversation.

## Suggested execution pattern

### Submit

```bash
scripts/manus_prompt.sh 'Manus, generate an image of a rainy forest'
```

### Wait and collect

```bash
python3 scripts/manus_wait_and_collect.py <task_id> 900
```

### Optional slides conversion

```bash
node scripts/manus_slides_json_to_pptx.mjs <slides.json> <output.pptx>
```

## Parsing expectations

The submit response should usually contain a task id. If the response shape differs by Manus version:
- inspect the raw JSON
- extract the stable task identifier
- keep that parsing in the OpenClaw-side glue code, not in user-facing chat logic

## Result policy

- image request -> return image file(s)
- report/slide request -> return file + short summary
- still running -> acknowledge + continue bounded polling
- error -> include the real Manus error/status if available
