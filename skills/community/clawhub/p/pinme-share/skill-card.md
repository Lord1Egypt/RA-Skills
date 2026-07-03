## Description: <br>
Upload local files or directories to PinMe public IPFS and return a short shareable URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to publish files, directories, or generated HTML to PinMe and get a public URL for sharing. It also supports setup, history, unpin, wallet, and logout workflows for PinMe accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publicly publish local files to IPFS, where content may remain accessible after unpinning. <br>
Mitigation: Use it only for files intended for public release and avoid private, credential, client, or unreleased material. <br>
Risk: The helper may auto-install and invoke the PinMe npm CLI. <br>
Mitigation: Preinstall and verify the PinMe CLI in controlled environments when possible. <br>
Risk: A PinMe AppKey can be persisted locally for reuse. <br>
Mitigation: Use PINME_APPKEY for temporary sessions when appropriate, inspect stored credentials, and run logout after testing. <br>


## Reference(s): <br>
- [ClawHub Pinme Share page](https://clawhub.ai/songhonglei/pinme-share) <br>
- [PinMe service](https://pinme.eth.limo) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and final-line JSON output from the upload helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads may produce public PinMe/IPFS URLs; warnings and progress are sent to stderr while structured results are emitted as JSON on stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and artifact README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
