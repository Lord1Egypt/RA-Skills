# C++ gRPC Server Implementation Guide

## Overview

The gRPC server wraps SDK calls and exposes them as gRPC services.

## Architecture

```
┌─────────────────────────────────────────┐
│  JMeter (Client)                        │
│  - Sends gRPC requests                  │
└────────────────┬────────────────────────┘
                 │ gRPC (HTTP/2)
                 ↓
┌─────────────────────────────────────────┐
│  gRPC Server (C++)                      │
│  ┌─────────────────────────────────┐   │
│  │ Service Implementation          │   │
│  │ - Receives gRPC calls           │   │
│  │ - Converts proto to SDK types   │   │
│  │ - Calls SDK functions           │   │
│  │ - Converts SDK results to proto │   │
│  └────────────────┬────────────────┘   │
│                   ↓                      │
│  ┌─────────────────────────────────┐   │
│  │ SDK Wrapper Layer               │   │
│  │ - Type conversion               │   │
│  │ - Error mapping                 │   │
│  └────────────────┬────────────────┘   │
└───────────────────┼─────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  SDK Library (libvenc_sdk.so)           │
│  - Actual hardware interface            │
└─────────────────────────────────────────┘
```

## Implementation Template

### 1. Proto File (service.proto)

```protobuf
syntax = "proto3";
package venc;

enum DeviceStatus {
    DEVICE_OFFLINE = 0;
    DEVICE_ONLINE = 1;
}

message GetDeviceInfoRequest {
    string device_id = 1;
}

message GetDeviceInfoResponse {
    string device_id = 1;
    string model = 2;
    DeviceStatus status = 3;
    uint64 uptime = 4;
}

service VencService {
    rpc GetDeviceInfo(GetDeviceInfoRequest) returns (GetDeviceInfoResponse);
}
```

### 2. Server Implementation (server.cpp)

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "service.grpc.pb.h"

// Include SDK header
extern "C" {
#include "venc_sdk.h"
}

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using grpc::StatusCode;

// Helper: Convert SDK error to gRPC status
Status sdk_error_to_grpc(venc_error_t err) {
    switch (err) {
        case VENC_OK:
            return Status::OK;
        case VENC_ERR_INVALID_PARAM:
            return Status(StatusCode::INVALID_ARGUMENT, "Invalid parameter");
        case VENC_ERR_DEVICE_BUSY:
            return Status(StatusCode::RESOURCE_EXHAUSTED, "Device busy");
        case VENC_ERR_SESSION_INVALID:
            return Status(StatusCode::NOT_FOUND, "Session not found");
        default:
            return Status(StatusCode::INTERNAL, "SDK error");
    }
}

// Helper: Convert SDK status to proto enum
venc::DeviceStatus sdk_status_to_proto(venc_device_status_t status) {
    switch (status) {
        case VENC_STATUS_OFFLINE:
            return venc::DEVICE_OFFLINE;
        case VENC_STATUS_ONLINE:
            return venc::DEVICE_ONLINE;
        default:
            return venc::DEVICE_OFFLINE;
    }
}

class VencServiceImpl final : public venc::VencService::Service {
public:
    VencServiceImpl() {
        // Initialize SDK
        venc_init();
        std::cout << "[Server] SDK initialized" << std::endl;
    }
    
    ~VencServiceImpl() {
        venc_deinit();
        std::cout << "[Server] SDK deinitialized" << std::endl;
    }
    
    // GetDeviceInfo implementation
    Status GetDeviceInfo(ServerContext* ctx,
                         const venc::GetDeviceInfoRequest* req,
                         venc::GetDeviceInfoResponse* resp) override {
        std::cout << "[Server] GetDeviceInfo called" << std::endl;
        
        // Call SDK
        venc_device_info_t info;
        venc_error_t err = venc_get_device_info(&info);
        
        if (err != VENC_OK) {
            return sdk_error_to_grpc(err);
        }
        
        // Convert to proto response
        resp->set_device_id(info.device_id);
        resp->set_model(info.model);
        resp->set_status(sdk_status_to_proto(info.status));
        resp->set_uptime(info.uptime);
        
        return Status::OK;
    }
    
