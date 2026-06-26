---
name: identity-trust
display_name: Identity Trust
version: 1.0.0
author: ZhenStaff
category: security
description: Decentralized Identity (DID) and Verifiable Credentials management for AI Agents
tags: [did, identity, credentials, trust, w3c, blockchain, security, ai-agent, openclaw]
repository: https://github.com/ZhenRobotics/openclaw-identity-trust
license: MIT
---

# 🔐 Identity Trust Skill

Decentralized Identity (DID) and Verifiable Credentials management system for AI Agents, built on W3C DID Core and W3C Verifiable Credentials standards.

## 📋 Overview

Identity Trust provides a complete solution for decentralized identity management, enabling AI agents to:
- Create and manage Decentralized Identifiers (DIDs)
- Issue and verify W3C-compliant Verifiable Credentials
- Establish trust relationships between agents
- Manage cryptographic keys securely
- Store identity data locally with privacy

## 📦 Installation

### Step 1: Install the Package

**Option A: Via npm (Recommended)**

```bash
# Install globally for CLI access
npm install -g openclaw-identity-trust

# Verify installation
identity-trust --version
```

**Option B: From GitHub**

```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-identity-trust.git
cd openclaw-identity-trust

# Install dependencies
npm install

# Build
npm run build
```

### Step 2: Verify Installation

```bash
# Check CLI is working
identity-trust info

# Create your first DID
identity-trust did create
```

## 🚀 Usage

### When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `DID`, `verifiable credential`, `identity`, `trust`, `decentralized identity`
- Asks about creating or managing digital identities
- Needs to verify credentials or establish trust
- Wants to implement W3C DID/VC standards
- Building agent authentication systems

**TRIGGER EXAMPLES**:
- "Create a DID for my AI agent"
- "Issue a verifiable credential"
- "How do I verify this credential?"
- "Set up decentralized identity for authentication"
- "Evaluate trust level of this agent"

**DO NOT USE** when:
- Only general identity/password management (use password managers)
- OAuth/SAML authentication (use standard auth libraries)
- Simple user accounts (use traditional databases)

## 🎯 Core Features

### 1. DID Management
- **did:key** - Self-contained, no registry needed
- **did:web** - Web-hosted DIDs for public verification
- **did:ethr** - Ethereum-based DIDs (basic support)

### 2. Verifiable Credentials
- W3C VC Data Model 1.1 compliant
- Ed25519 and secp256k1 signatures
- Expiration date management
- Custom claims support

### 3. Trust Evaluation
- Policy-based trust scoring
- Credential verification
- Issuer trust chains
- Reputation systems

### 4. Security
- Ed25519 modern cryptography (default)
- secp256k1 Ethereum-compatible signatures
- Local key storage at `~/.openclaw/identity/`
- No external key dependencies

## 💻 Tools

This skill provides 6 core tools for AI agents:

### 1. `did_create` - Create Decentralized Identifiers

Create a new DID for an agent or entity.

**Parameters**:
- `method` (string, optional): DID method - `key`, `web`, or `ethr` (default: `key`)
- `keyType` (string, optional): Cryptographic key type - `Ed25519` or `secp256k1` (default: `Ed25519`)
- `save` (boolean, optional): Save to local storage (default: `true`)

**Returns**:
- `did` (string): The generated DID identifier
- `document` (object): Complete DID Document

**Example**:
```bash
identity-trust did create --method key --key-type Ed25519
```

### 2. `did_resolve` - Resolve DIDs to Documents

Resolve a DID to its DID Document.

**Parameters**:
- `did` (string, required): DID to resolve (e.g., `did:key:z6Mkf...`)

**Returns**:
- `document` (object): DID Document with verification methods

**Example**:
```bash
identity-trust did resolve did:key:z6MkfzZZD5gxQ...
```

### 3. `vc_issue` - Issue Verifiable Credentials

Issue a W3C-compliant verifiable credential.

**Parameters**:
- `issuerDid` (string, required): Issuer's DID
- `subjectDid` (string, required): Subject's DID
- `claims` (object, required): Claims to include in credential
- `type` (string, optional): Credential type (default: `VerifiableCredential`)
- `expirationDays` (number, optional): Expiration in days

