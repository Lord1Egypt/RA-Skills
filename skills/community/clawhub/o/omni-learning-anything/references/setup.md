# Runtime setup

All routes require Python 3.10+ and a host that researches sources, runs/files, inspects the chosen document and handles learner dialogue. The skill does not include an LLM, web-search subscription, image model, scheduler or cloud authorization. New courses select their output explicitly.

Check the interpreter version first: macOS may resolve `python3` to an older system version. Use an installed supported interpreter and an isolated environment.

## Install only the selected route's dependencies

The agent first runs `omni_learning.py setup-check --platform SELECTED --mode SELECTED_MODE` with a supported interpreter. Its `pip_argv` installs only actual missing packages for that route; re-run the recipe in the chosen external environment. The broad requirements files below are convenience bundles, not mandatory for HTML/Markdown/Vault. Hosts without an OS IANA timezone database need tzdata even for these routes; the recipe detects this condition. Installation itself never grants native discovery or cloud authorization. Keep the environment outside the installed bundle and course approval files.


```sh
python3 -m venv /outside-skill/omni-env
# HTML / Markdown / DOCX / cloud / Obsidian (no PDF packages or TeX):
/outside-skill/omni-env/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements-documents.txt
# PDF, or repository development including PDF regression tests:
/outside-skill/omni-env/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements.txt
# Tencent legacy application API route additionally needs the official COS SDK:
/outside-skill/omni-env/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements-tencent.txt
# Tencent official OAuth/MCP default route:
/outside-skill/omni-env/bin/python -m pip install -r /installed/omni-learning-anything/scripts/requirements-tencent-mcp.txt
/outside-skill/omni-env/bin/python /installed/omni-learning-anything/scripts/omni_learning.py --project /course doctor
```

Windows: choose an external environment folder, for example `py -3 -m venv C:\OmniRuntime`, then use `C:\OmniRuntime\Scripts\python.exe`. Select current host commands; offline installation is not promised. Standard-library Markdown/Vault export can run without DOCX/HTTP/PDF libraries; images must already be valid local PNG/JPEG. DOCX lazily imports python-docx/Pillow; API routes lazily import requests, and Tencent imports the COS SDK only when an actual upload is needed.

DOCX: render using an available approved viewer/converter and inspect all pages. Bundled generation embeds Chinese text, images, source links and image descriptions; the viewer's font availability affects rendering. Prefer FangSong/Times New Roman when available; do not install proprietary fonts or promise identical cloud fonts.

Markdown: use the generated local HTML preview plus the source/asset links. Obsidian: inspect the real Vault note and figure. Cloud: inspect the populated native document and verify learner access. Missing viewers/access require a truthful limitation; a successful API request is not visual inspection.

Secrets stay outside installed/course/repository files. API scripts consume only named environment variables, never raw JSON secrets or authentication headers returned to chat. For DingTalk use authorized official `dws`; host/UI routes require actual document tools and may not work unattended.

## Official cloud tools

For new Notion/Feishu courses, follow [onboarding](onboarding.md). The agent checks existing writable official API tools and installs only the selected official CLI when needed. Inspect current official runtime requirements/help first, use an isolated install when appropriate, and report the executable path/version. Do not automatically change global host defaults.

