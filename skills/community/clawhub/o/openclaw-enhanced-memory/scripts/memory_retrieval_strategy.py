#!/usr/bin/env python3
"""
记忆检索策略 (Memory Retrieval Strategy)
根据对话类型自动检索最相关的记忆模块
"""

import os
import re
from pathlib import Path

MEMORY_BASE = Path("/home/clawdbot/.openclaw/workspace/memory")

# 查询类型分类
QUERY_TYPES = {
    # 食物相关
    "food": [
        r"吃的|吃的什么|午饭|晚饭|早餐|中午|晚上|宵夜|点外卖|吃饭|菜|味道|好吃|难吃",
        r"食谱|菜谱|做法|配料|调味",
    ],

    # 训练/运动相关
    "training": [
        r"训练|运动|健身|爬山|攀岩|跑步|跳绳|力量|练肌肉|器材|场地|消耗|卡路里|体重",
        r"桌球|台球|羽毛球|篮球|足球|游戏",
    ],

    # 关系/人物相关
    "relation": [
        r"朋友|朋友叫什么|认识|谁认识谁|社交|聚会|关系",
        r"父母|家人|父母在干嘛|回家|视频",
        # 常见人名（高优先级匹配）
        r"(杨凌霄|张浩东|刘子锐|高东瑞|吕澄轩|廖擎杰|赵鸿剑|邱冠儒|王隆哲|母琳珲|刘辉|冯葵开|何展逸|范昕|刘泽洋|黄谢郁|张雨晨|刘妍君|李豆豆|咪咪豆|豆豆|吴疆|彭潇冉|胡慧琳|杨郑州|张仲光)",
        # 人名模式（匹配常见模式）
        r"[刘杨张王李黄何廖吕高邱赵][峰|浩|宇|洋|明|杰|磊|雨|泽|涛|洋|洋|鹏|军]?\s*哥?|"
        r"[王李张刘杨赵][辉|伟|明|杰|丽|芳|娜|婷]?\s*姐?|"
        r"[陈杨林何郭黄李王张刘][峰|宇|浩|洋|明|杰|磊|杰|雨|泽]?\s*哥?|"
        r"[何展逸|范昕|刘泽洋|黄谢郁|刘妍君|李豆豆|咪咪豆|豆豆|吴疆|彭潇冉|胡慧琳|杨郑州|张仲光]",
    ],

    # 悠悠相关（宠物）
    "yoyo": [
        r"悠悠|yoyo|狗狗|宠物|狗|泰迪|汪汪|叫",
    ],

    # 系统相关
    "system": [
        r"系统|配置|bug|报错|崩溃|重启|openclaw|gateway|机器人",
    ],

    # 情绪/心情相关
    "mood": [
        r"心情|开心|难过|生气|焦虑|想骂人|吐槽",
    ],

    # 莫莫咖相关
    "momonga": [
        r"莫莫咖|momonga|飞鼠|可爱|夸奖|抱抱|亲亲|干嘛|为什么",
    ],

    # 项目/工作相关
    "project": [
        r"项目|工作|开发|代码|git|commit|push|pull|bug|修复",
    ],
}

# 默认检索范围（如果不确定）
DEFAULT_SCOPE = "current"


def classify_query(query: str) -> str:
    """
    根据查询内容分类查询类型
    Returns: "food", "training", "relation", "yoyo", "system", "mood", "momonga", "project", 或 "default"
    """
    query_lower = query.lower()

    # 按优先级检查
    for query_type, patterns in QUERY_TYPES.items():
        for pattern in patterns:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return query_type

    return "default"


def get_relevant_paths(query: str, top_k: int = 3) -> list:
    """
    根据查询类型返回最相关的记忆路径
    Returns: list of (path, score)
    """
    query_type = classify_query(query)
    relevant_paths = []

    # 定义各类型的检索范围（使用相对于 MEMORY_BASE 的路径）
    SCOPE_MAPPING = {
        "food": ["food", "current/food"],
        "training": ["training", "current/training"],
        "relation": ["RELATION", "connections.md"],
        "yoyo": ["RELATION/悠悠.md", "connections.md"],
        "system": ["system"],
        "mood": ["current"],
        "momonga": ["current"],
        "project": ["current", "misc"],
        "default": ["current", "2026-02"],
    }

    scopes = SCOPE_MAPPING.get(query_type, SCOPE_MAPPING["default"])

    # 扫描各个范围
    for scope in scopes:
        scope_path = MEMORY_BASE / scope
        if scope_path.exists():
            # 如果是文件
            if scope_path.is_file():
                relevant_paths.append((str(scope_path), 1.0))

            # 如果是目录，扫描所有 .md 文件
            elif scope_path.is_dir():
                # 提取人名列表
                names = re.findall(r"([刘杨张王李黄何廖吕高邱赵][峰|浩|宇|洋|明|杰|磊|雨|泽|涛|洋|洋|鹏|军]?\s*哥?|[王李张刘杨赵][辉|伟|明|杰|丽|芳|娜|婷]?\s*姐?|[何展逸|范昕|刘泽洋|黄谢郁|刘妍君|李豆豆|咪咪豆|豆豆|吴疆|彭潇冉|胡慧琳|杨郑州|张仲光])", query)

                for md_file in scope_path.rglob("*.md"):
                    # 跳过归档文件
                    if "archived" in str(md_file):
                        continue
                    # 计算相关性分数
                    score = 0.5  # 基础分数

                    # 人名匹配优先
                    if query_type == "relation":
                        file_name = md_file.stem
                        # 检查查询中是否包含文件名中的人名
                        for name in names:
                            if name and name.lower() in file_name.lower():
                                score = 1.0  # 完全匹配！
                                break
                        if score < 0.8:
                            score = 0.8  # 基础关系文件分数
                    elif query_type == "yoyo" and "悠悠" in str(md_file):
                        score = 1.0

                    relevant_paths.append((str(md_file), score))

    # 按分数排序
    relevant_paths.sort(key=lambda x: x[1], reverse=True)

    # 返回前 top_k 个路径
    return relevant_paths[:top_k]


def search_memory_smart(query: str, top_k: int = 5):
    """
    智能记忆检索 - 根据查询类型自动检索最相关的记忆
    """
    print(f"🔍 [Smart Search] Query: {query}")
    print(f"📊 Query Type: {classify_query(query)}")

    relevant_paths = get_relevant_paths(query, top_k)

    if not relevant_paths:
        print("⚠️ No relevant memory paths found.")
        return []

    print(f"📂 Relevant paths (top {len(relevant_paths)}):")
    for path, score in relevant_paths:
        print(f"   - {path} (score: {score})")

    # 这里可以继续调用 memory_skill.py 的 search 功能
    # 或者直接读取这些文件的内容

    return relevant_paths


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 memory_retrieval_strategy.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = search_memory_smart(query)
