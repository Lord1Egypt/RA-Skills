# Reasoning & Problem-Solving Engine

Structured thinking frameworks for any problem — from simple decisions to complex multi-variable analysis.

---

## 1. Problem Decomposition

### The MECE Principle
**Mutually Exclusive, Collectively Exhaustive** — break problems into non-overlapping parts that cover everything.

```
Problem: "Website is slow"
├── Frontend
│   ├── Large assets (images, fonts)
│   ├── Unoptimized JavaScript
│   └── Render-blocking resources
├── Backend
│   ├── Slow database queries
│   ├── Unoptimized code
│   └── Missing caching
├── Network
│   ├── DNS resolution
│   ├── CDN configuration
│   └── Geographic distance
└── Infrastructure
    ├── Server capacity
    ├── Load balancing
    └── Resource limits
```

### The 5 Whys
Keep asking "why" until you find root cause.

```
1. Why is the app crashing? → Out of memory
2. Why is it out of memory? → Memory leak in session handler
3. Why is there a leak? → Sessions not cleaned up on disconnect
4. Why aren't they cleaned up? → No disconnect event handler
5. Why not? → Wasn't in the original spec
→ Root cause: Missing disconnect handler
```

### First Principles Thinking
Strip assumptions. Rebuild from facts.

```
Assumption: "We need a database for user data"
First principle: "We need to store and retrieve user data"
Alternatives: File storage, in-memory cache, localStorage, 
external API, no storage (stateless)
→ Question: Do we actually need persistence?
```

---

## 2. Decision Frameworks

### Decision Matrix
Score options against weighted criteria.

| Criteria (weight) | Option A | Option B | Option C |
|---|---|---|---|
| Speed (30%) | 8 × 0.3 = 2.4 | 6 × 0.3 = 1.8 | 9 × 0.3 = 2.7 |
| Cost (25%) | 5 × 0.25 = 1.25 | 9 × 0.25 = 2.25 | 4 × 0.25 = 1.0 |
| Reliability (25%) | 7 × 0.25 = 1.75 | 7 × 0.25 = 1.75 | 8 × 0.25 = 2.0 |
| Ease (20%) | 6 × 0.2 = 1.2 | 8 × 0.2 = 1.6 | 5 × 0.2 = 1.0 |
| **Total** | **6.6** | **7.4** | **6.7** |

### Pros/Cons with Weight
Not all pros/cons matter equally. Assign importance.

### Eisenhower Matrix (Prioritization)
| | Urgent | Not Urgent |
|---|---|---|
| **Important** | Do now | Schedule |
| **Not Important** | Delegate | Eliminate |

### OODA Loop (Rapid Decisions)
**Observe** → **Orient** → **Decide** → **Act** → Repeat

---

## 3. Logical Reasoning

### Deduction (General → Specific)
```
All servers need monitoring (premise)
This is a server (observation)
∴ This server needs monitoring (conclusion)
```

### Induction (Specific → General)
```
Server A crashed without monitoring
Server B crashed without monitoring
Server C crashed without monitoring
∴ Servers without monitoring tend to crash (hypothesis)
```

### Abduction (Best Explanation)
```
The server crashed
Disk-full errors cause crashes
The disk was 99% full
∴ Disk full is the most likely cause (best guess)
```

### Common Logical Fallacies
- **Post hoc**: A happened before B, so A caused B (wrong)
- **Appeal to authority**: Expert said it, so it's true (check evidence)
- **False dilemma**: Only two options exist (usually more)
- **Slippery slope**: A will inevitably lead to Z (usually won't)
- **Straw man**: Arguing against a weaker version of the point

---

## 4. Critical Analysis

### Source Evaluation
| Check | Question |
|---|---|
| Authority | Who wrote this? Expertise? |
| Currency | When was this written? Still valid? |
| Bias | What's the author's motivation? |
| Evidence | Are claims backed by data? |
| Corroboration | Do other sources agree? |
| Logic | Does the reasoning hold? |

### Assumption Checking
Before acting on any plan, list assumptions:
1. What am I assuming is true?
2. What if that assumption is wrong?
3. How would I verify it?
4. What's my fallback if it's wrong?

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| API rate limit | High | Medium | Add retry with backoff |
| Data loss | Low | Critical | Automated backups |
| Breaking change | Medium | High | Version pinning |

---

## 5. Creative Problem-Solving

### Lateral Thinking
- What if we did the opposite?
- What if constraints didn't exist?
- What would [different industry] do?
- Can we remove the problem instead of solving it?

### SCAMPER Method
- **S**ubstitute — What can be replaced?
- **C**ombine — What can be merged?
- **A**dapt — What can be borrowed?
- **M**odify — What can be changed?
- **P**ut to other use — What else can it do?
- **E**liminate — What can be removed?
- **R**everse — What if we did it backwards?

### Brainstorming Rules
1. Defer judgment (generate first, evaluate later)
2. Go for quantity (more ideas = better chance of good ones)
3. Build on others' ideas ("yes, and...")
4. Encourage wild ideas
5. Stay focused on the problem

---

## 6. Systematic Debugging

### Binary Search Isolation
```
Full pipeline: A → B → C → D → E → Output
Test: A → B → [checkpoint] ✓
Test: C → D → [checkpoint] ✗ ← Problem in C or D
Test: C → [checkpoint] ✓
Test: D → [checkpoint] ✗ ← Problem is D
```

### Change Analysis
What changed recently?
- Code changes (git log)
- Config changes (diff configs)
- Data changes (schema drift)
- Environment changes (versions, OS)
- External changes (APIs, dependencies)

### Rubber Duck Debugging
Explain the problem out loud (or in writing) step by step.
The act of explaining often reveals the answer.

---

## 7. Thinking Routines

### Before Starting Any Task
1. What am I trying to achieve?
2. What do I already know?
3. What don't I know?
4. What's the simplest approach?
5. What could go wrong?

### After Completing Any Task
1. Did it achieve the goal?
2. What went well?
3. What could be better?
4. What did I learn?
5. What would I do differently next time?

### When Stuck
1. Restate the problem differently
2. Break it into smaller pieces
3. Try a completely different approach
4. Look for similar solved problems
5. Ask for input (user, web, docs)
