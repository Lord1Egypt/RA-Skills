# Version-Adaptive SQL Evidence

Use this reference when SQL is required to identify an OceanBase cluster or tenant, verify lifecycle health, inspect backup/archive state, or prove another data-plane outcome. SQL evidence must match the actual OceanBase version, compatibility mode, account, and exposed catalog.

## Resolve the SQL Surface

Before selecting a query template, record the deployment and endpoint, component artifact/version, tenant and compatibility mode, database account, and intended evidence. Start with the least privileged authenticated connection that can answer the question.

Do not assume that a system variable, view, or column exists because it appeared in another OceanBase release. In particular, do not use `@@cluster_id` or a remembered backup/archive view shape as a universal identity or health query.

Use this order:

1. derive a version candidate from the registered artifact and component identity;
2. confirm the runtime version through a minimal query supported by the connected mode when available;
3. use the installed/released version-matched documentation to identify candidate views;
4. inspect the candidate view's existence and exposed columns through a supported catalog, describe, or show operation;
5. select or construct a read-only query using only the observed columns.

Record the discovered view and column set with the query result. Do not issue a chain of speculative queries whose errors obscure the real health state.

## Interpret Missing or Changed Catalog Objects

A missing variable, view, or column means that query path is unsupported for the observed surface; it does not by itself mean the cluster, tenant, archive, or backup task failed. Select another version-proved evidence path or mark that acceptance layer unavailable. Do not alias an unrelated field merely because its name looks similar.

For backup and archive work, establish the exact task, tenant, and recovery identity before interpreting status columns. Require a version-supported terminal state and corroborate it with OBD task state, manifest/catalog identity, storage evidence, or restored data as the workflow requires.

For cluster or tenant identity, corroborate any SQL identifier with the registered deployment, server topology, endpoint, and intended tenant. A successful connection to the wrong endpoint is not acceptance.

## Preserve Safety and Evidence

Keep credentials and business data out of query text, transcripts, and reports. Record the redacted query shape, endpoint identity, observed schema surface, result classification, and timestamp. A SQL syntax or catalog-compatibility error is evidence about the query path; report product health separately.

## Keep Resolved Credentials on the Controller

Some installed OBD builds expose a usable connection string or decrypted password through `cluster display`. Do not stream that complete output back to the automation runner merely to construct a second SSH command, and do not interpolate the resolved password into a local or remote process argument.

When authenticated SQL evidence requires a credential known only to the controller, run one permission-controlled wrapper on that controller and keep the credential lifecycle inside that process:

1. prefer an installed OBD or SQL-client input mechanism that accepts protected input without placing the secret in process arguments;
2. otherwise, capture the minimum required OBD output inside the wrapper, extract the credential without echoing it, and immediately pass it through a version-proved protected client mechanism;
3. if the installed client proves support for an option/defaults file, create it under a unique mode-`0700` task directory with mode `0600`, use it for the single bounded query, and remove only that task-owned file after recording the non-secret result;
4. if no protected client mechanism is available, stop and report the credential-input limitation instead of falling back to `-p<password>`, a reusable command, shell history, or runner-visible output.

Return only the redacted query shape, endpoint identity, result, timestamp, and other non-secret evidence. Treat any controller trace or protected capture that contains the credential as sensitive evidence and retain or remove it only under the normal evidence and cleanup boundary.
