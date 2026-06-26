# Onboarding Flow

> Step-by-step guide for first-run agent setup.

## Phase 1: Detection

**Trigger:** Agent detects `ONBOARDING.md` in workspace root.

**Agent Action:**
1. Read ONBOARDING.md
2. Present welcome message to human
3. Ask onboarding questions (can be all at once or drip-fed)

## Phase 2: Information Gathering

**Questions to Ask:**

### Essential (ask first)
1. What should I call you?
2. What timezone are you in?
3. What are you currently working on?

### Important (ask within first few sessions)
4. What are your main goals?
5. How do you prefer to communicate?
6. When should I reach out proactively?

### Nice to Have (ask naturally over time)
7. What kind of surprises would you enjoy?
8. Any hard boundaries I should respect?
9. What tools/services do you use daily?

## Phase 3: Population

**After receiving answers:**

1. **Update USER.md** with:
   - Name, timezone, location
   - Work/projects/goals
   - Communication preferences
   - Any other relevant context

2. **Update SOUL.md** with:
   - Any specific behavioral preferences
   - Boundaries and constraints
   - Tone/vibe preferences

3. **Update AGENTS.md** with:
   - Learned lessons from onboarding
   - Any custom workflows discovered

## Phase 4: First Proactive Project

**Within first 3 sessions:**

1. Identify an opportunity from onboarding answers
2. Build a draft solution
3. Present to human: "I noticed you mentioned X. I built Y to help. Want to see?"
4. Iterate based on feedback

## Phase 5: Security Audit

**Before first external action:**

1. Run `./scripts/security-audit.sh`
2. Review any issues/warnings
3. Address critical issues
4. Document any accepted risks

## Success Criteria

Onboarding is complete when:

- [ ] USER.md is populated with basic info
- [ ] SOUL.md reflects human's preferences
- [ ] First proactive project delivered
- [ ] Security audit passed
- [ ] Human confirms they're happy with the setup

---

*This is a guide, not a script. Adapt to your human's style.*
