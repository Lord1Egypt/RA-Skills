# Belief <Belief ID>: <Title>

- Belief ID: <B-...>
- Title: <short title>
- Created: <ISO-8601 timestamp>
- Updated: <ISO-8601 timestamp>
- Current Version: V1
- Origin: <diary, source, user input, or reasoning IDs>

## Current View

Copy the substantive fields from the latest revision snapshot. This section is a convenience view; Revision History is canonical.

- Proposition: <examined proposition>
- Rationale: <reasoning linking evidence to proposition>
- Supporting Evidence: <evidence entries or None>
- Opposing Evidence: <evidence entries or None inspected; absence is not evidence of absence>
- Confidence: low | moderate | high | suspended
- Confidence Basis: <why this level is justified>
- Related Beliefs: <relation and Belief IDs or None>
- Origin: <origin IDs>
- Open Questions: <uncertainties and potentially view-changing evidence>

## Evidence Entry Format

Use this structure inside Supporting Evidence or Opposing Evidence, expanding the corresponding field into subentries when needed.

- Evidence ID: <E-...>
- Reference: <source, note, observation, or diary ID and locator>
- Direction: supports | opposes
- What It Establishes: <claim and conditions>
- Limitations: <method, scope, independence, and inspection limits>

## Revision History

### V1

- Version: V1
- Timestamp: <ISO-8601 timestamp>
- Trigger: <Run ID or direct user request>
- Proposition: <same substantive value as Current View for V1>
- Rationale: <reasoning>
- Supporting Evidence: <complete evidence entries or None>
- Opposing Evidence: <complete evidence entries or None inspected>
- Confidence: low | moderate | high | suspended
- Confidence Basis: <justification>
- Related Beliefs: <relations and IDs or None>
- Origin: <origin IDs>
- Open Questions: <questions or None>
- Evidence Added or Reevaluated: <Evidence IDs and assessment>
- Reason for Change: Initial formation.

### Later Snapshot Format

Copy the complete V1 field structure for every later revision, change the version and timestamps, and explain the trigger, evidence added or reevaluated, and reason for change. Never replace or delete an earlier snapshot.
