## Description: <br>
Drafts interpretive comments for complex laboratory panel results, including delta-check flags, critical-value notation, pattern recognition, and clinical-correlation language for pathologist or licensed-provider review before result release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical laboratory scientists, pathologists, lab directors, residents, and fellows use this skill to draft reviewed interpretive comments for complex laboratory panels. It supports abnormal-result summaries, critical-value notation, delta-check language, specimen-quality notes, pattern interpretation, and clinical-correlation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks the bundle suspicious because an included autoreview helper defaults to nested review tooling with full sandbox bypass. <br>
Mitigation: Manually review the bundle before installation and disable full-access autoreview defaults, for example by using --no-yolo where applicable. <br>
Risk: Fallback review workflows may expose private code or secrets if diffs contain sensitive material. <br>
Mitigation: Avoid fallback reviewers for sensitive diffs and use scoped credentials for any moderation workflow. <br>
Risk: Draft clinical language could be incorrect, incomplete, or inappropriate for local laboratory policy. <br>
Mitigation: Require licensed pathologist or authorized-provider review, confirm institutional reference ranges and critical thresholds, and do not release or transmit results from the draft. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/interpretive-lab-comment-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft interpretive comment with review block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft output only; licensed pathologist or authorized provider review is required before release.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and changelog, released 2026-05-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
