## Description:

Turn a source image or multi-color mask image into a 3D-printable bas-relief STL by mapping colors or grayscale values to heights through a deterministic pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajmwagar](https://clawhub.ai/user/ajmwagar)

### License/Terms of Use:


## Use Case:

Developers, makers, and external users can use this skill to convert flat-color, palette-based, or grayscale images into printable bas-relief STL models. It is suited for deterministic image-to-geometry workflows where the agent should provide conversion commands and produce model files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional preview path has a code-execution issue when filenames or paths may be attacker-controlled.

Mitigation: Use the skill in a constrained environment, avoid --preview-svg for untrusted paths, and prefer a fixed version with the preview issue patched.

Risk: The wrapper may install unpinned Python packages into a cache virtual environment on first use.

Mitigation: Pre-provision, pin, or vendor dependencies before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajmwagar/skills/image-to-relief-stl)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [ASCII STL file and optional SVG preview, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, potrace, and mkbitmap; first use may create a cached Python virtual environment.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
