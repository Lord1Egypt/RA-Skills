# Issue Prioritizer

Analyze and prioritize GitHub issues by ROI and solution sanity (Tripping Scale).

## Prerequisites

- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated (`gh auth login`)
- [`jq`](https://jqlang.github.io/jq/) installed

## Commands

- `/issue-prioritizer` - Analyze issues from a repository

## Usage

```
/issue-prioritizer owner/repo
/issue-prioritizer owner/repo --quick-wins
/issue-prioritizer owner/repo --level beginner
/issue-prioritizer owner/repo --limit 500 --batch-size 20 --max-concurrency 30
/issue-prioritizer owner/repo --history-dir ~/.local/state/issue-prioritizer/runs --retain 20
/issue-prioritizer --resume 20260222-113000_owner_repo
/issue-prioritizer owner/repo --limit 200 --diff-from latest
```
