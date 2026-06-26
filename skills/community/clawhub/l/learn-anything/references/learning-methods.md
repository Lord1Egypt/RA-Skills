# Learning Methods Reference

Deep dive on proven learning techniques.

## Spaced Repetition

**Principle:** Review material at increasing intervals to combat forgetting curve.

**Optimal intervals:**
| Review | Interval | Cumulative |
|--------|----------|------------|
| 1st | 1 day | Day 1 |
| 2nd | 3 days | Day 4 |
| 3rd | 1 week | Day 11 |
| 4th | 2 weeks | Day 25 |
| 5th | 1 month | Day 55 |

**Implementation:**
- Track when user completes each milestone
- Calculate next review date automatically
- Remind user when reviews are due

**Tools:**
- Anki (flashcards)
- RemNote
- Or simply: calendar reminders

## Feynman Technique

**Four steps:**
1. **Pick a concept** — Choose something to learn
2. **Teach it to a beginner** — Explain in simple terms (imaginary 12-year-old)
3. **Identify gaps** — Where did you struggle? What's unclear?
4. **Refine and simplify** — Fill gaps, use analogies

**Prompts to use:**
- "Explain [concept] as if I'm 12 years old"
- "How would you teach this to a complete beginner?"
- "What's a real-world analogy for [concept]?"

**Signs of true understanding:**
- No jargon without explanation
- Clear analogies
- Can answer "why does this work?"

## Active Recall

**Principle:** Retrieving information strengthens memory more than re-reading.

**Weak learning:**
- Re-reading notes
- Highlighting
- Watching videos passively

**Strong learning:**
- Quizzing yourself
- Explaining from memory
- Practice problems
- Flashcards

**Quiz types:**
1. **Recall** — "What is X?"
2. **Application** — "How would you use X in situation Y?"
3. **Comparison** — "What's the difference between X and Y?"
4. **Analysis** — "Why does X work this way?"

## Interleaving

**Principle:** Mix related topics rather than studying one at length.

**Blocked practice (less effective):**
```
Day 1: Only derivatives
Day 2: Only integrals
Day 3: Only series
```

**Interleaved (more effective):**
```
Day 1: Derivatives + integrals mixed
Day 2: Integrals + series mixed
Day 3: All three mixed
```

**When to interleave:**
- After basics are established
- Related concepts
- Preparing for varied application

## Pomodoro Technique

**Structure:**
1. 25 minutes focused work
2. 5 minute break
3. After 4 pomodoros: 15-30 minute break

**Benefits:**
- Reduces mental fatigue
- Creates urgency
- Easy to track progress

**Adaptations:**
- Some prefer 50/10 for deep work
- Adjust based on task complexity

## Dual Coding

**Principle:** Combine verbal and visual learning.

**Techniques:**
- Diagrams alongside explanations
- Mind maps for concepts
- Visual analogies
- Sketch notes

**When coding:** Flowcharts before implementation.

## Elaborative Interrogation

**Principle:** Ask "why" to deepen understanding.

**Questions:**
- Why does this work?
- Why is this the standard approach?
- Why not [alternative]?
- How does this connect to what I already know?

**Example:**
> "Python uses zero-based indexing." 
> → Why? Because it represents offset from start. 
> → Why offset? Because array pointers work that way.

## Concrete Examples

**Principle:** Abstract concepts become memorable with concrete instances.

**Pattern:**
1. Learn concept abstractly
2. Immediately generate 2-3 concrete examples
3. Create your own example
4. Test edge cases

**Example for "recursion":**
- Abstract: Function that calls itself with smaller input
- Concrete 1: Factorial calculation
- Concrete 2: Directory tree traversal
- Your example: [user generates]

## Retrieval Practice

**Types:**
| Type | Difficulty | Effectiveness |
|------|------------|---------------|
| Recognition (MCQ) | Low | Low |
| Cued recall (hints) | Medium | Medium |
| Free recall (no hints) | High | High |
| Application | Highest | Highest |

**Recommendation:** Prefer free recall and application over multiple choice.

---

## Putting It Together

**Optimal learning session:**
1. **Pre-study quiz** — Test what you already know (activates retrieval)
2. **Focused study** — 25 min pomodoro with the material
3. **Immediate recall** — Write summary from memory
4. **Elaboration** — Generate examples, ask "why"
5. **Spaced schedule** — Plan next review

**Weekly review:**
- Summarize week's learning
- Interleave related topics
- Self-test across all material
