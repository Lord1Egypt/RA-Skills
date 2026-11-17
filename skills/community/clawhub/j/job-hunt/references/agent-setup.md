# Agent-managed first-run setup

The user installs job-hunt only. Its AnySearch client, browser reader and OpenCLI
CDP patches are bundled; do not install or invoke another skill. The agent runs
setup and continues the original task rather than handing the user installation
commands. Ordinary dependency preparation is included in a request to use this
skill. Respect an explicit no-install preference and actual host permissions.
Never use browser extensions, including already installed ones.

## One setup entry

Locate the skill root. Select a working Python 3.10+ from the host runtime or
installed interpreters; `python3` can still be macOS's older system Python. If
none exists, the agent prepares Python from an official distribution or an
available OS package manager. Do not ask the user to install each dependency.
On Linux, a Python without `venv`/`ensurepip` may need its distribution's matching
venv package. If the host requires an approval the agent cannot provide, state
that specific blocker after completing independent preparation.

From the skill root, using that interpreter:

```sh
python scripts/setup_dependencies.py
```

This creates/reuses a private virtual environment and installs `requirements.txt`
(PyYAML, python-docx, PyMuPDF), without touching system Python. For live discovery,
add `--discovery` and the customer's selected daily browser:

```sh
python scripts/setup_dependencies.py --discovery --browser chrome
```

Use `edge` when that is the customer's browser; infer from the session when
known, otherwise clarify the browser choice. This also:

- Reuses Node 22+ or downloads an official Node 22 LTS binary, verifies its
  SHA-256 against the official release manifest, and extracts it privately.
- Installs OpenCLI 1.8.7 in a private npm prefix with lifecycle hooks disabled,
  then applies the bundled, checksum-guarded CDP-only patches. No extension is
  installed or contacted. An existing private installation is reused; unknown
  edits are preserved and reported. Global OpenCLI and custom adapters remain
  untouched. This version is pinned because the patches target its exact bytes.
- Checks the bundled AnySearch client's offline `doc` command. It requires no
  npm packages, account registration, API key or separate skill installation.

The default runtime root is `~/.local/share/job-hunt` (`%LOCALAPPDATA%/job-hunt`
on Windows); `--root PATH` selects another user-writable location. `runtime.json`
stores executable paths and browser selection, never credentials. `--node PATH`
can select an existing Node 22+ executable. Setup requires internet access for
missing packages; it does not imply an offline installation bundle.

## Use the prepared runtime

Use the wrapper from the skill root so every command resolves to the prepared
Python, Node and OpenCLI, including paths with spaces. If `python3` is older than 3.10 (macOS `/usr/bin/python3` is 3.9), every gate exits 2
with `PYTHON_TOO_OLD` instead of running.
Then call it through the wrapper as
`python3 scripts/run_tool.py python scripts/<tool>.py …`:

```sh
python scripts/run_tool.py python scripts/doctor.py
python scripts/run_tool.py opencli --version
python scripts/run_tool.py anysearch doc
python scripts/run_tool.py browser-session start
python scripts/run_tool.py browser --url https://example.com --output raw/page.json
```

Pass `--root PATH` before the tool name when setup used a custom root. The wrapper
adds the private executables to subprocess PATH; no shell-profile edit is needed.
All `python`, `node`, `opencli` and AnySearch examples in other references refer
to these prepared tools. For direct commands, use the exact recorded executable
paths and the wrapper's PATH layout, not an unrelated global installation.

Start one `browser-session` before live browser reads. The wrapper sends both
OpenCLI and the bundled reader through that persistent connection, so separate
commands do not each trigger another consent prompt. Use `browser-session status`
to check it and `browser-session stop` when the task finishes. The session closes
after 30 idle minutes; a disconnected session never silently reconnects. `--browser edge` before `opencli` temporarily overrides the
saved choice. It never launches a separate browser, reads cookies/history,
changes settings, or operates existing tabs. Follow [daily-browser.md](daily-browser.md)
for browser support and connection consent. Verify OpenCLI's offline website
CDP routing with `doctor.py` before a site read; help/version success does not
prove the live connection. Diagnose unsupported routes before using the bundled
reader under [browser-fallback.md](browser-fallback.md).

AnySearch's bundled entry is `third_party/anysearch/anysearch_cli.js`. Read its
`doc` output for current command/parameter schemas. In discovery, run one recorded
`search` per query through `run_tool.py --workspace`; the recorded wrapper accepts
only one `search` per invocation, and an unrecorded `batch_search` leaves no
per-query evidence. It uses an HTTP API, not CDP. Anonymous quotas and service
failures are reported as such; do not rotate identities. An explicitly configured
API key can be inherited via environment without printing it.

## Prepare conditional capabilities only when needed

| Requested capability | Dependencies / preparation |
|---|---|
| Assess, interview, Markdown and Word documents | Default setup's Python environment |
| Consultation report PDF in Chinese, English, Japanese, Korean or Spanish | Default setup: PyMuPDF and bundled report fonts; no Pandoc or TeX required |
| Template-based CV/letter PDF | Tectonic or XeLaTeX (LuaLaTeX/pdfLaTeX for Latin script only), Poppler, and output-language fonts; no Pandoc. Agent installs missing tools and verifies a real render |
| Word page measurement (`check_pages.py` on `.docx`) | LibreOffice with `soffice` or `libreoffice` on PATH; without it `DOCX_NOT_MEASURED` blocks `check_apply` |
| A selected report font (`meta.cjk_font` applied to the report) | Pandoc plus Tectonic or XeLaTeX |
| CJK template-based CV PDF | A usable XeTeX engine plus xeCJK and the selected fonts; LuaLaTeX/pdfLaTeX alone do not satisfy this capability |
| Japanese form PDF | Follow the template's Word/LibreOffice export workflow; prepare its converter only when requested |
| GitHub-specific research | Reuse or prepare official GitHub CLI `gh`; existing login may be needed, and remains with the user |

