# AES-256-IGE Encryption

MTProto's custom encryption mode implementation.

## Overview

**IGE** (Infinite Garble Extension) is a block cipher mode that:
- Propagates errors throughout the message
- Is self-synchronizing
- Provides integrity checking through error propagation

## Algorithm

### Basic Principle

```
For each block i:
    x_i = AES(x_{i-1} XOR plaintext_i) XOR y_{i-1}
    
Where:
    x_i = ciphertext block i
    y_i = plaintext block i
    x_{i-1} = previous ciphertext block (or IV part 1)
    y_{i-1} = previous plaintext block (or IV part 2)
```

### Encryption

```go
func encryptAESIGE(plaintext, key, iv []byte) []byte {
    block, _ := aes.NewCipher(key) // AES-256
    
    // IGE requires two IV blocks
    x := iv[:16]   // x_{-1}
    y := iv[16:]   // y_{-1}
    
    ciphertext := make([]byte, len(plaintext))
    
    for i := 0; i < len(plaintext); i += 16 {
        // Current plaintext block
        plainBlock := plaintext[i : i+16]
        
        // x_i = AES(x_{i-1} XOR plain_i)
        tmp := xor(x, plainBlock)
        encrypted := make([]byte, 16)
        block.Encrypt(encrypted, tmp)
        
        // x_i = encrypted XOR y_{i-1}
        x = xor(encrypted, y)
        
        copy(ciphertext[i:], x)
        y = plainBlock
    }
    
    return ciphertext
}
```

### Decryption

```go
func decryptAESIGE(ciphertext, key, iv []byte) ([]byte, error) {
    block, _ := aes.NewCipher(key)
    
    x := iv[:16]   // x_{-1}
    y := iv[16:]   // y_{-1}
    
    plaintext := make([]byte, len(ciphertext))
    
    for i := 0; i < len(ciphertext); i += 16 {
        // Current ciphertext block
        cipherBlock := ciphertext[i : i+16]
        
        // y_i = AES^{-1}(cipher_i XOR y_{i-1}) XOR x_{i-1}
        tmp := xor(cipherBlock, y)
        decrypted := make([]byte, 16)
        block.Decrypt(decrypted, tmp)
        
        y = xor(decrypted, x)
        
        copy(plaintext[i:], y)
        x = cipherBlock
    }
    
    return plaintext, nil
}
```

## Key Derivation

### From Auth Key and Message Key

```go
func deriveKeys(authKey, msgKey []byte) (aesKey, aesIV []byte) {
    // SHA256(msg_key + auth_key[:36])
    x := sha256.Sum256(append(msgKey, authKey[:36]...))
    
    // SHA256(auth_key[40:76] + msg_key)
    y := sha256.Sum256(append(authKey[40:76], msgKey...))
    
    // aes_key = x[:8] + y[8:24]
    aesKey = make([]byte, 32)
    copy(aesKey[0:8], x[0:8])
    copy(aesKey[8:24], y[8:24])
    
    // aes_iv = y[:8] + x[24:32]
    aesIV = make([]byte, 32)
    copy(aesIV[0:8], y[0:8])
    copy(aesIV[8:16], x[24:32])
    
    return
}
```

### From New Nonce and Server Nonce (Temp Keys)

```go
func generateTempKeys(newNonce, serverNonce []byte) (key, iv []byte) {
    // SHA1(new_nonce + server_nonce)
    hash1 := sha1.Sum(append(newNonce, serverNonce...))
    
    // SHA1(server_nonce + new_nonce)
    hash2 := sha1.Sum(append(serverNonce, newNonce...))
    
    // SHA1(new_nonce + new_nonce)
    hash3 := sha1.Sum(append(newNonce, newNonce...))
    
    // Key = hash1 + hash2[:12]
    key = make([]byte, 32)
    copy(key[0:20], hash1[:])
    copy(key[20:32], hash2[0:12])
    
    // IV = hash2[12:20] + hash3 + 0x00...0x00
    iv = make([]byte, 32)
    copy(iv[0:8], hash2[12:20])
    copy(iv[8:28], hash3[:])
    // Last 4 bytes are zeros
    
    return
}
```

## Helper Functions

### XOR Operation

```go
func xor(a, b []byte) []byte {
    result := make([]byte, len(a))
    for i := range a {
        result[i] = a[i] ^ b[i]
    }
    return result
}
```

### PKCS7 Padding

