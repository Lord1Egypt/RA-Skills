# Install And Invoke `obclip`

## Install The Codex Skill

When the user wants this skill installed into Codex, use:

```text
Use $skill-installer to install the skill from https://github.com/Rycen7822/obclip-skill/tree/main/skills/obclip
```

After installation, tell the user to restart Codex so the new skill is discovered.

## Install The npm Package

Prefer a global install when the user wants the `obclip` command on `PATH`:

```powershell
npm install -g @harris7/obclip
obclip --help
```

Use `npx` when the user does not want a global install:

```powershell
npx @harris7/obclip --help
```

## Local Source-Repo Fallback

When working directly in the source repo and no global command exists:

```powershell
cd D:\dev\ob-web-clip\obclip
npm run build
node .\dist\cli.cjs --help
```

## Decide Which Invocation To Use

- Use `obclip ...` when the command already resolves.
- Use `npx @harris7/obclip ...` when the package is not installed globally.
- Use `node .\dist\cli.cjs ...` when developing inside the repo.

## Verify Before Clipping

Run one of these before using the tool on a real page:

```powershell
obclip --help
npx @harris7/obclip --help
node .\dist\cli.cjs --help
```
