## Description:

Queries Huawei Cloud CES monitoring metric lists and metric datapoints with read-only ListMetrics and ShowMetricData operations, returning JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and site reliability engineers use this skill to inspect Huawei Cloud CES metric catalogs and retrieve metric datapoints for monitoring checks, performance analysis, alert investigation, and capacity planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags cloud credential handling as overly broad and process-visible.

Mitigation: Use a scoped, read-only Huawei IAM identity and prefer a safer hcloud profile or secret mechanism instead of passing long-lived AK/SK through process-visible command arguments.

Risk: Dynamic scanning of Huawei-like environment variables may select credentials that were not intended for this skill.

Mitigation: Run the skill in a constrained shell or task environment that exposes only the intended Huawei Cloud credentials.

Risk: The documented remote hcloud installer is not verified by the artifact.

Mitigation: Verify or pin the hcloud installer before execution, or install KooCLI through a trusted package management path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huawei-cloud-ces-list)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud CES API reference](https://support.huaweicloud.com/api-ces/ces_03_0057.html)
- [IAM permissions](artifact/iam-policies.md)
- [hcloud CLI installation guide](artifact/cli-installation-guide.md)
- [Verification method](artifact/verification-method.md)
- [Dataflow diagram](artifact/dataflow-diagram.md)
- [Acceptance criteria](artifact/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses from the skill, with Markdown guidance and shell command examples in the documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [List output includes count, total, marker, and metrics; show output includes metric_name and datapoints; errors are JSON on stderr with non-zero exit codes.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
