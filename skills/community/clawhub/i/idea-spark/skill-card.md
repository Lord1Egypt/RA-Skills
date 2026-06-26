## Description: <br>
Generates actionable project ideas for a requested domain by researching public pain points and optionally checking each idea with idea-check. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, builders, and product teams use Idea Spark to turn a domain or interest into ranked project ideas grounded in public pain points from Hacker News, Reddit, and GitHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web-backed research can surface stale, noisy, or unverified public complaints. <br>
Mitigation: Review the cited pain points before using generated ideas for product planning or implementation. <br>
Risk: Optional validation may run a local mcporter command when idea-check and idea-reality are installed. <br>
Mitigation: Review the separate validation tool before enabling automatic checks, or skip validation when the tool is unavailable or untrusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spideystreet/idea-spark) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown list of ranked project ideas with pain-point sources, effort estimates, and optional validation signals.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source labels from web research and optional validation status when idea-check is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
