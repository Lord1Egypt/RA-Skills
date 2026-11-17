## Description:

Guides ChatCut talking-head and screen-recording edits through a reviewable sample, approvals, and an editable timeline handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maojiebc](https://clawhub.ai/user/maojiebc)

### License/Terms of Use:

MIT

## Use Case:

Creators use this skill to plan and review ChatCut edits of spoken videos and screen recordings, approve a representative sample before full-length changes, and receive an editable timeline with a verification report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled repository instructions may require pushing code to a remote branch without fresh approval.

Mitigation: Review repository instructions before use and require explicit authorization for each remote push.

Risk: Export, generated media, music, and motion graphics may exceed the intended edit scope.

Mitigation: Keep these actions disabled unless the user specifically approves them.

Risk: Offline checks and simulations do not establish that real ChatCut edits look and sound correct.

Mitigation: Mark real end-to-end results unverified until fresh ChatCut evidence and human review support them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/maojiebc/skills/majia-chatcut-koubo)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language review and handoff report; editable ChatCut timeline when supported and approved]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Export and publication are off by default; unverified real-world editing outcomes must not be reported as validated.]

## Skill Version(s):

1.7.0 (source: server release, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
