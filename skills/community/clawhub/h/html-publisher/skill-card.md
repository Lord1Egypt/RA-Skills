## Description: <br>
Publishes selected HTML content as an online web page and returns an accessible public URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyi9531](https://clawhub.ai/user/huyi9531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and content creators use this skill to publish static HTML through the gnomic CLI and retrieve a public URL for sharing, review, or lightweight web delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published HTML and referenced resources become publicly accessible. <br>
Mitigation: Review HTML before publishing and remove secrets, private content, internal links, tokens, and sensitive embedded resources. <br>
Risk: The workflow may require installing and running gnomic-cli globally from npm. <br>
Mitigation: Verify that gnomic-cli is trusted and install it only in an approved environment. <br>


## Reference(s): <br>
- [gnomic-cli source repository](https://github.com/huyi9531/gnomic_cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow returns or extracts a public URL from gnomic CLI JSON or text output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
