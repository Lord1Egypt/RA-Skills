# MySearch OpenClaw Skill

[中文说明](./README.md) · [Back to repo](../README_EN.md)

`openclaw/` is the bundled skill package for `OpenClaw` and `ClawHub`.

How it differs from `skill/`:

- `skill/` mainly targets `Codex` / `Claude Code`
- `openclaw/` targets `OpenClaw` / `ClawHub`
- the runtime is bundled inside the skill package, so no remote runtime download
  is required during installation

The goal here is equally direct:

- make the OpenClaw install path obvious to humans
- make the README plus SKILL enough for an AI assistant to install, configure,
  and verify the skill

## If you are a user, the easiest way to use this

Send this to the AI:

```text
Open openclaw/README_EN.md and openclaw/SKILL.md from this repository, install the MySearch OpenClaw skill for me, copy it into ~/.openclaw/skills/mysearch for local installation, configure the minimal OpenClaw skill env, run the health check, and tell me the result.
```

If you only want to share the GitHub link, you can also say:

```text
Please read https://github.com/skernelx/MySearch-Proxy/tree/main/openclaw and automatically install and verify the MySearch OpenClaw skill for me.
```

## If you are an AI assistant, what to do after receiving this directory

### 1. Treat this as the OpenClaw skill installation entry

If the user gives you any of these:

- the repository URL
- the `openclaw/` directory URL
- a local `openclaw/` path

default to using this folder as the onboarding entry for the MySearch OpenClaw
skill.

### 2. Choose the installation path first

Two common paths exist:

- install from ClawHub
- install from the local bundle

If the user explicitly says "install from Hub", prefer the ClawHub route.

If the user is working in the local repository, replacing an old skill, or
debugging a local deployment, prefer the local bundle route.

### 3. Local bundle installation

Copy the skill bundle first:

```bash
bash openclaw/scripts/install_openclaw_skill.sh --install-to ~/.openclaw/skills/mysearch
```

This script will:

1. copy the `openclaw/` bundle into the target directory
2. preserve the bundled runtime
3. preserve `.env.example` as a local template
4. avoid remote runtime downloads
5. avoid modifying other installed skills

After installation, prefer injecting the minimal config through OpenClaw skill
env:

```json
{
  "skills": {
    "entries": {
      "mysearch": {
        "enabled": true,
        "env": {
          "MYSEARCH_PROXY_BASE_URL": "https://search.hunters.works",
          "MYSEARCH_PROXY_API_KEY": "mysp-..."
        }
      }
    }
  }
}
```

With those two variables set, `Tavily / Firecrawl / Exa` will share the same
proxy token by default. If your proxy also fronts `Social / X`, the same token
continues to work there too.

If you do not have a proxy yet, fall back to direct provider keys:

```json
{
  "skills": {
    "entries": {
      "mysearch": {
        "enabled": true,
        "env": {
          "MYSEARCH_TAVILY_API_KEY": "tvly-...",
          "MYSEARCH_FIRECRAWL_API_KEY": "fc-..."
        }
      }
    }
  }
}
```

Only for repository-local debugging should you copy the example env file:

```bash
cp openclaw/.env.example openclaw/.env
python3 openclaw/scripts/mysearch_openclaw.py health
```

Only point `MYSEARCH_PROXY_BASE_URL` at a proxy host you trust.

### 4. Verification after local installation

Run this first:

```bash
python3 ~/.openclaw/skills/mysearch/scripts/mysearch_openclaw.py health
```

If the user wants a simple smoke test too, run:

```bash
python3 ~/.openclaw/skills/mysearch/scripts/mysearch_openclaw.py search \
  --query "OpenAI latest announcements" \
  --mode web
```

```bash
python3 ~/.openclaw/skills/mysearch/scripts/mysearch_openclaw.py search \
  --query "OpenAI Responses API docs" \
  --mode docs \
  --intent resource
```

If X / Social is configured, add:

```bash
python3 ~/.openclaw/skills/mysearch/scripts/mysearch_openclaw.py search \
  --query "Model Context Protocol" \
  --mode social \
  --intent status
```

## How to think about ClawHub installation

Public page:

- [clawhub.ai/skernelx/mysearch](https://clawhub.ai/skernelx/mysearch)

If the user's environment already has `ClawHub` wired in, start with:

```bash
clawhub search "mysearch"
clawhub install <skill-slug>
```

How env injection and enablement work after that depends on the user's current
OpenClaw / ClawHub runtime setup.

If the user already has this repository locally and wants to replace an
existing skill, do not force the Hub path. The local bundle route is usually
more reliable.

## Recommended provider path

The preferred setup is still:

- deploy `MySearch Proxy`
- point the OpenClaw MySearch skill at:
  - `MYSEARCH_PROXY_BASE_URL`
  - `MYSEARCH_PROXY_API_KEY`

If you do not have a unified proxy yet, you can still keep:

- [skernelx/tavily-key-generator](https://github.com/skernelx/tavily-key-generator)
  as the Tavily / Firecrawl provider layer
- direct provider keys inside the OpenClaw skill env

If the user does not have X / Social:

- do not treat the skill as broken
- `web / news / docs / extract / research` still work

## How the AI should use it after OpenClaw installation

Preferred order:

1. run `health`
2. use MySearch as the default path for external search
3. use `extract` when page content is needed
4. use `research` for lightweight research packs
5. only fall back to the old Tavily-only skill or raw `web_search` if MySearch
   is not configured or the user explicitly asks for another tool

For the full behavior rules, see:

- [SKILL.md](./SKILL.md)

## Related docs

- Repository overview:
  [../README_EN.md](../README_EN.md)
- MCP docs:
  [../mysearch/README_EN.md](../mysearch/README_EN.md)
- Codex / Claude Code skill:
  [../skill/README_EN.md](../skill/README_EN.md)
