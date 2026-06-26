# discord.js Patterns

Use this reference when working in JavaScript or TypeScript with discord.js.

## Preferred Stack

- `discord.js` current major used by the repo
- TypeScript when the project already uses TS or when creating a new structured bot
- `dotenv` or native env loading

## Recommended Command Shape

Each command module should usually expose:
- metadata / builder definition
- execute handler

Typical responsibilities:
- validate permissions
- validate arguments/options
- defer reply if slow
- catch and report errors cleanly

## Recommended Event Shape

Each event module should usually expose:
- event name
- once flag
- execute handler

## Registration Guidance

Use guild registration during development for fast propagation.
Use global registration only when the command set is ready for production.

## Interaction Safety

- Acknowledge interactions within Discord's time window.
- Prefer `deferReply` for slow operations.
- Use ephemeral responses for setup/admin actions where appropriate.
- Namespace component custom IDs.

## Common Pitfalls

- Using outdated v13 examples in v14+ projects
- Mixing CommonJS and ESM incorrectly
- Forgetting `GatewayIntentBits`
- Registering commands against the wrong application or guild
- Not enabling privileged intents in the developer portal
