## Description: <br>
Scans iOS development disk usage across simulators, runtimes, device support, DerivedData, CocoaPods cache, archives, Swift Package Manager cache, and Xcode caches, then offers cleanup commands with before-and-after reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesseluo](https://clawhub.ai/user/jesseluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill on macOS systems with Xcode to inspect local iOS development storage and decide which simulator, runtime, cache, archive, or build artifacts to clean up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete unavailable simulator devices and runtimes before the user reviews the full scan results. <br>
Mitigation: Run it in report-only mode first and require explicit approval for every delete command, including unavailable simulator and runtime cleanup. <br>
Risk: Cleanup commands can remove local Xcode caches, archives, device support files, or build artifacts that may be expensive or inconvenient to recreate. <br>
Mitigation: Review the generated summary tables before deletion, confirm archive status before removing xcarchive files, and prefer the documented Xcode or simctl commands for simulator resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jesseluo/ios-dev-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports scanned categories, top items by size and last-used metadata, cleanup choices, and reclaimed disk space.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
