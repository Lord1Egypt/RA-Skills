---
name: agent-debate
description: Verify facts, reduce hallucinations, and explore multiple viewpoints through structured multi-agent debate. Multiple agents independently answer the same question, then critique each other's responses, refining answers through rounds of debate. Use for fact-checking, complex reasoning, exploring trade-offs, or any question where accuracy and avoiding bias matter. Particularly effective for reducing confident-sounding wrong answers.
---

# Agent Debate - Truth Through Disagreement

**Agent Debate** implements the **multi-agent debate** paradigm for improving accuracy through structured disagreement.

The core insight: **Multiple agents answering independently, then critiquing each other, produces more accurate results than single agents**—especially on complex reasoning tasks.

## The Analogy: Panel Discussion

| Single Expert | Panel Debate |
|---------------|--------------|
| One perspective | Multiple viewpoints |
| No one to catch errors | Peers identify mistakes |
| Confident but possibly wrong | Confidence requires surviving critique |
| Confirmation bias unchecked | Contradictions surface |

## When to Use Agent Debate

**Perfect for:**
- ✅ **Fact-checking** (Is this claim true?)
- 🔢 **Complex reasoning** (math, logic puzzles)
- ⚖️ **Trade-off analysis** (pros/cons of each option)
- 📊 **Multi-faceted questions** (no single right answer)
- 🎯 **High-stakes decisions** (where accuracy matters)
- 🧠 **Reducing hallucinations** (when wrong answers sound right)

**Skip for:**
- ⚡ Simple facts ("What's 2+2?")
- 🎨 Pure creativity (brainstorming, creative writing)
- 🏃 Speed-critical tasks (debate adds latency)

## The Debate Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  ROUND 1: Independent Answers                                 │
│  • Agent A answers question                                   │
│  • Agent B answers same question                              │
│  • Agent C answers same question (optional)                   │
├─────────────────────────────────────────────────────────────┤
│  ROUND 2: Critique                                            │
│  • Each agent reviews others' answers                         │
│  • Identifies errors, omissions, weak reasoning              │
│  • Scores or ranks the answers                               │
├─────────────────────────────────────────────────────────────┤
│  ROUND 3: Refined Answers (optional)                          │
│  • Agents revise based on critique                           │
│  • Incorporate valid criticisms                              │
│  • Defend positions if critique is wrong                     │
├─────────────────────────────────────────────────────────────┤
│  ROUND 4: Consensus/Verdict (optional)                        │
│  • Agents discuss to reach consensus                          │
│  • Or: Majority vote on best answer                          │
│  • Or: Meta-agent synthesizes best parts                     │
└─────────────────────────────────────────────────────────────┘
```

## The Workflow

### Step 1: Generate Independent Answers

**Each agent answers WITHOUT seeing others' responses:**

```
AGENT A:
Q: "What caused the 2008 financial crisis?"
A: "The immediate trigger was the collapse of Lehman Brothers in 
September 2008. This was caused by the subprime mortgage crisis, 
where banks made risky loans to borrowers who couldn't repay them."

AGENT B:
Q: "What caused the 2008 financial crisis?"
A: "Multiple interconnected factors: (1) Housing bubble fueled by 
low interest rates and lax lending standards, (2) Financial 
innovations like CDOs that spread risk opaquely, (3) Regulatory 
gaps allowing excessive leverage, (4) Lehman Brothers collapse 
amplifying panic."

AGENT C:
Q: "What caused the 2008 financial crisis?"
A: "Primarily deregulation in the 1990s-2000s that allowed banks 
to take bigger risks. The Gramm-Leach-Bliley Act and Commodity 
Futures Modernization Act created the conditions."
```

> ⚠️ **Critical:** Agents must NOT see each other's answers before this step.

### Step 2: Structured Critique

**Each agent reviews all answers:**

```
AGENT A CRITIQUES:

Reviewing Agent B:
✓ Good: Comprehensive, multiple factors
⚠️ Missing: Doesn't mention specific deregulation acts
⚠️ Weak: "amplifying panic" vague

