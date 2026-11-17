"""开源大模型选型助手 - 根据任务/预算/部署推荐最优模型"""

MODELS = {
    "deepseek-v3": {
        "name": "DeepSeek V3",
        "company": "深度求索",
        "region": "cn",
        "architecture": "MoE (671B, 37B激活)",
        "context": 128_000,
        "api_cost_per_m": 0.28,  # 元/百万token
        "local_possible": True,
        "strengths": ["reasoning", "math", "code", "logic"],
        "best_for": "推理/数学/代码天花板",
    },
    "deepseek-r1": {
        "name": "DeepSeek R1",
        "company": "深度求索",
        "region": "cn",
        "architecture": "MoE (671B, 37B激活)",
        "context": 128_000,
        "api_cost_per_m": 0.56,
        "local_possible": True,
        "strengths": ["reasoning", "math", "logic", "science"],
        "best_for": "深度推理/思维链",
    },
    "qwen3-72b": {
        "name": "Qwen3-72B",
        "company": "阿里巴巴",
        "region": "cn",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 2.0,
        "local_possible": True,
        "strengths": ["chinese", "multimodal", "tool_use", "code"],
        "best_for": "中文对话/多模态/工具调用",
    },
    "chatglm-4": {
        "name": "ChatGLM-4",
        "company": "智谱AI",
        "region": "cn",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 1.0,
        "local_possible": True,
        "strengths": ["chinese", "tool_use", "enterprise"],
        "best_for": "中文理解/企业级/工具调用",
    },
    "yi-34b": {
        "name": "Yi-1.5-34B",
        "company": "零一万物",
        "region": "cn",
        "architecture": "Dense",
        "context": 200_000,
        "api_cost_per_m": 1.5,
        "local_possible": True,
        "strengths": ["long_context", "reasoning", "math"],
        "best_for": "长文档/推理",
    },
    "minimax-01": {
        "name": "MiniMax-Text-01",
        "company": "MiniMax",
        "region": "cn",
        "architecture": "MoE (456B, 45.9B激活)",
        "context": 1_000_000,
        "api_cost_per_m": 0.5,
        "local_possible": False,
        "strengths": ["long_context", "linear_attention", "cost"],
        "best_for": "超长文档/低成本",
    },
    "kimi-k3": {
        "name": "Kimi K3",
        "company": "月之暗面",
        "region": "cn",
        "architecture": "MoE (1T+, 稀疏激活)",
        "context": 128_000,
        "api_cost_per_m": 0.6,
        "local_possible": False,
        "strengths": ["agent", "subagent", "long_context", "multimodal"],
        "best_for": "Agent/子Agent架构",
    },
    "llama4-70b": {
        "name": "Llama 4",
        "company": "Meta",
        "region": "global",
        "architecture": "MoE (17B-2T)",
        "context": 128_000,
        "api_cost_per_m": 1.0,
        "local_possible": True,
        "strengths": ["community", "ecosystem", "fine_tune", "multilingual"],
        "best_for": "社区生态/微调/多语言",
    },
    "mistral-7b": {
        "name": "Mistral 7B",
        "company": "Mistral AI",
        "region": "global",
        "architecture": "Dense",
        "context": 32_000,
        "api_cost_per_m": 0.3,
        "local_possible": True,
        "strengths": ["efficiency", "code", "lightweight"],
        "best_for": "轻量部署/效率优先",
    },
    "mixtral-8x22b": {
        "name": "Mixtral 8x22B",
        "company": "Mistral AI",
        "region": "global",
        "architecture": "MoE (8x22B, 39B激活)",
        "context": 65_000,
        "api_cost_per_m": 0.8,
        "local_possible": True,
        "strengths": ["code", "reasoning", "multilingual"],
        "best_for": "MoE效率/代码/多语言",
    },
    "gemma3-27b": {
        "name": "Gemma 3 27B",
        "company": "Google",
        "region": "global",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 0.5,
        "local_possible": True,
        "strengths": ["lightweight", "safety", "vision"],
        "best_for": "单GPU部署/安全对齐",
    },
    "phi-4-14b": {
        "name": "Phi-4 14B",
        "company": "Microsoft",
        "region": "global",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 0.3,
        "local_possible": True,
        "strengths": ["small_model", "reasoning", "edge"],
        "best_for": "小模型推理天花板/端侧部署",
    },
    "falcon2-180b": {
        "name": "Falcon 2 180B",
        "company": "TII",
        "region": "global",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 1.2,
        "local_possible": True,
        "strengths": ["multilingual", "arabic", "enterprise"],
        "best_for": "多语言/企业级",
    },
    "granite3-34b": {
        "name": "Granite 3 34B",
        "company": "IBM",
        "region": "global",
        "architecture": "Dense",
        "context": 128_000,
        "api_cost_per_m": 0.8,
        "local_possible": True,
        "strengths": ["code", "rag", "compliance", "enterprise"],
        "best_for": "企业级代码/RAG/安全合规",
    },
    "dbrx": {
        "name": "DBRX",
        "company": "Databricks",
        "region": "global",
        "architecture": "MoE (132B, 36B激活)",
        "context": 32_000,
        "api_cost_per_m": 0.6,
        "local_possible": True,
        "strengths": ["moe", "reasoning", "code"],
        "best_for": "MoE架构/推理/代码",
    },
}


