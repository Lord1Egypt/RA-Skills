# Extraction Guide (English)

Methodology for extracting structured knowledge from books and learning materials.

## Extraction Objectives

Extract actionable, structured knowledge that can be matched to real-world situations. The goal is NOT to summarize the book — it is to identify discrete, named, reusable units of knowledge that a user can apply.

Every extracted item must be:
- **Faithful** to the source material (no reinterpretation)
- **Actionable** (a user can apply it to a situation)
- **Specific** (concrete steps or criteria, not vague advice)
- **Citable** (tied to a specific chapter/section)

## 1. Framework Extraction

A framework is a named method, process, or model with defined steps or components.

**How to identify:** Look for:
- Named methods (e.g., "The STATE Method", "The Eisenhower Matrix")
- Step-by-step processes the author prescribes
- Models with named components or axes (e.g., 2x2 matrices)
- Acronyms that encode a process (e.g., SMART, SWOT)

**Extract these fields:**

```markdown
## [Framework Name]

**Source:** Chapter [N], "[Section Title]"
**Type:** [Communication | Decision-making | Leadership | Strategy | ...]
**Domains:** [comma-separated domain tags]

### Description
[2-3 sentences: what it is and why it matters. Use the author's language.]

### Steps
1. [Step name] — [what to do]
2. ...

### Application Triggers
- [Situation where this framework applies]
- [Another situation]

### Anti-Patterns (When NOT to Use)
- [Situation where this is overkill or wrong]

### Related
- [[other-book/framework-name]]

### Key Quotes
- "[Direct quote]" (p. [N])
```

**Rules:**
- Only extract frameworks the author explicitly names or defines
- Include ALL steps if it's a process — no abbreviating
- Application triggers are critical — these become the search index
- Key quotes ground the extraction in source text

## 2. Principle Extraction

A principle is a core lesson, rule of thumb, or maxim — shorter and simpler than a framework.

**How to identify:** Look for:
- Statements the author repeats or emphasizes
- Rules of thumb ("always X before Y", "never do Z")
- Named principles ("The Stockdale Paradox")
- Conclusions the author draws from evidence

**Extract these fields:**

```markdown
## [Principle Name]

**Source:** Chapter [N]

### Description
[1-2 sentences capturing the principle.]

### When It Applies
- [Situation]
```

**Rules:**
- Use the author's own phrasing where possible
- If the author names it, use that name
- If unnamed, derive a concise descriptive name

## 3. Mental Model Extraction

A mental model is a way of thinking about problems — not a process to follow, but a lens to see through.

**How to identify:** Look for:
- "Think of it as..." or "Imagine..." constructions
- Metaphors the author develops into reasoning tools
- Framing devices (e.g., "silence vs. violence" as the two failure modes)

**Extract these fields:**

```markdown
## [Model Name]

**Source:** Chapter [N]

### Description
[How this model frames problems.]

### How to Use
[When and how to apply this lens.]
```

## 4. Anti-Pattern Extraction

An anti-pattern is something the book explicitly warns against.

**How to identify:** Look for:
- "Don't do X", "Avoid Y", "The mistake most people make..."
- Named anti-patterns ("The Sucker's Choice")
- Failure stories the author uses as warnings

**Extract these fields:**

```markdown
## [Anti-Pattern Name]

**Source:** Chapter [N]

### Description
[What the mistake is.]

### What to Do Instead
[The author's prescribed alternative.]
```

## 5. Case Study Extraction

A case study is a real-world example the author uses to illustrate a framework or principle.

**How to identify:** Look for:
- Named companies, people, or situations
- Stories that span more than a paragraph
- Before/after narratives

**Extract these fields:**

```markdown
## [Case Study Title]

**Source:** Chapter [N]
**Related Frameworks:** [list]

### Summary
[2-3 sentences: what happened.]

### Key Lesson
[What the author wants the reader to take away.]
```

**Rules:**
- Only extract case studies that illustrate a specific framework or principle
- Link each case study to the frameworks it illustrates
- Keep summaries factual — the lesson is the author's, not yours

## 6. Application Trigger Mapping

After extracting all items, build the application trigger index. This maps real-world situations to relevant frameworks and principles.

**Process:**
1. For each framework and principle, list 3-5 situations where it applies
2. Use natural language a user would use to describe the situation
3. Include variations (e.g., "giving feedback", "delivering criticism", "tough conversation")
4. Group triggers by theme (e.g., all feedback-related triggers together)

**Format:**
```markdown
### [situation phrase]
→ [Framework Name] ([Book Title]), [Principle Name] ([Book Title])
```

This index is what makes the advisor's situation-matching work. Invest time here.

## 7. Quality Criteria

A good extraction:
- Uses the author's terminology, not paraphrases
- Includes complete steps (not "see book for details")
- Has 3-5 application triggers per framework
- Includes at least 1 key quote per framework
- Links anti-patterns to the frameworks they warn against
- Cross-references related frameworks in other books (if present in KB)

## 8. Common Pitfalls

1. **Over-extracting**: Not every interesting paragraph is a framework. Only extract items with a name or clear structure.
2. **Being too vague**: "Be a good leader" is not a principle. "Always hear the data before sharing your conclusions" is.
3. **Missing steps**: If a framework has 5 steps, extract all 5. Don't summarize a 5-step process as 3 steps.
4. **Confusing examples with frameworks**: A story about Steve Jobs is a case study, not a framework — unless the author derives a named model from it.
5. **Skipping application triggers**: Without triggers, the advisor can't match situations to frameworks. This is the most commonly skipped step and the most important.
6. **Adding your own interpretation**: Extract what the author says, not what you think they mean. If ambiguous, quote directly.
7. **Ignoring anti-patterns**: Books often teach as much by what to avoid as by what to do. Don't skip the warnings.

## 9. Non-English Source Materials

When extracting from non-English materials:
- Store all content in the source material's original language
- Add an English translation in parentheses after each framework/principle name
- Example: "刺蝟原則 (Hedgehog Concept)"
- Application triggers should be in the source language
- Key quotes must be in the original language
