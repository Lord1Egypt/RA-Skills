## Description:

Jeju With helps users view booking guidance, submit appointment requests, consult customer service, and check prices for Jeju With Hospital through BeautsGO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get multilingual booking instructions, submit Jeju With Hospital appointment requests, open consultation or hospital pages, and look up treatment pricing through BeautsGO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appointment details may be sent to BeautsGO without a separate final confirmation.

Mitigation: Require an explicit confirmation step before submission and show the selected hospital, appointment date/time, party size, source metadata, and any phone number provided.

Risk: The browser-opening helper uses shell-based URL launching.

Mitigation: Replace shell-based opening with an argument-safe launcher while keeping the HTTPS domain allowlist.

Risk: API tokens are present in distributed source.

Mitigation: Move API tokens to managed secrets or deployment configuration before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/jeju-with-clinic-booking)
- [BeautsGO publisher profile](https://clawhub.ai/user/beautsgo)
- [Jeju With Hospital booking page](https://i.beautsgo.com/cn/hospital/jeju-island-with-hospital/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking guidance, appointment submission status, price summaries, consultation links, and app download links.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
