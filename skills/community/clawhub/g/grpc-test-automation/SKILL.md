---
name: grpc-test-automation
description: |
  Complete gRPC test automation for embedded devices with C/C++ SDK.
  
  Input: requirements.md + SDK (C/C++ headers and libraries)
  Output: Test framework + JMX + Excel report
  
  Workflow:
  1. Analyze SDK headers → Design gRPC interfaces
  2. Write C++ gRPC server (wraps SDK) + Proto definition
  3. Compile server → Generate proto descriptor
  4. Create JMeter JMX test plan
  5. Simulate serial communication → Mount resources to board
  6. Board starts gRPC service
  7. JMeter executes tests
  8. Generate Excel report
  
  Triggers: "grpc test", "板端测试", "协议测试", "SDK测试", "嵌入式测试",
  "create test framework", "generate jmx", "串口测试"
---

# gRPC Test Automation for Embedded Devices

Automated framework for testing C/C++ SDK on embedded boards via gRPC + JMeter.

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  输入: 需求文档 + C/C++ SDK (头文件 + 库)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: 分析 SDK 头文件                                         │
│  - 提取函数签名                                                   │
│  - 识别错误码枚举                                                 │
│  - 理解数据结构                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: 编写 C++ gRPC 服务端                                    │
│  - 创建 Proto 文件 (基于 SDK 接口)                                │
│  - 实现 gRPC 服务类 (封装 SDK 调用)                               │
│  - 编写 CMakeLists.txt                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: 编译生成                                                │
│  - cmake + make → 生成可执行文件                                  │
│  - protoc → 生成 proto descriptor (.protobin)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: 编写 JMeter JMX                                        │
│  - 引用 proto descriptor                                        │
│  - 配置 gRPC Sampler                                            │
│  - 定义测试用例                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: 串口下发资源到板端                                       │
│  - 模拟串口通信 (TCP Socket)                                     │
│  - 下发: SDK库 + 服务程序 + Proto                                │
│  - 挂载到板端目录                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: 板端拉起服务                                            │
│  - 设置 LD_LIBRARY_PATH                                         │
│  - 执行 ./grpc_server 8080                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 7: JMeter 执行测试                                         │
│  - jmeter -n -t test.jmx                                       │
│  - 收集响应数据                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 8: 生成 Excel 报告                                         │
│  - 测试概览                                                      │
│  - 测试详情                                                      │
│  - 性能指标                                                      │
│  - 错误详情                                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Input Files

### Required
- `sdk/include/*.h` - SDK header files
- `sdk/lib/*.so` or `sdk/lib/*.a` - SDK libraries

### Optional
- `requirements.md` - Interface specifications
- `test_cases.md` - Historical test cases
- `test_framework/` - Historical framework code

## Output Structure

```
grpc_test/
├── proto/
│   └── service.proto            # Generated from SDK analysis
├── server/
│   ├── CMakeLists.txt          # Build configuration
│   ├── grpc_server.cpp         # gRPC server (wraps SDK)
│   ├── build/                  # Build output
│   │   ├── grpc_server         # Compiled executable
│   │   └── service.protobin    # Proto descriptor for JMeter
│   └── service.pb.h/cc         # Generated protobuf code
├── client/
│   └── test_client.cpp         # Optional test client
├── jmeter/
│   ├── test_plans/
│   │   └── test.jmx           # JMeter test plan
│   ├── results/
│   │   ├── result.jtl         # Raw results
│   │   └── report.xlsx        # Excel report
│   └── service.protobin       # Proto descriptor (copied)
├── scripts/
│   ├── serial_simulator.py    # Serial communication simulator
│   ├── deploy_to_board.sh     # Deploy resources to board
│   ├── run_server.sh          # Start server on board
│   └── run_tests.sh           # Execute full test cycle
└── sdk/                        # Original SDK (mounted to board)
    ├── include/
    └── lib/
```

## Scripts Usage

### 1. Analyze SDK Headers

```python
scripts/analyze_sdk.py sdk/include/
```

Extracts: functions, enums, structs, error codes

### 2. Generate Proto + Server

```python
scripts/generate_grpc_server.py --sdk sdk/ --output server/
```

Creates: proto file, server.cpp, CMakeLists.txt

### 3. Build

```bash
cd server/build && cmake .. && make
```

Generates: grpc_server executable, service.protobin

### 4. Deploy to Board

```bash
scripts/deploy_to_board.sh --board localhost:9999 --sdk sdk/ --server server/build/
```

### 5. Run Tests

```bash
scripts/run_tests.sh --jmx jmeter/test_plans/test.jmx --output jmeter/results/
```

## Key Implementation Details

### SDK Analysis Pattern

```cpp
// SDK Header
venc_error_t venc_get_device_info(venc_device_info_t *info);
typedef struct { char device_id[64]; ... } venc_device_info_t;
typedef enum { VENC_OK=0, VENC_ERR_PARAM=1001 } venc_error_t;

↓ Analysis ↓

// Proto Definition
service VencService {
    rpc GetDeviceInfo(GetDeviceInfoRequest) returns (GetDeviceInfoResponse);
}

message GetDeviceInfoResponse {
    string device_id = 1;
    ErrorCode error = 2;
}
```

### Server Wrapper Pattern

```cpp
// gRPC Server wraps SDK calls
Status GetDeviceInfo(ServerContext* ctx, 
                     const GetDeviceInfoRequest* req,
                     GetDeviceInfoResponse* resp) override {
    venc_device_info_t info;
    venc_error_t err = venc_get_device_info(&info);  // Call SDK
    
    if (err == VENC_OK) {
        resp->set_device_id(info.device_id);
        return Status::OK;
    }
    return Status(StatusCode::INTERNAL, "SDK error");
}
```

### Serial Communication Protocol

```json
// Commands
{"command": "MOUNT", "source_path": "/path/to/sdk"}
{"command": "UPLOAD", "filename": "grpc_server", "content": "..."}
{"command": "START_SERVER", "port": 8080}
{"command": "STATUS"}
{"command": "STOP_SERVER"}
```

## See Also

- `references/sdk-analysis.md` - SDK header parsing patterns
- `references/cpp-server.md` - C++ gRPC server implementation
- `references/serial-protocol.md` - Serial communication details
- `references/jmeter-config.md` - JMeter gRPC plugin configuration
