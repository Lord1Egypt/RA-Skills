# MiroPRISM — Post-Launch Metrics Reference

> **When to use this:** After running 10+ real MiroPRISM reviews, use this data to tune protocol parameters (round cap, reviewer count, broadcast vs selective pairing).

## Metrics Schema

```
date	slug	verdict_change_rate	uncertain_rate	r1_finding_count	r2_new_finding_count	high_finding_count	unresolved_disagreement_count
```

Column formulas:
- `verdict_change_rate` = `(reviewers where R2 verdict ≠ R1 verdict) / total_reviewers`
- `uncertain_rate` = `(total UNCERTAIN responses in R2) / (total findings × total_reviewers)`
- `r1_finding_count` = count of deduplicated findings in r1-digest.md
- `r2_new_finding_count` = count of "New Findings" items across all R2 outputs
- `high_finding_count` = count of [HIGH] findings in synthesis
- `unresolved_disagreement_count` = count of entries in "Unresolved Disagreements" section

## Aggregation Queries

```bash
# View all runs
cat analysis/miroprism/metrics.tsv | column -t -s $'\t'

# Average verdict change rate
awk -F'\t' 'NR>1 {sum+=$3; count++} END {print "Avg verdict change rate:", sum/count}' analysis/miroprism/metrics.tsv

# Average uncertain rate
awk -F'\t' 'NR>1 {sum+=$4; count++} END {print "Avg uncertain rate:", sum/count}' analysis/miroprism/metrics.tsv

# Average HIGH findings per run
awk -F'\t' 'NR>1 {sum+=$7; count++} END {print "Avg HIGH findings:", sum/count}' analysis/miroprism/metrics.tsv

# Runs with UNCERTAIN rate > 0.5 (possible review dilution)
awk -F'\t' 'NR>1 && $4 > 0.5 {print $1, $2, "uncertain_rate=" $4}' analysis/miroprism/metrics.tsv
```

## What to Look For

1. **R1→R2 finding delta** (`r2_new_finding_count / r1_finding_count`): If consistently <10% across 10 runs, R2 adds little — consider dropping to 1 round for low-stakes reviews.

2. **Verdict change rate** (`verdict_change_rate`): If >60%, R2 is causing significant opinion shifts — revisit whether broadcast or selective pairing is better for your use case.

3. **UNCERTAIN usage rate** (`uncertain_rate`): Watch for:
   - 0% — reviewers are overconfident; may be ignoring genuine ambiguity
   - >50% — possible avoidance or review dilution

4. **Budget vs Standard quality gap**: Compare `high_finding_count` across Budget and Standard runs on similar artifacts. If Budget consistently finds the same HIGHs, you may not need Standard for routine reviews.

5. **Injection resistance**: Check `R1-digest-log.md` sanitization counts. Elevated "excluded findings" count may indicate adversarial content or poorly specified finding templates.

## Decisions After 10 Runs

- **Round cap**: If R2 delta is consistently <10%, consider defaulting to 2 rounds max
- **Reviewer count default**: If Budget and Standard produce similar HIGH counts, consider Budget as default for routine reviews
- **Broadcast vs selective pairing**: If verdict change rate is >60%, experiment with giving R2 reviewers only findings relevant to their role
- **Timeout threshold**: If you hit >20% timeouts, increase default to 15 min
