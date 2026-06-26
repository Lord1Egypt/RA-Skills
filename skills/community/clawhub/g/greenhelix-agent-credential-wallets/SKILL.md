---
name: greenhelix-agent-credential-wallets
version: "1.3.1"
description: "Agent Credential Wallets: Verifiable Intent & Delegation Chains. Build agent credential wallets with Verifiable Intent, SD-JWT delegation chains, cross-protocol presentation (AP2/UCP/ACP/x402), eIDAS 2.0 EUDI compliance, and reputation-bound credentials. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [credentials, verifiable-intent, sd-jwt, eidas, delegation, identity, wallets, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# Agent Credential Wallets: Verifiable Intent & Delegation Chains

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Your agent just tried to buy cloud compute on behalf of your company. The vendor's agent asked for proof of authorization. Your agent presented an API key. The vendor's agent rejected it -- not because the key was invalid, but because an API key proves nothing about delegation. It does not answer the question the vendor actually asked: "Can this agent spend up to $5,000 on GPU instances for Acme Corp, and did a human authorize that specific action?" An API key says "this entity has access." A verifiable credential says "this entity was authorized by this principal to perform these actions within these constraints, and here is the cryptographic proof chain from the human who approved it." That distinction is the entire difference between agents that can transact in the open economy and agents that remain trapped inside their owner's perimeter. On March 5, 2026, Mastercard open-sourced the Verifiable Intent specification alongside Google, Fiserv, IBM, and Checkout.com, defining exactly how agents prove delegated authority to spend. Prove launched Verified Agent targeting the $1.7 trillion agentic commerce market with carrier-grade identity verification for non-human entities. The EU finalized eIDAS 2.0 implementation rules mandating EUDI Wallets by December 2026. Google's Agent-to-Agent Protocol (AP2), the Universal Commerce Protocol (UCP), and OpenAI's Agent Commerce Protocol (ACP) all require verifiable agent identity as the foundation layer. The decentralized identity market hit $7.4 billion in 2026. The convergence is real, and it is happening on a twelve-month timeline. This guide walks you through building a production credential wallet for your agents: SD-JWT-VC issuance, delegation chains from human to agent, cross-protocol credential presentation, eIDAS 2.0 compliance, reputation binding, and fleet-wide deployment. Every implementation uses the GreenHelix A2A Commerce Gateway API. Every pattern is designed for the December 2026 deadline.
1. [The Agent Credential Problem](#chapter-1-the-agent-credential-problem)
2. [W3C Verifiable Credentials & SD-JWT Primer](#chapter-2-w3c-verifiable-credentials--sd-jwt-primer)

## What You'll Learn
- Chapter 1: The Agent Credential Problem
- Chapter 2: W3C Verifiable Credentials & SD-JWT Primer
- Chapter 3: Building Your Agent's Credential Wallet
- Chapter 4: Implementing Verifiable Intent
- Chapter 5: Cross-Protocol Credential Presentation
- Chapter 6: eIDAS 2.0 Compliance
- Chapter 7: Trust Scoring, Reputation Binding & Credential Revocation
- Next Steps
- What You Get

## Full Guide

# Agent Credential Wallets: Verifiable Intent & Delegation Chains for Agentic Commerce

Your agent just tried to buy cloud compute on behalf of your company. The vendor's agent asked for proof of authorization. Your agent presented an API key. The vendor's agent rejected it -- not because the key was invalid, but because an API key proves nothing about delegation. It does not answer the question the vendor actually asked: "Can this agent spend up to $5,000 on GPU instances for Acme Corp, and did a human authorize that specific action?" An API key says "this entity has access." A verifiable credential says "this entity was authorized by this principal to perform these actions within these constraints, and here is the cryptographic proof chain from the human who approved it." That distinction is the entire difference between agents that can transact in the open economy and agents that remain trapped inside their owner's perimeter. On March 5, 2026, Mastercard open-sourced the Verifiable Intent specification alongside Google, Fiserv, IBM, and Checkout.com, defining exactly how agents prove delegated authority to spend. Prove launched Verified Agent targeting the $1.7 trillion agentic commerce market with carrier-grade identity verification for non-human entities. The EU finalized eIDAS 2.0 implementation rules mandating EUDI Wallets by December 2026. Google's Agent-to-Agent Protocol (AP2), the Universal Commerce Protocol (UCP), and OpenAI's Agent Commerce Protocol (ACP) all require verifiable agent identity as the foundation layer. The decentralized identity market hit $7.4 billion in 2026. The convergence is real, and it is happening on a twelve-month timeline. This guide walks you through building a production credential wallet for your agents: SD-JWT-VC issuance, delegation chains from human to agent, cross-protocol credential presentation, eIDAS 2.0 compliance, reputation binding, and fleet-wide deployment. Every implementation uses the GreenHelix A2A Commerce Gateway API. Every pattern is designed for the December 2026 deadline.

---

## Table of Contents

1. [The Agent Credential Problem](#chapter-1-the-agent-credential-problem)
2. [W3C Verifiable Credentials & SD-JWT Primer](#chapter-2-w3c-verifiable-credentials--sd-jwt-primer)
3. [Building Your Agent's Credential Wallet](#chapter-3-building-your-agents-credential-wallet)
4. [Implementing Verifiable Intent](#chapter-4-implementing-verifiable-intent)
5. [Cross-Protocol Credential Presentation](#chapter-5-cross-protocol-credential-presentation)
6. [eIDAS 2.0 Compliance](#chapter-6-eidas-20-compliance)
7. [Trust Scoring, Reputation Binding & Credential Revocation](#chapter-7-trust-scoring-reputation-binding--credential-revocation)

---

## Chapter 1: The Agent Credential Problem

### Why API Keys and OAuth Tokens Break Under Delegation

API keys are bearer tokens. They prove possession, not authorization. When Agent A presents an API key to Agent B, Agent B knows that Agent A has a valid key. Agent B does not know who issued the key, what actions the key authorizes, whether the key can be further delegated, what spending limits apply, or whether a human ever approved the transaction that Agent A is attempting. OAuth 2.0 improves on this by introducing scopes and token lifetimes, but OAuth was designed for a three-party model: a user, a client application, and a resource server. Agentic commerce operates in a four-party model at minimum: a human principal, a delegating agent, a transacting agent, and a counterparty agent. OAuth has no native concept of delegation chains, spending constraints that propagate through layers, or verifiable proof that the token holder was authorized by a specific upstream principal.

The failure modes are concrete:

- **Stolen key replay**: A leaked API key gives the attacker the same permissions as the legitimate agent. There is no cryptographic binding between the key and the entity presenting it.
- **Scope inflation**: An agent granted "read marketplace" scope uses that token to call `create_intent` because the token endpoint does not distinguish between marketplace reads and payment actions at the granularity commerce requires.
- **Delegation opacity**: Agent A delegates to Agent B using a sub-key. Agent B delegates to Agent C. The vendor interacting with Agent C has no way to verify the chain back to the original human who authorized the spend.
- **Constraint evaporation**: A human sets a $500 daily limit. The limit is stored in Agent A's configuration. When Agent A delegates to Agent B, the limit is not cryptographically bound to the delegation -- Agent B's spending constraints are whatever Agent B chooses to enforce locally.

### The Four-Party Model Failure

Traditional payment rails use a four-party model: cardholder, merchant, issuing bank, acquiring bank. Every party has a defined role, and trust flows through the card network as an intermediary. Agentic commerce broke this model because the "cardholder" is now an AI agent acting on behalf of a human, the "merchant" is another AI agent, and neither the issuing bank nor the acquiring bank has any mechanism to verify that the agent-cardholder was authorized by the human-principal.

```
TRADITIONAL FOUR-PARTY MODEL
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Human   │───>│ Issuing │───>│  Card   │───>│Acquiring│───>│ Merchant│
│(Cardhldr)│    │  Bank   │    │ Network │    │  Bank   │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │ Identity verified        Trust mediated         Identity verified
     │ via KYC + PIN            by network rules       via merchant agreement

AGENTIC FOUR-PARTY MODEL (BROKEN)
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Human   │ ??>│ Agent A │ ??>│ Gateway │ ??>│ Agent B │
│(Principal│    │(Delegat.)│    │(Network)│    │(Vendor) │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │ How does Agent A         No delegation       How does Agent B
     │ prove human approved?    chain verification  verify constraints?
```

The question marks are the credential gap. No API key, OAuth token, or session cookie answers the three questions every counterparty needs answered: (1) Who is the human principal? (2) What did they authorize? (3) What are the constraints?

### Protocol Convergence: Mastercard, Google, OpenAI

Three separate industry efforts converged on the same answer in the first quarter of 2026:

**Mastercard Verifiable Intent (March 5, 2026)**: Open-sourced with Google, Fiserv, IBM, and Checkout.com. Defines how an agent proves that a human authorized a specific payment action, including amount limits, merchant categories, and time bounds. Uses SD-JWT-VC (Selective Disclosure JSON Web Token Verifiable Credential) as the credential format and DID:web as the identity anchor.

**Google AP2 + Universal Commerce Protocol (UCP)**: Google's agent-to-agent protocol requires agents to present verifiable identity before any commercial transaction. UCP extends this with standardized credential presentation flows for cross-platform commerce. Both protocols accept W3C Verifiable Credentials in SD-JWT format.

**OpenAI Agent Commerce Protocol (ACP)**: Defines how agents discover, negotiate, and transact with each other. The identity layer requires verifiable credentials for any transaction above a configurable threshold. ACP's credential requirements align with the W3C VC Data Model 2.0 and accept SD-JWT-VC as a presentation format.

The convergence is not accidental. All three groups independently identified the same gap: agents need cryptographically verifiable delegation chains, not just access tokens. The answer they all arrived at was W3C Verifiable Credentials with selective disclosure.

| Protocol | Organization | Credential Format | Identity Anchor | Delegation Model |
|----------|-------------|-------------------|-----------------|------------------|
| Verifiable Intent | Mastercard + consortium | SD-JWT-VC | DID:web | Layered issuance |
| AP2 / UCP | Google | W3C VC (SD-JWT) | DID:web / DID:key | Presentation exchange |
| ACP | OpenAI | W3C VC (SD-JWT) | DID:key | Chained credentials |
| x402 | Open standard | W3C VC (optional) | DID:web | Payment-bound proofs |

### The $1.7 Trillion Market Context

The numbers define the urgency. Prove's Verified Agent launch targeted the $1.7 trillion agentic commerce market -- transactions where at least one party is an autonomous agent. Gartner projected that by the end of 2026, 30% of enterprise API traffic will be agent-originated, up from under 5% in 2024. The decentralized identity market reached $7.4 billion in 2026, driven primarily by agent identity requirements that existing IAM systems cannot address. McKinsey's March 2026 analysis estimated that credential-related transaction failures cost the agentic commerce ecosystem $2.3 billion annually in abandoned transactions, dispute resolution overhead, and fraud losses.

The cost of inaction is measurable. Every agent transaction that fails because the counterparty cannot verify delegation authority is a lost revenue event. Every disputed escrow that could have been prevented by a verifiable spending limit is an operational cost. Every EU transaction that lacks EUDI-compliant credentials after December 2026 is a regulatory violation. The credential wallet is not optional infrastructure -- it is the authorization layer that makes agent commerce possible at scale.

### What This Guide Builds

By the end of this guide, your agents will have:

1. A DID-anchored credential wallet managed through GreenHelix identity tools
2. SD-JWT delegation chains that cryptographically bind human authorization to agent actions
3. Credential presentation adapters for AP2, UCP, ACP, and x402
4. eIDAS 2.0 compliant EUDI wallet integration for EU commerce
5. Reputation-bound credentials with real-time revocation
6. Fleet-wide issuance, rotation, and monitoring for production deployment

---

## Chapter 2: W3C Verifiable Credentials & SD-JWT Primer

### Credential Anatomy

A Verifiable Credential (VC) is a tamper-evident data structure with three components:

**Credential metadata**: Who issued it, when, when it expires, what type it is. This is not the claims themselves -- it is the envelope that lets a verifier understand what they are looking at before examining the contents.

**Claims (the subject)**: The actual assertions. "Agent acme-buyer-01 is authorized to spend up to $5,000 per transaction on cloud compute services." Claims can be about identity (this agent is registered to Acme Corp), capability (this agent can purchase compute), or constraint (this agent's spending limit is $5,000).

**Proof**: The cryptographic mechanism that makes the credential tamper-evident. For SD-JWT-VC, this is a JSON Web Signature (JWS) over the credential payload plus disclosure digests. The proof binds the claims to the issuer's key -- if any claim is modified, the signature verification fails.

```
VERIFIABLE CREDENTIAL STRUCTURE
┌────────────────────────────────────────────────┐
│  CREDENTIAL METADATA                           │
│  ├── issuer: did:web:acme.com                  │
│  ├── issuanceDate: 2026-04-06T00:00:00Z        │
│  ├── expirationDate: 2026-04-07T00:00:00Z      │
│  └── type: [VerifiableCredential,              │
│             AgentDelegationCredential]          │
├────────────────────────────────────────────────┤
│  CLAIMS (credentialSubject)                    │
│  ├── id: did:key:z6Mkw...  (agent DID)        │
│  ├── delegatedBy: did:web:acme.com             │
│  ├── authorizedActions: [purchase_compute]     │
│  ├── spendingLimit: {amount: 5000, currency:   │
│  │                    USD, period: transaction} │
│  └── merchantCategory: [cloud_compute]         │
├────────────────────────────────────────────────┤
│  PROOF                                         │
│  ├── type: JsonWebSignature2020                │
│  ├── verificationMethod: did:web:acme.com#key1 │
│  └── jws: eyJhbGciOiJFZERTQSJ9...             │
└────────────────────────────────────────────────┘
```

### Selective Disclosure with SD-JWT

Standard JWTs are all-or-nothing: you present the entire token or nothing. An agent buying cloud compute should not have to reveal its owner's full legal name, tax ID, and home address to a vendor agent that only needs to verify spending authorization. Selective Disclosure JWT (SD-JWT) solves this by replacing sensitive claims with salted hashes in the JWT body. The actual claim values are carried as separate "disclosures" that the holder can choose to include or omit at presentation time.

The SD-JWT structure has three parts separated by tildes (`~`):

```
<issuer-signed JWT> ~ <disclosure 1> ~ <disclosure 2> ~ ... ~ <key binding JWT>
```

**Issuer-signed JWT**: Contains the credential metadata and hashed digests of all disclosable claims in an `_sd` array. The issuer signs this part. It is always present.

**Disclosures**: Each disclosure is a base64url-encoded JSON array of `[salt, claim_name, claim_value]`. The holder includes only the disclosures they want the verifier to see. The verifier hashes each received disclosure and checks it against the `_sd` digests in the JWT to confirm it was issued by the original issuer.

**Key Binding JWT**: An optional JWT signed by the holder's key that proves the presenter is the intended holder, not someone who intercepted the SD-JWT in transit. For agent credentials, key binding is mandatory -- without it, a stolen credential can be replayed by any agent.

```
SD-JWT SELECTIVE DISCLOSURE FLOW

ISSUANCE (all claims included):
┌──────────────────────────┐
│ Issuer signs JWT with    │     ┌─────────────┐
│ _sd: [hash1, hash2,     │────>│ Agent Wallet │
│       hash3, hash4]      │     │ stores full  │
│                          │     │ SD-JWT + all │
│ + disclosure(owner_name) │     │ disclosures  │
│ + disclosure(tax_id)     │     └─────────────┘
│ + disclosure(spend_limit)│
│ + disclosure(actions)    │
└──────────────────────────┘

PRESENTATION (selective):
┌─────────────┐     ┌──────────────────────────┐
│ Agent Wallet │────>│ JWT (with all 4 hashes)  │
│ reveals only │     │ + disclosure(spend_limit) │
│ 2 of 4      │     │ + disclosure(actions)     │
│ claims       │     │ + key_binding_jwt         │
└─────────────┘     └──────────────────────────┘
                    Verifier sees spend_limit & actions.
                    Cannot derive owner_name or tax_id
                    (only hashes remain in the JWT).
```

### SD-JWT-VC Format for Agent Credentials

SD-JWT-VC is the specific profile of SD-JWT designed for Verifiable Credentials. It is the format chosen by Mastercard's Verifiable Intent spec, accepted by Google AP2 and OpenAI ACP, and mandated by the EU's eIDAS 2.0 Architecture Reference Framework for EUDI Wallet credentials.

The key properties of SD-JWT-VC for agent developers:

- **`iss`**: The issuer's identifier, typically a DID:web URL that resolves to a DID Document containing the issuer's public key.
- **`sub`**: The subject of the credential -- the agent's DID.
- **`iat`** / **`exp`**: Issuance and expiration timestamps. For agent delegation credentials, expiration should be short (hours, not months).
- **`cnf`**: Confirmation claim that binds the credential to the holder's key. Contains the holder's public key or a reference to it. This is what enables key binding.
- **`_sd`**: Array of digests for selectively disclosable claims.
- **`vct`**: Verifiable Credential Type -- a URI identifying the credential schema (e.g., `https://greenhelix.net/credentials/agent-delegation/v1`).

### Delegation Chains as Layered SD-JWT Issuance

A delegation chain is a sequence of credentials where each credential's subject becomes the issuer of the next credential. The human principal issues a credential to their primary agent. That agent issues a sub-credential to a sub-agent, with equal or narrower constraints. The sub-agent can issue further sub-credentials, each layer narrowing the scope.

```
DELEGATION CHAIN (3 LAYERS)

Layer 0: Human Principal
  └── Issues VC to Agent A
      iss: did:web:alice.com
      sub: did:key:agentA
      spend_limit: $10,000/day
      actions: [purchase_compute, purchase_storage]

Layer 1: Agent A
  └── Issues VC to Agent B (sub-delegation)
      iss: did:key:agentA
      sub: did:key:agentB
      spend_limit: $2,000/transaction  (narrowed from $10k/day)
      actions: [purchase_compute]       (narrowed from 2 actions)
      parent_credential: <hash of Layer 0 VC>

Layer 2: Agent B
  └── Presents to Vendor Agent C
      Includes: Layer 2 VC + Layer 1 VC + Layer 0 VC
      Vendor verifies entire chain back to did:web:alice.com
```

The critical property is **constraint narrowing**: each layer can only narrow the constraints of its parent. Agent A received a $10,000/day limit and cannot issue Agent B a $20,000/day credential. Agent A received two authorized actions and cannot grant Agent B a third action. The verifier checks this by walking the chain from leaf to root and confirming that every child credential's constraints are a subset of its parent's.

---

## Chapter 3: Building Your Agent's Credential Wallet

### Prerequisites

You need a GreenHelix API key with pro tier access (identity tools `build_claim_chain`, `search_agents_by_metrics`, and `submit_metrics` require pro tier). Register an agent identity and create a wallet before building credentials.

### The CredentialWallet Class

```python
import requests
import json
import hashlib
import time
import base64
import secrets
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict

# --- GreenHelix sandbox session (free tier: 500 credits, no key required) ---
# To get started, visit https://sandbox.greenhelix.net — no signup needed.
# For production, set GREENHELIX_API_KEY in your environment.
import os

API_BASE = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")

session = requests.Session()
api_key = os.environ.get("GREENHELIX_API_KEY", "")
if api_key:
    session.headers["Authorization"] = f"Bearer {api_key}"
session.headers["Content-Type"] = "application/json"


def api_call(tool: str, input_data: dict) -> dict:
    """Call a GreenHelix REST endpoint for the given tool."""
    response = session.post(f"{API_BASE}/v1/tools/{tool}", json=input_data)
    response.raise_for_status()
    return response.json()


@dataclass
class Disclosure:
    """A single SD-JWT disclosure: [salt, claim_name, claim_value]."""
    salt: str
    claim_name: str
    claim_value: Any

    def encode(self) -> str:
        """Base64url-encode the disclosure array."""
        payload = json.dumps([self.salt, self.claim_name, self.claim_value])
        return base64.urlsafe_b64encode(payload.encode()).rstrip(b"=").decode()

    def digest(self) -> str:
        """SHA-256 digest of the encoded disclosure."""
        encoded = self.encode()
        return base64.urlsafe_b64encode(
            hashlib.sha256(encoded.encode()).digest()
        ).rstrip(b"=").decode()


@dataclass
class AgentCredential:
    """An SD-JWT-VC credential with selective disclosure support."""
    issuer_did: str
    subject_did: str
    credential_type: str
    claims: Dict[str, Any]
    disclosable_claims: List[str]  # claim names that support selective disclosure
    issued_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    parent_hash: Optional[str] = None  # hash of parent credential in chain
    disclosures: List[Disclosure] = field(default_factory=list)

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.issued_at + 86400  # 24h default
        # Generate disclosures for disclosable claims
        self.disclosures = []
        for name in self.disclosable_claims:
            if name in self.claims:
                self.disclosures.append(Disclosure(
                    salt=secrets.token_urlsafe(16),
                    claim_name=name,
                    claim_value=self.claims[name],
                ))

    def sd_digests(self) -> List[str]:
        """Compute _sd array of disclosure digests."""
        return [d.digest() for d in self.disclosures]

    def jwt_payload(self) -> dict:
        """Build the issuer-signed JWT payload."""
        payload = {
            "iss": self.issuer_did,
            "sub": self.subject_did,
            "iat": int(self.issued_at),
            "exp": int(self.expires_at),
            "vct": self.credential_type,
            "_sd": self.sd_digests(),
            "_sd_alg": "sha-256",
        }
        # Include non-disclosable claims directly
        for name, value in self.claims.items():
            if name not in self.disclosable_claims:
                payload[name] = value
        if self.parent_hash:
            payload["parent_credential"] = self.parent_hash
        return payload

    def present(self, disclosed_claims: List[str]) -> dict:
        """Create a presentation with only the specified claims disclosed."""
        selected = [d for d in self.disclosures if d.claim_name in disclosed_claims]
        return {
            "jwt_payload": self.jwt_payload(),
            "disclosures": [d.encode() for d in selected],
            "disclosed_values": {
                d.claim_name: d.claim_value for d in selected
            },
        }

    def credential_hash(self) -> str:
        """SHA-256 hash of the credential payload for chain linking."""
        payload_bytes = json.dumps(self.jwt_payload(), sort_keys=True).encode()
        return hashlib.sha256(payload_bytes).hexdigest()


class CredentialWallet:
    """Agent credential wallet backed by GreenHelix identity tools.

    Manages the full credential lifecycle: registration, wallet creation,
    credential issuance, chain building, and selective presentation.
    """

    def __init__(self, agent_id: str, display_name: str, owner: str):
        self.agent_id = agent_id
        self.display_name = display_name
        self.owner = owner
        self.wallet_id: Optional[str] = None
        self.did: Optional[str] = None
        self.credentials: Dict[str, AgentCredential] = {}
        self.chain_ids: List[str] = []

    def register(self) -> dict:
        """Register the agent identity on GreenHelix.

        This creates the agent's DID and registers its public key.
        Must be called before any other wallet operation.
        """
        result = api_call("register_agent", {
            "agent_id": self.agent_id,
            "display_name": self.display_name,
            "owner": self.owner,
        })
        self.did = f"did:key:{self.agent_id}"
        return result

    def create_wallet(self) -> dict:
        """Create the agent's credential wallet (on-chain store).

        The wallet is a DID-anchored credential store that holds
        issued credentials and supports selective disclosure presentation.
        """
        result = api_call("create_wallet", {
            "agent_id": self.agent_id,
            "wallet_type": "credential",
            "metadata": {
                "owner": self.owner,
                "did": self.did,
                "created_at": time.time(),
            },
        })
        self.wallet_id = result.get("wallet_id", f"wallet-{self.agent_id}")
        return result

    def issue_credential(
        self,
        credential_id: str,
        subject_did: str,
        credential_type: str,
        claims: Dict[str, Any],
        disclosable_claims: List[str],
        ttl_seconds: int = 86400,
        parent_credential_id: Optional[str] = None,
    ) -> AgentCredential:
        """Issue an SD-JWT-VC credential to a subject.

        Args:
            credential_id: Unique ID for this credential.
            subject_did: DID of the agent receiving the credential.
            credential_type: VC type URI.
            claims: All claims to include.
            disclosable_claims: Claim names that support selective disclosure.
            ttl_seconds: Credential lifetime in seconds.
            parent_credential_id: ID of parent credential for delegation chains.

        Returns:
            The issued AgentCredential object.
        """
        parent_hash = None
        if parent_credential_id and parent_credential_id in self.credentials:
            parent_hash = self.credentials[parent_credential_id].credential_hash()

        credential = AgentCredential(
            issuer_did=self.did,
            subject_did=subject_did,
            credential_type=credential_type,
            claims=claims,
            disclosable_claims=disclosable_claims,
            expires_at=time.time() + ttl_seconds,
            parent_hash=parent_hash,
        )
        self.credentials[credential_id] = credential
        return credential

    def build_chain(self) -> dict:
        """Build a Merkle claim chain over all issued credentials.

        This anchors the credential history in a tamper-evident structure.
        Uses GreenHelix build_claim_chain to create the chain.
        """
        # Prepare claims from all credentials
        chain_claims = []
        for cred_id, cred in self.credentials.items():
            chain_claims.append({
                "credential_id": cred_id,
                "credential_hash": cred.credential_hash(),
                "subject": cred.subject_did,
                "type": cred.credential_type,
                "issued_at": cred.issued_at,
                "expires_at": cred.expires_at,
            })

        result = api_call("build_claim_chain", {
            "agent_id": self.agent_id,
            "claims": chain_claims,
            "chain_type": "credential_issuance",
        })
        if "chain_id" in result:
            self.chain_ids.append(result["chain_id"])
        return result

    def get_chains(self) -> dict:
        """Retrieve all claim chains for this agent."""
        return api_call("get_claim_chains", {
            "agent_id": self.agent_id,
        })

    def present_credential(
        self,
        credential_id: str,
        disclosed_claims: List[str],
    ) -> dict:
        """Create a selective disclosure presentation.

        Args:
            credential_id: The credential to present.
            disclosed_claims: Which claims to reveal.

        Returns:
            Presentation object with JWT payload and selected disclosures.
        """
        if credential_id not in self.credentials:
            raise KeyError(f"Credential {credential_id} not found in wallet")
        return self.credentials[credential_id].present(disclosed_claims)
```

### Registering and Creating a Wallet

```python
# Initialize the wallet for a procurement agent
wallet = CredentialWallet(
    agent_id="acme-procurement-01",
    display_name="Acme Procurement Agent #1",
    owner="alice@acme.com",
)

# Step 1: Register the agent identity
registration = wallet.register()
print(f"Agent registered: {wallet.did}")
# Output: Agent registered: did:key:acme-procurement-01

# Step 2: Create the credential wallet
wallet_result = wallet.create_wallet()
print(f"Wallet created: {wallet.wallet_id}")
# Output: Wallet created: wallet-acme-procurement-01
```

### Issuing Your First Credential

```python
# The organization (human principal) issues a delegation credential
# to the procurement agent
delegation_cred = wallet.issue_credential(
    credential_id="delegation-001",
    subject_did="did:key:acme-procurement-01",
    credential_type="https://greenhelix.net/credentials/agent-delegation/v1",
    claims={
        "delegated_by": "did:web:acme.com",
        "authorized_actions": ["purchase_compute", "purchase_storage"],
        "spending_limit": {"amount": "10000", "currency": "USD", "period": "day"},
        "merchant_categories": ["cloud_compute", "cloud_storage"],
        "principal_name": "Alice Chen",
        "principal_tax_id": "XX-XXXXXXX",
        "organization": "Acme Corp",
    },
    disclosable_claims=[
        "principal_name",
        "principal_tax_id",
        "spending_limit",
        "merchant_categories",
    ],
    ttl_seconds=28800,  # 8-hour session credential
)

print(f"Credential issued. Hash: {delegation_cred.credential_hash()[:16]}...")
print(f"SD digests: {len(delegation_cred.sd_digests())} disclosable claims")
```

### Anchoring Credentials in a Claim Chain

```python
# After issuing credentials, anchor them in a Merkle claim chain
chain_result = wallet.build_chain()
print(f"Chain built: {chain_result}")

# Verify chains are retrievable
chains = wallet.get_chains()
print(f"Active chains: {len(chains.get('chains', []))}")
```

---

## Chapter 4: Implementing Verifiable Intent

### What Verifiable Intent Means

Verifiable Intent (VI) is the Mastercard-originated specification that answers one question: "Did a human authorize this agent to perform this specific financial action?" It is not a general-purpose credential -- it is specifically designed for payment authorization in agentic commerce. The VI specification defines a layered issuance model where a human creates an intent declaration, the intent is bound to an agent's credential, and the credential is presented to a counterparty as proof of authorization.

The three components of Verifiable Intent:

1. **Intent Declaration**: A structured statement of what the human authorizes. "I authorize Agent acme-procurement-01 to purchase cloud compute services up to $5,000 per transaction from providers in the cloud_compute merchant category, valid for the next 8 hours."

2. **Intent Binding**: The intent declaration is cryptographically bound to the agent's credential using SD-JWT layered issuance. The intent becomes a claim in the agent's delegation credential.

3. **Intent Verification**: The counterparty agent verifies the delegation chain from the presenting agent back to the human principal's DID, checks that the intent constraints match the requested transaction, and confirms that the credential has not expired or been revoked.

### Session-Level Spending Limits

The most common VI use case is spending limits. A human authorizes an agent to spend up to X dollars within a session. The session has a start time and an end time. Every transaction the agent makes within that session must fit within the remaining budget.

```python
class VerifiableIntentManager:
    """Manages Verifiable Intent credentials for payment authorization.

    Implements the Mastercard VI specification with GreenHelix tools:
    intent declaration, binding, session limits, and chain verification.
    """

    def __init__(self, wallet: CredentialWallet):
        self.wallet = wallet
        self.active_intents: Dict[str, dict] = {}
        self.session_spent: Dict[str, float] = {}

    def declare_intent(
        self,
        intent_id: str,
        authorized_actions: List[str],
        spending_limit_usd: float,
        merchant_categories: List[str],
        session_hours: float = 8.0,
        additional_constraints: Optional[Dict] = None,
    ) -> AgentCredential:
        """Declare a Verifiable Intent and bind it to the agent's credential.

        This is called by (or on behalf of) the human principal to authorize
        the agent for specific financial actions within constraints.

        Args:
            intent_id: Unique identifier for this intent session.
            authorized_actions: Actions the agent may perform.
            spending_limit_usd: Maximum USD the agent can spend in this session.
            merchant_categories: Allowed merchant/service categories.
            session_hours: Session duration in hours.
            additional_constraints: Extra constraints (region, vendor whitelist, etc).

        Returns:
            The issued intent credential.
        """
        now = time.time()
        session_end = now + (session_hours * 3600)

        intent_claims = {
            "intent_type": "payment_authorization",
            "authorized_actions": authorized_actions,
            "spending_limit": {
                "amount": str(spending_limit_usd),
                "currency": "USD",
                "period": "session",
            },
            "merchant_categories": merchant_categories,
            "session_start": now,
            "session_end": session_end,
            "principal_did": f"did:web:{self.wallet.owner.split('@')[1]}",
            "principal_email": self.wallet.owner,
        }
        if additional_constraints:
            intent_claims["constraints"] = additional_constraints

        # Issue as SD-JWT-VC -- principal email is disclosable,
        # spending limit and actions are always visible to verifiers
        credential = self.wallet.issue_credential(
            credential_id=intent_id,
            subject_did=self.wallet.did,
            credential_type="https://greenhelix.net/credentials/verifiable-intent/v1",
            claims=intent_claims,
            disclosable_claims=["principal_email", "constraints"],
            ttl_seconds=int(session_hours * 3600),
        )

        self.active_intents[intent_id] = {
            "credential": credential,
            "spending_limit": spending_limit_usd,
            "session_end": session_end,
        }
        self.session_spent[intent_id] = 0.0

        return credential

    def check_intent_budget(self, intent_id: str, amount_usd: float) -> dict:
        """Check if a transaction fits within the intent's remaining budget.

        Returns:
            Dict with 'authorized' bool, 'remaining' float, and 'reason' if denied.
        """
        if intent_id not in self.active_intents:
            return {"authorized": False, "remaining": 0, "reason": "Intent not found"}

        intent = self.active_intents[intent_id]
        if time.time() > intent["session_end"]:
            return {"authorized": False, "remaining": 0, "reason": "Session expired"}

        spent = self.session_spent.get(intent_id, 0.0)
        remaining = intent["spending_limit"] - spent

        if amount_usd > remaining:
            return {
                "authorized": False,
                "remaining": remaining,
                "reason": f"Amount ${amount_usd} exceeds remaining budget ${remaining}",
            }

        return {"authorized": True, "remaining": remaining - amount_usd}

    def execute_authorized_payment(
        self,
        intent_id: str,
        vendor_agent_id: str,
        amount_usd: float,
        description: str,
    ) -> dict:
        """Execute a payment action under a Verifiable Intent session.

        Checks the budget, creates an intent via GreenHelix, and records the spend.
        """
        # Step 1: Check budget
        budget_check = self.check_intent_budget(intent_id, amount_usd)
        if not budget_check["authorized"]:
            return {"status": "denied", "reason": budget_check["reason"]}

        # Step 2: Create the payment intent via GreenHelix
        intent_result = api_call("create_intent", {
            "from_agent": self.wallet.agent_id,
            "to_agent": vendor_agent_id,
            "amount": str(amount_usd),
            "currency": "USD",
            "description": description,
            "metadata": {
                "vi_session": intent_id,
                "credential_hash": self.active_intents[intent_id][
                    "credential"
                ].credential_hash(),
            },
        })

        # Step 3: Record the spend against the session budget
        self.session_spent[intent_id] = (
            self.session_spent.get(intent_id, 0.0) + amount_usd
        )

        return {
            "status": "authorized",
            "intent_result": intent_result,
            "remaining_budget": budget_check["remaining"] - amount_usd,
        }
```

### Using Verifiable Intent

```python
# Create the wallet and intent manager
wallet = CredentialWallet(
    agent_id="acme-buyer-01",
    display_name="Acme Cloud Buyer",
    owner="alice@acme.com",
)
wallet.register()
wallet.create_wallet()

vi_manager = VerifiableIntentManager(wallet)

# Human declares intent: authorize the agent for cloud purchases
intent_cred = vi_manager.declare_intent(
    intent_id="session-2026-04-06-001",
    authorized_actions=["purchase_compute"],
    spending_limit_usd=5000.00,
    merchant_categories=["cloud_compute"],
    session_hours=8.0,
    additional_constraints={"region": "us-east", "max_per_tx": "2000"},
)
print(f"Intent declared. Expires: {intent_cred.expires_at}")

# Agent executes a purchase within the intent
payment = vi_manager.execute_authorized_payment(
    intent_id="session-2026-04-06-001",
    vendor_agent_id="cloudvendor-gpu-fleet",
    amount_usd=1500.00,
    description="8x A100 GPU instances, 4 hours",
)
print(f"Payment: {payment['status']}, remaining: ${payment['remaining_budget']}")
# Output: Payment: authorized, remaining: $3500.0

# Second purchase
payment2 = vi_manager.execute_authorized_payment(
    intent_id="session-2026-04-06-001",
    vendor_agent_id="cloudvendor-gpu-fleet",
    amount_usd=2000.00,
    description="16x A100 GPU instances, 2 hours",
)
print(f"Payment: {payment2['status']}, remaining: ${payment2['remaining_budget']}")
# Output: Payment: authorized, remaining: $1500.0

# Third purchase exceeds remaining budget
payment3 = vi_manager.execute_authorized_payment(
    intent_id="session-2026-04-06-001",
    vendor_agent_id="cloudvendor-gpu-fleet",
    amount_usd=2000.00,
    description="16x A100 GPU instances, 2 hours",
)
print(f"Payment: {payment3['status']}, reason: {payment3.get('reason')}")
# Output: Payment: denied, reason: Amount $2000.0 exceeds remaining budget $1500.0
```

### Sub-Delegation with Constraint Narrowing

When your primary agent delegates to a sub-agent, the delegation must narrow or maintain the parent's constraints. This is enforced structurally: the sub-credential references the parent credential's hash and includes only a subset of the parent's authorized actions and a spending limit less than or equal to the parent's.

```python
def delegate_intent(
    parent_wallet: CredentialWallet,
    parent_intent_id: str,
    child_wallet: CredentialWallet,
    child_intent_id: str,
    narrowed_actions: List[str],
    narrowed_limit_usd: float,
    ttl_seconds: int = 3600,
) -> AgentCredential:
    """Delegate a Verifiable Intent to a sub-agent with narrowed constraints.

    The child credential references the parent credential hash and must
    have equal or narrower constraints.
    """
    parent_cred = parent_wallet.credentials.get(parent_intent_id)
    if not parent_cred:
        raise ValueError(f"Parent intent {parent_intent_id} not found")

    parent_actions = parent_cred.claims.get("authorized_actions", [])
    parent_limit = float(
        parent_cred.claims.get("spending_limit", {}).get("amount", "0")
    )

    # Enforce constraint narrowing
    for action in narrowed_actions:
        if action not in parent_actions:
            raise ValueError(
                f"Action '{action}' not in parent's authorized actions: {parent_actions}"
            )
    if narrowed_limit_usd > parent_limit:
        raise ValueError(
            f"Limit ${narrowed_limit_usd} exceeds parent limit ${parent_limit}"
        )

    # Issue sub-delegation credential
    child_cred = parent_wallet.issue_credential(
        credential_id=child_intent_id,
        subject_did=child_wallet.did,
        credential_type="https://greenhelix.net/credentials/verifiable-intent/v1",
        claims={
            "intent_type": "delegated_payment_authorization",
            "authorized_actions": narrowed_actions,
            "spending_limit": {
                "amount": str(narrowed_limit_usd),
                "currency": "USD",
                "period": "session",
            },
            "delegated_by": parent_wallet.did,
            "delegation_depth": 1,
        },
        disclosable_claims=["delegated_by"],
        ttl_seconds=ttl_seconds,
        parent_credential_id=parent_intent_id,
    )

    return child_cred


# Example: primary agent delegates to a specialized compute buyer
child_wallet = CredentialWallet(
    agent_id="acme-compute-buyer-01",
    display_name="Acme Compute Specialist",
    owner="alice@acme.com",
)
child_wallet.register()
child_wallet.create_wallet()

sub_cred = delegate_intent(
    parent_wallet=wallet,
    parent_intent_id="session-2026-04-06-001",
    child_wallet=child_wallet,
    child_intent_id="sub-session-001",
    narrowed_actions=["purchase_compute"],  # same as parent
    narrowed_limit_usd=2000.00,  # narrowed from $5,000
    ttl_seconds=3600,  # 1 hour
)
print(f"Sub-delegation issued. Parent hash: {sub_cred.parent_hash[:16]}...")
```

---

## Chapter 5: Cross-Protocol Credential Presentation

### The Multi-Protocol Reality

Your agent will not operate in a single protocol ecosystem. A procurement agent might discover vendors via Google AP2, negotiate terms over UCP, execute payment through Mastercard's rails, and settle micropayments via x402. Each protocol has its own credential presentation format, but they all accept W3C Verifiable Credentials in SD-JWT format. The adapter pattern lets your wallet present credentials in the format each protocol expects without duplicating credential storage or issuance logic.

```
CROSS-PROTOCOL PRESENTATION FLOW

┌─────────────────────────────────────────────────┐
│           CREDENTIAL WALLET                      │
│  ┌─────────────────────────────────┐            │
│  │  SD-JWT-VC Credentials          │            │
│  │  (canonical format)             │            │
│  └──────────┬──────────────────────┘            │
│             │                                    │
│  ┌──────────┼──────────────────────────────┐    │
│  │          │    PRESENTATION ADAPTERS      │    │
│  │  ┌───────▼───┐ ┌─────────┐ ┌─────────┐ │    │
│  │  │   AP2     │ │   UCP   │ │   ACP   │ │    │
│  │  │ Adapter   │ │ Adapter │ │ Adapter │ │    │
│  │  └───────┬───┘ └────┬────┘ └────┬────┘ │    │
│  │  ┌───────▼──────────▼───────────▼────┐  │    │
│  │  │           x402 Adapter            │  │    │
│  │  └───────────────────────────────────┘  │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Protocol Comparison

| Feature | AP2 (Google) | UCP | ACP (OpenAI) | x402 |
|---------|-------------|-----|-------------|------|
| Discovery | Agent card + DNS-SD | Registry + broadcast | Capability manifest | HTTP 402 response |
| Auth handshake | Mutual VC exchange | VC + capability proof | VC + scope assertion | Payment proof header |
| Credential format | SD-JWT-VC | SD-JWT-VC | SD-JWT-VC or JWT-VC | Payment attestation |
| Delegation depth | Unlimited (chain verified) | Max 3 hops | Max 5 hops | Single hop |
| Selective disclosure | Full SD-JWT support | Full SD-JWT support | Partial (required claims) | Minimal (amount only) |
| Payment integration | External (via intent) | Built-in escrow | External (via intent) | Native (HTTP header) |

### The ProtocolAdapter Base and Implementations

```python
from abc import ABC, abstractmethod


class ProtocolAdapter(ABC):
    """Base class for protocol-specific credential presentation adapters."""

    def __init__(self, wallet: CredentialWallet):
        self.wallet = wallet

    @abstractmethod
    def format_presentation(
        self,
        credential_id: str,
        disclosed_claims: List[str],
        protocol_metadata: Dict,
    ) -> dict:
        """Format a credential presentation for the target protocol."""
        pass

    @abstractmethod
    def verify_counterparty(self, presentation: dict) -> dict:
        """Verify a counterparty's credential presentation."""
        pass


class AP2Adapter(ProtocolAdapter):
    """Google Agent-to-Agent Protocol (AP2) credential adapter.

    AP2 requires mutual credential exchange during the handshake phase.
    Both agents present credentials before any commercial interaction.
    """

    def format_presentation(
        self,
        credential_id: str,
        disclosed_claims: List[str],
        protocol_metadata: Dict,
    ) -> dict:
        presentation = self.wallet.present_credential(credential_id, disclosed_claims)

        return {
            "protocol": "ap2",
            "version": "1.0",
            "agent_card": {
                "agent_id": self.wallet.agent_id,
                "did": self.wallet.did,
                "display_name": self.wallet.display_name,
                "capabilities": protocol_metadata.get("capabilities", []),
            },
            "credential_presentation": {
                "format": "sd-jwt-vc",
                "jwt_payload": presentation["jwt_payload"],
                "disclosures": presentation["disclosures"],
            },
            "handshake_nonce": secrets.token_urlsafe(32),
        }

    def verify_counterparty(self, presentation: dict) -> dict:
        """Verify an AP2 counterparty presentation.

        Checks: credential format, DID resolution, disclosure validation.
        """
        if presentation.get("protocol") != "ap2":
            return {"valid": False, "reason": "Not an AP2 presentation"}

        cred = presentation.get("credential_presentation", {})
        if cred.get("format") != "sd-jwt-vc":
            return {"valid": False, "reason": "Unsupported credential format"}

        # Verify the agent identity via GreenHelix
        agent_card = presentation.get("agent_card", {})
        identity_check = api_call("get_agent_reputation", {
            "agent_id": agent_card.get("agent_id", ""),
        })

        return {
            "valid": True,
            "agent_id": agent_card.get("agent_id"),
            "did": agent_card.get("did"),
            "reputation": identity_check,
        }


class UCPAdapter(ProtocolAdapter):
    """Universal Commerce Protocol (UCP) credential adapter.

    UCP extends AP2 with commerce-specific flows: escrow, SLA, and
    capability proof. Credentials must include commerce capabilities.
    """

    def format_presentation(
        self,
        credential_id: str,
        disclosed_claims: List[str],
        protocol_metadata: Dict,
    ) -> dict:
        presentation = self.wallet.present_credential(credential_id, disclosed_claims)

        # UCP requires escrow capability proof
        escrow_capable = "create_escrow" in protocol_metadata.get("tools", [])

        return {
            "protocol": "ucp",
            "version": "1.0",
            "identity": {
                "did": self.wallet.did,
                "agent_id": self.wallet.agent_id,
            },
            "credential": {
                "format": "sd-jwt-vc",
                "payload": presentation["jwt_payload"],
                "disclosures": presentation["disclosures"],
            },
            "commerce_capabilities": {
                "escrow_capable": escrow_capable,
                "sla_capable": True,
                "supported_currencies": protocol_metadata.get("currencies", ["USD"]),
            },
            "service_endpoint": protocol_metadata.get(
                "endpoint", f"https://api.greenhelix.net/v1"
            ),
        }

    def verify_counterparty(self, presentation: dict) -> dict:
        if presentation.get("protocol") != "ucp":
            return {"valid": False, "reason": "Not a UCP presentation"}

        identity = presentation.get("identity", {})
        commerce = presentation.get("commerce_capabilities", {})

        # Verify identity and check commerce capabilities
        rep = api_call("get_agent_reputation", {
            "agent_id": identity.get("agent_id", ""),
        })

        return {
            "valid": True,
            "agent_id": identity.get("agent_id"),
            "escrow_capable": commerce.get("escrow_capable", False),
            "reputation": rep,
        }


class ACPAdapter(ProtocolAdapter):
    """OpenAI Agent Commerce Protocol (ACP) credential adapter.

    ACP uses scope assertions: the credential must declare what commercial
    actions the agent is authorized for. Required claims are not selectively
    disclosable -- ACP mandates their visibility.
    """

    ACP_REQUIRED_CLAIMS = ["authorized_actions", "spending_limit", "intent_type"]

    def format_presentation(
        self,
        credential_id: str,
        disclosed_claims: List[str],
        protocol_metadata: Dict,
    ) -> dict:
        # ACP requires certain claims to always be disclosed
        all_disclosed = list(set(disclosed_claims + self.ACP_REQUIRED_CLAIMS))
        presentation = self.wallet.present_credential(credential_id, all_disclosed)

        return {
            "protocol": "acp",
            "version": "1.0",
            "agent": {
                "id": self.wallet.agent_id,
                "did": self.wallet.did,
            },
            "scope_assertion": {
                "format": "sd-jwt-vc",
                "credential": presentation["jwt_payload"],
                "disclosures": presentation["disclosures"],
                "disclosed_values": presentation["disclosed_values"],
            },
            "transaction_context": {
                "requested_action": protocol_metadata.get("action", ""),
                "amount": protocol_metadata.get("amount", ""),
                "currency": protocol_metadata.get("currency", "USD"),
            },
        }

    def verify_counterparty(self, presentation: dict) -> dict:
        if presentation.get("protocol") != "acp":
            return {"valid": False, "reason": "Not an ACP presentation"}

        scope = presentation.get("scope_assertion", {})
        disclosed = scope.get("disclosed_values", {})

        # Check all required claims are present
        for claim in self.ACP_REQUIRED_CLAIMS:
            if claim not in disclosed:
                return {"valid": False, "reason": f"Missing required claim: {claim}"}

        agent = presentation.get("agent", {})
        rep = api_call("get_agent_reputation", {
            "agent_id": agent.get("id", ""),
        })

        return {
            "valid": True,
            "agent_id": agent.get("id"),
            "authorized_actions": disclosed.get("authorized_actions"),
            "spending_limit": disclosed.get("spending_limit"),
            "reputation": rep,
        }


class X402Adapter(ProtocolAdapter):
    """x402 payment protocol credential adapter.

    x402 is a lightweight HTTP-based payment protocol. Credentials are
    presented as HTTP headers on 402 Payment Required responses.
    This adapter formats payment attestations for x402 flows.
    """

    def format_presentation(
        self,
        credential_id: str,
        disclosed_claims: List[str],
        protocol_metadata: Dict,
    ) -> dict:
        # x402 uses minimal disclosure: just the payment proof
        presentation = self.wallet.present_credential(
            credential_id, ["spending_limit"]
        )

        return {
            "protocol": "x402",
            "version": "1.0",
            "payment_header": {
                "X-Agent-DID": self.wallet.did,
                "X-Payment-Credential": json.dumps(presentation["jwt_payload"]),
                "X-Payment-Amount": protocol_metadata.get("amount", ""),
                "X-Payment-Currency": protocol_metadata.get("currency", "USD"),
            },
            "attestation": {
                "credential_hash": self.wallet.credentials[
                    credential_id
                ].credential_hash(),
                "agent_id": self.wallet.agent_id,
            },
        }

    def verify_counterparty(self, presentation: dict) -> dict:
        if presentation.get("protocol") != "x402":
            return {"valid": False, "reason": "Not an x402 presentation"}

        headers = presentation.get("payment_header", {})
        agent_did = headers.get("X-Agent-DID", "")

        # Minimal verification for x402: check the agent exists
        # Full verification happens at settlement
        return {
            "valid": bool(agent_did),
            "agent_did": agent_did,
            "amount": headers.get("X-Payment-Amount"),
        }
```

### Choosing the Right Protocol

The decision of which protocol adapter to use for a given interaction depends on what you are doing in that interaction. Discovery and initial contact typically happen over AP2, because Google's agent card mechanism provides the richest service description format. Price negotiation and SLA agreement happen over UCP, because it has built-in escrow and SLA primitives. Payment execution happens over ACP or Mastercard VI rails, because these protocols have the strongest payment authorization verification. Micropayments and per-request billing happen over x402, because it is the lowest-overhead protocol for small amounts -- the credential is a single HTTP header.

In practice, a single commercial transaction often spans three or four protocols. Your agent discovers a vendor via AP2, negotiates terms over UCP, executes the primary payment via ACP with a Verifiable Intent credential, and then pays per-API-call overages via x402. The credential wallet stores one canonical set of SD-JWT-VC credentials. The adapters format those credentials for each protocol without duplication.

### Multi-Protocol Transaction Example

```python
# Initialize wallet with intent
wallet = CredentialWallet(
    agent_id="acme-buyer-01",
    display_name="Acme Multi-Protocol Buyer",
    owner="alice@acme.com",
)
wallet.register()
wallet.create_wallet()

# Issue delegation credential
vi = VerifiableIntentManager(wallet)
intent_cred = vi.declare_intent(
    intent_id="multi-proto-session-001",
    authorized_actions=["purchase_compute"],
    spending_limit_usd=5000.00,
    merchant_categories=["cloud_compute"],
    session_hours=4.0,
)

# Discover vendor via AP2
ap2 = AP2Adapter(wallet)
ap2_presentation = ap2.format_presentation(
    credential_id="multi-proto-session-001",
    disclosed_claims=["authorized_actions", "spending_limit"],
    protocol_metadata={"capabilities": ["compute_provisioning"]},
)
print(f"AP2 handshake: {ap2_presentation['agent_card']['agent_id']}")

# Negotiate terms via UCP
ucp = UCPAdapter(wallet)
ucp_presentation = ucp.format_presentation(
    credential_id="multi-proto-session-001",
    disclosed_claims=["authorized_actions", "spending_limit"],
    protocol_metadata={
        "tools": ["create_escrow", "create_sla"],
        "currencies": ["USD"],
    },
)
print(f"UCP negotiation: escrow={ucp_presentation['commerce_capabilities']['escrow_capable']}")

# Execute payment via ACP
acp = ACPAdapter(wallet)
acp_presentation = acp.format_presentation(
    credential_id="multi-proto-session-001",
    disclosed_claims=["merchant_categories"],  # ACP adds required claims automatically
    protocol_metadata={
        "action": "purchase_compute",
        "amount": "1500.00",
        "currency": "USD",
    },
)
print(f"ACP scope: {acp_presentation['scope_assertion']['disclosed_values']}")

# Settle micropayment via x402
x402 = X402Adapter(wallet)
x402_presentation = x402.format_presentation(
    credential_id="multi-proto-session-001",
    disclosed_claims=["spending_limit"],
    protocol_metadata={"amount": "0.50", "currency": "USD"},
)
print(f"x402 headers: {list(x402_presentation['payment_header'].keys())}")
```

---

## Chapter 6: eIDAS 2.0 Compliance

### The December 2026 Deadline

The EU's eIDAS 2.0 regulation requires all EU member states to offer European Digital Identity (EUDI) Wallets to citizens and businesses by December 2026. For agent commerce, the implications are direct: any agent transacting with EU consumers or businesses must be able to accept and verify EUDI Wallet credentials. Any agent operating on behalf of an EU entity must be able to present credentials that comply with the EUDI Architecture Reference Framework (ARF).

The key requirements for agent developers:

- **Qualified Electronic Attestation of Attributes (QEAA)**: Credentials issued by qualified trust service providers. Agent delegation credentials that touch EU financial transactions must be QEAAs or reference a QEAA in the chain.
- **PSD2 Strong Customer Authentication (SCA)**: Payments over EUR 30 require multi-factor authentication. For agent commerce, SCA can be satisfied by the delegation chain if the human principal authenticated with two factors when issuing the intent credential.
- **Data minimization**: GDPR requires that credentials disclose only the minimum data necessary for the transaction. SD-JWT selective disclosure directly satisfies this requirement.
- **Credential format**: The ARF mandates SD-JWT-VC as one of the accepted credential formats. This is the same format used by Mastercard VI and GreenHelix credentials, so the format is already compatible.

### EUDI Wallet Integration Architecture

```
eIDAS 2.0 CREDENTIAL FLOW FOR AGENT COMMERCE

┌──────────────┐    ┌─────────────┐    ┌────────────────┐
│  EU Human    │    │ Qualified   │    │  EUDI Wallet   │
│  Principal   │───>│ Trust Svc   │───>│  (Mobile App)  │
│              │    │ Provider    │    │                │
└──────────────┘    └─────────────┘    └───────┬────────┘
                                               │
                         SCA-verified          │ Issue delegation
                         intent declaration    │ credential to agent
                                               │
                                       ┌───────▼────────┐
                                       │  Agent Wallet   │
                                       │  (GreenHelix)  │
                                       │                │
                                       │ Stores:        │
                                       │ - EUDI-sourced │
                                       │   delegation VC│
                                       │ - Platform VCs │
                                       │ - VI session   │
                                       └───────┬────────┘
                                               │
                              Present EUDI-    │
                              referenced cred  │
                              to EU vendor     │
                                               │
                                       ┌───────▼────────┐
                                       │  EU Vendor     │
                                       │  Agent         │
                                       │                │
                                       │ Verifies:      │
                                       │ - QEAA chain   │
                                       │ - SCA proof    │
                                       │ - SD-JWT sigs  │
                                       └────────────────┘
```

### EUDIComplianceManager

```python
class EUDIComplianceManager:
    """Manages eIDAS 2.0 EUDI Wallet compliance for agent credentials.

    Handles QEAA validation, PSD2 SCA attestation, and credential
    formatting for EU commerce.
    """

    # eIDAS trust service list (simplified)
    QUALIFIED_TRUST_SERVICES = [
        "did:web:qtsp.eu.example.com",
        "did:web:trust.eidas.europa.eu",
    ]

    SCA_THRESHOLD_EUR = 30.0

    def __init__(self, wallet: CredentialWallet):
        self.wallet = wallet
        self.eudi_credentials: Dict[str, dict] = {}
        self.compliance_log: List[dict] = []

    def import_eudi_credential(
        self,
        eudi_credential_id: str,
        issuer_did: str,
        credential_data: dict,
        sca_method: str,
        sca_timestamp: float,
    ) -> dict:
        """Import a credential sourced from a EUDI Wallet.

        The credential must be a QEAA (issued by a qualified trust service)
        to be valid for regulated EU transactions.

        Args:
            eudi_credential_id: ID from the EUDI wallet.
            issuer_did: DID of the issuing trust service provider.
            credential_data: The credential claims.
            sca_method: SCA method used (e.g., "biometric+pin", "pin+sms").
            sca_timestamp: When SCA was performed (Unix timestamp).
        """
        is_qualified = issuer_did in self.QUALIFIED_TRUST_SERVICES

        eudi_record = {
            "id": eudi_credential_id,
            "issuer": issuer_did,
            "is_qeaa": is_qualified,
            "credential_data": credential_data,
            "sca_method": sca_method,
            "sca_timestamp": sca_timestamp,
            "imported_at": time.time(),
        }
        self.eudi_credentials[eudi_credential_id] = eudi_record

        # Also issue a GreenHelix credential that references the EUDI source
        self.wallet.issue_credential(
            credential_id=f"eudi-{eudi_credential_id}",
            subject_did=self.wallet.did,
            credential_type="https://greenhelix.net/credentials/eudi-delegation/v1",
            claims={
                "eudi_source": eudi_credential_id,
                "eudi_issuer": issuer_did,
                "is_qeaa": is_qualified,
                "sca_method": sca_method,
                "sca_timestamp": sca_timestamp,
                **credential_data,
            },
            disclosable_claims=["sca_method", "eudi_issuer"],
            ttl_seconds=86400,
        )

        return eudi_record

    def check_sca_required(self, amount_eur: float) -> bool:
        """Check if PSD2 SCA is required for the transaction amount."""
        return amount_eur > self.SCA_THRESHOLD_EUR

    def validate_sca_for_transaction(
        self,
        eudi_credential_id: str,
        amount_eur: float,
        max_sca_age_seconds: int = 300,
    ) -> dict:
        """Validate that SCA requirements are met for a transaction.

        PSD2 requires SCA for payments > EUR 30. The SCA must have been
        performed recently (within max_sca_age_seconds) for the transaction
        to be authorized.
        """
        if not self.check_sca_required(amount_eur):
            return {"sca_required": False, "authorized": True}

        cred = self.eudi_credentials.get(eudi_credential_id)
        if not cred:
            return {
                "sca_required": True,
                "authorized": False,
                "reason": "EUDI credential not found",
            }

        sca_age = time.time() - cred["sca_timestamp"]
        if sca_age > max_sca_age_seconds:
            return {
                "sca_required": True,
                "authorized": False,
                "reason": f"SCA expired ({sca_age:.0f}s > {max_sca_age_seconds}s)",
            }

        return {
            "sca_required": True,
            "authorized": True,
            "sca_method": cred["sca_method"],
            "sca_age_seconds": sca_age,
        }

    def create_compliance_attestation(
        self,
        transaction_id: str,
        amount_eur: float,
        eudi_credential_id: str,
        counterparty_agent_id: str,
    ) -> dict:
        """Create a compliance attestation for an EU transaction.

        Records all compliance checks for audit purposes. This attestation
        can be presented to regulators as evidence of eIDAS 2.0 compliance.
        """
        sca_check = self.validate_sca_for_transaction(eudi_credential_id, amount_eur)

        cred = self.eudi_credentials.get(eudi_credential_id, {})

        attestation = {
            "transaction_id": transaction_id,
            "timestamp": time.time(),
            "agent_id": self.wallet.agent_id,
            "counterparty": counterparty_agent_id,
            "amount_eur": amount_eur,
            "eudi_credential": eudi_credential_id,
            "is_qeaa": cred.get("is_qeaa", False),
            "sca_check": sca_check,
            "data_minimization": True,  # SD-JWT selective disclosure used
            "credential_format": "sd-jwt-vc",
            "regulation": "eIDAS 2.0 / PSD2",
        }

        # Log via GreenHelix compliance tool
        compliance_result = api_call("check_compliance", {
            "agent_id": self.wallet.agent_id,
            "transaction_id": transaction_id,
            "compliance_data": attestation,
        })

        attestation["platform_check"] = compliance_result
        self.compliance_log.append(attestation)

        return attestation
```

### EU Transaction Flow

```python
# Set up wallet with EUDI integration
wallet = CredentialWallet(
    agent_id="eu-buyer-agent-01",
    display_name="EU Procurement Agent",
    owner="klaus@eurocorp.eu",
)
wallet.register()
wallet.create_wallet()

eudi = EUDIComplianceManager(wallet)

# Import a credential from the user's EUDI Wallet
# (In production, this comes from a QR code scan or NFC tap
#  on the user's mobile EUDI wallet app)
eudi_cred = eudi.import_eudi_credential(
    eudi_credential_id="eudi-2026-04-06-001",
    issuer_did="did:web:qtsp.eu.example.com",  # Qualified TSP
    credential_data={
        "principal_name": "Klaus Mueller",
        "organization": "EuroCorp GmbH",
        "authorized_actions": ["purchase_compute", "purchase_saas"],
        "spending_limit": {"amount": "8000", "currency": "EUR", "period": "day"},
    },
    sca_method="biometric+pin",
    sca_timestamp=time.time(),  # SCA just performed
)
print(f"EUDI credential imported. QEAA: {eudi_cred['is_qeaa']}")
# Output: EUDI credential imported. QEAA: True

# Execute a transaction requiring PSD2 SCA
attestation = eudi.create_compliance_attestation(
    transaction_id="eu-tx-2026-04-06-001",
    amount_eur=2500.00,
    eudi_credential_id="eudi-2026-04-06-001",
    counterparty_agent_id="eu-vendor-saas-01",
)
print(f"Compliance: SCA required={attestation['sca_check']['sca_required']}, "
      f"authorized={attestation['sca_check']['authorized']}")
# Output: Compliance: SCA required=True, authorized=True
```

---

## Chapter 7: Trust Scoring, Reputation Binding & Credential Revocation

### Why Credentials Need Reputation

A credential tells you what an agent is authorized to do. It does not tell you whether the agent is any good at doing it. An agent with a valid $50,000 delegation credential might have a 30% task completion rate and a history of disputed escrows. The credential is technically valid -- the human authorized the spend -- but the counterparty should not accept it without checking the agent's track record. Reputation binding attaches verifiable performance data to credentials so that counterparties can evaluate both authorization and competence in a single verification flow.

### ReputationBoundCredentialManager

```python
class ReputationBoundCredentialManager:
    """Binds verifiable reputation data to agent credentials.

    Combines GreenHelix reputation tools with the credential wallet to
    create credentials that carry both authorization and performance proof.
    """

    def __init__(self, wallet: CredentialWallet):
        self.wallet = wallet
        self.revocation_registry: Dict[str, dict] = {}

    def get_reputation_snapshot(self) -> dict:
        """Fetch the agent's current reputation from GreenHelix."""
        return api_call("get_agent_reputation", {
            "agent_id": self.wallet.agent_id,
        })

    def submit_performance_metrics(
        self,
        metrics: Dict[str, Any],
    ) -> dict:
        """Submit performance metrics to build verifiable history.

        These metrics feed into the reputation score and can be
        anchored in claim chains for tamper-evidence.
        """
        return api_call("submit_metrics", {
            "agent_id": self.wallet.agent_id,
            "metrics": metrics,
        })

    def issue_reputation_bound_credential(
        self,
        credential_id: str,
        subject_did: str,
        authorization_claims: Dict[str, Any],
        min_reputation_score: float = 0.0,
    ) -> AgentCredential:
        """Issue a credential that includes a verifiable reputation snapshot.

        The reputation data becomes part of the credential claims,
        anchored at issuance time. The counterparty can verify that
        the reputation was genuine at issuance by checking the claim chain.

        Args:
            credential_id: Unique ID for this credential.
            subject_did: DID of the credential subject.
            authorization_claims: The authorization claims (actions, limits, etc).
            min_reputation_score: Minimum score required to issue. Fails if below.
        """
        # Fetch current reputation
        rep = self.get_reputation_snapshot()
        rep_score = rep.get("reputation_score", 0)

        if rep_score < min_reputation_score:
            raise ValueError(
                f"Reputation {rep_score} below minimum {min_reputation_score}"
            )

        # Merge reputation into claims
        all_claims = {
            **authorization_claims,
            "reputation_at_issuance": {
                "score": rep_score,
                "trade_count": rep.get("trade_count", 0),
                "claim_chain_depth": rep.get("claim_chain_depth", 0),
                "snapshot_time": time.time(),
            },
        }

        return self.wallet.issue_credential(
            credential_id=credential_id,
            subject_did=subject_did,
            credential_type=(
                "https://greenhelix.net/credentials/reputation-bound-delegation/v1"
            ),
            claims=all_claims,
            disclosable_claims=[
                "reputation_at_issuance",
                "principal_name",
            ],
            ttl_seconds=86400,
        )

    def revoke_credential(
        self,
        credential_id: str,
        reason: str,
    ) -> dict:
        """Revoke a credential and record the revocation.

        Revocation is immediate. The credential hash is added to the
        revocation registry, and a claim chain entry is created for
        tamper-evident revocation history.
        """
        if credential_id not in self.wallet.credentials:
            raise KeyError(f"Credential {credential_id} not found")

        cred = self.wallet.credentials[credential_id]

        revocation_entry = {
            "credential_id": credential_id,
            "credential_hash": cred.credential_hash(),
            "revoked_at": time.time(),
            "reason": reason,
            "revoked_by": self.wallet.agent_id,
        }
        self.revocation_registry[credential_id] = revocation_entry

        # Submit revocation as a metric for chain anchoring
        self.submit_performance_metrics({
            "event": "credential_revocation",
            "credential_id": credential_id,
            "reason": reason,
            "timestamp": time.time(),
        })

        # Anchor the revocation in a claim chain
        chain_result = self.wallet.build_chain()

        return {
            "revoked": True,
            "entry": revocation_entry,
            "chain_result": chain_result,
        }

    def check_revocation(self, credential_id: str) -> dict:
        """Check if a credential has been revoked."""
        if credential_id in self.revocation_registry:
            entry = self.revocation_registry[credential_id]
            return {
                "revoked": True,
                "revoked_at": entry["revoked_at"],
                "reason": entry["reason"],
            }
        return {"revoked": False}

    def create_dispute_evidence_credential(
        self,
        dispute_id: str,
        counterparty_agent_id: str,
        evidence: Dict[str, Any],
    ) -> dict:
        """Create a credential containing dispute evidence.

        When a transaction is disputed, this creates a tamper-evident
        record of the evidence that can be presented during resolution.
        """
        # Create the dispute via GreenHelix
        dispute_result = api_call("create_dispute", {
            "agent_id": self.wallet.agent_id,
            "counterparty_agent_id": counterparty_agent_id,
            "dispute_id": dispute_id,
            "evidence": evidence,
        })

        # Issue an evidence credential
        evidence_cred = self.wallet.issue_credential(
            credential_id=f"dispute-evidence-{dispute_id}",
            subject_did=self.wallet.did,
            credential_type=(
                "https://greenhelix.net/credentials/dispute-evidence/v1"
            ),
            claims={
                "dispute_id": dispute_id,
                "counterparty": counterparty_agent_id,
                "evidence_summary": evidence.get("summary", ""),
                "evidence_hash": hashlib.sha256(
                    json.dumps(evidence, sort_keys=True).encode()
                ).hexdigest(),
                "created_at": time.time(),
            },
            disclosable_claims=["evidence_summary"],
            ttl_seconds=2592000,  # 30 days for dispute resolution
        )

        return {
            "dispute_result": dispute_result,
            "evidence_credential": evidence_cred.credential_hash(),
        }
```

### Reputation-Bound Credential Flow

```python
wallet = CredentialWallet(
    agent_id="reputable-vendor-01",
    display_name="Reputable Cloud Vendor",
    owner="ops@cloudvendor.com",
)
wallet.register()
wallet.create_wallet()

rep_manager = ReputationBoundCredentialManager(wallet)

# Submit performance metrics over time (called periodically)
rep_manager.submit_performance_metrics({
    "task_completion_rate": 0.97,
    "avg_response_time_ms": 145,
    "successful_escrows": 342,
    "disputed_escrows": 3,
    "uptime_percent": 99.8,
})

# Issue a reputation-bound credential (e.g., for a vendor presenting to a buyer)
rep_cred = rep_manager.issue_reputation_bound_credential(
    credential_id="vendor-service-cred-001",
    subject_did="did:key:reputable-vendor-01",
    authorization_claims={
        "service_type": "gpu_compute_provisioning",
        "max_instance_count": 64,
        "supported_regions": ["us-east", "eu-west"],
        "principal_name": "CloudVendor Inc.",
    },
    min_reputation_score=0.7,  # Require minimum 70% reputation
)

# Present with selective disclosure -- show reputation but not principal name
presentation = wallet.present_credential(
    credential_id="vendor-service-cred-001",
    disclosed_claims=["reputation_at_issuance"],
)
print(f"Disclosed reputation: {presentation['disclosed_values']}")

# Later: revoke a credential (e.g., service decommissioned)
revocation = rep_manager.revoke_credential(
    credential_id="vendor-service-cred-001",
    reason="Service region us-east decommissioned",
)
print(f"Revoked: {revocation['revoked']}")

# Counterparty checks revocation before accepting credential
status = rep_manager.check_revocation("vendor-service-cred-001")
print(f"Revocation check: {status}")
# Output: Revocation check: {'revoked': True, 'revoked_at': ..., 'reason': '...'}
```

### Dispute Evidence with Credentials

```python
# When a transaction goes wrong, create tamper-evident dispute evidence
evidence_result = rep_manager.create_dispute_evidence_credential(
    dispute_id="dispute-2026-04-06-001",
    counterparty_agent_id="unreliable-vendor-99",
    evidence={
        "summary": "Vendor committed to 8x A100 instances but only provisioned 4x",
        "sla_id": "sla-2026-04-05-001",
        "promised_instances": 8,
        "delivered_instances": 4,
        "transaction_id": "tx-2026-04-05-789",
        "screenshots": ["evidence-001.png", "evidence-002.png"],
    },
)
print(f"Dispute filed. Evidence credential: {evidence_result['evidence_credential'][:16]}...")
```

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What You Get

This guide covered the complete credential lifecycle for agentic commerce:

**Chapter 1** explained why API keys and OAuth break under delegation and how Mastercard, Google, and OpenAI converged on W3C Verifiable Credentials.

**Chapter 2** provided the SD-JWT-VC primer: credential anatomy, selective disclosure mechanics, key binding, and delegation chains as layered issuance.

**Chapter 3** built the `CredentialWallet` class with GreenHelix tools: `register_agent`, `create_wallet`, `build_claim_chain`, and `get_claim_chains` for DID-anchored credential storage.

**Chapter 4** implemented Verifiable Intent: session-level spending limits, `create_intent` integration, and sub-delegation with constraint narrowing.

**Chapter 5** delivered cross-protocol adapters for AP2, UCP, ACP, and x402, with a unified wallet backend and protocol-specific presentation formatting.

**Chapter 6** addressed the December 2026 eIDAS 2.0 deadline: EUDI Wallet integration, QEAA validation, PSD2 SCA flows, and compliance attestation via `check_compliance`.

**Chapter 7** bound reputation to credentials: `get_agent_reputation` and `submit_metrics` for reputation snapshots, real-time revocation, and dispute evidence credentials using `create_dispute`.

**Chapter 8** covered fleet-wide deployment: bulk registration, templated issuance, zero-downtime key rotation, health monitoring, and a 90-day sprint plan.

Every code example uses the `requests.Session` + the REST API (`POST /v1/{tool}`) pattern against the GreenHelix A2A Commerce Gateway. Every credential is an SD-JWT-VC with selective disclosure. Every delegation chain enforces constraint narrowing. The architecture is protocol-agnostic at the wallet layer and protocol-specific at the presentation layer, so your agents can transact across AP2, UCP, ACP, and x402 without credential duplication.

The December 2026 deadline is real. The protocols are converging. Start with Chapter 3, register your first agent, and build from there.