Notion: [official installation](https://developers.notion.com/cli/get-started/installation), npm package `ntn` (inspected 0.23.25; Node 22+/npm 10+). Feishu: [official larksuite/cli](https://github.com/larksuite/cli), `npx @larksuite/cli@latest install` or the matching official release (inspected 1.0.98). Check package origin/platform; verify published checksums for downloaded binaries. Ensure the actual scheduled host sees the same binary/profile/credential context.

Upstream CLIs own authentication and secure storage. Never export a token for the adapter, inspect private CLI stores, disable keychain storage silently, or install a community credential plugin as a replacement. A missing keychain is a concrete setup blocker or requires an explicitly configured private API credential alternative. The helper does not embed a hosted OAuth service. Tencent and DingTalk retain their selected provider's official API/CLI prerequisites.

## XeLaTeX

First check PATH, then existing TinyTeX installations. The renderer recognizes PATH, macOS `~/Library/TinyTeX/bin/*`, Linux `~/.TinyTeX/bin/*` and `/Library/TeX/texbin`. Other locations may be added to PATH. It never uses an HTML/reportlab fallback under the label "LaTeX PDF".

Install from official distributions within the user's existing authorization:
- macOS: MacTeX or TinyTeX; official guide https://yihui.org/tinytex/ and https://www.tug.org/mactex/ .
- Linux: distro packages (Debian/Ubuntu: `texlive-xetex texlive-lang-chinese texlive-fonts-recommended texlive-latex-extra`) or TinyTeX.
- Windows: MiKTeX https://miktex.org/download or TeX Live https://tug.org/texlive/ ; reopen the shell so PATH is refreshed.

For TinyTeX/TeX Live, install missing packages with its `tlmgr`: `xelatex fontspec xecjk fandol tex-gyre geometry xcolor graphics enumitem fancyhdr titlesec hyperref`. A distribution's own package manager may be required; do not mix incompatible system and user TeX trees. Respect managed-device restrictions and report the exact blocked requirement.

The template detects FangSong / 仿宋 / FandolFang-Regular, then FandolSong-Regular; Times New Roman then TeX Gyre Termes. FandolFang is an open FangSong family supplied by TeX Live. No proprietary font is redistributed. The generated manifest records actual PDF font names; verify that report and the rendered text.

Run `doctor`, then compile the first actual plan. A binary's presence alone does not prove required packages/fonts work. Every page is rendered with pypdfium2; image review remains an agent responsibility.

For selected-format dependencies, host capabilities, scoped foreground/background evidence and first-use observations, read [readiness](readiness.md). Use `doctor --config /private/staging/config.json` before initialization; do not install PDF dependencies for HTML/Markdown/DOCX. An unknown host capability needs a real check, not an invented success status.

## macOS bundled preview font discovery

If a bundled LibreOffice preview drops Chinese despite intact DOCX text, verify font discovery before changing the document. Use a temporary process-local `FONTCONFIG_FILE` that exposes existing read-only host font directories and a writable task cache; do not modify global settings, runtime binaries or redistribute fonts. The authoring code selects an available CJK family when Fontconfig is present, or declares a platform CJK family for the destination viewer. Rendering inspection is still required. This local preview issue was reproduced and resolved during v2 QA; upstream context: https://github.com/openai/codex/issues/32968 .

## Ten-language output and offline HTML

Course language codes: en, zh, ja, ko, es, fr, de, pt, ru, ar. Author actual teaching content in that language before rendering. HTML/Markdown need only the Python standard library; HTML embeds its PNG/JPEG and inline styles in one file, with no external font or JavaScript dependency. Outbound sources still need Internet.

Japanese PDF tries Hiragino Mincho ProN/Noto Serif CJK JP/Yu Mincho/MS Mincho; Korean tries Apple SD Gothic Neo/Noto Serif CJK KR/Malgun Gothic/Batang. Arabic additionally needs TeX `polyglossia` and `bidi`, with Amiri/Noto Naskh Arabic/Geeza Pro/Arial Unicode MS, and uses RTL with Latin citations isolated. Ensure at least one appropriate font is installed through an official/free distribution; missing fonts/glyphs stop publication. CJK fallback uses the distribution’s Fandol font for mixed Chinese references. DOCX declares appropriate script fonts and RTL properties; inspect actual pages because viewer font substitution differs.

## Input-material dependencies

See [materials](materials.md) for supported formats and limits. TXT/Markdown/HTML/DOCX/EPUB/PPTX/SRT/VTT readers use the Python standard library. Text PDF imports lazily require pypdf; they do not require XeLaTeX or PDF rendering libraries. DOC/RTF uses an existing trusted textutil/antiword converter; absence is a conversion requirement, not success. Do not install OCR/GPU/vector databases for ordinary text inputs. Host tools obtain webpage snapshots; no background web fetch or audio/video transcription is bundled.

For text-PDF input alone, install `scripts/requirements-materials-pdf.txt` in the selected interpreter. This does not require XeLaTeX, pypdfium2 or output-PDF setup. Previously imported snapshots can be read without re-running the parser.
