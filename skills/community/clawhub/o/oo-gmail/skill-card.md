## Description: <br>
Gmail (workspace.google.com). Use this skill for ANY Gmail request: reading, creating, updating, and deleting data through the OOMOL Gmail connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate Gmail through an OOMOL-connected account. It supports reading and searching mail, managing drafts, labels, filters, mailbox settings, and performing confirmed send, reply, trash, and bulk label workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive Gmail actions can change mailbox state, send messages, or move and delete drafts, filters, labels, messages, and threads. <br>
Mitigation: Confirm the exact action, target, payload, and expected effect with the user before write actions; require explicit approval for destructive actions. <br>
Risk: Incorrect payloads or stale assumptions about connector inputs can cause failed actions or unintended Gmail changes. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing payloads and use label, message, draft, thread, and filter IDs returned by read actions. <br>


## Reference(s): <br>
- [ClawHub Gmail skill page](https://clawhub.ai/oomol/oo-gmail) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Gmail homepage](https://workspace.google.com/gmail/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; command responses include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
