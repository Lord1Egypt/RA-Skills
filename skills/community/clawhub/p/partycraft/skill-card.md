## Description: <br>
Plan events with budgets, guest lists, and timelines. Use when organizing weddings, coordinating birthdays, managing vendors, drafting invitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Partycraft to plan weddings, birthdays, corporate events, and parties from the command line by tracking budgets, tasks, guests, timelines, and checklist suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied event names, guest names, task text, IDs, and budget values can be embedded into local Python source by the shell script and may execute unintended local code. <br>
Mitigation: Review before use, avoid untrusted pasted inputs, and run only in a trusted local environment until arguments are passed as data. <br>
Risk: Event planning data is persisted locally in ~/.partycraft/events.json. <br>
Mitigation: Delete ~/.partycraft/events.json when saved planning data is no longer needed and avoid storing sensitive guest or budget details unless local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/partycraft) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [CLI text output with local JSON data persistence] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists event records under ~/.partycraft/events.json.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0 and script info says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
