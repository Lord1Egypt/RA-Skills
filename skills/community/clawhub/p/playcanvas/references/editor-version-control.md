# Version Control

## Version Control
Once you've moved beyond the simplest of projects, you will find that version control becomes an important part of your application development process. Version Control is a system that:
- Allows you to turn back time to a previous version of your code and assets
- Allows you to see changes that have been made to a project over time
- Allows you to trial new changes in a safe place, isolated from other developers, and merge changes when ready
PlayCanvas has version control tools built directly into the Editor with three main features:
- **Checkpoints** — Snapshots of your project at a point in time, forming a timeline of changes.
- **Branches** — Isolated lines of development for features or individual developers.
- **Merging & Resolving Conflicts** — Combining branches and resolving conflicts when both branches edit the same data.
## How PlayCanvas VCS Compares to Git
| Concept | PlayCanvas | Git |
|---------|-----------|-----|
| Snapshot | Checkpoint | Commit |
| Current edits | Un-checkpointed changes | Working directory |
| Restore | Restore checkpoint | `git checkout <commit>` |
| Isolation | Branch | Branch |
| Combine | Merge | Merge |
## Storage Impact
Every checkpoint only stores changes from the previous checkpoint. Creating a branch copies the project state at that checkpoint, which can increase storage usage significantly.
Explicit deletion of checkpoints/branches is only possible via:
- Hard reset to a checkpoint
- Deleting a branch
If you need more storage space, contact support@playcanvas.com.
## Version Control Branches
A branch is an isolated line of development in PlayCanvas. Every checkpoint belongs to a branch. A project always has at least one branch (main) and often multiple branches for features.
## Main Branch
Every project has a "main" branch that cannot be deleted. In many respects it's no different from other branches, but the REST API uses it as the default. A common pattern: main = current development, branches for stable releases and features.
## Current Branch
You always have one branch set as your **current branch**. All edits apply to this branch.
## Creating a Branch
Version Control panel → select checkpoint → dropdown → **New Branch** → name it descriptively (e.g., `fix-player-bug`, `refactor-sound-effects`). You're automatically switched to the new branch, and it's favorited for quick access.
## Filtering & Searching
Filter branches by: Favorites, Open, Closed. Use the search bar to find specific branches.
## Switching Branches
Select branch → dropdown → **Switch to this branch**. Editor reloads on the chosen branch.
## Closing a Branch
Select branch → dropdown → **Close this branch**. You cannot close your current branch or the main branch. Optionally create a checkpoint before closing (enabled by default). ⚠️ Unticking creates a checkpoint loses work since the last checkpoint. Closed branches can be reopened.
## Deleting a Branch
Only possible if:
- The branch has not been merged into another branch
- No branches created from this branch
Select branch → dropdown → **Delete this branch** → type branch name to confirm. ⚠️ Deleted branches cannot be recovered. When in doubt, close instead.
## Version Control Checkpoints
A checkpoint is a snapshot of your project at a point in time, similar to commits in other VCS. It contains the complete data for your project so you can restore this state at any point. Once created, checkpoints cannot be deleted.
## Creating a Checkpoint
Open the Version Control panel → click **New Checkpoint** → enter description. Keyboard: **Ctrl+S** (Cmd+S on macOS).
## Restoring a Checkpoint
Open Version Control panel → find the checkpoint → dropdown menu → **Restore checkpoint**. The editor reloads the project at that checkpoint.
## Hard Reset
Hard reset deletes all checkpoints after a selected one. Conditions:
- No branches created from checkpoints being deleted
- Checkpoints not created by a merge
To use: dropdown menu → **Hard reset** → type 'hard reset' to confirm → editor reloads.
⚠️ Deleted checkpoints cannot be recovered.
## Version Control Merging
Merging combines work performed in one branch with work from another branch. It's a core part of the branch-based workflow.
## How Merging Works
A merge takes **two checkpoints** from two different branches, calculates the changes since their last shared ancestor, combines them, and creates a new checkpoint.
## Starting a Merge
1. Switch to the **destination branch** (the branch you're merging INTO)
2. Select the **source branch** → dropdown → **Merge into current branch**
**Options before merging:**
- Source branch: Create checkpoint first (include un-checkpointed changes), Close branch after merging
- Destination branch: Create checkpoint first (ticked by default — recommended)
## Automatic Merging
PlayCanvas auto-merges non-conflicting changes. If no conflicts, the Editor reloads with merged changes.
## Resolving Conflicts
When both branches changed the same property (e.g., both moved the same entity), conflicts arise. The **Conflict Manager** opens:
- Lists each conflicted resource on the left
- Shows comparison: Base (original) vs each branch's version
- For each conflicted property, choose which version to accept
- Click **Complete Merge** to finish