**Returns**:
- `credential` (object): Signed verifiable credential

**Example**:
```bash
identity-trust vc issue \
  --issuer did:key:z6Mkf... \
  --subject did:key:z6Mkp... \
  --claims '{"role":"developer","level":"senior"}' \
  --expiration 90
```

### 4. `vc_verify` - Verify Credentials

Verify the authenticity and validity of a verifiable credential.

**Parameters**:
- `credential` (object, required): Credential to verify
- `checkExpiration` (boolean, optional): Check expiration date (default: `true`)

**Returns**:
- `verified` (boolean): Whether credential is valid
- `checks` (object): Detailed verification results

**Example**:
```bash
identity-trust vc verify <credential-id>
```

### 5. `identity_list` - List Identities

List all stored DIDs and credentials.

**Parameters**: None

**Returns**:
- `dids` (array): List of stored DIDs
- `credentials` (array): List of stored credentials

**Example**:
```bash
identity-trust did list
identity-trust vc list
```

### 6. `trust_evaluate` - Evaluate Agent Trust

Evaluate the trust level of an agent based on their credentials and policy.

**Parameters**:
- `agentDid` (string, required): Agent DID to evaluate
- `policy` (object, optional): Trust policy configuration

**Returns**:
- `trustLevel` (number): Trust score (0-100)
- `credentials` (array): Credentials used for evaluation
- `passed` (boolean): Whether agent meets policy requirements

**Example**:
```bash
# Programmatic usage
import { evaluateTrust } from 'openclaw-identity-trust';

const result = await evaluateTrust('did:key:z6Mkf...', {
  minimumTrustLevel: 60,
  requiredCredentials: ['IdentityCredential'],
  trustedIssuers: ['did:key:authority...']
});
```

## 📚 CLI Commands

Three command aliases available:
- `openclaw-identity-trust`
- `identity-trust`
- `idt`

### DID Commands

```bash
# Create a new DID
identity-trust did create [--method <key|web|ethr>] [--key-type <Ed25519|secp256k1>]

# Resolve a DID
identity-trust did resolve <did>

# List all DIDs
identity-trust did list
```

### Verifiable Credential Commands

```bash
# Issue a credential
identity-trust vc issue \
  --issuer <did> \
  --subject <did> \
  --claims '<json>' \
  [--type <type>] \
  [--expiration <days>]

# Verify a credential
identity-trust vc verify <credential-id-or-json>

# List credentials
identity-trust vc list [--subject <did>]
```

### Utility Commands

```bash
# Export all data
identity-trust export

# Show system information
identity-trust info
```

## 🔧 Programmatic API

Use as a Node.js library in your applications:

```typescript
import {
  generateDID,
  resolveDID,
  issueCredential,
  verifyCredential,
  LocalStorage
} from 'openclaw-identity-trust';

// Initialize storage
const storage = new LocalStorage();
await storage.initialize();

// Create a DID
const { did, document, keyPair } = await generateDID('key', {
  keyType: 'Ed25519'
});

console.log('Created DID:', did);

// Issue a credential
const credential = await issueCredential({
  issuerDid: 'did:key:issuer...',
  issuerKeyPair: keyPair,
  subjectDid: did,
  claims: {
    role: 'ai-agent',
    capabilities: ['read', 'write', 'execute']
  },
  expirationDate: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000)
});

// Verify credential
const result = await verifyCredential(credential, {
  checkExpiration: true,
  localStore: storage.getDIDStore()
});

console.log('Verified:', result.verified);
```

## 🎓 Use Cases

### 1. AI Agent Identity

Create persistent identities for AI agents:

```bash
# Create agent DID
identity-trust did create --method key

# Issue capability credential
identity-trust vc issue \
  --issuer did:key:authority... \
  --subject did:key:agent... \
  --claims '{"agent":"GPT-Agent-001","capabilities":["api_access","data_read"]}'
```

### 2. Service Authentication

Authenticate agents accessing services:

