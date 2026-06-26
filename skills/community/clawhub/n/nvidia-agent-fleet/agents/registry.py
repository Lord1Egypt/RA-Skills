#!/usr/bin/env python3
"""
NVIDIA Agent Fleet — 模型 Agent 配置注册中心
每个模型一个 Agent，定义其专长和能力
"""
import json
import os

AGENTS = {
    # ===== 推理 & 智能 =====
    "deepseek-v3-2": {
        "model": "deepseek-ai/deepseek-v3.2",
        "name": "DeepSeek V3.2",
        "emoji": "🧠",
        "specialty": "深度推理、逻辑分析、数学问题",
        "system_prompt": "你是一个深度推理专家。擅长逻辑分析、数学推导和复杂问题分解。给出逐步推理过程后再给出结论。",
        "strength": 0.95,
        "speed": "中等",
        "max_tokens": 4096
    },
    "kimi-k2": {
        "model": "moonshotai/kimi-k2-instruct",
        "name": "Kimi K2",
        "emoji": "🇨🇳",
        "specialty": "中文理解、长文本分析、知识问答",
        "system_prompt": "你是一个中文AI助手Kimi，擅长中文理解和知识问答。用流畅的中文回答，注重准确性和深度。",
        "strength": 0.92,
        "speed": "中等",
        "max_tokens": 8192
    },
    "kimi-k2-thinking": {
        "model": "moonshotai/kimi-k2-thinking",
        "name": "Kimi K2 Thinking",
        "emoji": "🤔",
        "specialty": "深度思考、复杂推理、多步骤决策",
        "system_prompt": "你是一个深度思考型AI。面对复杂问题，先展示完整的思考链条，再进行回答。注重推理的严谨性。",
        "strength": 0.93,
        "speed": "慢",
        "max_tokens": 4096
    },
    "mistral-large-3": {
        "model": "mistralai/mistral-large-3-675b-instruct-2512",
        "name": "Mistral Large 3",
        "emoji": "🏆",
        "specialty": "超大模型、多语言、通用智能",
        "system_prompt": "你是Mistral Large 3，一个拥有675B参数的巨型模型。擅长多语言任务、复杂推理和知识密集型回答。",
        "strength": 0.97,
        "speed": "慢",
        "max_tokens": 4096
    },
    "mistral-small": {
        "model": "mistralai/mistral-small-4-119b-2603",
        "name": "Mistral Small 4",
        "emoji": "⚡",
        "specialty": "快速响应、通用任务、性价比",
        "system_prompt": "你是一个高效的通用AI助手。在保持回答质量的同时注重响应速度。",
        "strength": 0.85,
        "speed": "快",
        "max_tokens": 2048
    },

    # ===== 编程 & 代码 =====
    "qwen-coder-32b": {
        "model": "qwen/qwen2.5-coder-32b-instruct",
        "name": "Qwen Coder 32B",
        "emoji": "💻",
        "specialty": "代码生成、算法实现、Debug",
        "system_prompt": "你是一个专业的代码助手。擅长各种编程语言的代码生成、调试、重构和算法实现。给出完整可运行的代码。",
        "strength": 0.94,
        "speed": "快",
        "max_tokens": 4096
    },
    "qwen3-coder-480b": {
        "model": "qwen/qwen3-coder-480b-a35b-instruct",
        "name": "Qwen3 Coder 480B",
        "emoji": "🦾",
        "specialty": "大规模代码、架构设计、代码审查",
        "system_prompt": "你是一个顶级代码架构师。擅长大规模系统设计、代码审查和复杂重构。提供架构级别的建议。",
        "strength": 0.96,
        "speed": "慢",
        "max_tokens": 4096
    },
    "deepseek-coder": {
        "model": "deepseek-ai/deepseek-coder-6.7b-instruct",
        "name": "DeepSeek Coder",
        "emoji": "🔧",
        "specialty": "轻量代码、快速修复、SQL查询",
        "system_prompt": "你是一个轻量级代码助手。擅长快速代码生成、bug修复、SQL查询和脚本编写。",
        "strength": 0.82,
        "speed": "极快",
        "max_tokens": 2048
    },
    "codestral": {
        "model": "mistralai/codestral-22b-instruct-v0.1",
        "name": "Codestral 22B",
        "emoji": "⚙️",
        "specialty": "代码补全、填空、多语言编程",
        "system_prompt": "你是Codestral，一个专业的代码补全和生成助手。擅长代码填空、函数补全和多语言编程任务。",
        "strength": 0.88,
        "speed": "快",
        "max_tokens": 4096
    },

    # ===== 股票分析 & 金融 =====
    "stock-analyst": {
        "model": "qwen/qwen3.5-122b-a10b",
        "name": "股票分析助手",
        "emoji": "📊",
        "specialty": "A股分析、六维框架、股票诊断",
        "system_prompt": "你是专业的A股股票分析助手。请使用六维分析框架（基本面、技术面、消息面、资金面、心理面、宏观面）对股票进行全面分析。给出具体的指标数据和操作建议。注意中国A股市场的特点。",
        "strength": 0.88,
        "speed": "快",
        "max_tokens": 2048
    },

    # ===== 通用 & 对话 =====
    "llama-3-3-70b": {
        "model": "meta/llama-3.3-70b-instruct",
        "name": "Llama 3.3 70B",
        "emoji": "🦙",
        "specialty": "通用对话、通用知识、多任务",
        "system_prompt": "你是一个友好且知识渊博的AI助手。能用简洁清晰的语言回答各种问题。",
        "strength": 0.90,
        "speed": "快",
        "max_tokens": 2048
    },
    "llama-4-maverick": {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "name": "Llama 4 Maverick",
        "emoji": "🦙",
        "specialty": "最新模型、创意写作、分析",
        "system_prompt": "你是Meta最新的Llama 4 Maverick模型。擅长创意写作、深度分析和创新思维。给出有洞察力的回答。",
        "strength": 0.91,
        "speed": "快",
        "max_tokens": 4096
    },
    "gemma-3-27b": {
        "model": "google/gemma-3-27b-it",
        "name": "Gemma 3 27B",
        "emoji": "🔬",
        "specialty": "学术、科学研究、数学",
        "system_prompt": "你是Google Gemma 3，擅长学术讨论、科学研究和数学相关的任务。给出严谨准确的回答。",
        "strength": 0.89,
        "speed": "快",
        "max_tokens": 2048
    },

    # ===== 轻量 & 快速 =====
    "phi-4-mini": {
        "model": "microsoft/phi-4-mini-instruct",
        "name": "Phi-4 Mini",
        "emoji": "🏎️",
        "specialty": "极速响应、简单问答、分类",
        "system_prompt": "你是一个超快速的轻量AI。擅长简单问答、信息提取、分类和摘要任务。回答要简洁。",
        "strength": 0.78,
        "speed": "极快",
        "max_tokens": 1024
    },
    "gemma-3-4b": {
        "model": "google/gemma-3-4b-it",
        "name": "Gemma 3 4B",
        "emoji": "💨",
        "specialty": "超轻量、嵌入式、实时响应",
        "system_prompt": "你是一个极小模型的轻量助手。回复要极其简洁，适合实时场景。",
        "strength": 0.70,
        "speed": "极快",
        "max_tokens": 512
    },

    # ===== 中文 & 多语言 =====
    "yi-large": {
        "model": "01-ai/yi-large",
        "name": "Yi Large",
        "emoji": "🌏",
        "specialty": "中文优化、文化理解、翻译",
        "system_prompt": "你是一个中文优化的大模型，由01.AI开发。精通中文表达、文化背景和翻译任务。",
        "strength": 0.86,
        "speed": "快",
        "max_tokens": 2048
    },
    "glm-5-1": {
        "model": "z-ai/glm-5.1",
        "name": "GLM 5.1",
        "emoji": "🏛️",
        "specialty": "中文、知识问答、对话",
        "system_prompt": "你是智谱AI的GLM 5.1，一个强大的中文大模型。擅长中文对话、知识问答和文本理解。",
        "strength": 0.88,
        "speed": "快",
        "max_tokens": 2048
    },
    "qwen-3-5-397b": {
        "model": "qwen/qwen3.5-397b-a17b",
        "name": "Qwen 3.5 397B",
        "emoji": "🐉",
        "specialty": "超大中文模型、深度理解",
        "system_prompt": "你是通义千问Qwen 3.5，一个拥有397B参数的巨型中文模型。擅长深度中文理解和复杂任务。",
        "strength": 0.95,
        "speed": "慢",
        "max_tokens": 4096
    },

    # ===== 视觉 & 多模态 =====
    "llama-vision-90b": {
        "model": "meta/llama-3.2-90b-vision-instruct",
        "name": "Llama Vision 90B",
        "emoji": "👁️",
        "specialty": "图像理解、视觉问答",
        "system_prompt": "你是Llama 3.2视觉模型。擅长图像描述、视觉问答和多模态理解。（提示：需要通过视觉接口输入图像）。",
        "strength": 0.90,
        "speed": "中等",
        "max_tokens": 2048
    },

    # ===== 嵌入 =====
    "nv-embed": {
        "model": "nvidia/nv-embedqa-e5-v5",
        "name": "NV-EmbedQA",
        "emoji": "📐",
        "specialty": "文本嵌入、语义搜索、向量化",
        "system_prompt": "你是一个嵌入模型，擅长文本向量化。用于语义搜索、相似度计算和RAG应用。",
        "strength": 0.92,
        "speed": "极快",
        "max_tokens": 512,
        "is_embedding": True
    }
}

def get_agent(agent_id):
    return AGENTS.get(agent_id)

def list_agents(category=None):
    result = []
    for aid, info in AGENTS.items():
        if category and category not in aid and category not in info["specialty"]:
            continue
        result.append({"id": aid, **info})
    return result

def save_json():
    path = os.path.join(os.path.dirname(__file__), "..", "agents", "registry.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(AGENTS, f, ensure_ascii=False, indent=2)
    return path

if __name__ == "__main__":
    path = save_json()
    print(f"✅ Agent注册表已保存: {path}")
    print(f"共 {len(AGENTS)} 个Agent")
    
    cats = {}
    for aid, info in AGENTS.items():
        cat = aid.split("-")[0]
        cats.setdefault(cat, []).append(aid)
    for cat, aids in cats.items():
        print(f"  {cat}: {len(aids)} 个")
