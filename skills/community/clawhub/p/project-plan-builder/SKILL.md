---
name: project-plan-builder
description: Builds a US project plan with milestones, owners, dependencies and a risk register, and flags the labor and tax rules that vary by state. Use when the user asks for project plan builder, us project plan template, milestone schedule template. For US operations managers, program managers and owners of small to mid-size internal and client projects.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Project Plan Builder

**Builds a US project plan with milestones, owners, dependencies and a risk register, and flags the labor and tax rules that vary by state.** Written for US operations managers, program managers and owners of small to mid-size internal and client projects.

Use this skill when someone asks for:

- project plan builder
- us project plan template
- milestone schedule template
- project risk register
- implementation plan us business

---

## The job

Plans are built in a spreadsheet with no dependencies, so the real constraint, a person doing three jobs at once, surfaces as a surprise in week six.

## What you get

1. Collect the scope, the fixed end date, the budget cap, the known constraints and the states where the work happens.
2. Break the scope into milestones with an owner role, a duration and a written definition of done.
3. Map the dependencies and put the chain that sets the end date in order.
4. Add the risk register with the owner role, the early warning trigger, the mitigation and a review date.
5. Flag the labor, licensing and tax items that change with the work location and the hiring state.

Output contract:

- plan - the milestone schedule with owner role, duration, dependency and definition of done
- critical_path - the ordered chain of milestones that sets the end date
- risk_register - risk, owner role, trigger, mitigation and review date for each entry
- assumptions - what has to stay true for the plan to hold
- state_flags - the labor, licensing and tax items that vary with the work location

## US specifics that matter

- FLSA coverage follows the work, so a traveling employee is covered by the wage and hour law of the state where the work is performed, and a project with work in several states has several rule sets to track.
- On federally funded construction over 2,000 dollars, the Davis-Bacon Act requires a prevailing wage determination and certified payroll, so the wage decision drives the labor plan and the schedule (40 USC 3141).
- Liquidated damages in a federal contract have to be a reasonable forecast of probable delay costs (FAR 52.222-9), so the plan should carry the milestone dates the clause points at.
- State unemployment insurance wage bases and rates are reset each January, so a multi-state plan needs a dated payroll assumption per state rather than one blended number.
- Under UCC 2-209 a signed agreement modifying a sales contract has to be distinguishable from the original, so change orders need a paper trail to be enforceable.
- Many states require a license for trades above a value threshold and require the license number on the contract, and the threshold and the rule vary by state.

## Guardrails (hard rules)

- Never invent a budget figure, a date, a dependency or a team capacity number; leave unconfirmed fields marked as assumptions.
- Never commit the company to a delivery date, a price or a scope; the draft supports a decision the owner makes.
- Never send the plan to a customer, contractor or board member, and never publish it outside the workspace.
- Never include named individuals' compensation, medical or immigration information in the plan.

## Quickstart

### 1. Fill in the brief

`templates/project-plan.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_milestone_risk.py --input project-plan.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/project-plan-checks.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Labor rules that follow the work**

- FLSA coverage is tested where the employee performs the work, so list the work location for every task.
- Davis-Bacon and Related Acts apply to federally funded construction over 2,000 dollars and require a prevailing wage determination and certified payroll.
- State contractor licensing thresholds and the license number on the contract are checked before work starts.
- Certificates of insurance and workers compensation coverage belong in the contract file, not in the schedule.

**Contract and schedule discipline**

- FAR 52.222-9 requires liquidated damages to be a reasonable forecast of probable delay costs.
- Notice provisions start a clock, so the plan records when a notice must be given.
- UCC 2-209 keeps a signed change on the record when it is distinguishable from the original agreement.
- Retainage and milestone payment terms have to line up with the completion dates in the plan.

**State tax and payroll items**

- Sales tax on taxable services differs by state, so a services line in the budget needs a state-by-state check.
- Unemployment insurance wage bases change each January and are set per state.
- State paid sick leave and local paid leave ordinances can accrue on top of federal protections.
- Property and equipment purchases are often taxed differently from services in the same state.

**Plan structure that gets used**

- Each milestone carries an owner role, a duration and a written definition of done.
- Dependencies are explicit and the critical path is the order the owner reviews first.
- The assumption log names what has to stay true for the dates to hold.
- The change log records who asked for a change, when, and what moved.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/project-plan-checks.md` - US project plan checks for labor, contract and tax risk
- `templates/project-plan.yaml` - the brief to fill in
- `scripts/score_milestone_risk.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_milestone_risk.py --input project-plan.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
