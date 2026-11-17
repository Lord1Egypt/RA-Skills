# Mallary CLI - Project Structure

## Overview

Mallary CLI is the official command-line interface for the public Mallary API. This architecture guide starts with read-only inspection paths. It also inventories explicit-request, state-changing code paths later in the document. For an AI agent, an implemented code path is not authorization to suggest or use it.

## Agent Safety Boundary

This file is an architecture inventory, not a workflow recommendation. An AI agent must:

- start with the minimum read-only discovery needed for the user's request
- never treat a listed command, endpoint, or code path as permission to invoke it
- avoid suggesting an upload or state-changing command unless the user explicitly asks for that type of action
- treat a clear request to publish, schedule, upload media for that post, or send a reply as authorization for that action; do not ask for a second confirmation
- ask only for missing material details, keep the action within the request, run it once, and verify it with a read-only command

## Directory Structure

```text
cli/
├── src/                          # Source code
│   ├── index.ts                  # CLI entry point
│   ├── main.ts                   # Command parsing, request handling, rendering
│   ├── oauth.ts                  # OAuth device flow, refresh, revocation, credential storage
│   └── version.ts                # Version export
│
├── dist/                         # Build output (generated)
│   ├── index.js                  # Executable entry
│   ├── main.js                   # Compiled command logic
│   ├── oauth.js                  # Compiled OAuth logic
│   └── version.js                # Compiled version module
│
├── test/                         # CLI tests
│   ├── cli.test.ts               # Command and behavior tests
│   └── oauth-auth.test.ts        # OAuth, refresh, precedence, and token-safety tests
│
├── package.json                  # Package configuration
├── package-lock.json             # npm lockfile
├── tsconfig.json                 # TypeScript configuration
├── .gitignore                    # Git ignore rules
├── README.md                     # Main documentation
├── SKILL.md                      # AI agent usage guide
├── QUICK_START.md                # Quick start guide
├── PROFILES.md                   # Profile IDs, scoping, API endpoints, and limits
├── PROJECT_STRUCTURE.md          # This file
├── FEATURES.md                   # Feature summary
├── PROVIDER_SETTINGS.md          # Provider-settings agent safety boundary
├── SUPPORTED_FILE_TYPES.md       # Read-only media format reference
└── other supporting .md docs     # Additional usage, workflow, and publishing notes
```

## File Descriptions

### Source Files

#### `src/index.ts`

- executable entry point
- imports `runCli()` from `main.ts`
- exits with the returned CLI exit code

#### `src/main.ts`

- primary implementation file
- uses the built-in `parseArgs` module of Node
- validates CLI input
- resolves local media files
- uploads local files to Mallary
- sends authenticated requests to the Mallary API
- shows human output and JSON output

#### `src/oauth.ts`

- starts OAuth device authorization with read, publish, engage, and manage access in one login
- exchanges and refreshes tokens without printing them
- revokes OAuth access on logout
- stores credentials outside the project with restrictive local permissions

#### `src/version.ts`

- exports the CLI version for the help output and the version output

### Configuration Files

#### `package.json`

- package name: `@mallary/cli`
- executable bin: `mallary`
- scripts: `build`, `dev`, `start`, `test`
- metadata for npm publishing

#### `tsconfig.json`

- TypeScript compiler configuration
- outputs compiled files into `dist/`

### Documentation Files

#### `README.md`

- read-only OpenClaw agent overview
- intentionally omits write commands, payloads, and mutation workflows

#### `SKILL.md`

- condensed safety contract and command reference for AI agents and LLM-driven workflows

#### `QUICK_START.md`

- read-only installation, authentication, and discovery guide that routes any requested write to the request-handling rules in `SKILL.md`

#### `PROFILES.md`

- explains profiles, public profile IDs, profile-scoped resources, and plan limits
- documents profile-aware CLI flags and API endpoints

#### `PROJECT_STRUCTURE.md`

- architecture overview
- file descriptions
- command flow and integration points

### Test Files

#### `test/cli.test.ts`

- validates command behavior
- checks input validation, upload handling, and API request shaping

## Build Process

### Development Build

```bash
cd cli
npm run build
```

- compiles TypeScript to ESM JavaScript
- writes output to `dist/`

### Production Build

```bash
cd cli
npm run build
```

Build characteristics:

1. compiles `src/index.ts`, `src/main.ts`, and `src/version.ts`
2. preserves the executable entry file
3. emits small, plain JS output rather than a bundled framework build

### Output

- `dist/index.js` - executable wrapper
- `dist/main.js` - main compiled CLI logic
- `dist/version.js` - version metadata

## Commands Architecture

### Command Flow