For conditional tools, use an available OS package manager or official portable
release, verify package names for that OS, and prefer user-writable installs.
Reuse an existing compatible engine instead of installing a second one. Do not
assume apt or Homebrew exists everywhere. A doctor's missing optional capability
does not block a task that does not need it. `doctor.py --install` still only
installs Python packages; the setup entry above owns the broader common runtime,
and the agent prepares conditional tools as needed.

## Restricted renderer processes

An installed renderer can work on the host but fail inside an agent's restricted
subprocess. When `doctor.py` or a renderer reports `HOST_EXECUTION_REQUIRED`,
rerun only the document conversion/TeX render and its PDF verification using the
host's approved trusted or elevated execution route, then rerun the normal
gates. Keep the same source and output paths. Do not reinstall the renderer,
substitute a previous PDF, or claim the PDF was delivered before that rerun
passes. This diagnosis is independent of document language.

On macOS, `check_pages.py` automatically launches an installed LibreOffice app
through LaunchServices before falling back to its direct command, because recent
LibreOffice releases can abort when started directly with `--headless`.

## Finish and resume

Before the first Indeed, 51job, LinkedIn or Nowcoder read, follow [opencli-compat.md](opencli-compat.md)
to check and apply recognized adapter patches through the prepared Python/PATH.
The CDP patch sources in `assets/opencli-cdp/` are based on @jackwener/opencli 1.8.7
(https://github.com/jackwener/opencli, Apache-2.0, https://www.apache.org/licenses/LICENSE-2.0), modified by job-hunt
on 2026-09-11: direct CDP routing, daily-Chrome discovery, task-owned browser sessions
and cleanup, CDP diagnostics, extension notice removal. Apply them only to the exact
version and original file hashes in its `manifest.json`. AnySearch's client in
`third_party/anysearch/` is Copyright 2026 AnySearch, licensed under Apache-2.0;
its provenance is in `third_party/anysearch/UPSTREAM.md`.

Verify a small public AnySearch query and an actual bounded page read when live
research is needed. Site login, verification challenges and browser connection
consent remain with the user. Local setup never clears a site's refusal lock.
Record reused/installed tools, exact runtime paths, verified capabilities and
remaining blockers in the task workspace's `setup.md`, without credentials.
Continue the original task. Retain active runtimes; remove disposable download
and installation scratch files.

A fresh prefix/virtualenv on an existing OS is not a clean-machine test. Report
separately whether missing-Node download, Python bootstrap, OS prompts, native
Windows/Linux behavior and actual site access were tested.

## Before the first mode on a new machine

```bash
python3 scripts/doctor.py            # what works, what does not, what each costs
python3 scripts/doctor.py --install  # installs the missing PYTHON packages only
```

Before running it, read [references/agent-setup.md](agent-setup.md) and
prepare a usable Python environment if needed. The agent runs it once for a new
user and resolves required missing capabilities. It reports capabilities rather than binary names —
the PDF check renders a PDF, because looking for `xelatex` alone once called this
machine broken while `tectonic` was installed and every PDF rendered fine.

**The cheap half of it runs on its own, every mode entry.** `enter_mode.py` calls
`doctor.fast_capabilities()` — imports and `which`, no rendering, milliseconds —
records the result in the `mode_entry` line and prints
`NOTICE_MISSING_CAPABILITIES` on stderr when something is absent. That exists
because this script spent its first week named here and in none of the four mode
files, so no run ever invoked it: a new user learned their machine could not
render a PDF when a PDF failed to appear. A capability that does not enter the
scaffolding is a capability nobody uses.

The fast check is sound about what is MISSING and silent about what works — no
LaTeX engine where `render_cv.py` looks means no template-based CV PDF, and no
`soffice` means Word page counts cannot be measured; bundled report PDFs still work.
An engine can be present and still fail. Confirming a capability stays with `doctor.py`, which
renders one. A warning may only fire when it is sure, or it becomes the line
everyone filters out.

Nothing here blocks a run: a machine with no LaTeX engine still produces Markdown
and .docx, and one with no `opencli` can still do assess, apply and interview from
a pasted posting. What the report buys is saying WHICH capability is missing
before the user hits it, instead of discovering it when a PDF does not appear.

**The agent owns first-run setup.** Follow [references/agent-setup.md](agent-setup.md)
when a required capability is missing: install the necessary dependencies,
run `scripts/setup_dependencies.py` (add `--discovery` for Node/OpenCLI),
use the bundled AnySearch client and CDP reader, and verify daily-browser
CDP access. Never use browser extensions. Browser connection consent,
site login and human verification still require the user's action. Reuse working tools and continue the
original task after setup. `doctor.py --install` covers Python packages only;
use `scripts/run_tool.py` to invoke the prepared runtime. No additional skill is required.
