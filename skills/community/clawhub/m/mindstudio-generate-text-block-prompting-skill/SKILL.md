---
name: mindstudio-generate-text-block-prompting-skill
description: Write, review, or improve prompts for MindStudio Generate Text blocks — whether the output is plain text or structured JSON. Use this skill whenever someone asks to write a MindStudio prompt, configure a Generate Text block, set up JSON output schema, use variables in a prompt, add conditional logic to a prompt, or access JSON data with dot notation inside a MindStudio workflow. Always use this skill for any MindStudio prompt-writing task, even if the request seems simple.
---

# MindStudio Generate Text Block Prompting Skill

A skill for writing production-ready prompts for MindStudio's Generate Text block, covering text output, JSON output, variable injection, conditional logic, and dot-notation data access.

---

## Step 1: Interview the User First

**Always gather context before writing a single line of prompt.** The quality of a MindStudio prompt depends entirely on knowing what variables exist, what the block is supposed to do, and what comes next in the workflow. Never guess at variable names — use the exact names the user has defined.

Ask the user these questions before starting. You don't need all answers for every case, but get as many as apply:

**About the block's purpose:**
- What should this Generate Text block do? (What's the job?)
- Where does it sit in the workflow — early, middle, or final step?

**About the inputs (variables coming IN):**
- What variables are available at this point in the workflow?
- What are their exact names (e.g., `topic`, `userMessage`, `scrapedContent`)?
- Are any of them JSON objects or arrays? If so, what does the structure look like?

**About the output:**
- Should the output be shown to the user, or saved to a variable for later use?
- If saved to a variable, what will you name it?
- Should the output be plain text, or structured JSON?
- If JSON, what fields does the next block need to access?

**About what comes after:**
- Does a Run Workflow block or another Generate Text block consume this output?
- If iterating, what does each item in the array represent?

Once you have these answers, use the exact variable names the user provided throughout the prompt — never invent placeholder names like `{{yourVariable}}` or `{{inputData}}`.

---

## How the Generate Text Block Works

The Generate Text block sends a prompt to an AI model and returns a response. There are two core decisions to make before writing any prompt:

**1. Output Behavior**
- `Display to User` — the response is shown directly to the end user.
- `Assign to Variable` — the response is saved to a named variable (e.g., `reportJSON`) for use in later blocks.

**2. Output Schema**
- `Text (Default)` — plain text or markdown. Good for display, emails, chat responses.
- `JSON` — structured data. Required when downstream blocks need to access specific fields, iterate over arrays, or pass data to sub-workflows.
- `CSV` — tabular data for spreadsheets.

Always confirm both before writing the prompt. The output schema shapes every other decision.

---

## Prompt Structure Best Practices

MindStudio prompts are plain text written directly into the block's Prompt field. Use Markdown headings and sections to organize longer prompts — the AI reads and follows structure well.

### The Basic Template

```
<context_variable>
  {{variableName}}
</context_variable>

## Task
Describe exactly what the AI should do.

## Style
Describe tone, length, and format expectations.

## Output
Describe what the final response should look like.
```

Use XML-style tags (e.g., `<topic>`, `<research>`, `<userInput>`) to wrap injected variables. This clearly separates data from instructions and reduces hallucination.

### Injecting Variables

Use double curly braces to inject any workflow variable into the prompt:

```
The user's topic is: {{topic}}
Today's date is: {{currentDate}}
```

Variables are resolved at runtime — whatever value the variable holds at that moment gets injected as plain text.

---

## Text Output Prompts

For `Text (Default)` output, write the prompt as a clear set of instructions. Be specific about format and length.

### Example: Simple Text Output

```
<userInput>
  {{userMessage}}
</userInput>

Respond to the user's message above in a friendly, helpful tone.
Keep your response to 2-3 paragraphs.
Do not include headers or bullet points.
```

### Example: Markdown-Formatted Report

```
<topic>
  {{topic}}
</topic>
<researchNotes>
  {{allResearchMaterials}}
</researchNotes>

## Task
Write a comprehensive report based on the research notes above.

## Formatting Rules
- Use ## for major section headings
- Use ### for subsection headings
- Write in prose paragraphs, not bullet points
- Minimum 800 words

## Style
Write like a Bloomberg or NYT analyst: specific, factual, engaging.
```

### Markdown Reference for Prompts

Use these inside prompts to control AI output formatting:

| Element | Syntax | Use it for |
|---|---|---|
| Heading 1 | `# Title` | Top-level report title |
| Heading 2 | `## Section` | Major sections |
| Heading 3 | `### Subsection` | Subsections |
| Bold | `**text**` | Emphasis on key instructions |
| Italic | `*text*` | Secondary emphasis |
| Bullet list | `- item` | Unordered lists |
| Numbered list | `1. item` | Ordered steps |
| Blockquote | `> text` | Callouts or notes |
| Code | `` `code` `` | Variable names or exact strings |

---

## JSON Output Prompts

When Output Schema is set to `JSON`, the prompt must instruct the model to return only valid JSON and nothing else — no preamble, no markdown fences, no explanation.

### The Golden Rule for JSON Prompts

Always end with an explicit output instruction that shows the exact schema:

```
Respond only with valid JSON. Do not include any explanation, preamble, or markdown code fences.

JSON Output:
{
  "key": "value"
}
```

### The Sample Output Field (MindStudio Block Setting)

When Output Schema is set to `JSON` in MindStudio, a **Sample Output** field appears below it. This is separate from the prompt — it tells MindStudio what the JSON structure looks like so it can parse and route the data correctly.

**The Sample Output must use realistic example data, not placeholder types like `"string"` or `"number`.** MindStudio reads this field to understand the shape of the output, so it needs to look like a real response the AI would actually return.

For every JSON prompt you write, always deliver two things:

1. The prompt itself (with the schema at the bottom using type hints like `"string"`)
2. A separate Sample Output block with realistic fake data to paste into the MindStudio block setting

**Example — People Extraction:**

Prompt schema (inside the prompt):
```json
[
  {
    "firstName": "string",
    "lastName": "string",
    "jobTitle": "string",
    "company": "string",
    "linkedin": "string"
  }
]
```

Sample Output (paste into the MindStudio block setting):
```json
[
  {
    "firstName": "Sarah",
    "lastName": "Chen",
    "jobTitle": "VP of Marketing",
    "company": "Acme Corp",
    "linkedin": "https://www.linkedin.com/in/sarahchen"
  }
]
```

**Example — Research Report:**

Prompt schema (inside the prompt):
```json
{
  "title": "string",
  "subtitle": "string",
  "sections": [
    {
      "header": "string",
      "subsections": [
        {
          "h3": "string",
          "paragraphs": ["string"]
        }
      ]
    }
  ]
}
```

Sample Output (paste into the MindStudio block setting):
```json
{
  "title": "The Rise of Autonomous AI Agents",
  "subtitle": "How software that acts on its own is reshaping the enterprise",
  "sections": [
    {
      "header": "Market Overview",
      "subsections": [
        {
          "h3": "Current Adoption",
          "paragraphs": ["Enterprise adoption of AI agents has accelerated rapidly since 2023, with over 40% of Fortune 500 companies piloting autonomous workflow tools."]
        }
      ]
    }
  ]
}
```

**Rules for writing Sample Output:**
- Use realistic names, titles, dates, and sentences — not `"string"`, `"value"`, or `"example"`
- Match the exact same keys and nesting structure as the prompt schema
- For arrays, include just one item — MindStudio only needs to see the shape
- For strings, write a realistic short value (a real name, a real sentence, a real URL)

### Example: Simple JSON Output

```
<userTopic>
  {{topic}}
</userTopic>

Generate 3 diverse Google search queries that would help research the topic above.

Respond only with a JSON array of strings. No explanation, no markdown.

JSON Output:
["query1", "query2", "query3"]
```

### Example: Complex Nested JSON Output

```
<articleMaterials>
  {{allResearchMaterials}}
</articleMaterials>

Write a full research report based on the materials above.

## Output Rules
- Title: concise, descriptive
- Subtitle: one compelling hook sentence
- At least 3 sections, each with 2+ subsections
- Each subsection must have at least 2 long paragraphs
- Sources: include URL and title for each source used

Respond only with valid JSON matching this exact schema. No markdown, no preamble.

JSON Output:
{
  "title": "string",
  "subtitle": "string",
  "sections": [
    {
      "header": "string",
      "subtitle": "string",
      "subsections": [
        {
          "h3": "string",
          "paragraphs": ["paragraph 1", "paragraph 2"]
        }
      ]
    }
  ],
  "sources": [
    {
      "url": "string",
      "title": "string"
    }
  ]
}
```

### Common JSON Output Mistakes to Avoid

| Mistake | Fix |
|---|---|
| AI wraps output in ```json fences | Add "Do not use markdown code fences" to prompt |
| AI adds explanation before the JSON | Add "Respond ONLY with JSON and nothing else" |
| AI uses single quotes | Specify "Use double quotes for all keys and values" |
| AI adds trailing commas | Add "Ensure valid JSON with no trailing commas" |
| Output schema is missing | Always include a sample JSON schema in the prompt |

---

## Accessing JSON Data with Dot Notation

When a variable holds a JSON object or array, access specific fields using dot notation inside any subsequent prompt or block.

### Accessing Object Properties

If a variable `user` holds:
```json
{
  "name": "Alice",
  "contact": {
    "email": "alice@example.com"
  }
}
```

Access it in a prompt like this:
```
Name: {{user.name}}
Email: {{user.contact.email}}
```

### Accessing Array Items

If a variable `data` holds:
```json
{
  "fruits": ["apple", "banana", "cherry"]
}
```

Access by index (zero-based):
```
First fruit: {{data.fruits.[0]}}
Second fruit: {{data.fruits.[1]}}
```

### Accessing Arrays of Objects

If a variable `team` holds:
```json
{
  "users": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ]
}
```

Access like this:
```
First user: {{team.users.[0].name}}
Second user's ID: {{team.users.[1].id}}
```

### Real-World Pattern: Sub-workflow Receives a Person Object

In a sub-workflow launched with a `person` launch variable:
```json
{
  "firstName": "Mark",
  "lastName": "Benioff",
  "jobTitle": "CEO",
  "company": "Salesforce"
}
```

Use in the prompt:
```
Find the work email for {{person.firstName}} {{person.lastName}},
who is the {{person.jobTitle}} at {{person.company}}.
```

---

## Conditional Logic in Prompts

Use `{{#if}}` / `{{else}}` / `{{/if}}` to branch prompt behavior based on whether a variable exists and has a value.

### Basic Conditional

```
{{#if customerName}}
Write a personalized thank-you email to {{customerName}}.
{{else}}
Write a general thank-you email to all customers.
{{/if}}
```

### Nested Conditionals

```
{{#if userType}}
  {{#if isPremium}}
  Generate a premium onboarding message for {{userType}}.
  {{else}}
  Generate a standard onboarding message for {{userType}}.
  {{/if}}
{{else}}
Generate a generic onboarding message.
{{/if}}
```

### When to Use Conditionals

- When a variable may or may not exist depending on the workflow path
- When the prompt should behave differently for different user types
- When an optional field (like a name or preference) should personalize the output if present

---

## Run Workflow + JSON Array Pattern

When a Generate Text block outputs a JSON array and a downstream Run Workflow block iterates over it, each item becomes `{{item}}` in the sub-workflow.

### Parent Workflow Prompt (generates the array)

```
Generate an array of 3 Google search queries for the topic: {{topic}}

Respond only with a JSON array. No explanation.

JSON Output:
["query1", "query2", "query3"]
```

Configure the Run Workflow block:
- Iterator: `JSON Array Input (Advanced)`
- Input Array: `{{queries}}`
- Launch Variable: `query : {{item}}`

### Sub-workflow Prompt (receives one item)

```
Search query: {{query}}

Based on this query, write 3 key findings from research on the topic.
```

---

## Quick Checklist Before Finalizing a Prompt

**For any prompt:**
- [ ] Are all variables wrapped in `{{double curly braces}}`?
- [ ] Is injected data wrapped in descriptive XML tags (e.g., `<userInput>`, `<research>`)?
- [ ] Is the task instruction clear and specific?
- [ ] Is the expected output format stated explicitly?

**For JSON output:**
- [ ] Does the prompt say "Respond ONLY with valid JSON"?
- [ ] Does the prompt say "No markdown, no preamble, no code fences"?
- [ ] Is the full JSON schema shown as a sample at the end of the prompt?
- [ ] Is the Output Schema in the block settings set to `JSON`?
- [ ] Has a Sample Output been provided with realistic example data (not `"string"` placeholders) to paste into the MindStudio block setting?

**For dot notation access:**
- [ ] Is the variable name correct (matches the Output Variable name from the block that created it)?
- [ ] Are array indexes wrapped in square brackets: `.[0]`, `.[1]`?
- [ ] Is each property access separated by a `.`?
