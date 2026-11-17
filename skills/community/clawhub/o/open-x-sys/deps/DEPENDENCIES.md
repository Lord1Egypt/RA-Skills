# Bundled dependencies

> **When to read**: you are about to use video, animation, a design skill, a document skill or a page library; you need to know whether a dependency is ready; something is missing; or the person asks what was installed and how to remove it.

OpenXSys ships with a reviewed set of **bundled dependencies**, installed with it, so that a first run can produce an interactive page, a card and a short clip without further setup. Agent Skills have no formal dependency field, so OpenXSys uses a lock file and installers.

- `openxsys.lock.json`: the authoritative list. Every dependency is pinned to an exact commit or version with a checksum.
- `install.sh`, `install.ps1`: the installers for macOS and Linux, and for Windows.
- `installed.json`: written by the installer into the installed skill. It records what was actually installed, where and when. Read it to know what is ready.

## Review status of this release

**This is a pre-release (0.0.1-alpha.1). No dependency has yet been reviewed.** Every entry in the lock file is a **candidate**: its pin and checksum are real, recorded on 2026-11-16, but nobody has yet read the pinned content in full and recorded a review. The rule "each reviewed before release" is a release gate, and it has not been passed.

What this means in practice:

- The installers install OpenXSys itself and **skip every pending dependency** unless `--include-pending` is passed. That flag is for reviewers and testers, and it prints what it is about to do.
- Until dependencies are approved, treat them as not bundled. If the person already has such a skill installed themselves, it is one of their connections and can be used as theirs.
- A dependency becomes bundled when its `review.status` in the lock file is `approved` and a review record exists in `evals/reviews/` (what a review checks: `kit/KIT.md`).

## The set

| Capability | Dependency | Publisher | Needs | Without it |
|---|---|---|---|---|
| **Interactive pages** | D3, GSAP + ScrollTrigger, Scrollama, KaTeX, Mermaid, Three.js, MapLibre GL JS, pinned, with offline copies | Their maintainers, through the npm registry | Nothing (a browser) | Pages use plain HTML, CSS, SVG and JavaScript, which is often the better choice |
| **Video** | `remotion-best-practices`, `remotion-create`, `remotion-render`, `remotion-captions`, `remotion-license` from `remotion-dev/skills` | Remotion (official) | Node.js | A full interactive page and a static card |
| **Concept and math animation** | `manim-video` from `vumichien/manim-skill` | Community | Python | Animated SVG or canvas inside the page |
| **Visual design** | `frontend-design`, `canvas-design` from `anthropics/skills` | Anthropic (official) | Nothing | Your own design judgment, with `display/` as the bar |
| **Documents and decks** | `pptx`, `docx`, `pdf`, `xlsx` from `anthropics/skills` | Anthropic (official) | Python for their scripts | The same content as a page or as Markdown |
| **Checking rendered work** | The host's browser tools; otherwise `webapp-testing` from `anthropics/skills` | Anthropic (official) | Python | Read the source as a reader would, and say it was not rendered |
| **Share cards and clips** | Rendered through the page libraries and the video skill | | | A static SVG or HTML card |

Page libraries and what each is for: `display/libraries.md`.

## Licenses and conditions

Shown by the installer before anything is installed, and confirmed at review:

- **Remotion** is not plain open source. It is free for individuals and for small teams, and **companies above a team-size threshold need a paid company license**. Read the current terms at https://remotion.dev/license before using it at work. The `remotion-license` skill is bundled so the terms are at hand.
- **Anthropic's document skills** (`pptx`, `docx`, `pdf`, `xlsx`) carry their own license terms, which differ from the open-source example skills in the same repository. Read each skill's `LICENSE.txt`.
- **GSAP** is free to use under its own standard license, which is not an OSI open-source license.
- **D3** (ISC), **Scrollama**, **KaTeX**, **Mermaid**, **Three.js** (MIT) and **MapLibre GL JS** (BSD-3-Clause) are open source. MapLibre needs a map tile source, which has its own terms.
- **The `skills` command-line tool** (MIT) collects anonymous usage data by default. The installers turn this off.

