## Description:

Generate professional prior authorization request letters for insurance companies with proper clinical justification and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare administrative staff, clinicians, and agent workflows can use this skill to draft structured prior authorization request letters from patient, provider, service, diagnosis, and clinical justification inputs. Users should review the generated letter for medical accuracy, payer requirements, and privacy compliance before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may handle medical and insurance data, including protected health information.

Mitigation: Use only in an approved healthcare-compliant environment and avoid entering real PHI unless privacy, access control, retention, and review requirements are satisfied.

Risk: The packaged script writes letter output to local paths and defaults to prior_auth_letter.txt.

Mitigation: Restrict input and output paths to a private workspace, choose explicit output filenames, and check for existing files before execution.

Risk: Evidence.security flags unsafe install instructions and unnecessary requirements.

Mitigation: Remove unnecessary requirements or explicitly accept them during review before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/prior-auth-letter-drafter)
- [Carrier requirements](artifact/references/carrier_requirements.json)
- [Clinical justification phrases](artifact/references/clinical_phrases.md)
- [Clinical guidelines references](artifact/references/guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain-text prior authorization letter with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The packaged script reads JSON input and writes a letter file, defaulting to prior_auth_letter.txt when no output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
