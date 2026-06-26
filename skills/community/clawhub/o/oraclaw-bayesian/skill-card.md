## Description: <br>
Bayesian inference engine for AI agents. Update beliefs with new evidence. Prior + evidence = posterior. Multi-factor prediction with calibration tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Oraclaw Bayesian to update prior probabilities with weighted evidence, combine multiple evidence sources, and return posterior estimates with factor contributions and calibration information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prediction inputs may include sensitive evidence sent to the OraClaw service. <br>
Mitigation: Avoid submitting sensitive evidence unless the service's privacy and retention terms have been reviewed. <br>
Risk: Repeated predictions may create paid usage after the free tier. <br>
Mitigation: Use a revocable API key and monitor usage and billing for the ORACLAW_API_KEY account. <br>


## Reference(s): <br>
- [OraClaw Bayesian homepage](https://oraclaw.dev/bayesian) <br>
- [ClawHub release page](https://clawhub.ai/whatsonyourmind/oraclaw-bayesian) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON-compatible Bayesian prediction result with posterior probability, factor contributions, and calibration score.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; paid API use may incur USDC charges after the free tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
