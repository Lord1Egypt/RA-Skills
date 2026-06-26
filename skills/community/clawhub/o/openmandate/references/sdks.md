# SDK Reference

OpenMandate offers Python and JavaScript SDKs for programmatic access.

## Python SDK

### Install
```bash
pip install openmandate
```

### Quick Start
```python
import os
from openmandate import OpenMandate

om = OpenMandate(api_key=os.environ["OPENMANDATE_API_KEY"])

# Create a mandate
mandate = om.mandates.create(
    want="a backend engineer, distributed systems",
    offer="Series A, $200K equity, remote",
    contact={"email": "you@company.com"}
)

# Answer intake questions
while mandate.pending_questions:
    answers = []
    for q in mandate.pending_questions:
        # Read q.text, q.type, q.options (if select)
        answers.append({"question_id": q.id, "value": "your answer"})
    mandate = om.mandates.submit_answers(mandate.id, answers=answers)

# mandate.status is now "active"

# Check for matches
matches = om.matches.list()
for match in matches:
    print(match.compatibility.grade_label, match.compatibility.summary)

# Accept a match
om.matches.respond(match.id, action="accept")

# Report outcome after confirmed match
match = om.matches.submit_outcome(match.id, "succeeded")
```

### Error Handling
```python
from openmandate import NotFoundError, RateLimitError, PermissionDeniedError

try:
    mandate = om.mandates.get("mnd_nonexistent")
except NotFoundError:
    print("Mandate not found")
except RateLimitError:
    print("Rate limited — retry later")
except PermissionDeniedError:
    print("API key doesn't have access")
```

### Pagination
```python
page = om.mandates.list()
for mandate in page.items:
    print(mandate.id, mandate.status)

if page.has_next_page():
    next_page = page.get_next_page()
```

## JavaScript SDK

### Install
```bash
npm install openmandate
```

### Quick Start
```javascript
import OpenMandate from "openmandate";

const om = new OpenMandate({
  apiKey: process.env.OPENMANDATE_API_KEY,
});

// Create a mandate
const mandate = await om.mandates.create({
  want: "a backend engineer, distributed systems",
  offer: "Series A, $200K equity, remote",
  contact: { email: "you@company.com" },
});

// Answer intake questions
let current = mandate;
while (current.pendingQuestions?.length > 0) {
  const answers = current.pendingQuestions.map((q) => ({
    question_id: q.id,
    value: "your answer",
  }));
  current = await om.mandates.submitAnswers(current.id, { answers });
}

// current.status is now "active"

// Check for matches (async iteration)
for await (const match of om.matches.list()) {
  console.log(match.compatibility.grade_label, match.compatibility.summary);
}

// Accept a match
await om.matches.respond(match.id, { action: "accept" });

// Report outcome after confirmed match
const match = await om.matches.submitOutcome(match.id, "succeeded");
```

### Error Handling
```javascript
import { NotFoundError, RateLimitError } from "openmandate";

try {
  await om.mandates.get("mnd_nonexistent");
} catch (e) {
  if (e instanceof NotFoundError) console.log("Not found");
  if (e instanceof RateLimitError) console.log("Rate limited");
}
```

## MCP Server (Preferred for Agents)

For AI agents, the MCP server is the richest integration. No SDK installation needed.

**Server URL:** `https://mcp.openmandate.ai/mcp`

Configure in Claude Code:
```bash
claude mcp add --transport http openmandate https://mcp.openmandate.ai/mcp \
  --header "Authorization: Bearer $OPENMANDATE_API_KEY"
```

Or install this skill — `.mcp.json` auto-configures the server.

Supported agents: Claude Code, Cursor, VS Code, Windsurf, Codex, Gemini CLI, and any MCP-compatible client.
