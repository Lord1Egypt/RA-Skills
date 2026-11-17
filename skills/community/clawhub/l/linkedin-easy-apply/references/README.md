# LinkedIn Automation (OpenClaw skill)

Automates LinkedIn Easy Apply job sprints: login verification, job search, AI-answered
application questions, submission logging, and optional hiring-team connection requests.

This package contains only the OpenClaw skill definition ([SKILL.md](SKILL.md)) — no
implementation code. The automation itself runs as a separately distributed Python
runtime that you install once, outside of ClawHub.

## Setup

The runtime is installed manually, once, before you ever ask the agent to run a sprint —
this skill never downloads or executes anything itself.

1. Get the `linkedin-automation-runtime-<version>` archive and its published `.sha256`
   digest from the maintainer's canonical release source: the GitHub Releases page of this
   project's repository (the same repository this skill package ships from) — never a
   third-party mirror, forum link, or unofficial re-upload, even if it claims to host the
   same archive. Prefer a specific pinned version over "latest" — treat any archive without
   a published digest, or one obtained from anywhere other than that canonical release page,
   as untrusted and do not install it.
2. Verify the archive **before** extracting it — a `cli.py` file existing inside is not
   itself a trust signal, only a shape check:
   ```
   # Windows
   Get-FileHash linkedin-automation-runtime-<version>.zip -Algorithm SHA256

   # macOS / Linux
   sha256sum linkedin-automation-runtime-<version>.zip
   ```
   Compare that output against **two independent sources**, not just one:
   - the `.sha256` file published next to the archive, and
   - `expectedRuntimeSha256` in this skill's own `SKILL.md` frontmatter.

   These two are published through separate channels (the runtime's own distribution point
   vs. this skill package, reviewed and distributed through ClawHub) — a `.sha256` file
   sitting beside the archive proves nothing on its own if that whole channel is
   compromised, since an attacker who can swap the archive can swap the file next to it too.
   Only trust the archive if it matches **both**. If either doesn't match, stop — do not
   extract or run anything from that archive, and do not proceed assuming it's a stale-pin
   issue on the skill's side.
3. Extract it, then run its installer yourself:
   ```
   # Windows
   pwsh install.ps1

   # macOS / Linux
   ./install.sh
   ```
   This installs the runtime's Python dependencies and the Playwright Chrome browser the
   automation drives. Review `install.ps1`/`install.sh`/`requirements.txt` yourself before
   running them if you don't already trust the source you got the archive from.
4. Either set `LINKEDIN_AUTOMATION_RUNTIME_DIR` to the extracted runtime's path, or move it
   to `~/.openclaw/workspace/linkedin-automation-runtime/` (the skill's default search
   path). Use an absolute path you control — not a shared or world-writable directory,
   and not a symlink to one.
5. Configure the runtime: copy its `.env.example` to `.env` and set `ANTHROPIC_API_KEY` at
   minimum. See the runtime's own `README.md` for the full settings reference.

You do not need to hash `cli.py` yourself — the agent re-verifies it against
`expectedCliSha256`, a value pinned in this skill's own reviewed `SKILL.md` frontmatter at
build time, before every invocation. A hash generated locally from whatever `cli.py` is
present after extraction wouldn't prove anything about that file's origin; pinning it in the
skill package instead means the expected value comes from a channel the runtime directory
itself can't influence.

The runtime drives a dedicated Chrome profile (`CHROME_PROFILE_DIR`) that holds your live
LinkedIn session cookies — treat that profile directory as sensitive, the same as a
password store, and keep its filesystem permissions restricted to your own user.

The runtime's only expected network destinations are `linkedin.com`/`www.linkedin.com` (the
browser automation) and `api.anthropic.com` (AI-answered questions, via `ANTHROPIC_API_KEY`).
If your environment supports outbound network allowlisting, restrict the runtime to those
two hosts — traffic to anywhere else means something other than the documented automation is
running.

Once installed, ask your OpenClaw agent to start or resume a LinkedIn application sprint —
this skill tells it how to find and drive the already-installed runtime, and will ask you to
confirm before it submits any application.

## License

MIT-0 for this skill package. The separately distributed runtime has its own license terms.
