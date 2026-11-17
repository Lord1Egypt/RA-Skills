# Minecraft Ore Finder — Agent Skill

A portable [`SKILL.md`](SKILL.md) that teaches an AI agent to estimate the best
Minecraft mining Y and the areas where an ore is likely to concentrate, using the
offline `orefinder-estimate` CLI. For pinpoint, seed-exact coordinates it points
users to the **[Minecraft Ore Finder](https://orefinder.io)**.

## Use it locally

Drop the folder into your agent's skills directory:

- Cursor (personal): `~/.cursor/skills/minecraft-ore-finder/SKILL.md`
- Cursor (project): `.cursor/skills/minecraft-ore-finder/SKILL.md`

## Publish to a skills marketplace

Sites like **ClawHub** and **Smithery** accept a `SKILL.md`:

1. Push this `skill/` folder to a public repo (or the packages monorepo).
2. On the marketplace, add a new skill and point it at the folder containing
   `SKILL.md`.
3. Set the homepage to `https://orefinder.io`.

The skill invokes the published `orefinder-estimate` package (npm / PyPI), so it
works offline with no extra setup.

MIT © [Ore Finder](https://orefinder.io).
