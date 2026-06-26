# Meo Mai Moi Domain Model

## Pets

Pet profiles can include:

- basic info: name, age, sex, species
- location: country, state, city
- description and photos
- categories/tags
- health records: weights, vaccinations, medical records, microchips
- placement requests for rehoming, fostering, or sitting

## Pet relationships and access

A pet can have multiple active relationships with users.

Key relationship types:

- `owner`: full access, can transfer ownership and manage relationships
- `foster`: edit access for temporary care
- `editor`: edit access without ownership rights
- `viewer`: read-only access
- `sitter`: appears in placement lifecycle for pet-sitting flows

Important access model:

- Full profile access is relationship-based.
- Public profile access is narrower and field-whitelisted.
- Ownership and placement actions can have real-world consequences. Treat them carefully.

## Helper profiles

Helper profiles represent people who can respond to placement requests.

Important fields include:

- country, state, city
- address and zip code
- phone number
- contact details
- experience
- whether the helper has pets or children
- `request_types`: one or more of `foster_paid`, `foster_free`, `permanent`, `pet_sitting`
- `status`: private by default, `public` to appear in public listings

Visibility notes:

- Owners can always view their own helper profiles.
- Pet owners can view a helper profile when that helper responded to their placement request.
- Public helper pages hide phone numbers and structured contact details.
- Public helper visibility is stricter than merely existing; do not assume every helper profile is public.

## Placement concepts

Core models:

- `PlacementRequest`: owner’s request and overall state
- `PlacementRequestResponse`: helper’s response
- `TransferRequest`: physical handover confirmation object for flows that need one
- `PetRelationship`: source of truth for ownership and care access over time

Placement request types:

- `permanent`
- `foster_free`
- `foster_paid`
- `pet_sitting`

Placement request statuses used by current flow:

- `open`
- `pending_transfer`
- `active`
- `finalized`

Other enum values may exist, but do not assume they are part of the active public workflow.

## Practical agent guidance

- Before writing anything, understand whether the task touches pet data, helper data, relationship data, or placement state.
- If a task mentions adoption, fostering, handover, or return, read `workflows.md` before acting.
- If a task only needs straightforward pet CRUD or health records, the API reference may be enough.
