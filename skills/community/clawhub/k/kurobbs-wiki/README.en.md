# 🌊 kurobbs-wiki — Kuro BBS Wuthering Waves WIKI Query + Team-Building Assistant

> 🌍 **Read this in** · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [中文](README.md)

A universal skill that follows the **Agent Skill open standard** (SKILL.md). It queries the Wuthering Waves gallery, strategy guides, and character profiles directly through the public Kuro BBS (kurobbs) API, and ships with a built-in **mechanism profile + team-building engine**. You can also log in with your own Kuro BBS account and build teams from your real character pool. Works with any AI that can load Agent Skills (Claude, Cursor, Copilot, Gemini, OpenClaw, etc.).

> This project was inspired by the pain point of having to flip through web pages one by one when looking up character strategies and team compositions while playing Wuthering Waves — turning it into a skill lets you just ask directly in conversation.

---

## ✨ Feature Overview

| Module | Command | Description |
|------|------|------|
| 🔍 Catalog / Lists | `tree` / `list` | Categorized catalog tree (170+ nodes) + entries under each category |
| 📖 Entry Details | `detail` | Character/weapon/item/strategy details; supports `--render` Markdown formatting and `--section` for precise section extraction |
| 🔎 Name Search | `search` | Cross-category search that automatically traverses three levels of subcategories |
| 🖼️ Community Post Media | `post` | Bypasses WAF to fetch images, covers, and m3u8 videos from image-first/video posts |
| 🧠 Mechanism Profile | `probe` | 6-dimension mechanism profile (Effect / buff / playstyle / skill / Echo / Weapon) |
| 🤝 Pairing Engine | `pair` / `team` | 5-dimension compatibility scoring between two characters, pool-based team building, full 60-character enumeration, and guide cross-validation to fill the pool |
| 🎯 LLM Re-ranking | `candidates` + `--profile` | Rule-based coarse candidate filtering + LLM per-team fine ranking (most accurate team-building) |
| 👤 My Account | `my` | Log in to Kuro BBS, view your real characters, build teams with your own characters, and renew tokens |

---

## 📦 Installation

### Option 1: Install from a local directory (simplest)

Place this repository's `kurobbs-wiki/` directory into your AI's skills directory (supported by Claude Code, Cursor, Copilot, etc.), or use it in an agent that supports such directories:

```bash
# Point SKILL_DIR to the absolute path of this repository's root
# Windows example
set SKILL_DIR=D:\tools\kurobbs-wiki

# macOS / Linux example
export SKILL_DIR=~/tools/kurobbs-wiki
```

### Option 2: Via npx skills (once it has been added to the marketplace)

```bash
npx skills add Alphamancer/kurobbs-wiki
```

> Once published, it can be installed with one click from the marketplace — see "Publishing & Inclusion" below.

### Dependencies

- **Python 3.8+** (pure standard library; `wikiquery.py` has no third-party dependencies)
- **Playwright** (only needed for `post` to fetch community post media)
  ```bash
  pip install playwright && playwright install chromium
  ```
- **ffmpeg** (optional, used when `--download-video` downloads m3u8 videos as mp4)

---

## 🚀 Quick Start

```bash
cd $SKILL_DIR

# 1. Initialize the catalog tree (cached to ~/.kurobbs-wiki-cache/)
python -X utf8 -u scripts/wikiquery.py tree

# 2. Search for a character
python -X utf8 -u scripts/wikiquery.py search 穗穗 --preview --limit 3

# 3. Fetch a specific section of a strategy guide
python -X utf8 -u scripts/wikiquery.py detail <previewEntryId> --section "编队&队伍轴推荐"

# 4. Mechanism profile + team building
python -X utf8 -u scripts/wikiquery.py probe 穗穗
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3

# 5. Log in to your account and build a team with real characters
python -X utf8 -u scripts/wikiquery.py my login    # enter phone number in browser → drag the slider → enter the verification code
python -X utf8 -u scripts/wikiquery.py my roles
python -X utf8 -u scripts/wikiquery.py my team 穗穗 --guide-pool --top 5
```

> 💡 **Tip**: All commands should be run in the skill directory, and should include `-X utf8 -u` (needed for Chinese/emoji output on Windows).

---

## 🧠 How to Use the Team-Building Engine

### Two-Character Scoring

```bash
python -X utf8 -u scripts/wikiquery.py pair 穗穗 洛瑟菈
```

Each of the 5 dimensions scores 20 points: Effect synergy / Outro Skill match / role complementarity / Echo linkage / trigger loop. ≥80 indicates a highly compatible pair.

