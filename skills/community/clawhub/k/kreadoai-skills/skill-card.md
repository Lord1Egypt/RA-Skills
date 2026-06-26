## Description: <br>
KreadoAI Skills helps an agent call KreadoAI for digital avatar video generation, text-to-speech, instant avatar cloning, account queries, and subtitle or watermark removal through Node.js subcommands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifefiei](https://clawhub.ai/user/shifefiei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate KreadoAI media workflows from an agent, including API token configuration, account checks, avatar selection or upload, video generation, TTS synthesis, instant avatar cloning, and subtitle or watermark removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar cloning can be used on likenesses without clear consent. <br>
Mitigation: Use clone and avatar upload workflows only for people or assets the user owns or has explicit permission to modify. <br>
Risk: Subtitle or watermark removal can remove attribution or rights signals from third-party media. <br>
Mitigation: Avoid using removal workflows on third-party media unless the user has documented rights to edit it. <br>
Risk: Media URLs, image URLs, and generated content are sent to KreadoAI services. <br>
Mitigation: Do not submit sensitive media unless the user accepts KreadoAI processing; disclose that remote API calls are required. <br>
Risk: KREADO_API_TOKEN can be exposed through logs, screenshots, shell history, or source control. <br>
Mitigation: Prefer environment variables or the credentials file with restricted permissions, and do not echo or commit tokens. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shifefiei/kreadoai-skills) <br>
- [KreadoAI OpenAPI homepage](https://www.kreadoai.com/openapi) <br>
- [KreadoAI API documentation](https://kreadoai.gitbook.io/kreadoai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, a KreadoAI Pro account, and KREADO_API_TOKEN or stored credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
