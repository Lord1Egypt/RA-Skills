#!/usr/bin/env python3
"""
数据质量清洗脚本
校验并清理 refs/ 与本地案例 JSON 数据库中的污染数据。
"""

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "shape_spirit"
AWARD_DIR = SKILL_DIR / "data" / "award_docs"

# ═══ 案由-领域映射（用于交叉验证）══════════════════
CAUSE_DOMAIN = {
    # 民事
    "民间借贷": "civil", "借款合同": "civil", "买卖合同": "civil",
    "租赁合同": "civil", "承揽合同": "civil", "建设工程": "civil",
    "物业服务": "civil", "委托合同": "civil", "居间合同": "civil",
    "合伙协议": "civil", "保证合同": "civil", "保险合同": "civil",
    "信用卡": "civil", "储蓄存款": "civil", "储蓄合同": "civil",
    "离婚": "civil", "抚养": "civil", "赡养": "civil",
    "探望权": "civil", "监护权": "civil", "继承": "civil",
    "法定继承": "civil", "遗嘱": "civil", "婚约财产": "civil",
    "分家析产": "civil", "共有": "civil", "物权": "civil",
    "返还原物": "civil", "排除妨害": "civil", "建筑物区分": "civil",
    "土地承包": "civil", "交通事故": "civil", "医疗损害": "civil",
    "产品责任": "civil", "环境污染": "civil", "网络侵权": "civil",
    "名誉权": "civil", "隐私权": "civil", "个人信息": "civil",
    "生命权": "civil", "健康权": "civil", "身体权": "civil",
    "姓名权": "civil", "肖像权": "civil",
    "劳动争议": "civil", "劳动合同": "civil", "工伤": "civil",
    "经济补偿": "civil", "赔偿金": "civil",
    "股权转让": "civil", "股东资格": "civil", "公司清算": "civil",
    "公司决议": "civil",
    # 商事
    "保险纠纷": "commercial", "海商": "commercial", "海事": "commercial",
    "票据": "commercial", "证券": "commercial",
    "不正当竞争": "commercial", "垄断": "commercial",
    # 刑事
    "故意杀人": "criminal", "故意伤害": "criminal", "强奸": "criminal",
    "抢劫": "criminal", "盗窃": "criminal", "诈骗": "criminal",
    "贪污": "criminal", "受贿": "criminal", "滥用职权": "criminal",
    "玩忽职守": "criminal", "挪用公款": "criminal", "走私": "criminal",
    "贩卖毒品": "criminal", "非法持有": "criminal", "交通肇事": "criminal",
    "危险驾驶": "criminal",
    # 行政
    "行政处罚": "administrative", "行政许可": "administrative",
    "行政强制": "administrative", "行政赔偿": "administrative",
    "行政复议": "administrative", "信息公开": "administrative",
    "征收": "administrative", "拆迁": "administrative",
    "规划": "administrative", "土地管理": "administrative",
    "工商": "administrative", "税务": "administrative",
    "专利": "administrative", "商标": "administrative",
}

# 无效/损坏字段标记
CORRUPT_MARKERS = ["提取失败", "null", "占位符", "[PLACEHOLDER]", "暂无数据", "待补充"]


def _detect_domain(title: str, facts: str) -> str:
    """根据标题和事实判断领域"""
    for kw, domain in CAUSE_DOMAIN.items():
        if kw in title:
            return domain
    for kw, domain in CAUSE_DOMAIN.items():
        if kw in facts[:200]:
            return domain
    return ""


def clean_shape_spirit():
    """清洗形与神案例库"""
    stats = {"total": 0, "removed": 0, "corrupt": 0}
    
    for vol_file in ["civil.json", "criminal.json", "commercial.json", "administrative.json"]:
        path = DATA_DIR / vol_file
        if not path.exists():
            continue
        
        with open(path) as f:
            data = json.load(f)
        
        cases = data.get("extracted_cases", [])
        stats["total"] += len(cases)
        clean_cases = []
        
        for c in cases:
            title = c.get("title", "")
            facts = c.get("brief_facts", "")
            kw = json.dumps(c.get("keywords", []), ensure_ascii=False)
            writing = c.get("writing_experience", "")
            expert = c.get("expert_analysis", "")
            
            # 检查损坏数据
            is_corrupt = False
            for field_val in [title, facts, writing, expert]:
                for marker in CORRUPT_MARKERS:
                    if marker in str(field_val):
                        is_corrupt = True
                        break
            
            if is_corrupt:
                stats["corrupt"] += 1
                print(f"  [损坏] {vol_file} #{c.get('num','?')}: {title[:40]}")
                continue
            
            # 检查跨卷污染（标题在民事卷但事实明显属于行政/刑事）
            expected_domain = vol_file.replace(".json", "")
            actual_domain = _detect_domain(title, facts)
            
            if actual_domain and actual_domain != expected_domain:
                # 标题-事实严重不匹配
                if "证券" in facts or "操纵市场" in facts or "虚假申报" in facts:
                    if expected_domain == "administrative":
                        print(f"  [跨卷] {vol_file} #{c.get('num','?')}: {title[:40]} → 实际={actual_domain}")
                        stats["removed"] += 1
                        continue
            
            clean_cases.append(c)
        
        data["extracted_cases"] = clean_cases
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        removed = len(cases) - len(clean_cases)
        print(f"  {vol_file}: {len(cases)} → {len(clean_cases)} (移除 {removed})")
    
    return stats


def main():
    print("=" * 60)
    print("📊 数据质量清洗")
    print("=" * 60)
    
    print("\n1️⃣  形与神案例库清洗...")
    stats = clean_shape_spirit()
    
    print(f"\n{'='*60}")
    print(f"清洗报告:")
    print(f"  总案例数: {stats['total']}")
    print(f"  移除跨卷污染: {stats['removed']}")
    print(f"  移除损坏数据: {stats['corrupt']}")
    print(f"  清洗后剩余: {stats['total'] - stats['removed'] - stats['corrupt']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
