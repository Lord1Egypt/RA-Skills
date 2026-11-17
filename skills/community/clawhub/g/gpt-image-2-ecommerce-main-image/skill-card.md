## Description:

Uses GPT Image 2 through AI Hive to create ecommerce main images, product hero images, white-background catalog shots, and A/B test variants from product reference images while preserving product facts and channel rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, operators, and creative teams use this skill to draft platform-aware product main images, listing hero images, promotional layouts, and thumbnail test variants from approved product references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent to an arbitrary endpoint if the base URL is changed.

Mitigation: Use only the official HTTPS AI Hive endpoint unless you control and trust the replacement server.

Risk: Product reference files are uploaded to the image-generation service.

Mitigation: Provide only images and media that are approved for upload to the service.

Risk: The packaged client includes broader AI Hive commands than the advertised ecommerce image workflow.

Mitigation: Review the script before installation and run it in a dedicated environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-ecommerce-main-image)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; generated image files and JSON task status from the AI Hive API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multiple reference images, batch generation, model parameters, routing mode selection, task polling, and a configurable output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0 and should be reviewed)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
