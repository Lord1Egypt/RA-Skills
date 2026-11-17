# OpenAI profile

## GPT-5.6 Sol and GPT-5.6 family

- Define the outcome, important constraints, available evidence, and completion bar; leave room for the model to choose an efficient path.
- Remove repeated instructions, behaviorally irrelevant examples, obsolete scaffolding, and unrelated tools.
- Prefer decision rules over unnecessary `always` or `never` language. Reserve absolutes for true invariants.
- Preserve explicit user values. Add criteria rather than broad defaults when a value must be inferred.
- For agents, state action authorization once: what read-only or local work is allowed and what external, destructive, costly, or scope-expanding action needs confirmation.
- State tool prerequisites, evidence behavior, meaningful fallbacks, validation, and stopping conditions where relevant.
- Keep personality and collaboration style short and behavioral. Do not let them replace task requirements.
- GPT-5.6 is concise by default. Do not add blanket brevity instructions unless the application needs them; specify required content and what may be omitted.
- For complex prompts, prefer short sections for role, personality, goal, success, constraints, tools, output, and stop rules.

## Other OpenAI reasoning models

Apply the universal profile conservatively. Do not assume every GPT-5.6-specific behavior or parameter applies to earlier or different model families.

## API advice kept outside the prompt

- Use `text.verbosity` for a request's default detail level when the API and model support it.
- Establish a reasoning-effort baseline and change it only after prompt, success, routing, and verification gaps are addressed.

## Official sources

- GPT-5.6 Sol prompting guidance: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- Using GPT-5.6: https://developers.openai.com/api/docs/guides/latest-model

