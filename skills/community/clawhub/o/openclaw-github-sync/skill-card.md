## Description: <br>
Keep an OpenClaw agent's non-sensitive context (selected memory, MD files, notes, and custom skills) under version control in a separate Git repository for remote review/tweaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bradvin](https://clawhub.ai/user/bradvin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to export selected workspace context to a private Git repository for review, version control, scheduled push syncs, and manual pull-back of reviewed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default sync setup can upload broad memory, persona, and skill files to a private Git repository. <br>
Mitigation: Narrow references/export-manifest.txt to reviewed non-sensitive files and prefer memory/public over raw memory before enabling scheduled sync. <br>
Risk: Pulling from the sync repository can overwrite workspace files that affect future agent behavior. <br>
Mitigation: Treat pull as high-risk: run a dry run, review changes manually, and do not automate pull operations. <br>
Risk: Repository credentials can grant access to exported agent context. <br>
Mitigation: Use least-privilege GitHub credentials or a deploy key for the private sync repository. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/bradvin/openclaw-github-sync) <br>
- [Export manifest](references/export-manifest.txt) <br>
- [Commit grouping rules](references/groups.json) <br>
- [Secret scan ignore rules](references/secret-scan-ignore.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and generated repository files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, rsync, python3, and SYNC_REMOTE for normal sync operation.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
