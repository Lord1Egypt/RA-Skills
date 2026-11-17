# IAM Policies — huawei-cloud-daily-hot-topics

## Required Huawei Cloud permissions

**None.**

This skill does not call the Huawei Cloud CLI (KooCLI), any Huawei Cloud SDK, or
any Huawei Cloud REST API, so no IAM policy, agency, or permission is required.
It never creates, reads, modifies, or deletes any Huawei Cloud resource.

## Credentials

No AK/SK, token, or project/region credential is needed. The skill calls only
public, authentication-free hot-list endpoints over HTTPS.

## Network access

The only outbound traffic is read-only HTTPS GET requests to the public hot-list
providers configured in `scripts/fetch_hot_topics.py`. If the environment has no
outbound access, the skill degrades to its bundled sample dataset and still runs
without any credential.

## Data handling

Fetched content is held in memory only for the duration of the run and is
displayed on standard output (or written to a user-chosen `--output` file). It is
not persisted to any cloud service and is not re-published by the skill.