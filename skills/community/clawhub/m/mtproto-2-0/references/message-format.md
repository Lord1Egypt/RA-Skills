# MTProto Message Format

Binary protocol structure for encrypted messages.

## Encrypted Message Structure

```
┌─────────────────────────────────────────────────────────┐
│ Auth Key ID     │ 8 bytes  │ SHA1(authKey)[96:128]      │
├─────────────────────────────────────────────────────────┤
│ Message Key     │ 16 bytes │ SHA256(plaintext)[8:24]    │
├─────────────────────────────────────────────────────────┤
│ Encrypted Data  │ Variable │ AES-256-IGE encrypted      │
└─────────────────────────────────────────────────────────┘

Total: 24 bytes header + encrypted payload
```

## Auth Key ID

⚠️ **CRITICAL**: Auth Key ID is **8 bytes** (64 bits), not 4 bytes.

```go
func calcAuthKeyID(authKey []byte) []byte {
    // SHA1(auth_key)[96:128] bits = [12:16] bytes = 4 bytes
    // But MTProto expects 8 bytes, so we pad or use full 64-bit
    
    // CORRECT: Use 64-bit from SHA1
    hash := sha1.Sum(authKey)
    authKeyID := make([]byte, 8)
    copy(authKeyID[0:4], hash[12:16])  // Lower 32 bits
    // Upper 32 bits can be zero or derived from additional hash
    return authKeyID
}

// Alternative: Use SHA256 and take first 8 bytes
func calcAuthKeyIDSecure(authKey []byte) []byte {
    hash := sha256.Sum256(authKey)
    return hash[0:8]  // First 8 bytes
}
```

**Purpose**: 
- Identifies which auth_key was used
- Server can quickly find the correct key
- **MUST be 8 bytes** in the encrypted message header

## Message Key

```go
func calcMsgKey(plaintext, authKey []byte) []byte {
    // SHA256(plaintext + auth_key)[8:24]
    data := append(plaintext, authKey...)
    hash := sha256.Sum256(data)
    return hash[8:24]  // Middle 16 bytes
}
```

**Purpose**:
- Message integrity verification
- IV generation for AES-IGE
- Duplicate message detection

## Plaintext Structure

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ Salt            │ 8 bytes  │ Server salt                │
├─────────────────────────────────────────────────────────┤
│ Session ID      │ 8 bytes  │ Unique session identifier  │
├─────────────────────────────────────────────────────────┤
│ Message ID      │ 8 bytes  │ Timestamp + sequence       │
├─────────────────────────────────────────────────────────┤
│ Sequence Number │ 4 bytes  │ Packet sequence            │
├─────────────────────────────────────────────────────────┤
│ Length          │ 4 bytes  │ Message body length        │
├─────────────────────────────────────────────────────────┤
│ Message Body    │ Variable │ TL-serialized data         │
├─────────────────────────────────────────────────────────┤
│ Padding         │ 0-15 B   │ Random padding             │
└─────────────────────────────────────────────────────────┘
```

### Salt (8 bytes)

```go
type Salt struct {
    Value int64
}

// Server provides salt during handshake
// Client must include current salt in every message
// Salt changes periodically (every 1 hour typically)
```

**Anti-replay protection**:
- Server validates salt is recent
- Old salts are rejected

### Session ID (8 bytes)

```go
sessionID := generateRandom(8)  // 64-bit random
```

**Purpose**:
- Identifies connection session
- Multiple sessions per auth_key
- Session-specific state

### Message ID (8 bytes)

```go
// Structure (64 bits):
// | 32-bit timestamp (seconds) | 1-bit direction | 31-bit sequence |
// Or alternatively:
// | 32-bit timestamp | 32-bit counter |

func generateMessageID() int64 {
    now := time.Now().Unix()
    // Use high bits for timestamp
    // Low bits for sequence counter
    return (now << 32) | atomic.AddInt32(&counter, 1)
}
```

**Rules**:
- Must be strictly increasing per session
- Time-based component prevents replay
- Direction bit distinguishes client/server

### Sequence Number (4 bytes)

```go
type SeqNo struct {
    Value int32
}

// Even numbers: container or content-related
// Odd numbers:  RPC call
```

**Even seqno**:
- 0, 2, 4, 6... for containers
- Messages requiring acknowledgment

**Odd seqno**:
- 1, 3, 5, 7... for RPC calls
- Methods requiring response

### Length (4 bytes)

```go
length := uint32(len(messageBody)) / 4  // Length in 4-byte words
```

**Note**: Length is in 4-byte words, not bytes!

### Message Body

TL-serialized object:
```
┌─────────────────────────────────────────────────────────┐
│ Constructor ID  │ 4 bytes  │ Object type identifier     │
├─────────────────────────────────────────────────────────┤
│ Fields          │ Variable │ Serialized field values    │
└─────────────────────────────────────────────────────────┘
```

Example:
```go
// messages.sendMessage#520c3870 flags:# ... = Updates;
// Constructor ID: 0x520c3870

