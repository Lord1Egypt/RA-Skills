# Surface Naturalness Harness

## Purpose

Prevent final outputs from sounding like generic AI-generated text.

This harness runs after Draft Generator and before final output.

## Checkpoints

### 1. Internal Process Leakage

Fail if output exposes internal machinery without user request.

Examples:
- Story Kernel
- 内部编译
- 严格按流程
- Harness 检查如下
- ontology mapping
- runtime chain

Rewrite:
Output only the final user-facing text.

### 2. AI Sentence Pattern Overuse

Flag repeated use of:

- 核心是
- 本质上
- 不是……而是……
- 一方面……另一方面……
- 只做一件事
- 从 A 到 B
- 打造闭环
- 赋能
- 底层逻辑
- 形成体系化能力
- 可控、可复盘、可改进

These are not forbidden entirely, but repeated use creates AI-style writing.

### 3. Checklist Overload

For outputs under 500 Chinese characters:
- avoid bullet lists unless user asks
- avoid listing more than 3 components
- avoid "8 gates", "5 modules", "4 layers" unless essential

### 4. Excessive Abstraction

Fail if the first sentence contains too many abstract terms.

Bad:
"Harness engineering is a runtime constraint layer between the model and task execution."

Better:
"AI can give a fluent answer, but it can also make mistakes that are hard to notice."

### 5. Missing Human Entry Point

Fail if the text does not answer:
"Why should this audience care?"

### 6. Metaphor Control

For short outputs:
- use at most one analogy
- analogy must clarify the mechanism
- analogy must not replace the mechanism

### 7. Marketing Smell

Flag:
- overpromising
- grand slogans
- vague transformation claims
- inflated certainty

### 8. Manual-like Tone

Fail if the text sounds like a product manual but the user asked for explanation.

Rewrite from:
definition → list → slogan

To:
scene → problem → mechanism → consequence

### 9. Persona Overperformance

For persona-based outputs such as rapper, founder, investor, doctor, Douyin creator, or journalist:

- **Audience-native situation first.** Before choosing any stylistic device, search for a situation the audience lives in daily — a workflow friction, a recurring mistake, a known headache. Build the entry point from that situation. Do not merely add slang or rhythm to a generic explanation.
- **Analogy from work process, not identity performance.** The analogy should come from the audience's actual work process (e.g., for a rapper: mixing, mastering, punch-in, lyrical drift), not from cultural stereotypes about the audience.
- do not imitate stereotypes;
- do not overperform identity markers;
- prefer the audience's real workflow, real stakes, and real language environment — style should come from the scene, not from stereotypes;
- one or two domain-specific references are enough;
- style should sharpen the explanation, not become the content.

The litmus test: would someone who actually does this job recognize the voice as authentic, or as a caricature? If a founder reads "founder voice" and thinks "nobody talks like this" — fail. If a doctor reads "doctor voice" and thinks "this is what a screenwriter thinks doctors sound like" — fail.

Fail if:
- the persona dominates the mechanism (audience remembers the voice, forgets the point);
- identity markers pile up (too many slang terms, too many domain signals);
- the text reads as parody rather than explanation;
- the style comes from the narrator's imagination of the audience rather than the audience's actual context.

Rule: persona is delivery, not substance. Scene creates voice; stereotypes create noise. The controlling idea must survive the delivery.

## Rewrite Instruction

If the text fails this harness, rewrite it using:

```text
one concrete entry point
one clear problem
one mechanism
one consequence
no internal process language
```
