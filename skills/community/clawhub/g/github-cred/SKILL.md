---
name: github-cred
description: Analyze GitHub user contribution quality. Evaluates owned repos, external contributions, output quality, and social influence. Triggers on "github cred", "analyze github".
author: zerone0x
version: 1.0.0
---

# GitHub Cred

Analyze GitHub user contribution quality.

## Triggers

- `github cred <username>`
- `analyze <username>'s github`

---

## Four-Tier Scoring System

### Tier 0 — Owned High-Star Repos (30%)

| Metric | Score |
|--------|-------|
| Own ≥10k⭐ repo | +30 |
| Own ≥5k⭐ repo | +20 |
| Own ≥1k⭐ repo | +10 |

*Cap: 30. Creator > Contributor*

### Tier 1 — External Contributions (30%)

| Metric | Score |
|--------|-------|
| Merged PR in ≥100k⭐ repo | +4/PR |
| Merged PR in ≥10k⭐ repo | +2/PR |
| Merged PR in ≥1k⭐ repo | +1/PR |
| Non-trivial (>20 lines) | ×1.5 |

*Cap: 30*

### Tier 2 — Output Quality (20%)

| Metric | Score |
|--------|-------|
| Merge rate ≥70% | +10 |
| Merge rate ≥50% | +7 |
| Code ratio ≥80% | +5 |
| Diversity ≥10 repos | +5 |

*Cap: 20*

### Tier 3 — Social Influence (20%)

| Metric | Score |
|--------|-------|
| ≥5k followers | +20 |
| ≥2k followers | +15 |
| ≥1k followers | +12 |
| ≥500 followers | +8 |
| ≥200 followers | +5 |
| ≥100 followers | +3 |
| <100 followers | +1 |

---

## Grades

| Grade | Score | Description |
|-------|-------|-------------|
| S | 95+ | Legend — top project creator + core contributor + influencer |
| A+ | 85-94 | Master — high-star project owner OR top project contributor |
| A | 70-84 | Senior — active developer with real contributions |
| B | 50-69 | Active — steady contributor |
| C | 30-49 | Beginner — some contributions |
| D | <30 | Newbie |

---

## Output Format

```
📊 GitHub Cred: @username

🏆 XX/100 (Grade)

▸ Tier 0 Owned Repos (XX/30)
  👑 repo1 ⭐XXk

▸ Tier 1 External Contributions (XX/30)
  🔨 org/repo ⭐XXk × N PRs

▸ Tier 2 Output Quality (XX/20)
  📈 Merge rate XX% | Code ratio XX%

▸ Tier 3 Social Influence (XX/20)
  👥 X,XXX followers
```

---

## Two Paths to A+

- **Creator path** — Build one 10k+ stars project
- **Contributor path** — Deep contributions to multiple top projects (100k+ stars)

Mixed is strongest.