msg := &mtproto.TLMessagesSendMessage{
    Peer:     peer,
    Message:  "Hello",
    RandomId: rand.Int63(),
}

body := msg.Encode()
// [0x70, 0x38, 0x0c, 0x52, ...]  // Little-endian constructor ID
```

### Padding (0-15 bytes)

```go
padding := make([]byte, rand.Intn(16))  // 0-15 random bytes
rand.Read(padding)
```

**Purpose**:
- Obscure message length
- Prevent traffic analysis
- Must be stripped during decryption

## Container Messages

For batching multiple messages:

```go
type MsgContainer struct {
    Messages []*Message
}

// Structure:
// 0x73f1f8dc (container constructor)
// count: int32
// messages: [Message, Message, ...]

type Message struct {
    MsgID    int64
    SeqNo    int32
    Bytes    int32  // Body length in bytes
    Body     []byte // Serialized TL object
}
```

## Go Implementation

```go
func constructPlaintext(salt, sessionID int64, seqNo int32, body []byte) []byte {
    // Calculate padding
    baseSize := 8 + 8 + 8 + 4 + 4 + len(body)  // Without padding
    paddingSize := (16 - (baseSize % 16)) % 16   // Align to 16 bytes
    padding := generateRandom(paddingSize)
    
    // Build plaintext
    plaintext := make([]byte, 0, baseSize+paddingSize)
    
    // Salt
    plaintext = append(plaintext, int64ToBytes(salt)...)
    
    // Session ID
    plaintext = append(plaintext, int64ToBytes(sessionID)...)
    
    // Message ID
    msgID := generateMessageID()
    plaintext = append(plaintext, int64ToBytes(msgID)...)
    
    // Sequence Number
    plaintext = append(plaintext, int32ToBytes(seqNo)...)
    
    // Length (in 4-byte words)
    length := uint32(len(body) + len(padding)) / 4
    plaintext = append(plaintext, int32ToBytes(int32(length))...)
    
    // Body
    plaintext = append(plaintext, body...)
    
    // Padding
    plaintext = append(plaintext, padding...)
    
    return plaintext
}

func parsePlaintext(plaintext []byte) (*MessageInfo, []byte, error) {
    if len(plaintext) < 32 {
        return nil, nil, errors.New("plaintext too short")
    }
    
    msg := &MessageInfo{}
    
    // Salt
    msg.Salt = bytesToInt64(plaintext[0:8])
    
    // Session ID
    msg.SessionID = bytesToInt64(plaintext[8:16])
    
    // Message ID
    msg.MessageID = bytesToInt64(plaintext[16:24])
    
    // Sequence Number
    msg.SeqNo = bytesToInt32(plaintext[24:28])
    
    // Length
    length := bytesToInt32(plaintext[28:32]) * 4  // Convert to bytes
    
    // Body + Padding
    if int(32+length) > len(plaintext) {
        return nil, nil, errors.New("invalid length")
    }
    
    bodyWithPadding := plaintext[32 : 32+length]
    
    // Strip padding (find actual body length from TL)
    body := stripPadding(bodyWithPadding)
    
    return msg, body, nil
}
```

## Validation Rules

### Server-Side Validation

```go
func validateMessage(msg *MessageInfo) error {
    // 1. Salt must be recent
    if !isValidSalt(msg.Salt) {
        return errors.New("invalid salt")
    }
    
    // 2. Message ID must increase
    if msg.MessageID <= lastMessageID {
        return errors.New("message ID too old")
    }
    
    // 3. Time window (±5 minutes)
    msgTime := msg.MessageID >> 32
    now := time.Now().Unix()
    if abs(now-msgTime) > 300 {
        return errors.New("message outside time window")
    }
    
    // 4. Sequence number parity
    if msg.SeqNo%2 != expectedParity {
        return errors.New("invalid sequence number parity")
    }
    
    return nil
}
```

## Message Acknowledgment

### ACK Message

```go
// msgs_ack#62d6b459 msg_ids:Vector<long> = MsgsAck;

ack := &mtproto.TLMsgsAck{
    MsgIds: []int64{msgID1, msgID2, msgID3},
}
```

### RPC Result

```go
// rpc_result#f35c6d01 req_msg_id:long result:Object = RpcResult;

result := &mtproto.TLRpcResult{
    ReqMsgId: requestMsgID,
    Result:   response,
}
```

## Common Issues

### 1. Alignment Errors

```go
// Wrong - not aligned to 16 bytes
plaintext := make([]byte, 30)  // Not divisible by 16!

// Correct
plaintext := make([]byte, 32)  // Divisible by 16
```

### 2. Wrong Length Encoding

```go
// Wrong - length in bytes
length := uint32(len(body))

// Correct - length in 4-byte words
length := uint32(len(body)) / 4
```

### 3. Session Confusion

```go
// Wrong - using wrong session ID
msg.SessionID = session1.ID

// But encrypting with session2's auth key!
ciphertext := encrypt(msg, session2.AuthKey)

// Correct - always match session and auth key
```
