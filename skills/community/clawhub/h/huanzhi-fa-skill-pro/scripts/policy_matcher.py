#!/usr/bin/env python3
"""
OPC政策匹配引擎
焕智AI FaSkill Pro — OPC初创企业AI融资顾问

输入: 企业画像JSON（阶段/赛道/区域）
输出: 可申领政策清单JSON

用法:
    python3 policy_matcher.py < input.json
    python3 policy_matcher.py '{"district": "徐汇区", "sector": "AI智能体", "stage": "刚注册"}'
"""

import json
import sys
from typing import Any, Dict, List, Optional


# ============================================================
# OPC政策数据库（精简版，完整版见 references/opc-policy-db.md）
# ============================================================

POLICY_DB: Dict[str, List[Dict[str, Any]]] = {
    "徐汇区": [
        {
            "name": "徐汇区OPC创业启动金",
            "type": "cash_grant",
            "amount": {"min": 50000, "max": 100000, "currency": "CNY"},
            "eligibility": [
                "注册在徐汇区",
                "属于优先赛道（AI/智能体/内容创作）",
                "团队≤10人",
            ],
            "deadline": "2026-12-31",
            "application_method": "线上申报+线下审核",
            "required_documents": ["营业执照", "项目计划书", "团队介绍"],
            "action": "准备材料，提交至徐汇区科创委",
            "status": "open",
        },
        {
            "name": "徐汇区算力券",
            "type": "voucher",
            "amount": {"max": 1000000, "currency": "CNY"},
            "eligibility": ["注册在徐汇区OPC社区", "使用算力服务"],
            "deadline": "2026-12-31",
            "application_method": "先用后付，年度结算",
            "required_documents": ["算力服务合同", "使用记录", "发票"],
            "action": "入驻模速空间后申请",
            "status": "open",
        },
        {
            "name": "徐汇区模型券",
            "type": "voucher",
            "amount": {"max": 1000000, "currency": "CNY"},
            "eligibility": ["注册在徐汇区OPC社区", "使用大模型调用服务"],
            "deadline": "2026-12-31",
            "application_method": "先用后付，年度结算",
            "action": "入驻模速空间后申请",
            "status": "open",
        },
        {
            "name": "徐汇区租房补贴",
            "type": "talent",
            "amount": {"max": 72000, "currency": "CNY", "note": "2000元/月×3年"},
            "eligibility": ["注册在徐汇区OPC社区", "符合人才认定"],
            "deadline": "2026-12-31",
            "action": "入驻后申请人才公寓",
            "status": "open",
        },
    ],
    "临港新片区": [
        {
            "name": "临港办公租金减免",
            "type": "space",
            "amount": {"note": "最长3年零租金，续约2年减半"},
            "eligibility": ["注册在临港新片区", "符合OPC认定"],
            "deadline": "持续开放",
            "action": "联系临港社区管理办公室",
            "status": "open",
        },
        {
            "name": "临港算力补贴",
            "type": "voucher",
            "amount": {"max": 300000, "note": "最高80%补贴，学生100%"},
            "eligibility": ["注册在临港", "使用AI算力"],
            "deadline": "2026-12-31",
            "action": "提交算力使用计划",
            "status": "open",
        },
        {
            "name": "临港创业担保贷款",
            "type": "loan",
            "amount": {"max": 800000, "currency": "CNY"},
            "eligibility": ["注册在临港", "符合创业担保条件"],
            "deadline": "持续开放",
            "action": "联系临港金融服务平台",
            "status": "open",
        },
        {
            "name": "临港出海服务补贴",
            "type": "cash_grant",
            "amount": {"note": "跨境专线/数据/支付合规指导"},
            "eligibility": ["注册在临港", "出海业务"],
            "deadline": "2026-12-31",
            "action": "申请跨境服务包",
            "status": "open",
        },
    ],
    "浦东新区": [
        {
            "name": "浦东免费算力",
            "type": "voucher",
            "amount": {"max": 300000, "currency": "CNY"},
            "eligibility": ["新注册AI OPC"],
            "deadline": "2026-12-31",
            "action": "入驻张江AI小镇后申请",
            "status": "open",
        },
        {
            "name": "浦东创业资助",
            "type": "cash_grant",
            "amount": {"max": 1000000, "note": "连续3年，每年最高100万"},
            "eligibility": ["注册在浦东", "与指标挂钩"],
            "deadline": "持续开放",
            "action": "提交创业资助申请",
            "status": "open",
        },
    ],
    "杨浦区": [
        {
            "name": "杨浦房租物业费减免",
            "type": "space",
            "amount": {"note": "首年全免，拎包入住"},
            "eligibility": ["入驻复兴岛OPC星火社区"],
            "deadline": "持续开放",
            "action": "联系复兴岛社区",
            "status": "open",
        },
        {
            "name": "杨浦大模型补贴",
            "type": "voucher",
            "amount": {"note": "调用费用最高50%补贴"},
            "eligibility": ["注册在杨浦", "使用大模型"],
            "deadline": "2026-12-31",
            "action": "提交大模型调用记录",
            "status": "open",
        },
        {
            "name": "杨浦新质秀带创新券",
            "type": "voucher",
            "amount": {"max": 200000, "currency": "CNY"},
            "eligibility": ["注册在杨浦"],
            "deadline": "2026-12-31",
            "action": "线上申请",
            "status": "open",
        },
    ],
    "静安区": [
        {
            "name": "静安入驻礼包",
            "type": "voucher",
            "amount": {"max": 100000, "currency": "CNY", "note": "算力+模型+语料+AI工具券"},
            "eligibility": ["入驻视听静界·π空间"],
            "deadline": "2026-12-31",
            "action": "入驻后申请",
            "status": "open",
        },
        {
            "name": "静安原创IP/AIGC扶持",
            "type": "cash_grant",
            "amount": {"max": 1000000, "currency": "CNY"},
            "eligibility": ["重大AIGC/原创IP项目"],
            "deadline": "2026-12-31",
            "action": "提交项目申报书",
            "status": "open",
        },
    ],
    "闵行区": [
        {
            "name": "虹橙工位补贴",
            "type": "space",
            "amount": {"note": "4.5折专项补贴（限100个工位）"},
            "eligibility": ["2026.7.31前入驻虹橙社区"],
            "deadline": "2026-07-31",
            "action": "联系虹橙社区",
            "status": "open",
        },
        {
            "name": "虹橙免费Tokens",
            "type": "voucher",
            "amount": {"note": "7000万Tokens体验，万亿Tokens计划"},
            "eligibility": ["入驻虹橙社区"],
            "deadline": "持续开放",
            "action": "入驻后申请",
            "status": "open",
        },
    ],
    "青浦区": [
        {
            "name": "青浦0门槛入驻",
            "type": "space",
            "amount": {"note": "0门槛、0租金、秒入驻，首年全额免租"},
            "eligibility": ["入驻青橙OPC社区"],
            "deadline": "持续开放",
            "action": "联系青橙社区",
            "status": "open",
        },
        {
            "name": "青浦种子基金",
            "type": "equity",
            "amount": {"max": 100000, "currency": "CNY", "note": "快速决策"},
            "eligibility": ["入驻青浦OPC社区"],
            "deadline": "持续开放",
            "action": "提交项目计划",
            "status": "open",
        },
    ],
    "松江区": [
        {
            "name": "松江工位租金优惠",
            "type": "space",
            "amount": {"note": "前3月免租+后6月6折，等效1000元/月"},
            "eligibility": ["入驻洞泾人工智能OPC社区"],
            "deadline": "持续开放",
            "action": "联系洞泾社区",
            "status": "open",
        },
        {
            "name": "松江大模型备案奖励",
            "type": "cash_grant",
            "amount": {"max": 500000, "currency": "CNY"},
            "eligibility": ["完成大模型备案"],
            "deadline": "2026-12-31",
            "action": "提交备案证明",
            "status": "open",
        },
        {
            "name": "松江数据集采购补贴",
            "type": "voucher",
            "amount": {"max": 5000000, "currency": "CNY"},
            "eligibility": ["松江智算专项"],
            "deadline": "2026-12-31",
            "action": "提交采购合同",
            "status": "open",
        },
    ],
    "嘉定区": [
        {
            "name": "嘉定六个一支持包",
            "type": "space",
            "amount": {"note": "注册地址+共享工位+AI工具券+开放场景+Demo支持+管家服务"},
            "eligibility": ["入驻嘉定高校AIGC创业社区"],
            "deadline": "持续开放",
            "action": "联系嘉定社区",
            "status": "open",
        },
    ],
    "黄浦区": [
        {
            "name": "黄浦区FTC-OPC专区入驻",
            "type": "space",
            "amount": {"note": "一地注册、多点办公，8处产业楼宇灵活办公，共享录影棚/商务中心/直播室/路演厅"},
            "eligibility": ["在外滩FTC登记注册的内容创作经营主体", "OPC创业者"],
            "deadline": "持续开放",
            "application_method": "凭外滩FTC统一租赁协议完成注册",
            "required_documents": ["租赁协议", "项目简介", "团队介绍"],
            "action": "联系外滩FTC专区管理方",
            "status": "open",
            "source": "上观新闻 2026-07-22",
        },
        {
            "name": "黄浦区一次性创业开办补贴",
            "type": "cash_grant",
            "amount": {"max": 10000, "currency": "CNY"},
            "eligibility": ["注册在黄浦区", "已享受市级初创期创业组织社会保险补贴"],
            "deadline": "2026-08-31",
            "application_method": "联系黄浦区人社局就业促进科",
            "required_documents": ["营业执照", "市级社保补贴获批证明", "银行账户"],
            "action": "市级社保补贴获批后申请",
            "status": "open",
            "source": "黄人社规〔2023〕3号",
        },
        {
            "name": "黄浦区创业带动就业补贴",
            "type": "cash_grant",
            "amount": {"note": "500元/人/月，最高5万元/年", "currency": "CNY"},
            "eligibility": ["注册在黄浦区", "吸纳本市劳动者并缴纳社保", "注册登记之日起36个月内"],
            "deadline": "2026-08-31",
            "application_method": "联系黄浦区人社局",
            "required_documents": ["营业执照", "社保缴纳记录", "劳动合同"],
            "action": "招用本市劳动者后申请",
            "status": "open",
            "source": "黄人社规〔2023〕3号",
        },
        {
            "name": "黄浦区创业孵化补贴",
            "type": "cash_grant",
            "amount": {"max": 20000, "currency": "CNY", "note": "以实际支付的房租/服务费/物业费为限，补贴期≤6个月"},
            "eligibility": ["进入黄浦区创业孵化示范基地孵化", "孵化期内成功创办创业组织", "吸纳1名本市劳动者就业+缴社保满6个月"],
            "deadline": "2026-08-31",
            "application_method": "联系黄浦区人社局",
            "required_documents": ["孵化协议", "创业成本支出凭证", "社保缴纳记录"],
            "action": "孵化期满后申请",
            "status": "open",
            "source": "黄人社规〔2023〕3号",
        },
        {
            "name": "黄浦创卡青年创业一卡通",
            "type": "space+cash",
            "amount": {"note": "6个月免费工位 + 2-4万元一次性创业补贴"},
            "eligibility": ["全日制高校在读或毕业5年内的高校毕业生创业者", "获得黄浦创卡"],
            "deadline": "持续开放",
            "application_method": "申请黄浦创卡 → 入驻区级创业孵化示范基地",
            "required_documents": ["学历证明", "创业计划书", "创卡获批证明"],
            "action": "18个月内成功创办创业组织+吸纳1名本市劳动者+缴社保满6个月后申领补贴",
            "status": "open",
            "source": "黄人社规〔2023〕3号",
        },
        {
            "name": "黄浦区创业赛事获奖启动资金",
            "type": "cash_grant",
            "amount": {"max": 50000, "currency": "CNY", "note": "区级最高5万/3万，市级及以上1:1配套"},
            "eligibility": ["参加人社部门组织的创业赛事获奖", "获奖后1年内在黄浦区开办创业组织", "吸纳1名本市劳动者+缴社保满6个月"],
            "deadline": "持续开放",
            "application_method": "联系黄浦区人社局",
            "required_documents": ["获奖证书", "营业执照", "社保缴纳记录"],
            "action": "获奖后申请",
            "status": "open",
            "source": "黄人社规〔2023〕3号",
        },
        {
            "name": "黄浦区FTC创造营培训",
            "type": "training",
            "amount": {"note": "5大训练营免费参与：AI创作/新人孵化/短剧漫剧/OPC创业/老字号联名"},
            "eligibility": ["入驻FTC-OPC专区"],
            "deadline": "持续开放",
            "action": "入驻后报名参与",
            "status": "open",
            "source": "上观新闻 2026-07-22",
        },
        {
            "name": "黄浦区AI短剧漫剧专项扶持",
            "type": "cash_grant",
            "amount": {"note": "2026年好内容1优质内容扶持计划首次增设，具体金额待发布"},
            "eligibility": ["深耕AI短剧漫剧赛道的优质创作者"],
            "deadline": "2026年，具体窗口待公布",
            "action": "关注黄浦区融媒体中心/FTC专区公告",
            "status": "upcoming",
            "source": "上观新闻 2026-07-22",
        },
    ],
}


