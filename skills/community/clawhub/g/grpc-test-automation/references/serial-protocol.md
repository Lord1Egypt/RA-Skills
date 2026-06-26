# Serial Communication Protocol

## Overview

Simulates serial communication between host PC and embedded board using TCP socket.

```
Host PC                    Embedded Board
(TCP Client)              (TCP Server)
     │                         │
     │──── Command ────────────→│
     │                         │
     │←─── Response ───────────│
     │                         │
```

## Connection

```python
# Host (Client)
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

# Board (Server)
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(1)
```

## Command Protocol

All commands are JSON formatted, newline-terminated.

### 1. MOUNT - Mount SDK to board

**Request:**
```json
{"command": "MOUNT", "source_path": "/path/to/sdk"}
```

**Response:**
```json
{
  "status": "OK",
  "message": "Mounted to /mnt/sdk",
  "files": ["libvenc_sdk.so", "venc_sdk.h"]
}
```

**Board Action:** Copy files from source_path to mount point

### 2. UPLOAD - Upload file to board

**Request:**
```json
{
  "command": "UPLOAD",
  "filename": "grpc_server",
  "content": "<base64 encoded binary>"
}
```

**Response:**
```json
{
  "status": "OK",
  "message": "File uploaded: grpc_server"
}
```

### 3. START_SERVER - Start gRPC service

**Request:**
```json
{"command": "START_SERVER", "port": 8080}
```

**Response:**
```json
{
  "status": "OK",
  "message": "Server started",
  "pid": 12345
}
```

**Board Action:**
```bash
export LD_LIBRARY_PATH=/mnt/sdk/lib:$LD_LIBRARY_PATH
cd /mnt/sdk
./grpc_server 8080 &
```

### 4. STOP_SERVER - Stop gRPC service

**Request:**
```json
{"command": "STOP_SERVER"}
```

**Response:**
```json
{
  "status": "OK",
  "message": "Server stopped"
}
```

### 5. STATUS - Query board status

**Request:**
```json
{"command": "STATUS"}
```

**Response:**
```json
{
  "status": "OK",
  "mount_path": "/mnt/sdk",
  "server_status": "RUNNING",
  "server_pid": 12345,
  "files": ["grpc_server", "libvenc_sdk.so"]
}
```

### 6. SHUTDOWN - Shutdown board

**Request:**
```json
{"command": "SHUTDOWN"}
```

**Response:**
```json
{
  "status": "OK",
  "message": "Shutting down"
}
```

## Implementation

### Serial Simulator (Board Side)

```python
class SerialSimulator:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.mount_path = '/tmp/board_sdk'
        self.server_process = None
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        while True:
            client, addr = self.socket.accept()
            self.handle_client(client)
    
    def handle_client(self, client):
        while True:
            data = client.recv(1024)
            if not data:
                break
            
            command = json.loads(data.decode())
            response = self.execute_command(command)
            client.send(json.dumps(response).encode() + b'\n')
    
    def execute_command(self, cmd):
        handler = getattr(self, f'handle_{cmd["command"].lower()}', None)
        if handler:
            return handler(cmd)
        return {"status": "ERROR", "message": "Unknown command"}
    
    def handle_mount(self, cmd):
        # Copy files from source to mount point
        import shutil
        source = cmd['source_path']
        shutil.copytree(source, self.mount_path, dirs_exist_ok=True)
        return {
            "status": "OK",
            "message": f"Mounted to {self.mount_path}",
            "files": os.listdir(self.mount_path)
        }
    
    def handle_start_server(self, cmd):
        # Start gRPC server process
        import subprocess
        server_path = os.path.join(self.mount_path, 'grpc_server')
        lib_path = os.path.join(self.mount_path, 'lib')
        
        env = os.environ.copy()
        env['LD_LIBRARY_PATH'] = lib_path + ':' + env.get('LD_LIBRARY_PATH', '')
        
        self.server_process = subprocess.Popen(
            [server_path, str(cmd.get('port', 8080))],
            cwd=self.mount_path,
            env=env
        )
        
        time.sleep(2)  # Wait for startup
        
        if self.server_process.poll() is None:
            return {
                "status": "OK",
                "message": "Server started",
                "pid": self.server_process.pid
            }
        else:
            return {"status": "ERROR", "message": "Failed to start"}
```

### Serial Client (Host Side)

```python
class SerialClient:
    def __init__(self, host='localhost', port=9999):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
    
    def send_command(self, command):
        self.socket.send(json.dumps(command).encode() + b'\n')
        response = self.socket.recv(4096)
        return json.loads(response.decode())
    
    def mount_sdk(self, sdk_path):
        return self.send_command({
            "command": "MOUNT",
            "source_path": sdk_path
        })
    
    def start_server(self, port=8080):
        return self.send_command({
            "command": "START_SERVER",
            "port": port
        })
    
    def get_status(self):
        return self.send_command({"command": "STATUS"})
```

## Deployment Script

```bash
#!/bin/bash
# deploy_to_board.sh

BOARD_HOST=${1:-localhost}
BOARD_PORT=${2:-9999}
SDK_PATH=${3:-./sdk}
SERVER_PATH=${4:-./server/build}

echo "Deploying to board at ${BOARD_HOST}:${BOARD_PORT}"

# Connect and mount SDK
python3 << EOF
import socket, json, time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('${BOARD_HOST}', ${BOARD_PORT}))

# Mount SDK
client.send(json.dumps({
    "command": "MOUNT",
    "source_path": "${SDK_PATH}"
}).encode() + b'\n')
print(client.recv(4096).decode())

# Upload server binary
with open('${SERVER_PATH}/grpc_server', 'rb') as f:
    content = f.read()
client.send(json.dumps({
    "command": "UPLOAD",
    "filename": "grpc_server",
    "content": content.hex()
}).encode() + b'\n')
print(client.recv(4096).decode())

# Start server
client.send(json.dumps({
    "command": "START_SERVER",
    "port": 8080
}).encode() + b'\n')
print(client.recv(4096).decode())

client.close()
EOF

echo "Deployment complete!"
```
