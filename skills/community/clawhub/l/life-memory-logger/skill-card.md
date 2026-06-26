## Description: <br>
生活记忆记录器。帮你记录人际交往中的重要细节（生日、喜好、承诺），自动提醒跟进，让你成为更贴心的人。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-productivity agents use this skill to record relationship details such as birthdays, preferences, commitments, and follow-up reminders in local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal relationship notes, including potentially sensitive health, financial, conflict, or third-party private information. <br>
Mitigation: Store only information the user is comfortable retaining, request confirmation before saving sensitive details, and periodically review or delete saved memories. <br>
Risk: Relationship memories can be misused or disclosed to the wrong person. <br>
Mitigation: Keep each person's notes private, do not share one person's information with another, and be transparent when asked how a detail was remembered. <br>
Risk: The artifact references helper scripts that are not included in the submitted files. <br>
Mitigation: Treat referenced helper scripts as unavailable until separately supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/life-memory-logger) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON memory record examples and reminder configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update local memory records under /memory/life-memories when the host agent has file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
