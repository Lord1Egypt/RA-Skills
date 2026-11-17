<p align="center">
  <img alt="mu-humanizer-minesweeping" src="assets/default-banner.png" width="100%">
</p>

# ✍️ mu-humanizer-minesweeping · 写作AI味消除与禁忌扫雷仪

> Evidence-conserving writing naturalizer and risk scanner for people who want clearer copy without invented details or unsafe automatic replacements.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-humanizer-minesweeping/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-humanizer-minesweeping)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-humanizer-minesweeping)](https://github.com/muippt/mu-humanizer-minesweeping/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-humanizer-minesweeping)](https://github.com/muippt/mu-humanizer-minesweeping/stargazers)

---

### 💡 Usage Examples

- 📣 **Polish public announcements** — remove filler while retaining numbers, actors, scope, and uncertainty.
- 📊 **Revise business updates** — identify templated transitions, duplicated claims, and filler conclusions.
- 📢 **Review brand and public copy** — flag unsupported absolutes, exaggerated promises, and identity-labeling language.
- 🧯 **Review high-sensitivity wording** — keep legal cases, minors, ethnicity, religion, sovereignty, and international relations as review-only items.
- 🌐 **Edit bilingual text** — apply Chinese or English expression patterns by sentence or paragraph while sharing factual anchors.
- 🔒 **Maintain local preferences** — keep company, team, and personal rules outside the public release.

---

### ✨ Core Highlights

#### 🧭 Evidence-conserving editing

Edits may only delete, compress, reorder, or restyle information already present in the source. The Skill never adds facts, names, dates, numbers, examples, quotations, or causal claims merely to make text sound more human.

#### 🔍 Independent fidelity audit

The audit reads only the source, edited text, and anchor list. It independently checks entities, numbers, time, causality, polarity, scope, and qualifiers; any drift reverts the affected text.

#### 🛑 NO-OP protection

Punctuation-only changes, formatting changes, and substitutions without a clear benefit are `NO-OP`s. They are reverted and reported as untreated signals rather than counted as completed edits.

#### 🧩 Four editing gates

Every candidate edit must pass eligibility, evidence-anchor, minimum-edit, and human-review gates. Delivery includes a per-item diff, stated benefit, anchor source, and audit result.

#### 💣 Original risk mapping

The written-risk module uses an original tiered mapping framework informed by public writing guidance. It does not reproduce, imitate, or replace source texts. High-sensitivity matches are always `review_only`.

#### 🔒 Private-rule isolation

Company, team, and personal preferences live under a local `rules/` directory ignored by Git. Public releases never bundle organizational or personal rules.

---

### 📌 Comparison

| Dimension | 🧭 This project | Conventional polishing | Dictionary replacement |
|---|---|---|---|
| Facts, numbers, and qualifiers | Extracts anchors first, then audits independently | Depends on the editor's self-check | Usually not checked |
| Ineffective edits | Detects and reverts `NO-OP`s | May be counted as edits | Can create mechanical substitutions |
| High-sensitivity wording | Review-only with a clear boundary | Handling varies | May suggest unsuitable replacements |
| Rule-source boundary | Original mapping; no source-text reproduction | Often undocumented | Depends on word lists |
| Local preferences | Optional and separated from releases | Varies | Varies |

---

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|---|---|---|
| Full edit | Rewrite plus written-risk scanning | Provide text and ask to polish, humanize, or rewrite it |
| Risk scan only | Check written-language risks without rewriting | Explicitly ask for a scan only |
| Private-rule management | Add, list, update, disable, or delete a local rule | Use an explicit rule-management request |

A full edit anchors the scene, calibrates style, performs evidence-conserving edits, runs an independent fidelity audit, and then scans written-language risks. Short texts still use occurrence counts; density reporting is omitted only where a rule specifies it.

---

### ⚙️ Technical Specs

| Item | Description |
|---|---|
| Type | Prompt-and-reference Skill |
| Dependencies | None |
| Compatible environments | AI-agent environments that load `SKILL.md` and local references |
| Package size | About 1.5 MB including the README banner asset |
| File structure | `SKILL.md`, `references/`, `rules/` (local only), and public documentation |
| Input support | Natural-language text; Chinese, English, and mixed-language passages |
| Output format | Per-item diff, stated benefit, anchor source, audit result, and untreated signals |
| Languages | Chinese and English editing; Chinese written-risk mapping |
| Version | 6.7.0 |
| License | MIT |

---

### 🛠️ Quick Start

**1. Install** — clone into your skills directory

```bash
git clone https://github.com/muippt/mu-humanizer-minesweeping.git ~/.claude/skills/mu-humanizer-minesweeping
```

> Using a different agent? Put the directory wherever that tool loads Skills from. Project-level use works too: `.claude/skills/mu-humanizer-minesweeping`.

**2. Verify** — restart or reload your agent and confirm that the Skill is picked up

```text
List my available skills
```

**3. Run** — paste a passage and state the outcome you need

```text
Please make the following announcement sound more natural and remove filler or templated language.
Preserve every fact, number, scope, and qualifier; list high-sensitivity wording as human-review items only.
```

Or invoke a specific workflow:

```text
Scan the following text for written-language risks only. Do not rewrite it.
```

```text
Add a local writing-preference rule for me. Do not include it in the public release.
```

---

### 🔒 Security & Privacy

- Runs locally as a prompt-and-reference Skill; it makes no network calls and collects no telemetry.
- Contains no credentials and does not write back to source documents.
- Private rules remain local, are ignored by Git, and are excluded from public releases.
- Does not infer authorship or provide AI-detection-evasion advice.

---

### ⭐ Star History

This is the first public release. Star history will appear after the repository has accumulated real public data.

> If this Skill is useful, a [GitHub star](https://github.com/muippt/mu-humanizer-minesweeping/stargazers) helps more writers discover an evidence-first editing workflow.

---

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

---

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 muippt

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for rule-source and reference notes. Contributions, corrections, and safety feedback are welcome through [CONTRIBUTING.md](CONTRIBUTING.md) and GitHub Issues.

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
