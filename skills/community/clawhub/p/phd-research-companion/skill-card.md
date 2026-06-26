## Description: <br>
A research workflow companion for computer science PhD students that helps initialize projects, search literature, analyze papers, generate LaTeX templates, track revisions, check math notation, and prepare submission-readiness reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yue123161](https://clawhub.ai/user/yue123161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and doctoral students use this skill to organize computer science research projects, automate literature and paper-review workflows, scaffold publication materials, and track revision and compliance evidence before advisor or venue review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review says the skill overstates some capabilities and that generated analyses or search outputs may be placeholders. <br>
Mitigation: Verify generated literature searches, paper analyses, and compliance reports against trusted source material before relying on them for research decisions. <br>
Risk: The server security review identifies under-disclosed local scanning, secondary file writes, and code-executing validation behavior. <br>
Mitigation: Run the skill in a dedicated test workspace first and review file paths and generated outputs before using it with important research materials. <br>
Risk: Background or scheduled runs can operate on broad paths or continue after the initiating session. <br>
Mitigation: Avoid enabling cron or background execution until output directories and input paths are constrained and monitored. <br>
Risk: Research topics and search workflow data may be logged locally or later sent to third-party services. <br>
Mitigation: Avoid sensitive or unpublished research topics unless logging and external-service exposure are acceptable for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yue123161/phd-research-companion) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [BACKGROUND-RUN.md](artifact/BACKGROUND-RUN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, generated project files, reports, LaTeX templates, BibTeX, JSON progress files, and YAML experiment configurations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local research project files and progress logs when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
