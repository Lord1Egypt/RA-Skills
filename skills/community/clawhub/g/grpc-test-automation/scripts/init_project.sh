#!/bin/bash
# gRPC Test Project Initializer
# 初始化 gRPC 测试项目结构

set -e

PROJECT_NAME=${1:-"grpc_test"}
BASE_DIR=$(pwd)/${PROJECT_NAME}

echo "=========================================="
echo "gRPC Test Project Initializer"
echo "=========================================="
echo ""
echo "Project: ${PROJECT_NAME}"
echo "Location: ${BASE_DIR}"
echo ""

# 创建目录结构
echo "[1/5] Creating directory structure..."
mkdir -p ${BASE_DIR}/{proto,server/{build},client,jmeter/{test_plans,results,lib},sdk/{include,lib,bin},scripts,logs}

echo "✅ Directory structure created"
echo ""

# 创建模板文件
echo "[2/5] Creating template files..."

# Proto 模板
cat > ${BASE_DIR}/proto/service.proto << 'EOF'
syntax = "proto3";

package service;

// TODO: Define your service here
service YourService {
    rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);
}

message GetInfoRequest {
    string id = 1;
}

message GetInfoResponse {
    string id = 1;
    string name = 2;
}
EOF

# 服务器模板
cat > ${BASE_DIR}/server/CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.15)
project(grpc_server CXX)

set(CMAKE_CXX_STANDARD 17)
find_package(Protobuf REQUIRED)

# Generate proto
set(PROTO_FILE ${CMAKE_SOURCE_DIR}/../proto/service.proto)
set(GEN_DIR ${CMAKE_BINARY_DIR}/generated)
file(MAKE_DIRECTORY ${GEN_DIR})

execute_process(
    COMMAND ${Protobuf_PROTOC_EXECUTABLE}
        --cpp_out=${GEN_DIR}
        --grpc_out=${GEN_DIR}
        --plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin
        -I ${CMAKE_SOURCE_DIR}/../proto
        ${PROTO_FILE}
)

add_executable(grpc_server
    server.cpp
    ${GEN_DIR}/service.pb.cc
    ${GEN_DIR}/service.grpc.pb.cc
)

target_include_directories(grpc_server PRIVATE ${GEN_DIR})
target_link_libraries(grpc_server grpc++ grpc ${Protobuf_LIBRARIES})
EOF

# 服务器代码模板
cat > ${BASE_DIR}/server/server.cpp << 'EOF'
#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "service.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class ServiceImpl final : public service::YourService::Service {
    Status GetInfo(ServerContext* context,
                   const service::GetInfoRequest* request,
                   service::GetInfoResponse* response) override {
        response->set_id(request->id());
        response->set_name("Test Device");
        return Status::OK;
    }
};

void RunServer(uint16_t port) {
    std::string address = "0.0.0.0:" + std::to_string(port);
    ServiceImpl service;

    ServerBuilder builder;
    builder.AddListeningPort(address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << address << std::endl;
    server->Wait();
}

int main(int argc, char** argv) {
    uint16_t port = argc > 1 ? std::stoi(argv[1]) : 8080;
    RunServer(port);
    return 0;
}
EOF

# JMX 模板
cat > ${BASE_DIR}/jmeter/test_plans/test_template.jmx << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="gRPC Test" enabled="true">
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="SERVER_HOST" elementType="Argument">
            <stringProp name="Argument.name">SERVER_HOST</stringProp>
            <stringProp name="Argument.value">localhost</stringProp>
          </elementProp>
          <elementProp name="SERVER_PORT" elementType="Argument">
            <stringProp name="Argument.name">SERVER_PORT</stringProp>
            <stringProp name="Argument.value">8080</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="Test Group" enabled="true">
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">1</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
      </ThreadGroup>
      <hashTree>
        <!-- TODO: Add GRPCSampler elements here -->
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
EOF

# 脚本模板
cat > ${BASE_DIR}/scripts/run_tests.sh << 'EOF'
#!/bin/bash
# Run gRPC tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "Starting gRPC tests..."

# 1. Start server
cd ${BASE_DIR}/server/build
./grpc_server 8080 &
SERVER_PID=$!
sleep 2

# 2. Run JMeter
cd /opt/jmeter/bin
./jmeter -n -t ${BASE_DIR}/jmeter/test_plans/test.jmx \
    -l ${BASE_DIR}/jmeter/results/result.jtl \
    -j ${BASE_DIR}/jmeter/results/jmeter.log

# 3. Stop server
kill $SERVER_PID

echo "Tests completed!"
EOF

chmod +x ${BASE_DIR}/scripts/run_tests.sh

echo "✅ Template files created"
echo ""

# 创建 README
echo "[3/5] Creating README..."
cat > ${BASE_DIR}/README.md << EOF
# ${PROJECT_NAME} - gRPC Test Project

## Directory Structure

\`\`\`
${PROJECT_NAME}/
├── proto/              # Protocol Buffers definitions
├── server/             # gRPC server implementation
├── client/             # Test clients
├── jmeter/             # JMeter test plans and results
├── sdk/                # SDK resources
├── scripts/            # Automation scripts
└── logs/               # Log files
\`\`\`

## Quick Start

1. Define your service in \`proto/service.proto\`
2. Build the server: \`cd server/build && cmake .. && make\`
3. Create test plan: \`jmeter/test_plans/test.jmx\`
4. Run tests: \`./scripts/run_tests.sh\`

## Generated: $(date)
EOF

echo "✅ README created"
echo ""

# 安装依赖
echo "[4/5] Checking dependencies..."
pip3 install grpcio grpcio-tools protobuf openpyxl -q 2>/dev/null || true
echo "✅ Dependencies checked"
echo ""

echo "[5/5] Project initialization complete!"
echo ""
echo "=========================================="
echo "Next steps:"
echo "1. Edit proto/service.proto with your service definition"
echo "2. Generate proto: cd server && python3 -m grpc_tools.protoc -I../proto --python_out=. --grpc_python_out=. ../proto/service.proto"
echo "3. Create your JMX test plan"
echo "4. Run tests: ./scripts/run_tests.sh"
echo "=========================================="
