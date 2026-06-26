import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from memory_manager import MemoryManager

def test_memory_flow():
    print("=== Testing Memory Core Flow ===")
    
    mm = MemoryManager()
    agent_id = "test_agent"
    
    print("\n[1] Ingesting Work Memory...")
    work_text = "I am a Python Backend Engineer using FastAPI."
    res1 = mm.ingest(agent_id, work_text)
    print(f"Stored: {res1}")
    assert res1['tags']['scene'] == 'coding' or res1['tags']['scene'] == 'work'
    
    print("\n[2] Ingesting Game Memory...")
    game_text = "I play a level 60 Hunter in World of Warcraft."
    res2 = mm.ingest(agent_id, game_text)
    print(f"Stored: {res2}")
    assert res2['tags']['scene'] == 'game'
    
    time.sleep(1)
    
    print("\n[3] Retrieving with Context: 'What is my tech stack?' (Scene: coding)")
    res3 = mm.retrieve(agent_id, "What is my tech stack?", scene="coding")
    print(f"Result: {json.dumps(res3, indent=2)}")
    
    found_work = any("Python" in m['text'] for m in res3['memories'])
    found_game = any("Hunter" in m['text'] for m in res3['memories'])
    
    if found_work and not found_game:
        print("✅ Success: Retrieved work memory, ignored game memory.")
    else:
        print(f"❌ Failure: Work={found_work}, Game={found_game}")
        
    print("\n[4] Retrieving with Context: 'What class do I play?' (Scene: game)")
    res4 = mm.retrieve(agent_id, "What class do I play?", scene="game")
    print(f"Result: {json.dumps(res4, indent=2)}")
    
    found_game_2 = any("Hunter" in m['text'] for m in res4['memories'])
    if found_game_2:
        print("✅ Success: Retrieved game memory.")
    else:
        print("❌ Failure: Did not retrieve game memory.")

    print("\n[5] Cleaning up...")
    mm.forget(res1['id'])
    mm.forget(res2['id'])
    print("Cleanup done.")

if __name__ == "__main__":
    test_memory_flow()
