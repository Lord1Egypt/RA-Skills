# TL Language (Type Language)

Telegram's binary serialization format.

## Overview

TL is a compact, type-safe binary serialization format used by Telegram.

**Key Features**:
- Compact binary encoding
- Strong typing
- Backward compatible
- Self-describing (constructor IDs)

## Basic Concepts

### Constructor ID

Every TL type has a unique 32-bit identifier:

```
0x1cb5c415  // Vector constructor
0x73f1f8dc  // MsgContainer constructor
```

### Type Declaration

```tl
// Simple type
int  // 32-bit signed integer
long // 64-bit signed integer
string  // UTF-8 string with length prefix
bytes   // Raw bytes with length prefix
bool    // Boolean (0xbc799737 or 0x997275b5)
double  // 64-bit floating point
```

## Composite Types

### Structures

```tl
// Constructor with fields
user#938458c1 id:long first_name:string last_name:string = User;

// Breakdown:
// user          - Name (for documentation)
// #938458c1     - Constructor ID (hex)
// id:long       - Field: name:type
// first_name:string
// last_name:string
// = User        - Result type
```

### Methods

```tl
// RPC method declaration
checkPhone#6fe51dfb phone_number:string = Bool;

// Parameters:
// phone_number:string - Input parameter
// = Bool              - Return type
```

## Serialization Examples

### Integer

```go
// int32 - Little-endian
func encodeInt32(v int32) []byte {
    return []byte{
        byte(v),
        byte(v >> 8),
        byte(v >> 16),
        byte(v >> 24),
    }
}

// Example: 0x12345678
// [0x78, 0x56, 0x34, 0x12]
```

### Long (int64)

```go
// int64 - Little-endian
func encodeInt64(v int64) []byte {
    return []byte{
        byte(v),
        byte(v >> 8),
        byte(v >> 16),
        byte(v >> 24),
        byte(v >> 32),
        byte(v >> 40),
        byte(v >> 48),
        byte(v >> 56),
    }
}
```

### String

```go
// String format:
// [length:1-3 bytes][data:length bytes]
// Length encoded as variable-length integer

func encodeString(s string) []byte {
    data := []byte(s)
    length := len(data)
    
    if length <= 253 {
        // Single byte length
        return append([]byte{byte(length)}, data...)
    }
    else {
        // 3-byte length (0xfe + 24-bit little-endian)
        result := []byte{0xfe, byte(length), byte(length >> 8), byte(length >> 16)}
        return append(result, data...)
    }
}

// Example: "Hi"
// [0x02, 0x48, 0x69]
```

### Bytes

Same encoding as string.

### Bool

```go
// True:  0x997275b5
// False: 0xbc799737

var (
    BoolTrue  = []byte{0xb5, 0x75, 0x72, 0x99}
    BoolFalse = []byte{0x37, 0x97, 0x72, 0xbc}
)
```

### Vector (Array)

```go
// Vector format:
// 0x1cb5c415 [count:int32] [items...]

func encodeVector(items [][]byte) []byte {
    result := []byte{0x15, 0xc4, 0xb5, 0x1c}  // Vector constructor
    result = append(result, encodeInt32(int32(len(items)))...)
    
    for _, item := range items {
        result = append(result, item...)
    }
    
    return result
}
```

## Complete Example

```go
// TL Definition:
// user#938458c1 id:long first_name:string last_name:string = User;

type TLUser struct {
    ID        int64
    FirstName string
    LastName  string
}

func (u *TLUser) Encode() []byte {
    // Constructor ID
    result := []byte{0xc1, 0x58, 0x84, 0x93}
    
    // ID (long)
    result = append(result, encodeInt64(u.ID)...)
    
    // FirstName (string)
    result = append(result, encodeString(u.FirstName)...)
    
    // LastName (string)
    result = append(result, encodeString(u.LastName)...)
    
    return result
}

func (u *TLUser) Decode(data []byte) error {
    if len(data) < 4 {
        return errors.New("data too short")
    }
    
    // Verify constructor
    if binary.LittleEndian.Uint32(data[0:4]) != 0x938458c1 {
        return errors.New("wrong constructor")
    }
    
    offset := 4
    
    // ID
    u.ID = int64(binary.LittleEndian.Uint64(data[offset:offset+8]))
    offset += 8
    
    // FirstName
    firstName, n := decodeString(data[offset:])
    u.FirstName = firstName
    offset += n
    
    // LastName
    lastName, n := decodeString(data[offset:])
    u.LastName = lastName
    
    return nil
}
```

## Flags System

### Optional Fields

```tl
// Flags indicate optional fields
user#8d4d2247 flags:# id:long 
    first_name:flags.0?string 
    last_name:flags.1?string 
    username:flags.2?string = User;

// flags.# - 32-bit bitfield
// flags.N?type - Field present if bit N is set
```

```go
type TLUserFlags struct {
    Flags     uint32
    ID        int64
    FirstName *string  // flags.0
    LastName  *string  // flags.1
    Username  *string  // flags.2
}

func (u *TLUserFlags) Encode() []byte {
    // Calculate flags
    var flags uint32
    if u.FirstName != nil {
        flags |= 1 << 0
    }
    if u.LastName != nil {
        flags |= 1 << 1
    }
    if u.Username != nil {
        flags |= 1 << 2
    }
    
    // Encode...
}
```

## Go Implementation

### Code Generation

Use mtprotoc to generate Go code from .tl files:

```bash
# Generate Go code
mtprotoc -I schema/ -o generated/ schema/mtproto.tl

# Output:
# generated/user.go
# generated/messages.go
# ...
```

### Manual Implementation

```go
package mtproto

//go:generate mtprotoc -I ../schema -o . ../schema/mtproto.tl

type TLObject interface {
    Encode() []byte
    Decode([]byte) error
    ConstructorID() uint32
}
```

## Common Patterns

### Polymorphism

```tl
// Abstract type
InputPeer = InputPeerEmpty | InputPeerSelf | InputPeerChat | InputPeerUser;

// Constructors
inputPeerEmpty#7f3b18ea = InputPeer;
inputPeerSelf#7da07ec9 = InputPeer;
inputPeerChat#179be863 chat_id:long = InputPeer;
inputPeerUser#7b8e7de6 user_id:long access_hash:long = InputPeer;
```

```go
// Go implementation using interface
type InputPeer interface {
    TLObject
    isInputPeer()
}

type TLInputPeerChat struct {
    ChatID int64
}

func (*TLInputPeerChat) isInputPeer() {}
```

### Error Handling

```tl
// rpc_error#2144ca19 error_code:int error_message:string = RpcError;
```

```go
func decodeResponse(data []byte) (TLObject, error) {
    constructor := binary.LittleEndian.Uint32(data[0:4])
    
    switch constructor {
    case 0x2144ca19:  // rpc_error
        err := &TLRpcError{}
        err.Decode(data)
        return nil, fmt.Errorf("RPC error %d: %s", err.ErrorCode, err.ErrorMessage)
        
    // ... other cases
    }
}
```

## Schema Resources

### Official Schemas

- [MTProto Schema](https://core.telegram.org/schema)
- [TL Language Spec](https://core.telegram.org/mtproto/TL)

### Layer Versions

| Layer | Features |
|-------|----------|
| 165   | Current stable |
| 166+  | Newer features |

## Best Practices

1. **Always check constructor IDs** before decoding
2. **Handle unknown constructors** gracefully
3. **Use generated code** instead of manual encoding
4. **Validate data length** before accessing offsets
5. **Handle optional fields** using flags system
