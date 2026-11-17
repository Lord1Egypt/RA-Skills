# Contributing

Development process for this repository. This is not skill knowledge — an agent
sending a message does not need any of it. See [SKILL.md](SKILL.md) for that.

## Changing the skill

Use the normal Git/PR lifecycle. Do not commit to `main` directly.

1. Start from the current `main` and create a focused branch, e.g.
   `docs/update-authentication`.
2. Make the change and validate it.
3. Commit and push the branch.
4. Open a PR with `gh pr create`, summarising the change and how it was verified.
5. Merge only after the user explicitly approves. A concise "merge" is sufficient
   authorization. Use a squash merge, delete the feature branch, then verify the
   PR state and branch deletion with `gh`.

Documentation-only changes, including README updates, follow the same path.
Branch, validate, push, open a PR, leave it for review.

## Verifying a PR before reporting it

Test the exact remote revision, not a local copy that might differ:

```bash
gh pr view <number> --json headRefOid
git switch -c pr-<number> <sha>     # non-tracking branch at the verified SHA
```

A non-tracking branch is the fallback when a shallow clone's fetch refspec
prevents `gh pr checkout` from setting up tracking.

Then run, at minimum:

```bash
bash containers/build.sh                 # all four variants
bash containers/test/default.sh          # no external exposure
bash scripts/doctor.sh                   # environment verdict
```

The container suite covers script behavior, refusal paths, and dependency
detection. It is **not** authoritative for latency — see
[containers/README.md](containers/README.md).

Tunnel behavior is opt-in because it genuinely exposes a browser:

```bash
LINE_OA_TEST_ALLOW_TUNNEL=1 containers/test/tunnel.sh 60
```

A change touching the send path additionally needs a no-send dry run against a
real authenticated LINE UI, which the credential-free container cannot provide.

## GitHub CLI authentication

Run `gh auth status` in the same OS user and runtime that will run the commands.
A browser session or a CLI login in another shell does not authenticate this one.

If auth is missing:

```bash
gh auth login --hostname github.com --git-protocol https --web
```

When the user asks you to "just run it and give me the code", run the flow and
reply with only the one-time device code and `https://github.com/login/device`.
No extra explanation. Wait for their authorization, then confirm with
`gh auth status`.

## Publishing

`.github/workflows/publish-clawhub.yml` publishes to ClawHub on tag push. It
publishes the repository root, so `references/` and `containers/` ship with the
skill. Broken relative links reach consumers — check them before tagging.

The workflow needs `CLAW_HUB_TOKEN` in the repository's Actions secrets.

## Making the repository public

See [the public repository checklist](references/public-repository-checklist.md)
for the full audit, settings, and verification sequence. Audit **all reachable
history**, not just the current files.

## Repository layout

| Path | Purpose |
| --- | --- |
| `SKILL.md` | What an agent needs to decide and act |
| `README.md` | What a human evaluating or operating the tool needs |
| `scripts/` | The implementation |
| `scripts/lib/` | Shared shell libraries |
| `references/` | Depth material, read on demand |
| `containers/` | Linux test environment and its suites |
| `openspec/` | Change proposals, designs, specs, and tasks |
