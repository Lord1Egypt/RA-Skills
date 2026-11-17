## Description:

Calls JD Cloud Lingjing JoyCreator AI generation APIs through a three-stage workflow that parses image or video requests, recommends a supported Doubao, Hailuo, Kling, or PaiWo model, and builds or submits the API task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scorpiongao](https://clawhub.ai/user/scorpiongao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn natural language image or video requests into JoyCreator model choices, request parameters, executable Python or shell usage, and submitted generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JoyCreator App Key exposure could allow unauthorized use of the connected account.

Mitigation: Provide the key through a protected environment variable or hidden secret input, avoid chat text and command-line flags, and rotate the key if it may have been exposed.

Risk: Prompts, image URLs, and reference media are sent to an external JoyCreator API provider.

Mitigation: Do not submit confidential prompts, private images, or non-expiring public media URLs unless that external processing is acceptable.

Risk: Submitted generation tasks may consume JD Cloud JoyCreator account quota or create billable usage.

Mitigation: Confirm intended use, model choice, and request parameters before submitting tasks to the API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scorpiongao/skills/lingjingtest)
- [Router rules](references/router-rules.md)
- [Model choice rules](references/choice-rules.md)
- [Doubao JoyCreator API reference](references/doubao.md)
- [Hailuo JoyCreator API reference](references/hailuo.md)
- [Kling JoyCreator API reference](references/kling.md)
- [PaiWo JoyCreator API reference](references/paiwo.md)
- [JoyCreator submitTask endpoint](https://model.jdcloud.com/joycreator/openApi/submitTask)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown or terminal text with JSON request bodies, Python or curl examples, and JoyCreator task identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external JoyCreator API and return a generated task ID rather than final media.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