# ============================================================
# 国家层面政策
# ============================================================

NATIONAL_POLICIES = [
    {
        "name": "创业担保贷款（个人）",
        "type": "loan",
        "amount": {"max": 600000, "currency": "CNY", "note": "财政贴息"},
        "eligibility": ["毕业5年内青年创业者"],
        "deadline": "持续开放",
        "action": "联系当地人社局",
        "status": "open",
    },
    {
        "name": "创业担保贷款（企业）",
        "type": "loan",
        "amount": {"max": 5000000, "currency": "CNY", "note": "财政贴息"},
        "eligibility": ["小微企业"],
        "deadline": "持续开放",
        "action": "联系当地人社局",
        "status": "open",
    },
    {
        "name": "科创贷（中国银行）",
        "type": "loan",
        "amount": {"max": 10000000, "note": "纯信用最高500万"},
        "eligibility": ["高企/专精特新/科技型中小企业"],
        "deadline": "持续开放",
        "action": "联系中国银行当地分行",
        "status": "open",
    },
    {
        "name": "高新技术企业认定",
        "type": "tax_break",
        "amount": {"note": "15%企业所得税（vs 25%）"},
        "eligibility": ["通过高新技术企业认定"],
        "deadline": "每年两批",
        "action": "准备认定材料",
        "status": "open",
    },
    {
        "name": "研发费用加计扣除",
        "type": "tax_break",
        "amount": {"note": "按实际发生额100%加计扣除"},
        "eligibility": ["开展研发活动"],
        "deadline": "年度汇算清缴",
        "action": "建立研发费用台账",
        "status": "open",
    },
    {
        "name": "小微企业所得税优惠",
        "type": "tax_break",
        "amount": {"note": "年应纳税所得额≤300万，按5%征收"},
        "eligibility": ["小微企业"],
        "deadline": "持续有效",
        "action": "汇算清缴时自动享受",
        "status": "open",
    },
]


