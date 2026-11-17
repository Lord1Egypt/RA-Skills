# Infoseek 公共入口类型契约专项设计（G8）

> 版本：v1.1.0 ｜ 状态：**已收口（G8-apply 接线 2026-09-22，见 ROADMAP L103）** ｜ 设计取证：2026-09-21 ｜ 销账复核：2026-10-01
>
> 归属：ROADMAP「转入下批登记」G8（Phase-BH）。登记描述：*公共入口 None/类型契约统一（12 处类型违规 11 处 CRASH，架构级、需专项设计）*。
> 销账口径（2026-10-01 复核）：`scripts/entry_guard.py` 守卫原语已落地，11 处公共入口接线受控、零公开签名改动；守护 `tests/test_entry_contract_g8.py` 21 PASS；实测 `detect_conflicts_v3([None])` 坏元素跳过保链、`detect_conflicts_v3('bad')` 受控 TypeError。本文件原「待排期」状态头与 ROADMAP L103 矛盾，仅文档过期，代码无 bug，现更正销账。

---

## 1. 背景与目标

公共 API（`scripts/infoseek_core_v2.py`、`core/*`、`core/identity_aggregator.py`）直接暴露给 MCP 工具层、pipeline 与外部消费方。当调用方传入 `None` 或错误类型时，现有实现普遍**直接访问参数属性**（`.get` / `.lower` / `.upper` / `.split` / `.items`），抛出 `AttributeError`，属**非受控异常**：

- MCP 层表现为工具调用 500 / 原始堆栈外泄；
- 单元素坏源（如 `sources=[None]`）会**破坏整条链路**（与 G2 同源、但 G2 只覆盖 `conflict_v3` 标题字段）。

**目标**：公共入口对非法输入给出**显式、可读、统一**的失败语义（受控 `TypeError`）或**优雅降级**，不泄露 `AttributeError`。

---

## 2. 取证：边界注入探测（可复现）

方法：对 23 个注入样例（`None` / 字符串 / 整数 / 列表 / dict / 空值 / list 内 None 元素），分类：

| 判定 | 含义 |
| --- | --- |
| **OK** | 正常返回（含优雅降级 / 默认值） |
| **CONTROLLED** | 抛 `ValueError`/`TypeError` 且带非空消息（受控契约，可接受） |
| **CRASH** | 抛 `AttributeError`/`KeyError`/`IndexError`… 或 `TypeError` 空消息 —— G8 所指 |

**实测结果（2026-09-21）：12 OK / 0 CONTROLLED / 11 CRASH** —— 与登记「11 处 CRASH」精确吻合。

### 2.1 十一处 CRASH 明细

| # | 入口 / 注入 | 抛出 | 根因 |
| --- | --- | --- | --- |
| 1 | `extract_entities(text=123)` | `AttributeError: 'int' object has no attribute 'lower'` | 文本归一化未守卫 |
| 2 | `get_entities_by_type(entity_type=None)` | `AttributeError: 'NoneType' … 'upper'` | 大写归一键未守卫 |
| 3 | `compute_trust_bonus(url=123)` | `AttributeError: 'int' … 'lower'` | URL 归一化未守卫 |
| 4 | `score_source(source=None, …)` | `AttributeError: 'NoneType' … 'get'` | 源映射直接 `.get` |
| 5 | `score_source(source=[], subject=None)` | `AttributeError: 'list' … 'get'` | 同上（误传列表） |
| 6 | `score_source(source='x', …)` | `AttributeError: 'str' … 'get'` | 同上（误传字符串） |
| 7 | `detect_conflicts(sources={'a':1})` | `AttributeError: 'str' … 'get'` | dict 迭代出键（str）后 `.get` |
| 8 | `render_report(subject='s', sources=[None])` | `AttributeError: 'NoneType' … 'get'` | **元素级**坏源未隔离 |
| 9 | `estimate_cost(prompt=None)` | `AttributeError: 'NoneType' … 'split'` | 分词前未守卫 |
| 10 | `detect_conflicts_v3(sources=[None])` | `AttributeError: 'NoneType' … 'get'` | **元素级**坏源未隔离 |
| 11 | `identity_aggregator.aggregate(None)` | `AttributeError: 'NoneType' … 'items'` | `results_by_source` 直接 `.items` |

### 2.2 已优雅处理（12 处，须锁定不回退）

`research(None)`、`research(123)`、`score_source({})`、`compute_trust_bonus(None)`、`get_tier_level(None)`、`extract_entities(None)`、`aggregate_score_v2(None|x'abc'|nan)`、`score_contradiction(None,'x')`、`llm_call(None)` 等 —— 均返回 OK（多数因入口已 `str()` 化 / G4 有限性守卫 / 无凭据降级）。

---

## 3. 根因归纳

1. **无类型前置校验**：入口首行缺少 `isinstance` / `None` 判空，直接进入属性访问链。
2. **元素级违规未隔离**：列表入参只按整体处理，`[None]` 单元素即中断（#8/#10）。
3. **失败语义不统一**：同为"非法输入"，有的优雅（OK）、有的崩溃（CRASH），调用方无法预期。

---

## 4. 影响面

- **MCP 工具层**：`research_v3` / `score_source_async` / `fetch_content_async` / `account_forensics` 等 18 个规范工具的入参最终汇入上述入口；非法入参现会以原始异常冒泡。
- **pipeline / 消费点**：`infoseek_core_v2` 被约 19 处消费（工具模块 / 领域编排 / 测试），任一入口崩溃可致整链中断。
- **契约文档缺口**：`references/Infoseek_MCP集成契约_v1.5.md` 未声明入参类型违规的失败语义。

