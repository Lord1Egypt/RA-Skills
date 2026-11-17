## Description: <br>
memory-distiller-free helps an agent compress Markdown memory logs into structured summaries with key events, todo items, and keyword-based extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to distill long daily Markdown memory logs into shorter structured summaries for archiving, review, and storage reduction. It is intended for single-file log compression workflows that may read local logs, run a Node.js command, and write Markdown output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local memory logs and write distilled summaries back into persistent memory. <br>
Mitigation: Review the source logs and generated summaries before appending output to MEMORY.md, and avoid processing sensitive or confidential logs unless that storage path is approved. <br>
Risk: The skill documentation includes Node.js command execution and references a required memory-compress.js script that is not present in the artifact evidence. <br>
Mitigation: Require the publisher to provide and document the referenced script before execution, then inspect the script and run it only in a controlled workspace. <br>
Risk: The documentation mixes local-only processing claims with callback URL, external API, and credential guidance. <br>
Mitigation: Do not provide API keys or callback URLs unless the intended data flow is explicitly reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-distiller-free) <br>
- [Published skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be written to a Markdown summary file and appended to persistent memory after user review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