```go
func pkcs7Pad(data []byte, blockSize int) []byte {
    padding := blockSize - len(data)%blockSize
    padtext := bytes.Repeat([]byte{byte(padding)}, padding)
    return append(data, padtext...)
}

func pkcs7Unpad(data []byte) ([]byte, error) {
    if len(data) == 0 {
        return nil, errors.New("empty data")
    }
    padding := int(data[len(data)-1])
    if padding > len(data) || padding == 0 {
        return nil, errors.New("invalid padding")
    }
    return data[:len(data)-padding], nil
}
```

## Complete Encryption Flow

```go
func encryptMessage(plaintext, authKey []byte) ([]byte, error) {
    // 1. Add random padding (0-15 bytes)
    padding := generateRandom(rand.Intn(16))
    plaintext = append(plaintext, padding...)
    
    // 2. Calculate message key
    msgKey := calcMsgKey(plaintext, authKey)
    
    // 3. Derive AES keys
    aesKey, aesIV := deriveKeys(authKey, msgKey)
    
    // 4. Encrypt
    ciphertext := encryptAESIGE(plaintext, aesKey, aesIV)
    
    // 5. Construct final message
    authKeyID := calcAuthKeyID(authKey)
    
    result := make([]byte, 8+16+len(ciphertext))
    copy(result[0:8], authKeyID)
    copy(result[8:24], msgKey)
    copy(result[24:], ciphertext)
    
    return result, nil
}
```

## Security Properties

### Error Propagation

If one ciphertext block is corrupted:
- That plaintext block is completely garbled
- The next plaintext block has bit errors at the same positions
- All subsequent blocks are completely garbled

```
Corrupted block i:
- plaintext_i: completely random
- plaintext_{i+1}: XOR with error pattern
- plaintext_{i+2...}: completely garbled
```

### Self-Synchronization

After corruption, the cipher resynchronizes after 2 blocks:
```
Block i:   corrupted
Block i+1: corrupted (with error pattern)
Block i+2: correct decryption resumes
```

## Comparison with Other Modes

| Mode | Error Propagation | Parallelizable | Integrity |
|------|------------------|----------------|-----------|
| CBC  | 2 blocks         | Decrypt only   | No        |
| CTR  | 1 bit            | Yes            | No        |
| GCM  | Complete message | Yes            | Yes       |
| **IGE** | **All remaining** | **No** | **Partial** |

## Common Mistakes

### 1. Wrong IV Size

```go
// Wrong - using 16-byte IV
iv := make([]byte, 16)

// Correct - using 32-byte IV
iv := make([]byte, 32)
```

### 2. Reusing IV

```go
// Wrong - same IV for multiple messages
ciphertext1 := encryptAESIGE(plaintext1, key, iv)
ciphertext2 := encryptAESIGE(plaintext2, key, iv) // Don't do this!

// Correct - unique IV per message
```

### 3. Not Checking Plaintext Length

```go
// Wrong - not padding
if len(plaintext)%16 != 0 {
    panic("plaintext not aligned")
}

// Correct - always pad
plaintext = pkcs7Pad(plaintext, 16)
```

## Testing

### Test Vectors

```go
func TestAESIGE(t *testing.T) {
    key := make([]byte, 32)
    iv := make([]byte, 32)
    plaintext := []byte("Hello, MTProto!")
    
    // Pad plaintext
    plaintext = pkcs7Pad(plaintext, 16)
    
    // Encrypt
    ciphertext := encryptAESIGE(plaintext, key, iv)
    
    // Decrypt
    decrypted, err := decryptAESIGE(ciphertext, key, iv)
    if err != nil {
        t.Fatal(err)
    }
    
    // Unpad
    decrypted, err = pkcs7Unpad(decrypted)
    if err != nil {
        t.Fatal(err)
    }
    
    // Verify
    if !bytes.Equal(plaintext[:len(plaintext)-16+len("Hello, MTProto!")], decrypted) {
        t.Fatal("decryption failed")
    }
}
```

## Performance Considerations

### Not Parallelizable

IGE cannot be parallelized - each block depends on the previous:
```
Block 0: depends on IV
Block 1: depends on Block 0
Block 2: depends on Block 1
...
```

### Use Hardware AES

Go's crypto/aes automatically uses AES-NI when available:
```go
import _ "crypto/aes"
// Automatically uses hardware acceleration
```

### For Large Messages

Consider chunking for very large messages (>1MB):
```go
const maxChunkSize = 65536  // 64KB chunks

for i := 0; i < len(plaintext); i += maxChunkSize {
    end := min(i+maxChunkSize, len(plaintext))
    chunk := plaintext[i:end]
    // Encrypt chunk
}
```
