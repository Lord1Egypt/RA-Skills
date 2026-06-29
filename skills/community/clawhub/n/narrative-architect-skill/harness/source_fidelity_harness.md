# Source Fidelity Harness

## Purpose

Validate that the rendered output preserves the meaning and structural relationships of the source material, even after narrative transformation.

The Claim Harness checks whether claims are bounded. The Source Fidelity Harness checks whether the story built from those claims still reflects what the source actually says—not just at the fact level, but at the relationship level.

## Why This Harness Exists

Narrative transformation can distort meaning without violating any individual claim. A story can be "factually accurate" sentence by sentence, yet fundamentally misrepresent the source by:
- Reordering events to create false causation
- Elevating a minor point to central importance
- Omitting a counterweight that changes the meaning of what remains
- Reframing a descriptive observation as a prescriptive argument

Source fidelity is not fact-checking. It is meaning-checking.

## Checkpoints

### 1. Relationship Preservation

Check that the relationship between entities in the output matches the relationship in the source.

Fail if:
- Correlation in source → causation in output
- Coincidence in source → pattern in output
- One factor among many in source → primary factor in output
- Conditional relationship in source → unconditional relationship in output

Example:
Source: "Complication rates were lower in the barbed suture group, though the study was not powered to detect this difference."
Output: "Barbed sutures reduce complications." (correlation → causation, caveat removed)

### 2. Proportionality

Check that the emphasis in the output is proportional to the emphasis in the source.

Fail if:
- A footnote in the source becomes the headline in the output
- A primary finding in the source becomes a passing mention in the output
- The source's own qualification or limitation is omitted
- The source's own conclusion is contradicted by selective emphasis