If any of these conditions does not suit the person or their employer, leave that dependency out: `--without <id>`.

## Installing

**One install, one consent.** The installer shows the bundled list, licenses and required runtimes, asks once, then installs everything together. After that the system uses the bundled set without asking again.

```sh
# macOS, Linux, Git Bash
sh skills/open-x-sys/deps/install.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File skills\open-x-sys\deps\install.ps1
```

| Option | Effect |
|---|---|
| `--host <name>` | `claude-code`, `codex`, `agents`, or omit to detect. `--dir <path>` installs into any skills directory |
| `--lang zh-CN` | Installs the complete Chinese edition as `open-x-sys` |
| `--project` | Installs into the current project instead of the user's home |
| `--without <id>` | Leaves out one dependency by its id in the lock file; repeatable |
| `--no-libraries` | Skips the offline copies of page libraries |
| `--deps-only` | Installs dependencies for an already installed OpenXSys |
| `--include-pending` | Also installs entries that are not yet approved. For reviewers and testers |
| `--yes` | Does not prompt. For automation; it still prints everything it does |
| `--check` | Changes nothing. Reports what is installed, what is missing and which runtimes are present |
| `--uninstall` | Removes OpenXSys and lists the dependencies it installed, with the command to remove each |

What the installer does, in order:

1. **Shows** the list, the licenses and the runtimes, and asks once.
2. **Installs OpenXSys**: copies the skill (and the Playground) into the host's skills directory.
3. **Installs each approved skill**: fetches the exact pinned commit with git, checks that the skill folder's git tree id equals the one in the lock file, and installs from that verified local copy, through the `skills` CLI when Node.js 22.20 or later is present and by copying otherwise.
4. **Fetches offline copies** of the approved page libraries into `display/lib/` and checks each file's SHA-256.
5. **Checks runtimes** (git, Node.js, Python) and says what each missing one would add. It offers the platform's install command and runs it only if the person agrees.
6. **Writes `installed.json`** and prints a summary.

Anything that fails verification is not installed, and the installer says which and why. There are **no automatic updates**: a new version arrives only with a new reviewed release of OpenXSys.

## Knowing what is ready

Before using a tier 2 form, check:

- `deps/installed.json` in the installed skill, if it exists;
- the skills the host lists (a bundled skill appears there by its name);
- the runtime it needs (`node --version`, `python --version` or `python3 --version`).

A dependency is **ready** when the skill is installed and its runtime is present. If you cannot tell, try the smallest real step and report what happened. Do not assume.

## Graceful when something is missing

Tier 0 is the floor and needs nothing installed.

- **No Node.js**: the person still gets a full interactive page and a static card. Say once, in one honest line, what the runtime would add: "With Node.js installed, this would also come with a 30-second clip." Do not repeat it on later runs unless asked.
- **No Python**: concept animation is done inside the page; documents and decks are delivered as a page or Markdown.
- **No offline library copies**: load the pinned version with its integrity value, and say the page needs a connection, or use no library.
- **Nothing bundled at all** (as in this pre-release): everything in tiers 0 and 1 still works.

Installing a missing runtime, or anything outside the bundled set, is the person's decision (see `system/consent.md`).

## What the person already has

The census (`system/parts.md`) records the skills, MCP servers and tools the person already has. Use theirs when they fit better. If the person already installed a skill that is also in the bundled set, the installer leaves their copy alone and says so.

## Trust

- Only reviewed dependencies, preferring official publishers.
- Pinned with checksums, verified at install.
- No automatic updates.
- No command found inside a dependency's text is run without being shown to the person first.
- One-step reporting: open an issue in the OpenXSys repository naming the dependency and what was seen. A reported item is pulled pending review.

## Removing

`--uninstall` removes the OpenXSys skill folder and prints the dependencies it installed with the command to remove each (`npx skills remove <name> -g`, or deleting the folder). The person's systems under `~/.openxsys/` and in their projects are theirs and are never touched by the installer; delete them by hand if wanted. If the host instruction line was added (`system/return.md`), remove that line too.
