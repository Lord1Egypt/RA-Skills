# Test Case Patterns

## Test Categories

### 1. Functional Tests (P0)

Verify normal operation of each interface.

**Pattern:**
```
TC-00X: [Interface Name]
- Request: Valid parameters
- Expected: Success response with correct data
```

**Example:**
```
TC-001: GetDeviceInfo
- Request: {"device_id": "BOARD-001"}
- Expected: {"device_id": "BOARD-001", "status": 1, ...}
```

### 2. Exception Tests (P1)

Verify error handling for invalid inputs.

**Pattern:**
```
TC-00X: [Interface Name] - [Error Condition]
- Request: Invalid parameters
- Expected: Error response with appropriate status code
```

**Example:**
```
TC-007: StartEncoding - Invalid Channel
- Request: {"channel": 10, ...}
- Expected: INVALID_ARGUMENT error
```

### 3. Performance Tests (P2)

Verify system under load.

**Pattern:**
```
TC-00X: [Interface Name] - Concurrent
- Config: N threads × M loops
- Metrics: Avg response time, throughput, error rate
```

## Test Dependencies

```
TC-001 (GetDeviceInfo) ─┐
TC-002 (GetVersion) ────┤
                        ├──→ TC-003 (Start) ──→ TC-004 (Status)
                        │                    ├─→ TC-005 (Update)
                        │                    └─→ TC-006 (Stop)
                        └──→ TC-007, TC-008 (Exception tests)
```

## Session ID Flow

```
Start ──→ session_id ──→ GetStatus
                      ──→ UpdateParams
                      ──→ Stop
```

Always extract `session_id` from Start response for subsequent calls.

## Common Test Cases

| Interface | Functional | Exception | Performance |
|-----------|------------|-----------|-------------|
| GetDeviceInfo | Valid ID | Invalid ID | 100 req/s |
| GetVersion | Basic call | N/A | N/A |
| StartEncoding | Valid params | Invalid channel | N/A |
| GetEncodingStatus | Valid session | Invalid session | N/A |
| UpdateEncodingParams | Valid update | Invalid session | N/A |
| StopEncoding | Valid stop | Invalid session | N/A |

## Validation Points

### Response Validation
- [ ] Status code matches expected
- [ ] Response contains required fields
- [ ] Field values are within valid range
- [ ] No unexpected null values

### Performance Validation
- [ ] Response time < threshold
- [ ] Error rate < threshold
- [ ] Throughput > threshold
