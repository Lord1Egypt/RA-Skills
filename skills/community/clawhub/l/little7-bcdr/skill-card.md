## Description: <br>
Create, maintain, and verify Little7 business continuity and disaster recovery backups for identity, memory, learnings, scripts, and local skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little7unifai](https://clawhub.ai/user/little7unifai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, automate, retain, and verify Little7 continuity backups for local identity, memory, learnings, scripts, skills, and selected documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup process can copy private identity, memory, keys, tokens, or other secrets into backup archives. <br>
Mitigation: Review LITTLE7_SECRET_PATHS_FILE or docs/LITTLE7_SECRET_PATHS.txt before use, keep secrets archives separate, and protect or encrypt backup destinations you control. <br>
Risk: Cron-driven backups may silently write archives to an unintended Google Drive or filesystem location if environment variables are wrong. <br>
Mitigation: Confirm LITTLE7_WORKSPACE_ROOT, LITTLE7_GDRIVE_BASE, and cron entries before enabling automation. <br>
Risk: Restore readiness can be overstated if only archive filenames are checked. <br>
Mitigation: Use the health check and inspect archive contents for critical identity, memory, script, and secrets markers before claiming restore readiness. <br>


## Reference(s): <br>
- [Little7 Bcdr ClawHub release](https://clawhub.ai/little7unifai/little7-bcdr) <br>
- [Publisher profile](https://clawhub.ai/user/little7unifai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create tar.gz backup archives, latest pointers, and restore manifest files when the bundled shell scripts are run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
