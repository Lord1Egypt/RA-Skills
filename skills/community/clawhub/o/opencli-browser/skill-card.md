## Description:

Helps an agent drive a real Chrome window via opencli to inspect pages, fill forms, click through logged-in flows, extract ad-hoc data, and handle selector-first targeting, compound fields, stale references, network capture, and structured CLI envelopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to control a live Chrome browser through opencli for page inspection, form interaction, logged-in workflows, and ad-hoc data extraction. It is not intended for building reusable opencli adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to drive a real browser session, including logged-in workflows and potentially sensitive form fields.

Mitigation: Use explicit approval for sensitive steps and avoid passwords, MFA codes, payment data, and high-impact account changes unless each action is reviewed.

Risk: Browser automation can make real changes to pages, forms, or accounts if an agent acts on the wrong target.

Mitigation: Inspect before acting, prefer fresh refs from the current page state, and verify critical writes with read-back commands.

Risk: Captured network responses may contain sensitive data and can remain available in the opencli network cache.

Mitigation: Close the browser session when finished and clear the opencli network cache after sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/opencli-browser)
- [Publisher profile](https://clawhub.ai/user/liberalchang)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes structured command envelopes, selector or ref targeting, and verification after browser writes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
