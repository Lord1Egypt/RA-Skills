## Description: <br>
Huo15 Skills is a third-party OpenClaw skill collection centered on enterprise Word/PDF document generation, with additional modules for web scraping, knowledge bases, PPT creation, SearXNG deployment, and agent workflow modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this toolkit to generate business documents, automate office artifacts, create knowledge bases, scrape JavaScript-rendered sites, deploy self-hosted search, and coordinate planning, exploration, verification, and multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes multiple unrelated high-impact tools beyond the advertised Word/PDF document workflow. <br>
Mitigation: Review the package contents before installation and remove or avoid subdirectories that are not needed for the intended use. <br>
Risk: Some modules can use sensitive credentials, login cookies, local files, or cloud upload workflows. <br>
Mitigation: Run the skill in an isolated workspace, provide only task-specific credentials, and inspect configuration before any scraping, upload, or credential-backed action. <br>
Risk: Some modules can deploy Docker services or coordinate multi-agent execution and process permissions. <br>
Mitigation: Review shell scripts before execution, use least-privilege accounts, and explicitly confirm ports, processes, and spawned-agent actions. <br>


## Reference(s): <br>
- [Huo15 Skills on ClawHub](https://clawhub.ai/zhaobod1/huo15-skills) <br>
- [Package README](artifact/README.md) <br>
- [Primary Skill Definition](artifact/SKILL.md) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaobod1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with generated code, shell commands, configuration snippets, and file-producing script workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify DOCX, PDF, PPTX, knowledge-base, scraped-data, Docker, and OpenClaw configuration artifacts depending on the selected subskill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
