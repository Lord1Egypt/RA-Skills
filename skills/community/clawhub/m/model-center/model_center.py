"""
NVIDIA AI模型中心
NVIDIA AI Model Center
功能：
1. 集成NVIDIA NIM API (42+模型)
2. 支持LLM、视觉模型、嵌入模型
3. 统一的API调用接口
4. 价格比较和优化建议
"""

import os
import json
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

# NVIDIA NIM API配置
NVIDIA_API_BASE = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")  # 需要从NVIDIA开发者平台获取

# Enrichment data (pricing, capabilities) — API doesn't expose this
# Real model list is fetched live from https://integrate.api.nvidia.com/v1/models
MODELS_ENRICHED = {
    "meta/llama-3.1-70b-instruct": {
        "name": "Llama 3.1 70B Instruct", "provider": "Meta", "type": "chat",
        "context_length": 128000, "pricing": {"input": 0, "output": 0},
        "description": "Meta's most capable open-source model", "strengths": ["multilingual", "long context"]
    },
    "meta/llama-3.1-405b-instruct": {
        "name": "Llama 3.1 405B Instruct", "provider": "Meta", "type": "chat",
        "context_length": 128000, "pricing": {"input": 0, "output": 0},
        "description": "Meta's largest open-source model", "strengths": ["top performance", "long context"]
    },
    "01-ai/yi-large": {
        "name": "01.AI Yi Large", "provider": "01.AI", "type": "chat",
        "context_length": 32000, "pricing": {"input": 1.0, "output": 1.0},
        "description": "01.AI flagship model", "strengths": ["reasoning", "programming"]
    },
    "qwen2.5-72b-instruct": {
        "name": "Qwen 2.5 72B Instruct", "provider": "Alibaba",
        "context_length": 32768, "pricing": {"input": 0.9, "output": 0.9},
        "description": "Alibaba Qwen series flagship", "strengths": ["Chinese", "code"]
    },
    "mistralai/mistral-7b-instruct-v0.3": {
        "name": "Mistral 7B v0.3 Instruct", "provider": "Mistral AI",
        "context_length": 32768, "pricing": {"input": 0.1, "output": 0.1},
        "description": "Efficient open-source model", "strengths": ["efficiency", "multilingual"]
    },
    "deepseek-ai/deepseek-coder-6.7b-instruct": {
        "name": "DeepSeek Coder 6.7B", "provider": "DeepSeek",
        "context_length": 16384, "pricing": {"input": 0.2, "output": 0.2},
        "description": "Specialized code generation model", "strengths": ["code", "reasoning"]
    },
    "google/gemma-2-27b-it": {
        "name": "Gemma 2 27B IT", "provider": "Google",
        "context_length": 8192, "pricing": {"input": 0.3, "output": 0.3},
        "description": "Google's efficient model", "strengths": ["efficiency", "reasoning"]
    },
    "baai/bge-m3": {
        "name": "BGE-M3", "provider": "BAAI", "type": "embedding",
        "context_length": 8192, "pricing": {"input": 0.05, "output": 0},
        "description": "Multilingual embedding model", "strengths": ["multilingual", "retrieval"]
    },
    "stabilityai/sdxl-turbo": {
        "name": "SDXL Turbo", "provider": "Stability AI", "type": "image-generation",
        "pricing": {"input": 0.04, "output": 0.04},
        "description": "Fast image generation", "strengths": ["speed", "quality"]
    },
    "stabilityai/sdxl-lightning": {
        "name": "SDXL Lightning", "provider": "Stability AI", "type": "image-generation",
        "pricing": {"input": 0.02, "output": 0.02},
        "description": "Ultra-fast image generation", "strengths": ["ultra-fast", "low cost"]
    },
}

def _categorize_model(model_id):
    l = model_id.lower()
    if "embed" in l or "bge" in l:
        return "embedding"
    if "rerank" in l:
        return "rerank"
    if any(k in l for k in ["sdxl", "playground", "stable-diffusion"]):
        return "vision"
    return "llm"


