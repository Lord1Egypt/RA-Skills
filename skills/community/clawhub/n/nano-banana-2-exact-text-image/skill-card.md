## Description:

Guides agents to generate or edit Nano Banana 2 images through AI Hive for short, exact text in posters, product cards, social covers, and packaging concepts, with text-cell planning and manual proofing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent operators use this skill to prepare concise image-generation prompts, run the fixed Nano Banana 2 helper, and proof short visible text before using generated marketing or concept assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper requires an AI Hive API key and stores or reads credentials locally.

Mitigation: Use a dedicated low-privilege API key, prefer a virtual environment, and keep local credential files restricted to the current user.

Risk: Reference images selected by the user may be uploaded to the AI Hive service.

Mitigation: Upload only images approved for that service and avoid sensitive, private, or regulated source material unless separately authorized.

Risk: Security evidence flags broad handling of remote URLs and output filenames.

Mitigation: Run the skill in a controlled environment, set a dedicated output directory, and review downloaded files before reuse.

Risk: Generated visible text may contain substitutions, missing characters, extra text, or layout problems.

Mitigation: Proof every text cell character by character and switch to a text-free background plus manual layout for prices, dates, model numbers, legal claims, QR codes, or long copy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-exact-text-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash examples, JSON configuration, Python helper code, and downloaded image files from API tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Nano Banana 2 public model, optional reference-image uploads, an AI Hive API key, polling for task status, and a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