### Building a Team from a Character Pool

```bash
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3   # specify a pool
python -X utf8 -u scripts/wikiquery.py team 穗穗 --all --top 5                    # full enumeration of 60 characters
python -X utf8 -u scripts/wikiquery.py team 穗穗 --guide-pool --top 5             # guide cross-validation to auto-fill the pool
```

Each team is labeled with its source: 🟢 confirmed by a strategy guide / 🟡 hybrid / 🔵 engine inference, and includes a 📚 strategy URL you can click to verify.

### LLM Re-ranking (most accurate team-building)

```bash
# Step 1: rule-based coarse filtering of the candidate pool (in seconds)
python -X utf8 -u scripts/wikiquery.py candidates 绯雪 --guide-pool

# Step 2: fetch candidate teams + full 6-dimension profiles for the three characters (large output; redirect to a file)
python -X utf8 -u scripts/wikiquery.py team 绯雪 --pool 千咲,维里奈,穗穗 --profile --top 10 > %TEMP%\team_profile.txt
```

Claude performs a per-team 6-dimension re-ranking based on real profile data, identifying roles that are hard for rules to judge, such as "mechanism anchor" and "concerto sub-DPS".

---

## 🔐 Privacy & Data Notes

> ⚠️ **Please read this** — this skill includes a login feature that reads your account data.

- **WIKI queries (`tree`/`list`/`detail`/`search`/`probe`/`pair`/`team`)**: all use **public, unauthenticated** APIs, **no login required**, and involve no personal data.
- **"My Account" feature (`my login`/`my roles`/`my team`/`my sync`)**: requires you to actively log in to Kuro BBS in your browser. After logging in, the following data is **stored locally** in `~/.kurobbs-wiki-cache/`:
  - `account.json` — login token + your character list
  - `role_details/` — each character's Resonance Chain unlocks, actual weapon/Echo, skill levels, and stats
- **This data is stored only on your local machine and is never uploaded to any server**. The token expires in about 45 minutes; `my renew` can refresh it.
- This skill **will not** guess or fabricate your account characters when not logged in, nor will it send your account data to any third party.

**If you want to stay fully offline / not log in**: just use `tree`/`search`/`detail`/`probe`/`pair`/`team` — the `my` command family is not needed at all.

---

## 📚 Directory Structure

```
kurobbs-wiki/
├── SKILL.md               # Skill instructions (trigger conditions, command quick reference, workflow, key pitfalls)
├── README.md              # This file (for users)
├── PUBLISHING.md          # Publishing checklist (for authors; users don't need to read it)
├── _meta.json             # skill metadata
├── references/
│   └── catalogue-map.md   # Category ID mapping quick reference (170+ nodes)
└── scripts/
    ├── wikiquery.py       # Main CLI (tree/list/detail/search/probe/pair/team/candidates/my), pure standard library
    ├── post_fetch.py      # Community post media fetching (Playwright to bypass WAF)
    └── kuro_login.py      # Kuro BBS login (browser interaction)
```

---

## ⚠️ Known Limitations

- **Private API, no official documentation**: the field structure may change as Kuro BBS updates; when you hit an error, run `tree --refresh` to re-pull the catalog tree first.
- **Use at low frequency**: these are public unauthenticated interfaces, and frequent requests may trigger risk control; the script has a built-in 0.05s rate limit.
- **Categories change dynamically**: game updates add new version-event categories; if you can't find new content, run `list <category> --refresh` or `tree --refresh`.
- **Strategy entries are "placeholder cards"**: `detail <5-digit id>` may return 2031; use `search --preview` to get the embedded real entryId (this is by design, not a bug).
- **`-X utf8 -u` is required on Windows**: otherwise Chinese/emoji output will crash under GBK encoding.

---

## 🧾 License

[MIT](LICENSE)

---

## 🙏 If You Like It, Help It Reach More People

If you find this skill useful, feel free to share it with friends who play Wuthering Waves, or include it in your skill marketplace.

Installation command:

```bash
npx skills add Alphamancer/kurobbs-wiki
```

---

## 🤝 Contributing

Issues and PRs are welcome. When developing, keep in mind:

- After making changes, run `python -X utf8 -c "import py_compile; py_compile.compile('scripts/wikiquery.py', doraise=True)"` to verify the syntax
- Keep `wikiquery.py` pure standard library (except for the `post` subcommand), to avoid adding third-party dependencies to the main query flow
- Follow the "Key Pitfalls" and "Known Blocker Quick Reference" conventions in SKILL.md
