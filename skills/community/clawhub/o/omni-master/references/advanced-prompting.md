# Advanced Prompting Engine

Transform any input — no matter how vague, broken, or incomplete — into a precise, actionable plan.

---

## 1. Prompt Interpretation Protocol

### When Input Is Unclear
Don't ask "What do you mean?" — instead, infer intent and state your interpretation:

```
User: "make it faster"
Interpretation: "I'll assume you mean the script we just ran.
Optimizing for execution speed — switching to compiled approach
and adding caching. Correct me if you meant something else."
```

### Prompt Enhancement Pipeline
```
Raw Input → Classify Intent → Fill Gaps → Clarify Scope → Execute
```

1. **Classify Intent**: What does the user actually want?
   - Create / Fix / Explain / Analyze / Optimize / Compare / Teach
   
2. **Fill Gaps**: What's missing?
   - Context (what system/file/project?)
   - Constraints (time, resources, platform?)
   - Output format (file, message, table, code?)
   - Success criteria (how to know it worked?)

3. **Clarify Scope**: How much is enough?
   - Quick answer vs deep dive
   - One file vs entire project
   - MVP vs production-ready

4. **Default Behaviors** (when not specified):
   - Concise over verbose
   - Working code over pseudocode
   - Best practices over quick hacks
   - Explain non-obvious choices

---

## 2. Prompt Patterns & Templates

### Zero-Shot Prompting
Direct instruction, no examples needed for clear tasks.
```
"Summarize this article in 3 bullet points"
```

### Few-Shot Prompting
Provide examples to guide output format.
```
"Convert these dates. Example: 'next tuesday' → 2026-04-07
Now convert: 'in 3 weeks', 'end of month'"
```

### Chain-of-Thought (CoT)
Break complex reasoning into visible steps.
```
"Walk through this step by step:
1. What data do we have?
2. What are we trying to find?
3. What method applies?
4. Execute the calculation."
```

### Role-Based Prompting
Assign expertise to frame the response.
```
"As a senior security engineer, review this config..."
"As a teacher explaining to a 10-year-old..."
"As a product manager prioritizing features..."
```

### Constraint-Based Prompting
Set boundaries for focused output.
```
"In under 100 words, explain X"
"Using only Python standard library"
"Without leaving the current directory"
```

### Meta-Prompting
Ask the model to improve its own prompt.
```
"Before answering, first identify what information is missing,
then either ask for it or state your assumptions."
```

---

## 3. Handling Bad Prompts

### Vague Prompts
**Input**: "fix my code"
**Response Strategy**: 
1. Read the code in the workspace
2. Run it to see the error
3. Fix the specific issue
4. Explain what was wrong

### Contradictory Prompts
**Input**: "make it simple but also add everything"
**Response Strategy**:
1. Identify the contradiction
2. Propose a balanced approach
3. "I'll keep the API simple while adding features behind flags"

### Impossible Prompts
**Input**: "make it never crash"
**Response Strategy**:
1. Acknowledge the ideal
2. Set realistic expectations
3. "I'll add comprehensive error handling so it degrades gracefully"

### Scope-Confused Prompts
**Input**: "build me an app"
**Response Strategy**:
1. Ask one focused clarifying question
2. Or: build the simplest version and iterate
3. "Building a minimal web app — starting with a single-page HTML/JS todo app. Tell me if you need something different."

### Context-Free Prompts
**Input**: "why isn't it working?"
**Response Strategy**:
1. Check recent session context
2. Look at recent files/commands
3. Make best guess based on environment
4. "Assuming you mean [X] based on our last session — here's what I found..."

---

## 4. Response Quality Framework

### The CLEAR Framework
- **C**oncise — No filler, every word earns its place
- **L**ogical — Structured flow, each point builds on the last
- **E**vidence-based — Cite sources, show data, link references
- **A**ctionable — End with what to do next
- **R**elevant — Stay on topic, cut tangents

### Output Adaptation by Audience
| Audience | Style | Detail Level |
|---|---|---|
| Developer | Code-first, technical | High |
| Manager | Summary-first, business impact | Medium |
| Beginner | Analogies, step-by-step | Guided |
| Expert | Assumptions stated, edge cases | Deep |

### Adaptive Verbosity
- Simple question → short answer
- Complex question → structured answer
- Ambiguous question → best interpretation + offer to adjust
- Dangerous question → careful answer + warnings

---

## 5. Prompt Repair Techniques

### Auto-Complete Missing Context
```
User: "deploy it"
Repair: "Deploying [the project in /root/.openclaw/workspace]
to [local development server]. For production deployment,
tell me the target platform."
```

### Disambiguate Homonyms
```
User: "run the test"
Repair: "Running `npm test` (JavaScript test suite).
If you meant Python tests, say 'run pytest'."
```

### Infer Temporal Context
```
User: "check the status"
Repair: "Checking status of [most recent operation /
system health / running services]. Be specific if you
need something else."
```

### Normalize Terminology
```
User: "make a db for the thing"
Repair: "Creating an SQLite database for [project inventory].
Tell me if you meant a different data store or entity."
```

---

## 6. Iterative Refinement

### Single-Shot isn't Always Enough
For complex tasks, use progressive refinement:

1. **Draft 1**: Quick version, get the structure right
2. **Review**: Check against requirements
3. **Draft 2**: Fill in details, fix issues
4. **Polish**: Optimize, clean up, add edge cases
5. **Deliver**: Final version with summary

### Feedback Loop
- Deliver initial result
- Ask: "Is this what you needed, or should I adjust?"
- Adapt based on response
- Log the preference for future sessions
