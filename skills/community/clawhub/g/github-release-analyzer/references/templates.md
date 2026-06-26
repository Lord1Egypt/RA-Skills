# Output Templates

Current template name:

- `default`

Template routing is deterministic in `scripts/summary_formatter.py`.

## Language policy

- Keep the rendered message in the same language as the invocation instruction.
- Pass `language: zh` or `language: en` to `run.py render` stdin payload.

## Single release

### zh

```markdown
**{owner}/{repo} 最新 Release：{tag_name}**

- 发布时间：{published_at}

{summary_markdown}

- 链接：{html_url}
```

### en

```markdown
**{owner}/{repo} Latest Release: {tag_name}**

- Published at: {published_at}

{summary_markdown}

- Link: {html_url}
```

## Multi-release

### zh

```markdown
**{owner}/{repo} 新版本汇总（共 {count} 个）**

**1. {tag_name}**
- 发布时间：{published_at}

{summary_markdown}

- 链接：{html_url}
```

### en

```markdown
**{owner}/{repo} Release Summary ({count} total)**

**1. {tag_name}**
- Published at: {published_at}

{summary_markdown}

- Link: {html_url}
```

Repeat the numbered block for each release.

## Mode policy

- manual: reply with the rendered message only, no state language, no workflow narration
- cron: emit only the final rendered message, no filler, no step labels, no JSON
