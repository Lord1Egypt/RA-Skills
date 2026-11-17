## Description:

Transcribes Chinese meeting audio with OpenAI Whisper and combines recordings with PPT, image, or PDF materials to produce page-aligned speech reconstruction PDFs, Word meeting minutes, or TXT transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulei223344-lang](https://clawhub.ai/user/fulei223344-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused teams use this skill to turn meeting or presentation recordings into transcripts, structured meeting minutes, or slide-aligned speech reconstruction documents when supporting PPT, image, or PDF materials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python packages before processing.

Mitigation: Run it in a controlled virtual environment and pin or verify packages before approving installation.

Risk: Meeting recordings, transcripts, and presentation materials may contain confidential or regulated information.

Mitigation: Use approved local storage and avoid sensitive recordings unless the processing environment, retention behavior, and generated files are acceptable.

Risk: Generated transcripts or reconstructed presentation pages may be inaccurate when audio quality is poor or materials do not match the recording.

Mitigation: Review the generated PDF, Word, or TXT output before sharing or using it as an authoritative record.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fulei223344-lang/skills/ppt-speech-fusion)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and Python code; generated deliverables may be PDF, Word, or TXT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process user-provided recordings and PPT, PDF, or image materials; PDF reconstruction mode aligns generated pages to source material pages.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
