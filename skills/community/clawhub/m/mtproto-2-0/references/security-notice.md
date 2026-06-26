# Security Notice & Corrections

⚠️ **CRITICAL ISSUES IDENTIFIED IN v1.0.0**

This document lists known issues and their corrections for production use.

## Issue 1: Auth Key ID Size Mismatch

### Problem
Original code returned 4 bytes, but MTProto protocol requires 8 bytes.

### Incorrect (v1.0.0)
```go
func calcAuthKeyID(authKey []byte) []byte {
    hash := sha1.Sum(authKey)
    return hash[12:16]  // ❌ Only 4 bytes!
}
```

### Correct
```go
func calcAuthKeyID(authKey []byte) []byte {
    hash := sha1.Sum(authKey)
    // Take lower 64 bits from SHA1
    authKeyID := make([]byte, 8)
    copy(authKeyID, hash[12:20])  // ✅ 8 bytes
    return authKeyID
}
```

## Issue 2: Using math/rand Instead of crypto/rand

### Problem
math/rand is NOT cryptographically secure and MUST NOT be used for:
- Nonce generation
- Key material
- Padding
- Session IDs

### Incorrect
```go
import "math/rand"

nonce := make([]byte, 16)
rand.Read(nonce)  // ❌ Not secure!
```

### Correct
```go
import "crypto/rand"

nonce := make([]byte, 16)
_, err := rand.Read(nonce)  // ✅ Cryptographically secure
if err != nil {
    panic(err)
}
```

## Issue 3: Padding Generation

### Incorrect
```go
padding := make([]byte, rand.Intn(16))  // ❌ math/rand
rand.Read(padding)
```

### Correct
```go
import "crypto/rand"

paddingSize := 0
binary.Read(rand.Reader, binary.LittleEndian, &paddingSize)
paddingSize = paddingSize % 16

padding := make([]byte, paddingSize)
_, err := rand.Read(padding)
if err != nil {
    panic(err)
}
```

## Issue 4: Off-By-One Errors in Message Format

### Problem
Confusion between length-in-words vs length-in-bytes.

### Header Structure (CORRECT)
```
Auth Key ID:     8 bytes
Message Key:     16 bytes
Encrypted Data:  variable (must be multiple of 16)

Total header: 24 bytes
```

### Plaintext Structure (CORRECT)
```
Salt:            8 bytes
Session ID:      8 bytes
Message ID:      8 bytes
Sequence Number: 4 bytes
Length:          4 bytes  (in 4-byte words!)
Message Body:    variable
Padding:         0-15 bytes (to align to 16)
```

### Important: Length Field
```go
// Length is in 4-byte words, not bytes!
lengthInWords := uint32(len(bodyWithPadding)) / 4
```

## Issue 5: Session ID Generation

### Incorrect
```go
sessionID := rand.Int63()  // ❌ math/rand
```

### Correct
```go
sessionIDBytes := make([]byte, 8)
_, err := rand.Read(sessionIDBytes)
if err != nil {
    panic(err)
}
sessionID := int64(binary.LittleEndian.Uint64(sessionIDBytes))
```

## Issue 6: DH Private Key Generation

### Incorrect
```go
b := make([]byte, 256)
rand.Read(b)  // ❌ math/rand
```

### Correct
```go
import (
    "crypto/rand"
    "math/big"
)

// Generate private key in range [1, p-1]
b, err := rand.Int(rand.Reader, new(big.Int).Sub(p, big.NewInt(1)))
if err != nil {
    panic(err)
}
b.Add(b, big.NewInt(1))  // Ensure b >= 1
```

## Production Checklist

Before deploying to production:

- [ ] Replace ALL `math/rand` with `crypto/rand`
- [ ] Verify Auth Key ID is 8 bytes everywhere
- [ ] Test against Telegram's official reference vectors
- [ ] Validate all buffer sizes match protocol spec
- [ ] Run constant-time comparison for MAC verification
- [ ] Implement proper error handling (no panic in production)
- [ ] Add comprehensive logging (without leaking keys)
- [ ] Have security audit by experienced cryptographer

## Testing Against Official Vectors

```go
// Official test vectors from Telegram
func TestOfficialVectors(t *testing.T) {
    // Auth Key ID test
    authKey := hexToBytes("...")
    expectedID := hexToBytes("...")
    
    actualID := calcAuthKeyID(authKey)
    if !bytes.Equal(actualID, expectedID) {
        t.Errorf("Auth Key ID mismatch")
    }
    
    // Message Key test
    plaintext := hexToBytes("...")
    expectedMsgKey := hexToBytes("...")
    
    actualMsgKey := calcMsgKey(plaintext, authKey)
    if !bytes.Equal(actualMsgKey, expectedMsgKey) {
        t.Errorf("Message Key mismatch")
    }
}
```

## References

- [Telegram MTProto Docs](https://core.telegram.org/mtproto)
- [Go crypto/rand Package](https://golang.org/pkg/crypto/rand/)
- [Constant Time Comparison](https://pkg.go.dev/crypto/subtle#ConstantTimeCompare)

## Disclaimer

This skill is for educational purposes. The code examples illustrate protocol concepts but may contain errors. ALWAYS:

1. Verify against official Telegram documentation
2. Test with official reference implementations
3. Have security experts review before production use
4. Never use example code directly in production

Report issues: https://clawhub.ai/skills/mtproto-2-0
