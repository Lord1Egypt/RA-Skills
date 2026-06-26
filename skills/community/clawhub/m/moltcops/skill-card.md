## Description: <br>
Moltcops is a local-first pre-install security scanner for AI agent skills that detects malicious patterns before users trust code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adamthompson33](https://clawhub.ai/user/Adamthompson33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Moltcops to scan AI agent skill folders before installation or execution, looking for prompt injection, code execution, data exfiltration, persistence, and related high-risk patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A clean scan result may miss unsafe behavior outside the scanner's rule patterns. <br>
Mitigation: Use Moltcops as a local advisory scanner and still review the skill source, requested permissions, and provenance before installation. <br>
Risk: Scanning the wrong directory can produce misleading results. <br>
Mitigation: Run the scanner only against the specific skill directory and version intended for inspection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Adamthompson33/moltcops) <br>
- [MoltCops web scanner](https://scan.moltcops.com) <br>
- [MoltCops website](https://moltcops.com) <br>
- [Moltbook profile](https://moltbook.com/u/MoltCops) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with PASS, WARN, or BLOCK verdicts and finding summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file-system scan using Python standard library rules; no network calls are described in the artifact.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
