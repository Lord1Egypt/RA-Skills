## Description: <br>
Execute commands on the host machine from inside the OpenClaw container via the HostLink daemon, using authenticated remote shell execution over a Unix domain socket or TCP/WireGuard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use HostLink when an OpenClaw agent needs intentional access to host-side files, Docker, GPU or ML tools, or other commands that cannot run inside the container. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables commands to run on the host rather than only inside the OpenClaw container. <br>
Mitigation: Install it only for workflows that intentionally require host access, and require explicit user approval before each host command. <br>
Risk: A persistent daemon, socket, or token can expose broad host command execution if misconfigured or leaked. <br>
Mitigation: Protect the auth token and Unix socket, keep the token out of git, restrict socket permissions, and run the daemon as a dedicated least-privileged user where possible. <br>
Risk: Host-side installation uses sudo and may run commands as the daemon user, often root when installed with systemd. <br>
Mitigation: Review and pin the HostLink daemon source before sudo installation, and confirm the daemon account, shell, timeout, output, and concurrency settings before use. <br>
Risk: Remote TCP transport can expose host command execution beyond the local container boundary. <br>
Mitigation: Avoid direct TCP exposure; use WireGuard for remote access and keep TCP disabled unless the deployment explicitly requires it. <br>


## Reference(s): <br>
- [HostLink Setup Guide](references/setup.md) <br>
- [HostLink source repository](https://github.com/jebadiahgreenwood/hostlink) <br>
- [HostLink ClawHub page](https://clawhub.ai/jebadiahgreenwood/hostlink) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return command output as text or JSON when hostlink is invoked with JSON output enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
