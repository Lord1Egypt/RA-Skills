#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""memory-cross-engine —— 跨引擎记忆贯通总线。

让规划(planner) / 记忆(memory) / 验证(verify) 等「四引擎」共享同一份结构化记忆，
使超级智能体在一次长程任务内跨引擎检索与关联，越跑越连贯。

设计要点（参考 continual-memory-engine 的 CJK 分词修正）：
- 记忆条目带 engine 标签（来自哪个引擎），type 分类，payload 正文，links 关联。
- retrieve 用 单字+二元组 集合做 relevance，规避 CJK 分词缺失导致 relevance=0 的坑。
- 支持跨引擎检索（默认全部引擎）与按引擎过滤（engines=[...]）。

用法：
  python memory_bus.py --selftest
  python memory_bus.py write   --engine planner --type goal --payload "部署静态站点并验证可达"
  python memory_bus.py link   --a e0001 --b e0002
  python memory_bus.py retrieve --query "部署 沙箱 验证" --topk 5
  python memory_bus.py view
"""
import os, sys, json, re, datetime


class MemoryBus:
    def __init__(self, store_path=None):
        self.store_path = store_path or os.path.join(os.path.dirname(__file__), "memory_bus.jsonl")
        self.entries = []
        self._load()

    def _load(self):
        if os.path.exists(self.store_path):
            try:
                with open(self.store_path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.entries.append(json.loads(line))
            except Exception:
                pass

    def _save(self):
        with open(self.store_path, "w", encoding="utf-8") as f:
            for e in self.entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    def write(self, engine, etype, payload, links=None, meta=None):
        eid = "e%04d" % (len(self.entries) + 1)
        e = {
            "id": eid,
            "engine": engine,
            "type": etype,
            "payload": payload,
            "ts": datetime.datetime.now().isoformat(timespec="seconds"),
            "links": links or [],
            "meta": meta or {},
        }
        self.entries.append(e)
        self._save()
        return eid

    def link(self, a, b):
        for e in self.entries:
            if e["id"] == a and b not in e["links"]:
                e["links"].append(b)
            if e["id"] == b and a not in e["links"]:
                e["links"].append(a)
        self._save()

    @staticmethod
    def _tokens(text):
        text = re.sub(r"\s+", "", str(text).lower())
        toks = set(text)
        bigrams = set(text[i:i + 2] for i in range(len(text) - 1))
        return toks | bigrams

    def retrieve(self, query, topk=5, engines=None):
        q = self._tokens(query)
        scored = []
        for e in self.entries:
            blob = "%s %s %s" % (e["type"], e["payload"], " ".join(e["links"]))
            t = self._tokens(blob)
            score = len(q & t) / (len(q) + 1.0)
            if engines and e["engine"] not in engines:
                score = 0.0
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        return [e for _, e in scored[:topk]]

    def cross_engine_view(self):
        view = {}
        for e in self.entries:
            view[e["engine"]] = view.get(e["engine"], 0) + 1
        return {
            "engines": view,
            "total": len(self.entries),
            "links": sum(len(e["links"]) for e in self.entries),
        }


def _selftest():
    tmp = os.path.join(os.path.dirname(__file__), "memory_bus_selftest.jsonl")
    if os.path.exists(tmp):
        os.remove(tmp)
    bus = MemoryBus(tmp)
    # 三个引擎各写一条
    p1 = bus.write("planner", "goal", "部署静态站点并验证可达性")
    m1 = bus.write("memory", "fact", "用户偏好部署到 CloudStudio 沙箱")
    v1 = bus.write("verify", "check", "站点首页返回 200 即视为通过")
    # 跨引擎关联
    bus.link(p1, m1)
    bus.link(p1, v1)
    bus.link(m1, v1)
    # 跨引擎检索：查询应同时贯通 planner 与 memory
    res = bus.retrieve("部署 沙箱 验证 可达", topk=5)
    engines_in = {e["engine"] for e in res}
    assert len(engines_in) >= 2, "跨引擎检索未贯通多引擎: %s" % engines_in
    # verify 引擎条目可被检索到
    res2 = bus.retrieve("验证 站点 返回 200 通过", topk=5)
    assert any(e["id"] == v1 for e in res2), "验证引擎条目未被检索到"
    # 关联数正确
    view = bus.cross_engine_view()
    assert view["links"] >= 3, "关联数不足: %s" % view["links"]
    assert view["total"] == 3, "条目总数异常: %s" % view["total"]
    # 按引擎过滤
    only_plan = bus.retrieve("部署", engines=["planner"])
    assert all(e["engine"] == "planner" for e in only_plan), "引擎过滤失效"
    os.remove(tmp)
    print("✅ memory-cross-engine selftest 全过 (三引擎贯通+关联+检索+过滤)")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        _selftest()
        return
    bus = MemoryBus()
    if not args:
        print("用法: --selftest | write --engine E --type T --payload P | link --a A --b B | retrieve --query Q | view")
        return
    cmd = args[0]
    kv = {}
    i = 1
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            kv[a[2:]] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else ""
            i += 2
        else:
            i += 1
    if cmd == "write":
        eid = bus.write(kv.get("engine", "unknown"), kv.get("type", "note"), kv.get("payload", ""))
        print("✍️ 已写入 %s" % eid)
    elif cmd == "link":
        bus.link(kv.get("a"), kv.get("b"))
        print("🔗 已关联 %s <-> %s" % (kv.get("a"), kv.get("b")))
    elif cmd == "retrieve":
        for e in bus.retrieve(kv.get("query", ""), topk=int(kv.get("topk", 5) or 5)):
            print("[%s|%s] %s" % (e["engine"], e["id"], e["payload"]))
    elif cmd == "view":
        print(json.dumps(bus.cross_engine_view(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