def recommend(task_type: str, budget: str = "balanced", deploy: str = "api"):
    """推荐模型"""
    task_map = {
        "reasoning": ["reasoning", "math", "logic", "science"],
        "chat": ["chinese", "multilingual", "tool_use"],
        "code": ["code"],
        "vision": ["multimodal", "vision"],
        "agent": ["agent", "subagent", "tool_use"],
        "long_doc": ["long_context", "linear_attention"],
        "edge": ["small_model", "lightweight", "edge"],
        "enterprise": ["enterprise", "compliance"],
    }

    required = task_map.get(task_type, ["chinese", "code"])
    candidates = []

    for key, m in MODELS.items():
        match = sum(1 for s in required if s in m["strengths"])
        if match == 0:
            continue
        if deploy == "local" and not m["local_possible"]:
            continue
        candidates.append((match, key))

    if not candidates:
        return {"error": f"No models for task: {task_type}"}

    candidates.sort(key=lambda x: -x[0])
    best_key = candidates[0][1]
    best = MODELS[best_key]

    # 按预算调整
    if budget == "cheap" and best["api_cost_per_m"] > 0.5:
        cheap = [k for k, v in MODELS.items() if v["api_cost_per_m"] <= 0.5 and deploy != "local" or v["local_possible"]]
        if cheap:
            best_key = cheap[0]
            best = MODELS[best_key]

    return {
        "recommended": best_key,
        "model": best["name"],
        "company": best["company"],
        "region": "国内" if best["region"] == "cn" else "国际",
        "architecture": best["architecture"],
        "context": f"{best['context']:,} tokens",
        "api_cost": f"¥{best['api_cost_per_m']}/百万token",
        "best_for": best["best_for"],
    }


def list_all(region: str = None):
    """列出所有模型"""
    result = []
    for key, m in MODELS.items():
        if region and m["region"] != region:
            continue
        result.append({
            "key": key,
            "name": m["name"],
            "company": m["company"],
            "region": "国内" if m["region"] == "cn" else "国际",
            "cost": f"¥{m['api_cost_per_m']}/M",
            "strengths": ", ".join(m["strengths"]),
            "best_for": m["best_for"],
        })
    return result


if __name__ == "__main__":
    import json

    print("=== 开源大模型选型助手 ===")
    print()

    tasks = ["reasoning", "chat", "code", "agent", "long_doc", "edge", "enterprise"]
    for t in tasks:
        r = recommend(t, budget="balanced", deploy="api")
        if "error" not in r:
            print(f"[{t}] → {r['model']} ({r['company']}) - {r['best_for']} | {r['api_cost']}")

    print()
    print("=== 国内模型 ===")
    for m in list_all(region="cn"):
        print(f"  {m['name']:20s} {m['company']:8s} {m['cost']:10s} {m['best_for']}")

    print()
    print("=== 国际模型 ===")
    for m in list_all(region="global"):
        print(f"  {m['name']:20s} {m['company']:12s} {m['cost']:10s} {m['best_for']}")
