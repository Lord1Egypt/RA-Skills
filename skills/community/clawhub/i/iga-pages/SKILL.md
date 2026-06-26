---
name: iga-pages
description: Deploy frontend and full-stack projects to IGA Pages. Use when the user mentions IGA Pages or requests deployment ("deploy my app", "publish this site", "push this live", "deploy and give me the link", "create a preview deployment", "deploy to IGA Pages", "ship to production"), or wants to develop an API ("write an API", "create an endpoint", "build a backend service").
metadata:
  author: iga-pages
  version: "1.0.5"
---

# IGA Pages Skill

Two areas: **CLI** (`iga` tool for auth, link, dev, build, deploy) and **Project development** (functions, API routes).

Run `iga <command> -h` for full flag details.

## Critical: CLI Version

The `@iga-pages/cli` version must be **>= 1.0.3**. Check with `iga --version`; if it's older (or not installed), upgrade before running any other command:

```bash
npm i -g @iga-pages/cli@latest
```

## Critical: Framework Compatibility

Supported frameworks: Next.js, Vite, Vue CLI, Create React App, Angular, Hexo, Docusaurus, VitePress, VuePress, Hugo. Frameworks not in this list (e.g. Nuxt, Remix, Astro) are unsupported — **proactively inform the user** before proceeding.

Pure static assets (plain HTML/JS/CSS) can also be deployed — the project root is used as the output directory by default.

## Critical: Login Authentication

Before any deploy or link command, authenticate with `iga login`. The login method depends on the environment:

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

All `iga` commands must run **inside the project root**. Scaffolding tools (`create-next-app`, `npm create vite`, `hugo new site`, etc.) create a subdirectory — you **must `cd` into it** before any `iga` command:

```bash
npx create-next-app@latest my-app --yes
cd my-app && iga pages deploy --name my-app
```

## Quick Reference

```bash
npm i -g @iga-pages/cli

iga login                         # local IDE: opens browser
iga login --accessKey <AK> --secretKey <SK>  # remote/headless: AK/SK login

## new project
iga pages deploy --name <my-app>   # deploy (auto-creates project on first run)
## project already linked
iga pages deploy

iga pages link                     # link to existing project without deploying
iga pages dev                      # local dev server
iga pages build                    # build for production
```

- **deploy** auto-detects GitHub remote → Git deploy; otherwise → upload deploy. Only GitHub is supported for Git integration.
- If deploy output includes a preview URL with `?iga_token=...&iga_time=...`, share that **full** URL (query included); omitting it can break access.

## Anti-Patterns

**CLI**

- Running `iga` commands outside the project directory → always `cd` into the scaffolded subdirectory first
- Deploy without login → always `iga login` first
- Committing `.iga/` → it's auto-gitignored, don't remove the entry
- `provider: "upload_v2"` with GitHub remote → delete `.iga/project.json` and redeploy to switch to Git deploy
