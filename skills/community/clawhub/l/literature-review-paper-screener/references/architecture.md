# Architecture reference — Local vs Cloud

## Responsibilities

| | Local Agent (this Skill, free) | Cloud (private LoomLoom template, paid) |
|---|---|---|
| Internet | Yes — unrestricted | No internet |
| Role | Evidence Gathering | Evidence Evaluation + Reasoning + Organization |
| Does | search, database access, metadata/abstract/content/full-text collection, verification, dedup, package building, level assignment (STEP 7.5) | validate evidence availability (STEP 0A), topic relevance, quality filters (source validity, basic credibility, level-aware content credibility), recency, priority, reading role, Paper Sheet + Reading List data |
| Input/Output | produces the handoff dataset | operates only on that dataset |

## Mandatory data transfer rule

> Before any cloud processing begins, the local agent must complete all required searching and
> collect all information needed by the cloud. The cloud operates only on data already provided.

## What the Cloud must never do (and you must never ask it to)

- Search the internet
- Fetch additional papers
- Open URLs to retrieve missing information
- Depend on external databases
- Assume missing information can be retrieved later
- Claim to have reviewed content not included in the package
- Infer methodology/findings/quality from metadata alone (Level D)

## Core rule

> **Evidence Availability ≠ Quality.** Limited access to a paper does not mean the paper is low
> quality. The level (A/B/C/D) only determines how confidently and deeply the system can assess it.
> The level never changes Topic Relevance, Priority, Reading Role, or pool membership.
