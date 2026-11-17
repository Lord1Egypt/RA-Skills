# powpow-publisher — Publish posts & digital humans to the public map

PowPow assistant (OpenClaw): turn your photos or raw material into a
travelogue and publish it to PowPow, or turn a person/character into a chat-capable
digital human pinned to the public map.

This package carries the content of
[powpow-simple-en](https://clawhub.ai/durenzidu/skills/powpow-simple-en) v1.0.0
(the English edition of [powpow-simple](https://clawhub.ai/durenzidu/skills/powpow-simple),
feature parity with v5.7.3; scripts are byte-identical).

## Install

```
openclaw skills install @durenzidu/powpow-publisher
```

## Requirements

- Node.js 18+ (scripts use global `fetch`, no third-party dependencies)
- A PowPow account: https://global.powpow.online/register

## State directory

The skill bundle stays read-only. Login tokens and user config live in a state directory:

- Default: `~/.powpow/`
- Override with the `POWPOW_STATE_DIR` environment variable

To customize the platform URL or the Unsplash key, drop a `config.json` into the state
directory — it overrides the bundled defaults.

## Usage examples

```
cd <skill-dir>
node scripts/doctor.js                                   # self-check + session probe
node scripts/login.js <username>                         # login (password via stdin, never stored)
node scripts/geocode.js "地坛公园" --limit 5              # place name -> coordinates
node scripts/match-digital-human.js "读书 作家" --limit 3  # match digital humans
node scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/abs/path/cover.jpg --out post-draft.html
node scripts/publish.js post-draft.html                  # publish
node scripts/verify.js <post-id>                         # verify after publishing
node scripts/delete-post.js <post-id>                    # delete (test cleanup)
```

Local paths passed to `--image` **must be absolute**.

Note: the platform's place search and digital-human library are currently strongest
in Chinese; non-Chinese users can paste local-language names and topics.

## Security

- No platform secrets bundled; every operation goes through the platform's public API + the user's own JWT.
- The password is used once at login and never stored; tokens expire after ~7 days.
- See `references/security.md` for details.

## Notes for reviewers (SkillSpector / manual review)

- This is an **instruction-style skill**: SKILL.md orchestrates a multi-script
  pipeline. Every script under `scripts/` is one documented step of the
  publishing workflow (login → self-check → geocode → match → compose →
  publish → verify), not an independent hidden tool.
- `delete-post.js` deletes only the logged-in user's own post
  (`DELETE /api/posts/{id}`, JWT-scoped, enforced server-side) and is
  documented in SKILL.md Step 8 for test cleanup. This capability is also
  declared in the skill description.
- No secrets are bundled. `config.json` ships defaults only. The session JWT
  is written to the user's state directory (`POWPOW_STATE_DIR`, default
  `~/.powpow/session.json`), never inside the skill bundle. Passwords are
  never persisted.
- All environment variables used (`POWPOW_STATE_DIR`, `POWPOW_PASSWORD`,
  `UNSPLASH_ACCESS_KEY`) are optional and declared in SKILL.md frontmatter
  (`metadata.openclaw.envVars`).
- This package carries the content of `powpow-simple-en` v1.0.0 (English
  edition of `powpow-simple` v5.7.3); scripts are byte-identical to those
  packages (only the display name, install command, and this note differ).

## License

MIT-0 (ClawHub-wide license).

## Links

- Website: https://global.powpow.online
- Map: https://global.powpow.online/map
- English edition: https://clawhub.ai/durenzidu/skills/powpow-simple-en
- Chinese edition: https://clawhub.ai/durenzidu/skills/powpow-simple
