# Merge Requests

Verified against `glab 1.90.0`.

## Listing and Filtering

```bash
glab mr list --assignee=@me --output json
glab mr list --reviewer=@me --output json
glab mr list --source-branch="$(git branch --show-current)"
glab mr list --target-branch=main
glab mr list --search "feature X"
glab mr list --label needs-review
```

## Creating Merge Requests

```bash
# Create from the current branch
glab mr create -t "Fix bug" -d "Fixes issue #123"

# Ask for review and add labels
glab mr create -t "Add feature" -d "Implements X" --reviewer alice,bob -l "feature,backend"

# Link the MR to an existing issue
glab mr create --related-issue 123 --fill --yes

# Create a draft MR against another branch
glab mr create --draft -b develop -t "RFC: new flow"

# Match project settings for source-branch cleanup
glab mr create --remove-source-branch -t "Cleanup branch handling"
```

Use `--related-issue 123`. Do not pass the issue IID positionally to `glab mr create`.

`glab mr create --fill` sets `push` to true. Confirm the current branch, remote, and pending changes before using `--fill --yes`.

## Reviewing and Updating

```bash
glab mr checkout 123
glab mr view 123 --comments
glab mr view 123 --output json
glab mr approve 123
glab mr note 123 -m "Please add tests"
glab mr update 123 --draft
glab mr update 123 --ready
glab mr update 123 --reviewer alice,bob
glab mr update 123 --label "bug,confirmed"
```

`glab mr view 123` already renders in the terminal. Use `--web` only when the browser is the goal.

## Merging and Closing

```bash
glab mr merge 123
glab mr merge 123 --auto-merge
glab mr merge 123 --sha <head-sha>
glab mr merge 123 --squash -d
glab mr close 123
glab mr reopen 123
```

Use `--sha` when the user wants to guarantee that only the reviewed commit set gets merged.

## Common Failures

### `source branch already has a merge request`

Find the existing MR instead of creating a new one:

```bash
glab mr list --source-branch="$(git branch --show-current)"
glab mr view 123
glab mr update 123 --title "Updated title"
```

### Pipeline Must Pass Before Merge

Check the pipeline first:

```bash
glab ci status
glab pipeline ci view
```

If the project allows auto-merge, queue it instead of retrying merge manually:

```bash
glab mr merge 123 --auto-merge
```

### Need Full Discussion History

```bash
glab mr view 123 --comments
glab mr note list 123
```
