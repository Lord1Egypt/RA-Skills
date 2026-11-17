# grokified-code-review

An agent skill that reviews a git diff with a Grok model through [Grokified](https://grokified.com), an OpenAI-compatible API for Grok models. It finds real problems (bugs, security issues, data loss, race conditions, missing error handling, missing tests) and leaves the praise out.

The skill works with OpenClaw and any agent that reads the `SKILL.md` format.

## What it does

The agent runs `scripts/review.sh`, which:

1. Takes the diff for the range you ask for: your uncommitted changes, `main...HEAD`, the last commit, or any other git revision range.
2. Leaves out files that usually hold secrets (`.env*`, `*.pem`, `*.key`, `*.p12`, `id_rsa*`, `id_ed25519*`).
3. Stops if the diff is larger than 80,000 bytes, so a request stays under the 32,000 input-token cap per request that free accounts have.
4. Sends the diff to `https://api.grokified.com/v1/chat/completions` with the `grok-build-0.1` model and a short reviewer prompt.
5. Prints the review, and the token counts on stderr.

Nothing is stored by the script. The diff goes to the Grokified API and nowhere else. A secret written directly into ordinary source code is not detected, so do not review a diff that contains one.

## Requirements

- `git`, `curl` and `jq` on the PATH
- A Grokified API key in the `GROKIFIED_API_KEY` environment variable

## Setup

1. Create an account and an API key at [grokified.com/login](https://grokified.com/login). Keys start with `gk_live_` and are shown once.
2. Export the key:

   ```bash
   export GROKIFIED_API_KEY=your_grokified_api_key
   ```

3. Install the skill from ClawHub:

   ```bash
   clawhub install grokified-code-review
   ```

4. Ask your agent: "Review my uncommitted changes" or "Review this branch against main".

You can also run the script by hand from inside any git repository:

```bash
bash scripts/review.sh              # all uncommitted changes against HEAD
bash scripts/review.sh main...HEAD  # this branch against main
```

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `GROKIFIED_API_KEY` | none, required | Your Grokified API key |
| `GROKIFIED_MODEL` | `grok-build-0.1` | Model slug. See the [model list](https://grokified.com/docs/models). `grok-4.7` needs a Basic or higher Grokified plan |
| `GROKIFIED_REVIEW_MAX_BYTES` | `80000` | Largest diff the script will send |

## Pricing

Grokified charges 50% of the list price on every request, per token, from a prepaid balance. See the [pricing page](https://grokified.com/pricing) and the [docs](https://grokified.com/docs) for current rates and how credits work.

## Links

- Home: https://grokified.com
- Docs: https://grokified.com/docs
- Sign up and get a key: https://grokified.com/login

Grokified is operated by DEEPORAX AI LTD, UK company 17293947.

## Licence

Published on ClawHub under MIT-0.
