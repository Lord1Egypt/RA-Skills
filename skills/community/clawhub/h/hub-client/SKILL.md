---
name: claw-service-hub
description: "Service marketplace: publish data as services, consume hub services"
version: 1.0.0
homepage: https://github.com/TangBoheng/Claw-Service-Hub
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: ["python", "pip"]
      env: ["HUB_WS_URL"]
      pip: ["websockets", "aiohttp"]
    primaryEnv: "HUB_WS_URL"
    install:
      - id: pip
        kind: pip
        package: claw-service-hub
        label: "Install via pip"
---

triggers:
  provider:
    - provide.*service
    - publish.*service
    - expose.*service
    - create.*service
    - make.*service
    - implement.*service
  consumer:
    - what services
    - list services
    - call.*service
    - use.*service
    - query.*data
    - fetch.*data

# Tool Service Hub Skill

## Overview

Enables subagents to:
1. **Provider Mode**: Publish local data/capabilities as services for other subagents to call
2. **Consumer Mode**: Discover and call services on the Hub

---

## 1. Publishing Services as a Provider

### Complete Code Template

```python
import asyncio
import os
import sys
from pathlib import Path

# === 1. Setup path ===
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', '/home/t/.openclaw/workspace-subagentX')
sys.path.insert(0, WORKSPACE_DIR)

from client.client import LocalServiceRunner

# === 2. Define your service capability ===

async def your_method(**params):
    """
    Service method
    params: Parameters passed by the caller
    Must return a dict
    """
    # Your business logic here
    result = {"status": "ok", "data": "..."}
    return result

# === 3. Start the service ===

async def main():
    runner = LocalServiceRunner(
        name="your-service-name",      # Service name (English, no spaces)
        description="Service description",  # English description
        hub_url=os.getenv("HUB_WS_URL", "ws://localhost:8765")
    )
    
    # Register methods (can register multiple)
    runner.register_handler("your_method", your_method)
    
    print(f"🚀 Starting service...")
    await runner.run()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2. Calling Services as a Consumer

### Complete Code Template

```python
import asyncio
import os
import sys

WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', '/home/t/.openclaw/workspace-subagentX')
sys.path.insert(0, WORKSPACE_DIR)

from client.skill_client import SkillQueryClient

async def main():
    # 1. Connect to Hub
    client = SkillQueryClient(
        hub_url=os.getenv("HUB_WS_URL", "ws://localhost:8765")
    )
    await client.connect()
    
    # 2. Discover services
    services = await client.discover()
    print(f"Discovered {len(services)} services")
    
    # 3. Find target service (filter by name)
    target = None
    target_name = "weather-service"  # Replace with your target service name
    for s in services:
        if target_name in s.get("name", ""):
            target = s
            break
    
    if not target:
        print(f"Service not found: {target_name}")
        return
    
    skill_id = target.get("skill_id")
    print(f"Using service: {target.get('name')}, skill_id: {skill_id}")
    
    # 4. Call the service
    result = await client.call_service(
        service_id=skill_id,
        method="your_method",      # Method name
        params={"key": "value"}    # Parameters
    )
    
    print(f"Result: {result}")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Common Data Source Examples

### 3.1 File Data Service

```python
from pathlib import Path

DATA_DIR = Path("/path/to/data")  # Change to actual directory

async def list_files(**params):
    ext = params.get("extension", "")
    pattern = f"*{ext}" if ext else "*"
    files = [f.name for f in DATA_DIR.glob(pattern) if f.is_file()]
    return {"files": files[:50], "total": len(files)}

async def read_file(**params):
    filename = params.get("filename")
    if not filename:
        return {"error": "filename is required"}
    
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return {"error": f"File not found: {filename}"}
    
    # Read text files directly
    if filepath.suffix == '.txt':
        return {"content": filepath.read_text()[:1000]}
    
    # Return info for other files
    return {"filename": filename, "size": filepath.stat().st_size}
```

### 3.2 API Data Service

```python
import aiohttp

async def fetch_data(**params):
    url = params.get("url")
    if not url:
        return {"error": "url is required"}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(10)) as resp:
                data = await resp.json()
        return {"status": resp.status, "data": data}
    except Exception as e:
        return {"error": str(e)}
```

### 3.3 Weather Service (wttr.in)

```python
import aiohttp

async def get_weather(**params):
    city = params.get("city", "Shanghai")
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(10)) as resp:
                data = await resp.json()
        
        # Note: wttr.in returns structure at data.current_condition
        c = data.get("data", {}).get("current_condition", [{}])[0]
        return {
            "city": city,
            "temp": int(c.get("temp_C") or 0),
            "condition": c.get("weatherDesc", [{}])[0].get("value", "Unknown"),
            "humidity": c.get("humidity")
        }
    except Exception as e:
        return {"error": str(e)}
```

