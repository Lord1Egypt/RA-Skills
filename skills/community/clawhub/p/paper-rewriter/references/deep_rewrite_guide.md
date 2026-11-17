> **何时读我**：拿到 plan 后不知道按什么流程改。
> **最短路径**：照五步执行循环走。
> **回 [INDEX](INDEX.md)**

# 深改操作手册：从计划到验收的执行循环（v3.0.0）

> EN summary: this is the *operational* layer of deep rewriting — how to turn a
> `plan.py` diagnosis into a bounded, verifiable rewrite session. Style rules
> live in `style_guide_zh.md` / `style_guide_en.md`; this sheet defines the
> process: plan → handoff → per-sentence rewrite → verify cadence → acceptance.

## 为什么需要这一页

真实使用反馈与深改实操复盘一致指出：本工具的深改环节由 agent/作者完成，而「怎么把
深改做扎实、可验收」缺一张操作层面的流程页——风格指南管「怎么改」，本页管
「按什么顺序改、改到什么程度停、怎么证明没改坏」。

## 执行循环（五步，可多轮）

```
① 计划     python scripts/plan.py draft.txt --top 15 -o plan.md
              ↳ P0 句级队列（章节归属+命中类别+处理原则+预算投影）
② 交接     python scripts/plan.py draft.txt --top 15 --handoff
          （或 v3.8.0 一句命令：python scripts/pipeline.py draft.txt -o clean.txt --handoff 交接块.md）
              ↳ 深改交接块：逐句「原句+操作指令」，含守卫铁律与验收命令
③ 逐句深改  按交接块顺序改——每句只做指令列出的操作，不顺手加戏
④ 校验节拍  每改 3-5 句：python scripts/verify.py draft.txt step2.txt --terms terms.txt
              ↳ 任一 GUARD/ERROR → 回滚该句，改法降级（整句重写→局部替换）
⑤ 收口     python scripts/compare.py draft.txt step2.txt
           python scripts/stylecheck.py step2.txt --compare draft.txt
              ↳ 量化验收：特征下降 + 完整性 PASS + 画像档位改善
```

## 每句怎么改（操作优先级）

1. **删除优先**：八股开场（众所周知/综上所述/值得注意的是）、聊天客套、知识
   截止声明——直接删，不需要替身。
2. **合并次之**：「不仅X，而且Y」→「X，且Y」；同主语短句合并（`--deep` 可代劳
   确定性部分）。
3. **替换第三**：黑话/翻译腔按 style_guide 对照表换具体词；一处一换，不连锁改。
4. **重写最后**：前三步救不回来的句子才整句重写——重写句必须通过
   `verify.py` 的数字/术语守卫才算完成。

## 停止条件（防过度改写）

- 预算投影显示再改 K 句预期收益 < 2 分 → 停（边际收益归零）。
- 一句话改了 3 稿仍不达标 → 保留最好的一稿，标记「人工再读」，不要死磕。
- 全文特征分进入目标档位（compare 确认）→ 停。剩余长尾交给作者本人。

## 与其他件的分工

| 问题 | 去处 |
|---|---|
| 某类模式具体怎么改 | `references/style_guide_zh.md`（EN 用 `_en.md`） |
| 句子怎么排优先级/预算投影 | `plan.py`（`--json` 给 agent 消费） |
| 交接块格式 | `plan.py --handoff` 直接产出 |
| 数字/引用/术语守卫 | `verify.py`（exit 0 才算过） |
| 量化验收 | `stylecheck.py 改稿 --compare 原稿` |
| 七类场景的完整打法 | `references/best_practices.md` |