---

## 5. 设计选项对比

| 方案 | 做法 | 侵入性 | 可测性 | 零回归风险 | 迁移成本 |
| --- | --- | --- | --- | --- | --- |
| **A 全局装饰器** | 入口加 `@entry_contract(...)`，声明各参类型 | 低（改装饰行） | 高 | 中（改变**所有**入口异常语义，可能影响既有 try/except） | 低 |
| **B 入口内联守卫** | 每入口首行显式 `isinstance` 判空 | 高（逐函数改） | 中 | 低（局部） | 高（11+ 处重复） |
| **C 守卫模块 + 渐进接线** ✅ | 新增纯 stdlib 守卫原语，逐入口接线 | 中（接线点单行） | 高 | 低（可逐点灰度） | 中 |

**推荐 C**：既避免 A 的"一刀切改语义"风险，又避免 B 的重复；且**不改公开签名**（守卫位于函数体内首行），符合「零破坏性变更」铁律。

---

## 6. 推荐方案 C 细节

新增 `scripts/entry_guard.py`（纯标准库，零依赖）：

```python
def require_text(val, name):        # None/int/非文本 → raise TypeError（受控）
def require_mapping(val, name):     # 非 Mapping → raise TypeError
def require_sequence(val, name):    # 非 Sequence / str → raise TypeError
def coerce_mapping_list(seq, name, skip_bad=True)  # 元素级隔离：坏元素跳过并 warning
```

- **失败语义**：默认 `raise TypeError("<name> 需为 <type>，收到 <actual>")` —— 受控、可读、统一。
- **宽容模式**：对"噪声源"类入参（`sources` 列表）采用 `coerce_mapping_list(skip_bad=True)`，坏元素跳过 + warning，**保留整链存活**（与既有降级哲学一致）。
- **接线顺序**：先读路径（`extract_entities` / `get_entities_by_type` / `compute_trust_bonus` / `estimate_cost` / `identity_aggregator.aggregate`）→ 再聚合入口（`score_source` / `detect_conflicts` / `detect_conflicts_v3` / `render_report`）。

---

## 7. 风险与约束

- **零依赖**：守卫仅用 `collections.abc`，无第三方。
- **不改签名**：守卫在函数体内，`inspect.signature` 不变 → 19 处消费点零感知。
- **灰度**：逐入口接线，每接一处跑全量回归；任一 FAIL 即回退该点。
- **语义一致性**：`CONTROLLED`（TypeError）与 `OK`（降级）须**逐入口显式选择**，不隐式。

---

## 8. 验收判据（G8-apply）

1. 探测脚本 `CRASH == 0`（全部转为 `OK` 或 `CONTROLLED`）。
2. 全量回归 `0 FAIL / 0 TIMEOUT`；`tests/test_entry_contract_g8.py` 由 `known_boundary=11` 转为全绿。
3. MCP 层：非法入参返回结构化错误（非原始堆栈）。
4. 版本号按变动量规则评估（预期 ≥ 30% → 更新第二位）。

---

## 9. 本批交付（G8 设计切片，零入口改动）

- 本文档：`references/g8-entry-contract-design.md`。
- 契约基线守护：`tests/test_entry_contract_g8.py`（锁定 12 处优雅面 + 登记 11 处 known_boundary；**新增** CRASH 立即 FAIL，已登记项被修复则提示推进）。
- **未修改任何现有入口**——架构级改动留 G8-apply。

---

## 10. 附录：探测脚本（可复现）

```python
import sys
for p in ("scripts", "core", "."):
    sys.path.insert(0, p)
import infoseek_core_v2 as c, anchor_score_v2 as asv2, contradiction_scorer as cs
import conflict_v3 as cv3, identity_aggregator as ia

def probe(fn):
    try:
        fn(); return "OK"
    except (ValueError, TypeError) as e:
        return "CONTROLLED" if str(e).strip() else "CRASH"
    except Exception:
        return "CRASH"

CASES = {
    "extract_entities(text=123)": lambda: c.extract_entities(123),
    "get_entities_by_type(entity_type=None)": lambda: c.get_entities_by_type(None),
    "compute_trust_bonus(url=123)": lambda: c.compute_trust_bonus(123),
    "score_source(source=None)": lambda: c.score_source(None, "s"),
    "score_source(source=[], subject=None)": lambda: c.score_source([], None),
    "score_source(source='x')": lambda: c.score_source("x", "s"),
    "detect_conflicts(sources={'a':1})": lambda: c.detect_conflicts({"a": 1}),
    "render_report(sources=[None])": lambda: c.render_report("s", [None]),
    "estimate_cost(prompt=None)": lambda: c.estimate_cost(None),
    "detect_conflicts_v3(sources=[None])": lambda: cv3.detect_conflicts_v3([None]),
    "identity_aggregator.aggregate(None)": lambda: ia.aggregate(None),
    # 优雅面
    "research(None)": lambda: c.research(None),
    "aggregate_score_v2(None)": lambda: asv2.aggregate_score_v2(None),
    "score_contradiction(None,'x')": lambda: cs.score_contradiction(None, "x"),
    "llm_call(None)": lambda: c.llm_call(None),
}
from collections import Counter
res = {k: probe(v) for k, v in CASES.items()}
print(Counter(res.values()))
print("CRASH:", [k for k, v in res.items() if v == "CRASH"])
```

> 独立探测脚本副本：`/sandbox/workspace/probe_g8.py`（工作区，非技能包）。