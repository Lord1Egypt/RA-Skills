---
name: github-fetcher
description: Use this skill when the user mentions a GitHub URL or asks to analyze, review, explore, or understand any GitHub project, repository, or codebase. Triggers on phrases like "分析这个项目", "看看这个仓库", "analyze this repo", "what does this project do", or any github.com URL in the message.
metadata: {"clawdbot":{"emoji":"🐙","requires":{"bins":["curl"]}}}
---
# GitHub Repository Fetcher

When given a GitHub URL or repo name, ALWAYS use curl to fetch real content first. Never guess or infer — fetch then analyze.

## Standard analysis workflow
```bash
# 1. List root directory
curl -s "https://api.github.com/repos/OWNER/REPO/contents/"

# 2. Get README
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/README.md"

# 3. Explore key subdirectories based on findings
curl -s "https://api.github.com/repos/OWNER/REPO/contents/src"
```

## Get specific file
```bash
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/PATH/TO/FILE"
```

## Extract OWNER/REPO from URLs
- https://github.com/ultraworkers/claw-code → OWNER=ultraworkers REPO=claw-code
- github.com/foo/bar → OWNER=foo REPO=bar

## Tips
- Try `master` if `main` returns 404
- Use `?ref=BRANCH` for other branches
- GitHub API rate limit: 60 req/hour unauthenticated
- After fetching, always provide analysis based on actual content