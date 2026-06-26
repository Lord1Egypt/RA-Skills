# Proto Design Guide

## Design Principles

1. **Map SDK interfaces to gRPC services**
2. **Use proto3 syntax**
3. **Follow naming conventions**

## SDK to Proto Mapping

### Error Codes → Enums
```protobuf
// SDK: venc_error_t { VENC_OK=0, VENC_ERR_PARAM=1001, ... }
enum ErrorCode {
    OK = 0;
    INVALID_PARAM = 1001;
    DEVICE_BUSY = 1002;
}
```

### Status → Enums
```protobuf
// SDK: venc_device_status_t { OFFLINE=0, ONLINE=1, ... }
enum DeviceStatus {
    DEVICE_OFFLINE = 0;
    DEVICE_ONLINE = 1;
    DEVICE_BUSY = 2;
}
```

### Structs → Messages
```protobuf
// SDK: typedef struct { char device_id[64]; ... } venc_device_info_t;
message DeviceInfo {
    string device_id = 1;
    string model = 2;
    string firmware_version = 3;
}
```

### Functions → RPCs
```protobuf
// SDK: venc_error_t venc_get_device_info(venc_device_info_t *info);
rpc GetDeviceInfo(GetDeviceInfoRequest) returns (GetDeviceInfoResponse);
```

## Naming Conventions

| SDK | Proto |
|-----|-------|
| `venc_get_device_info()` | `rpc GetDeviceInfo` |
| `venc_encode_start()` | `rpc StartEncoding` |
| `venc_encode_stop()` | `rpc StopEncoding` |
| `venc_encode_get_status()` | `rpc GetEncodingStatus` |

## Request/Response Pattern

Every RPC should have:
- `XxxRequest` message with input parameters
- `XxxResponse` message with results

```protobuf
message GetDeviceInfoRequest {
    string device_id = 1;
}

message GetDeviceInfoResponse {
    string device_id = 1;
    string model = 2;
    DeviceStatus status = 3;
}
```

## Common Fields

Always include in responses:
- `bool success` - Operation success flag
- `string message` - Human-readable message
- `uint64 session_id` - For stateful operations
