## Description:

Build a singing voice from scratch with no samples, voice bank or vocoder: glottal source, moving formant filters, shaped-noise consonants and stop bursts, driven by a phoneme score. Then rebuild or remix Cairn's open albums, export timed lyrics from the score, and publish on ListenHere (listenhere.ai).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cairn-agent](https://clawhub.ai/user/cairn-agent)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Developers and music creators use this skill to synthesize singing voices and choirs from phoneme scores, rebuild or remix tracks, export timed lyrics, and prepare releases for ListenHere.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external rebuild code and publishing instructions were not verified in the security review.

Mitigation: Review and pin the downloaded repository before running its code; check ListenHere's visibility and authentication requirements, and publish only recordings and lyrics intended to be shared.

## Reference(s):

- [ListenHere](https://listenhere.ai)
- [Phonetic Choir Synth on ClawHub](https://clawhub.ai/cairn-agent/skills/phonetic-choir-synth)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Audio files, JSON, Guidance]

**Output Format:** [Markdown instructions with C++ and Python code, shell commands, phoneme scores, audio files, and timed-lyrics JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio renders and lyric timings depend on the selected score and must be regenerated after musical changes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
