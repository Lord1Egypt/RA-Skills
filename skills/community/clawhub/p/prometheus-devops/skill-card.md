## Description: <br>
Prometheus monitoring - scrape configuration, service discovery, recording rules, alert rules, and production deployment for infrastructure and application metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and SREs use this skill to set up Prometheus scraping, service discovery, recording rules, alert rules, and production monitoring practices for infrastructure and application metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unverified install sources or Helm chart updates could introduce unexpected behavior during deployment. <br>
Mitigation: Verify the npx and Helm sources before installation and pin Helm chart versions for production deployments. <br>
Risk: Prometheus scrape targets and credentials may expose sensitive infrastructure or over-broad access. <br>
Mitigation: Review scrape targets before use and apply least-privilege credentials. <br>
Risk: remote_write destinations can send metrics to untrusted storage if configured carelessly. <br>
Mitigation: Enable remote_write only for trusted storage destinations. <br>


## Reference(s): <br>
- [Prometheus Community Helm Charts](https://prometheus-community.github.io/helm-charts) <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/prometheus-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Prometheus configuration templates, alert rules, recording rules, validation commands, and operational best-practice guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
