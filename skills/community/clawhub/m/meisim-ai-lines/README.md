# MeiSIM AI lines: a skill for AI agents

Real US mobile numbers for AI agents, on the T-Mobile network, not virtual numbers. Texts over the API and webhooks; voice over SIP with the number as caller ID. $35 a month for texts, $45 with voice, two months up front. Every account passes an identity check, and we keep spammers off our lines.

`SKILL.md` is what the agent reads. It walks the agent through these steps:

1. Read the live offer (`GET https://api.meisimusa.com/web/ai-lines/offer`, no key).
2. Explain the line and its price to its owner in plain words.
3. Send the owner to https://www.meisimusa.com/get-started.html. The owner passes the identity check and pays. The agent never does either.
4. With the owner's API key in `MEISIM_API_KEY`, check the account.
5. Ask the owner to approve the exact price, and order only on a clear yes.
6. Order the line (`POST /api/v1/sms/order`).
7. Read texts by webhook or over the API, and reply.
8. Set up voice over SIP, with the AI saying it is an AI at the start of every call.

It needs `curl`. `MEISIM_API_KEY` is optional until the owner has an account, so the skill loads before the key exists.

API reference: https://www.meisimusa.com/api-docs.html#sms-lines. Terms: https://www.meisimusa.com/api-terms.html. Help: support@meisimusa.com.

## Publishing (maintainers)

ClawHub publishes the whole folder, this file included. Keep nothing private in it.

Before each release:

1. Check that the prices in `SKILL.md` match `https://api.meisimusa.com/web/ai-lines/offer`.
2. Check that every path in `SKILL.md` is still in https://www.meisimusa.com/api-docs.html.
3. Check that https://www.meisimusa.com/get-started.html is live.

First release:

1. Install the command line tool: `npm i -g clawhub`
2. Sign in with the GitHub account that will own the listing: `clawhub login`. It prints a link and a one-time code. Open the link, sign in with GitHub, and enter the code. ClawHub asks for a GitHub account at least 14 days old.
3. Check the sign-in: `clawhub whoami`
4. From the repository root, publish:

   ```bash
   clawhub skill publish ./clawhub/meisim-ai-lines \
     --slug meisim-ai-lines \
     --name "MeiSIM AI Lines" \
     --version 1.0.0 \
     --changelog "First release: live offer, owner sign-up, ordering only on the owner's clear yes, texts by webhook or API, voice over SIP."
   ```

   Add `--owner <organization handle>` to publish under an organization instead of the signed-in account.
5. Wait for the automated security checks. A new release stays out of search and installs until they pass. Its page is `https://clawhub.ai/<handle>/skills/meisim-ai-lines`, and its record is https://clawhub.ai/api/v1/skills/meisim-ai-lines.
6. Once it is listed, add it to `website/llms.txt` in the AI lines section and deploy the website:

   ```
   - Skill for AI agents on ClawHub: https://clawhub.ai/<handle>/skills/meisim-ai-lines
   ```

Later releases: edit `SKILL.md`, raise `version` in its front matter, and publish again with the same command, the new `--version` and a new `--changelog`.

Agents install it with `openclaw skills install @<handle>/meisim-ai-lines`.

Every skill on ClawHub is licensed MIT-0. ClawHub has no paid skills, so the skill carries no price metadata. The prices live in the instructions and in the live offer.
