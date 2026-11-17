---
name: project-weekly-report
description: Generate evidence-based project weekly reports from a local code repository. Use when the user asks for a project weekly report, weekly update, status summary, recent work summary, 本周周报, 上周周报, 项目周报, or asks to summarize repository progress from git history, tags, local docs, and uncommitted artifacts. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/work/project-weekly-report
---

# Project Weekly Report

## Goal

Create a reusable weekly report from local repository evidence. Prefer conclusions that explain product, delivery, performance, cost, quality, or risk impact.

Do not turn commits into a changelog. Compress evidence into a small number of meaningful workstreams.

## Inputs

Collect only what is needed:

- repository path
- reporting window; if absent, use the previous full calendar week relative to the current date
- audience or report style, if provided
- any user-provided context that cannot be discovered from local files

## Evidence Workflow

1. Confirm the repository and reporting window.
2. Run `git status --short` to separate committed work from local uncommitted artifacts.
3. Run `git ls-files --others --exclude-standard` to find local docs, generated reports, prototypes, or assets.
4. Run a no-merge log for the window:

   ```bash
   git log --since='YYYY-MM-DD 00:00:00' --until='YYYY-MM-DD 23:59:59' --no-merges --date=short --pretty=format:'%h%x09%ad%x09%an%x09%s'
   ```

5. If tags exist, inspect recent release tags:

   ```bash
   git for-each-ref --sort=creatordate refs/tags --format='%(creatordate:short)%09%(refname:short)%09%(subject)'
   ```

6. Read only high-signal files needed to understand the work: PRD, release notes, design docs, smoke reports, todo files, or changed files tied to the main workstreams.
7. If evidence is thin or contradictory, say so and keep the report conservative.

## Synthesis Rules

Build an internal evidence matrix before writing:

```text
source / change / affected workflow or module / value type / verification status
```

Group work into 1-3 main workstreams:

- product or business capability
- delivery quality or release readiness
- performance, reliability, or cost improvement
- risk reduction, observability, validation, or rollback readiness
- documentation or workflow assets, only when they reduce repeated work or improve handoff

Down-rank these unless they clearly support one of the values above:

- pure refactors
- naming cleanup
- formatting
- internal abstractions
- tests with no visible quality or risk link
- docs that only restate implementation

Do not invent PR review results, incident IDs, approval states, launch outcomes, production metrics, or external user impact. If a claim cannot be verified locally or from explicit user context, mark it as unverified.

## High-Density Writing

Each main work item must include:

1. concrete action
2. affected object, workflow, interface, or module
3. mechanism, scope, or coverage
4. product, performance, cost, quality, or risk value

Avoid weak summary phrases by themselves, such as:

- optimized performance
- improved workflow
- polished docs
- fixed issues

Rewrite them with object and value, for example:

- Reworked report validation around local git, tag, and artifact evidence so weekly summaries separate committed work from uncommitted assets and avoid unverifiable launch claims.

## Output Format

Unless the user gives a different template, output both versions.

### Detailed Version

Use this structure:

1. `项目背景`
2. `工作内容`
3. `成果`
4. `思考和问题`

Write in Chinese by default. Mention commit hashes, tags, or local paths only when they strengthen evidence.

### Brief Version

Use this structure:

1. `项目名`
2. `项目背景`
3. `工作内容`
4. `进展`

Keep the brief version under 300 Chinese characters. Focus only on the highest-value outcomes.

## Boundaries

- Keep committed code, local uncommitted artifacts, tags, and unverifiable external facts clearly separated.
- Do not broad-scan the whole repository when a focused evidence path is enough.
- Do not include private account details, credentials, personal contact information, customer data, or internal-only identifiers.
- Do not claim online results unless the user supplied them or local evidence clearly proves them.
- If the user asks for a future plan instead of a weekly report, switch to planning and label it separately from completed work.

## Final Check

Before finalizing, verify:

- every major claim has evidence
- the report is not a commit list
- the brief version stays under 300 Chinese characters
- each main work item states action, object, mechanism or scope, and value
- maintenance-only work is omitted or demoted unless it supports clear value
- unverified external effects are labeled

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
