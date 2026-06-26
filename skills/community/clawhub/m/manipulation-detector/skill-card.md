## Description: <br>
Analyze text for manipulation patterns such as urgency, false authority, social proof, FUD, grandiosity, dominance assertions, us-vs-them framing, and emotional manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudio-prime](https://clawhub.ai/user/claudio-prime) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents, developers, and other users use this skill to review messages, social posts, or text files for common manipulation-pattern signals before deciding how much skepticism to apply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keyword matching can produce false positives or miss subtle manipulation that does not use obvious phrases. <br>
Mitigation: Treat the report as a rough signal and combine it with human judgment, context, and other review methods. <br>
Risk: The script reads user-provided text or local files selected at runtime. <br>
Mitigation: Run it only on text or files you intend to analyze, and avoid providing sensitive content unless local analysis is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text CLI report with scores, flags, and matched patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads stdin or a local text file and does not require network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
