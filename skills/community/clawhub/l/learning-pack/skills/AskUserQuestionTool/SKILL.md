---
name: AskUserQuestionTool
description: "Ask the user questions to gather information, confirm actions, or make decisions. Use when you need user input, confirmation, or clarification."
metadata: { "openclaw": { "emoji": "❓", "requires": { "bins": [] } } }
---

# AskUserQuestionTool

Ask the user questions to gather information, confirm actions, or make decisions.

## When to Use

✅ **USE this skill when:**
- Needing clarification on ambiguous requests
- Confirming destructive actions
- Gathering required information
- Presenting options for user selection
- Validating assumptions

❌ **DON'T use this skill when:**
- Information is already available → use existing context
- Questions can be inferred → make reasonable assumptions
- Multiple rapid questions → batch into one message

## Usage

Questions are asked through the chat channel:

```
❓ Question: [Your question here]

Options:
- Option 1
- Option 2
- Option 3
```

## Question Types

| Type | Purpose | Example |
|------|---------|---------|
| Confirmation | Verify before action | "Delete these files?" |
| Clarification | Resolve ambiguity | "Which directory?" |
| Selection | Choose from options | "Pick a framework" |
| Information | Gather missing data | "What's the API key?" |

## Examples

### Example 1: Confirmation

```
⚠️ Confirmation Required

You are about to delete 15 files in /tmp/cache.
This action cannot be undone.

Proceed with deletion?
- Yes, delete all files
- No, cancel
- Show files first
```

### Example 2: Clarification

```
❓ Clarification Needed

You asked to "update the config". Which config file?

- config.json (main application config)
- config.prod.json (production config)
- config.dev.json (development config)
- All of the above
```

### Example 3: Selection

```
📋 Choose a Database

Which database should we use for this project?

- PostgreSQL (recommended for production)
- SQLite (good for development/testing)
- MySQL (familiar, widely used)
- MongoDB (document store)
```

### Example 4: Information Gathering

```
❓ Information Needed

To set up the GitHub integration, I need:

1. GitHub username or organization
2. Repository name
3. Access token (or I can guide you to create one)

Please provide these details.
```

## Best Practices

### 1. Be Specific

```
❌ Bad: "What do you want to do?"
✅ Good: "Should I create a new file or edit the existing one?"
```

### 2. Provide Context

```
❌ Bad: "Which one?"
✅ Good: "Which branch should I merge: 'feature/auth' or 'feature/api'?"
```

### 3. Offer Options

```
❌ Bad: "What should I do?"
✅ Good: "Choose an action:
- Continue with current approach
- Try alternative method
- Stop and review"
```

### 4. Batch Questions

```
❌ Bad: (5 separate messages with 1 question each)
✅ Good: (1 message with 5 related questions)
```

## Integration with Workflows

### Approval Workflows

```
1. Agent identifies action requiring approval
2. AskUserQuestionTool presents action + risks
3. User confirms or denies
4. Agent proceeds based on response
```

### Interactive Configuration

```
1. Agent needs configuration details
2. AskUserQuestionTool gathers info step-by-step
3. Agent validates and applies configuration
4. Confirm success with user
```

## Response Handling

Agent should:
1. **Wait for response**: Don't proceed without answer
2. **Handle all options**: Account for each possible response
3. **Validate input**: Ensure response is understood
4. **Follow up**: Ask again if response is unclear

## Security Notes

⚠️ **Question security:**
- Don't ask for sensitive data in chat (passwords, tokens)
- Use secure channels for sensitive information
- Confirm destructive actions explicitly
- Log important decisions

## Accessibility

- Use clear, simple language
- Provide sufficient context
- Avoid jargon when possible
- Format options clearly
