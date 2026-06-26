## Description: <br>
Common input handling for Java Maven project review workflows that unpack ZIP archives or clone GitLab repositories, normalize the project root, and identify Maven modules before deeper review or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a shared intake layer for Java Maven review workflows when project source arrives as a ZIP archive or GitLab repository URL. It prepares a normalized project root and Maven module summary for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe work or JSON output paths can cause local files to be deleted or overwritten. <br>
Mitigation: Run the helper only with disposable temporary work directories and non-critical JSON output paths. <br>
Risk: Untrusted ZIP archives or cloned repositories can introduce unsafe project contents into the local workspace. <br>
Mitigation: Unpack or clone into isolated temporary directories and scan inputs before downstream review. <br>
Risk: Repository URLs can expose credentials if credential-bearing URLs are supplied. <br>
Mitigation: Use user-authorized SSH access and avoid credential-bearing repository URLs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [JSON summary and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project intake metadata including input mode, normalized root path, project name, Maven module list, module count, and scan-limited status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
