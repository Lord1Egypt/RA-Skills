# MindGraph OpenClaw skill

This folder is versioned with the MindGraph app. It teaches OpenClaw how to call MindGraph’s HTTP API using your account token.

**Agent behavior:** Most users only specify a **topic** (sent as **`prompt`**) and a **diagram type** — the eight **Thinking Maps** plus **mind map** (and **concept map** when needed). If someone wants **exact text on certain nodes**, the skill describes **`GET` diagram + `PATCH` nodes** instead of regenerating from scratch.

## Install (end users)

```bash
openclaw skills install mindgraph
```

Or copy this folder to the OpenClaw workspace `skills/mindgraph/`.

## Configure

**Fast path:** open **`demo.json`** in this folder — it is a ready-made `skills.entries` block you can merge into your OpenClaw config (e.g. `~/.openclaw/openclaw.json` or your host’s equivalent, such as Tencent WorkBuddy skill settings if the UI accepts JSON). Delete the `_instructions` key after merging.

Minimal shape:

```json
{
  "skills": {
    "entries": {
      "mindgraph": {
        "env": {
          "MINDGRAPH_BASE_URL": "https://test.mindspringedu.com",
          "MINDGRAPH_ACCOUNT": "138xxxxxxxx",
          "MINDGRAPH_TOKEN": "mgat_..."
        }
      }
    }
  }
}
```

- **MINDGRAPH_BASE_URL**: HTTPS origin of your MindGraph deployment (no trailing slash). Use the same origin you would use for API calls (not only the `/mindgraph` SPA path).
- **MINDGRAPH_ACCOUNT**: Phone number / account login (same as in MindGraph).
- **MINDGRAPH_TOKEN**: Generated in the app under **账户信息 → API Token** (shown once; **90-day** validity).

**HTTP timeouts:** Any host or tool that calls **`/api/web_content_mindmap_png`** (or other LLM + export routes) should allow **at least ~180 seconds** read timeout unless you know your server is faster. Default short timeouts in HTTP clients cause spurious failures.

### Tencent WorkBuddy (where is `env`?)

WorkBuddy is built on the OpenClaw stack, but **the UI changes by version** and there is **no single documented screen** that always says “skill environment variables.” Try this order:

1. **Settings / 设置** in WorkBuddy → search for **技能**, **Skills**, **Claw**, **OpenClaw**, **高级**, or **配置文件** — some builds expose a **JSON** or **per-skill** section where you can paste the `skills.entries.mindgraph.env` block from **`demo.json`** (same shape as the JSON above).
2. **Skill hub / 技能市场** → open the installed **MindGraph** (or your imported skill) → look for **配置**, **环境变量**, **编辑**, or a **⋯** menu on the skill card.
3. **Config file on disk** (if the app uses the standard layout): merge `demo.json` into **`%USERPROFILE%\.openclaw\openclaw.json`** if that file exists after WorkBuddy has run once. Other locations to check: **`%USERPROFILE%\.codebuddy\`**, **`%APPDATA%\CodeBuddy`**, or a **`.workbuddy`** folder under your user profile (per CodeBuddy docs for `models.json`). Close WorkBuddy, edit, save, restart.
4. **No env UI found:** Many WorkBuddy tutorials (e.g. third-party skills) put secrets **in the chat** (“here is my base URL / account / token”). You can do the same for testing: give **`MINDGRAPH_BASE_URL`**, **`MINDGRAPH_ACCOUNT`**, and **`MINDGRAPH_TOKEN`** in the Claw dialog; the model should follow **`SKILL.md`** and call the API with those values **without echoing the token**.

If nothing works, use **WorkBuddy / CodeBuddy in-app feedback** or **Tencent Cloud support** and ask specifically: *where to set `skills.entries.<name>.env` for OpenClaw skills* for your build.

### After you change auth

MindGraph applies new tokens and account checks on **every request**—no wait on the server. If you edit `MINDGRAPH_*` in OpenClaw/WorkBuddy and calls still fail or act like the old token, your **client** may have loaded env only at startup: **save** the config, then **restart** WorkBuddy or OpenClaw (or use a “reload skills / config” action if the product provides one). The next requests will use the new values.

## Publish updates (maintainers)

From the MindGraph repo root:

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./openclaw/skills/mindgraph --slug mindgraph --name "MindGraph" --version 1.3.0 --tags latest
```

Bump the **ClawHub** `--version` when `SKILL.md` or this README changes (current publish target: **1.3.0**).

**Inline recommendations:** the `start` and `next_batch` HTTP endpoints use **Server-Sent Events (SSE)**, not JSON-only responses. See `SKILL.md` §6.

## Files in this bundle

| File | Role |
|------|------|
| `SKILL.md` | Agent instructions (API paths, auth, timeouts, §3 `url` + `filename`, PNG signing, §8 shortcuts) |
| `demo.json` | Copy-paste `skills.entries.mindgraph` for `openclaw.json` |
| `README.md` | Install, configure, WorkBuddy hints, publish command |
