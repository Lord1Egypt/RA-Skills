# AI Memory Protocol 迭代方法论

## 核心准则（每次迭代前必过）

```
第一性 → 系统性 → 逻辑性 → 结构化 → 简单 → 易用 → 可靠 → 稳定
```

---

## 迭代流程

### 1. 读 changelog — 搞清楚"谁改了什么"

```
head -60 ai_memory_protocol_vX.X.X.py
```
先看 changelog，了解 Leo 加了什么，再动手。

---

### 2. diff 对比 — 找实际改动

```bash
diff ai_memory_protocol_v1.1.4.py ai_memory_protocol_v1.1.5.py | less
```

Leo 可能加了代码但 changelog 没同步，或者 changelog 和代码不一致。

---

### 3. 版本常量验证

```python
grep 'PROTOCOL_VERSION\|DB_VERSION' ai_memory_protocol_v1.1.5.py
```

确认 Python 常量和文件声称的版本号是否一致。

---

### 4. 集成测试 — 每个功能单独验证

测试顺序（发现问题的顺序）：
1. search_count — 最常用
2. get_session_extended — 常用
3. vacuum — 破坏性操作
4. priority_levels 持久化 — 重启测试
5. tag_filter — 边界情况

```python
# 测试模板
import sys, tempfile, os, time
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location('protocol', 'ai_memory_protocol_v1.1.5.py')
mod = module_from_spec(spec)
spec.loader.exec_module(mod)
db_path = tempfile.mktemp(suffix='.db')
sm = mod.SessionManager(db_path)
# ... run tests ...
os.unlink(db_path)
```

---

### 5. Bug 定位 — 从症状到根因

**原则：先隔离层，再修。**

症状 → 哪条路径（LIKE/FTS/DB直接） → 查具体代码行

例如 tag_filter 问题：
- 症状：search_count 返回 0，LIKE 直接执行返回 1
- 原因：search_count 走 LIKE 路径，tag_filter 传了 list 但接口要 string
- 根因：SessionManager 层没有归一化

**不要**：在一堆代码里猜测原因，用 print/查 DB 直接验证。

---

### 6. 修复原则 — 简单优先

能用一行的不在第五行。

| 场景 | 方案 |
|------|------|
| 过度复杂的设计 | 直接还原到上一个能工作的版本 |
| 类型不一致 | 加 isinstance 判断，不改数据结构 |
| 参数归一化 | wrapper 层转换，不改底层接口 |
| 并发问题 | 加锁/加 timeout，不改业务逻辑 |

---

### 7. 更新文档

改完测试 PASS 后必做：
1. 更新源文件 changelog（头部）
2. 新建 `CHANGELOG_vX.X.X.md`
3. 更新 cron job（如有必要）
4. 如果改了常量（PROTOCOL_VERSION/DB_VERSION），必须验证

---

### 8. Cron job 更新

```bash
hermes_cron update e9805661b493 \
  --prompt "cd /opt/claw/hermes/protocol && python3 -c \"
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location('protocol', 'ai_memory_protocol_v1.1.5.py')
mod = module_from_spec(spec)
spec.loader.exec_module(mod)
print(mod.SessionManager().recall_what_now())
\""
```

---

## 常见错误清单

1. **in-place patch** — 改乱了不知道哪个版本是什么。规则：每版新文件，不动旧文件。

2. **修复引入新 bug** — 改了 search_count 但没改 SessionManager wrapper，或者反过来。规则：每个调用链都验证。

3. **版本常量不一致** — 文件名 v1.1.5、标题 v1.1.4、常量 "1.1.5"。规则：三统一。

4. **复杂设计** — 试图一步到位解决所有边界情况。规则：先让核心路径工作，边界情况下一个版本再说。

5. **没测边界** — search_count 用 list 测了但没想到接口要 string。规则：每个参数类型都单独验证。

---

## 文件命名规则

```
ai_memory_protocol_v1.1.5.py     ← 源文件
CHANGELOG_v1.1.5.md              ← changelog
backups/YYYYMMDD_vXXX/           ← 备份
mark_memory.db                   ← 数据库
```

不 in-place patch。不覆盖旧文件。
