#!/usr/bin/env python3
"""
博物馆参观路线规划模块：根据用户画像和文物列表生成最优参观路线
"""

import json
import random
import sys
from typing import List, Dict, Any
from collections import defaultdict

from extract_profile import call_llm_api


def normalize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """标准化用户画像，确保字段格式一致"""
    normalized = {
        "museum_name": profile.get("museum_name", ""),
        "duration": profile.get("duration", "2-3小时"),
        "with_children": profile.get("with_children", False),
        "artifact_types": profile.get("artifact_types", []),
        "dynasties": profile.get("dynasties", []),
        "domains": profile.get("domains", []),
        "first_visit": profile.get("first_visit", False)
    }
    
    # 处理文物种类别名
    artifact_mapping = {
        "铜器": "青铜器",
        "玉器": "玉器宝石",
        "书画": "书画古籍"
    }
    normalized_artifacts = []
    for t in normalized["artifact_types"]:
        normalized_artifacts.append(artifact_mapping.get(t, t))
    normalized["artifact_types"] = normalized_artifacts
    
    return normalized


# 朝代别名映射
PERIOD_ALIAS = {
    "远古时期":       ["远古", "史前", "新石器", "旧石器", "新石器时代", "旧石器时代"],
    "夏商西周":       ["夏", "商", "殷", "西周", "殷商"],
    "春秋战国":       ["春秋", "战国", "东周"],
    "秦汉":           ["秦", "西汉", "东汉", "汉"],
    "三国两晋南北朝": ["三国", "魏", "蜀", "吴", "晋", "西晋", "东晋", "南北朝", "北朝", "南朝"],
    "隋唐五代":       ["隋", "唐", "五代", "五代十国"],
    "辽宋夏金元":     ["宋", "北宋", "南宋", "辽", "金", "元", "西夏"],
    "明清":           ["明", "清", "清代", "明代"],
}

def match_period(artifact_period: str, user_dynasties: list) -> bool:
    """判断文物时期是否匹配用户选择的朝代（含别名，自动去除"时期"后缀）"""
    normalized = artifact_period.replace("时期", "").strip()
    for user_dynasty in user_dynasties:
        # 直接匹配
        if user_dynasty == artifact_period or user_dynasty == normalized:
            return True
        
        # 检查文物时期是否在用户朝代的别名中
        for key, aliases in PERIOD_ALIAS.items():
            # 如果用户朝代是某个朝代的名称或别名
            if user_dynasty == key or user_dynasty in aliases:
                # 检查文物时期是否匹配该朝代或其别名
                if artifact_period == key or normalized == key or artifact_period in aliases or normalized in aliases:
                    return True
    return False


def calculate_score(artifact: Dict[str, Any], profile: Dict[str, Any]) -> float:
    """计算文物的匹配得分"""
    score = 0.0

    # 1. 文物种类匹配：一致 +2，不一致 +0.5
    artifact_type = artifact.get("type", "")
    if artifact_type in profile.get("artifact_types", []):
        score += 2.0
    else:
        score += 0.5

    # 2. 朝代匹配：一致 +2，不一致 +0
    artifact_period = artifact.get("period", "")
    if match_period(artifact_period, profile.get("dynasties", [])):
        score += 2.0

    # 3. 镇馆之宝 vs 一般文物
    is_treasure = artifact.get("is_treasure", False)
    first_visit = profile.get("first_visit", None)
    if first_visit is True:
        # 首次参观：镇馆之宝 +3，一般文物 +0
        if is_treasure:
            score += 3.0
    else:
        # 非首次参观（含 None）：镇馆之宝 +0.5，一般文物 +0
        if is_treasure:
            score += 0.5

    # 4. 领域匹配（辅助加分）
    artifact_domains = artifact.get("domains", [])
    for domain in artifact_domains:
        if domain in profile.get("domains", []):
            score += 0.5

    return score


