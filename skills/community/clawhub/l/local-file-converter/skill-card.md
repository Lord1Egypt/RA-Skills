## Description: <br>
Local File Converter helps convert local files across image, video, audio, document, ebook, and data formats using command-line tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiantian-pago](https://clawhub.ai/user/tiantian-pago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users with local conversion tools installed use this skill to choose a converter for a source file and target format, run the conversion, and return the output file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion commands operate on local files and can be high impact when run against important or untrusted inputs. <br>
Mitigation: Review the selected command, input path, output path, and target format before execution, and keep conversions in a controlled output directory. <br>
Risk: Large files and video conversions can consume substantial CPU, storage, and time. <br>
Mitigation: Run large conversions when adequate local resources are available and confirm output location before starting. <br>
Risk: Lossy conversions or unsupported format combinations can reduce quality or fail. <br>
Mitigation: Keep the original file, confirm required tools and codecs are installed, and inspect converted output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tiantian-pago/local-file-converter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted local files when the required command-line tools are installed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
