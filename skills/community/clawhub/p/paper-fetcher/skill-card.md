## Description: <br>
Fetch academic papers from Sci-Hub given a DOI, download PDFs, and save them with clean filenames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biohackerrrrrr](https://clawhub.ai/user/biohackerrrrrr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, and developers use this skill to retrieve papers by DOI and build a local PDF collection in a workspace. It is intended for workflows where the user supplies a DOI or PubMed context and wants a saved paper file plus a confirmation path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Sci-Hub to retrieve papers, which can raise legal, institutional-policy, and source-trust concerns. <br>
Mitigation: Use only when permitted by applicable rules and prefer lawful publisher, library, or open-access sources when required. <br>
Risk: Downloaded PDFs are written into the workspace and may come from a third-party source. <br>
Mitigation: Use a dedicated output folder such as research/papers/ and open downloaded files with normal document-safety precautions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biohackerrrrrr/paper-fetcher) <br>
- [Sci-Hub domain used by the skill](https://www.sci-hub.su) <br>
- [DOI resolver](https://doi.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Terminal text with saved PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads PDFs to a workspace output directory, commonly research/papers/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
