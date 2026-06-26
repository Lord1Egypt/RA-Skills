## Description: <br>
Operate, debug, and automate Hospitable via its Public API with a read-first workflow for properties, reservations, calendars, and non-price calendar controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwill2023](https://clawhub.ai/user/jiangwill2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, developers, and automation builders use this skill to inspect Hospitable properties, reservations, and calendars, then plan or apply controlled non-price calendar changes with delayed verification. It is intended for Hospitable account workflows where authenticated API access and human approval for writes are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The write helper can make broad authenticated Hospitable API requests beyond the documented calendar-only workflow. <br>
Mitigation: Require human approval for every non-GET request, keep writes limited to documented non-price calendar actions, and verify the exact endpoint, method, and body before execution. <br>
Risk: The skill relies on a Hospitable token and may export reservation or calendar data. <br>
Mitigation: Use the least-privileged token available, never expose the token in chat or logs, and protect exported JSON files that contain account, reservation, or calendar details. <br>
Risk: Calendar writes may be asynchronous, so immediate readback can misrepresent whether a change succeeded. <br>
Mitigation: Wait after accepted writes, re-read the same date window, and compare operational fields before relying on the result. <br>
Risk: Changing HOSPITABLE_BASE_URL could direct authenticated requests away from Hospitable's official API. <br>
Mitigation: Keep HOSPITABLE_BASE_URL pinned to Hospitable's official API base URL unless a trusted operator explicitly approves a different endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangwill2023/hospitable-ops) <br>
- [Hospitable Public API v2 base URL](https://public.api.hospitable.com/v2/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request or response excerpts, and operational status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read helpers return a statusCode/body JSON envelope; write workflows should report the tested object and date, acceptance or rejection, delayed readback, conclusion, and remaining gap.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
