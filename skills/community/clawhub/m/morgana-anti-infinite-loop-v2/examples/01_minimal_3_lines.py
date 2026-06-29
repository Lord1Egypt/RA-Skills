"""
🌀 Example 1: Minimal 3-line integration (dev solo + Llama local).

Le cas le plus simple : un agent qui retry la même action.
Tu wrap ton agent avec le guard, et c'est tout.
"""

from anti_loop import AntiLoop


# Imagine: a fake agent that keeps retrying the same lookup
def fake_agent_loop(state, action):
    """A minimal agent stub: returns whatever was asked, every time."""
    return action  # no progress, just echoes


if __name__ == "__main__":
    guard = AntiLoop(mode="heal", max_iter=10)

    state = {"messages": [], "intent": "Find user 42"}
    
    for turn in range(6):
        action = "search for user 42"  # agent never varies
        result = guard.observe(action, intent=state["intent"])
        
        if result["intervene"]:
            d = result["directive"]
            print(f"  [turn {turn+1}] 🛑 INTERVENE: {d['action']}")
            if d.get("system_message"):
                print(f"     → {d['system_message']}")
            # In real life: inject d["system_message"] into the LLM context
        else:
            print(f"  [turn {turn+1}] ✅ OK (novelty={result['novelty']:.2f})")
