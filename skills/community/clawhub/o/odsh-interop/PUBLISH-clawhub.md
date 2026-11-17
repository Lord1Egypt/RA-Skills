# Publishing odsh-interop to ClawHub

> This skill is the **OpenClaw-side brain** of ODSH Bridge. Publishing it to ClawHub makes
> it one-command installable for any OpenClaw operator.

## Prerequisites
- A machine where the **`openclaw` CLI** is available (the OpenClaw container or the Windows
  host that runs it — **not** the DSH container, which has no CLI).
- You are logged in to ClawHub on that machine (`openclaw login` if required).
- `SKILL.md` frontmatter carries the ClawHub-required fields: `name`, `description`,
  `version`, `author`, `author_email`, `maintainers`, `license`, `tags`, `categories`,
  `when_to_use`.

## Steps

```bash
# 1. dry-run first (validates frontmatter + local checks without publishing)
openclaw skills publish --dry-run

# 2. real publish from the skill dir (adjust path to wherever SKILL.md lives)
cd <dir-containing-SKILL.md>
openclaw skills publish

# 3. verify the published artifact matches by re-pulling
openclaw skills install odsh-interop --force   # or the hub-install equivalent
openclaw skills list | grep odsh-interop
```

## Keep in sync
- Bump `version` in the frontmatter on **every** protocol change and re-publish.
- The bridge repo also carries a pristine copy at `skills/odsh-interop/SKILL.md`; keep the
  ClawHub copy in lock-step with it.

## Typical failure modes
- **Missing/invalid frontmatter** → dry-run will flag it; fix and retry.
- **Not logged in / no registry scope** → run `openclaw login`; ClawHub publishing may need
  the same permission the GitHub push used.
- **Semver conflict** → don't reuse an already-published `version`; bump it.