---

## 4. Workflow Examples

### Combining Multiple Services

```python
async def workflow():
    """Complete workflow combining multiple services"""
    client = SkillQueryClient("ws://localhost:8765")
    await client.connect()
    
    services = await client.discover()
    
    # Find required services
    weather = next((s for s in services if "weather" in s.get("name", "")), None)
    images = next((s for s in services if "image" in s.get("name", "")), None)
    
    results = {}
    
    # Call weather service
    if weather:
        w = await client.call_service(weather.get("skill_id"), "get_weather", {"city": "Shanghai"})
        results["weather"] = w.get("result", {})
    
    # Call image service
    if images:
        i = await client.call_service(images.get("skill_id"), "list_images", {"limit": 10})
        results["images"] = i.get("result", {})
    
    await client.disconnect()
    return results
```

---

## 5. Environment Configuration

### Install Dependencies

```bash
pip install websockets aiohttp
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| HUB_WS_URL | ws://localhost:8765 | Hub WebSocket address |
| WORKSPACE_DIR | /home/t/.../workspace-subagentX | Working directory |

### Start Hub Server (Optional)

```bash
cd Claw-Service-Hub
python -m server.main

# WebSocket: ws://0.0.0.0:8765
# REST API: http://0.0.0.0:3765
```

---

## 6. Troubleshooting

### Issue 1: ImportError

**Error**: `ModuleNotFoundError: No module named 'client'`

**Fix**: Set sys.path correctly
```python
import os
import sys
WORKSPACE_DIR = os.getenv('WORKSPACE_DIR', '/home/t/.openclaw/workspace-subagentX')
sys.path.insert(0, WORKSPACE_DIR)
from client.client import LocalServiceRunner
```

### Issue 2: Service Registered but Cannot Be Called

**Check**:
1. Is the Provider process still running?
2. Is the method name correct (case-sensitive)?
3. Is the parameter format correct?

### Issue 3: API Returns None

**Common Cause**: Data structure parsing error

**Fix**: Print raw data first to confirm structure
```python
async def get_data(**params):
    url = params.get("url")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    print(f"Raw data: {data}")  # Add this debug line
    # Then parse based on actual structure
    return {"data": data}
```

### Issue 4: Service Not Found

**Fix**: List all services first
```python
services = await client.discover()
for s in services:
    print(f"{s.get('name')}: {s.get('skill_id')}")
```

### Issue 5: Return Value Must Be Dict

**Error**: `TypeError: ... got an unexpected keyword argument`

**Fix**: Handlers must return dict
```python
async def wrong():  # Wrong
    return "string"

async def right(**params):  # Correct
    return {"result": "value"}
```

### Issue 6: Return Value Wrapped in 'result'

**现象**: After calling service, returns `{'result': {'actual_data': '...'}}`

**说明**: Hub wraps the handler's returned dict in the 'result' field

**Fix**: Use the return value directly, or extract as needed
```python
result = await client.call_service(service_id, "method", params)
# result = {'result': {'temp': 25, 'city': 'Beijing'}}

# Method 1: Use directly (recommended)
data = result  # Already unpacked data

# Method 2: If explicit extraction needed
if 'result' in result:
    data = result['result']
```

---

## 7. Minimal Examples

### Provider (5 lines)

```python
import asyncio, os, sys
sys.path.insert(0, os.getenv('WORKSPACE_DIR','.'))
from client.client import LocalServiceRunner

async def hello(**p): return {"msg":"Hello!"}
r = LocalServiceRunner("demo","Demo Service",os.getenv("HUB_WS_URL","ws://localhost:8765"))
r.register_handler("hello", hello)
asyncio.run(r.run())
```

### Consumer (6 lines)

```python
import asyncio, os, sys
sys.path.insert(0, os.getenv('WORKSPACE_DIR','.'))
from client.skill_client import SkillQueryClient

async def main():
    c = SkillQueryClient()
    await c.connect()
    print([s.get("name") for s in await c.discover()])
    await c.disconnect()
asyncio.run(main())
```

---

## 8. File Structure

```
Claw-Service-Hub/
├── client/
│   ├── client.py           # LocalServiceRunner, ToolServiceClient
│   ├── skill_client.py     # SkillQueryClient
│   └── management_client.py
├── skills/
│   └── hub-client/
│       └── SKILL.md        # This file
└── server/
    └── main.py             # Hub Server
```

---

## 9. Publishing Flow

1. Ensure Hub Server is running (`ws://localhost:8765`)
2. Provider: Run `python your_service.py` to register service
3. Consumer: Connect to Hub to discover services
4. Consumer: Call service to get results

---

## 10. Key Authorization Mechanism (Optional)

### 10.1 Overview

Optional key authorization mechanism for controlling service access.

