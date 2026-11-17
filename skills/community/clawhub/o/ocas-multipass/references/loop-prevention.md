# Loop Prevention Rules

LLMs get stuck. They retry the same action with meaningless variations, invent theories about why something failed ("too fast," "data isn't ready yet"), and wait for things that aren't coming. Multipass has hard circuit breakers. Read `references/resilience.md` §Circuit breakers for the full logic.

## Rules every worker must follow

- **Same action, same result = move on.** If an endpoint returned an error, calling it again with slightly different headers or timing will return the same error. Two identical failures on the same endpoint is the maximum. After that, the endpoint is dead. Skip it.
- **A failure is an answer, not a mystery.** A 403 means you're not authorized. A 404 means it doesn't exist. A connection refused means the server is down. Do not theorize about why. Do not invent timing explanations. Read the error, log it, move on.
- **No waits longer than 30 seconds.** The only legitimate wait is polling for a verification email (10s intervals, 2min max). Everything else is the agent stalling. If a step needs "waiting," it's failed.
- **No folk theories.** Do not reason about whether the server is "busy," "processing," "eventually consistent," or "warming up." If the response isn't what you expected, it failed. Try a different approach or a different service.
- **Track every action.** Before performing any action, check `log.jsonl`: have I done this before? If the same URL+method appears 2+ times with failures, do not try it again.
- **Budget per gap.** Maximum 5 total candidates attempted per capability gap. If 5 candidates all fail, the gap is unsolvable with available tools. Report it and move on.
