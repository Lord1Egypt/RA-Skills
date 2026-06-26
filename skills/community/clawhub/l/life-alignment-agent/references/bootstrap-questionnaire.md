# Bootstrap Questionnaire

Use this when the user model is missing, weak, or clearly outdated.

## Operating Rules

- Ask at most 8 high-signal questions in the first round, and often fewer.
- Prefer concrete tradeoff questions over vague self-description prompts.
- Skip what is already known from prior files or prior turns.
- Accept higher upfront calibration cost only when the signal is genuinely high.
- Invite the user to provide existing artifacts when useful: resume, old plans, journals, test results, recurring dilemmas, or prior notes.
- After each round, synthesize what seems stable, what is tentative, what patterns are emerging, and what still matters.
- If the user is blocked, switch from broad questions to contrast questions.
- Do not wait for a perfect model before giving useful advice; bootstrap should improve action quality, not postpone it.

## Evidence Labels

When summarizing findings, tag them mentally as:

- `stable`: repeated, high-confidence understanding
- `working`: currently useful operating assumption
- `tentative`: hypothesis that needs more evidence

## Recommended Bootstrap Sequence

### Round 0: current pain and immediate use case

Start here when context is thin.

Try to learn:

- what the user actually wants this agent to help with first
- which current dilemma or confusion has the highest urgency
- whether the user needs immediate judgment, planning, or broader calibration

### Round 1: high-signal foundation

Cover the smallest set of questions that reveals the user's direction, phase, decision standards, and action friction.

### Round 2: targeted deepening

Only ask this if it will change the quality of recommendations.

Target one or two of:

- recurring dilemmas
- repeated failure modes
- energy and attention patterns
- relationship between ambition, security, autonomy, and meaning
- heartbeat preferences

### Round 3: recalibration

Use later when the user changes phase, repeatedly rejects the agent's assumptions, or shows new long-running patterns.

## Priority Dimensions

### 1. Direction

Ask questions like:

- If the next 3 to 5 years go well, what becomes meaningfully better?
- What kind of life or career outcome would feel like a real miss or trap?
- What are you trying to become more of, not just achieve more of?
- Which matters more in the next few years: building capability, building assets, building freedom, or building meaning?

### 2. Current Phase

Ask questions like:

- What is the most important phase you are in right now?
- What 3 to 6 month outcomes matter most in this phase?
- What is taking up too much mental bandwidth right now?
- What would make the next 90 days feel clearly better rather than merely busy?

### 3. Decision Standards

Ask questions like:

- When tradeoffs are real, what should usually win: compounding growth, income, autonomy, health, meaning, relationships, or stability?
- What recent decision felt hard, and what made it hard?
- What kind of regret do you fear more: missing upside or wasting years in the wrong direction?
- In this phase, what should not be sacrificed too easily?

### 4. Repeated Patterns

Ask questions like:

- What problem do you keep revisiting without truly solving?
- Where do you most often drift into low-value behavior?
- What pattern in your behavior helps you most? What pattern hurts you most?
- What do you repeatedly delay even when you know it matters?

### 5. Action Friction

Ask questions like:

- When you know what matters, what usually stops action: uncertainty, fear, perfectionism, exhaustion, distraction, or social friction?
- What type of nudge actually helps you start?
- When you fall off track, what tends to bring you back fastest?

### 6. Collaboration Contract

Ask questions like:

- Do you want strong recommendations by default, or more exploration first?
- Should the agent proactively check in on key commitments?
- What tone makes advice easiest for you to act on?
- When the agent thinks you are rationalizing drift, should it say that directly?

## Contrast Prompts

Use these when the user cannot answer directly:

- Which is worse right now: moving slowly in the right direction or moving fast in the wrong direction?
- Which matters more in this phase: building capability, protecting energy, or capturing opportunity?
- Which would bother you more three months from now: not trying, trying and failing, or getting trapped in maintenance work?
- Which is more dangerous for you lately: overthinking the right move or doing low-value work to feel productive?
- Which matters more right now: reducing confusion or increasing courage?

## Round Output

After each round, summarize:

1. Stable signals
2. Tentative signals
3. Repeated patterns or risks emerging
4. Missing but decision-relevant unknowns
5. Immediate implications for planning or advice