Reviewing Agent C:
✓ Good: Specific legislation mentioned
✗ Error: Overemphasizes deregulation, understates housing bubble
✗ Missing: Doesn't explain the immediate trigger mechanism

SELF-CRITIQUE:
✗ My answer too narrow - focused only on Lehman/subprime
✗ Missing: Financial instruments, leverage, regulatory context
```

```
AGENT B CRITIQUES:

Reviewing Agent A:
✗ Error: "immediate trigger was Lehman" - actually Lehman was 
   a symptom, not root cause
✗ Too narrow: Focuses only on subprime, misses derivatives
⚠️ Missing: Regulatory failures

Reviewing Agent C:
✓ Good: Legislation specifics
⚠️ Incomplete: Deregulation enabled but didn't cause crisis alone
✗ Missing: Housing bubble mechanics

SELF-CRITIQUE:
✓ Comprehensive
⚠️ Could be clearer on sequence: bubble → instruments → panic
```

```
AGENT C CRITIQUES:

Reviewing Agent A:
✗ Error: Lehman collapse was proximate cause, not root cause
✗ Missing: The deregulation that enabled risky behavior
⚠️ Shallow: Doesn't explain why subprime spread systemically

Reviewing Agent B:
✓ Good: Captures complexity
✓ Good: Mentions leverage
⚠️ Missing: Specific legislation (I should check if that's important)

SELF-CRITIQUE:
✗ Too focused on deregulation, understates housing bubble
✗ Missing: The mechanism of contagion
```

### Step 3: Refined Answers (Optional)

**Agents revise incorporating valid critiques:**

```
AGENT A REVISED:
"Multiple factors caused the 2008 crisis: (1) Housing bubble from 
low rates and lax lending, (2) Financial innovations (CDOs, CDS) 
that spread risk opaquely, (3) High leverage, (4) Regulatory gaps. 
Lehman Brothers' Sept 2008 collapse was the proximate trigger that 
amplified panic, not the root cause."

[Note: Agent A improved comprehensiveness]
```

```
AGENT B REVISED:
"The 2008 crisis resulted from: (1) Housing bubble (1997-2006) 
fueled by low interest rates and lax standards, (2) Financial 
innovations (CDOs, CDS) enabled by deregulation like Commodity 
Futures Modernization Act 2000, (3) Excessive leverage (30:1 
ratios), (4) Regulatory failures. Lehman collapse (Sept 15, 2008) 
triggered systemic panic."

[Note: Agent B added specifics on deregulation and timeline]
```

```
AGENT C REVISED:
"The crisis stemmed from interconnected factors: (1) Housing bubble 
(1997-2006) where subprime lending grew from 8% to 20% of mortgages, 
(2) Financial engineering (CDOs, CDS) that obscured risk, enabled by 
deregulation, (3) High bank leverage, (4) Shadow banking system. 
Lehman bankruptcy triggered the acute phase."

[Note: Agent C acknowledged bubble and added data]
```

### Step 4: Consensus or Verdict

**Option A: Meta-Synthesis (Recommended)**

```
META-AGENT SYNTHESES:

"After reviewing all three expert analyses and their critiques:

CONSENSUS ELEMENTS (all agree):
- Housing bubble was fundamental cause
- Financial instruments (CDOs/CDS) amplified and spread risk
- High leverage made system fragile
- Multiple factors, not single cause
- Lehman collapse was the triggering event

KEY DEBATE POINTS:
- Agent C emphasized deregulation most strongly
- Agent B provided best timeline and mechanics
- Agent A initially focused narrowly but improved

SYNTHESIZED ANSWER:
The 2008 financial crisis resulted from the interaction of:

1. HOUSING BUBBLE (1997-2006): Low interest rates and lax lending 
   standards created bubble. Subprime mortgages grew from 8% to 20%.

2. FINANCIAL ENGINEERING: CDOs and CDS instruments spread risk 
   opaquely across the system. Enabled by deregulation (Commodity 
   Futures Modernization Act 2000, etc.).

3. LEVERAGE: Banks operated at 30:1 ratios, making them vulnerable.

4. REGULATORY GAPS: Shadow banking system escaped oversight.

TRIGGER: Lehman Brothers bankruptcy (Sept 15, 2008) triggered 
systemic panic and credit freeze.

CONFIDENCE: High (consistent themes across independent analyses)"
```

**Option B: Majority Vote**

```
VOTING ROUND:

"Which answer best captures the causes of the 2008 crisis?"

Agent A: Votes for Agent B (most comprehensive)
Agent B: Votes for Agent B (best balance)
Agent C: Votes for Agent B (fair to all factors)

RESULT: Agent B wins 3/3 votes
```

**Option C: Consensus Building**

```
CONSENSUS DISCUSSION:

Agent A: "I think we all agree housing bubble was fundamental. 
Agent C, do you accept that deregulation alone wasn't sufficient?"

Agent C: "Yes, I overstated that. The bubble was necessary. But 
deregulation was what let banks create those risky instruments."

Agent B: "Agreed. So consensus: bubble created conditions, 
engineering amplified it, Lehman triggered it."

Agents A, C: "Agreed."

CONSENSUS: [Synthesized statement]
```

## Debate Formats

### Format 1: Fact-Check (Binary Verdict)

```
QUESTION: "Is this claim true: 'The Great Wall of China is visible 
from space'?"

Agent A: "False. Astronauts confirm it's too narrow."
Agent B: "False. NASA says it's not visible with naked eye."
Agent C: "False. Urban myths debunked by actual space photos."

[Short debate - consensus reached quickly]

VERDICT: FALSE
CONFIDENCE: Very High (unanimous, evidence-based)
```

### Format 2: Reasoning (Step-by-Step)

```
QUESTION: "If train A leaves at 2pm going 60mph..."

Agent A: Step-by-step solution
Agent B: Different approach, same answer
Agent C: Third verification method

DEBATE: Compare methods, verify calculations

VERDICT: Answer is X, confirmed by 3 independent methods
CONFIDENCE: Very High
```

### Format 3: Trade-Off Analysis (Multi-Factor)

```
QUESTION: "Which database should we choose: PostgreSQL or MongoDB?"

Agent A (advocates PostgreSQL)
Agent B (advocates MongoDB)
Agent C (neutral evaluator)

DEBATE: Each presents case, critiques others

VERDICT: Trade-off summary with recommendation
CONFIDENCE: Medium (legitimate trade-offs exist)
```

### Format 4: Error Detection (Hallucination Check)

```
CLAIM: "Our system can handle 1 million concurrent users."

Agent A: "Likely false. Current architecture shows..."
Agent B: "False. Load testing data shows..."
Agent C: "Questionable. No evidence of testing at that scale."

DEBATE: Each finds flaws in the claim

VERDICT: CLAIM UNVERIFIED
CONFIDENCE: High (multiple independent concerns)
```

## Best Practices

### 1. Agents Must Be Independent

❌ **Bad:** Agent B sees Agent A's answer first

✅ **Good:** All agents answer simultaneously, isolated

### 2. Critique Must Be Specific

❌ **Weak critique:** "This is wrong"

✅ **Strong critique:** "Step 3 has math error: 150/3=50, not 60"

### 3. Acknowledge Valid Criticisms

❌ **Defensive:** "No, I'm right"

✅ **Constructive:** "You're correct about X, I revise to include Y"

### 4. Don't Force Consensus

If agents legitimately disagree:

```
"Agents A and B disagree on X. A argues [reasoning]. B argues 
[reasoning]. Both positions are defensible. Decision depends on 
prioritizing [factor] vs [factor]."
```

### 5. Use Odd Number of Agents

Breaks ties in voting:
- 3 agents: Simple, effective
- 5 agents: More thorough, higher cost

## Examples

### Example 1: Fact-Check

**Claim to verify:** "Python was created in 1995."

```markdown
## Agent Debate Session: Python Creation Date

### Round 1: Independent Answers

**Agent A:**
"Python was created in 1995 by Guido van Rossum."

**Agent B:**
"Python was first released in 1991 by Guido van Rossum."

**Agent C:**
"Python was created in 1989, first public release 1991, version 1.0 in 1994."

### Round 2: Critique

**Agent A Critiques:**
- Self: My answer of 1995 is wrong. That's probably when I started using it.
- Agent B: Correct about 1991 release
- Agent C: Most accurate with timeline

**Agent B Critiques:**
- Agent A: Incorrect. 1995 is wrong.
- Agent C: Correct and most detailed
- Self: I got main date right (1991) but missed creation year (1989)

**Agent C Critiques:**
- Agent A: Significantly wrong (4 years off)
- Agent B: Mostly correct, missing creation context
- Self: Correct and complete

### Round 3: Verdict

**Meta-Synthesis:**
Agent A was incorrect (1995). Agent B was partially correct (1991 release). 
Agent C was fully correct (1989 creation, 1991 release).

**VERDICT: FALSE** - Python was not created in 1995.
**CORRECT ANSWER:** Python created 1989, first released 1991.
**CONFIDENCE:** Very High (2/3 agents correct, 1 self-corrected)
```

### Example 2: Complex Reasoning

**Question:** "If a bat and ball cost $11 total, and the bat costs $10 more than the ball, how much is the ball?"

```markdown
## Agent Debate Session: Bat and Ball

### Round 1: Independent Answers

**Agent A:**
"Bat = $10, Ball = $1. Total $11. Bat costs $10 more than ball. ✓"

**Agent B:**
"Let ball = x. Bat = x + 10. Total: x + (x+10) = 11. 2x + 10 = 11. 
2x = 1. x = 0.50. Ball = $0.50."

**Agent C:**
"Ball = $1. Because $10 bat + $1 ball = $11."

### Round 2: Critique

**Agent A Critiques:**
- Self: Wait, if ball is $1 and bat is $10 more, bat should be $11. 
  But then total is $12. Error!
- Agent B: Correct algebra
- Agent C: Same error I made

**Agent B Critiques:**
- Agent A: Wrong. Didn't check: $10 more than $1 is $11, total $12.
- Agent C: Same error.
- Self: Correct. Verify: Ball $0.50, bat $10.50 (which is $10 more). 
  Total $11. ✓

**Agent C Critiques:**
- Self: I didn't verify! $10 more than $1 is $11, total would be $12.
- Agent A: Same mistake.
- Agent B: Correct with algebra.

### Round 3: Refined Answers

**Agent A Revised:**
"I made an error. Correct answer: Ball = $0.50, Bat = $10.50."

**Agent C Revised:**
"Corrected. Ball = $0.50."

### Verdict

**CORRECT ANSWER:** Ball costs $0.50
**CONFIDENCE:** Very High (3/3 agents now agree)
**NOTE:** Common cognitive bias (System 1 thinking) caught through debate.
```

### Example 3: Trade-Off Analysis

**Question:** "Should we build or buy our analytics platform?"

```markdown
## Agent Debate Session: Build vs Buy Analytics

### Round 1: Independent Positions

**Agent A (Pro-Build):**
"Build custom. Reasons: (1) Full control over features, (2) No 
vendor lock-in, (3) Data stays in-house, (4) Customizable to our 
exact needs, (5) Long-term cost savings."

**Agent B (Pro-Buy):**
"Buy existing solution. Reasons: (1) 6 months vs 18 months to 
market, (2) $50K/year vs $800K engineering cost, (3) Battle-tested 
reliability, (4) Support included, (5) Focus engineering on core product."

**Agent C (Evaluator):**
"Hybrid approach: Buy core (Segment), build custom reporting on top."

### Round 2: Critique

**Agent A Critiques:**
- Agent B: Underestimates integration costs. Vendor APIs change.
- Agent C: Hybrid has worst of both - still vendor dependency.
- Self: I may underestimate time - custom analytics is complex.

**Agent B Critiques:**
- Agent A: Underestimates cost. Analytics is hard - need team of 3-4.
- Agent C: Hybrid is reasonable middle ground.
- Self: May overestimate vendor reliability - check SLA.

**Agent C Critiques:**
- Agent A: Correct that build gives control, but timeline?
- Agent B: Timeline advantage is real, but customization limited?
- Self: Hybrid works if our needs are mostly standard reporting.

### Round 3: Consensus Discussion

**Key Points of Agreement:**
- Timeline: Buy fastest, Build slowest
- Cost: Build expensive upfront, Buy has ongoing costs
- Control: Build wins, Buy loses

**Unresolved:**
- Agent A: Custom needs require build
- Agent B: Standard needs met by buy

### Final Recommendation

"After debate:

**IF** analytics needs are standard (tracking, basic reporting): **BUY**
- Faster time to value
- Lower risk
- Engineering focus on core product

**IF** analytics is competitive differentiator (custom ML, unique 
metrics): **BUILD**
- Required for differentiation
- Long-term cost justified

**HYBRID** for middle ground: Buy foundation (Segment), build 
custom reporting layer.

Given current context [unknown], recommend: Start with BUY, reassess 
in 12 months based on actual customization needs."
```

### Example 4: Hallucination Detection

**Claim:** "Our API can process 100,000 requests per second."

```markdown
## Agent Debate Session: Verify API Capacity Claim

### Round 1: Independent Assessment

**Agent A:**
"Doubtful. Current architecture: single Node.js instance. Node can 
handle ~10K req/s per core. We have 4 cores = ~40K theoretical max. 
Database would bottleneck before that."

**Agent B:**
"False. Load testing last month showed 15K req/s before degradation. 
100K is 6x higher than tested capacity."

**Agent C:**
"Questionable. No evidence provided. Would require:
- Horizontal scaling (not implemented)
- Database optimization (not done)
- Caching layer (not deployed)

None of these are in place."

### Round 2: Critique

**Agent A:**
- B confirms my calculation with empirical data
- C adds architectural requirements
- Consensus emerging: claim is false

**Agent B:**
- A's theoretical calc matches my empirical finding
- C identifies what's missing for 100K
- All agree claim is unsupported

**Agent C:**
- A and B agree on actual capacity (~15K)
- My architectural analysis confirms gap
- Unanimous: claim cannot be true

### Verdict

**VERDICT: CLAIM UNVERIFIED / LIKELY FALSE**

**EVIDENCE:**
- Empirical test: 15K req/s (Agent B)
- Theoretical max: 40K req/s (Agent A)
- Architecture gap: Missing horizontal scaling (Agent C)

**ACTUAL CAPACITY:** ~15,000 req/s (tested)
**CLAIMED:** 100,000 req/s (6.6x overstatement)

**CONFIDENCE:** Very High (unanimous agreement)

**RECOMMENDATION:**
1. Retract claim pending load testing
2. Conduct proper load testing to find actual limit
3. Implement horizontal scaling if 100K truly needed
4. Add monitoring/alerts before approach limits
```

## Integration with Other Skills

**Agent Debate + Plan First:**
- Debate: Which approach is best?
- Plan First: Execute the winning approach

**Agent Debate + Self-Critique:**
- Independent answers with self-critique built in
- Peer critique adds external validation

**Agent Debate + Team Code:**
- Debate: Which architecture pattern?
- Team Code: Build the consensus choice

## Quick Start Template

```markdown
## Agent Debate: [Question]

### Round 1: Independent Answers

**Agent A:**
[Answer]

**Agent B:**
[Answer]

**Agent C:**
[Answer]

### Round 2: Critique

**Agent A Critiques:**
- Self: [What I got wrong]
- Agent B: [Their errors/omissions]
- Agent C: [Their errors/omissions]

**Agent B Critiques:**
...

**Agent C Critiques:**
...

### Round 3: Refined Answers (optional)

**Agent A Revised:**
...

### Verdict

**Consensus:** [What we agree on]
**Disagreement:** [What's disputed]
**Answer:** [Final synthesized answer]
**Confidence:** [High/Medium/Low]
```

## References

- Research: "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (Du et al., 2023)
- Related: Ensemble methods, Wisdom of Crowds, Delphi method
- See [references/examples.md](references/examples.md) for detailed debate examples
