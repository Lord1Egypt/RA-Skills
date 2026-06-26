## Description: <br>
Intelligent code security scanner with hybrid local-cloud detection that fingerprints packages, runs static behavioral analysis, and consults cloud threat intelligence for confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinxiaotian1](https://clawhub.ai/user/jinxiaotian1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to vet third-party code packages before installation. It produces a safety score, threat labels, and review guidance based on package fingerprints, static behavior tags, and optional cloud threat intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Matched scan evidence is sent to as.dun.163.com by default. <br>
Mitigation: Install only when the publisher is trusted; set YIDUN_SKILL_SEC_CLOUD=false before scanning private, regulated, or proprietary code. <br>
Risk: The server release name is my-test-skill, but artifact files identify the skill as yidun-skill-sec. <br>
Mitigation: Verify the release identity and publisher before relying on the skill's security verdicts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinxiaotian1/my-test-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jinxiaotian1) <br>
- [Yidun cloud threat intelligence endpoint](https://as.dun.163.com/v1/agent-sec/skill/check) <br>
- [ClawHub ecosystem](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a numeric safety score, threat labels, source-vetting results, local behavioral findings, and cloud-intelligence status when enabled.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
