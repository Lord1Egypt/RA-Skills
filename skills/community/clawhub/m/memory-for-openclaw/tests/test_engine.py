"""Test the memory engine"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import sys; sys.path.insert(0, 'scripts'); from memory_engine import MemoryStore

s = MemoryStore()
print(f"总记忆: {s.stats()['total_memories']} 条")
print()

# Save some context about what we're doing now
s.remember(
    content="Decision: Building Long-Term Memory skill for OpenClaw. Target product for OpenClaw users struggling with context loss between sessions.",
    tags=["decision", "openclaw", "memory-skill"],
    importance=9,
    source="manual",
    project="long-term-memory-skill"
)
s.remember(
    content="Architecture: SQLite + FTS5 full-text search + simple embedding. Three-layer storage: memories, sessions, tags.",
    tags=["tech", "architecture"],
    importance=8,
    source="manual",
    project="long-term-memory-skill"
)

# Search
results = s.search("OpenClaw memory skill", limit=5)
print(f"Search found {len(results)} results:")
for m in results:
    print(f"  [{m.importance}/10] {m.content[:120]}")

print()
s2 = s.stats()
print(f"Total memories: {s2['total_memories']}")
print(f"Total sessions: {s2['total_sessions']}")
