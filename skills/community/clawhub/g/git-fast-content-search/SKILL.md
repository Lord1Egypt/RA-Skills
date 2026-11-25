---
name: git-fast-content-search
description: Search Git projects and normal files for literal text quickly.
triggers: git content search, git grep nested directories, search files for text, fast content search
source: custom
---

# git-fast-content-search

## When to use

Use this skill when given a file or directory and a literal string to find.
It supports Windows and macOS through Python 3.

## Steps

1. Run the script with Python 3:

   ```sh
   python scripts/fast_content_search.py "<directory-or-file>" "<text>"
   ```

2. Return each JSON line as one match. `path` is absolute.
3. Read `is_git_project_file` to identify a file found in Git.
4. Read `search_method` to identify `git-grep` or `filesystem-untracked`.

The script walks non-Git directories recursively. When it finds a Git worktree,
it runs `git grep -I -l -z -F` for tracked files. It then finds every untracked
file with `git status --porcelain=v1 -z --untracked-files=all` and searches those
files normally. Git metadata, symlinks, and likely binary files are skipped.
A UTF-16 BOM is supported.

## Gotchas

- The search is literal. It does not interpret regular expressions.
- Git results include files Git searches in that worktree, normally tracked files.
- Files with NUL bytes are skipped unless they start with a UTF-16 BOM.
- Permission errors and unreadable files are skipped.
- Use `--format lines` for tab-separated human-readable output.
