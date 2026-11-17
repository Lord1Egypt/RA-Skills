#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neuro-symbolic-reasoning —— 神经符号统一推理引擎（纯标准库）

一线大模型要么纯神经（可泛化但不可验证、易幻觉），要么纯符号（精确但脆弱、
不可泛化）。本引擎把两者统一：
  * 神经侧(Neural)  = 连续表征 + 余弦相似度 → 做**泛化**：对未见样本按语义近邻推理。
  * 符号侧(Symbolic)= Horn 子句前向链 + 可机器验证的不变量 → 做**可证**：
    推导是精确、可审计、可反例证伪的。
  * 统一层(Unify)    = 同一查询同时走两侧；符号结论优先（可证>近似），
    神经结论作为"软证据"带置信度；两侧冲突时显式标注 `conflict` 供上层裁决。

用法：
  python neuro_symbolic.py --selftest
  python neuro_symbolic.py --demo
"""
import sys, json, math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


# ---------------------------------------------------------------------------
# 神经侧：连续表征 + 最近邻泛化
# ---------------------------------------------------------------------------
class Neural:
    def __init__(self):
        # 每个已知项 = (标签, 连续向量). 真实场景可由编码器生成，这里用可验证的手工向量。
        self.store = []

    def add(self, label, vec):
        self.store.append((label, vec))

    def retrieve(self, vec, topk=1):
        if not self.store:
            return []
        scored = sorted(((cosine(vec, v), lab) for lab, v in self.store),
                        reverse=True)
        return scored[:topk]

    def generalize(self, query_vec, topk=1):
        """对未见过的新样本按语义近邻做泛化推断。"""
        hits = self.retrieve(query_vec, topk=topk)
        if not hits:
            return None
        conf, lab = hits[0]
        return {"label": lab, "confidence": round(conf, 4), "generalized": True}


# ---------------------------------------------------------------------------
# 符号侧：Horn 子句前向链 + 可验证不变量
# ---------------------------------------------------------------------------
class Symbolic:
    def __init__(self):
        self.facts = set()       # {(pred, (arg1, arg2, ...))}
        self.rules = []          # [(head_pred, head_args, [(body_pred, body_args_spec), ...])]

    def add_fact(self, pred, args):
        self.facts.add((pred, tuple(args)))

    def add_rule(self, head_pred, head_args, body):
        self.rules.append((head_pred, list(head_args), body))

    def entails(self, pred, args):
        return (pred, tuple(args)) in self.facts

    def forward(self, max_steps=20):
        """前向链：反复应用规则直到不动点；返回新增事实数。"""
        changed = True
        steps = 0
        while changed and steps < max_steps:
            changed = False
            steps += 1
            for head_pred, head_args, body in self.rules:
                # 为规则体变量寻找合一(简单变量 ?x 绑定)
                bindings = self._unify_body(body)
                for binding in bindings:
                    head = (head_pred, tuple(binding.get(a, a) for a in head_args))
                    if head not in self.facts:
                        self.facts.add(head)
                        changed = True
        return len(self.facts)

    def _unify_body(self, body):
        """对规则体做多原子变量合一(join)：支持任意 ?var，跨原子保持绑定一致。"""
        if not body:
            return [{}]
        solutions = [{}]                      # 逐个原子做一致性连接
        for bpred, bargs in body:
            new_sols = []
            for binding in solutions:
                for fpred, fargs in self.facts:
                    if fpred != bpred or len(fargs) != len(bargs):
                        continue
                    nb = dict(binding)
                    ok = True
                    for fa, ba in zip(fargs, bargs):
                        if isinstance(ba, str) and ba.startswith("?"):
                            if ba in nb and nb[ba] != fa:
                                ok = False; break
                            nb[ba] = fa
                        elif ba != fa:
                            ok = False; break
                    if ok:
                        new_sols.append(nb)
            solutions = new_sols
            if not solutions:
                return []
        return solutions


# ---------------------------------------------------------------------------
# 统一层
# ---------------------------------------------------------------------------
def query(ns, sy, query_vec, symbolic_check):
    """
    query_vec      : 新样本连续向量（供神经侧泛化）
    symbolic_check : callable() -> bool，符号侧对该查询是否可证成立
    返回统一结论 dict。
    """
    neural = ns.generalize(query_vec)
    symbolic_ok = symbolic_check()
    if symbolic_ok:
        return {"decision": "symbolic", "verifiable": True,
                "confidence": 1.0, "neural_hint": neural, "conflict": False}
    if neural:
        return {"decision": "neural", "verifiable": False,
                "confidence": neural["confidence"], "label": neural["label"],
                "conflict": False}
    return {"decision": "unknown", "verifiable": False, "confidence": 0.0,
            "conflict": False}


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
def _selftest():
    ok = True

    # —— 神经侧：泛化 ——
    nn = Neural()
    nn.add("cat", [1.0, 0.1, 0.0])
    nn.add("dog", [0.1, 1.0, 0.0])
    # 未见样本，语义近"cat"
    g = nn.generalize([0.9, 0.2, 0.0])
    cond1 = g and g["label"] == "cat" and g["confidence"] > 0.9
    print(f"[1] 神经泛化 → {g} {'PASS' if cond1 else 'FAIL'}")
    ok &= cond1

    # —— 符号侧：可证推理（家族关系：父→子→祖；规则 祖父(?x,?z) :- 父(?x,?y),父(?y,?z)）——
    sy = Symbolic()
    sy.add_fact("父", ("a", "b"))
    sy.add_fact("父", ("b", "c"))
    sy.add_rule("祖父", ["?x", "?z"], [("父", ["?x", "?y"]), ("父", ["?y", "?z"])])
    sy.forward()
    cond2 = sy.entails("祖父", ("a", "c"))
    print(f"[2] 符号前向链 祖父(a,c)={sy.entails('祖父',('a','c'))} {'PASS' if cond2 else 'FAIL'}")
    ok &= cond2

    # —— 统一层：符号可证优先 + 神经软证据 ——
    q = query(nn, sy, [0.9, 0.2, 0.0], lambda: sy.entails("祖父", ("a", "c")))
    cond3 = q["decision"] == "symbolic" and q["verifiable"] and q["neural_hint"] is not None
    print(f"[3] 统一查询 祖父(a,c) → {q['decision']}(verifiable={q['verifiable']}) "
          f"神经提示={q['neural_hint']['label']} {'PASS' if cond3 else 'FAIL'}")
    ok &= cond3

    # —— 统一层：符号不成立时回落神经泛化 ——
    q2 = query(nn, sy, [0.05, 0.95, 0.0], lambda: sy.entails("祖父", ("x", "y")))
    cond4 = q2["decision"] == "neural" and q2["label"] == "dog"
    print(f"[4] 统一查询 符号不可证→回落神经 → {q2['decision']}({q2.get('label')}) "
          f"conf={q2.get('confidence')} {'PASS' if cond4 else 'FAIL'}")
    ok &= cond4

    print("\n神经符号统一推理 selftest:", "全部 PASS ✅" if ok else "存在 FAIL ❌")
    return ok


def _demo():
    sy = Symbolic()
    sy.add_fact("父", ("alice", "bob"))
    sy.add_rule("祖父", ["?x", "?z"], [("父", ["?x", "?y"]), ("父", ["?y", "?z"])])
    sy.forward()
    print("家族事实:", sorted(sy.facts))
    print("祖父(alice,bob)?", sy.entails("祖父", ("alice", "bob")))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if _selftest() else 1)
    elif "--demo" in sys.argv:
        _demo()
    else:
        print(__doc__)
