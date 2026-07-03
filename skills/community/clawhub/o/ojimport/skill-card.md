## Description: <br>
搬题姬 imports programming-contest problems from OJ platforms such as AtCoder and Codeforces, generates standardized problem packages, and can create test data from user-provided problem statements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and contest administrators use this skill to import OJ problems, format Chinese problem packages, write standard solutions, generate boundary-aware test data, and package files for judge systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The normal workflow creates, deletes, compiles, runs, and zips files in the active workspace. <br>
Mitigation: Install and run it only in a dedicated disposable or sandboxed project directory. <br>
Risk: Generated standard solutions and test generators are compiled and executed as part of producing outputs. <br>
Mitigation: Review generated std.cpp, mkin.h, and related configuration before compiling or running them. <br>
Risk: Cleanup and packaging steps can remove or overwrite work_* and testdata artifacts. <br>
Mitigation: Avoid running it where work_* directories or testdata files contain content that must be preserved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fslong520/skills/ojimport) <br>
- [Test Data Design Reference](artifact/references/testdata-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with generated C++ source, YAML configuration, .in/.out test files, and zip archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and remove work directories, compile generated C++ programs, run test-data generators, and package judge-ready archives.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
