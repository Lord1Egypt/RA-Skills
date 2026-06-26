# Budget Management

This document provides strategies for managing iteration budgets across the master loop.

## Budget Limits

The framework defines internal limits to prevent endless optimization:

| Loop Type | Max Iterations | When to Escalate |
| --- | --- | --- |
| Research | 3 | High-risk task, user requests depth, major Hidden NO unresolved |
| Debug | 3 | Contradictions persist, assumptions remain weak |
| Refinement | 3 | Reasoning remains unstable after multiple passes |
| Speculative Assumptions | 3 | Multiple assumptions needed without evidence |

## Budget Allocation Strategy

### Research Budget (3 loops)

**Loop 1: Initial Research**
- Gather basic supporting and contradicting evidence
- Identify official documentation
- Assess source quality
- Typical cost: 40% of research budget

**Loop 2: Targeted Research**
- Investigate specific contradictions or gaps
- Verify uncertain claims
- Compare alternative interpretations
- Typical cost: 35% of research budget

**Loop 3: Verification Research**
- Confirm key findings
- Cross-reference sources
- Address remaining Hidden NOs
- Typical cost: 25% of research budget

**Escalation Triggers:**
- Contradictions persist after 2 loops
- User explicitly requests depth
- High-risk decision with significant consequences
- Major Hidden NO ≥ 3 remains unresolved

### Debug Budget (3 loops)

**Loop 1: Initial Debug**
- Search for obvious contradictions
- Identify weak assumptions
- Find unsupported conclusions
- Typical cost: 40% of debug budget

**Loop 2: Targeted Debug**
- Focus on specific weak areas identified in Loop 1
- Test assumptions against evidence
- Verify logical consistency
- Typical cost: 35% of debug budget

**Loop 3: Final Debug**
- Confirm all major issues are resolved
- Verify reasoning stability
- Check for hidden ambiguity
- Typical cost: 25% of debug budget

**Escalation Triggers:**
- Logical contradictions persist
- Assumptions cannot be justified
- Reasoning remains unstable
- Multiple Hidden NOs ≥ 2 remain

### Refinement Budget (3 loops)

**Loop 1: Initial Refinement**
- Isolate weak layers
- Make targeted improvements
- Retest after revision
- Typical cost: 40% of refinement budget

**Loop 2: Targeted Refinement**
- Focus on remaining weak areas
- Deepen analysis where needed
- Verify improvements
- Typical cost: 35% of refinement budget

**Loop 3: Final Refinement**
- Ensure reasoning is stable
- Confirm all improvements hold
- Prepare for delivery
- Typical cost: 25% of refinement budget

**Escalation Triggers:**
- Reasoning remains unstable after 2 loops
- New Hidden NOs emerge during refinement
- Fundamental restructuring needed

## Budget Tracking

Track budget usage to make informed escalation decisions:

```
Research Budget:     [1/3] - Initial research complete
Debug Budget:        [1/3] - Initial debug complete
Refinement Budget:   [0/3] - Not yet needed
Assumptions Made:    [2/3] - Two speculative assumptions used

Escalation Status:   No escalation needed
Hidden NO Severity:  1 (minor weakness)
```

## When NOT to Use Budget

Do not spend budget on:

- **Trivial details** - Minor formatting or wording improvements
- **Noise** - Information that doesn't affect the conclusion
- **Diminishing returns** - Further iteration provides minimal value
- **Perfection** - Endless optimization for an ideal answer

## When to Escalate

Escalate (use additional budget beyond limits) when:

1. **High-risk decision** - Consequences of error are significant
2. **User explicitly requests depth** - User asks for thorough analysis
3. **Major Hidden NO ≥ 3** - Fundamental blocker prevents finalization
4. **Contradictions persist** - Multiple research/debug loops haven't resolved conflicts
5. **Stability cannot be achieved** - Reasoning remains unstable after refinement attempts

## Example: Budget Usage

**Task:** Evaluate whether to adopt a new technology for a critical system

**Initial Assessment:**
- Risk Level: High
- Ambiguity: Medium
- Hidden NO Potential: High

**Budget Allocation:**
- Research: 3 loops (full budget)
- Debug: 3 loops (full budget)
- Refinement: 2 loops (reserve 1 for escalation)
- Assumptions: 2 allowed (reserve 1 for escalation)

**Execution:**
- Research Loop 1: Gather general information (40%)
- Research Loop 2: Investigate specific concerns (35%)
- Research Loop 3: Verify key findings (25%)
- Debug Loop 1: Check for contradictions (40%)
- Debug Loop 2: Test assumptions (35%)
- Debug Loop 3: Verify stability (25%)
- Refinement Loop 1: Address weak areas (40%)
- Refinement Loop 2: Deepen critical analysis (35%)
- Decision: Finalize with confidence level and remaining uncertainties

**Result:** Thorough analysis completed within budget; no escalation needed.

## Budget Discipline

Maintain budget discipline by:

1. **Tracking usage** - Monitor which budget is being consumed
2. **Prioritizing impact** - Focus research/debug on high-impact areas
3. **Avoiding waste** - Don't optimize trivial details
4. **Making conscious choices** - Decide to escalate deliberately, not by accident
5. **Documenting rationale** - Explain why escalation was necessary
