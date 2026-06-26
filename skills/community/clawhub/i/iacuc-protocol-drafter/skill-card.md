## Description: <br>
Draft IACUC protocol applications with focus on the 3Rs principles justification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, compliance staff, and developers use this skill to draft local IACUC protocol text from structured JSON input, with emphasis on Replacement, Reduction, and Refinement justification sections. Generated text is a draft that requires institution-specific and factual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads an input path and can write an output path supplied by the user. <br>
Mitigation: Run it in an intended workspace and avoid pointing input or output arguments at sensitive files. <br>
Risk: Generated IACUC protocol language may be incomplete, inaccurate, or mismatched to local institutional requirements. <br>
Mitigation: Treat output as a draft and have qualified institutional, regulatory, and scientific reviewers verify the protocol before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/iacuc-protocol-drafter) <br>
- [Publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text protocol draft from JSON input, written to stdout or a local output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports sample JSON generation, stdin input, local file input, and local file output using Python 3.8+ standard library.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
