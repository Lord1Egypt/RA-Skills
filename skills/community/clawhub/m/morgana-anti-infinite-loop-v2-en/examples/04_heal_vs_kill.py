"""
🌀 Example 4: Healing vs Pause vs Hard-kill.

The guard has 3 intervention modes. Choose based on your context.
"""

import time
from anti_loop import AntiLoop


def demo_mode(mode: str, max_iter: int = 5):
    print(f"\n=== Mode: {mode} ===")
    guard = AntiLoop(mode=mode, max_iter=max_iter)
    for i in range(max_iter):
        result = guard.observe("search for X", intent="find X")
        if result["intervene"]:
            d = result["directive"]
            print(f"  iter {i+1}: {d['action']} → {d.get('message', d.get('system_message', d))[:80]}")
            if mode == "pause":
                # In real life: time.sleep(d["duration_seconds"])
                print(f"           (would sleep {d['duration_seconds']}s)")
            elif mode == "hard_kill":
                print("           (would raise/abort here)")
                break
            elif mode == "heal":
                # In real life: inject d["system_message"] into the LLM context
                pass
        else:
            print(f"  iter {i+1}: ok")


if __name__ == "__main__":
    demo_mode("heal")
    demo_mode("pause")
    demo_mode("hard_kill")
