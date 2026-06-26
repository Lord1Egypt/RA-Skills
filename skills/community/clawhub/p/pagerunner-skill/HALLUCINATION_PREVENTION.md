# Hallucination Prevention: Semantic Metadata & Result Clarity

How to prevent LLMs from making wrong assumptions about tool responses.

---

## The Incident: "25 likes vs 25 views"

### What Happened

An agent evaluated a tweet's metrics:

```javascript
const metrics = await evaluate(sessionId, tabId, `
  [
    document.querySelectorAll('.like-btn').length,
    document.querySelectorAll('.reply-btn').length
  ]
`);
// Result: [25, 2]
```

**Agent's assumption:** "25 likes, 2 replies"

**Reality:** "25 views, 2 likes"

The agent was wrong. Arrays have no inherent field labels. The agent guessed.

### Why It Happened

```javascript
// [25, 2] could mean:
// - 25 likes + 2 replies? ← agent guessed
// - 25 views + 2 likes? ← actual
// - 25 bookmarks + 2 shares?
// - 25 retweets + 2 quotes?

// No way to know from the data structure alone.
```

---

## The Fix: Always Return Labeled Objects

```javascript
// ❌ WRONG — ambiguous
return [25, 2];

// ✅ RIGHT — unambiguous
return {
  likes: 25,
  replies: 2
};
```

**Rule:** Never return arrays of primitives from `evaluate()`. Return labeled objects or primitives only.

```javascript
// ✅ OK — single primitive
return document.title;  // Returns: "My Page"

// ✅ OK — labeled object
return { title: "My Page", length: 4200 };

// ✅ OK — array of labeled objects
return Array.from(document.querySelectorAll('.item')).map(el => ({
  name: el.querySelector('.name').textContent,
  price: parseFloat(el.querySelector('.price').textContent)
}));

// ❌ WRONG — array of primitives
return document.querySelectorAll('.item').length;  // Wait, this is a number, OK

// ❌ WRONG — array of arrays
return Array.from(document.querySelectorAll('.item')).map(el => [
  el.querySelector('.name').textContent,
  el.querySelector('.price').textContent
]);
```

---

## Semantic Metadata: How Pagerunner Prevents This

Pagerunner wraps every MCP tool response with metadata blocks that provide context.

### Metadata Structure

```json
{
  "content": [
    {
      "type": "text",
      "text": "...actual response from tool..."
    },
    {
      "type": "text",
      "text": "{...metadata block...}"
    }
  ]
}
```

**Read the metadata block.** It tells you:
- What tool returned this
- What type the result is
- If it's ambiguous (array)
- What went well or went wrong

### Metadata for evaluate()

```json
{
  "_tool": "evaluate",
  "_result_type": "array",
  "_warning": "Result is an array — field meanings cannot be inferred. Always use labeled objects: { field1: val1, field2: val2 }"
}
```

**When you see `_result_type: "array"` with `_warning`:**
- The result is ambiguous
- Re-run evaluate() with labeled returns
- Example: `{ likes: 25, replies: 2 }` instead of `[25, 2]`

**When result is an object:**

```json
{
  "_tool": "evaluate",
  "_result_type": "object",
  "_hint": "Labels are clear. Proceed."
}
```

### Metadata for wait_for()

Disambiguates what actually happened:

```json
{
  "_tool": "wait_for",
  "_condition_type": "selector",
  "_condition_met": true,
  "_note": "Selector found within timeout. Proceed with next action."
}
```

**vs fixed delay:**

```json
{
  "_tool": "wait_for",
  "_condition_type": "fixed_delay",
  "_condition_met": false,
  "_note": "Fixed delay completed. No condition was checked. Page may not be ready."
}
```

**Why it matters:** If you used `wait_for(ms: 2000)`, you don't know if the page finished loading. Metadata tells you exactly what happened.

### Metadata for list_tabs()

