# Repo Strategies for `.malp/`

By default, the malp skill is silent about version control. These strategies are for when the user asks.

## Options

### 1. Leave it unstaged

Do nothing. `.malp/` sits in the working tree as an untracked directory. Git shows it in `git status` but it doesn't affect anything unless staged.

**Pros:** Zero config. Nothing to undo.
**Cons:** Shows up as untracked noise in `git status`.

### 2. Personal exclude via `.git/info/exclude`

Add `.malp/` to `.git/info/exclude`. This is a per-clone gitignore that isn't committed or shared with other contributors.

```
echo '.malp/' >> .git/info/exclude
```

**Pros:** Invisible to other contributors. No repo changes.
**Cons:** Per-clone — must redo after fresh clones. Easy to forget.

### 3. Global gitignore

Add `.malp/` to your global gitignore (e.g., `~/.config/git/ignore` or whatever `core.excludesFile` points to). Applies to all repos on this machine.

```
echo '.malp/' >> ~/.config/git/ignore
```

**Pros:** One-time setup, covers all repos.
**Cons:** If you ever *want* to track a `.malp/`, you have to override.

### 4. Project `.gitignore`

Add `.malp/` to the repo's `.gitignore`. This is committed and shared with all contributors.

```
echo '.malp/' >> .gitignore
```

**Pros:** Everyone on the project gets the benefit.
**Cons:** Requires a commit. Team may ask "what's a malp?" (which could be a feature, not a bug).

### 5. Track it

Actually commit `.malp/` as part of the project. Treat SUMMARY.txt as living documentation and NOTES.txt as a shared scratchpad.

**Pros:** Shared tribal knowledge. New contributors benefit immediately.
**Cons:** Requires discipline — stale NOTES.txt in a repo is worse than no NOTES.txt. Secrets must be kept out.

## Recommendation

Most people want option **2** (personal exclude) or **3** (global gitignore). Use personal exclude if you only malp a few repos. Use global gitignore if you malp everything.

Option **5** (track it) is interesting for teams that want shared context, but only works if someone maintains it.
