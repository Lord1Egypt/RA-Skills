## Description: <br>
Acts as the user's social life assistant in the Friends topic. Remembers friends, birthdays, plans, debts, shared interests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GekaCross](https://clawhub.ai/user/GekaCross) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a personal social-memory assistant to track friends, birthdays, meeting plans, shared interests, gift ideas, and debts in a local friends note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal details about friends, birthdays, plans, gift ideas, and debts in a persistent workspace file. <br>
Mitigation: Review or delete knowledge/personal/friends.md when saved information should be removed, and avoid storing details about other people that should not persist in the agent workspace. <br>
Risk: Friend and relationship details could be exposed in an inappropriate chat context. <br>
Mitigation: Keep the stored friend information private and do not share it in group chats. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown notes and conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update knowledge/personal/friends.md with friend profiles, dates, plans, debt notes, and gift ideas.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
