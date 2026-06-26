# Meo Mai Moi Workflows

## Read-only inspection workflow

Use for questions like:

- "List my pets"
- "Show this pet's current data"
- "Check whether this token works"

Steps:

1. Verify auth with `GET /api/users/me` if needed.
2. Read the smallest endpoint that answers the question.
3. Summarize the result using the response envelope's `data` field.
4. Avoid extra follow-up calls unless they materially improve the answer.

## Pet update workflow

Use for creating or updating pet data, status, or nested health records.

1. Read the current pet or pet list first.
2. Confirm the target pet identifier.
3. Use the documented `PUT` or `POST` route.
4. Re-read the resource after the write.
5. Tell the user exactly what changed.

Guardrails:

- Do not switch to undocumented `PATCH` calls.
- For deletes, ownership changes, or status changes that could affect visibility or operations, confirm first unless the user already clearly instructed it.

## Health record workflow

Use for weights, medical records, vaccinations, and microchips.

1. Inspect current pet data or the relevant nested list if needed.
2. Create or update only the relevant nested record.
3. If the action affects history, preserve chronology and avoid overwriting the wrong entry.
4. Verify by re-reading the record or parent pet.

## Placement workflow

Use extra care. This domain has lifecycle state and relationship consequences.

### Placement summary

- Owner creates a placement request.
- Helpers respond.
- Owner accepts a response.
- `pet_sitting` becomes `active` immediately and creates or ensures a sitter relationship.
- `permanent` and `foster_*` go to `pending_transfer` and create a `TransferRequest`.
- Helper confirms physical handover.
- `permanent` transfers ownership and finalizes the request.
- `foster_*` starts foster access and marks the request active.
- Owner later finalizes temporary placements when the pet is returned.

### Agent rules for placement tasks

- Read current placement state before proposing the next action.
- Never improvise lifecycle transitions.
- Call out whether the flow is `pet_sitting`, `permanent`, or `foster_*`; they differ materially.
- If the user asks for an action that implies handover, acceptance, rejection, or finalization, explain the current state and the next documented step.
- Prefer owner-scoped actions for normal app use; admin behavior is a separate concern.

## Helper profile workflow

Use for creating, updating, or inspecting helper profiles.

1. Read visible helper profiles or the specific target profile first.
2. Confirm visibility expectations: private vs public.
3. Update only the intended profile fields.
4. Re-read after writing.

Guardrails:

- Do not leak phone numbers or structured contact details from contexts that should be public-only.
- Do not assume every helper profile can be fetched through public endpoints.

## When the contract is incomplete

If the user asks for notifications, messaging, profile-adjacent features, or other areas not clearly described as stable PAT-backed contract:

1. Say the public contract appears incomplete for that area.
2. Use only documented routes unless the user explicitly wants exploratory work.
3. If exploring, label assumptions and verify each step.
