"""测试记忆萃取 + 光点神经树。"""
from memoryguard.discover import WorkspaceDiscoverer
from memoryguard.rules import RuleContext
from memoryguard.extractor import MemoryExtractor
from memoryguard.light_graph import LightGraphManager
from pathlib import Path

ws = r"H:\ai\workspace\工具项目\memoryguard\tests\fixtures\workspace"
d = WorkspaceDiscoverer(Path(ws)).discover()
ctx = RuleContext(agrs=d.agrs)
ext = MemoryExtractor(ctx)
claims = ext.extract_all()
print(f"extracted {len(claims)} claims:")
for c in claims[:8]:
    print(f"  [{c.memory_type}] {c.display_label[:40]}")

g = LightGraphManager()
for c in claims:
    g._claims[c.id] = c
g._next_claim_id = max((c.id for c in claims), default=0) + 1
g.fit_vectorizer()
g.attach_all_claims()
g.promote_or_dissolve()
s = g.stats()
print(f"graph stats: {s}")
snap = g.build_live_snapshot()
print(f"snapshot: {len(snap['nodes'])} nodes, {len(snap['edges'])} edges")
print(f"merge suggestions: {len(g.suggest_merge())}")
print("OK")
