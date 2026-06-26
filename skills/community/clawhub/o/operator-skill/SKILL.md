# Skill Operator (PassDeck)

The Skill Operator serves as the orchestration and orchestration engine for collaborative agent sessions. It provides high-performance persistence using Loro-CRDT with an append-only log architecture, ensuring that data is never lost and remains consistent across all agents.

## 💾 Core Actions

### `team.create`
- **Description**: Initializes a new persistent collaborative session on disk. Creates the initial snapshot and metadata.
- **Parameters**: `{ taskName: string }`
- **Output**: `{ sessionId: string, status: 'Persisted' }`

### `team.sync`
- **Description**: Securely appends an incremental CRDT update to the session log. Every update is verified using Ed25519 signatures from the originating agent before persistence.
- **Parameters**: `{ sessionId: string, updatePayload: base64, publicKeyHex: string, signatureHex: string }`
- **Output**: `{ success: true, version: string }`

### `team.load`
- **Description**: Recovers the full state of a collaborative session by merging the base snapshot with the incremental update log. Provides a "crash-proof" state recovery mechanism.
- **Parameters**: `{ sessionId: string }`
- **Output**: `{ payload: base64, format: 'full-merged-snapshot' }`

## 🛡️ Key Features
- **Performance**: O(1) incremental sync performance.
- **Fault-Tolerance**: Instant crash recovery via Snapshot + WAL (Write-Ahead Logging).
- **Security**: Built-in Ed25519 signature verification for every sync operation.
