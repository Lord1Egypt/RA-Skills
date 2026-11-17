## Description:

Turns supplied security policies and awareness materials into an interactive digital-human security awareness course that learners can interrupt with voice questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Security and training teams use this skill to create awareness courses from their own security policies and source materials. It supports course creation, source upload, grounded review, optional assessment, and delivery of the correct private or share URL after the course is playable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can run service-provided commands and install native executables.

Mitigation: Install only if the PersonWise release and update service are trusted, and approve only exact commands that are clearly PersonWise CLI or skill updates.

Risk: The workflow can use browser OAuth, upload selected documents, consume existing course credits, and publish or share a course when requested.

Mitigation: Use only user-selected materials, keep the default access target private unless broader access is requested, and require new approval for additional courses, payments, broader visibility, deletion, transfer, or organization administration.

Risk: A course could overstate security outcomes or include unsupported security facts if the source material is weak or ambiguous.

Mitigation: Keep the course grounded in supplied materials, avoid claims of certification or guaranteed security, and route suspected incidents only to reporting channels named in the materials.

## Reference(s):

- [Security Awareness Training ClawHub Skill Page](https://clawhub.ai/personwiseai/skills/personwise-security-awareness-training)
- [PersonWise Publisher Profile](https://clawhub.ai/user/personwiseai)
- [PersonWise Service](https://personwise.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Concise text or Markdown with JSON command inputs and CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return run IDs, project IDs, source statuses, review results, terminal state, access mode, and the correct playable course URL.]

## Skill Version(s):

2.1.9 (source: server release evidence and skill attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
