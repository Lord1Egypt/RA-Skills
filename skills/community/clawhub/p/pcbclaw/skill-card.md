## Description:

PCBClaw helps agents design and verify editable KiCad boards, generate JLCPCB manufacturing bundles, and compare Economic PCBA assembly pricing with supplier review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liseman](https://clawhub.ai/user/liseman)

### License/Terms of Use:

MIT

## Use Case:

Developers and hardware engineers use PCBClaw to turn conversational PCB requirements into editable KiCad projects, verification reports, manufacturing candidate packages, and JLCPCB Economic PCBA cost comparisons. The workflow supports new designs, modifications, resume/reprice flows, and packaging for supplier review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and modify local PCB project files, run KiCad and shell diagnostics, and generate manufacturing packages.

Mitigation: Review the skill before installation, run it in an intended project workspace, and rely on its checkpointing, backup, ERC/DRC, and package verification steps before using generated files.

Risk: Supplier uploads, GitHub publication, orders, payments, and account actions could expose private project data or create external commitments.

Mitigation: Keep those actions behind explicit approval and review any files, carts, publications, or account operations before proceeding.

Risk: Generated CAD files, clean helper tests, or supplier-ready packages do not prove electrical function, production certification, or physical fit.

Mitigation: Perform independent engineering review, prototype bring-up, and project-specific supplier approval before manufacturing or production use.

Risk: Assembly eligibility, component stock, and pricing can change and may be unknown without authorized supplier access.

Mitigation: Verify current manufacturer data, JLCPCB Economic PCBA eligibility, stock, and quote or estimate sources at delivery time, and mark unknown costs or blocked rows instead of treating them as zero.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liseman/skills/pcbclaw)
- [PCBClaw README](artifact/README.md)
- [Design and verification detail](artifact/references/design.md)
- [Environment and defaults](artifact/references/environment.md)
- [Economic PCBA cost policy](artifact/references/costs.md)
- [Release packaging](artifact/references/release.md)
- [Supplier and cart review](artifact/references/supplier.md)
- [Installation and update validation](artifact/references/validation.md)
- [Release notes](artifact/RELEASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with local project files, KiCad command usage, CSV/Markdown reports, manufacturing bundles, and configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include editable KiCad projects, Gerbers, drills, BOM/CPL files, PDFs, verification reports, cost comparisons, source archives, and release bundles. Supplier uploads, GitHub publication, orders, payments, and account actions require explicit approval.]

## Skill Version(s):

0.2.0-beta.1 (source: evidence release metadata, README, and RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
