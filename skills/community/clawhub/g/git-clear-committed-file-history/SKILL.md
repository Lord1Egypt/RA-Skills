---
name: git-filter-repo-remove-file
description: |
  Guide users to permanently remove files from Git repository history. Use this skill when users mention any of the following scenarios:
  - "git filter-repo", "completely delete files", "clean git history"
  - Want to remove sensitive information (passwords, keys, tokens, private keys) from Git history
  - Want to delete accidentally committed large files
  - Want to rewrite Git history, remove all traces of specific files
  - Mention "force push", "rewrite commit history"
  - Need to delete a file from all branches and all tags
  Even if the user doesn't explicitly mention git-filter-repo, use this skill whenever there's a need to permanently delete files from Git history.
---

# Permanently Remove Files from Git History

When you delete a file in Git, it still remains in the Git repository history.
This skill guides users to use the `git filter-repo` tool to permanently delete specified files from the complete history of a Git repository.

## Applicable Scenarios

- Accidentally committed sensitive information (passwords, API keys, private keys, tokens)
- Accidentally committed large files, causing repository bloat
- Need to clean up specific files from history
- Need to remove a file from all branches and tags

## Core Workflow

### 1. Important! First Step: Ask the User

Ask the user to confirm:
- The repository path
- Whether it's the current working directory
- Whether they need to backup the repository (strongly recommended)

**Must wait for user confirmation before proceeding with subsequent steps.**

### 2. Backup Repository (Strongly Recommended)

Before performing any operations, backup the repository first:

```bash
# Method 1: Copy the entire repository directory
cp -r your-repo your-repo-backup

# Method 2: Create a bare repository backup
git clone --bare your-repo your-repo-backup.git
```

### 3. Install git filter-repo

Choose installation method based on your operating system:

**macOS:**
```bash
brew install git-filter-repo
```

**Ubuntu / Debian:**
```bash
pip install git-filter-repo
```

**Windows:**
```bash
pip install git-filter-repo
```

### 4. Verify Current Repository Status

After entering the repository directory, check:

```bash
git status
git remote -v
```

If there's no remote repository, add one first:

```bash
git remote add origin git@github.com:username/repository.git
```

### 5. Use git filter-repo to Delete Files

Assuming the file to delete is `secrets.txt`:

```bash
git filter-repo --path secrets.txt --invert-paths
```

**What this step does:**
- Removes the file from all commits
- Removes the file from all branches
- Removes the file from all tags

**Delete multiple files:**

```bash
git filter-repo --path file1.txt --path file2.txt --path secrets/ --invert-paths
```

**Delete entire directory:**

```bash
git filter-repo --path directory-name/ --invert-paths
```

### 6. Verify File Has Been Deleted

Check if the file still exists in history:

```bash
git log --all -- filename
```

If there's no output, the file has been completely removed.

### 6. Force Push to Remote Repository

Because the history has been rewritten, a force push is required:

```bash
# Push all branches
git push origin --force --all

# Push all tags
git push origin --force --tags
```

## Additional Steps After Removing Sensitive Information

If you deleted sensitive information (keys, tokens, passwords, private keys), in addition to deleting history, you should also:

### Immediately Revoke Old Keys
- Immediately revoke/delete old keys on the corresponding service platform (GitHub, AWS, Azure, etc.)
- Generate new keys

### Check Other Locations
- Check if anyone else has forked the repository
- Check CI/CD caches
- Check if local clones still retain old content

**Important Reminder:** Just because history is deleted doesn't mean others haven't copied it before. Once sensitive information is committed to a public repository, it should be considered leaked.

## Notify Collaborators

Because the commit history has changed, other people's local repositories will be inconsistent with the remote. You need to notify them:

1. **Re-clone the repository** (recommended)
2. **Or execute the following command to sync:**
   ```bash
   git fetch origin
   git reset --hard origin/main  # Will lose unpushed local changes, use with caution
   ```

3. **Warning:** Do not continue development based on the old history, otherwise the deleted files will be reintroduced when pushing again

## Common Issues

### Q: Getting "fatal: not a git repository"?
Make sure you're executing commands in the Git repository root directory.

### Q: Getting "git filter-repo: command not found"?
Install git-filter-repo first, refer to the installation steps above.

### Q: Repository size hasn't decreased after deletion?
Run garbage collection:
```bash
git gc --aggressive --prune=now
```

### Q: Only want to modify the most recent commit?
If the file is only in the most recent commit, you don't need filter-repo, use:
```bash
git rm --cached filename
git commit --amend
```

## One-Liner Version

The most core commands:

```bash
# Delete file
git filter-repo --path filename --invert-paths

# If no remote, add first
git remote add origin <repo-url>

# Force push
git push origin --force --all
git push origin --force --tags
```
