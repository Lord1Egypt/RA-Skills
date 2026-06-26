## Description: <br>
Scores lead domains from 0 to 100 by analyzing website, DNS, sitemap, and social-presence signals with customizable JSON scoring profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, partnerships, and growth teams use this skill to qualify and prioritize lead domains, including single-domain checks, multi-domain runs, and CSV batch scoring. Developers can adjust JSON scoring profiles to emphasize the website, DNS, content, social, contact, or keyword signals that matter for their outreach workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script makes DNS and web requests to the domains supplied by the user. <br>
Mitigation: Run it only against domains you intend to evaluate and avoid untrusted or internal targets unless private-address blocking is added. <br>
Risk: The web fetch path disables normal TLS certificate verification. <br>
Mitigation: Restore standard TLS certificate verification before relying on scores at scale or in production workflows. <br>
Risk: Results can be written to a user-selected output path. <br>
Mitigation: Choose output locations deliberately and review generated JSON before sharing it outside the scoring workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/psyduckler/lead-scorer-free) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON to stdout or a user-selected output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes domain score, grade, per-signal evidence, raw collected data, and a summary; batch mode returns one result per domain.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