```json
{
  "_tool": "list_tabs",
  "_total": 3,
  "_schema": {
    "target_id": "Use in navigate, get_content, click, evaluate, etc.",
    "url": "Current page URL",
    "title": "Page title (may be sanitized)"
  }
}
```

**Describes every field** so you know what each value means.

### Metadata for list_sessions()

```json
{
  "_tool": "list_sessions",
  "_total": 2,
  "_schema": {
    "id": "session_id for open_session / close_session / list_tabs",
    "profile": "Chrome profile name",
    "stealth": "boolean — stealth mode enabled?",
    "anonymize": "boolean — PII anonymization enabled?"
  }
}
```

---

## The Three Rules

### Rule 1: Always Return Labeled Objects from evaluate()

```javascript
// ❌ BAD
return [count, selected, disabled];

// ✅ GOOD
return { count, selected, disabled };
```

If you're tempted to return an array, add labels:

```javascript
// ❌
return [25, 2];

// ✅ Add a label
return { likes: 25, replies: 2 };

// ✅ Or explicit structure
return {
  engagement: {
    likes: 25,
    replies: 2
  }
};
```

### Rule 2: Read Metadata Blocks

Every tool response includes metadata. Check it:

- `_warning` fields mean something went wrong or is ambiguous
- `_schema` fields describe the returned structure
- `_condition_met` for wait_for tells you what happened
- `_result_type: "array"` + `_warning` means re-run with labeled results

### Rule 3: Use get_content + evaluate Strategically

**get_content:** Read the page structure (HTML as text)

```javascript
const content = await get_content(sessionId, tabId);
// Returns: "Product Name: Widget | Price: $19.99 | Qty: 5 in stock"
```

**evaluate:** Extract specific values programmatically

```javascript
const data = await evaluate(sessionId, tabId, `
  ({
    name: document.querySelector('.product-name').textContent,
    price: parseFloat(document.querySelector('.price').textContent.replace('$', '')),
    inStock: parseInt(document.querySelector('[data-qty]').getAttribute('data-qty'))
  })
`);
// Returns: { name: "Widget", price: 19.99, inStock: 5 }
```

Never mix:

```javascript
// ❌ WRONG — parsing HTML string in your head
const content = await get_content(...);
// Claude reads "Product Name: Widget | Price: $19.99"
// Claude tries to parse: "OK so first is the product, second is price..."
// Error-prone and slow

// ✅ RIGHT — structured extraction
const data = await evaluate(..., "({name: ..., price: ...})");
// Clear structure, no ambiguity
```

---

## Case Study: Correct Form Verification

**Wrong approach (array):**

```javascript
// Agent wants to verify form validation worked
const result = await evaluate(sessionId, tabId, `
  [
    document.querySelector('input[name="email"]').hasAttribute('aria-invalid'),
    document.querySelector('.error-message').textContent
  ]
`);
// Returns: [true, "Email is invalid"]
// Agent guesses: field is invalid? Or error message is field validity?
// Ambiguous!
```

**Right approach (labeled object):**

```javascript
const result = await evaluate(sessionId, tabId, `
  ({
    emailFieldHasError: document.querySelector('input[name="email"]').hasAttribute('aria-invalid'),
    errorMessage: document.querySelector('.error-message').textContent
  })
`);
// Returns: { emailFieldHasError: true, errorMessage: "Email is invalid" }
// Clear and unambiguous!
```

---

## Common Hallucination Patterns & Fixes

### Pattern 1: Array Result with Unknown Field Order

**Agent hallucinates:** Assumes first field is X, second is Y

**Fix:** Return labeled object

```javascript
// ❌ Hallucination risk
return [total, completed, pending];  // Agent guesses order

// ✅ Safe
return { total, completed, pending };
```

### Pattern 2: Boolean Result Misinterpreted

**Agent hallucinates:** Assumes true/false means something other than intended

**Fix:** Return labeled boolean with context

