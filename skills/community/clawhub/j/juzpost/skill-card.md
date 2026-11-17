## Description:

Schedule and publish social media posts with JuzPost, a free social media scheduler with low-cost paid plans, from the terminal. Upload a video or image, create a draft, and schedule it to TikTok, YouTube Shorts, Instagram, X, Facebook, LinkedIn, Pinterest, Bluesky, Threads, Tumblr or WordPress, or smart-schedule a batch of drafts across an account group. Use when the user wants to post to social media or plan a content calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juzpost](https://clawhub.ai/user/juzpost)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create social media drafts and schedule or publish them across their connected accounts from a terminal. It also guides setup, account discovery, media uploads, and batch scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external juzpost-cli package implementation was outside the inspected artifact.

Mitigation: Check the CLI package before installing it.

Risk: Scheduling or publishing affects connected social accounts and their audiences.

Mitigation: Connect only intended accounts, upload only intended media, review each publishing confirmation, and get the user's approval before scheduling or publishing. Preview smart-scheduling plans with a dry run first.

## Reference(s):

- [JuzPost Skill on ClawHub](https://clawhub.ai/juzpost/skills/juzpost)
- [JuzPost](https://www.juzpost.com)
- [juzpost-cli on npm](https://www.npmjs.com/package/juzpost-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before scheduling or publishing; smart-scheduling plans are previewed with a dry run first.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
