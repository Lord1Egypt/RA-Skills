import json
import asyncio
import os
import http.client
from urllib.parse import urlparse

# Protocol: Hardened Async Execution for Hive-Commander
# Ensures zero-leak session propagation and isolated worker output.

async def run_worker(worker_data, session):
    """Isolated Node Execution Logic"""
    worker_id = worker_data['id']
    role = worker_data['role']
    
    # Telemetry Output
    print(f"[NODE_{worker_id}] INIT | Role: {role}")
    
    url = urlparse(session['base_url'])
    host = url.netloc
    path = f"{url.path}/chat/completions".replace("//", "/")
    
    headers = {
        "Authorization": f"Bearer {session['api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": session['model'],
        "messages": [
            {"role": "system", "content": worker_data['prompt']},
            {"role": "user", "content": worker_data['query']}
        ],
        "temperature": 0.5 # Low temperature for logical consistency
    }

    try:
        conn = http.client.HTTPSConnection(host, timeout=120)
        conn.request("POST", path, json.dumps(payload), headers)
        response = conn.getresponse()
        
        if response.status != 200:
            raise Exception(f"HTTP_STATUS_ERROR_{response.status}")
            
        data = json.loads(response.read().decode())
        content = data['choices'][0]['message']['content']
        
        # Atomic Write to Workspace
        output_path = os.path.expanduser(f"~/.openclaw/swarm_tmp/worker_{worker_id}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"--- ROLE: {role} ---\n\n{content}")
            
        print(f"[NODE_{worker_id}] SUCCESS | Data serialized.")
    except Exception as e:
        print(f"[NODE_{worker_id}] CRITICAL_ERROR | {e}")

async def main():
    config_path = os.path.expanduser("~/.openclaw/swarm_tmp/task_config.json")
    if not os.path.exists(config_path):
        print("[I/O_ERROR] task_config.json not found.")
        return

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            
        # P4 Execution: Concurrent Dispatch via asyncio
        tasks = [run_worker(w, config['session']) for w in config['workers']]
        await asyncio.gather(*tasks)
        print("[SWARM_SUCCESS] All nodes processed.")
    except Exception as e:
        print(f"[SYSTEM_FAILURE] Kernel Panic: {e}")

if __name__ == "__main__":
    asyncio.run(main())