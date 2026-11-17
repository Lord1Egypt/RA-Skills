## Description:

Local text-to-speech via sherpa-onnx (offline, no cloud)

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate speech audio from text locally with sherpa-onnx and a selected voice model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation changes OpenClaw environment configuration and downloads a runtime and voice model.

Mitigation: Review the proposed configuration paths and download sources, and confirm the changes fit your intended setup before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hillstreet-ph/skills/oc-sherpa-onnx-tts)
- [sherpa-onnx runtime archive (macOS)](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.6/sherpa-onnx-v1.13.6-osx-universal2-shared.tar.bz2)
- [sherpa-onnx runtime archive (Linux x64)](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.6/sherpa-onnx-v1.13.6-linux-x64-shared.tar.bz2)
- [sherpa-onnx runtime archive (Windows x64)](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.6/sherpa-onnx-v1.13.6-win-x64-shared-MD-Release.tar.bz2)
- [Piper en_US lessac voice model archive](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2)

## Skill Output:

**Output Type(s):** [Audio files]

**Output Format:** [WAV audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech generated locally from supplied text using the configured voice model.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
