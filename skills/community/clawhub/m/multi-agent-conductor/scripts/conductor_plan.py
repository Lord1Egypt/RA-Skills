# -*- coding: utf-8 -*-
"""多 agent 编排规划器：把任务拆成角色并给出 允许/禁止 边界。零依赖。"""
import argparse, json

ROLES = {
    "研究": ("检索/阅读外部资料", "写最终结论、改他人产物、访问密钥"),
    "写作": ("基于给定素材起草文档", "自行检索未授权源、改他人草稿结构"),
    "审查": ("核对事实/合规/质量", "直接改产物内容、对外发布"),
    "总控": ("汇总、排冲突、拦截越界", "写具体业务内容、替代专业 agent"),
    "数据": ("处理数据集/计算", "读取其他 agent 私有目录、外发数据"),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--agents", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.agents < 1:
        ap.error("--agents 至少为 1")
    keys = list(ROLES.keys())
    core = keys[: min(a.agents, len(keys))]
    # 超出核心角色数时，生成带独立编号与边界的「专员」角色，绝不复用同一角色
    extras = [f"专员{i}" for i in range(1, a.agents - len(core) + 1)]
    plan = []
    for i, role in enumerate(core, 1):
        allow, forbid = ROLES[role]
        plan.append({"id": i, "role": role, "allow": allow, "forbid": forbid})
    for j, role in enumerate(extras):
        allow = f"专属{j + len(core)}号位职责：单一定义、与他人不重叠（由总控显式指派）"
        forbid = "复述/侵入他人职责、越界写操作"
        plan.append({"id": len(core) + j + 1, "role": role, "allow": allow, "forbid": forbid})
    note = "" if not extras else f"\n⚠️ {len(extras)} 个专员位超出核心角色集，职责必须由总控逐个显式指派，禁止默认复用。"
    if a.json:
        print(json.dumps({"task": a.task, "roster": plan, "note": note.strip()}, ensure_ascii=False, indent=2))
        return
    print(f"任务：{a.task}\n编排方案（{len(plan)} agent）：\n" + "=" * 50)
    for p in plan:
        print(f"  Agent{p['id']} · {p['role']}")
        print(f"     ✅ 允许：{p['allow']}")
        print(f"     🔒 禁止：{p['forbid']}")
    print("=" * 50)
    if note:
        print(note.strip())
    print("总控（conductor）唯一出口：汇总各 agent 产物、排冲突、拦截越界写操作。")

if __name__ == "__main__":
    main()
