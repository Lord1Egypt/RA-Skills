# SourceGit Integration

Manage SourceGit GUI client's `preference.json` and custom actions.

## Configuration Path

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/SourceGit/preference.json` |
| Linux | `~/.config/SourceGit/preference.json` |
| Windows | `%APPDATA%\SourceGit\preference.json` |

Detect OS and use the appropriate path.

## When to Use

- User wants to add/remove a repository to SourceGit
- User wants to create/manage workspaces
- User wants to sync ghq repositories with SourceGit
- User mentions "sourcegit" or "SourceGit"
- User wants to rename a folder that is registered in SourceGit (folder rename)

## Instructions

### Step 0: Verify SourceGit is Closed

**CRITICAL**: SourceGit overwrites preference.json on exit. Always verify the app is closed before editing.

```bash
pgrep -x SourceGit
```

If running, ask user to quit first. Only proceed after confirming it is closed.

### Step 1: Read Current Configuration

Always read the current preference.json first:

```bash
cat ~/Library/Application\ Support/SourceGit/preference.json
```

### Step 2: Determine Operation

| User Request | Operation |
|--------------|-----------|
| "Add this repo to SourceGit" | Add to RepositoryNodes |
| "Create workspace X" | Add to Workspaces |
| "Sync ghq repos" | Scan ghq and update RepositoryNodes |
| "Remove repo X" | Remove from RepositoryNodes |
| "Rename folder" | Rename folder + update preference.json |

### Step 3: Execute Operation

#### Adding a Repository

1. Check if repository already exists in RepositoryNodes
2. Determine group structure (by host/org or custom)
3. Create node with proper structure:

```json
{
  "Id": "/path/to/repo",
  "Name": "repo-name",
  "Bookmark": 0,
  "IsRepository": true,
  "IsExpanded": false,
  "Status": null,
  "SubNodes": []
}
```

#### Creating Group Hierarchy (for ghq repositories)

For path like `/Users/es6kr/ghq/github.com/es6kr/blog.git`:

1. Find or create host group: `github.com`
2. Find or create org group: `es6kr` (under github.com)
3. Add repository: `blog.git` (under es6kr)

Group node structure:
```json
{
  "Id": "uuid-v4",
  "Name": "group-name",
  "Bookmark": 0,
  "IsRepository": false,
  "IsExpanded": true,
  "Status": null,
  "SubNodes": [...]
}
```

#### Creating a Workspace

```json
{
  "Name": "workspace-name",
  "Color": 4278221015,
  "Repositories": [],
  "ActiveIdx": 0,
  "IsActive": false,
  "RestoreOnStartup": true,
  "DefaultCloneDir": "/path/to/default/clone/dir/"
}
```

#### Renaming a Folder/Repository

When user requests folder rename:

1. **Rename the actual folder first**:
   ```bash
   mv /old/path/oldname /old/path/newname
   ```

2. **If it's a git repo, commit changes inside if needed**

3. **Update preference.json** - must update ALL occurrences:

   a. **RepositoryNodes**: Find and update both `Id` and `Name`
   ```json
   // Before
   "Id": "/path/to/oldname",
   "Name": "oldname",

   // After
   "Id": "/path/to/newname",
   "Name": "newname",
   ```

   b. **Workspaces.Repositories**: Update path strings in all workspaces
   ```json
   // Before
   "Repositories": ["/path/to/oldname", ...]

   // After
   "Repositories": ["/path/to/newname", ...]
   ```

4. **Search pattern**: Use the old path to find all references:
   - Search for `"Id": "/old/path"` in RepositoryNodes
   - Search for `"/old/path"` in Workspaces[].Repositories arrays

### Step 4: Warn About Running SourceGit

**CRITICAL**: Before editing preference.json, always warn the user:

> WARNING: If SourceGit is running, changes will be overwritten.
> Please close SourceGit before editing.

**Why**: SourceGit keeps preference.json in memory while running. Any external edits will be overwritten when SourceGit saves on exit.

### Step 5: Apply Changes

Use Edit tool to modify preference.json with the updated structure.

**Important**: Edits must be made while SourceGit is closed for changes to take effect. If running, changes will be lost when it overwrites preference.json on exit.

## ghq Integration

When user says "sync ghq" or "add-ghq":

1. Get ghq root: `ghq root`
2. List all ghq repos: `ghq list -p`
3. Parse each path to extract host/org/repo
4. Create hierarchical group structure
5. Add repositories under appropriate groups

### Clone and Add Workflow

For `/sourcegit add-ghq <url>`:

```bash
ghq get <url>
# Parse the result to get local path
# Add to RepositoryNodes with proper grouping
```

## Output Guidelines

- Confirm what was added/modified
- Show the group hierarchy if applicable
- Note that edits only take effect when SourceGit is closed

## Example Outputs

### Repository Added
```
Added repository to SourceGit:
- Path: /Users/es6kr/works/my-project
- Group: (root level)

Will be reflected next time SourceGit is opened.
```

### ghq Repository Added
```
Cloned and added to SourceGit:
- Path: /Users/es6kr/ghq/github.com/es6kr/blog.git
- Group: github.com > es6kr

Will be reflected next time SourceGit is opened.
```

### Workspace Created
```
Created workspace 'my-workspace':
- DefaultCloneDir: /Users/es6kr/projects/
- Color: Default blue

Switch to this workspace in SourceGit's workspace selector.
```

### Folder Renamed
```
Folder rename complete:
- Before: /Users/es6kr/works/project/oldname
- After: /Users/es6kr/works/project/newname

SourceGit updated:
- RepositoryNodes: oldname -> newname
- Workspaces[Default]: path updated

Will be reflected next time SourceGit is opened.
```
