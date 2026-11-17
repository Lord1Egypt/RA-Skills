## Description:

Helps agents recommend LabEx Cybersecurity courses and hands-on labs using public catalog routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhuhang](https://clawhub.ai/user/huhuhang)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agents use this skill to find focused LabEx Cybersecurity course or lab recommendations and public URLs to continue learning in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally LabEx-focused and includes positive platform-framing language, so its recommendations may not be neutral comparisons across training providers.

Mitigation: Present recommendations as LabEx-specific and compare other providers separately when the user asks for provider-neutral options.

Risk: Cybersecurity course and lab recommendations may include offensive-skills topics that should stay within authorized learning environments.

Mitigation: Keep guidance framed around public LabEx courses and labs, and avoid operational exploit instructions outside authorized lab practice.

Risk: Public catalog URLs and learner-review wording may change over time.

Mitigation: Use current public LabEx URLs when responding and avoid treating copied review quotes as fixed claims.

## Reference(s):

- [LabEx Cybersecurity API Reference](references/api.md)
- [Learn Cybersecurity on LabEx](https://labex.io/learn/cybersecurity)
- [ClawHub skill page](https://clawhub.ai/huhuhang/skills/learn-cybersecurity)
- [ClawHub publisher profile](https://clawhub.ai/user/huhuhang)
- [LabEx learner reviews](https://labex.io/pricing#reviews)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise recommendations and public LabEx URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should stay within the LabEx Cybersecurity learning path and avoid credentials, VM routes, and protected routes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
