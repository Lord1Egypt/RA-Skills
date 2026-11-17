## Description:

Call LogicX frontend proxy APIs for health checks, browser binding, password login, user info, orders, payments, and account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qihangyang](https://clawhub.ai/user/qihangyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a LogicX account, verify account status, review orders and payments, and perform confirmed account actions through the LogicX proxy API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password login can expose user credentials through chat history or command arguments.

Mitigation: Prefer browser binding and do not send a password to the agent; the publisher should remove or replace the password-based flow.

Risk: The default service endpoint uses HTTP, which is not appropriate for real account authentication.

Mitigation: Use this only with a trusted HTTPS LogicX endpoint and avoid real accounts on the default HTTP endpoint.

Risk: Authentication headers could be sent outside the intended service if untrusted absolute URLs are accepted.

Mitigation: Restrict requests to the intended LogicX proxy API and reject untrusted absolute URLs before execution.

Risk: Saved LogicX user tokens are sensitive local credentials.

Mitigation: Protect the state file, avoid sharing its contents, and provide a clear token-clearing process before deployment.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Example Dialogues](examples.md)
- [ClawHub Skill Page](https://clawhub.ai/qihangyang/skills/logicx-skill-test)
- [Publisher Profile](https://clawhub.ai/user/qihangyang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown or plain text summaries with inline shell commands and JSON API responses when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist LogicX link state and user tokens in a local state file.]

## Skill Version(s):

0.0.8 (source: ClawHub release evidence, released 2026-03-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
