## Description:

Observe, intercept, and modify browser network requests and responses through Chrome DevTools Protocol, including traffic monitoring, request blocking, response mocking, header, cookie, query, body, and page content changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github-hewei](https://clawhub.ai/user/github-hewei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to observe browser HTTP traffic, test behavior under modified network conditions, block unwanted requests, and mock or rewrite request and response data for sites they control or are authorized to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can observe and alter browser traffic, including cookies, credentials, request and response bodies, and page content.

Mitigation: Use it only on sites you control or are authorized to test, and avoid real accounts, production credentials, payment flows, and sensitive third-party sessions.

Risk: Broad or ambiguous interception rules can modify unintended traffic.

Mitigation: Start in observe mode when rules are not explicit, narrow match conditions, review rules before running, and prefer a pinned install version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/github-hewei/skills/network-request-twister)
- [Actions reference](references/actions.md)
- [Conditions reference](references/conditions.md)
- [Basic rule example](examples/basic.json)
- [Request modification example](examples/request-mod.json)
- [Response modification example](examples/response-mod.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON rule configuration snippets; observe mode can produce JSONL network logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rules are passed as JSON configuration, preferably through STDIN; response bodies may be truncated in observation mode unless full-body observation is requested.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
