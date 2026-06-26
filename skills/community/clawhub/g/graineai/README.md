# NoddyAI API skill (ClawHub / OpenClaw)

This folder is a **skill definition**: markdown the host loads so agents know how to call **https://api.graine.ai**. It is not a standalone runtime.

---

## 1. `openclaw run` shows "unknown command run"

**Expected.** Many OpenClaw CLI builds do not include `run`. The tool is mainly for packaging and publishing skills, not executing them like a local runner.

**What to do**

1. Check your CLI: `openclaw --help`
2. Test the API directly (Bearer token):

   ```bash
   curl -sS -H "Authorization: Bearer YOUR_gat_TOKEN" \
     "https://api.graine.ai/api/v1/api-tokens/validate-token"
   ```

3. After publish, use the skill from the ClawHub / workspace flow your setup expects.

---

## 2. ClawHub: "Server Error Called by client" (validation OK, publish fails)

This text is a **generic Convex/client wrapper** used on ClawHub when a mutation fails. It is a **known pain point** upstream; fixes have landed on `main` but some users still see it in the **web UI** (see [openclaw/clawhub#477](https://github.com/openclaw/clawhub/issues/477), [openclaw/clawhub#1179](https://github.com/openclaw/clawhub/issues/1179)).

**Try in order**

| Step | Action |
|------|--------|
| Network | DevTools -> Network -> click Publish -> read the failing request **status** and **response body** (not only the banner). |
| First-time publisher | If this is your first publish, failure may be `users:ensure` / publisher setup; see issue **#1179** and retry after login or support fix. |
| Slug | Use a unique slug (e.g. `graineai-voice-api-<your-init>`). |
| Changelog | Replace auto-generated text with one short line: `Initial release.` |
| Smaller bundle | Upload only `SKILL.md`, `endpoints.md`, `examples.md`, `webhooks.md` (omit this README) to rule out extra file handling. |
| Import path | If the site offers **Import from GitHub**, try that instead of folder upload. |
| Browser | Incognito, different browser, disable blockers. |

If the API returns **500** with a minimal payload and unique slug, it is likely **ClawHub/Convex** - open an issue on [openclaw/clawhub](https://github.com/openclaw/clawhub) with **screenshot of Network response** and **timestamp**.

---

## 3. Files in this package

| File | Purpose |
|------|---------|
| `SKILL.md` | Main instructions for the agent |
| `endpoints.md` | Paths and methods |
| `examples.md` | Example bodies |
| `webhooks.md` | Webhook shapes |

Auth: `Authorization: Bearer <API_KEY>` (keys start with `gat_`), plus `org_id` where required (see `SKILL.md`).

---

## 4. ClawHub "suspicious" / OpenClaw security flag

Automated review may flag **telephony** skills because they describe powerful APIs. `SKILL.md` now states explicitly: **no credentials in the package**, user-supplied secrets only, confirmation before calls/transfers/deletes, and session-scoped ID retention.

If the flag persists after you publish an updated version, open an issue on [openclaw/clawhub](https://github.com/openclaw/clawhub) and ask for a **manual review** or breakdown; link your skill page and mention the updated `Security, credentials, and user consent` section.

## 5. Note

ClawHub is distribution. Your API still works with public docs and `curl`; this skill is one packaging format on top.
