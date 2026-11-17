# API 参考（程序化集成）

> 供想在 Python 内直接调用核心函数的用户/agent。所有函数纯标准库、零网络。
> CLI 优先场景请直接用命令行（见 SKILL.md）；本文档面向需要嵌入自己管线的人。

## hxt_core

```python
import sys
sys.path.insert(0, "<技能目录>/scripts")
import hxt_core
```

### hxt_core.scan(text, lang=None, profile="academic") → dict

风格特征扫描（≤1MB 文本）。

- `text`：str，待扫文本（必填）
- `lang`：`"zh"|"en"|"mix"|None`——None 时自动检测
- `profile`：`"academic"`（默认，论文口径）| `"general"`（八股/公文信号 ×0.4）
- 返回：`{"score": int 0-100, "level": "低|中|高|极高", "critical_hit": bool,
  "lang": str, "profile": str, "units": float, "sentences": int,
  "categories": {cat: {"label", "count", "weight", "samples", "auto_fixable"}},
  "guards_applied": [...], "stats": {"burstiness_cv", "connector_density", ...},
  "suggestions": [{"from", "to"}], "honest_note"}`

```python
r = hxt_core.scan("这个方案为业务赋能，打法清晰。")
print(r["score"], r["level"], r["categories"].get("zh_jargon", {}).get("count"))
```

### hxt_core.scan_chunked(text, lang=None, profile="academic") → dict

超大文本分块扫描（>1MB 自动启用；CLI 的 detect/pipeline 对 >1MB 输入自动走本函数）。
返回结构同 scan，额外带 `"chunked": 块数`；跨块边界的结构信号可能少量漏检（报告标注）。

### hxt_core.read_text(path, max_mb=50.0) → str

健壮文本读取：大小上限 / 二进制 NUL 检测 / BOM 剥离 / 乱码占比守卫 / .docx 直读。
失败抛 `ValueError`（消息含处置建议）或 `OSError`。

```python
try:
    text = hxt_core.read_text("稿件.docx")
except ValueError as e:
    print("输入不合规:", e)
```

### hxt_core.build_suggestions(orig, scan_result, guide) → str

把 scan 结果转为修订建议工作单（markdown 字符串：类别/样本/处理原则/指南锚点）。
`guide` 传指南相对路径（如 `references/style_guide_zh.md`）。

### hxt_core.verify_integrity 相关

完整性守卫的函数入口在 `verify.verify(orig, new, terms=None, max_len_change=25.0,
max_cjk_shift=0.12) -> {"ok": bool, "violations": [...], "warnings": [...], "stats": {...}}`
（`import verify as vf`）。退出码契约只属于 CLI 层。

## transform / extract_terms / verify（CLI 模块复用）

| 函数 | 说明 |
|---|---|
| `transform.load_fixes(lang=None, aggressive=False)` | 返回 (rx, repl, note, guards) 修复列表 |
| `transform.apply_auto_fixes(text, fixes)` | 应用机械修复（带术语守卫），返回 (text, applied) |
| `transform.drop_flagged_sentences(text)` | 客套句/截止声明整句删除（覆盖律+数字保护），返回 (text, removed) |
| `extract_terms.extract(orig, min_count=2, cap=40)` | 术语候选抽取，返回 [(term, count, kind)] |
| `verify.load_terms(path)` | 术语表加载（BOM/守卫内建） |

所有函数零网络、零环境变量、只读写调用方显式传入的路径。
