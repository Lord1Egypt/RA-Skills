## Description: <br>
PhiProto CLI helps agents inspect, decode, encode, and convert .phiproto files to and from CSV using the phicli command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengongpp](https://clawhub.ai/user/chengongpp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect PhiProto message files, decode them into CSV for review, or encode CSV data back into .phiproto artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup downloads an external phicli executable and installs it into $HOME/.local/bin, which places it on a commonly used command path. <br>
Mitigation: Install only if you trust the external release; prefer manually downloading the pinned release, checking any available checksum or signature, and reviewing getphi.sh before installation. <br>
Risk: The bundled workflow depends on a Linux x86_64 binary from an external GitHub release. <br>
Mitigation: Use the skill only on supported Linux x86_64 systems and avoid substituting binaries from other sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengongpp/phiproto) <br>
- [phicli 0.0.2 release binary](https://github.com/chengongpp/phiproto/releases/download/0.0.2/phicli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional CSV or .phiproto output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may run phicli locally to decode .phiproto files to CSV or encode CSV files to .phiproto, usually writing results to an explicit output path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
