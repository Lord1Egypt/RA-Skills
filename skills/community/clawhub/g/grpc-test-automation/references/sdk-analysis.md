# SDK Header Analysis Guide

## Goal

Parse C/C++ SDK headers to extract:
1. Function signatures (for gRPC methods)
2. Data structures (for proto messages)
3. Enumerations (for proto enums)
4. Error codes (for error handling)

## Parsing Patterns

### 1. Function Signatures

**Input (SDK Header):**
```c
venc_error_t venc_get_device_info(venc_device_info_t *info);
venc_error_t venc_encode_start(const venc_encode_params_t *params, uint64_t *session_id);
venc_error_t venc_encode_stop(uint64_t session_id);
```

**Output (Proto RPCs):**
```protobuf
rpc GetDeviceInfo(GetDeviceInfoRequest) returns (GetDeviceInfoResponse);
rpc StartEncoding(StartEncodingRequest) returns (StartEncodingResponse);
rpc StopEncoding(StopEncodingRequest) returns (StopEncodingResponse);
```

**Naming Convention:**
| SDK Function | Proto RPC |
|--------------|-----------|
| `venc_get_device_info()` | `GetDeviceInfo` |
| `venc_encode_start()` | `StartEncoding` |
| `venc_encode_stop()` | `StopEncoding` |
| `venc_encode_get_status()` | `GetEncodingStatus` |

Rule: Remove prefix `venc_`, convert snake_case to PascalCase

### 2. Data Structures

**Input (SDK Header):**
```c
typedef struct {
    char device_id[64];
    char model[128];
    char firmware_version[32];
    venc_device_status_t status;
    uint64_t uptime;
} venc_device_info_t;
```

**Output (Proto Message):**
```protobuf
message DeviceInfo {
    string device_id = 1;
    string model = 2;
    string firmware_version = 3;
    DeviceStatus status = 4;
    uint64 uptime = 5;
}
```

**Type Mapping:**
| C Type | Proto Type |
|--------|------------|
| `char[N]` | `string` |
| `uint8_t` / `int8_t` | `int32` |
| `uint16_t` / `int16_t` | `int32` |
| `uint32_t` / `int32_t` | `int32` / `uint32` |
| `uint64_t` / `int64_t` | `uint64` / `int64` |
| `float` | `float` |
| `double` | `double` |
| `bool` | `bool` |
| `enum xxx` | `EnumType` |
| `struct xxx` | `message Xxx` |

### 3. Enumerations

**Input (SDK Header):**
```c
typedef enum {
    VENC_CODEC_H264 = 0,
    VENC_CODEC_H265 = 1,
    VENC_CODEC_MJPEG = 2,
} venc_codec_t;

typedef enum {
    VENC_OK = 0,
    VENC_ERR_INVALID_PARAM = 1001,
    VENC_ERR_DEVICE_BUSY = 1002,
} venc_error_t;
```

**Output (Proto Enum):**
```protobuf
enum CodecType {
    CODEC_H264 = 0;
    CODEC_H265 = 1;
    CODEC_MJPEG = 2;
}

enum ErrorCode {
    OK = 0;
    INVALID_PARAM = 1001;
    DEVICE_BUSY = 1002;
}
```

**Naming Convention:**
- Remove prefix `VENC_`
- Remove `_t` suffix from type name
- Convert UPPER_SNAKE to UPPER_SNAKE (keep same)

### 4. Error Codes

Map SDK error codes to gRPC status codes:

| SDK Error | gRPC Status | HTTP Code |
|-----------|-------------|-----------|
| `VENC_OK` | `OK` | 200 |
| `VENC_ERR_INVALID_PARAM` | `INVALID_ARGUMENT` | 400 |
| `VENC_ERR_DEVICE_BUSY` | `RESOURCE_EXHAUSTED` | 429 |
| `VENC_ERR_NOT_INIT` | `FAILED_PRECONDITION` | 400 |
| `VENC_ERR_SESSION_INVALID` | `NOT_FOUND` | 404 |
| `VENC_ERR_TIMEOUT` | `DEADLINE_EXCEEDED` | 504 |

## Analysis Script

```python
import re

def parse_sdk_header(header_file):
    """Parse SDK header file"""
    with open(header_file, 'r') as f:
        content = f.read()
    
    # Extract functions
    func_pattern = r'(\w+_error_t)\s+(\w+)\s*\(([^)]+)\)\s*;'
    functions = re.findall(func_pattern, content)
    
    # Extract enums
    enum_pattern = r'typedef\s+enum\s*\{([^}]+)\}\s*(\w+)_t;'
    enums = re.findall(enum_pattern, content)
    
    # Extract structs
    struct_pattern = r'typedef\s+struct\s*\{([^}]+)\}\s*(\w+)_t;'
    structs = re.findall(struct_pattern, content)
    
    return {
        'functions': functions,
        'enums': enums,
        'structs': structs
    }
```

## Example: Complete SDK Analysis

**Input:** `venc_sdk.h`

```c
// Error codes
typedef enum {
    VENC_OK = 0,
    VENC_ERR_INVALID_PARAM = 1001,
} venc_error_t;

// Device status
typedef enum {
    VENC_STATUS_OFFLINE = 0,
    VENC_STATUS_ONLINE = 1,
} venc_device_status_t;

// Device info
typedef struct {
    char device_id[64];
    char model[128];
    venc_device_status_t status;
    uint64_t uptime;
} venc_device_info_t;

// Functions
venc_error_t venc_init(void);
venc_error_t venc_get_device_info(venc_device_info_t *info);
venc_error_t venc_encode_start(uint32_t channel, uint64_t *session_id);
venc_error_t venc_encode_stop(uint64_t session_id);
```

**Output:** Analysis result

```json
{
    "enums": [
        {"name": "ErrorCode", "values": ["OK=0", "INVALID_PARAM=1001"]},
        {"name": "DeviceStatus", "values": ["OFFLINE=0", "ONLINE=1"]}
    ],
    "messages": [
        {
            "name": "DeviceInfo",
            "fields": [
                {"name": "device_id", "type": "string"},
                {"name": "model", "type": "string"},
                {"name": "status", "type": "DeviceStatus"},
                {"name": "uptime", "type": "uint64"}
            ]
        }
    ],
    "services": [
        {"name": "Init", "input": "empty", "output": "InitResponse"},
        {"name": "GetDeviceInfo", "input": "GetDeviceInfoRequest", "output": "DeviceInfo"},
        {"name": "StartEncoding", "input": "StartEncodingRequest", "output": "StartEncodingResponse"},
        {"name": "StopEncoding", "input": "StopEncodingRequest", "output": "StopEncodingResponse"}
    ]
}
```
