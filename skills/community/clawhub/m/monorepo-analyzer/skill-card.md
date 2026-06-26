## Description: <br>
Analyze monorepo structure - detect workspace tools, map inter-package dependencies, find unused packages, detect version inconsistencies, compute build order, and identify circular dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit monorepos during onboarding, maintenance, or CI health checks by inspecting workspace configuration, package dependency relationships, cycles, version mismatches, unused packages, and build order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository statistics can expose recent contributor activity through Git history. <br>
Mitigation: Avoid running the stats command in repositories where recent contributor activity is sensitive. <br>
Risk: The skill reads package manifests, workspace configuration, source file counts, and Git history when those analyses are requested. <br>
Mitigation: Run it only in repositories where that local project metadata is appropriate for the agent to inspect. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python command blocks, plus optional text, JSON, Markdown, or Mermaid reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not install dependencies; reads package manifests, workspace configuration, source file counts, and Git history when repository statistics are requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