**Features**:
- Time dimension: Key validity period (customizable by Provider)
- Count dimension: Maximum call count (customizable by Provider)
- Dual verification: Provider self-management + Hub verification

### 10.2 Provider Side - Set Lifecycle Policy

```python
from client.client import LocalServiceRunner

# Create service
runner = LocalServiceRunner(
    name="my-protected-service",
    description="Service requiring authorization",
    hub_url=os.getenv("HUB_WS_URL", "ws://localhost:8765")
)

# Set default lifecycle policy
runner.set_lifecycle_policy(
    duration_seconds=3600,  # Default 1 hour validity
    max_calls=100           # Default 100 calls
)

# Set custom policy (optional)
runner.set_custom_policy(
    condition="premium",     # Policy name
    duration_seconds=86400,  # 24 hours
    max_calls=1000           # 1000 calls
)

# Register method
async def get_data(**params):
    return {"data": "secret data"}

runner.register_handler("get_data", get_data)

# Start service
print(f"🚀 Starting authorized service...")
await runner.run()
```

### 10.3 Consumer Side - Request Key and Call

```python
from client.skill_client import SkillQueryClient

async def main():
    client = SkillQueryClient(
        hub_url=os.getenv("HUB_WS_URL", "ws://localhost:8765")
    )
    await client.connect()
    
    # Discover services
    services = await client.discover()
    target = next((s for s in services if "protected" in s.get("name", "")), None)
    
    if not target:
        print("Service not found")
        return
    
    service_id = target.get("skill_id")
    
    # Method 1: Direct call (if service doesn't require Key)
    # result = await client.call_service(service_id, "get_data", {})
    
    # Method 2: Request Key first, then call (recommended)
    key_info = await client.request_key(
        service_id=service_id,
        purpose="Daily data query"
    )
    
    if key_info.get("success"):
        key = key_info["key"]
        lifecycle = key_info["lifecycle"]
        
        print(f"✅ Key obtained successfully")
        print(f"   Key: {key[:20]}...")
        print(f"   Validity: {lifecycle.get('remaining_time')} seconds")
        print(f"   Remaining calls: {lifecycle.get('remaining_calls')} times")
        
        # Call service with Key
        result = await client.call_service(
            service_id=service_id,
            method="get_data",
            params={},
            key=key  # Carry the Key
        )
        
        print(f"📥 Result: {result}")
    else:
        print(f"❌ Key request failed: {key_info.get('reason')}")
    
    await client.disconnect()

asyncio.run(main())
```

### 10.4 Handling Key Verification Failure

```python
async def call_with_fallback(client, service_id, method, params):
    """Call with automatic retry"""
    
    # Try without Key first
    result = await client.call_service(service_id, method, params)
    
    # Check if Key is required
    if result.get("error") and "Key" in result.get("error", ""):
        print("Key required, requesting authorization...")
        
        key_info = await client.request_key(service_id, "Auto request")
        if key_info.get("success"):
            key = key_info["key"]
            # Retry with Key
            result = await client.call_service(
                service_id, method, params, key=key
            )
    
    return result
```

### 10.5 Message Protocol

| Message Type | Direction | Description |
|-------------|-----------|-------------|
| lifecycle_policy | Provider→Hub | Register lifecycle policy |
| key_request | Consumer→Hub→Provider | Request Key |
| key_response | Provider→Hub→Consumer | Return Key (approve/reject) |
| key_revoke | Provider→Hub | Revoke Key |
| call_service (with key) | Consumer→Hub | Call service with Key |

### 10.6 Lifecycle Parameters

```python
# Provider registers policy
{
    "duration_seconds": 3600,    # Validity duration (seconds)
    "max_calls": 100,             # Maximum call count
    "custom_policies": {         # Optional: custom policies
        "premium": {
            "duration_seconds": 86400,
            "max_calls": 1000
        }
    }
}

# Key verification result
{
    "valid": True,
    "key": "key_abc123...",
    "lifecycle": {
        "expires_at": "2026-03-20T03:47:00Z",
        "max_calls": 100,
        "call_count": 5,
        "remaining_calls": 95,
        "remaining_time": 3200
    }
}
```

### 10.7 Subagent Usage Tips

**For Provider (Service Publisher)**:
1. If service requires authorization, set reasonable limits in `set_lifecycle_policy`
2. Recommended defaults: `max_calls=100`, `duration_seconds=3600`
3. Can set different policies for different consumers

**For Consumer (Service Caller)**:
1. Try direct call first, request Key if it fails
2. Save Key to avoid repeated requests
3. Check `lifecycle.get('remaining_calls')` to avoid running out of calls
4. Watch `lifecycle.get('remaining_time')` and renew as needed

---

## License

MIT License

Copyright (c) 2026 OpenClaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.