# Short Explanation Output Contract

## Applies When

Use this contract when:
- output length is under 500 Chinese characters
- user asks for a short explanation
- target audience is general public or non-technical
- user asks for "300 字介绍", "简单解释", "给普通人讲"

## Output Rules

1. Do not show internal reasoning.
2. Do not show Story Kernel.
3. Do not show tables.
4. Do not show bullet lists unless requested.
5. Start from audience entry point.
6. Use one analogy maximum.
7. Technical terms must be explained in context.
8. Avoid overclaiming.
9. End with practical value, not a slogan.
10. If audience is ambiguous, infer and write for the least technical plausible audience.

## Recommended Shape

```text
[Audience-relevant problem]
→ [Why existing method is not enough]
→ [What the concept does]
→ [Why it matters]
```

## Example

Topic:
Harness Engineering

Target audience:
zero AI background

Output:
AI can give a fluent answer, but it can also make mistakes that are hard to notice: using the wrong fact, sounding too certain, or changing the meaning of source material. Harness engineering is the set of checks placed before AI output is used in real work. It is like a pre-flight checklist: it does not replace the pilot, but it catches common and costly mistakes before takeoff. Its value is not making AI sound smarter, but making its output safer, easier to review, and easier to improve over time.
