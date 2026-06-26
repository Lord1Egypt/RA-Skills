## Description: <br>
Checks and rewrites Amazon product listing copy to flag prohibited or high-risk wording, suggest safer alternatives, and produce Rufus-oriented listing variants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and listing copywriters use this skill to review Amazon product titles and bullet points, replace risky claims, add scenario and intent language, and generate multiple compliant copy options for manual publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compliance report may be mistaken for official Amazon approval or legal advice. <br>
Mitigation: Treat the output as advisory drafting support and manually verify final listing text before publishing. <br>
Risk: The bundled Python checker executes local code when run by an agent or user. <br>
Mitigation: Review the script and run it only in an environment where local code execution is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/miaoji-compliance-copy) <br>
- [Banned Words Reference](references/banned-words.md) <br>
- [Compliance Checker Script](scripts/compliance-checker.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown-style compliance reports and rewritten listing copy, with optional JSON output from the bundled checker script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes compliance scores, matched terms, replacement suggestions, Rufus keyword coverage, search term suggestions, and multiple rewritten copy variants.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
