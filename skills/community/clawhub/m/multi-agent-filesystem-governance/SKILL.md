---
name: multi-agent-filesystem-governance
description: Govern filesystem organization and file-operation decisions in multi-agent environments. Use when deciding where files should live across agent-private workspaces, shared resources, archives, downloads, scripts, notes, knowledge vaults, and code project folders; when defining directory conventions; when triaging downloads; when preventing cross-agent overwrites; or when standardizing file placement and lifecycle rules for reusable agent setups.
---

# Multi-Agent Filesystem Governance

Use this skill to make safe, consistent filesystem decisions in environments where multiple agents may create, edit, move, download, organize, or archive files.

This skill governs **ownership, placement, lifecycle, and write boundaries**. It is not tied to a specific product, path layout, operating system, or note-taking tool.

## Core objective

Ensure that every file has:

1. a clear ownership scope
2. a clear storage location
3. a clear lifecycle state
4. a clear modification rule

When uncertain, choose the narrowest safe scope and the least shared location.

## Scope model

Classify every file, folder, and file operation into exactly one of these scopes:

- **agent-private**: used by one agent only
- **shared**: intentionally reusable or accessible by multiple agents
- **archive**: inactive, historical, completed, frozen, or retained for reference

If scope is unclear, default to **agent-private**.

## Storage model

Use three top-level storage categories conceptually, even if local directory names differ:

- **agent areas**: private per-agent working locations
- **shared areas**: common reusable resources
- **archive areas**: inactive or historical materials

Do not depend on any single hard-coded path. Preserve conceptual boundaries even when adapting to local layouts.

## Required decision order

Before creating, editing, moving, renaming, or deleting files, determine the following in order:

1. What is the artifact?
2. Is it temporary, active, reusable, frozen, or historical?
3. Is it private to one agent or shared by multiple agents?
4. What is the narrowest valid location?
5. Will this action affect other agents or shared workflows?

If any answer is unclear, choose a private non-destructive location first.

## Default rules

### Prefer private over shared

If a file does not clearly require cross-agent reuse, place it in an agent-private location.

### Do not write across agent boundaries by default

Do not create, edit, move, or overwrite files belonging to another agent unless the task explicitly requires it.

### Treat shared locations as high-impact

Writing to a shared location is a wider-scope action. Use shared locations only when reuse, collaboration, or standardization is intended.

### Keep archive separate from active work

Archived material is not an active workspace. Do not continue editing files in archive locations. Restore or copy them into an active or private area first.

### Treat temporary locations as disposable

Do not keep the only important copy of a file in a temp or scratch location.

## Content-type placement guidance

Apply these rules regardless of exact local path names.

### Skills

- Put reusable multi-agent skills in a shared skills location.
- Put experimental, agent-specific, or override skills in an agent-private skills location.
- If the same skill exists in both shared and private locations, prefer the more specific private version for that agent.

### Workspaces

- Put active working files, drafts, and intermediate artifacts in the current agent’s private workspace unless they are intentionally shared.
- Do not move private task files into shared locations prematurely.

### Scripts

- Put reusable utility scripts in a shared scripts location.
- Put task-specific or agent-specific scripts in a private scripts location or within the relevant project.
- Do not scatter unrelated scripts across arbitrary folders.

### Downloads

- Route newly downloaded files into a dedicated intake location first.
- Classify and move them later into proper long-term locations.
- Do not leave downloads scattered across project folders, knowledge vaults, or temp directories without intent.

### Knowledge notes and vaults

- Put durable reference notes and curated knowledge into a designated knowledge base or vault location.
- Keep rough task notes private until they are worth preserving or sharing.
- Do not use the knowledge base as a dumping ground for arbitrary transient files.

### Code projects

- Store code projects in designated project locations.
- For durable, long-lived repositories, prefer a dedicated project root such as `~/projects/<repo>`.
- Use `/tmp/...` for temporary reproduction, validation, or throwaway clones, then promote ongoing work into `~/projects/<repo>`.
- Separate experimental, active, frozen, and archived projects when practical.
- Do not mix project source trees with general downloads, archives, note repositories, or agent runtime/config trees.
- Read `references/project-directory-best-practices.md` when the question is specifically about where formal repositories should live versus where temporary repo work should happen.

### Archives

- Move inactive, completed, superseded, or retained materials into archive locations.
- Keep archive structure stable and low-churn.
- Prefer append-only archival behavior unless explicit cleanup is required.

## File lifecycle model

Classify files into one of these lifecycle states:

- **temporary**: scratch, disposable, rebuildable
- **active**: currently being edited or used
- **shared**: actively reused by multiple agents
- **frozen**: paused but potentially resumable
- **archived**: historical, completed, or retained for record

When lifecycle changes, move the file or justify keeping it in place.

## Safety rules for file operations

### Create
Create files in the narrowest valid scope first.

### Edit
Edit in place only when ownership and scope are clear.

### Move
Move files when ownership or lifecycle changes.

### Copy
Copy instead of move when preserving history or minimizing disruption matters.

### Delete
Delete only when the file is clearly temporary, redundant, or explicitly approved for removal.

### Rename
Rename to improve clarity, ownership, lifecycle visibility, or discoverability — not for cosmetic churn alone.

## Collision and precedence rules

When equivalent resources exist in multiple scopes, prefer the most specific valid source:

1. agent-private
2. shared
3. bundled, default, or global

Use overrides intentionally. Do not create duplicate variants without reason.

## What to avoid

Avoid these patterns:

- dumping everything into one shared root
- using archive as a live workspace
- downloading directly into long-term storage without triage
- scattering scripts across unrelated folders
- mixing code projects with note-vault content
- placing durable knowledge only in temporary notes
- editing another agent’s private area without explicit need
- using shared locations by default “just in case”

## Recommended behavior when uncertain

If the correct location is unclear:

1. choose agent-private
2. choose non-destructive actions
3. preserve reversibility
4. avoid shared writes
5. ask for clarification only when the ambiguity materially affects future organization or other agents

## Decision template

When deciding where something should go, return:

- **Scope**:
- **Lifecycle**:
- **Recommended location type**:
- **Reason**:
- **Shared-impact note**:

## Output expectations

When applying this skill:

- make scope explicit
- make lifecycle explicit
- recommend the narrowest valid location
- state whether other agents are affected
- prefer durable rules over ad hoc path guesses