Example:
Source: "The device shows promise but requires further validation in larger trials."
Output: "The device is a breakthrough." (source's own qualification removed)

### 3. Structural Integrity

Check that the source's argument structure survives narrative transformation.

Fail if:
- The source frames a finding as tentative → output frames it as conclusive
- The source presents multiple interpretations → output presents only one
- The source explicitly states "we don't know" → output fills the gap
- The source builds from premise to conclusion → output reverses the logic

### 4. Voice Appropriation

Check that the output does not put the source author's authority behind claims the source does not make.

Fail if:
- "According to..." followed by a claim the source doesn't make
- The source author's credibility is used to endorse a narrative the author would not endorse
- Disagreement within a field is presented as consensus

### 5. Gap Honesty

Check that gaps in the source material remain visible as gaps in the output.

Fail if:
- A gap in source knowledge is narratively smoothed over
- "We don't know" becomes implied "we know"
- An acknowledged limitation of the source is simply omitted

The mark of a trustworthy narrative is that it shows where it doesn't know. A narrative that hides gaps is propaganda regardless of how accurate its individual claims are.

### 6. Real Entity Fact Boundary

When the narrative object is a real company, public product, market category, person, institution, or current business entity, additional constraints apply.

The narrative must not invent concrete details unless supplied by the user or verified by source material.

Fail if the output fabricates:
- Specific numbers (revenue, market share, headcount, valuation, growth rate)
- Precise dates or timelines ("founded in 2003", "launched in 2018")
- Product names or version numbers not mentioned in source
- Client names or case studies not supplied
- Expansion history ("started with X, then moved into Y")
- Revenue model specifics not in source
- Comparative rankings ("the largest", "top 3", "market leader")
- Absolute claims about what a company does or does not do unless verified by source
- Illustrative examples presented as actual company facts

For capabilities and scope, prefer bounded framing over absolute statements.

Risky absolutes (fail unless explicitly sourced):

```text
"does not build databases"           → prefer "更偏向对接已有系统而非自建数据仓库"
"replaces existing systems"          → prefer "通常叠加在已有系统之上"
"never stores client data"           → prefer "公开材料更强调数据治理和权限控制"
"all information goes through..."    → prefer "核心能力之一是将分散数据映射为统一视图"
```

Bounded phrasing toolkit:

```text
可以理解为...          instead of inventing a founding story
核心之一              instead of "the most important"
更准确地说...          instead of fabricating precision
常见用法是...          instead of claiming exclusivity
通常被认为是...        instead of asserting consensus
更像                  instead of "is" for capabilities
通常                  instead of "always" or "never"
更偏向                instead of "replaces" or "eliminates"
```

### Platform-Style and Persona-Style Boundaries

For outputs rendered in platform-specific voices (Douyin, Twitter, LinkedIn) or persona voices (rapper, founder, doctor, journalist):

- **Metaphor must not narrow product scope.** A metaphor that makes the mechanism vivid but shrinks the company's actual scope is a fidelity violation. "它就像一个翻译器" may undersell; test if the metaphor still holds for the full product range.

- **Contrast phrases must be checked carefully.** "不是 X, 而是 Y" is dangerous when describing real companies with broad product scope. A company may do Y primarily but also do X in specific contexts, or may evolve to include X later.

- **Prefer "不只是 X" over "不是 X".** When the entity has broader or evolving capabilities, negation narrows while inclusion preserves openness:

```text
"不只是数据分析"      instead of "不是数据分析公司"
"不限于政府业务"      instead of "不做政府业务"
"核心不在这里"        instead of "不涉及这个方向"
```

- **Avoid declaring what a real company does not do unless explicitly verified by the source.** Even well-known limitations can shift. A company that "doesn't do consumer products" today may acquire a consumer division tomorrow. The narrative should not commit to a negative that might become false.

The test: if the company announces a new product line tomorrow, would the narrative still be accurate? If not, the negation was too absolute.

The test: if the company's own leadership would not recognize the description, the narrative has over-reached.

### Child Audience Simplification Boundary

When simplifying for children, analogy may replace surface details but must not replace the real mechanism.

The output should preserve three things:

1. **What the system helps decide.** A toy going to Thailand is a stand-in for a real product entering a real market. If the analogy removes the decision, it removes the value.
2. **What risk it reduces.** "以前要两年，到处问人，走错了路钱就白花了" — this is the real stake behind the game metaphor. Do not remove it for the sake of simplicity.
3. **What it cannot guarantee.** The output must not imply the system always finds the best answer, works instantly for any product, or replaces human judgment.

Fail if:
- the analogy replaces the mechanism ("it's like a magic map" with no further explanation);
- the stakes are removed to make the text "lighter";
- the output implies guarantees ("it will definitely work", "you'll always win");
- the child cannot answer "what does this system actually do?" after multiple game metaphors.

This does not forbid storytelling. Metaphor, analogy, scene, and structural contrast remain valid. But the facts within the story must trace to source, not to the narrator's imagination.

This does not forbid storytelling. Metaphor, analogy, scene, and structural contrast remain valid. But the facts within the story must trace to source, not to the narrator's imagination.

## Rewrite Instruction

If the output fails this harness:

For minor failures (emphasis drift, voice appropriation):
- Return to Main Renderer with specific structural corrections

For major failures (relationship distortion, gap suppression):
- Return to Story Kernel Builder
- The kernel may have been built on a misreading of the source
- Re-extract the kernel with the corrected understanding

## Relationship with Claim Harness

Claim Harness: checks individual statements for boundary violation.
Source Fidelity Harness: checks the whole narrative for meaning distortion.

Both must pass. Passing one does not excuse failing the other.

A narrative that passes Claim Harness but fails Source Fidelity Harness is factually bounded but structurally dishonest.
A narrative that passes Source Fidelity Harness but fails Claim Harness is structurally faithful but factually loose.

Neither is acceptable output.

## High-Profile Entity Fact Boundary

When the output references real public figures, major companies, public products, institutions, or current technologies:

1. Do not make categorical claims unless sourced.
2. Do not overstate current product status.
3. Do not say what a product "is not" unless verified.
4. Do not attribute motives, values, or beliefs to a person unless sourced or user-provided.
5. Use bounded language for public products and companies.

Risky:

```text
FSD is not a driver-assist feature.
He values zero bullshit.
Their story is uncontrolled.
```

Safer:

```text
FSD is often framed through driver-assistance language, while the broader autonomy story is more complex.
The pitch should be short, concrete, and testable.
Hard technical work can be judged through the wrong frame before the team has translated what changed.
```

## Public Figure Rule

For public figures, distinguish between:

```text
publicly observable facts
user-provided assumptions
public reputation
assistant inference
unsupported speculation
```

Do not present inference as fact.
