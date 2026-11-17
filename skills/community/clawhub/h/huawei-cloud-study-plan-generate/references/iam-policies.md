# IAM Policies

This skill does not access any Huawei Cloud service. It is a pure local Python generator
that reads a built-in topic pool and writes a study plan to standard output or a local
file.

- No Huawei Cloud API / SDK / KooCLI calls are made.
- No IAM user, agency, or policy is required.
- No cloud resource is read, created, modified, or deleted.

Therefore no IAM policy document is needed. If this skill is ever extended to read a
cloud-hosted topic pool, replace this file with a least-privilege policy that grants only
the required read action.