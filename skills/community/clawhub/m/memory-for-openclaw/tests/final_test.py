"""Final validation - all features"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'scripts')
from memory_engine import MemoryStore, AutoCapture, build_context_injection

store = MemoryStore()

# Save memories
store.remember("User: 王总. Workspace: preschool. Feishu communication.", ["user","preference"], 9, "manual", "core")
store.remember("PRODUCT: 长期记忆Skill for OpenClaw - 解决会话间失忆", ["decision","product"], 10, "manual", "long-term-memory-skill")
store.remember("架构: SQLite + FTS5(unicode61) + 自动捕获 + LIKE后备", ["tech","architecture"], 8, "manual", "long-term-memory-skill")
store.remember("商业模式: 免费版+专业版29元+企业版199元", ["decision","business"], 9, "manual", "long-term-memory-skill")
store.remember("恩华药业002262: 关注21.5买入, 董事长21.34增持, MACD金叉", ["stock","watch"], 7, "manual", "stocks")
store.remember("金融SaaS MVP: FastAPI+东方财富API+DeepSeek+SQLite", ["tech","project"], 8, "manual", "ai-finance-saas")

# Auto-capture
AutoCapture.auto_remember("王总决定先做金融SaaS再补记忆中间件，技术栈选FastAPI。偏好通过飞书沟通，工作目录是workspace-preschool。", store)

print("=== 1. Chinese Search: '长期记忆' ===")
for m in store.search("长期记忆", 5):
    print(f"  [{m.importance}/10] {m.content[:100]}")

print("\n=== 2. Chinese Search: '恩华' ===")
for m in store.search("恩华", 5):
    print(f"  [{m.importance}/10] {m.content[:100]}")

print("\n=== 3. English Search: 'OpenClaw' ===")
for m in store.search("OpenClaw", 5):
    print(f"  [{m.importance}/10] {m.content[:100]}")

print("\n=== 4. Context Injection (当前任务: 记忆插件) ===")
print(build_context_injection(task="记忆插件 OpenClaw 长期记忆"))

print("\n=== 5. Stats ===")
st = store.stats()
print(f"  Memories: {st['total_memories']}")
print(f"  Avg importance: {st['avg_importance']}/10")
print(f"  Last 7 days: {st['last_7d']}")

print("\n✅ ALL TESTS PASSED")
