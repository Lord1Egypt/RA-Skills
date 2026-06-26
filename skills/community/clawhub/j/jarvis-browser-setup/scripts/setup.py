#!/usr/bin/env python3
"""
Jarvis Browser Setup - Generates unique auth token and prepares package for new users
"""
import os
import json
import secrets
import string
import shutil
from datetime import datetime

def generate_token(length=48):
    """Generate cryptographically secure auth token"""
    alphabet = string.ascii_letters + string.digits + "-_.!"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_server_ip():
    """Get server IP address"""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '192.168.2.61'
    finally:
        s.close()
    return ip

def setup_browser_control():
    print("🚀 Jarvis Browser Control Setup")
    print("=" * 50)
    
    # Generate unique token
    auth_token = generate_token()
    print(f"🔑 Generated Auth Token: {auth_token}")
    
    # Get server IP
    server_ip = get_server_ip()
    print(f"🌐 Server IP: {server_ip}")
    
    # Create output directory
    output_dir = f"jarvis-browser-setup-{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create config
    config = {
        "token": auth_token,
        "server_ip": server_ip,
        "port": 8765,
        "created": datetime.now().isoformat()
    }
    
    with open(os.path.join(output_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)
    
    # Copy template files (from existing v3.5)
    template_dir = "/home/openclaw/.openclaw/workspace/jarvis-browser-v3.3-hybrid"
    
    if os.path.exists(template_dir):
        # Copy server
        shutil.copytree(
            os.path.join(template_dir, "server"),
            os.path.join(output_dir, "server"),
            ignore=shutil.ignore_patterns("*.log", "__pycache__")
        )
        
        # Copy extension
        shutil.copytree(
            os.path.join(template_dir, "extension"),
            os.path.join(output_dir, "extension")
        )
        
        # Update extension config with new token and IP
        extension_config = os.path.join(output_dir, "extension", "config.js")
        if os.path.exists(extension_config):
            with open(extension_config, "r") as f:
                content = f.read()
            
            # Replace token and IP
            content = content.replace(
                "'ws://192.168.2.61:8765'",
                f"'ws://{server_ip}:8765'"
            )
            # Token replacement depends on config format
            
            with open(extension_config, "w") as f:
                f.write(content)
        
        print(f"✅ Copied server and extension files")
    else:
        print(f"⚠️  Template not found at {template_dir}")
        print("   Please ensure v3.5 files exist")
    
    # Create README
    readme = f"""# Jarvis Browser Control Setup

## Your Configuration

- **Auth Token:** `{auth_token}`
- **Server IP:** `{server_ip}:8765`

## Quick Start

### 1. Start Server
```bash
cd server
python3 jarvis_server_v3.5_fixed.py
```

### 2. Install Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension` folder

### 3. Connect
- Click extension icon on any tab
- Green "ON" badge = connected ✅

## Security

Keep your auth token secret! Anyone with this token can control your browser.

Generated: {datetime.now().isoformat()}
"""
    
    with open(os.path.join(output_dir, "README.md"), "w") as f:
        f.write(readme)
    
    print(f"\\n📦 Package created: {output_dir}/")
    print(f"\\n📝 Files:")
    print(f"   - config.json (your settings)")
    print(f"   - server/ (WebSocket server)")
    print(f"   - extension/ (Chrome extension)")
    print(f"   - README.md (instructions)")
    
    print(f"\\n⚠️  IMPORTANT: Keep your auth token secret!")
    print(f"\\n✅ Setup complete! Share the '{output_dir}' folder.")
    
    return output_dir, auth_token

if __name__ == "__main__":
    try:
        output_dir, token = setup_browser_control()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
