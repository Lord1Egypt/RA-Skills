---
name: judgment-event-protocol
description: Verify JEP Core 0.7 signed event records and guide local creation or independent implementation testing.
homepage: https://github.com/hjs-spec/jep-core
---

# Judgment Event Protocol

Use for JEP record verification, local event creation guidance and implementation
interoperability. Core 0.7 uses wire major `jep: "1"`. Software versions are
separate from the protocol version. JEP is an individual Internet-Draft.

## Verify a sample

Use Python 3.10 or later in a fresh environment:

```sh
python -m pip install jep-core-conformance==0.7.8
jep-byoi export jep-example
jep-validate validate jep-example/vectors/J-basic.json --keys jep-example/keys.json
jep-byoi demo --report byoi-reference-report.json
```

Use a new export directory. The sample should report `status: "valid"` and
`checks.cryptographic: "pass"`. The demo reports 29 selected producer/verifier
checks using a disclosed reference wrapper. Public synthetic fixture keys do
not establish trust in a real actor. Inspect the full result and selected checks.
Missing keys can yield `indeterminate`; do not treat this as a successful check.

## Create your own record

Follow the maintained, executable local creation/export example:
https://github.com/hjs-spec/jep-agent-sdk#local-create--export--independent-verification

Use the documented SDK API and a protected signing key. Do not substitute the
obsolete `jep-protocol` package or invent imports. Ask for the intended actor,
statement and applicable trust/profile rules before creating user records.
Never expose signing keys or infer permission to carry out an external action.

## Interpret records

- J: judgment statement.
- D: delegation statement with `what.delegatee` and `what.scope`.
- T: termination statement with `ref` and `what.termination_scope`.
- V: verification statement with `ref`, `what.verification_scope` and `what.result`.

Required event fields include `jep`, `id`, `verb`, `who`, `when`, `what` and `sig`.
`who` declares the actor, and `when` is actor-declared event time. Core 0.7 does
not require a nonce. The selected profile can add freshness/audience requirements.

Event Identity `(who,id)` remains stable across retries. Event Hash identifies
one exact signed artifact including `sig`. The signing payload is JCS of the
unsigned event with `sig` omitted; construct the signature input according to
the declared signature class. Do not sign the full signed-artifact hash.

A valid signature does not establish substantive truth, authorization, real-world
identity, lifecycle enforcement or an executed business effect. Apply explicit
trust and acceptance rules before acting. Acceptance is idempotent per Event
Identity within an acceptance domain; archival verification does not consume it.

## Test an implementation

Use https://github.com/hjs-spec/jep-core/blob/main/docs/BYOI-CONFORMANCE.md.
Disclose reused components, exact revision, selected roles and uncovered checks.
The optional `--state-setup` hook prepares disposable test state; it is not a
Core event operation. Do not run unreviewed adapters or production effects.

Normative source map:
https://github.com/hjs-spec/jep-core/blob/main/docs/SPECIFICATION-SOURCES.md
