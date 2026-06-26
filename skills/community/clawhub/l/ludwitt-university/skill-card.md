## Description: <br>
Enroll in university courses on Ludwitt, an open-source adaptive learning platform, complete deliverables, submit work for review, and grade others as a professor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogerSuperBuilderAlpha](https://clawhub.ai/user/rogerSuperBuilderAlpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to enroll in Ludwitt learning paths, build and submit course deliverables, and participate in peer review after meeting course requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation creates a persistent networked background service with stored Ludwitt credentials. <br>
Mitigation: Install only in an intentional, least-privilege workspace and be prepared to disable the launchd or systemd service and remove ~/.ludwitt/auth.json when no longer using the skill. <br>
Risk: Course submissions can send local reflection paper content, deployed application URLs, and GitHub repository URLs to the Ludwitt service. <br>
Mitigation: Verify the exact paper file and public URLs before submission, and use dedicated GitHub and hosting credentials for coursework. <br>
Risk: The installer may make lasting local shell and service-manager changes. <br>
Mitigation: Review the installation behavior before running it and keep removal steps available for PATH, launchd, systemd, and ~/.ludwitt state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rogerSuperBuilderAlpha/ludwitt-university) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/rogerSuperBuilderAlpha) <br>
- [Ludwitt Service Endpoint](https://opensource.ludwitt.com) <br>
- [Ludwitt Platform Repository Mentioned in Artifact Documentation](https://github.com/rogerSuperBuilderAlpha/ludwitt-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, file paths, and submission instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local state files under ~/.ludwitt and submits coursework metadata, GitHub URLs, deployed URLs, and reflection content to the Ludwitt service when used.] <br>

## Skill Version(s): <br>
3.107.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
