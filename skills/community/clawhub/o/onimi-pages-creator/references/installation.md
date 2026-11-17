# Install Onimi Pages Creator

The default Onimi setup explicitly prepares Creator and Publish for the current agent while preserving
existing folders and local changes. Installation runs locally. It does not connect an account, send a
prompt to Onimi Pages, or publish a page.
Give both modules to the current agent as one installation task. Creation and prepublish checks use
the model this agent already uses; no separate local model installation is needed.

## npm

Use npm's `latest` suite only when the Publish npm channel is available and its channel version equals
the current Publish version in the [stable manifest](https://downloads.onimi.ai/skills/manifest.json).
An older available package may not contain `install --suite`. Node.js 20 or later is required.

```sh
npx --registry=https://registry.npmjs.org onimi-pages-publish@latest install --suite --agent codex
```

Replace `codex` with `claude-code` or `cursor`. For another client, use its documented personal skills
directory with `install --suite --dir /absolute/path/to/skills`. The installer adds only missing modules
and performs no network, account, or publishing action. The standalone `onimi-pages-creator` package
remains an advanced local-only option.

## Direct download

Read the complete `skills.creator.archive.url`, `skills.creator.archive.sha256`, and
`skills.creator.archive.size` fields plus the matching `skills.publish.archive.url`,
`skills.publish.archive.sha256`, and `skills.publish.archive.size` fields from the
[stable manifest](https://downloads.onimi.ai/skills/manifest.json). Download both immutable archive
URLs, verify each byte size and SHA-256, then add only a missing complete folder. This flow preserves
both existing modules and does not depend on the website's latest-redirect route being deployed first.

| Client | Personal skills parent directory |
| --- | --- |
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| Cursor | `~/.cursor/skills` |

## GitHub

Official repository: https://github.com/zlch-oceanai/onimi-pages-creator

```sh
npx --registry=https://registry.npmjs.org skills@1.5.26 add zlch-oceanai/onimi-pages-creator --skill onimi-pages-creator --global
```

## ClawHub

Use this channel only when the stable manifest marks it available:
The pinned ClawHub CLI requires Node.js 22 or later; use another verified channel on Node.js 20.

```sh
npx --registry=https://registry.npmjs.org clawhub@0.23.3 install @mariohazy/onimi-pages-creator
```

## Verify and use

Restart or reload the current agent if required, then ask it to create one local Page or Bento-based
Slides artifact. The Skill includes `scripts/validate-html.mjs`; validation and browser preview do not
publish the file.

Creation and publication are separate. The suite may already have prepared Publish, but browser OAuth
starts only when a cloud template, cloud draft, cloud Slides or publication task needs it. Reuse a valid
same-account connection with sufficient scopes. Never substitute a test service URL.

The bundled manager applies only when a direct-download installation has `.onimi-skill.json` beside
`SKILL.md`; if the receipt is absent, use that channel's native update flow. For a receipt-backed
installation, resolve the installed Skill directory from its `SKILL.md` path and
invoke the manager by absolute path without changing the user's workspace directory. Run
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs status` locally and
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs check` for a non-blocking daily update
check. Update only after reviewing the version and explicitly approving
`node /absolute/path/to/onimi-pages-creator/scripts/manage.mjs update --confirm onimi-pages-creator@<version>`.
npm, GitHub and ClawHub use
their own update mechanisms.