class NVIDIAAPIClient:
    """NVIDIA API客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or NVIDIA_API_KEY
        if not self.api_key:
            print("警告: NVIDIA_API_KEY 未设置。请设置环境变量或传入 api_key 参数。")
            print("获取密钥: https://build.nvidia.com")
        self.base_url = NVIDIA_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(
        self,
        model: str,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> Dict:
        """调用聊天完成API"""
        endpoint = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def generate_image(
        self,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        num_images: int = 1,
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        guidance_scale: float = 7.5
    ) -> Dict:
        """调用图像生成API"""
        endpoint = f"{self.base_url}/images/generations"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_images": num_images,
            "width": width,
            "height": height,
            "steps": steps,
            "guidance_scale": guidance_scale
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def get_embedding(
        self,
        model: str,
        input_text: str
    ) -> Dict:
        """调用嵌入API"""
        endpoint = f"{self.base_url}/embeddings"
        
        payload = {
            "model": model,
            "input": input_text
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}


class ModelCenter:
    """模型中心管理器"""
    
    def __init__(self, api_key: str = None):
        self.client = NVIDIAAPIClient(api_key)
        self._live_models = None
        self._try_fetch_live_models()
    
    def _try_fetch_live_models(self):
        """尝试从API获取实时模型列表"""
        if not self.client.api_key:
            return
        try:
            r = requests.get(f"{self.client.base_url}/models", headers=self.client.headers, timeout=10)
            if r.status_code == 200:
                self._live_models = r.json().get("data", [])
        except:
            pass
    
    def _merge_model(self, model_id: str, api_info: dict = None) -> Dict:
        """合并API数据与富化数据"""
        result = {"id": model_id, "category": _categorize_model(model_id)}
        if api_info:
            result["owned_by"] = api_info.get("owned_by", "")
        e = MODELS_ENRICHED.get(model_id, {})
        result.update(e)
        result.setdefault("owned_by", e.get("provider", "NVIDIA"))
        result.setdefault("type", result["category"])
        return result
    
    def list_models(self, category: str = None) -> List[Dict]:
        """列出所有模型或指定类别模型（从API获取实时列表）"""
        if self._live_models:
            models = [self._merge_model(m["id"], m) for m in self._live_models]
        else:
            models = [self._merge_model(mid) for mid in MODELS_ENRICHED]
        if category:
            models = [m for m in models if m.get("category") == category]
        return models
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """获取模型详细信息（实时API + 富化数据）"""
        if self._live_models:
            api_info = next((m for m in self._live_models if m["id"] == model_id), None)
            result = self._merge_model(model_id, api_info)
            if not api_info and model_id not in MODELS_ENRICHED:
                return None
            return result
        e = MODELS_ENRICHED.get(model_id)
        if not e:
            return None
        return self._merge_model(model_id)
    
    def compare_pricing(self, model_ids: List[str]) -> List[Dict]:
        """比较多个模型的价格"""
        comparisons = []
        for model_id in model_ids:
            info = MODELS_ENRICHED.get(model_id)
            if info:
                comparisons.append({
                    "model_id": model_id,
                    "name": info.get("name"),
                    "provider": info.get("provider"),
                    "input_price": info.get("pricing", {}).get("input", "N/A"),
                    "output_price": info.get("pricing", {}).get("output", "N/A")
                })
        return sorted(comparisons, key=lambda x: x["input_price"])
    
    def recommend_model(
        self,
        use_case: str,
        budget: str = "low",
        need_vision: bool = False
    ) -> List[Dict]:
        """根据用例推荐模型"""
        recommendations = []
        source = MODELS_ENRICHED
        
        for model_id, info in source.items():
            score = 0
            mtype = info.get("type", _categorize_model(model_id))
            
            if use_case in ["chat", "conversation", "qa"] and mtype == "chat":
                score += 10
            elif use_case in ["code", "programming", "coding"]:
                if "code" in str(info.get("strengths", [])).lower():
                    score += 10
            elif use_case in ["image", "generation", "art"]:
                if "generation" in mtype:
                    score += 10
            elif use_case in ["search", "retrieval", "embedding"]:
                if mtype in ("embedding", "rerank"):
                    score += 10
            
            price = info.get("pricing", {}).get("input", 999)
            if budget == "low" and price < 0.5:
                score += 5
            elif budget == "medium" and 0.5 <= price < 1.5:
                score += 5
            elif budget == "high" and price >= 1.5:
                score += 5
            
            if score > 0:
                rec = info.copy()
                rec["model_id"] = model_id
                rec["score"] = score
                recommendations.append(rec)
        
        return sorted(recommendations, key=lambda x: x["score"], reverse=True)[:5]
    
    def chat(
        self,
        model: str,
        message: str,
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ) -> str:
        """简单的聊天接口"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        result = self.client.chat_completion(model, messages, **kwargs)
        
        if "error" in result:
            return f"错误: {result['error']}"
        
        try:
            return result["choices"][0]["message"]["content"]
        except:
            return str(result)
    
    def estimate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict:
        """估算API调用成本"""
        info = self.get_model_info(model)
        if not info:
            return {"error": "未知模型"}
        
        pricing = info.get("pricing", {})
        input_price = pricing.get("input", 0)
        output_price = pricing.get("output", 0)
        
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price
        total_cost = input_cost + output_cost
        
        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": f"${input_cost:.6f}",
            "output_cost": f"${output_cost:.6f}",
            "total_cost": f"${total_cost:.6f}"
        }


