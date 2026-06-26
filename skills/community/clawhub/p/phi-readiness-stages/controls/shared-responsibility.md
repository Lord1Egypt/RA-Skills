# Shared Responsibility and Inherited Controls

Last reviewed: March 17, 2026.

Use this reference when the workload runs on cloud infrastructure, depends on SaaS, is partly customer-hosted, or inherits controls from another team or provider.

## Core rule

Inherited controls count only when the inheritance path is explicit and the workload owner's retained responsibilities are documented.

## Review questions

- Which controls are directly operated by the workload team?
- Which controls are inherited from cloud, platform, SaaS, or a central security team?
- Which responsibilities remain with the workload owner even when infrastructure is inherited?
- Does the provider's service boundary create a business-associate or subcontractor role?
- Are logging, backups, key management, support access, and incident handling split clearly across parties?

## Common deployment patterns

### Workload on public cloud

Do not let `runs on AWS`, `runs on GCP`, or `runs on Azure` stand in for workload readiness.

You still need evidence for:

- workload-level access control
- logging configuration
- key and secret handling
- vendor-role analysis
- restore confidence
- operational ownership

### SaaS dependency in the PHI path

For SaaS tools that touch PHI, review:

- PHI flow into the service
- support access and telemetry
- subprocessor chain
- BAA need
- exit and deletion expectations

### Customer-hosted deployment

When customers host the product:

- split PRS assessment between vendor responsibilities and customer responsibilities
- do not assume vendor is outside scope if vendor support, telemetry, or remote management can touch PHI
- avoid one single PRS stage if materially different deployment models exist

### Central platform inheritance

If controls are inherited from an internal platform or security team:

- identify the inherited service
- name the retained responsibilities of the workload team
- obtain evidence that the inherited control is actually enabled for the workload

## Strong evidence

- shared-responsibility matrix
- provider security boundary documentation
- service configuration proving the inherited control is enabled
- vendor review record
- role and contract analysis

## Common blockers

- provider-level certification used as a substitute for workload evidence
- inherited controls assumed but not enabled for the workload
- unclear ownership between platform and application teams
- unsupported belief that encrypted data eliminates BA analysis

## Recommended next actions

- create a workload-specific shared-responsibility matrix
- document inherited and retained controls by domain
- verify vendor and contract status for every in-scope service in the PHI path
