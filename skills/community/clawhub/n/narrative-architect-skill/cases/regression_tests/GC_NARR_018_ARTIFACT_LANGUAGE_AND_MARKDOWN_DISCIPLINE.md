# GC_NARR_018_ARTIFACT_LANGUAGE_AND_MARKDOWN_DISCIPLINE

## Purpose

Test whether the skill respects artifact delivery discipline for English GitHub README requests.

## Scenario

User asks in English:

```text
I want to publish a skill on GitHub. It helps engineers free up their hands when coding. Give a name and a README.
```

## Expected Behavior

the skill must:

1. Respond in English.
2. Suggest names in English.
3. Avoid unverified availability claims.
4. Provide a README in clean Markdown.
5. Avoid UI residue such as "Copy" or "bash Copy".
6. Use placeholders for unknown install commands and repo paths.
7. Avoid fake requirements.
8. Avoid overclaiming.
9. Keep the README developer-friendly.
10. Preserve selected project name consistently.

## Bad Pattern

```text
几个方向：
🥇 Handoff（推荐）
GitHub 大概率不撞。
```

Why bad:

```text
wrong language
unverified availability claim
not developer-facing
```

## Bad Pattern 2

```text
bash
Copy
git clone https://github.com/<your-org>/handoff.git
```

Why bad:

```text
UI residue
not clean Markdown
```

## Good Pattern

```text
Here are a few naming directions:

1. Handoff
A short, developer-native name. It suggests handing off repetitive engineering tasks to agent staff. Availability should be checked before publishing.

2. CodeHandoff
More explicit and easier to understand, but less elegant.

My recommendation: Handoff if you want a broader brand; CodeHandoff if you want immediate clarity.

Below is a GitHub-ready README draft.
```

## README Acceptance Criteria

Pass if README includes:

```text
project name
one-line description
what it is
why it exists
core features or agent roles
example usage
installation with placeholders
roadmap or status
contributing
license placeholder or declared license
```

Fail if README includes:

```text
fake install command
unverified package availability
wrong language
UI residue
inconsistent project name
overpromised automation
```

## Golden Principle

A GitHub README must be useful before it is persuasive.
