# Workflow Patterns

Use these when a skill needs staged execution.

## Discovery -> Plan -> Build -> Validate

Use for most creation skills.

Gate rules:
- Do not build before the discovery summary is accepted.
- Do not package before validation passes.

Outputs by stage:
- Discovery: inputs, outputs, triggers, constraints
- Plan: pattern choice, resource list, file plan
- Build: created or updated files
- Validate: script result and remaining gaps

## Interview-First Flow

Use when requirements are ambiguous.

1. Ask for the user's goal.
2. Ask for input and output examples.
3. Ask what a triggering request looks like.
4. Restate the skill in one short summary.
5. Wait for confirmation before scaffolding.

## Review-Driven Iteration

Use when improving an existing skill.

1. Read current `SKILL.md` and resources.
2. Identify gaps in triggering, resource choice, or execution clarity.
3. Rewrite the minimum set of files needed.
4. Run validation.
5. Report what changed and what still needs real-world testing.

## Hard Gates

Use explicit no-go conditions when needed.

Examples:
- "Do not create files until the target directory is known."
- "Do not synthesize the final skill until trigger examples are concrete."
- "Do not claim a script exists unless it was executed successfully."
