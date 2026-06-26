## Description: <br>
Leaptic is an OpenClaw skill for Leaptic device snapshot and status access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulei2140](https://clawhub.ai/user/liulei2140) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve a read-only Leaptic device snapshot, including battery, charging state, storage, media counts, and related timestamps, after the user provides a Leaptic App-Key and regional API base URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Leaptic App-Key is a secret and may be exposed if pasted into untrusted tools, sent to an untrusted host, or stored carelessly. <br>
Mitigation: Use only documented Leaptic regional hosts or an explicitly trusted base URL, treat the App-Key like a password, and prefer environment variables or an OS secret store over plaintext storage. <br>
Risk: Using the wrong regional base URL can send a credential to an unintended endpoint. <br>
Mitigation: Ask the user for the CN, EU, or US region when the base URL is unset and do not guess or retry blindly against another domain. <br>


## Reference(s): <br>
- [Leaptic homepage](https://www.leaptic.tech/) <br>
- [ClawHub release page](https://clawhub.ai/liulei2140/lp-test) <br>
- [CN device snapshot endpoint](https://photon-prod.leaptic.tech/photon-server/api/v1/skill/device/snapshot) <br>
- [EU device snapshot endpoint](https://photon-eu.leaptic.tech/photon-server/api/v1/skill/device/snapshot) <br>
- [US device snapshot endpoint](https://photon-us.leaptic.tech/photon-server/api/v1/skill/device/snapshot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for a disclosed read-only HTTP snapshot request and expected JSON response handling.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
