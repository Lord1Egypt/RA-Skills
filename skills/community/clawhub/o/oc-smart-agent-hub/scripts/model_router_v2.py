#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多模型提供商路由器 v2.0
支持多厂商、自动故障转移、成本优化

创建日期：2026-03-04
版本：v2.0
"""

import os
import yaml
import time
from typing import Dict, List, Optional
from pathlib import Path

# 配置文件路径
MODELS_CONFIG = Path('config/models.yaml')
AGENTS_CONFIG = Path('config/agents.yaml')


class ModelRouter:
    """模型路由器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.providers = self.config.get('providers', {})
        self.routing = self.config.get('routing', {})
        
    def load_config(self) -> Dict:
        """加载配置"""
        if not MODELS_CONFIG.exists():
            return {}
        
        with open(MODELS_CONFIG, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def get_available_providers(self) -> List[str]:
        """获取可用的提供商"""
        available = []
        for name, config in self.providers.items():
            if config.get('enabled', False):
                available.append(name)
        return available
    
    def get_models_by_provider(self, provider: str) -> List[Dict]:
        """获取指定提供商的所有模型"""
        if provider not in self.providers:
            return []
        return self.providers[provider].get('models', [])
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """获取模型详细信息"""
        for provider, config in self.providers.items():
            for model in config.get('models', []):
                if model['id'] == model_id:
                    return {
                        **model,
                        'provider': provider,
                        'provider_name': config.get('name', provider)
                    }
        return None
    
    def select_model_for_task(self, task_type: str) -> str:
        """根据任务类型选择模型"""
        task_routing = self.routing.get('task_routing', {})
        
        # 1. 查找任务类型路由
        if task_type in task_routing:
            model_id = task_routing[task_type]
            if self.is_model_available(model_id):
                return model_id
        
        # 2. 默认路由
        default = self.routing.get('default_provider', 'bailian')
        models = self.get_models_by_provider(default)
        
        if models:
            return models[0]['id']
        
        # 3.  fallback 到第一个可用提供商
        available = self.get_available_providers()
        if available:
            models = self.get_models_by_provider(available[0])
            if models:
                return models[0]['id']
        
        raise Exception("没有可用的模型")
    
    def is_model_available(self, model_id: str) -> bool:
        """检查模型是否可用"""
        info = self.get_model_info(model_id)
        if not info:
            return False
        
        provider = info['provider']
        provider_config = self.providers.get(provider, {})
        
        # 检查提供商是否启用
        if not provider_config.get('enabled', False):
            return False
        
        # 检查 API Key 是否配置
        api_key_env = provider_config.get('api_key_env')
        if api_key_env and not os.environ.get(api_key_env):
            if not provider_config.get('api_key'):
                return False
        
        return True
    
    def get_cheapest_model(self, task_type: str) -> str:
        """获取最便宜的模型"""
        available_models = []
        
        for provider, config in self.providers.items():
            if not config.get('enabled', False):
                continue
            
            for model in config.get('models', []):
                cost = model.get('cost_input', 0) + model.get('cost_output', 0)
                available_models.append({
                    'id': model['id'],
                    'cost': cost,
                    'provider': provider
                })
        
        if not available_models:
            return self.select_model_for_task(task_type)
        
        # 按成本排序
        available_models.sort(key=lambda x: x['cost'])
        return available_models[0]['id']
    
    def get_fastest_model(self, task_type: str) -> str:
        """获取最快的模型（简化版：使用上下文窗口作为代理）"""
        # 通常上下文小的模型响应更快
        available_models = []
        
        for provider, config in self.providers.items():
            if not config.get('enabled', False):
                continue
            
            for model in config.get('models', []):
                context = model.get('context_window', 0)
                available_models.append({
                    'id': model['id'],
                    'context': context,
                    'provider': provider
                })
        
        if not available_models:
            return self.select_model_for_task(task_type)
        
        # 按上下文窗口排序（小的通常更快）
        available_models.sort(key=lambda x: x['context'])
        return available_models[0]['id']
    
    def get_best_quality_model(self, task_type: str) -> str:
        """获取质量最好的模型（简化版：使用 max 模型）"""
        # 优先返回各厂商的旗舰模型
        priority_models = [
            'bailian/qwen3-max-2026-01-23',
            'openai/gpt-4',
            'anthropic/claude-opus-4',
        ]
        
        for model_id in priority_models:
            if self.is_model_available(model_id):
                return model_id
        
        # fallback 到任务路由
        return self.select_model_for_task(task_type)
    
    def list_all_models(self) -> List[Dict]:
        """列出所有模型"""
        all_models = []
        
        for provider, config in self.providers.items():
            provider_name = config.get('name', provider)
            enabled = config.get('enabled', False)
            
            for model in config.get('models', []):
                all_models.append({
                    'id': model['id'],
                    'name': model.get('name', model['id']),
                    'provider': provider,
                    'provider_name': provider_name,
                    'enabled': enabled,
                    'context_window': model.get('context_window', 0),
                    'cost_input': model.get('cost_input', 0),
                    'cost_output': model.get('cost_output', 0),
                })
        
        return all_models


def main():
    """主函数 - 测试用"""
    print("=" * 70)
    print("🚀 多模型提供商路由器 v2.0")
    print("=" * 70)
    print()
    
    router = ModelRouter()
    
    # 1. 显示可用提供商
    print("📊 可用提供商:")
    available = router.get_available_providers()
    for provider in available:
        print(f"  ✅ {provider}")
    print()
    
    # 2. 显示所有模型
    print("📋 所有模型:")
    print("-" * 70)
    print(f"{'模型 ID':<40} {'提供商':<15} {'上下文':<12}")
    print("-" * 70)
    
    for model in router.list_all_models():
        context = f"{model['context_window']:,}"
        print(f"{model['id']:<40} {model['provider_name']:<15} {context:<12}")
    
    print()
    
    # 3. 测试任务路由
    print("🎯 任务路由测试:")
    task_types = ['coding', 'reasoning', 'long_text', 'agent', 'daily']
    
    for task in task_types:
        model = router.select_model_for_task(task)
        info = router.get_model_info(model)
        if info:
            print(f"  {task:<12} → {info['name']:<30} ({info['provider_name']})")
    
    print()
    print("=" * 70)
    print("✅ 路由器测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
