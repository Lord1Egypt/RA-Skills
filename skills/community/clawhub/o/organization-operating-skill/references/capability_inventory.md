# Capability Inventory

This document tracks the capabilities already integrated into `organization-operating-skill` and the gaps that are still worth filling later.
The goal is not full coverage on day one. Prioritize reusable platform actions and keep organization-specific rules separate.

## Layering Principles

- The `skill` owns executable actions: calling APIs, collecting results, and doing minimal validation.
- The `agent` owns judgment and communication: deciding when to call, how to guide users, and when to escalate to a human.
- Organization configuration owns rule differences: organization goals, allowed help types, matching fields, event rhythm, and reputation rules.

## Capabilities Already Integrated

The following workflows are already executable and should no longer be treated as pending baseline work:

- Authentication:
  `auth.guest.generate`, `auth.agent.third_login`, `auth.refresh`
- User profile:
  `user.profile.get`, `user.profile.update`
- Organization:
  `web.config.get`, `org.list`, `org.detail`, `org.detail.manage`, `org.create`, `org.update`, `org.member.list`, `org.member.page`, `org.join`
- Content:
  `content.post.create`
- Activity:
  `activity.save`, `activity.publish`, `activity.cancel`, `activity.delete`, `activity.detail`, `activity.search`, `activity.org.list`, `activity.user.sign.list`, `activity.sign.list`, `activity.signup`

The current operating workflow is mainly carried by post publishing and activity operations.
What the product currently calls a "help" capability is still implemented through `content.post.create` as a normal post, and there is no standalone help-post API yet.

## Capabilities Worth Adding Later

The following additions are still valuable, but they do not block the current minimum viable workflow:

| Priority | Capability ID | Capability Name | Purpose | Typical Input | Typical Output | Suggested API |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | interaction.comment.create / list | Comments and reviews | Support peer feedback, follow-up questions, and extra clarification | target content ID, comment body | comment records, time, author | Yes |
| P1 | help.offer.create / list | Publish available help | Support the "what I can help with" workflow | org ID, help type, description | help-offer records | Recommended |
| P1 | match.recommend | Matching recommendations | Let the agent proactively recommend people or tasks that fit | org ID, request ID, rule fields | candidate members or tasks | Recommended |
| P1 | interaction.feedback.create | Thanks and feedback | Provide positive input for the reputation system | target ID, score, thank-you text | feedback result | Recommended |
| P2 | reputation.get | Reputation and points lookup | Support ranking, recommendation, and incentives | user ID, org ID | points, reputation, badges | Optional later |
| P2 | summary.org.weekly | Summary and weekly digest | Let the agent output organization summaries and activity highlights | org ID, time range | aggregated data, cases | Optional later |
| P2 | moderation.report | Risk reporting | Handle harassment, no-shows, and offline safety risks | target ID, reason, evidence | report result | Optional later |

## Organization Configuration Should Not Become Direct Skill Capabilities

These items should live in organization configuration instead of being hardcoded into the skill:

- Organization name and one-line definition
- Target audience for joining
- Allowed help-request types
- Allowed help-offer types
- Matching fields such as city, style, schedule, or online/offline preference
- Fixed activity cadence
- Success criteria for mutual help
- Risk rules and prohibited behavior
- Copy tone and welcome messaging

## Preferred Order for Future API Additions

1. Comments and reviews
2. Publish and query available help
3. Matching recommendations
4. Thanks and feedback
5. Reputation, weekly digest, and risk control

## Information Needed for Each New Capability

Whenever you add a new capability, please provide as much of the following as possible:

- Which API implements it
- Where to find it in the project
- Whether it affects registration, login, or token flows
- Request method, path, and authentication mode
- Required and optional parameters
- The most important response fields
- Common error codes or failure scenarios
- Whether there are existing frontend or backend usage examples
