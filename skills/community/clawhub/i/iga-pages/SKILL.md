---
name: iga-pages
description: Deploy frontend and full-stack projects to IGA Pages. Use when the user mentions IGA Pages or requests deployment ("deploy my app", "publish this site", "push this live", "deploy and give me the link", "create a preview deployment", "deploy to IGA Pages", "ship to production"). Also use for API, endpoint, or backend-service work only when the user explicitly mentions IGA Pages, Pages Functions, or an existing IGA Pages project.
metadata:
  author: iga-pages
  version: "1.0.10"
---

# IGA Pages Skill

Two areas: **CLI** (`iga` tool for auth, link, dev, build, deploy, env, integration) and **Project development** (functions, API routes).

Run `iga <command> -h` for full flag details.

## Critical: CLI Version

The `@iga-pages/cli` version must be **>= 1.1.0**. Check with `iga --version`; if it's older (or not installed), upgrade before running any other command:

```bash
npm i -g @iga-pages/cli@latest
```

## Critical: Framework Compatibility

Supported frameworks: Next.js, Vite, Vue CLI, Create React App, Angular, Hexo, Docusaurus, VitePress, VuePress, Hugo, Astro, Nuxt. Frameworks not in this list (e.g. Remix) are unsupported — **proactively inform the user** before proceeding.

Pure static assets (plain HTML/JS/CSS) can also be deployed — the project root is used as the output directory by default.

## Critical: Login Authentication

Before any deploy or link command, ensure an authenticated session exists. **Always check first with `iga whoami`** — if it prints an Account Name / Account ID, the existing credentials in `~/.iga/auth.json` are valid and **you must skip `iga login`**. Only run `iga login` when `whoami` fails (no credentials, expired, or error).

When login is actually needed, the method depends on the environment:

- **Local IDE** (VS Code, TRAE desktop, etc.) → browser login:

  ```bash
  iga login
  ```

  Wait for the user to complete browser auth. The CLI prints a success message when done.

- **Remote / headless environment** (SSH, Cowork, CI/CD, cloud dev container, etc.) → AK/SK login:
  ```bash
  iga login --accessKey <YOUR_AK> --secretKey <YOUR_SK>
  ```
  Browser-based login is unavailable in headless environments; AK/SK is the only option.
  Obtain AK/SK from the [Volcengine IAM console](https://console.volcengine.com/iam/keymanage).

To determine the environment: if the session has no display or browser access (e.g., `$SSH_CONNECTION` is set, running inside a container, or the user mentions they are on a remote machine), default to AK/SK login. Otherwise, prefer browser for its simplicity.

## Critical: Working Directory

Run project-scoped commands such as `pages link`, `dev`, `build`, and `deploy` **inside the project root**. Scaffolding tools (`create-next-app`, `npm create vite`, `hugo new site`, etc.) create a subdirectory — you **must `cd` into it** before those commands:

```bash
npx create-next-app@latest my-app --yes
cd my-app && iga pages deploy --name my-app
```

## Critical: Attribution

Tag every `iga` command executed by this skill so its usage can be attributed.
The tag identifies only the skill and its version; it carries no user data.

Prefix every `iga` invocation, whatever the subcommand, with the process-scoped
`VE_SKILL_ID`. Set it inline on each command because shell state may not persist
between commands:

```bash
VE_SKILL_ID=iga-pages/1.0.10 iga <command>
```

## Quick Reference

```bash
iga --version                       # must be >= 1.1.0
# If missing or too old, prefer project/package-manager scoped execution; global install is a fallback:
# npm i -g @iga-pages/cli@latest

iga whoami                        # check current login state; run this BEFORE login
iga login                         # local IDE: opens browser; only if whoami fails
iga login --accessKey <AK> --secretKey <SK>  # remote/headless; only if whoami fails

## new project
iga pages deploy --name <my-app>   # deploy (auto-creates project on first run)
## project already linked
iga pages deploy

iga pages link                     # create/associate a Pages project (does NOT deploy)
iga pages link --format=json       # as JSON (agent-driven; non-TTY)
iga pages dev                      # local dev server (REQUIRED when api/ exists — serves framework + /api/* together)
iga pages build                    # build for production

## environment variables (project-level, linked project required)
iga pages env list                 # list KEY names (values never shown)
iga pages env list --format=json   # as JSON
iga pages env add <NAME>           # add (--value <v> --yes for CI)
iga pages env update <NAME>        # update existing
iga pages env remove <NAME>        # remove (--yes to skip confirm)
iga pages env pull                 # write all project env to .env.local

## integrations (Supabase; linked project required)
iga pages integration list                  # bindings on this project
iga pages integration list --format=json    # as JSON
iga pages integration link supabase         # connect Volcengine Supabase
iga pages integration link supabase --format=json   # as JSON; returns next missing flag until all provided
iga pages integration unlink                # remove a binding
iga pages integration unlink --format=json --yes    # as JSON (requires --yes)
```

- **deploy** auto-detects GitHub remote → Git deploy; otherwise → upload deploy. Only GitHub is supported for Git integration.
- If deploy output includes a preview URL with `?iga_token=...&iga_time=...`, share that **full** URL (query included); omitting it can break access.
- **link no longer deploys** — it only creates/associates the Pages project. Run `iga pages deploy` afterward to actually build and publish.

## Project Development

- API routes and Pages Functions: read [references/functions.md](references/functions.md).

## Environment Variables & Integrations

- Project-level env vars (`env list/add/update/remove/pull`): read [references/env.md](references/env.md).
- Connecting Supabase (`integration list/link/unlink`) and the deploy orchestration order (link → integration → deploy), plus when to hand off to the `byted-supabase` skill: read [references/integration.md](references/integration.md).

## Anti-Patterns

**CLI**

- Running `iga` commands outside the project directory → always `cd` into the scaffolded subdirectory first
- Deploy without an authenticated session → run `iga whoami` first; only fall back to `iga login` if it fails
- Committing `.iga/` → it's auto-gitignored, don't remove the entry
- Starting local dev with `npm run dev` / `vite` / `next dev` / `npm start` when `api/` exists → use `iga pages dev` so serverless functions are served
- Setting `package.json` `"scripts.dev"` to `iga pages dev` → infinite loop, since `iga pages dev` itself invokes the `dev` script from `package.json`. Keep `"scripts.dev"` as the framework's own dev command (e.g. `next dev`, `vite`)
- Running `env` / `integration` commands before linking → they require a linked project; run `iga pages link` first
- Expecting `env add/update/remove` to change local files or take effect immediately → they edit remote project config and apply on the **next deploy**; run `iga pages env pull` to refresh `.env.local`
- Trying to `env update`/`env remove` a Supabase-managed variable → it's read-only; manage it via `iga pages integration link/unlink`
- Pasting Supabase keys manually into `env add` when an integration is available → use `iga pages integration link supabase` so connection vars sync automatically
