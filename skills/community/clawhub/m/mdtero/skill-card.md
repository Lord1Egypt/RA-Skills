## Description: <br>
Use when a user wants Mdtero to parse a paper from a DOI or URL into a structured Markdown package, translate a parsed paper while keeping structure, or download Mdtero task artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonbinc](https://clawhub.ai/user/jonbinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and external users use this skill to parse research papers into structured Markdown packages, translate parsed papers while preserving structure, and retrieve generated paper artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parse and translate requests may send selected paper content or paper-source material to Mdtero. <br>
Mitigation: Use this workflow only for content the user is comfortable sending to Mdtero, and avoid sensitive or proprietary manuscripts unless that boundary is accepted. <br>
Risk: The workflow uses MDTERO_API_KEY and may also use ELSEVIER_API_KEY for local acquisition. <br>
Mitigation: Keep API keys private, pass them through environment variables, and avoid exposing them in shared logs, prompts, or checked-in files. <br>
Risk: Elsevier or ScienceDirect acquisition may require a separate local helper on the user's machine. <br>
Mitigation: Review the helper locally before running it and avoid piping remote installer scripts directly into the shell. <br>


## Reference(s): <br>
- [Mdtero homepage](https://mdtero.com) <br>
- [Mdtero guide](https://mdtero.com/guide) <br>
- [Mdtero skill install handoff](https://api.mdtero.com/skills/install.md) <br>
- [ClawHub skill page](https://clawhub.ai/jonbinc/mdtero) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide downloads of paper_md, paper_bundle, optional paper_pdf, and translated_md artifacts.] <br>

## Skill Version(s): <br>
0.1.9 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
