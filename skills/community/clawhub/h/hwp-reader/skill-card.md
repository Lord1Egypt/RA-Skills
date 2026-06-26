## Description: <br>
Extract and analyze text, tables, images, and metadata from Korean HWP and HWPX documents, supporting both legacy and modern formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read, extract, summarize, compare, and draft content for Korean Hangul Word Processor documents, including government forms and HWP/HWPX templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed or untrusted HWP/HWPX files can stress document parsers. <br>
Mitigation: Handle untrusted documents in an isolated workspace and keep parsing dependencies up to date. <br>
Risk: Adapted command snippets can target the wrong file if paths are copied without care. <br>
Mitigation: Use safely quoted file paths and verify the target document before running extraction commands. <br>
Risk: Text extraction may omit formatting, table structure, or full preview content. <br>
Mitigation: Review the original document when layout, tables, or complete content affect the decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/hwp-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets plus extracted document text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Legacy HWP extraction depends on pyhwp; HWPX extraction uses ZIP and XML parsing from the Python standard library.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
