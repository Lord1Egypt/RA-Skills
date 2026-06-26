## Description: <br>
Comprehensive MBTI personality analysis tool with quick testing, cognitive function analysis, compatibility matching, and trending MBTI games. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shven273-design](https://clawhub.ai/user/shven273-design) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to explore MBTI-style personality types, run quick self-assessments, review cognitive-function summaries, compare compatibility, and generate entertainment-oriented MBTI games or daily readings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes exposed publishing credentials and publishing helpers that are unrelated to MBTI analysis. <br>
Mitigation: Treat bundled credentials as compromised, do not reuse them, and avoid publishing scripts unless you intentionally publish with your own authenticated accounts. <br>
Risk: Installation guidance includes a curl-to-bash pattern. <br>
Mitigation: Review downloaded files before execution and prefer a manual install path for controlled environments. <br>
Risk: The quick-test script stores result history under the user's home directory. <br>
Mitigation: Tell users where local history is written and remove the saved file when local retention is not desired. <br>
Risk: MBTI outputs can be mistaken for authoritative psychological or career advice. <br>
Mitigation: Use the results for entertainment and self-reflection only, not as the sole basis for consequential personal, hiring, medical, or relationship decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shven273-design/mbti-master) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/shven273-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance, often with inline bash commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive Bash scripts may ask questions, print MBTI summaries, and save quick-test history locally under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
