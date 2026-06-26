# PromptGit Limitations

What PromptGit **doesn't** do. Read before deploying.

---

## What It Doesn't Do

### 1. **Cloud Sync**
PromptGit is local-only. No automatic sync across devices.

**Why:** Cloud sync requires account management, conflict resolution, and infrastructure. Out of scope for a lightweight local tool.

**Workaround:** 
- Put `~/.promptgit` in Dropbox/Google Drive/OneDrive for basic sync
- Use Git to version your `.promptgit` directory
- Export/import for manual sharing

---

### 2. **Collaborative Editing**
No real-time collaboration, no multi-user conflict resolution, no merge tools.

**Why:** Conflict resolution for prompts is complex (text merge isn't always semantic merge). Requires infrastructure.

**Workaround:** 
- One person owns each prompt
- Use export/import to share finalized versions
- Or version the whole `.promptgit` dir with Git and use Git's merge tools

---

### 3. **Automatic Backups**
PromptGit doesn't automatically backup to external storage.

**Why:** Where to backup? Cloud? USB drive? That's user preference, not tool behavior.

**Workaround:** 
- Manually backup `~/.promptgit` directory
- Script periodic backups with cron/Task Scheduler
- Use a synced folder (see Cloud Sync workaround)

---

### 4. **Delete Command**
No built-in command to delete prompts or versions.

**Why:** Version control shouldn't make deletion easy. Accidental deletes are worse than clutter.

**Workaround:** 
- Manually delete folders from `~/.promptgit/prompts/`
- Or tag unwanted prompts as `deprecated` and filter them out

---

### 5. **Binary Content**
Text prompts only. No images, PDFs, or other binary content.

**Why:** Version control for binary files requires different storage strategies (Git LFS, etc.).

**Workaround:** 
- Store text descriptions of multimodal prompts
- Keep actual images/files elsewhere, reference them by path

---

### 6. **Semantic Diff**
Diffs show character/line changes, not semantic meaning changes.

**Why:** "You are helpful" → "You are friendly" is a big semantic change but a small text diff. Semantic analysis requires AI.

**Workaround:** 
- Use version notes to describe semantic changes
- Tag versions with test results (e.g., "best", "worse")
- Human review of diffs

---

### 7. **Merge Tools**
No 3-way merge, no conflict markers, no merge helpers.

**Why:** Text merge isn't always the right answer for prompts. "Helpful assistant" + "Friendly assistant" ≠ "Helpful and friendly assistant" automatically.

**Workaround:** 
- If you need merges, use Git on the `.promptgit` directory
- Or manually combine prompts and save as a new version

---

### 8. **Access Control**
No permissions, no user accounts, no read-only prompts.

**Why:** Local tool, single user. No security model needed.

**Workaround:** 
- Use filesystem permissions if sharing a `.promptgit` directory
- Export read-only markdown for documentation

---

### 9. **Large File Handling**
PromptGit stores full content for every version. Very large prompts (100k+ tokens) with many versions will eat disk space.

**Why:** Simple storage model: one file per version. No compression, no delta storage.

**Workaround:** 
- Prompts are usually small (< 10KB). Disk space is cheap.
- For massive prompts, manually clean up old versions

---

### 10. **Structured Prompts**
PromptGit treats prompts as plain text blobs. No understanding of structure (YAML frontmatter, JSON schema, etc.).

**Why:** Prompts come in all formats. No universal structure exists.

**Workaround:** 
- Store structured prompts as plain text
- Your own tooling can parse the content after retrieval

---

## Edge Cases

### Same Content, Different Notes
If you save the exact same content twice (even with different notes), the second save will fail with "identical content already exists."

**Why:** Version IDs are content hashes. Same content = same ID = duplicate.

**Workaround:** 
- If you really need two versions with identical content but different notes, add a comment or whitespace to make them unique

---

### Very Long Prompt Names
Prompt names are used as directory names. Very long names (200+ chars) may hit filesystem limits.

**Why:** Filesystem path length limits (Windows: 260 chars, Linux: 4096 chars).

**Workaround:** 
- Use shorter, descriptive names
- Or change `STORAGE_DIR` to a shorter path

---

### Unicode in Prompt Names
Prompt names with special characters (`/`, `\`, `:`, `*`, etc.) will cause errors.

**Why:** These are invalid in directory names on most filesystems.

**Workaround:** 
- Use alphanumeric names with hyphens/underscores
- PromptGit enforces name sanitization: names containing `..`, `/`, `\`, or null bytes are rejected with a ValueError. All path operations verify the resolved path stays inside the repository directory.

---

### Concurrent Access
If two processes write to the same repository simultaneously, corruption is possible.

**Why:** No locking mechanism. Filesystem writes aren't atomic at the repo level.

**Workaround:** 
- Don't run multiple PromptGit commands simultaneously
- Or use filesystem-level locking if scripting batch operations

---

## When NOT to Use PromptGit

- **Team collaboration in real-time:** Use a proper CMS or shared doc platform
- **Cloud-based prompt library:** Use a database or cloud storage with API
- **Production deployment:** PromptGit is for development/iteration, not live serving
- **Binary prompt assets:** Images, audio, video — out of scope

---

## When TO Use PromptGit

- **Solo prompt engineering:** Track your own iterations safely
- **Prompt experimentation:** Save every variation, roll back easily
- **Knowledge base:** Organize your best prompts for reuse
- **Audit trail:** See when/why prompts changed
- **Offline work:** Zero dependencies, works without internet

---

## Honest Summary

PromptGit is a **personal version control tool** for text-based AI prompts. It's Git-like, but simpler and prompt-focused. It's not a team collaboration platform, not a cloud service, not a production database. If you want local, offline, zero-dependency prompt versioning, this is it.
