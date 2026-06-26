# MTProto 2.0 Handshake Protocol

Complete DH key exchange implementation.

## Overview

The handshake establishes a shared 256-bit Auth Key using Diffie-Hellman key exchange over RSA-encrypted channels.

## Step-by-Step Implementation

### Step 1: req_pq

**Client Request:**
```go
type ReqPq struct {
    Nonce [16]byte  // 128-bit random
}

func (c *Client) reqPq() (*ResPq, error) {
    req := &ReqPq{
        Nonce: generateNonce(16),
    }
    return c.send(req)
}
```

**Server Response:**
```go
type ResPq struct {
    Nonce                    [16]byte
    ServerNonce              [16]byte
    Pq                       []byte  // pq = p * q (two primes)
    ServerPublicKeyFingerprints []int64
}
```

### Step 2: req_DH_params

**Factorize pq:**
```go
func factorize(pq []byte) (p, q []byte) {
    // Use Pollard's rho or trial division
    // Return p < q
}
```

**Generate new_nonce:**
```go
newNonce := generateNonce(32)  // 256-bit
```

**Encrypt with RSA:**
```go
data := &P_q_inner_data{
    Pq:        pq,
    P:         p,
    Q:         q,
    Nonce:     req.Nonce,
    ServerNonce: res.ServerNonce,
    NewNonce:  newNonce,
}

encrypted := rsaEncrypt(data.Encode(), serverPublicKey)
```

**Send request:**
```go
type ReqDHParams struct {
    Nonce                    [16]byte
    ServerNonce              [16]byte
    P                        []byte
    Q                        []byte
    PublicKeyFingerprint     int64
    EncryptedData            []byte
}
```

### Step 3: server_DH_params

**Server Response:**
```go
type ServerDHParamsOk struct {
    Nonce         [16]byte
    ServerNonce   [16]byte
    EncryptedAnswer []byte  // Contains Server_DH_inner_data
}

// Decrypted data contains:
type ServerDHInnerData struct {
    Nonce       [16]byte
    ServerNonce [16]byte
    G           int32   // Generator
    DHPrime     []byte  // Safe prime
    GA          []byte  // g^a mod p
    ServerTime  int32
}
```

### Step 4: set_client_DH_params

**Generate b and compute gb:**
```go
// Random b (2048 bits)
b := generateRandom(256)

// gb = g^b mod dh_prime
gb := new(big.Int).Exp(
    big.NewInt(int64(serverData.G)),
    new(big.Int).SetBytes(b),
    new(big.Int).SetBytes(serverData.DHPrime),
).Bytes()
```

**Compute Auth Key:**
```go
// auth_key = (g^a)^b mod p = g^(ab) mod p
authKey := new(big.Int).Exp(
    new(big.Int).SetBytes(serverData.GA),
    new(big.Int).SetBytes(b),
    new(big.Int).SetBytes(serverData.DHPrime),
).Bytes()
```

**Compute key identifier:**
```go
// auth_key_aux_hash = SHA1(auth_key)[0:8]
// auth_key_id = auth_key_aux_hash XOR new_nonce[0:8]
```

**Send confirmation:**
```go
data := &ClientDHInnerData{
    Nonce:       nonce,
    ServerNonce: serverNonce,
    GB:          gb,
}

encrypted := encryptAES(data.Encode(), tmpKey, tmpIV)

req := &SetClientDHParams{
    Nonce:         nonce,
    ServerNonce:   serverNonce,
    EncryptedData: encrypted,
}
```

### Step 5: dh_gen_ok

**Server Response:**
```go
type DhGenOk struct {
    Nonce         [16]byte
    ServerNonce   [16]byte
    NewNonceHash1 [16]byte  // SHA1(new_nonce + auth_key)[4:20]
}
```

**Verify:**
```go
expectedHash := sha1.Sum(append(newNonce, authKey...))
if !bytes.Equal(newNonceHash1, expectedHash[4:20]) {
    return errors.New("handshake verification failed")
}
```

## Security Considerations

### Prime Verification

