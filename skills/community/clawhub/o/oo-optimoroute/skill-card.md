## Description: <br>
OptimoRoute lets agents read, create, update, merge, sync, and delete OptimoRoute orders through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate OptimoRoute order workflows from an agent session, including order retrieval, bulk create/update/sync operations, and explicitly approved deletions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback setup can install the oo CLI by running a remote installer script directly in a shell. <br>
Mitigation: Review the installation path first, prefer manual installation from OOMOL's official instructions, and verify the source before allowing installation. <br>
Risk: The skill can perform write and destructive OptimoRoute order actions. <br>
Mitigation: Inspect the live action schema, review the exact payload and target records, and require explicit user approval before write or delete actions. <br>


## Reference(s): <br>
- [OptimoRoute homepage](https://optimoroute.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-optimoroute) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run oo CLI connector commands that return JSON responses from OptimoRoute.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
