## Description: <br>
Helps an agent coach users through a four-cluster intrinsic motivation audit and a bounded 30-day experiment when drive has faded without clinical or external-constraint causes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for motivation coaching when a user reports lost drive, post-achievement flatness, early burnout signals, or difficulty sustaining effort. It guides a four-cluster audit, identifies depleted motivation sources, and produces one concrete 30-day experiment with a next audit date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat motivation coaching as medical or mental-health advice. <br>
Mitigation: Use the skill only for motivation coaching and route clinical depression, severe burnout, or treatment needs to qualified professional support. <br>
Risk: Personal motivation, burnout, or work-history details could be retained unnecessarily. <br>
Mitigation: Do not save user-specific motivation details back into the skill unless the user explicitly chooses that and the details are anonymized first. <br>
Risk: The skill may be applied when external constraints or domain mismatch, rather than motivation depletion, are the real blocker. <br>
Mitigation: Apply the documented fit checks and stop-rule before designing experiments, and avoid using the skill when resources, structural barriers, or clinical concerns are primary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/intrinsic-drive) <br>
- [Primary sources](references/sources.md) <br>
- [Marie Curie example](examples/marie-curie-1891-1934.md) <br>
- [Intrinsic Motivation and Self-Determination in Human Behavior](https://doi.org/10.1007/978-1-4899-2271-7) <br>
- [Flow: The Psychology of Optimal Experience](https://www.harpercollins.com/products/flow-mihaly-csikszentmihalyi) <br>
- [Madame Curie: A Biography](https://archive.org/details/madamecurie012961mbp) <br>
- [Curie's laboratory notebooks](https://gallica.bnf.fr/ark:/12148/btv1b9064022h) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coaching response with a structured Drive Source Portfolio and 30-day experiment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include 1-5 cluster ratings, depleted and active sources, behavioral commitment, success indicator, and next audit date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
