## Description: <br>
Use when working with Halo CLI login, bearer token or basic auth, profile setup, profile switching, current profile inspection, or fixing missing keyring credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, inspect, switch, and repair Halo CLI authentication profiles for bearer-token or basic-auth workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication tokens or passwords could be exposed in shared transcripts, terminal history, or copied command examples. <br>
Mitigation: Review commands before running them and avoid exposing bearer tokens or basic-auth passwords in shared logs or shell history. <br>
Risk: Using profile delete --force against the wrong profile can remove credentials or configuration needed for a Halo CLI environment. <br>
Mitigation: Confirm the current target profile and URL before running destructive profile deletion commands. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ruibaby/halo-cli-auth) <br>
- [Publisher profile](https://clawhub.ai/user/ruibaby) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend --json for structured CLI output when another tool consumes profile information.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter shows 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
