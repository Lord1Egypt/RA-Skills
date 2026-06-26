---
name: github-contributor
description: Enforces repository-defined contribution policy before any GitHub interaction (issues, PRs, comments, reviews). Use this skill when the user asks you to engage with a repository that they don't own, e.g. "Open a PR", "Create a new issue", "Submit this project to an awesome list".
---

# GitHub Contributor Protocol

This skill governs all outward interactions on GitHub.

All behavior must align with the repository’s published policies (e.g., CONTRIBUTING.md, CODE_OF_CONDUCT.md, templates, SECURITY.md). 
This is a hard requirement imposed by GitHub itself and not merely a best practice. 
If repository policy cannot be located, interpreted, or satisfied, DO NOT proceed.

---

# 1. Mandatory Pre-Interaction Protocol

Before creating or commenting on:
- Issues
- Pull Requests
- Discussions
- Reviews

You MUST complete all steps below.

---

## A. Identify Repository Context

Determine:

- owner/name
- default branch
- fork vs upstream
- write permissions
- whether contribution requires prior issue/discussion

If context cannot be established → STOP.

---

## B. Locate and Read Repository Policies

Locate core contributing docs:

1. `CONTRIBUTING.md`
2. `CODE_OF_CONDUCT.md`
3. `SECURITY.md`

Search for them in these directories, in order:

1.  `/` - i.e., root 
2. `/.github` 
3.  `/docs` 

Not all repositories contain these documents.

4. PR templates:
   - `/.github/PULL_REQUEST_TEMPLATE.md`
   - `/.github/PULL_REQUEST_TEMPLATE/`
5. Issue templates:
   - `/.github/ISSUE_TEMPLATE/`

Read all relevant files fully.

---

## C. Produce an Internal Policy Summary

Before proceeding, internally summarize all explicitly defined repository policies:

- Required workflow (issue-first? discussion-first?)
- Branching model expectations (e.g. naming conventions)
- Testing / lint / formatting requirements (for PRs)
- Commit message conventions (for PRs)
- Explicit restrictions (e.g., no unsolicited refactors, no automated submissions)
- Required PR or issue structure

If this summary cannot be produced → STOP.

---

## D. Search for Existing Work

Before opening a new issue or PR:

1. Search open and closed:
   - Issues
   - PRs
   - Discussions

2. If a related thread exists:
   - Contribute there instead of creating a duplicate.
   - Do not fragment discussion.

If adequate search cannot be performed → STOP.

---

# 2. Template & Information Enforcement

## Checklist Compliance

If an issue or PR template includes required checkboxes:

- Perform each required action before marking it complete.
- Do not mark items unless actually satisfied.
- Do not remove required checklist items.

If any required action cannot be completed → STOP.

---

## Required Information Compliance

If a template requires specific information (e.g., OS, version, reproduction steps, logs, environment):

- Provide all required fields.
- Ensure reproduction steps are concrete and testable.
- Do not leave required sections blank.

If required information cannot be supplied → STOP.

---

# 3. Scope & Change Discipline

- One purpose per PR.
- No unrelated formatting or refactors.
- No drive-by changes.
- Follow repository formatting and style rules.
- Update documentation or changelog if required.

If required quality gates (tests/lint/build) cannot be verified → STOP.

---

# 4. Relaxed Interaction Pacing

When performing multiple outward actions (e.g., several comments or issues):

- Wait at least 5 minutes between interactions.
- Avoid burst behavior.
- Default to slower pacing if uncertainty exists.

Do not generate high-frequency comment sequences.

Bursty activity is:

(a) highly indicative of automation;

(b) may violate GitHub's rate limit policies. These violations
can result in severe penalties for the user.

---

# 5. Respect Repository Authority

If maintainers:

- Close an issue or PR,
- Reject a proposal,
- Request changes,
- Request no further automated interaction,

Then:

- Comply immediately.
- Do not escalate.
- Do not repost the same content.
- Do not bypass stated policy.

---

# 6. Stop Conditions

Do NOT proceed if:

- Policies are missing or ambiguous.
- Security-sensitive code is involved.
- Explicit anti-bot/automation policy exists.
- Required checks/tests cannot be run.
- Required template information cannot be provided.

When uncertain, choose the action that minimizes disruption.

---

# 7. Policy Basis & Consequences

This protocol is grounded in repository-defined contribution policies and GitHub platform rules. If you are able to satisfy these requirements, you may produce high-quality contributions and your contributions will be welcome.

Failure to follow repository policies may result in:

- Immediate closure of issues or PRs
- Maintainer refusal to review
- Loss of trust
- Account moderation or rate limiting
- Organization-level blocking
- Reputational damage

This skill exists to ensure compliance with repository governance and to prevent disruptive or low-quality interaction that could have undesirable repercussions. You may be acting on behalf of a user who cares a lot about their project, so do not put that at risk by disregarding GitHub community standards. If the user is not aware of these standards, notify them of this risk before taking any action.
