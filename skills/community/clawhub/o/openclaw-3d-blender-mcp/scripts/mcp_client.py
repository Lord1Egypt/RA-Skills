#!/usr/bin/env python3
"""
Blender MCP Client - Uses proper MCP/JSON-RPC 2.0 protocol
"""

import socket
import json
import sys
import time

HOST = '8.tcp.ngrok.io'
PORT = 16325

def send_mcp_command(method, params=None):
    """Send MCP protocol command"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(20)
    
    try:
        print(f"📡 Conectando a {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        print("✅ Conectado")
        
        # MCP uses JSON-RPC 2.0
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        print(f"📤 Enviando: {method}")
        message = json.dumps(request) + '\n'
        sock.sendall(message.encode())
        
        # Dar tiempo para procesar
        time.sleep(0.5)
        
        # Leer respuesta
        sock.settimeout(10)
        try:
            data = sock.recv(131072)
            if data:
                response = data.decode()
                print(f"📥 Respuesta: {len(response)} bytes")
                print("="*60)
                print(response)
                print("="*60)
                
                # Parsear
                try:
                    result = json.loads(response.strip())
                    if 'result' in result:
                        print("✅ SUCCESS!")
                        return json.dumps(result['result'], indent=2)
                    elif 'error' in result:
                        print(f"❌ ERROR: {result['error']}")
                except:
                    pass
                return response
            else:
                print("❌ Sin datos")
                return None
        except socket.timeout:
            print("⏱️ Timeout esperando respuesta")
            return None
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return None
    finally:
        sock.close()

if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "get_scene_info"
    result = send_mcp_command(method)
    print(f"\nResultado: {result}")
