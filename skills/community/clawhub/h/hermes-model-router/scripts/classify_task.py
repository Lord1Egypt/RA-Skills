#!/usr/bin/env python3
"""
Model Router - 任务分类器
根据任务描述判断复杂度并推荐模型
"""

import json
import sys
import os

# 简单任务关键词
SIMPLE_KEYWORDS = [
    "翻译", "润色", "格式", "转换", "查", "定义",
    "写一个简单的", "quick", "simple", "translate", "polish",
    "总结", "摘要", "提取"
]

# 复杂任务关键词
COMPLEX_KEYWORDS = [
    "调试", "分析", "架构", "设计", "战略", "报告",
    "debug", "analyze", "architecture", "design", "strategy",
    "3000字", "长文", "复杂", "推理", "证明", "为什么"
]

# 开发/全栈任务关键词（这类任务通常是复杂的）
DEV_KEYWORDS = [
    "写一个", "写个", "开发", "前端", "后端", "全栈",
    "SPA", "App", "应用", "网站", "系统", "平台",
    "接口", "API", "数据库", "登录", "注册", "管理后台",
    "组件", "页面", "路由", "切图", "UI", "UE",
    "classify", "classifier", "script", "脚本", "工具",
    "自动化", "机器人", "bot", "爬虫", "抓取",
    "部署", "docker", "k8s", "kubernetes", "CI/CD",
]


def classify_task(task_description: str, verbose: bool = False) -> dict:
    """判断任务复杂度并返回推荐模型"""
    
    task_lower = task_description.lower()
    
    # 推理类任务默认复杂
    has_reasoning = any(kw in task_lower for kw in ["推理", "证明", "为什么", "reason", "prove", "why"])
    
    # 复杂任务判断
    has_complex = any(kw in task_lower for kw in COMPLEX_KEYWORDS)

    # 开发/全栈任务判断（这类任务通常是复杂的）
    has_dev = any(kw in task_lower for kw in DEV_KEYWORDS)

    # 简单任务判断
    has_simple = any(kw in task_lower for kw in SIMPLE_KEYWORDS)

    if has_complex or has_reasoning or has_dev:
        complexity = "复杂"
        route = "服务商模型 (MiniMax / OpenRouter)"
        if has_dev:
            reason = "开发/全栈任务，需要多文件/多模块实现"
        else:
            reason = "需要深度推理或多步分析"
        local_model = None
        cloud_model = "MiniMax-Text-01"
    elif has_simple:
        complexity = "简单"
        route = "本地模型 (Ollama)"
        reason = "单次完成，无需迭代"
        local_model = "qwen2.5-coder:7b"
        cloud_model = None
    else:
        complexity = "简单"
        route = "本地模型 (Ollama)"
        reason = "默认简单任务"
        local_model = "qwen2.5-coder:7b"
        cloud_model = None
    
    result = {
        "task": task_description,
        "complexity": complexity,
        "route": route,
        "reason": reason
    }
    
    if verbose:
        result["local_model"] = local_model
        result["cloud_model"] = cloud_model
        result["matched_keywords"] = [
            kw for kw in COMPLEX_KEYWORDS + SIMPLE_KEYWORDS + DEV_KEYWORDS
            if kw.lower() in task_lower
        ]
    
    return result


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    if len(sys.argv) < 2:
        print("用法: python3 classify_task.py <任务描述> [--verbose]")
        print("")
        print("示例:")
        print('  python3 classify_task.py "帮我翻译成英文"')
        print('  python3 classify_task.py "分析市场策略" --verbose')
        sys.exit(1)
    
    # 获取任务描述（过滤掉 --verbose）
    task_description = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("--")])
    
    result = classify_task(task_description, verbose)
    
    print(f"\n📋 任务: {result['task']}")
    print(f"⚡ 复杂度: {result['complexity']}")
    print(f"🎯 路由: {result['route']}")
    print(f"💡 理由: {result['reason']}")
    
    if verbose and result.get("matched_keywords"):
        print(f"\n🔍 匹配关键词: {', '.join(result['matched_keywords'])}")
    
    if verbose:
        if result["local_model"]:
            print(f"\n📦 本地模型: {result['local_model']}")
        if result["cloud_model"]:
            print(f"☁️  服务商模型: {result['cloud_model']}")
    
    print()
    
    # 返回退出码：0=简单，1=复杂
    sys.exit(0 if result["complexity"] == "简单" else 1)


if __name__ == "__main__":
    main()
