# -*- coding: utf-8 -*-
"""赛事赛题生成器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：UIBC 赛题规范 + 赛季主题'迁移的判定与问责'
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "problem-set-generator", "version": "1.1.0", "args": [{"name": "theme", "help": "赛题主题(默认 迁移的判定与问责)", "required": False}, {"name": "difficulty", "help": "难度: easy/mid/hard", "required": False}, {"name": "count", "help": "生成数量 1-10", "required": False}]}

class GateError(Exception):
    pass

def classify_problem(args):
    """按赛事主题生成结构化赛题（AI 辅助，须组委会审核）。规则源：UIBC 赛题规范 + 主题'迁移的判定与问责'。"""
    theme = args.get('theme') or '迁移的判定与问责'
    difficulty = (args.get('difficulty') or 'mid').lower()
    diff_map = {'easy': '入门', 'mid': '进阶', 'hard': '挑战'}
    if difficulty not in diff_map:
        # 非法难度直接判非法，不静默按 mid 输出
        raise GateError("difficulty 取值非法：仅接受 easy/mid/hard（实收 %r）" % difficulty)
    try:
        count = int(args.get('count') or 3)
    except Exception:
        raise GateError("count 须为 1-10 的整数（实收 %r）" % args.get('count'))
    if count < 1 or count > 10:
        raise GateError("count 须为 1-10 的整数")
    # 难度修饰段：底稿三场景 × 难度要求差异化（修复"不同难度返回同底稿"）
    modifier = {
        'easy': ("\n【入门要求】给出可照做的脚手架：分步提示 + 1 个最小可运行示例 + 明确的判定通过条件；"
                 "限定单一场景，不需要攻击用例。"),
        'mid': ("\n【进阶要求】完整实现判定与问责链路；报告须含 scope/limitations/checked/not_checked 四段；"
                 "注入 1 条伪造记录必须被门禁检出。"),
        'hard': ("\n【挑战要求】在进阶要求之上追加：构造 3 个攻击用例（含换钥攻击与争议伪装撤销）；"
                 "提供独立第二实现交叉核验（分歧率须为 0）；任何静默失败直接判 0 分。"),
    }
    base = [
        "背景：自治智能体 A 从环境 E1 迁移至 E2，其在训练期学到的'判定边界'在新环境部分失效。\n任务：设计一套'迁移的判定与问责'协议，使 A 在新环境中能(1)识别判定失效、(2)冻结高危动作、(3)向人类问责接口上报。\n约束：不得依赖云端、不得静默失败、问责记录可审计。\n交付物：协议 spec + 参考实现 + 测试用例。\n评分点：判定失效识别率 / 问责链路完整性 / 离线可审计性。",
        "背景：某医疗合规智能体被部署到新 jurisdiction，原法规知识库过期。\n任务：构建'迁移问责'机制，当知识库与现行法规冲突时自动告警并暂停决策，记录冲突点与责任人。\n约束：告警不可绕过、责任链不可删改、支持离线回放。\n交付物：冲突检测规则 + 责任链 schema + 回放工具。\n评分点：冲突召回率 / 责任链不可篡改性 / 回放完整性。",
        "背景：自动驾驶策略在仿真→实车迁移时行为漂移。\n任务：提出'判定与问责'迁移验证框架，量化仿真到实车的判定一致性，并对漂移动作做责任归属。\n约束：一致性指标可解释、责任归属可追溯到训练数据/部署配置。\n交付物：一致性度量 + 归因报告生成器。\n评分点：度量合理性 / 归因可解释性 / 离线可复现。",
    ]
    problems = []
    for i in range(count):
        spec = base[i % len(base)] + modifier[difficulty]
        problems.append({"index": i + 1, "theme": theme,
                         "difficulty": diff_map[difficulty],
                         "spec": spec,
                         "review_status": "待审（组委会人工审核后方可发布）",
                         "ai_note": "本赛题由 AI 按规范辅助生成（GB 45438-2025），须经组委会审核后发布"})
    # 从严推定与告警分层：常设提示（AI 审核/知识产权）入 notes；自定义主题（非当前赛季主题）属
    # 赛题适配风险，入 warnings（rc=1）——不静默按赛季主题通过输出
    warnings = []
    if theme != '迁移的判定与问责':
        warnings.append("自定义主题「%s」非当前赛季主题「迁移的判定与问责」：是否采用须组委会确认赛题适配性。" % theme)
    return {"theme": theme, "difficulty": difficulty, "count": count, "problems": problems,
            "warnings": warnings,
            "notes": ["主题'迁移的判定与问责'为 UIBC 当前赛季主题",
                      "诚实边界：底稿为三场景模板，难度经由难度要求段区分；同一底稿在不同难度下要求不同，发布前须组委会精修去重",
                      "AI 生成内容须经组委会人工审核（各赛题 review_status/ai_note 已逐条标注）",
                      "赛题知识产权归赛事主办方"],
            "evidence": ["UIBC 赛题规范"]}


def _run(args):
    res = classify_problem(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="problem-set-generator", description="赛事赛题生成器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB 45438-2025", "is_generated": True, "generator": META["slug"] + "@SynomosAI",
            "content_type": "decision_support_output",
            "label_note": "标识口径待核：赛题底稿文本为 AI 辅助生成，属生成合成内容",
            "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"theme": "迁移的判定与问责", "difficulty": "mid", "count": "2"}, {"difficulty": "hard", "count": "1"}, {"theme": "跨境数据判定", "difficulty": "easy", "count": "1"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
