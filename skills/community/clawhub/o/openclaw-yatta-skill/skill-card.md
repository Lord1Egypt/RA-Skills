## Description: <br>
Personal productivity system for task and capacity management that helps agents create and organize tasks with rich attributes, track time and streaks, manage capacity across projects and contexts, view Eisenhower Matrix prioritization, sync calendar subscriptions, handle delegation and follow-ups, and get AI-powered insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisagiddings](https://clawhub.ai/user/chrisagiddings) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Yatta! tasks, projects, contexts, comments, calendar subscriptions, follow-ups, capacity, analytics, and Eisenhower Matrix views through API-backed workflows. It is suited for explicit, user-directed productivity operations where the user reviews task changes before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a full-access Yatta API key that can read, create, update, archive, delete, and sync account data. <br>
Mitigation: Install only if full-account API access is acceptable, store the key securely, avoid hardcoding it, and rotate or revoke unused keys. <br>
Risk: Unsafe command examples that interpolate user-controlled values into JSON bodies or URLs can expose credentials or corrupt task data. <br>
Mitigation: Use the provided safe wrapper script or jq-based payload construction and URL encoding before executing API calls. <br>
Risk: Batch updates, deletes, archives, calendar syncs, and follow-up changes can modify multiple records or trigger immediate account changes. <br>
Mitigation: Confirm the target records and operation effects before running destructive or bulk commands. <br>
Risk: API keys may be sent to an unexpected endpoint if YATTA_API_URL is misconfigured. <br>
Mitigation: Verify YATTA_API_URL before use and send credentials only to trusted Yatta endpoints. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chrisagiddings/openclaw-yatta-skill) <br>
- [Yatta! app](https://yattadone.com) <br>
- [Yatta! API documentation](https://yattadone.com/docs/api) <br>
- [API-REFERENCE.md](API-REFERENCE.md) <br>
- [SECURITY.md](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YATTA_API_KEY, YATTA_API_URL, curl, and jq; examples should use safe jq payload construction and URL encoding.] <br>

## Skill Version(s): <br>
0.2.2 (source: package.json, CHANGELOG, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
