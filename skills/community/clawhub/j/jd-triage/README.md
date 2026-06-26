# jd-triage

**Stop wasting cycles on bad-fit JDs.** Paste a job description, get a verdict against the criteria *you* defined.

A skill for [OpenClaw](https://github.com/openclaw) that evaluates job descriptions against your personal career criteria. Bootstrap your filter once; evaluate every JD against it forever. Maintains an evaluation history so you can compare new opportunities against past ones.

---

## What it does

- **Evaluates a JD** with a 4-tier verdict (✅ Strong Apply / 🎯 Apply / ⚠️ Caution / ❌ Skip / OUT) and 6-axis 5-star scoring
- **Bootstraps your criteria** through a one-time structured intake — 13 questions in 3 blocks
- **Refreshes itself** every 15 days with a single yes/no prompt — no nag, no rerun
- **Logs every evaluation** to a single history file with stable IDs (`JD-YYYYMMDD-XXX`)
- **Compares two JDs** side by side — useful when you have multiple offers or want to benchmark a new role against a previous one
- **Speaks your language** — bootstrap and output follow your input language (Chinese/English supported); stored data uses English keys + your-language values for grep-friendliness

## Who it's for

- People actively job hunting who want to filter inbound recruiter messages fast
- People who passively look at JDs and waste mental cycles re-evaluating the same dealbreakers
- Anyone whose criteria has multiple subtle dimensions (vibe / company type / lifestyle) that a salary-and-title filter misses

**Not for:** Recruiters evaluating candidates. The skill grades the JD against the user, not the other way around.

## Installation

```bash
clawdhub install jd-triage
```

Or manual:

```bash
git clone <repo-url> ~/.openclaw/skills/jd-triage
```

## First run

The first time you invoke the skill (paste a JD or run `/jd-triage`), you'll be asked 13 questions in 3 blocks:

1. **Profile** (3 Qs) — years of experience, current title/company, current salary
2. **Hard gates** (4 Qs) — salary floor, target cities, lifestyle tier, hard red lines
3. **Soft axes** (6 Qs) — title keywords, target industries, company type ratings, company size ratings, positive vibe anchors, negative vibe anchors

Your answers are saved to `~/.openclaw/workspace/jd_criteria.md`. Subsequent runs skip the bootstrap entirely until 15 days pass, at which point the skill asks one yes/no question to confirm nothing has changed.

## Commands

| Command | What it does |
|---|---|
| Paste a JD (or `/jd-triage`) | Evaluate the JD; bootstrap first if no criteria saved |
| `/jd-triage update` | Edit your criteria — current values pre-filled, change only what you want |
| `/jd-triage reset` | Wipe and re-bootstrap from scratch |
| `/jd-triage history` | Show last 10 evaluations as a one-line table |
| `/jd-triage compare <id1> [<id2>]` | Side-by-side comparison; if only one ID given, compares with most recent |

Natural language also works: "compare with the last one", "show my JD history", "update my criteria".

## Sample output

```
Verdict: ⚠️ Caution

Title fit         ★★★★☆
Industry/track    ★★★★★
Company type      ★★★☆☆ (mid-size, you weighted 3)
Company size      ★★★★☆
Vibe              ★★☆☆☆  ← key drag
Salary match      ★★★★☆

One-liner: Strong AI Agent role on paper, but company description leans heavily on
"growth funnels" and "conversion KPIs" — matches your negative vibe anchors.
Action: Negotiate first to clarify scope; backup option, not lead.

💡 If this evaluation changed your view on any criteria, say "update criteria".
```

## Files written

The skill writes to your OpenClaw workspace:

- `~/.openclaw/workspace/jd_criteria.md` — your criteria profile
- `~/.openclaw/workspace/jd_history.md` — append-only evaluation log

Both files are plain markdown. Edit them by hand if you want — the skill will trust your edits and only point out missing required fields.

## Privacy

By default, history entries store the verdict, scores, and a one-line summary — **not the raw JD text**. This avoids accidentally persisting recruiter contact info or unposted comp details.

If you set `history_detail: full` in your criteria file, raw JDs are stored too. The skill will warn you the first time you opt in. Don't sync your workspace to public clouds with this setting on.

## Limitations

- **Does not evaluate your fit for the role.** The skill grades how well a JD matches *your* criteria, not whether you match the JD's requirements. It does not read your resume.
- **Vibe is subjective.** The vibe-fit axis depends entirely on the anchor companies you provide. A 1★ vibe rating drops the verdict at least one tier — this is intentional, not a bug. If you don't care about vibe, don't fill in vibe anchors.
- **Salary signals can be missing.** Many JDs omit comp; the skill will flag this and ask you to follow up with the recruiter rather than guessing.
- **No salary-negotiation advice.** Out of scope.
- **Single-language summaries.** Stored summaries stay in the language you wrote them in — they are never auto-translated, even when you switch interaction languages.
- **No automatic history cleanup in v0.1.** Manage `jd_history.md` manually if it grows long.

## Author

Maintained by Barry Wang ([@bwancoding](https://github.com/bwancoding)). Issues and pull requests welcome at [https://github.com/bwancoding/jd-triage](https://github.com/bwancoding/jd-triage).

## License

MIT — see the [LICENSE](../LICENSE) file in the repo root.
