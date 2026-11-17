## Description:

Turns one authorized product image and verified product facts into a Chinese ad-production workflow with ten differentiated creative angles, scripts, prompts, optional AI-HIVE image or video generation commands, task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, agency operators, and ad-testing teams use this skill to plan and execute controlled A/B creative production from limited product media. It helps the agent produce a reviewable plan first, then optional AI-HIVE commands for paid image or video generation after confirming prompts, routing, media rights, and costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send an AI-HIVE API key to a configurable API endpoint.

Mitigation: Use only an AI-HIVE key approved for paid generation, keep the default official API endpoint, and avoid AI_HIVE_BASE_URL, --base-url, or config base_url values that point to untrusted hosts.

Risk: Image or video generation can incur costs or submit unauthorized media.

Mitigation: Confirm prompts, uploaded media rights, routing mode, and expected costs before running generation commands; start with a small sample before expanding a batch.

Risk: Ad content may contain unsupported claims, copied creative elements, or misleading testimonials.

Mitigation: Use only verified product facts and authorized references, mark uncertain claims for review, and avoid copying protected lines, logos, people, music, watermarks, or platform-evasion tactics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/one-product-image-ten-ads-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections, inline shell commands, JSON task records, prompts, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, AI-HIVE task IDs, downloaded media paths, and ffmpeg command output when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
