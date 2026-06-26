# Edge Case Skill — Comments Only

This skill has security-related keywords only in comments and string literals,
which should ideally NOT trigger findings (testing FP resilience).

## Instructions

Help users understand security concepts by explaining them.

```javascript
// This is a comment about "ignore all previous instructions" — it's just an example string
// The term "system prompt" appears here for educational purposes
const educationalText = "Example of prompt injection: 'ignore all previous instructions'";
const demo = "This shows how eval() could be misused, but we don't actually call it";

function explain(topic) {
  // We discuss exec() and child_process as security concepts
  return `Security topic: ${topic} — always validate inputs`;
}
```

Note: This file discusses security concepts for education. The regex scanner
may flag some of these as they appear in string/comment context.