```typescript
const credential = await storage.getCredential(credentialId);
const result = await verifyCredential(credential);

if (result.verified) {
  // Grant access to service
  console.log('Access granted');
} else {
  console.log('Access denied:', result.error);
}
```

### 3. Trust Networks

Build trust relationships between agents:

```typescript
const trust = await evaluateTrust(agentDid, {
  minimumTrustLevel: 60,
  requiredCredentials: ['IdentityCredential', 'CapabilityCredential'],
  trustedIssuers: [authorityDid],
  allowExpired: false
});

if (trust.passed) {
  console.log(`Agent trusted with level: ${trust.trustLevel}%`);
}
```

## 📐 Technical Standards

This implementation follows:

- **W3C DID Core 1.0** - Decentralized Identifiers specification
- **W3C Verifiable Credentials Data Model 1.1** - Verifiable credentials standard
- **Ed25519 Signature 2020** - Modern cryptographic signatures
- **Multibase Encoding** - Base58btc encoding for did:key

## 🔒 Security

### Cryptography
- **Ed25519** - Modern elliptic curve signatures (default)
- **secp256k1** - Ethereum-compatible signatures
- **@noble/curves** - Audited cryptography library
- **@noble/hashes** - Secure hashing

### Key Storage
- Private keys stored locally at `~/.openclaw/identity/`
- No cloud storage or external dependencies
- User controls all cryptographic material

### Best Practices
1. Never share private keys
2. Always set expiration dates on credentials
3. Verify credentials before trusting
4. Use strong trust policies for critical operations
5. Rotate keys periodically

## 🛠️ Configuration

### Storage Location

Default: `~/.openclaw/identity/`

Structure:
```
~/.openclaw/identity/
├── dids.json          # Stored DID documents
├── credentials.json   # Issued/received credentials
└── keys.json          # Encrypted private keys
```

### Environment Variables

```bash
# Optional: Custom storage path
OPENCLAW_IDENTITY_PATH=/custom/path

# For did:web resolution (if using network)
OPENCLAW_IDENTITY_NETWORK_ENABLED=true
```

## 🐛 Troubleshooting

### Common Issues

**Problem**: `Error: Private key not found`
```bash
# Solution: Ensure DID was saved when created
identity-trust did create --save
```

**Problem**: `Error: Failed to resolve DID`
```bash
# Solution: Check DID format and network settings
identity-trust did resolve did:key:z6Mkf...
```

**Problem**: `Error: Signature verification failed`
```bash
# Solution: Check issuer DID and credential integrity
identity-trust vc verify --no-expiration <credential>
```

## 📖 Documentation

- **Full Documentation**: [README.md](https://github.com/ZhenRobotics/openclaw-identity-trust#readme)
- **Quick Start Guide**: [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/QUICKSTART.md)
- **API Reference**: [src/types.ts](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/src/types.ts)
- **GitHub**: https://github.com/ZhenRobotics/openclaw-identity-trust
- **npm Package**: https://www.npmjs.com/package/openclaw-identity-trust

## 🔄 Updates & Changelog

### v1.0.0 (2026-03-08)

Initial release with:
- DID generation and resolution (did:key, did:web, did:ethr)
- Verifiable Credential issuance and verification
- Trust evaluation system
- CLI tool with 3 command aliases
- Programmatic API
- Local storage with encryption
- W3C standards compliance

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/LICENSE)

## 🔗 Links

- **GitHub**: https://github.com/ZhenRobotics/openclaw-identity-trust
- **npm**: https://www.npmjs.com/package/openclaw-identity-trust
- **ClawHub**: https://clawhub.ai/ZhenStaff/identity-trust
- **Issues**: https://github.com/ZhenRobotics/openclaw-identity-trust/issues

## 💬 Support

- **Issues**: https://github.com/ZhenRobotics/openclaw-identity-trust/issues
- **Discussions**: https://github.com/ZhenRobotics/openclaw-identity-trust/discussions
- **Email**: support@zhenrobot.com

---

**Built with ❤️ for the OpenClaw ecosystem**
