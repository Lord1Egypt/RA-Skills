## Description: <br>
Generate videos with Google Veo models via inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to generate text-to-video outputs with Google Veo models through the inference.sh CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on the external inference.sh CLI distribution and cloud service. <br>
Mitigation: Install only when inference.sh is trusted and prefer manual checksum verification before use. <br>
Risk: Video prompts and input files may be sent to a cloud service after login. <br>
Mitigation: Use the intended account and avoid including confidential material in prompts or input files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okaris/google-veo) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Streaming Results](https://inference.sh/docs/api/sdk/streaming) <br>
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) <br>
- [CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI-oriented instructions and prompts for running Google Veo video-generation apps through inference.sh.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
