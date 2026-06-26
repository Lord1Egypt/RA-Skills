## Description: <br>
Extracts and summarizes the most relevant webpage passages for focused, low-token research without loading or summarizing the full page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agitalent](https://clawhub.ai/user/agitalent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use LiteBrowse to answer focused questions from specific webpages or local HTML files while keeping context size small and citing the extracted supporting blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extractor can fetch URLs or read local HTML files supplied to the agent, which may expose private, authenticated, or internal content if those sources are used unintentionally. <br>
Mitigation: Use it only with URLs or local HTML files the user intends to inspect, and avoid private files, authenticated pages, or internal network addresses unless that access is deliberate. <br>


## Reference(s): <br>
- [LiteBrowse on ClawHub](https://clawhub.ai/agitalent/litebrowse) <br>
- [LiteBrowse documentation](https://agitalent.github.io/LiteBrowse.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and extracted text or JSON block references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bounded extraction settings such as top-k and maximum character limits to keep returned context compact.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
