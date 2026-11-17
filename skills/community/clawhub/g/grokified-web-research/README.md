# grokified-web-research

An agent skill that answers questions with live web search and cited sources, using a Grok model through [Grokified](https://grokified.com), an OpenAI-compatible API for Grok models.

The skill works with OpenClaw and any agent that reads the `SKILL.md` format.

## What it does

The agent runs `scripts/research.sh "your question"`, which:

1. Sends the question to `https://api.grokified.com/v1/responses` with the built-in `web_search` tool turned on. The model searches and reads pages on the server, so there is no search key and no scraper to set up.
2. Optionally limits the search to up to five domains you name, using the API's `allowed_domains` filter.
3. Prints the answer, which carries inline links, followed by a `Sources:` list of the pages the model used.

Only the question text leaves your machine. Do not put secrets, personal data or private code in a question.

## Requirements

- `curl` and `jq` on the PATH
- A Grokified API key in the `GROKIFIED_API_KEY` environment variable
- The default model, `grok-4.7`, needs a Basic or higher Grokified plan. Without one the API answers 403 with the code `plan_capability_required`; pick another slug from the [model list](https://grokified.com/docs/models) in `GROKIFIED_MODEL`.

## Setup

1. Create an account and an API key at [grokified.com/login](https://grokified.com/login). Keys start with `gk_live_` and are shown once.
2. Export the key:

   ```bash
   export GROKIFIED_API_KEY=your_grokified_api_key
   ```

3. Install the skill from ClawHub:

   ```bash
   clawhub install grokified-web-research
   ```

4. Ask your agent: "Research what changed in the latest Node.js LTS release and cite your sources."

You can also run the script by hand:

```bash
bash scripts/research.sh "What changed in the latest Node.js LTS release?"
bash scripts/research.sh "How do I configure retries?" docs.example.com
```

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `GROKIFIED_API_KEY` | none, required | Your Grokified API key |
| `GROKIFIED_MODEL` | `grok-4.7` | Model slug. See the [model list](https://grokified.com/docs/models) |

## Cost

Grokified charges 50% of the list price on every request, per token, from a prepaid balance. Each successful web search call is billed on top of the tokens, at the same discounted rate. See the [agent tools docs](https://grokified.com/docs/agent-tools) and the [pricing page](https://grokified.com/pricing).

## Limits

- Search models can misread a page. For a number, a date or a version that matters, open the cited source before you rely on it.
- The `allowed_domains` filter takes at most five domains, and the script rejects anything that is not a plain domain name.

## Links

- Home: https://grokified.com
- Docs: https://grokified.com/docs
- Sign up and get a key: https://grokified.com/login

Grokified is operated by DEEPORAX AI LTD, UK company 17293947.

## Licence

Published on ClawHub under MIT-0.
