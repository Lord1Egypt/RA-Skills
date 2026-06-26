# Migration Pattern: Blob Memory → Layered Memory

Use this when converting an agent from a generic persistent-memory system to a layered memory architecture.

## Goal
Do not "move everything into a new structure" blindly.
First separate memory by authority, time horizon, and scope.

## Step 1: Inventory the current memory store
Classify existing contents into:
- durable cross-session truths
- durable but detailed doctrine/architecture
- project-bound working notes
- episodic logs/history
- live operational state / generated snapshots
- junk / duplicates / stale content

## Step 2: Create the target layers
Minimum viable layered system:
- hot canon
- topic/doctrine docs
- project memory area
- episodic log area
- generated summaries area

## Step 3: Migrate by promotion class, not by source order
Move content into the new system by meaning:
- durable truths → hot canon
- doctrine / architecture → topic docs
- project-bound material → project memory
- dated events → episodic logs
- live snapshots → generated summaries or delete if rebuildable

## Step 4: Rewrite, do not just copy
During migration:
- collapse duplicates
- rewrite stale facts into current truth
- keep summary/detail split where needed
- remove derived-state noise from canon

## Step 5: Establish read order
Set the retrieval path:
1. hot canon
2. index/selector
3. relevant topic docs
4. project memory if needed
5. generated summaries for live ops
6. raw logs only when verification is required

## Step 6: Add maintenance rules
A layered memory system will still decay if maintenance is absent.
Add explicit rules for:
- promotion
- demotion
- dedupe
- stale-canon cleanup
- summary rewrite cadence

## Common mistakes
- migrating raw logs into canon
- keeping one giant index that points to everything equally
- treating generated summaries as primary truth
- keeping project memory and global canon mixed together
- preserving duplicates because they feel "safer"

## Good migration outcome
The result should be:
- easier to load cheaply
- easier to trust
- easier to maintain
- harder to poison with stale status noise
