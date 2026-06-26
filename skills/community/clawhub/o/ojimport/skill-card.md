## Description: <br>
从 OJ 平台搬运题目（含 AtCoder、Codeforces 等），生成标准化题目文件包；也可根据用户提供的题目仅生成测试数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Competitive programming educators, platform maintainers, and developers use this skill to import OJ problems from URLs, files, or text into standardized problem packages with Chinese statements, reference solutions, HydroOJ configuration, generated test data, and zip archives. It can also generate only test data when the user already has a complete problem statement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can delete local work or work_* directories during initialization. <br>
Mitigation: Run it in a scratch workspace and check for existing work directories before use. <br>
Risk: The workflow compiles and runs generated std.cpp and mkdata C++ programs to produce outputs. <br>
Mitigation: Review generated C++ before execution and prefer a sandbox or disposable directory for test-data generation. <br>
Risk: Imported problem content from URLs, local files, or pasted text can be incomplete or inaccurate. <br>
Mitigation: Verify generated statements, samples, constraints, and test-data coverage against the original problem source before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/ojimport) <br>
- [Test data design reference](references/testdata-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with generated source files, YAML configuration, test data files, and zip archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create work directories, compile and run generated C++ programs, and package outputs as zip files.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