def select_and_sort(artifacts: List[Dict[str, Any]], profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """根据用户画像筛选并排序文物"""
    if not artifacts:
        return []
    
    # 带儿童时，直接过滤掉不适合儿童的文物
    if profile.get("with_children"):
        artifacts = [a for a in artifacts if a.get("child_friendly", True)]

    # 计算每个文物的得分
    scored_artifacts = []
    for artifact in artifacts:
        score = calculate_score(artifact, profile)
        scored_artifacts.append((artifact, score))
    
    # 按得分降序排序
    scored_artifacts.sort(key=lambda x: -x[1])
    
    # 根据参观时长确定目标数量
    duration = profile["duration"]
    if duration == "2-3小时":
        target_n = 15
    elif duration == "4-5小时":
        target_n = 25
    else:
        target_n = 15

    # 分数阈值
    score_threshold = 4.5
    
    # 高于阈值的文物
    high_score_items = [(a, s) for a, s in scored_artifacts if s >= score_threshold]
    high_score_items.sort(key=lambda x: -x[1])
    len_high_score = len(high_score_items)
    
    output_items = []
    used_names = set()
    
    if len_high_score >= target_n:
        # 得分去重降序，取倒数第二小的分数
        unique_scores = sorted(set(s for _, s in high_score_items), reverse=True)
        if len(unique_scores) >= 2:
            second_lowest_score = unique_scores[-2]
        else:
            second_lowest_score = unique_scores[0]
        
        above_second = [(a, s) for a, s in high_score_items if s > second_lowest_score]
        num_above = len(above_second)
        
        equals_second = [(a, s) for a, s in scored_artifacts if s == second_lowest_score]
        num_needed = target_n - num_above
        
        if num_needed > 0:
            sample_size = min(num_needed, len(equals_second))
            sampled = random.sample(equals_second, sample_size) if equals_second else []
            output_items = above_second + sampled
        else:
            output_items = above_second
    else:
        output_items = high_score_items
    
    # 去重（按文物名称）
    output_list = []
    for artifact, score in output_items:
        name = artifact.get("name", "")
        if name not in used_names:
            output_list.append(artifact)
            used_names.add(name)
    
    current_n = len(output_list)
    
    # 如果不够 target_n，继续补充更低分数的文物
    if current_n < target_n:
        all_scores = sorted(set(s for _, s in scored_artifacts), reverse=True)
        for score in all_scores:
            if score <= score_threshold or len_high_score < target_n:
                candidates = [(a, s) for a, s in scored_artifacts if s == score and a.get("name", "") not in used_names]
                num_left = target_n - current_n
                if candidates:
                    sample_size = min(num_left, len(candidates))
                    sampled = random.sample(candidates, sample_size)
                    for artifact, _ in sampled:
                        name = artifact.get("name", "")
                        if name not in used_names:
                            output_list.append(artifact)
                            used_names.add(name)
                            current_n += 1
                if current_n >= target_n:
                    break
    
    # 按 visit_order > hall > period 排序
    period_order = ["远古时期","夏商西周","春秋战国","秦汉","三国两晋南北朝","隋唐五代","辽宋夏金元","明清"]
    
    def sort_key(artifact):
        if "visit_order" in artifact:
            return (0, artifact["visit_order"])
        hall = artifact.get("hall", "")
        if hall and hall not in ("待确认", "unknown", ""):
            return (1, hall, period_order.index(artifact.get("period", "")) if artifact.get("period", "") in period_order else 99)
        period = artifact.get("period", "")
        period_index = period_order.index(period) if period in period_order else 99
        return (2, period_index)
    
    output_list = sorted(output_list, key=sort_key)

    return output_list


def summarize_reasons_with_llm(artifacts: List[Dict[str, Any]], profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    """使用大模型生成每个文物的推荐理由"""
    if not artifacts:
        return []
    
    # 准备文物数据（含博物馆名称，离线模式下由 artifact.museum_name 提供）
    museum_name = profile.get("museum_name", "")
    artifacts_data = []
    for artifact in artifacts:
        artifacts_data.append({
            "name": artifact.get("name", ""),
            "museum": artifact.get("museum_name", museum_name),
            "type": artifact.get("type", ""),
            "period": artifact.get("period", ""),
            "hall": artifact.get("hall", ""),
            "description": artifact.get("description", ""),
            "is_treasure": artifact.get("is_treasure", False),
        })
    
    prompt = f"""
你是一位专业的博物馆讲解员，请为以下文物各生成一句简短推荐理由（30字以内）。
要求：突出文物的历史价值、艺术特色或趣味亮点，语气积极正向，不要出现任何否定表述。

文物列表：
{json.dumps(artifacts_data, ensure_ascii=False, indent=2)}

请返回JSON格式，key为文物名称，value为推荐理由：
{{
    "文物名称1": "推荐理由1",
    "文物名称2": "推荐理由2"
}}
"""
    
    try:
        result = call_llm_api(prompt)
        if "error" in result:
            # 如果API调用失败，生成默认理由
            for artifact in artifacts:
                artifact["reason"] = f"{artifact.get('name', '文物')}，{artifact.get('description', '')}"
            return artifacts
            
        # 为每个文物添加推荐理由
        for artifact in artifacts:
            name = artifact.get("name", "")
            if name in result:
                artifact["reason"] = result[name]
            else:
                artifact["reason"] = f"{artifact.get('name', '文物')}，{artifact.get('description', '')[:30]}..."
                
    except Exception as e:
        print(f"生成推荐理由失败: {e}", file=sys.stderr)
        for artifact in artifacts:
            artifact["reason"] = f"{artifact.get('name', '文物')}，{artifact.get('description', '')[:30]}..."
    
    return artifacts


def get_museum_info(museum_name: str) -> str:
    """获取博物馆信息"""
    prompt = f"""
    请提供{museum_name}的基本信息，包括：
    1. 位置
    2. 开放时间
    3. 门票信息
    4. 交通信息
    5. 馆内设施（如餐厅、厕所、寄存处等）
    6. 附近景点或设施
 
    要求：
    1. 信息准确，简洁明了，不要包含多余的描述
    2. 请严格按照以下JSON格式返回结果，不要添加任何其他内容：
    {{
        "位置": "博物馆的具体位置",
        "开放时间": "开放时间信息",
        "门票信息": "门票价格和预约方式",
        "交通信息": "如何到达博物馆",
        "馆内设施": "馆内设施信息",
        "附近景点或设施": "附近的景点或设施"
    }}
    """
    
    try:
        result = call_llm_api(prompt)
        if isinstance(result, dict):
            info = []
            if result.get("位置"):
                info.append(f"**📍 位置：** {result['位置']}")
            if result.get("开放时间"):
                info.append(f"**⏰ 开放时间：** {result['开放时间']}")
            if result.get("门票信息"):
                info.append(f"**🎫 门票：** {result['门票信息']}")
            if result.get("交通信息"):
                info.append(f"**🚗 交通：** {result['交通信息']}")
            if result.get("馆内设施"):
                info.append(f"**🏪 馆内设施：** {result['馆内设施']}")
            if result.get("附近景点或设施"):
                info.append(f"**🏙️ 附近：** {result['附近景点或设施']}")
            if info:
                return "\n".join(info)
    except Exception as e:
        print(f"获取博物馆信息失败: {e}", file=sys.stderr)
    
    # 默认信息
    default_info = [
        f"**📍 位置：** 请查询{museum_name}官方网站获取准确位置",
        f"**⏰ 开放时间：** 请查询{museum_name}官方网站获取准确开放时间",
        f"**🎫 门票：** 请查询{museum_name}官方网站获取准确门票信息",
        f"**🚗 交通：** 请查询{museum_name}官方网站获取准确交通信息",
        f"**🏪 馆内设施：** 请查询{museum_name}官方网站获取馆内设施信息",
        f"**🏙️ 附近：** 请查询{museum_name}官方网站获取附近景点信息"
    ]
    return "\n".join(default_info)


def format_markdown_table(artifacts: List[Dict[str, Any]]) -> str:
    """将文物列表格式化为Markdown表格"""
    if not artifacts:
        return "没有找到符合条件的文物"
    
    # 检查展馆信息是否充足
    valid_hall_count = 0
    for artifact in artifacts:
        hall = artifact.get("hall", "")
        if hall and hall != "待确认":
            valid_hall_count += 1
    
    # 决定是否显示展馆列
    show_hall = valid_hall_count > len(artifacts) * 0.3
    
    # 构建表头
    if show_hall:
        headers = ["序号", "文物名称", "展馆", "时期", "推荐理由"]
    else:
        headers = ["序号", "文物名称", "时期", "推荐理由"]
    
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---" for _ in headers]) + " |\n"
    
    # 构建表格内容
    for i, artifact in enumerate(artifacts, 1):
        name = artifact.get("name", "未知文物")
        period = artifact.get("period", "未知时期")
        reason = artifact.get("reason", "无推荐理由")
        
        # 处理长文本
        if len(reason) > 50:
            reason = reason[:47] + "..."
        
        # 为文物名称加粗
        bold_name = f"**{name}**"
    
        is_treasure = artifact.get("is_treasure", False)
        
        # 为镇馆之宝添加⭐标注
        if is_treasure:
            display_name = f"{bold_name} ⭐"
        else:
            display_name = bold_name
            
        if show_hall:
            hall = artifact.get("hall", "待确认")
            row = [
                str(i),
                display_name,
                hall,
                period,
                reason
            ]
        else:
            row = [
                str(i),
                display_name,
                period,
                reason
            ]
        
        table += "| " + " | ".join(row) + " |\n"
    
    return table


def main():
    import argparse
    parser = argparse.ArgumentParser(description="博物馆参观路线规划")
    parser.add_argument("--profile", required=True, help="用户画像JSON文件路径")
    parser.add_argument("--artifacts", required=True, help="文物列表JSON文件路径")
    parser.add_argument("--output", help="输出结果文件路径")
    args = parser.parse_args()
    
    # 读取用户画像
    with open(args.profile, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    
    # 读取文物列表
    with open(args.artifacts, 'r', encoding='utf-8') as f:
        artifacts = json.load(f)
    
    # 标准化用户画像
    normalized_profile = normalize_profile(profile)
    
    # 筛选并排序文物
    selected_artifacts = select_and_sort(artifacts, normalized_profile)
    
    # 生成推荐理由
    selected_artifacts = summarize_reasons_with_llm(selected_artifacts, normalized_profile)
    
    # 格式化为Markdown表格
    markdown_table = format_markdown_table(selected_artifacts)
    
    # 生成最终结果
    final_output = build_output(normalized_profile, selected_artifacts, markdown_table)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"路线规划结果已保存到: {args.output}")
    else:
        print(final_output)


def build_output(profile: dict, artifacts: list, markdown_table: str) -> str:
    """构建最终输出
    
    Args:
        profile: 标准化后的用户画像
        artifacts: 选中的文物列表
        markdown_table: 文物表格
        
    Returns:
        最终的Markdown输出
    """
    museum_name = profile.get("museum_name", "博物馆")
    header = f"\n## 🗺️ {museum_name} 参观路线规划\n"
    meta = f"### 📊 参观信息\n"
    meta += f"- ⏱️ 参观时长：{profile.get('duration')}\n"
    meta += f"- 📍 推荐文物数：{len(artifacts)} 件\n"
    meta += f"- 👣 首次参观：{'是' if profile.get('first_visit') else '否'}\n"
    meta += f"- 👶 携带儿童：{'是' if profile.get('with_children') else '否'}\n\n"
    
    # 添加博物馆信息
    museum_info = get_museum_info(museum_name)
    museum_info_section = f"\n## 🏛️ {museum_name} 基本信息\n{museum_info}\n"
    
    return header + meta + markdown_table + museum_info_section


if __name__ == "__main__":
    main()