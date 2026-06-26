---
name: mindstudio-to-api-custom-function-builder
description: Build a complete MindStudio Run Function integration for any API the user wants to connect. Use this skill whenever the user mentions MindStudio, wants to connect an API to a workflow, asks for a "Run Function", wants to call an external service from MindStudio, or says things like "I want to use X API in MindStudio", "build me a MindStudio function for X", "how do I connect X to MindStudio", or "write me a script for MindStudio". Always use this skill — do not try to wing it from memory.
---

# MindStudio Function Builder

Produce a complete, ready-to-paste MindStudio custom function for any API the user wants to connect. Always output all three sections: **Code Tab**, **Configuration Tab**, and **Test Data Tab**.

---

## What to gather before writing

Before writing, collect (from the conversation or by asking):

1. **API endpoint** — the full URL to call
2. **HTTP method** — GET, POST, etc.
3. **Authentication** — API key header name, Bearer token, Basic auth, OAuth, or none
4. **Required fields** — what parameters/body fields the API needs
5. **Optional fields** — any useful optional params (like `research_effort`, `language`, `model`, etc.)
6. **Response shape** — what fields come back (ask or infer from docs/examples)
7. **Output variables** — what the user wants to store in their workflow after the call
8. **Execution environment** — Sandbox (default, fast) or Virtual Machine (needed for npm packages)

If the user pastes API docs or a code example, extract all of the above from it directly. Only ask for what's missing.

---

## Output Format

Always produce exactly these three sections, in this order, formatted as fenced code blocks.

---

### Section 1 — Code Tab (JavaScript)

Rules:
- Read all user-configurable values from `ai.config.*`
- **CRITICAL — input vs output variable pattern:**
  - `inputVariable` type config fields are resolved by MindStudio BEFORE the code runs. The value arrives as a plain string. Always read them as `ai.config.fieldName` directly. NEVER use `ai.vars[ai.config.fieldName]` for inputs.
  - `outputVariableName` type config fields hold the NAME of a workflow variable chosen by the user. Always write outputs as `ai.vars[ai.config.outputVarName] = value` so results land in the right place.
- Always validate required fields and throw clear errors if missing
- Use `ai.log(...)` to show progress to the user during long calls
- Use `await fetch(...)` for HTTP calls — no imports needed in Sandbox
- Wrap the fetch in try/catch and re-throw with a readable message
- Use `input` not `query` for You.com APIs (learned fix)
- For Virtual Machine functions, export a named `handler` async function

Template structure:
```javascript
// --- Read config ---
const apiKey   = ai.config.apiKey;
const inputVal = ai.config.inputField;   // inputVariable type: value is already resolved, read directly from ai.config
const optional = ai.config.optionalField || "default_value";

// --- Validate ---
if (!apiKey)   throw new Error("Missing API key. Set it in block configuration.");
if (!inputVal) throw new Error("Missing [field]. Provide it in block configuration.");

ai.log("Calling [API name]...");

// --- Request ---
const url = "https://api.example.com/endpoint";
const res = await fetch(url, {
  method: "POST",           // or GET, etc.
  headers: {
    "Authorization": `Bearer ${apiKey}`,   // adjust per API auth style
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    field: inputVal,
    option: optional
  })
});

if (!res.ok) {
  const err = await res.text();
  throw new Error(`[API name] error (${res.status}): ${err}`);
}

const data = await res.json();
ai.log("Done. Storing results...");

// --- Store outputs ---
// outputVariableName type: user names the variable, so use ai.vars[ai.config.outputMain] pattern
ai.vars[ai.config.outputMain]  = data.someField ?? JSON.stringify(data);
ai.vars[ai.config.outputRaw]   = JSON.stringify(data);
```

---

### Section 2 — Configuration Tab

Rules:
- Use `"secret"` type for API keys — never `"text"`
- Use `"inputVariable"` type for fields that should accept a `{{variable}}` from the workflow. MindStudio resolves the value before code runs — read it in code as `ai.config.fieldName`, not via `ai.vars`
- Use `"select"` type with `selectOptions` for fixed-choice fields (e.g. model names, effort levels)
- Use `"outputVariableName"` type for fields where the user names their output variables
- Group into logical sections with clear `title` values
- Add `helpText` to every item
- Never include a dropdown for something the user controls via a workflow variable