```text
Read-only or explicitly requested input
    ↓
src/index.ts
    ↓
runCli() in src/main.ts
    ↓
Argument parsing / validation
    ↓
Optional local file upload handling (user-requested)
    ↓
Authenticated request to Mallary API
    ↓
Human output or --json output
```

### Read-Only Discovery Commands

This is the only command inventory intended for agent discovery. Request the minimum data needed and redact sensitive output before sharing it.

1. `health` - check Mallary service health without authentication
2. `profiles list` - inspect profile IDs and account structure
3. `platforms list` - inspect connected-platform state
4. `posts list` - inspect grouped post history and status
5. `jobs get <id>` - inspect one job and its result
6. `analytics list` - inspect available analytics rows
7. `audience list` - inspect follower and subscriber counts
8. `settings get` - inspect saved brand configuration
9. `webhooks list` - inspect configured webhook destinations

### Explicit-Request Code Paths (Syntax Intentionally Omitted)

The implementation also contains data-transmitting and state-changing handlers. Their executable CLI syntax is intentionally omitted from this agent-facing architecture guide. Their presence in `src/main.ts` is not permission to suggest or invoke them.

If the user explicitly asks for a state-changing Mallary action, follow the Agent Safety Boundary and `SKILL.md`: use read-only discovery only as needed, ask for missing material details, carry out a clear publishing request without another confirmation, run it once, and verify it with a read-only command.

## Environment Variables

| Variable | Required | Default | Usage |
| --- | --- | --- | --- |
| `MALLARY_API_KEY` | No | stored OAuth | Optional API-key override for CI or other non-interactive environments |

### Credential Handling

OAuth is the interactive default. It grants read, publish, engage, and manage access in one login, refreshes automatically, and stores credentials outside the project. Users do not choose scopes. When `MALLARY_API_KEY` is set, it takes precedence over stored OAuth.

`MALLARY_API_KEY` is a bearer credential. It can authorize posts, uploads, webhook changes, settings updates, and account-management actions. Treat it as a secret.

- Store keys in a local secret manager, a locked-down untracked env file, or a CI secret store. Never commit them to source control.
- Avoid shell-history exposure: do not paste a real key into shared terminals, documentation, tickets, prompts, or screenshots.
- Do not print keys with `echo`, `printenv`, debug traces, request logs, or CI output. Redact all characters except the last few before you share logs.
- In CI, pass the key through masked secrets such as `secrets.MALLARY_API_KEY`. Disable shell tracing around Mallary commands. Restrict log access.
- If a key appears in logs, chat, shell history, or a committed file, rotate or revoke it before you continue.

## Dependencies

### Runtime Dependencies

- Node.js built-ins such as `fs/promises`, `path`, and `util`
- global `fetch` available in Node 18+

### Dev Dependencies

- `typescript`
- `tsx`
- `vitest`
- `@types/node`

## Integration Points

### With the Repository

1. built from the standalone `cli/` package
2. tested with `npm test`
3. published from `cli/package.json`

### With the Mallary API

Read-only integration endpoints used during discovery:

1. `GET /health`
2. `GET /api/v1/profiles`
3. `GET /api/v1/platforms`
4. `GET /api/v1/posts`
5. `GET /api/v1/jobs/{id}`
6. `GET /api/v1/analytics`
7. `GET /api/v1/audience`
8. `GET /api/v1/settings`
9. `GET /api/v1/webhooks`

Explicit-request write endpoint paths are intentionally omitted from this agent-facing architecture guide. An endpoint implemented by the API is not authorization to call it.

Profile-aware endpoints accept a public `profile_id`. If you omit it, Mallary selects the default Dashboard profile.

Authentication:

- Bearer token from stored OAuth or `MALLARY_API_KEY`
- OAuth device authorization, token refresh, and token revocation use `https://auth.mallary.ai`
- CLI also sends `x-mallary-client: cli`

## Publishing

### To npm

```bash
cd cli
npm publish --access public
```

### Package Contents

- `dist/`
- `README.md`
- `SKILL.md`
- `PROFILES.md`

## Testing

### Manual Testing

```bash
# Build
cd cli && npm run build

# Test without OAuth or an API key. Authenticated commands must fail
node dist/index.js posts list

# Test safe OAuth status output
node dist/index.js auth status

# Test general help
node dist/index.js --help
```

### Automated Testing

```bash
cd cli
npm test
```

## Future Enhancements

- more command-specific help without authentication
- more platform-specific helper commands
- more structured JSON output for automation-heavy workflows
- more CLI-side checks for advanced `platform_options`

## Support

- Site: https://mallary.ai
- Docs: https://docs.mallary.ai
- Repository: https://github.com/mallarylabs/mallary-agent
- Support: support@mallary.ai
