## Description: <br>
Converts complex medical abstracts into plain language summaries for patients, caregivers, and the general public while preserving scientific accuracy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ewankeynes](https://clawhub.ai/user/ewankeynes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Health communicators, clinical research teams, and developers can use this skill to turn medical research abstracts into draft plain-language summaries for patients, caregivers, media, or the public. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain-language medical summaries may omit nuance, overstate findings, or otherwise be mistaken for medical advice. <br>
Mitigation: Treat generated summaries as drafts and have qualified health or research reviewers verify accuracy before sharing them with patients or the public. <br>
Risk: This is third-party local Python code executed in the user's environment. <br>
Mitigation: Inspect the script and run it only in an environment where local execution from this publisher is acceptable. <br>


## Reference(s): <br>
- [Lay Summary Gen References](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ewankeynes/lay-summary-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object containing a lay summary, reading level, key takeaways, word counts, target audience, and replaced jargon] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one abstract at a time; max_words defaults to 250.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
