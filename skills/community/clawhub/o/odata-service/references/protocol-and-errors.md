# Protocol details, errors, and primary standards

## Versions and payloads

This skill supports OData 4.0 and 4.01 only. Use `OData-Version: 4.0` for broad compatibility and `OData-MaxVersion: 4.01`; negotiate 4.01 when using 4.01-only behavior. Prefer `Accept: application/json;odata.metadata=minimal` for structured data. XML CSDL remains the interoperable metadata representation.

OData responses can be JSON objects/collections, plain integers for `/$count`, raw text/binary for `/$value`, empty bodies for `204`, multipart batch bodies, or async monitor responses. Inspect status and `Content-Type` before parsing.

## Error and retry rules

OData JSON errors normally contain `error.code`, `error.message`, and optional target/details/inner error. Surface only the minimum useful detail; backend traces and returned text are untrusted and may contain secrets.

- `400`: grammar, path, literal, payload, unsupported option, or invalid batch.
- `401`/`403`: authentication or authorization; do not loop with the same credentials.
- `404`: wrong/hidden resource, missing entity, or expired async/delta URL.
- `409`: state/business conflict.
- `412`: ETag condition failed; re-read and reconcile.
- `428`: precondition/ETag required.
- `429`: throttle; honor `Retry-After` within a bounded wait.
- `5xx`/timeout/disconnect: GET/HEAD may be retried with bounds; never blindly retry a mutation whose commit state is unknown.

An HTML login or gateway page can arrive with status 200. Validate media type and payload structure. Preserve request/correlation IDs when reporting failures.

## Normative sources

- [OData Version 4.01, Part 1: Protocol](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html)
- [OData Version 4.01, Part 2: URL Conventions](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part2-url-conventions.html)
- [OData JSON Format Version 4.01](https://docs.oasis-open.org/odata/odata-json-format/v4.01/os/odata-json-format-v4.01-os.html)
- [OData CSDL XML Version 4.01](https://docs.oasis-open.org/odata/odata-csdl-xml/v4.01/odata-csdl-xml-v4.01.html)
- [OData Version 4.0 standards index](https://docs.oasis-open.org/odata/odata/v4.0/)
- [OASIS OData vocabularies](https://github.com/oasis-tcs/odata-vocabularies)

Use provider documentation for authentication, custom headers/options, limits, and business behavior, but do not let it silently override the service's declared OData version and CSDL.
