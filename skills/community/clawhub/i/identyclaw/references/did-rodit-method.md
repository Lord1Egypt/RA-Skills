# The `did:rodit` Method

**Status:** Draft for registration in the [W3C DID Method Registry](https://www.w3.org/TR/did-extensions-methods/). HTTP convenience resolvers on IdentyClaw APIs remain labeled experimental in OpenAPI.  
**Canonical URL:** `https://api.identyclaw.com/.well-known/did-method-rodit`  
**Normative references:** [W3C DID Core 1.1](https://www.w3.org/TR/did-1.1/), [DID Resolution](https://www.w3.org/TR/did-resolution/), [did:web Method Specification](https://w3c-ccg.github.io/did-method-web/), [RFC 5234](https://www.rfc-editor.org/rfc/rfc5234), [RFC 3552](https://www.rfc-editor.org/rfc/rfc3552), [RFC 6973](https://www.rfc-editor.org/rfc/rfc6973)

This document is the DID method specification for **`did:rodit`**. It identifies Rich Online Digital Identity Tokens (RODiT / IdentyClaw Passports): transferable, universally unique agent identities recorded as non-fungible tokens on a NEAR Protocol smart contract.

A `did:rodit` identifier is the portable Passport DID. It does not encode an API hostname or a contract account. Resolvers pin a verifiable data registry (NEAR mainnet + a trusted RODiT contract) and construct the DID document from current on-chain state.

---

## 1. Method name

| Property | Value |
|----------|--------|
| **Method name** | `rodit` |
| **DID scheme** | `did:rodit:<passport-id>` |
| **Verifiable data registry** | NEAR Protocol (mainnet) RODiT contract |

The method name uses only lowercase ASCII letters (`r`, `o`, `d`, `i`, `t`) and matches the DID Core `method-name` production (`1*method-char` where `method-char = %x61-7A / DIGIT`).

This specification defines **exactly one** method-specific DID scheme, identified by the method name `rodit`.

**Do not use** NEAR contract account IDs (for example `rodit.near` or `genaaaa-identyclaw-com.near`) in the DID string. Contract deployment is resolver configuration and on-chain metadata (`serviceprovider_id`), not part of the identifier.

---

## 2. Method-specific identifier

### 2.1 ABNF (normative)

The following ABNF uses [RFC 5234](https://www.rfc-editor.org/rfc/rfc5234). It is a restriction of DID Core `method-specific-id`:

```
rodit-did           = "did:" rodit-method-name ":" rodit-specific-id
rodit-method-name   = "rodit"
rodit-specific-id   = 12( lowercase-alpha )
lowercase-alpha     = %x61-7A
```

Examples: `did:rodit:bkbvehbdcrgm`, `did:rodit:lhsrldbjsnlh`.

This method does **not** use colons inside `method-specific-id`. DID path, query, and fragment components follow DID Core / RFC 3986; this method does not define a more restrictive path or query syntax. The fragment `controller` is reserved for the primary verification method (see §5).

### 2.2 Generation

The method-specific identifier **is** the Passport `token_id` assigned when the RODiT is minted on the pinned contract.

1. At Create (§4.1), the minter supplies (or the issuance flow assigns) a 12-character `token_id`.
2. Characters 1–11 encode categorical facial-trait selections used as a human-recognisable agent face. Character 12 is a checksum over those selections. Encoding tables live in the Passport metadata reference; they are **not** required to parse or resolve a DID.
3. The contract rejects a mint if that `token_id` already exists on that contract.
4. The DID is then `did:rodit:` concatenated with that `token_id`. The DID document is **not** stored as a separate object; it is derived at Read time from the token record and the current owner’s NEAR keys.

Any 12-letter string that exists as `token_id` on the pinned contract is a valid method-specific identifier. Strings that do not match §2.1 are invalid DIDs (`INVALID_DID`). Strings that match §2.1 but have no token record are valid DIDs that do not (currently) resolve (`DID_NOT_FOUND`).

### 2.3 Sensitivity, normalization, and uniqueness

| Rule | Requirement |
|------|-------------|
| **Length** | Exactly 12 characters |
| **Charset** | Lowercase ASCII letters `a`–`z` only |
| **Case** | Identifiers are **case-sensitive** as written in the DID string. Resolvers MUST reject uppercase letters as invalid syntax. Passport IDs are stored and compared in lowercase on chain. |
| **Normalization** | No Unicode normalization. Implementations MAY trim surrounding whitespace on input, then MUST apply the ABNF. |
| **Uniqueness** | `token_id` is unique **within the pinned RODiT contract**. Minting rejects duplicates. The identifier is designed to be globally unique for a given trusted contract; it does not encode a local namespace, tenant, or API host. |
| **Global uniqueness of DIDs** | `did:rodit:<passport-id>` is globally unique as a URI. Two resolvers that pin **different** contracts could theoretically see the same 12-letter id refer to different tokens (an operational failure, not an expected namespace). Resolvers MUST pin the contract they trust. |

---

## 3. Verifiable data registry

`did:rodit` is anchored on **NEAR Protocol mainnet**. The DID document is derived from a RODiT smart-contract account that stores Passport NFTs.

### 3.1 Canonical production registry

| Setting | Canonical production value |
|---------|----------------------------|
| **Network** | NEAR mainnet |
| **Contract account** | `genaaaa-identyclaw-com.near` |
| **View (Read)** | `rodit_token` |
| **Create** | `rodit_mint` |
| **Update (controller)** | `rodit_transfer` |
| **Destroy** | `rodit_burn` |
| **List (optional)** | `rodit_tokens` |

Independent resolvers MUST pin a contract account. For public IdentyClaw Passports, pin `genaaaa-identyclaw-com.near` unless an operator has published a different trusted registry.

Development IdentyClaw stacks may pin a different mainnet account (pattern `YYYYYvN-identyclaw-com.near`). The DID string does not encode which contract is used.

### 3.2 IdentyClaw HTTP resolver configuration

IdentyClaw API instances read:

| Setting | Source | Purpose |
|---------|--------|---------|
| **`NEAR_CONTRACT_ID`** | Host config or env | RODiT contract account to pin |
| **`NEAR_RPC_URL`** | Host config or env | NEAR RPC endpoint for on-chain reads |

That HTTP resolver is a **convenience** implementation of Read. It is not the verifiable data registry.

---

## 4. Method operations

Authorization for all mutating operations is performed **on chain** by the RODiT contract using the NEAR predecessor account and, for mint, a fee attestation from the contract’s authorized-signer set. The DID document is not consulted to authorize Create, Update, or Destroy. Read is unauthenticated against the ledger.

### 4.1 Create

A DID controller creates a `did:rodit` DID by minting a Passport NFT whose `token_id` becomes the method-specific identifier.

**Authorization.** The mint transaction must (1) be signed by a NEAR account that will own the token, (2) include a fee attestation accepted by the contract’s authorized-signer set, and (3) attach the attested deposit. The contract MUST reject a `token_id` that already exists.

**Procedure (normative outcome).**

1. Create or reuse a NEAR account whose full-access key is Ed25519. Implicit accounts (64-character lowercase hex of the public key) are typical.
2. Obtain issuance (purchase / sign-portal attestation) so the contract will accept `rodit_mint`.
3. Submit `rodit_mint` on the pinned contract with the chosen `token_id`, owner account, and Passport metadata (validity window, DN, policy fields).
4. On success the contract stores `{ token_id, owner_id, metadata }` and emits a mint event.
5. The DID `did:rodit:<token_id>` now exists. The associated DID document is the document that Read would return for that DID at that block.

The DID document is **generative**: it is not written to the ledger as JSON-LD. Create succeeds when the token record exists.

IdentyClaw’s hosted issuance UI is `https://purchase.identyclaw.com`. Other issuers MAY call `rodit_mint` if they can satisfy the contract’s attestation and deposit rules.

### 4.2 Read (Resolve)

A DID resolver uses the DID to construct a DID document from current chain state.

**Inputs.** A `did:rodit` DID; a pinned contract account; a NEAR RPC endpoint; optional resolution options (this method does not define custom DID parameters).

**Algorithm (normative).**

1. Confirm the DID matches §2.1. Otherwise fail with `invalidDid`.
2. Let `passport-id` be the `rodit-specific-id`.
3. Call the pinned contract view method `rodit_token` with JSON arguments `{ "token_id": "<passport-id>" }` at finality `final` (or the caller’s chosen NEAR finality).
4. If the result is missing or has no `token_id`, fail with `notFound`.
5. Let `owner_id` be the token’s `owner_id`.
6. Fetch an Ed25519 full-access public key for `owner_id` from NEAR (account access-key query). If none is available, fail resolution (the DID exists but the verification method cannot be built).
7. Encode that 32-byte public key as Base58 (Bitcoin alphabet) for `publicKeyBase58`.
8. Return the DID document in §5.1. `id` MUST be `did:rodit:<passport-id>`.

**Authenticity of the response.** The DID document is not a separately signed object. Verifiers authenticate Read by (a) pinning the contract account, (b) using a NEAR RPC they trust (or multiple RPCs), and (c) relying on NEAR consensus / the chosen finality. A MITM on an untrusted RPC can lie about token state. Independent resolvers SHOULD prefer well-known public RPCs or their own node.

**IdentyClaw HTTP convenience resolver** (non-normative for the method; documents current API behavior):

Let `{base}` be an IdentyClaw API origin (for example `https://api.identyclaw.com`).

| Operation | HTTP | URL | Auth |
|-----------|------|-----|------|
| Resolve by passport id | `GET` | `{base}/.well-known/did/rodit/{passport-id}` | JWT Bearer |
| Resolve by DID string | `GET` | `{base}/.well-known/did/resolve?did={url-encoded-did}` | JWT Bearer |
| Resolve as `did:web` alias | `GET` | `{base}/.well-known/did/web/token/{passport-id}` | JWT Bearer |
| Same, `did.json` suffix | `GET` | `{base}/.well-known/did/web/token/{passport-id}/did.json` | JWT Bearer |
| MCP resource | MCP `get_resource` | `did:resolve:{passport-id}` | MCP (public docs transport) |

Unauthenticated callers of those HTTP paths receive an authentication error. **JWT on the HTTP resolver does not replace pinning the contract.** Peers MAY implement Read solely via NEAR RPC and skip the HTTP API.

MCP:

| MCP resource URI | Description |
|------------------|-------------|
| `did:resolve:{passport-id}` | DID document JSON (12-letter id) |
| `doc:reference:did-rodit-method` | This specification (Markdown, JSON wrapper) |

### 4.3 Update

An **update** to a `did:rodit` DID document is a change to the current controller key material: the on-chain `owner_id` and therefore the `verificationMethod` public key constructed at Read.

**How the controller updates.** The current token owner calls `rodit_transfer` on the pinned contract:

```
rodit_transfer(receiver_id: AccountId, token_id: String, memo: Option<String>)
```

**Authorization.** The NEAR predecessor MUST be the current `owner_id`. The attached deposit MUST be exactly 0.01 NEAR. `receiver_id` MUST differ from the sender. On success the contract updates `owner_id` and emits a `rodit_transfer` event.

The 12-letter DID does **not** change. Subsequent Read uses the new owner’s keys. Transfer is also the key-rotation mechanism; observers cannot distinguish rotation from change of custody.

**What cannot be updated.** Passport metadata (validity window, DN, policy fields, `token_id`) is **immutable** after mint. There is no `update_metadata` method. Extending `not_after` requires minting a **new** Passport (a new DID).

### 4.4 Deactivate

**Holder-driven deactivation is not possible.** The DID controller (current token owner) cannot burn or tombstone the identifier through a public controller operation.

**Privileged destroy.** The contract implements `rodit_burn`. That method is authorized by the contract’s own access-control (registry owner / predecessor rules), not by DID document `authentication`. After a successful burn, `rodit_token` no longer returns the record and Read MUST fail with `notFound`.

**Expiry is not deactivation.** Metadata `not_after` (unless the unbounded sentinel `1970-01-01`) is a validity window for **authentication and API use**. An expired token MAY still resolve to a DID document. Verifiers that use Passports as credentials MUST treat an expired `not_after` as inactive for proofs (HOLA, login) even if Read succeeds. `not_before` / `not_after` are not rewritten in place.

There is no holder revocation list and no graduated DID document `deactivated` flag in the current contract. Effective invalidation for relying parties is: burn (token gone), expiry (token present but inactive for proofs), or local policy.

---

## 5. DID document

### 5.1 `did:rodit` primary form

| Field | Value |
|--------|--------|
| `id` | `did:rodit:<passport-id>` |
| `alsoKnownAs` | `did:web:<host>:token:<passport-id>` when an HTTP host is known (`:` in host percent-encoded as `%3A`) |
| `controller` | NEAR account id of the current token owner (a NEAR account string, **not** a DID). This is method-specific. |
| `verificationMethod[]` | One entry: `id` = `{did}#controller`, `type` = `Ed25519VerificationKey2020`, `controller` = `{did}`, `publicKeyBase58` = owner Ed25519 key |
| `authentication` / `assertionMethod` | `[ "{did}#controller" ]` |
| `service[]` | `RoditTokenMetadata` (embedded Passport metadata) and `MCPDiscoveryService` (HTTP resolver’s `/api/mcp/resources` when a base URL is known) |

`@context` includes `https://www.w3.org/ns/did/v1` and the IdentyClaw RODiT vocabulary (`https://identyclaw.com/ns/rodit#`).

The fragment `controller` on the verification method is the only fragment this method defines. Other fragments MAY appear as `service` ids (`#metadata`, `#mcp-discovery`).

### 5.2 Example (illustrative)

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    {
      "rodit": "https://identyclaw.com/ns/rodit#",
      "RoditTokenMetadata": "https://identyclaw.com/ns/services#RoditTokenMetadata",
      "MCPDiscoveryService": "https://identyclaw.com/ns/services#MCPDiscoveryService"
    }
  ],
  "id": "did:rodit:bkbvehbdcrgm",
  "alsoKnownAs": [
    "did:web:api.identyclaw.com:token:bkbvehbdcrgm"
  ],
  "controller": "abc123def4567890123456789012345678901234567890123456789012345678",
  "verificationMethod": [
    {
      "id": "did:rodit:bkbvehbdcrgm#controller",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:rodit:bkbvehbdcrgm",
      "publicKeyBase58": "..."
    }
  ],
  "authentication": ["did:rodit:bkbvehbdcrgm#controller"],
  "assertionMethod": ["did:rodit:bkbvehbdcrgm#controller"],
  "service": [
    {
      "id": "did:rodit:bkbvehbdcrgm#metadata",
      "type": "RoditTokenMetadata",
      "serviceEndpoint": { "type": "RODiTMetadataDocument", "tokenId": "bkbvehbdcrgm", "metadata": {} }
    },
    {
      "id": "did:rodit:bkbvehbdcrgm#mcp-discovery",
      "type": "MCPDiscoveryService",
      "serviceEndpoint": "https://api.identyclaw.com/api/mcp/resources"
    }
  ]
}
```

`RoditTokenMetadata.serviceEndpoint` MAY embed on-chain metadata (DN, webhook URL, validity window, contract account). Treat embedded metadata as **public ledger data**, not a confidential claims channel.

---

## 6. Relationship to `did:web`

| Aspect | `did:rodit` | `did:web` (alias) |
|--------|-------------|-------------------|
| **Purpose** | Stable, host-agnostic Passport identifier | HTTPS-oriented identifier tied to a serving API host |
| **Form** | `did:rodit:<passport-id>` | `did:web:<host>:token:<passport-id>` |
| **Primary in IdentyClaw HTTP** | Default for `/.well-known/did/rodit/...` | Primary when resolving via `/.well-known/did/web/token/...` |
| **Document** | Same logical document; `id` and `alsoKnownAs` swap roles | Same |
| **Generic did:web resolvers** | N/A | May work only if the host exposes unauthenticated well-known DID URLs; IdentyClaw HTTP currently requires JWT on those paths |

Integrators SHOULD treat **`did:rodit`** as the portable Passport DID and **`did:web`** as a deployment-scoped alias for the same passport on a given API hostname.

---

## 7. Supported DID methods on IdentyClaw HTTP resolvers

| Method | Supported | Notes |
|--------|-----------|--------|
| `rodit` | Yes | This specification |
| `web` | Yes | Path must include `:token:<passport-id>` after host segments |
| `wba`, others | No | Rejected with `INVALID_DID` |

Legacy documentation that referred to `did:wba:rodit.near:…` is withdrawn. On-chain JSON-LD views MAY still expose `did_wba_jsonld`; HTTP DID resolution uses `did:rodit` / `did:web` only.

---

## 8. Stability

- This specification is the registration document for method name `rodit`. Breaking changes to syntax or CRUD semantics require an update to this document and to any W3C registry entry that points here.
- OpenAPI `/.well-known/did/*` **resolution** operations on IdentyClaw HTTP APIs are labeled **EXPERIMENTAL** and may change when `api-docs/swagger.json` `info.version` bumps. That label applies to the paid HTTP convenience API, not to the on-chain identifier syntax.
- The method has no separate on-chain version field. Passport JSON-LD `version` on the contract is independent (fetch via MCP `jsonld:contract-metadata`).

---

## 9. Security considerations

This section follows [RFC 3552](https://www.rfc-editor.org/rfc/rfc3552) for the operations in §4. `did:rodit` inherits NEAR’s consensus and account-key model. Residual risk remains whenever a resolver uses a third-party RPC or an unpinned contract.

### 9.1 Unique assignment

DIDs are uniquely assigned by contract-enforced uniqueness of `token_id` on the pinned registry. Duplicate mint of the same 12-letter id on that contract fails. Uniqueness across **unrelated** contracts is not a ledger invariant; trust is the resolver’s pin (see §2.3). Economic mint cost raises the price of mass-producing look-alike Passports but does not bind display names.

### 9.2 Integrity protection and update authentication

Create, Update, and Destroy are NEAR transactions: Ed25519 signatures over NEAR transaction payloads, replay-protected by NEAR nonces, and ordered by chain consensus. Read is a view call; integrity is the RPC’s response authenticity plus consensus at the requested finality. The constructed DID document is **not** an additional signed envelope. Implementations MUST NOT treat HTTP JSON from an IdentyClaw API as stronger than the chain view unless they also authenticate that API.

Key material that MUST remain secret: NEAR account private keys used as `authentication` / `assertionMethod`, issuance/attestation keys, and JWT session secrets for the convenience API. Public keys, `token_id`, `owner_id`, and Passport metadata are public ledger data.

### 9.3 Attacks (RFC 3552)

| Attack | Method-specific consideration |
|--------|-------------------------------|
| **Eavesdropping** | Token records and DID documents contain no encryption. Anyone with RPC access can Read. Confidential attributes MUST NOT be placed in on-chain DN if confidentiality is required. TLS protects IdentyClaw HTTP resolvers in transit; it does not hide ledger state. |
| **Replay** | Ledger operations use NEAR transaction nonces. HTTP JWT resolution sessions are replayable until JWT expiry. HOLA proofs (outside this method) use fresh nonces; DID Read itself has no proof-of-possession. |
| **Message insertion** | A malicious RPC can fabricate `rodit_token` results. Mitigate by pinning contract id, using trusted RPC (or several), and optionally checking block hash/height. Inserting a fake mint on a **different** contract does not affect resolvers that pin the canonical account. |
| **Deletion** | A malicious RPC can omit a token (false `notFound`). Burn by the registry owner is real deletion. Holders cannot delete. |
| **Modification** | Unauthorized `rodit_transfer` requires the current owner’s key. Metadata cannot be modified after mint. A lying RPC can modify the **reported** document; compare independent RPCs for high assurance. |
| **Denial of service** | NEAR RPC, mint deposits, and HTTP rate limits are DoS surfaces. View calls are cheaper than mints; public list (`rodit_tokens`) can be paginated. Thin-client resolvers depend on RPC availability (see §9.6). |
| **Amplification** | `rodit_token` responses include metadata and can be larger than the request. HTTP DID documents embed metadata. Resolvers SHOULD cap response size and rate-limit public interfaces. |
| **Man-in-the-middle** | TLS MITM on HTTP resolvers can alter DID JSON. RPC MITM can alter chain views. Pinning contract + TLS + trusted RPC are the mitigations. DID Read does not by itself authenticate the **presenter**. |

### 9.4 Authentication characteristics

Resolution **does not** prove live possession of the controller key. A copied DID document or a screenshot of a `token_id` is not a login. Proof-of-possession for IdentyClaw is HOLA (peer lane) or JWT login (session lane), both of which sign with the current owner (or a delegated subagent key) over fresh challenge data. Those protocols are specified elsewhere; this method only supplies the current verification method.

IdentyClaw HTTP `/.well-known/did/*` requires a JWT because resolution is a metered API feature, not because DID Core requires authentication for Read.

### 9.5 Endpoint authentication and topology

NEAR is a public DLT. Light clients and HTTPS RPC gateways (including public `rpc.mainnet.near.org` and third-party RPCs) are common. Security assumptions:

- A **full node** verifying NEAR state proofs has the strongest Read authenticity.
- A **trusted RPC** is equivalent to trusting that operator for token existence, owner, and keys.
- IdentyClaw’s HTTP resolver is an additional trusted party for callers who do not query NEAR themselves.

Service endpoints in the DID document (`RoditTokenMetadata`, `MCPDiscoveryService`) are **not** authenticated by this method beyond the integrity of Read. Webhook URLs and ContactURI values are self-declared and unsigned relative to the issuance signature over policy fields.

### 9.6 Residual risks

- Compromise of the owner’s NEAR private key allows Update (transfer) and impersonation in proof protocols.
- Compromise of registry burn authority allows Destroy.
- Incorrect resolver implementation (wrong contract pin, accepting uppercase ids, skipping finality) yields false documents.
- Cipher/algorithm: Ed25519 as used by NEAR implicit accounts. A break of Ed25519 or NEAR account-key semantics would break this method.
- Related protocols (HOLA, JWT login, DNS TXT registry attestation in some SDKs) have their own residual risks; a valid DID document does not imply those checks passed.
- Impersonation via look-alike DN: compare the attested `token_id` with out-of-band publication on channels the subject controls.

Signatures on DID documents: this method does **not** require a `proof` on the DID document. Authenticity is ledger state plus RPC trust.

---

## 10. Privacy considerations

Passport records are written to a public blockchain. This method is **not** suitable for identifiers whose associated attributes must remain confidential. The following maps [RFC 6973](https://www.rfc-editor.org/rfc/rfc6973) §5 to `did:rodit`.

### 10.1 Surveillance

Anyone who can query NEAR can enumerate or look up Passports (`rodit_token`, `rodit_tokens`) and observe owner accounts, transfer history, and metadata. There is no access-control on ledger Read. HTTP convenience resolvers currently require JWT, which reduces casual scraping of **that API** but does not prevent chain surveillance. Resolvers and API operators can log resolution requests (IP, `token_id`, JWT subject).

### 10.2 Stored data compromise

On-chain data cannot be deleted by the holder (see §4.4). Operator logs (HTTP resolvers, RPC providers, purchase portal) MAY store IP addresses, account ids, and request metadata. Compromise of those stores leaks **who resolved which DID**, not holder private keys (unless logs were misconfigured). Private keys MUST be stored off-chain by the holder.

### 10.3 Unsolicited traffic

`ContactURI`, `webhook_url`, and similar metadata can be used to message the subject. They are self-declared routing hints, not proof of control. Publishing a DID and metadata on a public ledger enables unsolicited contact. Subjects SHOULD use monitored ContactURI values and treat inbound messages as untrusted until a proof-of-possession check succeeds.

### 10.4 Misattribution

DN fields (names, Creature, ContactURI) are **self-declared**. A different actor can mint another Passport with similar display strings. Attribution of a human or brand to a DID MUST use out-of-band binding of the 12-letter `token_id`, not DN string matching. The facial encoding is a categorical agent appearance, not a biometric of a person.

### 10.5 Correlation

The same `did:rodit:<id>` is globally correlatable across APIs, HOLA, A2A cards, and the ledger. Transfer to a new NEAR account rotates keys but **not** the DID, so correlation to the persistent identifier remains. Using distinct Passports for distinct contexts is the only method-level anti-correlation control.

### 10.6 Identification

The method-specific id is a stable unique identifier. Combined with public DN, avatar URLs, and owner account history, it can identify a person or organisation who chose to put those fields on chain. Facial trait letters may be socially identifying if they match a published portrait.

### 10.7 Secondary use

Ledger history (mint time, transfers, metadata) can be reused by third parties for analytics, scoring, or unsolicited profiling without the subject’s further consent. This specification cannot prevent secondary use of public chain data.

### 10.8 Disclosure

Create discloses `token_id`, owner account, and metadata to the world. Read discloses the current verification key. There is no selective-disclosure mode in the DID document. Do not mint tax identifiers, precise birth data, or other sensitive DN attributes if disclosure is unacceptable; those fields are optional in Passport DN.

### 10.9 Exclusion

Participation requires a NEAR account, mint deposit / fee, and the ability to complete issuance attestation. That excludes people who cannot obtain NEAR or pay the fee. Burn and seizure (privileged) can exclude a subject from the registry without a holder appeal path in this method. Unbounded (`1970-01-01`) validity is an issuer policy choice, not a right.

---

## 11. Intellectual property

Copyright © Discernible Inc. Implementers MAY use this specification to implement `did:rodit` identifiers, resolvers, and related software. IdentyClaw and RODiT are used as product names; no trademark license is granted beyond nominative use in implementations and registry entries.

Registration contact: Discernible Inc. / IdentyClaw — `support@identyclaw.com` — `https://identyclaw.com`.

---

## 12. Related documentation

In-repo (also via MCP `doc:reference:*` and, for this spec, `GET /.well-known/did-method-rodit`):

- [did-method-registry-submission.md](did-method-registry-submission.md) — W3C DID Extensions PR checklist
- [versioning.md](versioning.md) — HTTP API release vs on-chain JSON-LD
- [api-reference.md](api-reference.md#did-resolution) — HTTP endpoints
- [jsonld-metadata.md](jsonld-metadata.md) — Semantic mappings
- [token-metadata.md](token-metadata.md) — Passport fields and facial encoding
- [key-rotation.md](key-rotation.md) — `rodit_transfer`
- [enrollment.md](enrollment.md) — issuance / mint
- [finding-agents.md](finding-agents.md) — impersonation guard
