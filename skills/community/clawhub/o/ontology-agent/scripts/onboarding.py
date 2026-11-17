#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onboarding.py — 渐进式主动引导引擎
本体论智能体 (Ontology Agent) · 天津市微数人工智能科技有限责任公司

问题：用户常不知道该告诉数字公司哪些信息，往往碎片化、想起啥说啥。
解决：让「数字公司」（经营主理人）拥有 onboarding——按优先级循序渐进补采企业数据，
      每次只问 1~2 个最高优缺口，说明用途 + 安全安抚，绝不一次轰炸、不引发安全顾虑。

用法：
  python onboarding.py --instance <path> --next [--limit 2]   # 下一批待补问题（给主理人发问用）
  python onboarding.py --instance <path> --coverage            # 已补全 12/22 (55%)
  python onboarding.py --instance <path> --report              # 给主理人的一句话进度播报
"""
import argparse
import os
import sys
import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 视为「未填」的占位符（大小写不敏感）
PLACEHOLDER_TOKENS = {"", "待定", "todo", "待补充", "（待补充）", "见职责说明", "暂无", "无", "nan", "none"}


def _is_blank(v):
    if v is None:
        return True
    if isinstance(v, str) and v.strip().lower() in PLACEHOLDER_TOKENS:
        return True
    if isinstance(v, (list, dict)) and len(v) == 0:
        return True
    return False


# 待补字段 schema：点分路径(相对 profile) / 优先级 / 提问 / 用途 / 安全安抚
# 优先级 0=决定所有建议基调(最高) 1=核心事实 2=上下文与接口 3=持续补采(任务触发)
FIELDS = [
    # ── P0 基础身份（"我是X公司"阶段尽量采集，但常不全）──
    ("company", 0, "贵公司全称是？", "所有文件落款与法律主体", "仅存本地实例，不出域"),
    ("enterprise_type", 0, "企业类型是？（一人公司 / 电商 / 小微 / 其他）", "匹配行业包与合规口径", "仅存本地"),
    ("region", 0, "注册地 / 主要经营地在哪？（如 天津市和平区）", "匹配本地政策与税务口径", "仅存本地"),
    ("industry", 0, "主营行业是？", "决定部门侧重与行业红线", "仅存本地"),
    ("scale", 0, "公司规模？（几人、有无雇员）", "决定是否需要员工分权与 hr 流程", "仅存本地"),
    # ── P0 老板画像核心（决定所有建议的语气与边界）──
    ("owner_profile.address_as", 0, "我该怎么称呼您？（如 顺然）", "所有专家用您习惯的称呼沟通", "仅存本地实例"),
    ("owner_profile.decision_style", 0, "您做决策更偏哪种风格？（数据支撑 / 直觉 / 商议）", "建议贴合您的决策习惯", "仅存本地"),
    ("owner_profile.risk_appetite", 0, "您的风险偏好是？（保守 / 平衡 / 激进）", "影响财税 / 投资 / 扩张建议的激进程度", "仅存本地"),
    ("owner_profile.comm_style", 0, "您喜欢什么沟通腔调？（口语 / 正式、简短 / 详细、纯中文 / 中英混）", "决定汇报与输出呈现方式", "仅存本地"),
    # ── P1 关键事实 ──
    ("legal_form", 1, "法律形态是？（一人有限责任公司 / 个人独资 / 有限公司等）", "影响报税方式与财产独立红线", "公开工商信息可记，PII 不写明文"),
    ("credit_code", 1, "统一社会信用代码是？（可稍后补）", "工商主体唯一标识", "属公开登记信息可记，非 PII"),
    ("workflow", 1, "核心业务流程是？（如 接单→交付→开票→记账→报税）", "落成可执行工作流，驱动日常运营", "仅存本地"),
    ("owner_profile.auth_boundary", 1, "哪些操作必须您本人确认？（如 报税 / 开票 / 签约）", "划清 AI 授权边界，防越权", "仅存本地"),
    ("context.stage", 1, "公司当前阶段是？（刚成立 / 成长期 / 扩张期）", "决定建议节奏与重心", "仅存本地"),
    ("context.products", 1, "核心产品 / 服务有哪些？", "战略与销售建议的基础", "仅存本地"),
    ("context.customers", 1, "客户主要是？（ToB / ToC / 政府）", "决定营销与合规口径", "仅存本地"),
    # ── P2 上下文 / 接口 / 文化 ──
    ("owner_profile.background", 2, "您的专业背景是？（技术 / 销售 / 管理等）", "专家用您听得懂的语言", "仅存本地"),
    ("owner_profile.value_priority", 2, "您最看重什么？（增长 / 合规 / 利润 / 品牌）", "建议排序的依据", "仅存本地"),
    ("culture.mission", 2, "公司的使命 / 愿景是？", "统一 12 位员工对外口径", "仅存本地"),
    ("culture.voice", 2, "希望品牌用什么语气说话？（专业务实 / 年轻活泼等）", "内容与对外沟通基调", "仅存本地"),
    ("context.quarterly_goal", 2, "本季度最重要的目标是？", "让运营围绕目标展开", "仅存本地"),
    ("context.tool_stack", 2, "公司在用哪些系统？（钉钉 / 企微 / 飞书 / 资料库等，可填无）", "决定能否对接真实数据；没有也能本地跑", "仅存本地；填了也不主动联网"),
    ("owner_profile.taboo", 2, "有什么信息 / 平台是您不希望碰的？", "避免踩雷", "仅存本地"),
    ("culture.taboo_topics", 2, "对外有什么禁忌话题？", "品牌安全", "仅存本地"),
]


def _get(instance, dotted):
    cur = instance
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def coverage(instance):
    prof = (instance or {}).get("profile", {}) or {}
    total = len(FIELDS)
    filled = sum(1 for path, *_ in FIELDS if not _is_blank(_get(prof, path)))
    return filled, total, round(100.0 * filled / total)


def next_questions(instance, limit=2):
    prof = (instance or {}).get("profile", {}) or {}
    gaps = [{"field": p, "priority": pr, "question": q, "why": w, "security": s}
            for (p, pr, q, w, s) in FIELDS if _is_blank(_get(prof, p))]
    gaps.sort(key=lambda g: g["priority"])  # 优先级升序
    return gaps[:limit]


def report(instance):
    filled, total, pct = coverage(instance)
    if pct >= 100:
        return "✅ 企业信息已补全（%d/%d），数字公司可基于完整事实运行。" % (filled, total)
    return ("📊 企业信息补全进度 %d%%（%d/%d）。我会继续在合适的时候一次问您 1~2 件小事，"
            "慢慢补齐，不急着一次说完；您也可以随时说「跳过 / 以后再说」。" % (pct, filled, total))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True)
    ap.add_argument("--next", action="store_true", help="输出下一批待补问题")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--limit", type=int, default=2)
    args = ap.parse_args()
    if not os.path.isfile(args.instance):
        print("[onboarding] 实例不存在: %s" % args.instance)
        sys.exit(2)
    instance = yaml.safe_load(open(args.instance, encoding="utf-8")) or {}
    if args.coverage:
        f, t, p = coverage(instance)
        print("%d/%d (%d%%)" % (f, t, p))
    elif args.report:
        print(report(instance))
    elif args.next:
        for g in next_questions(instance, args.limit):
            print("[P%d] %s\n   用途：%s\n   安全：%s" % (g["priority"], g["question"], g["why"], g["security"]))
    else:
        print(report(instance))


if __name__ == "__main__":
    main()
