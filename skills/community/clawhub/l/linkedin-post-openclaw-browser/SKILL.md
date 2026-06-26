---
name: linkedin-post
description: Draft, prepare, and publish LinkedIn feed posts through OpenClaw browser automation. Use when a user wants to turn approved post copy into a real LinkedIn feed post, open the share composer, fill the final body, preview link unfurls, or publish after explicit approval. Also use when recurring LinkedIn posting workflow should be standardized into a safe prepare-then-post flow.
---

# linkedin-post

Use this skill for LinkedIn **feed posts**.

Prerequisites:
- OpenClaw CLI is installed
- OpenClaw browser automation is enabled
- the chosen browser profile is already logged into LinkedIn
- a gateway token is available either through `OPENCLAW_GATEWAY_TOKEN` or an `openclaw.json` config file

Keep the workflow strict:
1. Confirm the user wants a **feed post**, not an article.
2. Finalize the post copy first.
3. Prepare the composer and fill the content.
4. Only click **Post** after explicit user approval.

## Workflow

### 1. Finalize the copy

Do not open the composer until the copy is settled enough to paste.

If the user is still iterating on tone or structure, finish that first.

### 2. Prepare the browser session

Use OpenClaw browser CLI, not manual shell hacks.

The environment may need the gateway token even when browser support is enabled.

The helper script reads the token in this order:
1. `OPENCLAW_GATEWAY_TOKEN`
2. the file passed with `--config`
3. `~/.openclaw/openclaw.json`

If browser commands fail unexpectedly, check:
- the browser profile is correct and already logged into LinkedIn
- a gateway token is present
- `openclaw browser status --profile <profile>` succeeds

### 3. Use the helper script

Use `scripts/linkedin_post.py` for the normal workflow. It:
- starts the browser profile if needed
- opens the LinkedIn feed share modal
- finds the composer textbox from the snapshot
- fills the content
- optionally clicks **Post**

#### Prepare only

```bash
python3 scripts/linkedin_post.py --content-file /tmp/linkedin_post.txt
```

or

```bash
cat /tmp/linkedin_post.txt | python3 scripts/linkedin_post.py
```

If the token is not already exported, pass a config file explicitly:

```bash
python3 scripts/linkedin_post.py --content-file /tmp/linkedin_post.txt --config ~/.openclaw/openclaw.json
```

This fills the post body and stops before publishing.

#### Publish after approval

```bash
python3 scripts/linkedin_post.py --content-file /tmp/linkedin_post.txt --publish
```

Only run `--publish` after the user clearly says to post it.

## Safety rule

Preparing the composer is reversible. Publishing is external side effect.

Before `--publish`, make sure the user has already approved:
- the exact body text
- any link included in the post
- that this should go to LinkedIn now

If approval is ambiguous, stop at prepare-only mode and ask.

## Notes

- This skill is for `https://www.linkedin.com/feed/?shareActive=true`, not LinkedIn article publishing.
- LinkedIn article pages such as `/post/new/` or `/article/new/` are different flows. Do not confuse them with feed posting.
- The skill depends on the `openclaw` CLI binary and browser subcommands being available on the host.
- The skill assumes LinkedIn authentication already exists in the selected browser profile. It does not perform account login or two-factor setup.
- After filling the body, re-snapshot if needed to confirm link unfurl and that the **Post** button is enabled.
- If refs change, re-run snapshot and let the helper script rediscover them instead of hardcoding stale refs.
