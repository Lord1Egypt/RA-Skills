## Description:

Helps cross-border ecommerce teams recreate the structure of a reference viral product video with the user's product assets, generating a replacement video prompt and delegating final video creation to LinkFox generation skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketers, and creators use this skill to turn a reference viral short video and their own product images into a structurally similar product video for target markets and languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use real LinkFox credentials and make credential-bearing network calls through bundled dependencies.

Mitigation: Run it only in trusted environments, protect LinkFox API keys, and avoid endpoint override environment variables unless the destination is controlled.

Risk: Reference-video and product-image URLs may point to untrusted, private, or unauthorized media.

Mitigation: Use only trusted URLs and media the user has rights to process, and review inputs before running generation.

Risk: Fallback frame extraction and file upload can make derived frames or uploaded media publicly accessible.

Mitigation: Do not process private media unless public exposure is acceptable, and review frame/upload outputs before sharing them downstream.

Risk: Bundled onboarding and payment flows can create API keys or start payment orders.

Mitigation: Use onboarding or payment commands only when the operator intends to log in, create credentials, or purchase capacity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-aigc-videogen-viral-replicate)
- [Workflow reference](artifact/references/workflow.md)
- [API mapping reference](artifact/references/api.md)
- [Prompt contract](artifact/references/prompts.md)
- [Data fields reference](artifact/references/data-fields.md)
- [Test cases](artifact/examples/test-cases.md)
- [Text generation dependency API](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [Multi-image video generation dependency API](artifact/skills/linkfox-aigc-videogen-multi/references/api.md)
- [File upload dependency API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown/text workflow output with local MP4 path strings from downstream video generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reference-video and product-image URLs; downstream video results are returned as local MP4 paths, while raw temporary video URLs are not shown.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