# ============================================================
# 社区推荐
# ============================================================

COMMUNITY_RECOMMENDATIONS = {
    "AI技术": {
        "name": "模速空间OPC超级创业者社区",
        "district": "徐汇区",
        "benefits": ["首年工位全免", "20亿元AI青年创业基金对接", "300+大模型企业生态圈"],
    },
    "大模型": {
        "name": "模速空间OPC超级创业者社区",
        "district": "徐汇区",
        "benefits": ["首年工位全免", "20亿元AI青年创业基金对接", "300+大模型企业生态圈"],
    },
    "智能体": {
        "name": "模速空间OPC超级创业者社区",
        "district": "徐汇区",
        "benefits": ["首年工位全免", "20亿元AI青年创业基金对接", "300+大模型企业生态圈"],
    },
    "出海": {
        "name": "零界魔方",
        "district": "临港新片区",
        "benefits": ["最长3年零租金", "80%算力补贴", "跨境数据/支付/合规全套服务"],
    },
    "跨境电商": {
        "name": "零界魔方",
        "district": "临港新片区",
        "benefits": ["最长3年零租金", "跨境专线补贴", "出海服务全套"],
    },
    "短剧": {
        "name": "视听静界·π空间",
        "district": "静安区",
        "benefits": ["原创IP最高100万扶持", "澎湃新闻媒体资源", "创作者大赛最高20万"],
    },
    "AIGC": {
        "name": "可灵AI+创作者生态",
        "district": "徐汇区",
        "benefits": ["最高100万投资+1亿流量", "算力券+模型券", "创作者经济生态"],
    },
    "内容创作": {
        "name": "外滩FTC-OPC专区",
        "district": "黄浦区",
        "benefits": ["一地注册多点办公（8处楼宇）", "共享录影棚/直播室/路演厅", "政务专窗+法务财税指导", "投融资社群+文商旅资源"],
    },
    "AI短剧": {
        "name": "外滩FTC-OPC专区",
        "district": "黄浦区",
        "benefits": ["全市首个FTC-OPC专区", "AI短剧漫剧专项扶持", "FTC创造营5大训练营", "外滩/南京东路线下展示"],
    },
    "数字文创": {
        "name": "外滩FTC-OPC专区",
        "district": "黄浦区",
        "benefits": ["FTC HUB线下载体", "文创展销+创意快闪", "一照通行多专区", "品牌出圈沉浸式场景"],
    },
    "金融科技": {
        "name": "陆家嘴数智港",
        "district": "浦东新区",
        "benefits": ["陆家嘴金融生态", "场景任务包", "创梦包十个一政策"],
    },
    "硬科技": {
        "name": "AlohaIdol孵化器",
        "district": "浦东新区张江",
        "benefits": ["张江AI创新小镇", "算力/模型/语料券各最高100万", "居住办公2合1"],
    },
    "AI+制造": {
        "name": "洞泾人工智能OPC社区",
        "district": "松江区",
        "benefits": ["50道国资赛题", "垂直模型最高500万补贴", "数据集最高500万补贴"],
    },
    "数字游民": {
        "name": "新丰科创小院",
        "district": "浦东新区",
        "benefits": ["数字游民友好", "月租≤2000元", "灵活办公"],
    },
    "高校创业": {
        "name": "嘉定高校大学生AI·OPC创业社区",
        "district": "嘉定区",
        "benefits": ["六个一支持包", "腾讯AIGC大赛直通", "高校资源对接"],
    },
}


