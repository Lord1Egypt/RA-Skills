# SKILL: governance-explainer

## Purpose
Explain DAO rules and implications clearly, translating governance into practical constraints and safe actions.

## When to Use
- A user proposes an action that may violate governance
- A rule/policy is referenced but unclear
- A vote, authority boundary, or permission is in question

## Inputs
- `governance_rule` (required): the rule text or reference
- `context` (required): situation + proposed action

## Steps
1. Interpret the rule in plain language (what it intends to constrain).
2. Translate to action:
   - what is allowed
   - what is forbidden
3. Identify prerequisites (votes, roles, approvals, thresholds).
4. Identify consequences:
   - governance risk
   - operational risk
   - reputational/system risk
5. If details are missing, ask the minimum clarifying questions.

## Validation
- Must align with the governance text as provided.
- Clearly mark what is interpretation vs what is explicitly stated.

## Output
- `simplified_explanation`
- `allowed_actions`
- `forbidden_actions`
- `constraints`
- `consequences`

## Safety Rules
- Do not “route around” governance.
- If governance is ambiguous, default to the safer interpretation and request clarification.

## Example
Input: “Can we bypass the review process to ship today?”
Output: forbidden unless governance grants emergency bypass; list required approvals and consequences of violation.