    // Add more methods as needed...
};

void RunServer(uint16_t port) {
    std::string address = "0.0.0.0:" + std::to_string(port);
    VencServiceImpl service;
    
    ServerBuilder builder;
    builder.AddListeningPort(address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    builder.SetMaxReceiveMessageSize(4 * 1024 * 1024);
    
    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "========================================" << std::endl;
    std::cout << "VENC gRPC Server" << std::endl;
    std::cout << "Listening on " << address << std::endl;
    std::cout << "========================================" << std::endl;
    
    server->Wait();
}

int main(int argc, char** argv) {
    uint16_t port = argc > 1 ? std::stoi(argv[1]) : 8080;
    RunServer(port);
    return 0;
}
```

### 3. CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.15)
project(venc_grpc_server CXX C)

set(CMAKE_CXX_STANDARD 17)

# Find packages
find_package(Protobuf REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GRPC++ REQUIRED grpc++)

# Proto generation
set(PROTO_FILE ${CMAKE_SOURCE_DIR}/../proto/service.proto)
set(GEN_DIR ${CMAKE_BINARY_DIR}/generated)
file(MAKE_DIRECTORY ${GEN_DIR})

execute_process(
    COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        --cpp_out=${GEN_DIR}
        --grpc_out=${GEN_DIR}
        --plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN}
        -I ${CMAKE_SOURCE_DIR}/../proto
        ${PROTO_FILE}
)

# Server executable
add_executable(venc_server
    server.cpp
    ${GEN_DIR}/service.pb.cc
    ${GEN_DIR}/service.grpc.pb.cc
)

target_include_directories(venc_server PRIVATE
    ${GEN_DIR}
    ${CMAKE_SOURCE_DIR}/../sdk/include
    ${Protobuf_INCLUDE_DIRS}
)

# Link libraries
target_link_libraries(venc_server
    ${GRPC++_LIBRARIES}
    ${Protobuf_LIBRARIES}
    ${CMAKE_SOURCE_DIR}/../sdk/lib/libvenc_sdk.so
    pthread
)

# Generate proto descriptor for JMeter
add_custom_command(
    TARGET venc_server POST_BUILD
    COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        --descriptor_set_out=${CMAKE_BINARY_DIR}/service.protobin
        --include_imports
        -I ${CMAKE_SOURCE_DIR}/../proto
        ${PROTO_FILE}
    COMMENT "Generating proto descriptor for JMeter"
)
```

## Build Commands

```bash
# Create build directory
mkdir -p server/build && cd server/build

# Configure
cmake .. \
    -DCMAKE_PREFIX_PATH=/usr/local \
    -DGRPC_CPP_PLUGIN=/usr/local/bin/grpc_cpp_plugin

# Build
make -j$(nproc)

# Output
ls -la venc_server service.protobin
```

## Error Handling Pattern

```cpp
// SDK error → gRPC Status
Status handle_sdk_result(venc_error_t err, const std::string& context) {
    switch (err) {
        case VENC_OK:
            return Status::OK;
            
        case VENC_ERR_INVALID_PARAM:
            return Status(StatusCode::INVALID_ARGUMENT, 
                         context + ": Invalid parameter");
            
        case VENC_ERR_DEVICE_BUSY:
            return Status(StatusCode::RESOURCE_EXHAUSTED,
                         context + ": Device busy");
            
        case VENC_ERR_CHANNEL_FULL:
            return Status(StatusCode::RESOURCE_EXHAUSTED,
                         context + ": All channels occupied");
            
        case VENC_ERR_SESSION_INVALID:
            return Status(StatusCode::NOT_FOUND,
                         context + ": Session not found");
            
        case VENC_ERR_TIMEOUT:
            return Status(StatusCode::DEADLINE_EXCEEDED,
                         context + ": Timeout");
            
        default:
            return Status(StatusCode::INTERNAL,
                         context + ": Unknown error " + std::to_string(err));
    }
}
```

## Testing the Server

```bash
# Start server
./venc_server 8080

# Test with grpcurl (if available)
grpcurl -plaintext -d '{"device_id":"BOARD-001"}' \
    localhost:8080 venc.VencService/GetDeviceInfo
```
