## Description:

Helps developers use JF device APIs to check device status, log in, capture live snapshots, and retrieve livestream URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate JF camera/device API workflows, including token retrieval, device login, status checks, snapshot capture, and livestream URL retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private JF credentials, device tokens, session IDs, snapshot URLs, and livestream URLs may be exposed in agent logs or shared terminal output.

Mitigation: Run only in trusted sessions, avoid shared logging for capture or livestream operations, and treat printed tokens and media URLs as credentials.

Risk: JF_ENDPOINT can direct API calls away from the intended service if set incorrectly.

Mitigation: Leave JF_ENDPOINT unset or set it only to a trusted official JF API host before execution.

Risk: Capture and livestream commands expose live device media to the current session output.

Mitigation: Run capture or livestream commands only when exposing that device media to the current agent session is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jftech-open-pro-capture-livestream)
- [JF Open Platform](https://open.jftech.com/)
- [JF API Documentation](https://docs.jftech.com/)
- [JF International API endpoint](https://api.jftechws.com)
- [JF China API endpoint](https://api-cn.jftech.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print device tokens, session IDs, snapshot URLs, and livestream URLs that should be treated as credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
