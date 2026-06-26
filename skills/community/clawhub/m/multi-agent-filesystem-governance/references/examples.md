# Examples

Use these examples to map common file operations to the correct scope, lifecycle, and storage location.

## Example 1: Newly downloaded document

A PDF, ZIP, image, or export file has just been downloaded and has not yet been reviewed.

- Scope: agent-private unless multiple agents will need it soon
- Lifecycle: temporary intake
- Recommended location type: download intake area
- Reason: newly downloaded files should be triaged before they are treated as durable knowledge, project assets, or archival material

Do not place new downloads directly into archives, knowledge vaults, or unrelated project folders unless the final destination is already certain.

## Example 2: Agent-specific scratch note

An agent creates a rough note during analysis, debugging, planning, or execution.

- Scope: agent-private
- Lifecycle: temporary or active
- Recommended location type: private workspace or private notes area
- Reason: rough notes are usually intermediate artifacts and should remain private until curated

Promote the note into a shared knowledge location only after it becomes useful beyond the current task or current agent.

## Example 3: Shared operating procedure

A procedure, workflow note, or policy is intended to guide multiple agents in repeated tasks.

- Scope: shared
- Lifecycle: shared active reference
- Recommended location type: shared knowledge base, shared notes area, or governance location
- Reason: operational guidance should be discoverable and stable when multiple agents depend on it

Do not keep shared procedure documents only in one agent’s private folder.

## Example 4: Reusable utility script

A script helps with repeated tasks such as cleanup, organization, export handling, archive rotation, or project initialization.

- Scope: shared if multiple agents use it; otherwise agent-private
- Lifecycle: active reusable utility
- Recommended location type: shared scripts area or private scripts area
- Reason: reusable scripts should be separated from ad hoc task outputs and given a predictable home

If the script is tightly tied to one project, keep it inside that project instead of a generic shared scripts area.

## Example 5: Project-specific helper script

A script exists only for one repository, one build flow, or one deployment workflow.

- Scope: project-local or agent-private
- Lifecycle: active
- Recommended location type: inside the project tree or the owning agent’s private area
- Reason: project-specific logic should remain near the project it serves

Do not move project-specific scripts into a global shared scripts area unless they have been intentionally generalized.

## Example 6: New code project

A new software project, automation tool, prototype, or repository is being created.

- Scope: shared if it is a multi-agent or team asset; otherwise agent-private
- Lifecycle: active or incubating
- Recommended location type: designated project area
- Reason: project roots should stay stable and distinct from downloads and notes

Do not start code projects inside temporary download folders or knowledge vaults.

## Example 7: Paused or inactive code project

A project is no longer active but may be resumed later.

- Scope: same ownership as before
- Lifecycle: frozen
- Recommended location type: frozen projects area or archive-ready holding area
- Reason: inactive projects should leave active work zones without losing resumability

If future work is unlikely, move the project into archive instead.

## Example 8: Completed project

A project has been delivered, replaced, or intentionally retired.

- Scope: usually shared if it served shared goals; otherwise private
- Lifecycle: archived
- Recommended location type: archive area
- Reason: completed work should leave active project areas to reduce clutter and ambiguity

Preserve recovery notes or build instructions before archival if future reopening may matter.

## Example 9: Curated reference note

A rough note has been cleaned up and is now useful as durable reference material.

- Scope: shared if broadly useful; otherwise private
- Lifecycle: durable reference
- Recommended location type: knowledge vault or reference area
- Reason: durable knowledge should live where it can be found and maintained

Do not leave long-term knowledge trapped in temporary folders or buried inside unrelated project trees.

## Example 10: Export generated from a project

A report, CSV export, rendered media file, or build artifact was created by a project.

- Scope: depends on intended consumers
- Lifecycle: temporary, active deliverable, or archival
- Recommended location type: project output area first, then shared delivery or archive area if needed
- Reason: outputs should stay traceable to the project until their final role is clear

Do not immediately scatter generated outputs into unrelated top-level directories.

## Example 11: Imported external reference material

A dataset, vendor document, API spec, or whitepaper is imported to support work across multiple tasks.

- Scope: shared if broadly reusable; otherwise private
- Lifecycle: active reference or archive
- Recommended location type: shared reference area, project-local docs area, or curated knowledge location
- Reason: imported references should be stored intentionally based on reuse level

Do not leave external references permanently mixed into raw download intake.

## Example 12: Agent handoff material

One agent prepares files that another agent will consume.

- Scope: shared unless the handoff is tightly scoped and temporary
- Lifecycle: active handoff
- Recommended location type: shared staging or designated handoff area
- Reason: cross-agent handoffs should not depend on one agent’s private workspace structure

Avoid hiding handoff materials in private temp directories.
