# PHI Readiness Stages (PRS)

Framework version: `PRS Framework v1.1`

Document role: public overview

Canonical citation: `PHI Readiness Stages (PRS) Framework v1.1`.

## Purpose

PRS exists to describe the lifecycle status of a workload that may handle protected health information without collapsing all status into the phrase `HIPAA compliant`.

PRS separates four dimensions that are often confused:

- technical safeguards
- organizational and process readiness
- formal internal approval for PHI use
- live operational maintenance

## What PRS is not

PRS is not:

- a legal opinion
- a certification
- a regulator-recognized attestation
- a substitute for counsel, formal review, or ongoing evaluation
- a company-wide label

## Scope model

PRS applies per:

- workload
- product boundary
- environment
- deployment boundary

The same company may have different workloads at different stages.

## Canonical stage set

| Stage | Public meaning | Frozen public label |
| --- | --- | --- |
| PRS-0 | Non-PHI only within the defined scope | PRS-0 Non-PHI - out of PHI scope |
| PRS-1 | Built with PHI-oriented security patterns, but not approved for PHI | PRS-1 Security-Aligned - not approved for PHI |
| PRS-2 | Technically and operationally prepared, but pending formal approval | PRS-2 PHI-Ready - pending internal approval |
| PRS-3 | Explicitly approved for PHI use in defined scope, but not yet live | PRS-3 PHI-Approved - internally approved for PHI use in defined scope |
| PRS-4 | Live with PHI in approved scope under ongoing controls | PRS-4 PHI-Operational - operating with PHI under ongoing controls |

## Core rule

A workload may be assigned `PRS-n` only if it satisfies the minimum criteria for every required domain for `PRS-n`. If any required domain is incomplete, the workload remains at the highest lower stage whose required domains are fully satisfied.

## Publication rule

Use PRS codes and frozen public labels in public or customer-facing status descriptions. Reserve internal gates, exceptions, residual-risk notes, and overdue-evidence notes for internal governance workflows.

## Normative details

Use `framework/spec.md` as the normative specification for:

- detailed stage definitions and entry criteria
- internal gate model
- downgrade rules
- evidence and approval constraints
