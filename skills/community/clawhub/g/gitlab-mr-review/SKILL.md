---
name: gitlab-mr-review
description: Review GitLab merge requests using a standardized code review template. Use when user asks to review an MR (e.g., "帮我review这个mr: https://gitlab.xxx.com/..."). Automatically fetches MR changes, analyzes the diff, and posts a review comment following the template.
---

# GitLab MR Review

This skill performs code reviews on GitLab merge requests using a standardized template.

## Trigger

When user says something like:
- "帮我review这个mr: ${url}"
- "review this mr: ${url}"
- "帮我审查这个mr: ${url}"

## Workflow

### Step 1: Extract MR URL and Project Info

Parse the MR URL to extract:
- GitLab host (e.g., gitlab.snowballtech.com)
- Project path (e.g., bp/iot-admin-arco)
- MR IID (e.g., 1321)

### Step 2: Configure glab for the GitLab instance

```bash
glab config set host https://<hostname>
```

### Step 3: Fetch MR Information

```bash
glab api projects/<project>/merge_requests/<iid>
```

### Step 4: Fetch MR Changes (Diff)

```bash
glab api projects/<project>/merge_requests/<iid>/changes
```

### Step 5: Analyze the Diff

Read the review template at `code-review-template.md` and analyze the diff for:
- TODO/FIXME comments
- Unfinished code
- Hardcoded values
- Potential bugs
- Security issues
- Code style issues
- Missing error handling

### Step 6: Generate Review Comment

Fill in the template with your analysis:
- **概述**: Brief summary of what the MR does
- **优点**: What went well
- **建议**: Specific suggestions with file paths and line numbers
- **问题**: Issues that need fixing
- **结论**: Action items (checkboxes)

### Step 7: Post Comment to MR

```bash
glab api projects/<project>/merge_requests/<iid>/notes --method POST \
  --raw-field body="$(cat review-comment.md)"
```

Or use inline with `--raw-field body="<content>"`

## Tips

- Use emoji to highlight severity (🔴 for critical, 🟡 for warnings, ✅ for good)
- Be specific: include file paths and line numbers
- Provide actionable feedback
- Balance praise with constructive criticism
