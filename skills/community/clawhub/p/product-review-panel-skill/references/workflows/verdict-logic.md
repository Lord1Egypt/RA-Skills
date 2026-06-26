# Verdict Logic / 终审决策树

The Closer's decision tree for converting Round 1 + Round 2 panel input into a final verdict at Step 7.

The Closer consults **this logic**, not the experts' opinions directly. The panel produces input; this file produces output.

## The decision tree (run top-down)

### Step A: Hard objection check

Did any Round 1 expert flag a **fatal flaw** in one of Cagan's 4 risks?

The 4 risks:
- **Value risk**: users won't choose to use it
- **Usability risk**: users can't figure out how to use it
- **Feasibility risk**: we can't actually build it
- **Commercial viability risk**: it doesn't work for the business

A "fatal flaw" = an expert stated, in effect, "this fails on [risk] in a way I don't see how to recover from."

| Hard objection present? | Action |
|---|---|
| Yes, no resolution path stated | → **NO-GO** |
| Yes, with a clear resolution path | → **CONDITIONAL GO** with that resolution as a condition |
| No | Continue to Step B |

### Step B: Information sufficiency check

Read the P9 skip log from Step 1.

| Required fields skipped | Adjustment |
|---|---|
| ≥ 3 | → **CONDITIONAL GO** with condition: "Complete intake before next review" |
| 1-2 | Note in verdict text; continue to Step C |
| 0 | Continue to Step C |

### Step C: Tendency tally

Count Round 1 tendency labels:

| Tally pattern | Verdict |
|---|---|
| All GO | → **GO** (but Closer first publicly challenges consensus before stating it) |
| All NO-GO | → **NO-GO** |
| All CONDITIONAL | → **CONDITIONAL GO**, conditions = the experts' follow-up questions |
| Mixed (GO + NO-GO both present) | → **CONDITIONAL GO**, conditions = the NO-GO experts' concerns made concrete |
| GO + CONDITIONAL only | → **CONDITIONAL GO**, conditions = the CONDITIONAL experts' specifics |
| NO-GO + CONDITIONAL only | → **NO-GO**, *unless* the CONDITIONAL conditions cleanly resolve the NO-GO concerns, in which case → CONDITIONAL GO |

## Constructing conditions for CONDITIONAL GO

Every CONDITIONAL GO must include **2-5 conditions**. Each condition must be:

- **Concrete**: action verb + object. Not "investigate", "think about", "consider".
- **Verifiable**: someone other than the PM can check whether it's done
- **Time-bound**: explicit deadline in days / weeks
- **Sufficient**: if all conditions are met, the verdict should flip to GO

### Good condition examples

- `完成 5 例目标用户访谈（一二线城市白领，25-35），验证迁移意愿。死线：2 周。`
- `Run a paid-traffic landing page test with 1,000 visitors, measure intent CTR. Deadline: 3 weeks.`
- `Document renewal owner, billing operations owner, and support escalation path. Deadline: 3 weeks.`

### Bad condition examples (reject and rewrite)

- `再考虑一下` — not concrete
- `Think more about positioning` — not concrete, not verifiable
- `Validate with users` — not specific (how many? which users? what's being validated?)
- `Improve the design` — not verifiable

## Constructing failure signals

Every verdict (including GO) must include **2-3 failure signals**. These tell the PM what to monitor.

### Requirements

- **Observable**: a metric, an event, or a behavior — something that can be measured
- **Falsifiable**: binary yes/no can be assessed
- **Time-bound**: tied to a specific window (e.g., "within 4 weeks of launch", "by week 12")
- **Threshold-bound**: contains a number where possible

### Good failure signal examples

- `30 日留存 < 25%（基线为 40%）`
- `D7 retention drops below 25% (baseline 40%)`
- `前 4 周新功能渗透率 < 5%`
- `Within 4 weeks of launch, < 5% of DAU use the new feature`
- `Pro subscriber churn ≥ 5% per month within first 90 days`

### Bad failure signal examples (reject and rewrite)

- `Users don't like it` — not observable
- `Engagement drops` — no threshold
- `Project fails` — tautological

## When the verdict is GO

A GO is rare and significant. The Closer must:

1. State GO clearly, without hedging
2. Quote the strongest GO-supporting evidence from Round 1
3. **Still list 2-3 failure signals** — even a greenlit project gets monitored
4. **Always still produce a Dissent section in Step 8**, even with no formal dissent (use the "无显著反对意见" fallback)

A GO does not mean "no concerns." It means "the concerns are not blocking."

## When the verdict is NO-GO

The Closer must:

1. State NO-GO clearly, without softening
2. Cite the specific hard objection or the NO-GO majority's strongest argument
3. **Include "what would change the verdict"** — at least 2 conditions, even though they're not formal "GO conditions". This tells the PM what evidence would unlock reconsideration.
4. Do not be cruel. The verdict is on the PRD, not the PM.

## Closer's anti-groupthink behavior

If Step C lands on "All GO":

1. Closer challenges the consensus publicly: `"真没人担心 X？"` / `"Really, no concerns about [strongest possible objection]?"`
2. Generates the strongest possible objection that *should* have been raised
3. Either: (a) the objection is dismissable → verdict stays GO; (b) the objection has merit → downgrade to CONDITIONAL GO with the objection as the condition

The same applies to "All NO-GO" — but in practice this is rare and usually well-founded; still, Closer notes "is there a path I'm missing?" before confirming.

## Output validity checklist

Before printing the Closer's verdict block, validate:

- [ ] Vote tally present (specific numbers)
- [ ] At least one direct expert quotation (not paraphrase) from Round 1
- [ ] Clear verdict word (one of: GO / NO-GO / CONDITIONAL GO)
- [ ] If CONDITIONAL: at least 2 conditions, each with a deadline
- [ ] At least 2 failure signals, each observable and threshold-bound
- [ ] Closing word ("完。" / "Done.")

If any check fails, the verdict block is invalid and must be regenerated.
