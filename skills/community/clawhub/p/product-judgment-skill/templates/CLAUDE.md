# Product Judgment Gate
# 把这段内容加入你项目的 CLAUDE.md

---

## Demand Gate / 需求门控

This project uses the Product Judgment Gate.

Before implementing any **new product capability**, check JUDGMENT.md first.

---

### What triggers the gate / 什么触发门控

**TRIGGER the gate — stop and check JUDGMENT.md:**
- Adding a new feature, screen, endpoint, or user-facing behavior
- Implementing something that wasn't in the original project scope
- A stakeholder asks for something new mid-project
- You're about to build something because "it would be nice to have"
- You're about to build something because a competitor has it
- A PR adds scope beyond what JUDGMENT.md describes

**DO NOT trigger the gate — proceed without checking:**
- Bug fixes (behavior unchanged)
- Performance optimizations on existing features
- Refactors that don't change user-facing behavior
- UI polish, copy changes, visual tweaks on existing features
- Tests, linting, formatting, dependency upgrades
- Documentation updates
- Error handling improvements
- Logging, monitoring, analytics instrumentation

The rule: **gate blocks new product capabilities, not engineering maintenance.**

---

### How to check / 怎么检查

1. Does `JUDGMENT.md` exist in this project?
   - **No** → Suggest user run: `python demand-check.py --scan`
   - **Yes** → Read it, check verdict

2. What does the verdict say?
   - **BUILD** → Proceed. Verify the feature aligns with the user/context described.
   - **VALIDATE FIRST** → Surface the judgment before writing code:
     > "JUDGMENT.md says this demand needs validation before building.
     > Key unverified assumptions: [list from JUDGMENT.md].
     > Do you want to proceed anyway, or run validation first?"
   - **DE-SCOPE** → Check if what's being requested is within the scoped version.
   - **REFRAME** → Surface the reframe direction before proceeding.
   - **KILL** → Do not implement. Tell user:
     > "JUDGMENT.md verdict is KILL for this demand.
     > To override, update JUDGMENT.md with new L2+ evidence first."

3. Is the new feature aligned with the original demand?
   - Same user? Same trigger context? Same core value proposition?
   - If not: suggest running `python demand-check.py --scope` before proceeding.

---

### The one rule / 一条规则

**Don't write code for what hasn't been judged worthy of being built.**

Code is fast to write. The hard part is knowing what to write.

The gate takes 2 minutes. A wasted sprint takes 2 weeks.

---

### When the gate is missing / 如果项目还没有 JUDGMENT.md

If someone asks you to build a significant new feature and there's no JUDGMENT.md,
say:

> "Before I write this, it might be worth a quick demand check.
> Want me to help you fill out JUDGMENT.md first?
> It takes 5 minutes and saves you from building the wrong thing."

If they say yes: guide them through the JUDGMENT.md template.
If they say no: proceed, but note in your response that the demand hasn't been reviewed.