Template:
```javascript
config = {
  configurationSections: [
    {
      title: "API Settings",
      items: [
        {
          type: "secret",
          label: "API Key",
          variable: "apiKey",
          helpText: "Your [API name] API key. Stored securely, not transferred on remix."
        },
        {
          type: "inputVariable",
          label: "Input Field Label",
          variable: "inputField",
          helpText: "Description of what this input does. Use a {{variable}} from your workflow or type a value directly."
        },
        {
          type: "select",
          label: "Option Label",
          variable: "optionalField",
          helpText: "Description of this option.",
          selectOptions: [
            { label: "Option A", value: "value_a" },
            { label: "Option B", value: "value_b" }
          ]
        }
      ]
    },
    {
      title: "Output",
      items: [
        {
          type: "outputVariableName",
          label: "Main Output Variable",
          variable: "outputMain",
          helpText: "Workflow variable where the main result will be stored."
        },
        {
          type: "outputVariableName",
          label: "Raw Response Variable",
          variable: "outputRaw",
          helpText: "Workflow variable for the full raw JSON response."
        }
      ]
    }
  ]
}
```

---

### Section 3 — Test Data Tab

Rules:
- Mirror every `ai.config.*` variable used in the code
- Use realistic placeholder values (not "test123")
- Use the actual default output variable names the user will likely use
- Match the output variable name values to what the user typed in the Output section config fields
- For `inputVariable` type fields, set the value directly in `config` (not in `vars`) — e.g. `inputField: "AAPL"`. MindStudio does not require a vars entry for these during testing.

Template:
```javascript
environment = {
  vars: {},
  config: {
    apiKey:        "your-api-key-here",
    inputField:    "A realistic example input for this API",
    optionalField: "value_a",
    outputMain:    "result",
    outputRaw:     "resultJSON"
  }
}
```

---

## API Authentication Patterns

| Auth type | Header / approach |
|-----------|-------------------|
| API key header | `"X-API-Key": apiKey` |
| Bearer token | `"Authorization": \`Bearer ${apiKey}\`` |
| Basic auth | `"Authorization": "Basic " + btoa(user + ":" + pass)` |
| No auth | Omit headers object or leave empty |

---

## Execution Environment Notes

**Sandbox** (default — use unless told otherwise):
- Runs in <50ms
- No npm installs
- `fetch`, `JSON`, `ai.*` methods all available
- Python via Pyodide (no pip in Sandbox)
- Does NOT support browser/Node APIs like `URLSearchParams`, `Buffer`, `process`, `require`, `crypto`, `fs`, or `path`

**Virtual Machine** (use when npm packages needed):
- Slower (~5s+ startup)
- Full Node.js or Python
- Must export a `handler` function:

```javascript
import * as someLib from 'some-lib';

export const handler = async () => {
  // your code here
  ai.vars.result = someLib.doSomething();
};
```

---

## Common Mistakes to Avoid

- **NEVER use `ai.vars[ai.config.fieldName]` for input fields.** `inputVariable` type config fields are resolved by MindStudio before the code runs and arrive as plain strings via `ai.config.fieldName`. Only use the `ai.vars[ai.config.outputVarName]` pattern for output variables where the user has named where results should land.
- Never use `URLSearchParams` in Sandbox — it is not available. Build query strings manually instead:
  ```javascript
  let query = "?token=" + apiKey;
  if (symbol) query += "&symbol=" + encodeURIComponent(symbol);
  const url = "https://api.example.com/endpoint" + query;
  ```
- Never use `Buffer`, `process`, `require`, `crypto`, or `fs` in Sandbox — these are Node.js APIs not available there
- Never use `query` as a body field for You.com APIs — use `input`
- Never use backtick template literals to inject `{{variables}}` into HTML — use `<script type="application/json">` instead
- Never hardcode API keys in the Code Tab — always use `ai.config.apiKey` with `"secret"` type
- Never use `ai.vars.outputName = value` when the output variable name is user-configured — use `ai.vars[ai.config.outputVarName] = value`
- Don't add a config dropdown for a value the user sets via a workflow variable — read it from `ai.vars` instead

---

## After Delivering the Function

Always end with a short note explaining:
1. What each output variable contains
2. Which config fields the user needs to fill in before running
3. Any gotchas specific to this API (rate limits, required plan tier, field naming quirks, etc.)
