## Description:

Automates uploading multiple sources (files, URLs, YouTube, Drive, text) to a NotebookLM notebook, generating a deep dive audio overview in a preferred language, and downloading the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyanch](https://clawhub.ai/user/shiyanch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create NotebookLM deep-dive audio overviews from local files, URLs, YouTube links, Google Drive documents, or pasted text, then download the generated MP3 artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run unverified third-party code before authentication and document upload.

Mitigation: Review setup steps first, use pinned versions or a reviewed commit for the CLI and epub2txt, and inspect the GitHub run.sh script before running it.

Risk: Source documents are uploaded to NotebookLM during the audio generation workflow.

Mitigation: Only upload documents the user is comfortable sending to NotebookLM.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyanch/skills/notebooklm-audio-generator)
- [epub2txt GitHub repository](https://github.com/SPACESODA/epub2txt.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands and downloaded audio file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or retrieves an MP3 audio overview after NotebookLM generation completes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