# ============================================================
# 匹配引擎
# ============================================================

def match_policies(data: Dict[str, Any]) -> Dict[str, Any]:
    """执行政策匹配"""
    
    district = data.get("district", "")
    sector = data.get("sector", "")
    stage = data.get("stage", "")

    matched_policies = []
    district_coverage = "covered" if district in POLICY_DB else "not_covered"

    # 1. 匹配区域政策
    if district in POLICY_DB:
        for policy in POLICY_DB[district]:
            matched_policy = policy.copy()
            # 检查赛道匹配
            eligibility = " ".join(policy.get("eligibility", []))
            if sector and any(kw in sector for kw in ["AI", "智能体", "大模型", "AIGC"]):
                if "AI" in eligibility or "智能体" in eligibility:
                    matched_policy["match_score"] = "high"
                else:
                    matched_policy["match_score"] = "medium"
            elif sector:
                matched_policy["match_score"] = "medium"
            else:
                matched_policy["match_score"] = "low"
            matched_policies.append(matched_policy)

    # 2. 匹配国家层面政策
    stage_map = {
        "刚注册": "early",
        "有产品": "early",
        "有收入": "growth",
        "准备融资": "growth",
        "已融资": "growth",
    }
    mapped_stage = stage_map.get(stage, "early")

    for policy in NATIONAL_POLICIES:
        matched_policy = policy.copy()
        if mapped_stage == "early" and "创业担保" in policy["name"]:
            matched_policy["match_score"] = "high"
        elif mapped_stage == "growth" and "科创贷" in policy["name"]:
            matched_policy["match_score"] = "high"
        elif "高新技术企业" in policy["name"]:
            matched_policy["match_score"] = "medium"
        else:
            matched_policy["match_score"] = "medium"
        matched_policies.append(matched_policy)

    # 3. 计算预估总额
    total_min = 0
    total_max = 0
    for policy in matched_policies:
        amt = policy.get("amount", {})
        if "min" in amt and amt["min"]:
            total_min += amt["min"]
        if "max" in amt and isinstance(amt["max"], (int, float)):
            total_max += amt["max"]

    # 4. 推荐社区
    recommended_community = None
    if sector:
        for sector_keyword, community in COMMUNITY_RECOMMENDATIONS.items():
            if sector_keyword in sector or sector in sector_keyword:
                recommended_community = community
                break

    if not recommended_community:
        recommended_community = {
            "name": "模速空间OPC超级创业者社区",
            "district": "徐汇区",
            "benefits": ["首年工位全免", "20亿元AI青年创业基金对接", "300+大模型企业生态圈"],
        }

    # 5. 生成行动建议
    action_plan = {
        "short_term": {
            "timeframe": "本周",
            "tasks": ["准备入驻材料（营业执照+项目简介+团队介绍）", "了解可申领政策申请流程"],
        },
        "medium_term": {
            "timeframe": "本月",
            "tasks": ["提交首轮政策申请", "启动高新技术企业认定准备"],
        },
        "long_term": {
            "timeframe": "本季度",
            "tasks": ["持续关注政策申报窗口", "建立知识产权布局"],
        },
    }

    return {
        "version": "3.0.0",
        "module": "policy_matcher",
        "user_profile": {
            "district": district,
            "sector": sector,
            "stage": stage,
        },
        "district_coverage": district_coverage,
        "district_coverage_hint": (
            "区域政策已在数据库中" if district_coverage == "covered"
            else f"[未收录] '{district}' 不在政策数据库中，请优先联网搜索该区域OPC扶持政策"
        ),
        "matched_policies": matched_policies,
        "total_estimated": {
            "min": total_min if total_min > 0 else None,
            "max": total_max if total_max > 0 else None,
            "currency": "CNY",
            "note": "估算值，以实际审批为准",
        },
        "recommended_community": recommended_community,
        "action_plan": action_plan,
        "disclaimer": "本建议仅供参考，政策以政府最新公布为准。申报前请核实官方文件。",
    }


def main():
    if len(sys.argv) > 1:
        input_data = json.loads(sys.argv[1])
    else:
        input_data = json.load(sys.stdin)

    result = match_policies(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()