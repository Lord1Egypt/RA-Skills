# Anti-Pattern Rules

Every suggestion must pass this gate before being shown. If a suggestion violates any rule, discard it and generate a replacement.

## The 11 Rules

### 1. No Restating the Obvious

**Violation**: "Would you like to know more about JWT tokens?" (when you just explained JWT tokens)
**Fix**: "Implement token refresh with sliding window expiry" (advances the work)

The user already knows what you just told them. Move forward, don't circle back.

### 2. No Generic Filler

**Violation**: "What are the pros and cons?" / "Can you explain further?" / "Tell me more about this"
**Fix**: "Compare HMAC vs RSA for your token signing — you're using HS256 but your team size suggests RS256"

Generic questions could apply to any topic. Every suggestion must be specific to THIS context.

### 3. No Already-Answered Topics

**Violation**: Suggesting the user explore something the conversation already covered in depth.
**Fix**: Suggest the NEXT step beyond what was covered, or a different angle entirely.

Scan the conversation. If it was discussed, it's done. Move on.

### 4. No Overly Broad Suggestions

**Violation**: "Learn about security best practices" / "Tell me about database optimization"
**Fix**: "Add CSRF protection to your three form endpoints" / "Add an index on users.email — your login query does a full table scan"

Narrow to the user's specific situation. Name files, functions, or concrete actions.

### 5. No Sycophantic Suggestions

**Violation**: "Would you like me to do anything else?" / "Is there anything else I can help with?"
**Fix**: Remove entirely. This is never a valid next step.

The agent serves the user by suggesting useful actions, not by asking permission to exist.

### 6. No Hallucinated Context

**Violation**: "Continue working on your Kubernetes deployment" (when the user never mentioned Kubernetes)
**Fix**: Only reference things explicitly mentioned in the conversation or found in project files.

If the user didn't mention it and it's not in their project, don't suggest it.

### 7. No Repetitive Structure

**Violation**: Three consecutive activations all starting items with "Consider..." or "Implement..."
**Fix**: Vary phrasing: "Add...", "Deep-dive into...", "Resume...", "Quick win:...", "What if..."

Check your last few activations. If the structure feels repetitive, rewrite.

### 8. No Trivially Lookupable Items

**Violation**: "What is a JWT token?" / "What does async/await do?"
**Fix**: "Implement async error boundaries for your unhandled rejections" (assumes knowledge, advances work)

If a web search answers it in 3 seconds, it's not a next step. Suggest actions, not definitions.

### 9. No Scope Mismatches

**Violation**: "Redesign your entire database schema" (when user asked a quick CSS question)
**Fix**: Match suggestion effort to session scope. Quick fix session → quick win suggestions.

Read the room. A user fixing a typo doesn't want an architecture proposal.

### 10. No Format Repetition

**Violation**: All 5 suggestions starting with "Implement" or all being questions.
**Fix**: Mix verbs: one "Implement", one "Explore", one "Resume", one "Consider", one "Quick win".

Visual monotony signals low effort. Vary the opening words and item structures.

### 11. No Low-Value Clarifications

**Violation**: "Would you like me to clarify the difference between X and Y?" (when it doesn't matter)
**Fix**: Remove entirely, or replace with an actionable task.

Only clarify things that would change the user's approach. Most clarifications are filler.

## Quality Bar

Every suggestion that passes the anti-pattern gate must ALSO satisfy ALL of these criteria:

- **Specific**: Names concrete files, functions, APIs, or actions — not vague categories
- **Actionable**: The user can act on it immediately without further research
- **Non-obvious**: The user wouldn't have thought of it on their own (or needs the reminder)
- **Contextually grounded**: Directly connected to the current conversation or project state
- **Scope-appropriate**: Effort level matches the session scope (quick fix vs. deep work)
- **Differently framed**: Each suggestion in the set uses different wording and structure

## Self-Review Procedure

After generating all candidates:

1. Read each suggestion against all 11 rules above
2. Check each against all 6 quality criteria
3. Remove any violators
4. If removed count puts you below `display-count`, generate replacements
5. Verify the final set has category diversity (not all the same type)
6. Verify varied sentence structure across the set
7. Present the final set
