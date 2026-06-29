## Description: <br>
学习娃 LearnWa generates parent-controlled single-file H5 math teaching aids for early-grade arithmetic, supporting break-ten, make-ten, and level-ten lesson flows with themed visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwter](https://clawhub.ai/user/lwter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, educators, and agents use this skill to turn a natural-language request into a small lesson-block configuration or a generated single-file HTML math lesson. The lessons are designed for a parent to operate while a child observes, answers aloud, and follows step-by-step arithmetic reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python generator that can write an HTML lesson to a selected output path. <br>
Mitigation: Use an explicit --output path and review the destination before running the command. <br>
Risk: Custom theme values can affect the generated lesson's text and visual styling. <br>
Mitigation: Keep custom theme values to normal colors and child-appropriate text before generating lessons. <br>
Risk: Generated math lessons may contain incorrect or unclear arithmetic steps if inputs or customizations are unsuitable. <br>
Mitigation: Review the generated lesson and verify the arithmetic flow before using it with a child. <br>


## Reference(s): <br>
- [Lesson block format](references/lesson-block-format.md) <br>
- [Math rules and step templates](references/math-rules.md) <br>
- [Theme configuration reference](references/themes.md) <br>
- [ClawHub skill page](https://clawhub.ai/lwter/neway-learnwa) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON lesson-block examples, shell commands, and generated single-file HTML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated lesson is a local single-file HTML document with inline CSS and JavaScript.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
