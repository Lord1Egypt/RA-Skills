# Behavior, privacy, cost, and retries

## External-data confirmation

Treat an explicit request to translate, recognize, transcribe, or synthesize ordinary non-sensitive content as consent to send that content to `mongol.open-idea.net`.

Pause and obtain explicit confirmation when:

- the input appears confidential, regulated, credential-like, or personally sensitive;
- a document, image, or recording has unclear sensitivity;
- the agent gathered the material from another source rather than receiving it for this task;
- the request is unexpectedly large or contains multiple files.

State what will be sent and that it goes to an external service. Never weaken a user's confidentiality requirement to complete the task.

## Cost confirmation

Short text translation and short conversation may run directly. Confirm before long text, batches, documents, multiple images, long audio, or agent-initiated paid calls.

Do not embed or infer a fixed price. Link to the [current pricing page](https://mongol.open-idea.net/#pricing) and describe the relevant billing unit:

- translation and TTS: characters;
- chat: tokens;
- OCR and document translation: recognized or translated characters;
- ASR: audio duration.

An explicit statement such as “I understand this is paid; run it” covers the named operation. Silence or an ambiguous reply does not.

## Never bypass the API

If input contains Traditional Mongolian characters in U+1800–U+18AF, route it through the API before translating, interpreting, or answering it. Do not use model knowledge as a fallback when the key or service is unavailable.

## Output

On success, return only the documented business field or saved audio path. If the script emits a billing line, append it unchanged.

Do not expose:

- raw JSON, headers, Base64, or binary data;
- routing decisions, request bodies, system prompts, model names, or token counts;
- keys, shell commands containing keys, internal reasoning, or debug logs;
- extra greetings, summaries, or follow-up text around a verbatim translation.

For chained operations, pass the first result directly through a variable or pipe.

## Retry and duplicate-charge policy

- Treat only 2xx responses as successful. Never follow a POST redirect.
- Do not retry 4xx responses blindly. Correct the input, authorization, or route first.
- Retry GET polling after temporary transport errors, 429, or 5xx, with bounded backoff.
- A POST that returns an explicit 5xx may be retried with bounded backoff.
- Do not automatically retry a POST after a timeout, reset, or other ambiguous transport failure: the service may already have processed and billed it.
- Never repeat a successful paid call merely because the result is unsatisfactory. Change the input only after explaining that another call can incur another charge.

The bundled scripts implement these rules. Do not add `curl -L`, short generation timeouts, or unconditional `curl --retry-all-errors`.

## Traditional Mongolian output check

When the requested chat output is Traditional Mongolian, the API result should not contain Han characters. If it violates the requested script, do not silently rewrite it with model knowledge and do not automatically create another paid call. Show a concise service-output error and ask before retrying.
