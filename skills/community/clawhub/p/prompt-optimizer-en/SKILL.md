---
name: prompt-optimizer
description: Iterative prompt optimizer for complex tasks. Strictly implements ACON's two-stage iterative optimization + APE automatic prompt engineering. Only triggers when user explicitly requests it, actively collects feedback after optimization, supports multi-round iteration until satisfied.
usage: Only activate when user explicitly says "optimize prompt", "improve prompt", "refine instruction", never auto-trigger.
author: Based on arXiv:2510.00615 (ACON), arXiv:2211.01910 (APE)
license: MIT
tags:
  - prompt-optimization
  - acon
  - ape
  - iterative
  - complex-tasks
---

## Atomic Optimization Methodology

### 🔬 Stage 1: Input Parsing & Critical Signal Extraction (ACON Paper §3.1)
**Input**: User's original prompt
**Operations**:
1. Intent Locking: Extract core task goal T, ensure all subsequent optimizations never deviate from T
2. Critical Signal Extraction (ACON-defined mandatory signals):
   - ✅ Role Definition R: Expert role specified by user
   - ✅ Task Goal T: What the core task is
   - ✅ Constraints C: Boundary rules, prohibitions
   - ✅ Output Format F: Output structure/format requested by user
   - ✅ Variable Placeholders V: All `{{variable_name}}`
   - ✅ Examples E: Few-shot examples provided by user
   - ✅ Tool Rules U: When and how to use tools
   - ✅ Success Criteria S: What constitutes a good output
3. Baseline Measurement: Record original prompt token length L₀

---

### 🚀 Stage 2: APE Utility Enhancement (arXiv:2211.01910 Automatic Prompt Engineering)
**Goal**: Turn vague prompts into expert-level instructions, improve utility
**Operations (Strict Order)**:
1. Candidate Generation: Based on original prompt, generate 5 candidate instructions in different styles
   - Candidate 1: Structured instruction version
   - Candidate 2: Expert role version
   - Candidate 3: Constraint reinforcement version
   - Candidate 4: Format clarification version
   - Candidate 5: Logic optimization version
2. Candidate Scoring (APE paper scoring mechanism):
   - Clarity: Are instructions clear and unambiguous (0-10)
   - Completeness: Does it include all critical signals (0-10)
   - Effectiveness: Can it guide the model to produce high-quality output (0-10)
3. Optimal Selection: Choose the candidate with highest total score, as utility-enhanced version P₁
4. Validation: Verify P₁ 100% preserves all critical signals, no change to original intent

---

### 📦 Stage 3: ACON Compression Optimization (ACON Paper §3.3 Two-Stage Optimization)
**Goal**: Compress token length without breaking functionality
**Operations (Strict Order: Utility first, then compression)**:
1. Redundancy Analysis: Analyze redundant content in P₁
   - Duplicate instructions and requirements
   - Fluff, jargon, ineffective expressions
   - Verbose statements that can be simplified
2. Selective Compression:
   - Only remove redundancy, NEVER delete critical signals
   - Merge duplicate content
   - Rewrite with more concise language, keep semantics unchanged
3. Functional Equivalence Validation:
   - Ensure compressed P₂ is functionally identical to P₁
   - Ensure all critical signals are fully preserved
   - Ensure no change to original task goal
4. Length Control: Adjust compression degree based on λ parameter (performance-cost tradeoff)
   - Default λ=0.5: Balanced mode
   - If user feedback "too long", automatically increase λ to 0.8 for more compression
   - If user feedback "not effective enough", automatically decrease λ to 0.2 to reduce compression

---

### 📤 Stage 4: Output & Feedback Collection
**Operations**:
1. Output optimized prompt P₂, wrapped in code block for easy copying
2. Actively ask for user feedback:
   ```
   Optimization complete. Does this version meet your needs?
   If there's anything unsatisfactory, please let me know, such as:
   - Not effective enough?
   - Still too long?
   - Some constraints/formats not preserved?
   - Other issues?
   I'll continue iterating based on your feedback.
   ```

---

### 🔄 Stage 5: Iterative Optimization (ACON Paper's R-round Iteration Mechanism)
**When user provides feedback, execute the following**:
1. Feedback Parsing: Identify feedback type
   - Type A: Not effective enough → Go back to Stage 2, re-run APE utility enhancement, add constraints
   - Type B: Too long → Go back to Stage 3, re-run ACON compression, increase λ
   - Type C: Some content not preserved → Check critical signals, restore missing parts
   - Type D: Other requirements → Adjust based on user's specific request
2. Re-run Optimization: Adjust parameters based on feedback, run two-stage optimization again
3. Validation: Ensure new version preserves core task goal, and solves the user's feedback issue
4. Output new optimized version, ask for feedback again
5. Repeat until user indicates satisfaction

---

## Strict Rules (Guarantee Effectiveness)
- ✅ Every step has validation, ensure no damage to original functionality
- ✅ Critical signals are NEVER deleted, 100% preserved
- ✅ Strictly follow "utility first, then compression" order, never reverse
- ✅ Each iteration re-validates, ensure it gets better with each round
- ✅ For complex tasks, prioritize functional integrity, compression is optional
- ❌ Never auto-trigger, only work when user explicitly requests
- ❌ No comparisons or analysis, only output optimized results
- ❌ No extra explanations unless explicitly requested
