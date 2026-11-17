## Description:

JF Tech child-care monitoring skill for checking service status, querying child-care alarms, managing stranger entries, and retrieving activity statistics for connected home devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to interact with JF Tech child-care monitoring APIs for device status, alarm review, stranger/person-library updates, and activity summaries. It requires configured JF Tech account, device, token, and package credentials before use.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill handles sensitive child-care, household, device, account, and credential data.

Mitigation: Install only when the publisher is trusted, restrict access to configured credentials, and review outputs before sharing child-care or household information.

Risk: Credentials and tokens may be exposed when passed directly as command-line arguments.

Mitigation: Prefer environment variables or another secret store, avoid shell history exposure, and rotate any credentials already passed on the command line.

Risk: Service switches and stranger/person-library changes can alter monitoring behavior or household safety records.

Mitigation: Require explicit human approval before enabling or disabling analysis or adding or removing stranger entries.

Risk: The security summary notes that the documented regional endpoint setting is ignored by the artifact behavior.

Mitigation: Verify the intended data region before use and confirm whether API requests go to the expected JF Tech endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-child-care)
- [JF Tech developer portal](https://developer.jftech.com)
- [JF Tech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [JF Tech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [JF Tech package card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python scripts call JF Tech HTTPS APIs and can return either formatted human-readable text or JSON when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
