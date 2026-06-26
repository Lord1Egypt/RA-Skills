## Description: <br>
Interact with Moodle LMS to browse courses, access learning materials, and answer questions about course content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4strium](https://clawhub.ai/user/4strium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, instructors, and agents working with Moodle course spaces use this skill to configure Moodle access, list courses, inspect course structure, search course materials, download files, and extract PDF text for course questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Moodle credentials, direct tokens, and SSO bearer URLs that can grant account access. <br>
Mitigation: Install only if you trust the release, prefer a revocable or limited Moodle token, and treat SSO URLs and tokens like passwords. <br>
Risk: Broad sync or --no-confirm can store Moodle course materials locally, including private class content. <br>
Mitigation: Choose a private download path and use broad sync or --no-confirm only when you intend to keep the selected course materials locally. <br>
Risk: The setup flow downloads and runs a release binary. <br>
Mitigation: Verify the documented SHA256 checksum before running the binary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4strium/moodle-claw) <br>
- [Moodle Claw repository](https://github.com/4strium/moodle-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; Moodle CLI commands can return markdown or JSON and downloaded file paths or extracted text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache downloaded Moodle files locally and extract text from PDFs when commands use --text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
