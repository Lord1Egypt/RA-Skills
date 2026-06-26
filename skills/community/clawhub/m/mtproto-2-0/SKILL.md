---
name: mtproto-2.0
description: MTProto 2.0 protocol implementation guide for Telegram backend development. Use when implementing MTProto encryption, handshake, message serialization, or building Telegram-compatible servers. Covers DH key exchange, AES-256-IGE encryption, TL language, and security best practices.
version: 1.0.1
---

# MTProto 2.0 Protocol

Complete implementation guide for Telegram's MTProto 2.0 encryption protocol.

⚠️ **IMPORTANT SECURITY NOTICE**

This skill provides educational guidance on MTProto 2.0 protocol. Before using in production:

1. **Verify Auth Key ID size**: Ensure 8-byte alignment throughout your implementation
2. **Use crypto/rand**: Never use math/rand for cryptographic operations
3. **Test against official vectors**: Validate against Telegram's reference implementations
4. **Audit by experts**: Have cryptographers review before handling real keys
5. **Check off-by-one errors**: Carefully validate all buffer sizes and offsets

See [references/security-notice.md](references/security-notice.md) for detailed corrections.

## Quick Reference

### Core Components
- **Auth Key**: 256-bit symmetric key from DH exchange
- **Server Salt**: 64-bit anti-replay nonce
- **Message Key**: 128-bit message identifier
- **AES-256-IGE**: Encryption mode with error propagation

### When to Use

Use this skill when:
1. Implementing MTProto handshake (req_pq → req_DH_params → set_client_DH_params)
2. Encrypting/decrypting MTProto messages
3. Serializing TL objects
4. Building Telegram-compatible gateways
5. Debugging connection issues

## Handshake Flow

```
Client                              Server
  |                                    |
  | 1. req_pq                        |
  |----------------------------------->|
  |                                    |
  | 2. server_public_key_fingerprints|
  |<-----------------------------------|
  |                                    |
  | 3. req_DH_params                 |
  |----------------------------------->|
  |                                    |
  | 4. server_DH_params              |
  |<-----------------------------------|
  |                                    |
  | 5. set_client_DH_params          |
  |----------------------------------->|
  |                                    |
  | 6. dh_gen_ok                     |
  |<-----------------------------------|
```

See [references/handshake.md](references/handshake.md) for detailed implementation.

## Encryption

### AES-256-IGE Mode

```go
// Key derivation from Auth Key + Message Key
func deriveKeys(authKey, msgKey []byte) (aesKey, aesIV []byte) {
    x := sha256.Sum256(append(msgKey, authKey[:36]...))
    y := sha256.Sum256(append(authKey[40:76], msgKey...))
    
    aesKey = append(x[:8], y[8:24]...)
    aesIV = append(y[:8], x[24:32]...)
    return
}
```

See [references/encryption.md](references/encryption.md) for complete algorithm.

## Message Format

### Encrypted Message Structure

```
┌─────────────────────────────────────────────────────────┐
│ Auth Key ID     │ 8 bytes  │ SHA1(authKey)[96:128]      │
├─────────────────────────────────────────────────────────┤
│ Message Key     │ 16 bytes │ SHA256(plaintext)[8:24]    │
├─────────────────────────────────────────────────────────┤
│ Encrypted Data  │ Variable │ AES-256-IGE encrypted      │
└─────────────────────────────────────────────────────────┘
```

### Plaintext Structure

```
┌─────────────────────────────────────────────────────────┐
│ Salt            │ 8 bytes  │ Server Salt                │
├─────────────────────────────────────────────────────────┤
│ Session ID      │ 8 bytes  │ Unique session ID          │
├─────────────────────────────────────────────────────────┤
│ Message ID      │ 8 bytes  │ Timestamp + sequence       │
├─────────────────────────────────────────────────────────┤
│ Sequence No     │ 4 bytes  │ Packet sequence            │
├─────────────────────────────────────────────────────────┤
│ Length          │ 4 bytes  │ Message body length        │
├─────────────────────────────────────────────────────────┤
│ Message Body    │ Variable │ TL-serialized data         │
├─────────────────────────────────────────────────────────┤
│ Padding         │ 0-15 B   │ Random padding             │
└─────────────────────────────────────────────────────────┘
```

See [references/message-format.md](references/message-format.md) for details.

## TL Language

### Type Serialization

```tl
// Constructor with ID
user#938458c1 id:long first_name:string = User;

// Method definition
checkPhone#6fe51dfb phone_number:string = Bool;
```

See [references/tl-language.md](references/tl-language.md) for TL schema reference.

## Security Features

### Forward Secrecy
- Auth Key derived from ephemeral DH exchange
- Keys rotated periodically
- Old key compromise doesn't expose history

### Anti-Replay Protection
- Server Salt changes per connection
- Message ID includes timestamp
- Sequence number verification
- Time window validation

### Integrity Verification
- Message Key from SHA256 hash
- AES-IGE error propagation
- Length field validation

## Go Implementation

### Basic Connection

```go
type MTProtoConn struct {
    conn      net.Conn
    authKey   []byte
    salt      int64
    sessionID int64
    seqNo     int32
}

func (m *MTProtoConn) Send(msg TLObject) error {
    // 1. Serialize
    plaintext := msg.Encode()
    
    // 2. Calculate Message Key
    msgKey := calcMsgKey(plaintext, m.authKey)
    
    // 3. Derive AES keys
    aesKey, aesIV := deriveKeys(m.authKey, msgKey)
    
    // 4. Encrypt
    encrypted := encryptAESIGE(plaintext, aesKey, aesIV)
    
    // 5. Construct packet
    packet := constructPacket(m.authKey, msgKey, encrypted)
    
    // 6. Send
    _, err := m.conn.Write(packet)
    return err
}
```

## References

- [Handshake Details](references/handshake.md) - Complete DH exchange
- [Encryption Algorithm](references/encryption.md) - AES-256-IGE
- [Message Format](references/message-format.md) - Binary protocol
- [TL Language](references/tl-language.md) - Type serialization
- [⚠️ Security Notice](references/security-notice.md) - **CRITICAL FIXES FOR PRODUCTION**

## Official Resources

- [MTProto Official](https://core.telegram.org/mtproto)
- [TL Schema](https://core.telegram.org/schema)
- [Telegram API](https://core.telegram.org/api)