def main():  # 注意: 交互式界面仅限 CLI 使用, OpenClaw 上下文中请直接调用 ModelCenter 方法
    """主函数 - 模型中心交互界面"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║            NVIDIA AI 模型中心 v1.0                          ║
    ║            NVIDIA AI Model Center                            ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║  选项:                                                       ║
    ║    1. 浏览所有模型 (Browse All Models)                       ║
    ║    2. 查看模型详情 (Model Details)                           ║
    ║    3. 价格比较 (Compare Pricing)                             ║
    ║    4. 推荐模型 (Recommend Model)                             ║
    ║    5. 成本估算 (Estimate Cost)                               ║
    ║    6. 测试聊天 (Test Chat)                                  ║
    ║    7. 获取API密钥 (Get API Key)                             ║
    ║    0. 退出 (Exit)                                           ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    center = ModelCenter()
    
    while True:
        try:
            choice = input("\n请选择操作 (0-7): ").strip()
            
            if choice == '1':
                print("\n" + "="*60)
                print("可用模型列表")
                print("="*60)
                
                for category, models in center.list_models().items():
                    print(f"\n【{category.upper()}】")
                    for model_id, info in models.items():
                        price = f"${info['pricing']['input']}/{info['pricing']['output']}"
                        print(f"  • {model_id}")
                        print(f"    名称: {info['name']}")
                        print(f"    价格: {price}")
                        print(f"    描述: {info['description']}")
            
            elif choice == '2':
                model_id = input("输入模型ID: ").strip()
                info = center.get_model_info(model_id)
                if info:
                    print(f"\n模型: {info['name']}")
                    print(f"提供商: {info['provider']}")
                    print(f"类型: {info['type']}")
                    print(f"上下文长度: {info['context_length']}")
                    print(f"价格: 输入${info['pricing']['input']}/M, 输出${info['pricing']['output']}/M")
                    print(f"优势: {', '.join(info['strengths'])}")
                    print(f"描述: {info['description']}")
                else:
                    print("未找到模型")
            
            elif choice == '3':
                print("\n可用模型ID:")
                all_models = []
                for category, models in center.list_models().items():
                    for model_id in models.keys():
                        all_models.append(model_id)
                        print(f"  {model_id}")
                
                ids_input = input("\n输入模型ID列表 (逗号分隔): ")
                model_ids = [x.strip() for x in ids_input.split(",")]
                comparisons = center.compare_pricing(model_ids)
                
                print("\n价格比较:")
                print("-"*60)
                for c in comparisons:
                    print(f"{c['name']}")
                    print(f"  输入: ${c['input_price']}/M, 输出: ${c['output_price']}/M")
            
            elif choice == '4':
                print("\n用例选项: chat, code, image, search")
                use_case = input("输入用例: ").strip()
                budget = input("预算 (low/medium/high): ").strip()
                recommendations = center.recommend_model(use_case, budget)
                
                print("\n推荐模型:")
                print("-"*60)
                for i, r in enumerate(recommendations, 1):
                    print(f"{i}. {r['name']}")
                    print(f"   模型ID: {r['model_id']}")
                    print(f"   价格: ${r['pricing']['input']}/${r['pricing']['output']}")
                    print(f"   匹配度: {r['score']}")
            
            elif choice == '5':
                model_id = input("模型ID: ").strip()
                try:
                    input_tokens = int(input("输入token数: "))
                    output_tokens = int(input("输出token数: "))
                    cost = center.estimate_cost(model_id, input_tokens, output_tokens)
                    print(f"\n成本估算:")
                    print(f"  输入费用: {cost['input_cost']}")
                    print(f"  输出费用: {cost['output_cost']}")
                    print(f"  总费用: {cost['total_cost']}")
                except Exception as e:
                    print(f"错误: {e}")
            
            elif choice == '6':
                print("\n注意: 需要设置NVIDIA_API_KEY环境变量")
                print("或在此处输入API密钥:")
                api_key = input("API Key (直接回车使用环境变量): ").strip()
                
                if api_key:
                    center = ModelCenter(api_key)
                
                model_id = input("模型ID: ").strip()
                message = input("输入消息: ").strip()
                
                print("\n回复:")
                response = center.chat(model_id, message)
                print(response)
            
            elif choice == '7':
                print("\n" + "="*60)
                print("获取NVIDIA API密钥")
                print("="*60)
                print("""
步骤:
1. 访问 https://build.nvidia.com/
2. 注册NVIDIA开发者账号
3. 选择模型并获取API密钥
4. 设置环境变量: 
   Windows: setx NVIDIA_API_KEY "your-api-key"
   或在Python中直接传入
                
免费额度:
- NVIDIA开发者计划提供免费试用
- 部分模型(如Llama 3.1)完全免费
                """)
            
            elif choice == '0':
                print("\n退出")
                break
            
            else:
                print("无效选项")
        
        except KeyboardInterrupt:
            print("\n\n退出")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()
