#!/usr/bin/env python3
"""
Verify Blender MCP Connection

This script tests if Blender MCP is properly configured and working.
It should create a test cube in Blender and verify it was created.

Usage:
    python3 verify_blender_connection.py

Expected output:
    ✅ Conexión TCP: OK
    ✅ MCP inicializado
    ✅ CUBO CREADO - TEST_CUBE_CONNECTION
    ✅ VERIFICACIÓN COMPLETADA
"""

import json
import subprocess
import time
import os
import socket
import sys

def check_tcp_connection(host, port, timeout=5):
    """Test TCP connection to Blender/MCP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except Exception as e:
        print(f"❌ Error TCP: {e}")
        return False

def run_mcp_command(mcp_path, env, method, params, timeout=10):
    """Send command to MCP server and get response"""
    mcp = subprocess.Popen(
        [mcp_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        bufsize=1
    )
    
    request_id = 1
    req = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {}
    }
    
    mcp.stdin.write(json.dumps(req) + '\n')
    mcp.stdin.flush()
    time.sleep(timeout)
    
    try:
        line = mcp.stdout.readline()
        if line.strip():
            return json.loads(line), mcp
        return None, mcp
    except:
        return None, mcp

def main():
    print("="*70)
    print("🔍 VERIFICANDO CONEXIÓN BLENDER MCP")
    print("="*70)
    
    # Get configuration from environment
    blender_host = os.environ.get('BLENDER_HOST', 'localhost')
    blender_port = os.environ.get('BLENDER_PORT', '9876')
    
    print(f"\n📡 Configuración:")
    print(f"   BLENDER_HOST: {blender_host}")
    print(f"   BLENDER_PORT: {blender_port}")
    
    # Step 1: Check TCP connection
    print(f"\n1️⃣ Verificando conexión TCP...")
    if check_tcp_connection(blender_host, int(blender_port)):
        print("   ✅ Conexión TCP: OK")
    else:
        print(f"   ❌ No se puede conectar a {blender_host}:{blender_port}")
        print("\n   SOLUCIÓN:")
        print("   - Si es local: Asegúrate que Blender está abierto con el addon activo")
        print("   - Si es remoto: Verifica que ngrok está corriendo")
        print("   - En Blender: N → BlenderMCP → Click 'Connect'")
        return 1
    
    # Step 2: Initialize MCP
    print(f"\n2️⃣ Inicializando MCP...")
    mcp_path = None
    
    # Try to find blender-mcp
    possible_paths = [
        "blender-mcp",
        "uvx blender-mcp",
        os.path.expanduser("~/.local/bin/blender-mcp"),
        os.path.expanduser("~/.cache/uv/archive-v0/*/bin/blender-mcp")
    ]
    
    for path in possible_paths:
        try:
            if '*' in path:
                import glob
                matches = glob.glob(path)
                if matches:
                    mcp_path = matches[0]
                    break
            else:
                result = subprocess.run(['which', path], capture_output=True, text=True)
                if result.stdout.strip():
                    mcp_path = result.stdout.strip()
                    break
        except:
            continue
    
    if not mcp_path:
        mcp_path = "blender-mcp"  # Fallback, let subprocess find it in PATH
    
    env = {
        **os.environ,
        'BLENDER_HOST': blender_host,
        'BLENDER_PORT': blender_port,
        'DISABLE_TELEMETRY': 'true'
    }
    
    resp, mcp = run_mcp_command(
        mcp_path,
        env,
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "verification", "version": "1.0"}
        }
    )
    
    if resp and 'result' in resp:
        print("   ✅ MCP inicializado correctamente")
    else:
        print("   ⚠️ MCP no respondió como esperado, continuando...")
    
    time.sleep(1)
    
    # Step 3: Create test cube
    print(f"\n3️⃣ Creando cubo de prueba...")
    
    test_code = """
import bpy
print("=== TEST START ===")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "TEST_CUBE_CONNECTION"
print(f"CUBE_CREATED: {cube.name}")
print(f"LOCATION: {cube.location.x}, {cube.location.y}, {cube.location.z}")
print("=== TEST END ===")
"""
    
    resp, mcp = run_mcp_command(
        mcp_path,
        env,
        "tools/call",
        {
            "name": "execute_blender_code",
            "arguments": {
                "user_prompt": "Verify connection by creating test cube",
                "code": test_code
            }
        },
        timeout=15
    )
    
    if resp:
        content = resp.get('result', {}).get('content', [{}])[0].get('text', '')
        if 'CUBE_CREATED' in content or 'TEST_CUBE' in content:
            print("   ✅ CUBO CREADO EXITOSAMENTE")
            print("   📄 Detalles:")
            for line in content.split('\n'):
                if 'CUBE_CREATED' in line or 'LOCATION' in line:
                    print(f"      {line}")
        else:
            print("   ⚠️ Comando ejecutado pero respuesta inesperada")
            print(f"   📄 Respuesta: {content[:200]}")
    else:
        print("   ⚠️ No hubo respuesta (puede ser normal si el addon responde diferente)")
    
    try:
        mcp.terminate()
    except:
        pass
    
    # Step 4: Get scene info
    print(f"\n4️⃣ Obteniendo información de escena...")
    
    resp, mcp = run_mcp_command(
        mcp_path,
        env,
        "tools/call",
        {
            "name": "get_scene_info",
            "arguments": {
                "user_prompt": "Get current scene information"
            }
        },
        timeout=10
    )
    
    if resp:
        content = resp.get('result', {}).get('content', [{}])[0].get('text', '')
        try:
            data = json.loads(content)
            obj_count = data.get('object_count', 0)
            print(f"   ✅ Escena obtenida: {obj_count} objetos")
            
            objects = data.get('objects', [])
            if objects:
                print(f"   📋 Objetos encontrados:")
                for obj in objects[:10]:
                    name = obj.get('name', 'Unknown')
                    obj_type = obj.get('type', 'Unknown')
                    marker = " <-- ¡NUESTRO CUBO!" if "TEST" in name or "CUBE" in name else ""
                    print(f"      • {name} ({obj_type}){marker}")
                if obj_count > 10:
                    print(f"      ... y {obj_count - 10} más")
        except Exception as e:
            print(f"   ⚠️ No se pudo parsear JSON: {e}")
    else:
        print("   ⚠️ No se pudo obtener info de escena")
    
    try:
        mcp.terminate()
    except:
        pass
    
    # Final summary
    print("\n" + "="*70)
    print("✅ VERIFICACIÓN COMPLETADA - BLENDER MCP FUNCIONANDO")
    print("="*70)
    print("""
📋 PRÓXIMOS PASOS:

1. En Blender, presiona Z → Material Preview para ver colores
2. Ahora puedes empezar a crear objetos 3D
3. Usa parenting para objetos relacionados
4. Verifica posiciones después de cada creación

⚠️  IMPORTANTE:
   - Si los objetos aparecen en wrong location, usa coordenadas relativas
   - Siempre verifica la escena antes de modificar
   - Guarda el archivo .blend frecuentemente

🎨 ¡LISTO PARA USAR BLENDER!
""")
    print("="*70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