Always verify DH parameters:
```go
func verifyDHParams(g int32, p []byte) error {
    pInt := new(big.Int).SetBytes(p)
    
    // 1. p is prime
    if !pInt.ProbablyPrime(20) {
        return errors.New("p is not prime")
    }
    
    // 2. (p-1)/2 is prime (safe prime)
    q := new(big.Int).Div(new(big.Int).Sub(pInt, big.NewInt(1)), big.NewInt(2))
    if !q.ProbablyPrime(20) {
        return errors.New("(p-1)/2 is not prime")
    }
    
    // 3. 2^2047 <= p < 2^2048
    if pInt.BitLen() != 2048 {
        return errors.New("p is not 2048 bits")
    }
    
    // 4. g is generator
    if g != 2 && g != 3 && g != 4 && g != 5 && g != 6 && g != 7 {
        return errors.New("invalid generator")
    }
    
    return nil
}
```

### Replay Protection

```go
// Server must validate:
// 1. nonce matches req_pq
// 2. server_nonce is one we generated
// 3. new_nonce is fresh (not seen before)
```

## Error Handling

### dh_gen_retry

When server asks client to retry with different parameters:
```go
type DhGenRetry struct {
    Nonce         [16]byte
    ServerNonce   [16]byte
    NewNonceHash2 [16]byte
}

// Client should retry with different b
```

### dh_gen_fail

When handshake fails:
```go
type DhGenFail struct {
    Nonce         [16]byte
    ServerNonce   [16]byte
    NewNonceHash3 [16]byte
}
```

## Go Implementation Example

```go
func (c *Client) performHandshake() ([]byte, error) {
    // Step 1: req_pq
    resPQ, err := c.reqPq()
    if err != nil {
        return nil, err
    }
    
    // Step 2: req_DH_params
    p, q := factorize(resPQ.Pq)
    newNonce := generateNonce(32)
    
    innerData := &P_q_inner_data{
        Pq:          resPQ.Pq,
        P:           p,
        Q:           q,
        Nonce:       resPQ.Nonce,
        ServerNonce: resPQ.ServerNonce,
        NewNonce:    newNonce,
    }
    
    serverKey := c.getServerKey(resPQ.ServerPublicKeyFingerprints[0])
    encrypted := rsa.EncryptOAEP(sha256.New(), rand.Reader, serverKey, innerData.Encode(), nil)
    
    reqDH := &ReqDHParams{
        Nonce:                resPQ.Nonce,
        ServerNonce:          resPQ.ServerNonce,
        P:                    p,
        Q:                    q,
        PublicKeyFingerprint: resPQ.ServerPublicKeyFingerprints[0],
        EncryptedData:        encrypted,
    }
    
    serverDH, err := c.reqDHParams(reqDH)
    if err != nil {
        return nil, err
    }
    
    // Step 3: Decrypt server_DH_params
    tmpKey, tmpIV := generateTempKeys(newNonce, serverDH.ServerNonce)
    decrypted := decryptAES(serverDH.EncryptedAnswer, tmpKey, tmpIV)
    serverDHInner := &ServerDHInnerData{}
    serverDHInner.Decode(decrypted)
    
    // Verify DH params
    if err := verifyDHParams(serverDHInner.G, serverDHInner.DHPrime); err != nil {
        return nil, err
    }
    
    // Step 4: set_client_DH_params
    b := generateRandom(256)
    gb := modExp(serverDHInner.G, b, serverDHInner.DHPrime)
    authKey := modExp(serverDHInner.GA, b, serverDHInner.DHPrime)
    
    clientDHInner := &ClientDHInnerData{
        Nonce:       resPQ.Nonce,
        ServerNonce: resPQ.ServerNonce,
        GB:          gb,
    }
    
    encryptedClientDH := encryptAES(clientDHInner.Encode(), tmpKey, tmpIV)
    
    setDH := &SetClientDHParams{
        Nonce:         resPQ.Nonce,
        ServerNonce:   resPQ.ServerNonce,
        EncryptedData: encryptedClientDH,
    }
    
    dhGenOk, err := c.setClientDHParams(setDH)
    if err != nil {
        return nil, err
    }
    
    // Step 5: Verify
    expectedHash := sha1.Sum(append(newNonce, authKey...))
    if !bytes.Equal(dhGenOk.NewNonceHash1, expectedHash[4:20]) {
        return nil, errors.New("handshake verification failed")
    }
    
    return authKey, nil
}
```
