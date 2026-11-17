## Description:

Wraps HLE benchmark questions in a structured Chain-of-Thought (CoT) reasoning process. Use when answering HLE questions to ensure strict step-by-step logic and format compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to format Humanity's Last Exam benchmark questions with a required reasoning and final-answer structure, then validate whether model outputs follow that structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports an undeclared persistent answer cache that can save user questions or model answers to disk.

Mitigation: Avoid using the cache with sensitive questions or answers unless it is removed, documented, or changed to an opt-in design with safer keying and retention controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Plain text prompt template and JavaScript validation result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies are declared.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
