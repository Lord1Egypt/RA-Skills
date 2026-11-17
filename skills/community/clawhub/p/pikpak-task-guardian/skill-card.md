## Description:

Monitors PikPak cloud-download tasks and can optionally submit new tasks for failed items from a user-maintained source list, using bounded backoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak users can review cloud-download task status and receive an at-a-glance summary. With separate authorization, they can enable notifications or submit a new task for a failed item when its exact source is registered; this is not an in-place retry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional resubmission creates a new PikPak task and may consume connected-app quota; an uncertain result could leave the submission outcome unclear.

Mitigation: Enable resubmission only when wanted, use an exact registered task-to-source match, check account quota, and manually reconcile submitting or unknown outcomes before trying again.

Risk: Task and account state can be confused if the active PikPak account, local command environment, or state directory is not the intended trusted one.

Mitigation: Verify the active account, use a distinct account scope, and keep the CLI environment, private state directory, and source registry under trusted control.

Risk: A local notification command returning successfully does not confirm that a person saw the notification.

Mitigation: Treat notification status as local acceptance only and verify important task outcomes in PikPak.

## Reference(s):

- [PikPak CLI](https://mypikpak.com/cli)
- [PikPak CLI help](https://mypikpak.com/en-US/help-center/connected_apps/pikpak_cli)
- [PikPak connected-app speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [Upstream design notes](references/upstream-design.md)
- [Celery bounded backoff reference](https://github.com/celery/celery/blob/ef37e616ef6726a2e08126635c000f3eacffcbc2/celery/utils/time.py)
- [python-telegram-bot network retry reference](https://github.com/python-telegram-bot/python-telegram-bot/blob/577e9c784607a42ff17746b9864b6416c3c30593/src/telegram/ext/_utils/networkloop.py)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown summaries and guidance, with shell command snippets and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize task counts. Notifications and new-task submissions are opt-in and require separate user authorization.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
