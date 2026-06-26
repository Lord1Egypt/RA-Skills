## Description: <br>
Batch clone GitLab group projects, check out key branches, and generate an Excel index of project metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pangfan](https://clawhub.ai/user/pangfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to clone or update repositories from GitLab groups or project paths, preserve group hierarchy, check out key branches, and create a project index spreadsheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitLab token handling can expose or over-privilege repository access during cloning and API calls. <br>
Mitigation: Review the script before use, run it in a controlled environment, use a least-privilege read-only GitLab token, and avoid passing secrets in command-line URLs. <br>
Risk: TLS verification is disabled while the skill uses a GitLab token. <br>
Mitigation: Re-enable TLS verification or configure a trusted internal certificate authority before using the skill with protected repositories. <br>
Risk: Runtime dependency installation can fetch unpinned packages. <br>
Mitigation: Preinstall pinned dependencies in a managed environment instead of allowing runtime package installation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Git repositories and an Excel index when the script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