```javascript
// ❌ Risk
return document.querySelector('.save-btn').disabled;  // Agent: "Button is disabled, abort"

// ✅ Safe
return { saveButtonReady: !document.querySelector('.save-btn').disabled };  // Clear intent
```

### Pattern 3: String Result with No Context

**Agent hallucinates:** Assumes string format (JSON? plain text? markdown?)

**Fix:** Return structured data

```javascript
// ❌ Risk
return document.querySelector('.status').textContent;  // "success" — agent misinterprets

// ✅ Safe
return { status: document.querySelector('.status').textContent, statusCode: 200 };
```

---

## Debugging Ambiguous Results

### Step 1: Check Metadata

If metadata says `_warning: "...array..."`, the result is ambiguous. Re-run.

### Step 2: Add Labels

Modify the evaluate() to return labeled objects:

```javascript
// Before (ambiguous)
return [a, b, c];

// After (clear)
return {
  firstValue: a,
  secondValue: b,
  thirdValue: c
};
```

### Step 3: Verify Structure

```javascript
const result = await evaluate(...);
console.log(result);  // Should print: { field1: value1, field2: value2, ... }

// If you see: [value1, value2, ...] — you made an array, fix it!
```

---

## Metadata Reference

### evaluate()

```json
{
  "_tool": "evaluate",
  "_result_type": "primitive|array|object",
  "_warning": "optional — present if result is array",
  "_hint": "optional — advice on how to fix"
}
```

### wait_for()

```json
{
  "_tool": "wait_for",
  "_condition_type": "selector|url|fixed_delay",
  "_condition_met": true|false,
  "_note": "What actually happened"
}
```

### list_tabs(), list_sessions()

```json
{
  "_tool": "tool_name",
  "_total": number,
  "_schema": { "field": "description", ... }
}
```

### navigate()

```json
{
  "_tool": "navigate",
  "_requested_url": "url",
  "_note": "Navigation dispatched. Use wait_for before next action."
}
```

### click(), fill(), type_text(), select(), scroll()

```json
{
  "_tool": "tool_name",
  "_selector": "selector_used",
  "_success": true,
  "_note": "Action succeeded. If async, use wait_for before next action."
}
```

---

## Best Practices

1. **Always label evaluate() results**
   - ✅ `{ likes: 25, replies: 2 }`
   - ❌ `[25, 2]`

2. **Read metadata after every tool call**
   - Look for `_warning` and `_result_type` fields
   - If array + warning, re-run with labels

3. **Use get_content for structure, evaluate for extraction**
   - get_content: "What does the page look like?"
   - evaluate: "Extract specific values"

4. **Test with sample data**
   - Before deploying, run evaluate() on real pages
   - Verify results make sense
   - Check metadata for warnings

5. **Iterate on ambiguous results**
   - If metadata warns of array, refactor to object
   - Re-run and verify
   - No guessing allowed

---

## FAQ

**Q: What if I need to return an array of values?**
A: Use an array of objects with labels:
```javascript
return [
  { id: 1, name: "Item A", price: 10 },
  { id: 2, name: "Item B", price: 20 }
];
```
Never:
```javascript
return [[1, "Item A", 10], [2, "Item B", 20]];
```

**Q: What if a field value is an array?**
A: That's fine — the structure is still labeled:
```javascript
return {
  userEmails: ["john@example.com", "jane@example.com"],
  userNames: ["John", "Jane"]
};
```

**Q: Can I return nested objects?**
A: Yes! As long as field names are clear:
```javascript
return {
  engagement: { likes: 25, replies: 2 },
  metrics: { impressions: 100, ctr: 0.25 }
};
```

**Q: How do I know if a result is ambiguous?**
A: Check metadata. If `_warning` is present and mentions "array", re-run with labels.

**Q: Do I need to read metadata every time?**
A: For critical workflows (ICP 3 security, ICP 4 pipelines), yes. For dev workflows, check when something looks wrong.
