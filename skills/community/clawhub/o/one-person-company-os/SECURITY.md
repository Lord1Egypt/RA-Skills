# Security Policy

## Scope

This repository contains a skill package, templates, references, helper scripts, and release assets.

It does not ship production infrastructure, but it can influence business decisions and generated customer-facing materials. Treat generated outputs as drafts that require human review.

## Marketplace Safety Boundary

- normal use does not require API keys or unrelated service credentials
- the marketplace build must not auto-install system packages
- script mode expects an existing local Python runtime that the user already trusts
- persisted writes should stay inside the founder-approved workspace directory
- if you cannot inspect local scripts, run them only inside an isolated folder, container, or VM

## Responsible Use

- review generated pricing, legal, compliance, and customer-facing language before publishing or sending
- require explicit founder approval before production deployment, destructive data changes, or budget spend
- avoid storing sensitive secrets directly in generated company workspaces

## Reporting

If you discover a security issue in the repository contents or scripts, report it privately to the maintainer before public disclosure.
