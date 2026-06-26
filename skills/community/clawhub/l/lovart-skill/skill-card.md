## Description: <br>
Generate images, videos, and audio or music through Lovart AI while managing Lovart projects, conversation threads, uploads, downloads, and generation settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovart-admin](https://clawhub.ai/user/lovart-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to send Lovart media-generation requests, manage Lovart projects and threads, upload reference files, and retrieve generated files through the provided command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Lovart API credentials. <br>
Mitigation: Install it only when Lovart access is intended, provide credentials through trusted environment variables, and rotate credentials if they may have been exposed. <br>
Risk: The skill can reuse persistent Lovart project and thread state. <br>
Mitigation: Review saved Lovart configuration and thread selections before generation or history actions, and use explicit Lovart wording for project or history requests. <br>
Risk: The skill can upload local files and download generated artifacts from remote URLs. <br>
Mitigation: Review files before upload and be cautious with arbitrary download URLs or generated artifact links from untrusted contexts. <br>


## Reference(s): <br>
- [ClawHub Lovart Skill](https://clawhub.ai/lovart-admin/lovart-skill) <br>
- [Lovart Project Canvas](https://www.lovart.ai/canvas?projectId={project_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations, JSON command output, and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Lovart API credentials and may save project and thread state locally for reuse.] <br>

## Skill Version(s): <br>
1.0.10 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
