## Description: <br>
Smart LLM Router for OpenClaw. Save up to 70% by routing every request to the right model. No coding required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Manifest to route LLM requests across supported providers while tracking usage, costs, and routing health. It supports local evaluation and cloud setup for teams that want spend controls and observability around agent traffic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud mode may send prompts, request metadata, usage data, or other LLM request contents to Manifest without enough upfront privacy disclosure. <br>
Mitigation: Prefer local mode for confidential, regulated, customer, source-code, or credential-bearing work unless the publisher documents collection, retention, protections, and how to disable cloud transfer. <br>
Risk: The skill requires a sensitive Manifest API key for cloud setup. <br>
Mitigation: Store the API key in the configured OpenClaw secret or environment mechanism, avoid committing it to files, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [Manifest documentation and source](https://github.com/mnfst/manifest) <br>
- [Manifest homepage](https://manifest.build) <br>
- [Manifest cloud app](https://app.manifest.build) <br>
- [ClawHub skill page](https://clawhub.ai/seanford/manifest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mentions MANIFEST_API_KEY for cloud authentication and supports local mode with data stored under ~/.openclaw/manifest/manifest.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
