## Description:

通过用户已打开的 Chrome 页面点击领取按钮，并以余额变化确认 ModelScope 每日魔粒领取结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ModelScope users use this skill to claim the daily Magicube allowance and check its balance through a browser session they opened themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional self-test visits live websites and could reach real claim buttons if its fake-page setup fails.

Mitigation: Use a dedicated browser profile with debugging restricted to loopback, avoid running the self-test in an authenticated browser until setup failures are handled reliably, and close the browser when finished.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/modelscope-magicube-checkin)
- [ModelScope Magicube introduction](https://modelscope.cn/docs/magicube/intro)
- [Chrome remote debugging port guidance](https://developer.chrome.com/blog/remote-debugging-port)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Text status reports, optional JSON results, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports CLAIMED, ALREADY, LOGGED_IN, NO_LOGIN, or UNKNOWN; JSON output is optional.]

## Skill Version(s):

1.3.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
