## Description:

Provides a local-first task queue for routing work across machines to Ollama or cloud services, with offline sync, retries, and resumable processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use it to queue and route batch, document, and other tasks between a workstation and a local Ollama worker, then sync results across machines. It also provides guidance for optional cloud routing when work needs web access or stronger reasoning.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Routing labels do not guarantee sensitive task data stays local; tasks and results are plaintext, and live integrations and external releases were not audited.

Mitigation: Before confidential work, explicitly assign L1 and verify Ollama uses a local endpoint. Review routing before enabling cloud integrations, and review and pin optional packages before running them.

Risk: Importing a sync package can replace an existing record when the incoming record has a matching ID and a newer timestamp.

Mitigation: Import only trusted synchronization files and keep backups.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/medxpert-offline-taskbox)
- [MedXpert hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON task records and sync packages, generated text results, and Markdown guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task processing results are plaintext; worker output is limited to a short conclusion, bullet points, and next steps. Routing is heuristic and may require manual level selection.]

## Skill Version(s):

2.4.10 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
