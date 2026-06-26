#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户自定义模型提供商管理器 v3.0
支持：
- 用户自定义厂商
- 本地模型（Ollama、LM Studio、vLLM 等）
- 自动发现本地模型服务
- 零代码配置

创建日期：2026-03-04
版本：v3.0
"""

import os
import yaml
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

# 配置文件路径
MODELS_CONFIG = Path('config/models.yaml')
LOCAL_MODELS_CACHE = Path('config/local_models_cache.json')


class ProviderManager:
    """模型提供商管理器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.local_cache = self.load_local_cache()
        
    def load_config(self) -> Dict:
        """加载配置"""
        if not MODELS_CONFIG.exists():
            return self.create_default_config()
        
        with open(MODELS_CONFIG, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def load_local_cache(self) -> Dict:
        """加载本地模型缓存"""
        if not LOCAL_MODELS_CACHE.exists():
            return {'models': [], 'last_scan': None}
        
        with open(LOCAL_MODELS_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_default_config(self) -> Dict:
        """创建默认配置"""
        default = {
            'providers': {
                'bailian': {
                    'name': '阿里云百炼',
                    'type': 'openai-compatible',
                    'enabled': True,
                    'base_url': 'https://coding.dashscope.aliyuncs.com/v1',
                    'models': []
                }
            },
            'local_discovery': {
                'enabled': True,
                'endpoints': [
                    {'name': 'Ollama', 'url': 'http://localhost:11434/api/tags', 'type': 'ollama'},
                    {'name': 'LM Studio', 'url': 'http://localhost:1234/v1/models', 'type': 'openai-compatible'},
                ]
            }
        }
        
        # 保存默认配置
        MODELS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        with open(MODELS_CONFIG, 'w', encoding='utf-8') as f:
            yaml.dump(default, f, allow_unicode=True)
        
        return default
    
    def list_providers(self) -> List[Dict]:
        """列出所有提供商"""
        providers = []
        
        for name, config in self.config.get('providers', {}).items():
            if config.get('enabled', False):
                is_local = 'localhost' in config.get('base_url', '') or '127.0.0.1' in config.get('base_url', '')
                providers.append({
                    'id': name,
                    'name': config.get('name', name),
                    'type': config.get('type', 'unknown'),
                    'base_url': config.get('base_url', ''),
                    'is_local': is_local,
                    'model_count': len(config.get('models', []))
                })
        
        # 添加自动发现的本地模型
        for model in self.local_cache.get('models', []):
            providers.append({
                'id': f"local_{model['id']}",
                'name': f"{model['name']} (本地)",
                'type': 'local',
                'is_local': True,
                'model_count': 1
            })
        
        return providers
    
    def list_models(self, provider_id: Optional[str] = None) -> List[Dict]:
        """列出所有模型"""
        models = []
        
        # 从配置加载
        if provider_id:
            providers = {provider_id: self.config['providers'].get(provider_id, {})}
        else:
            providers = self.config.get('providers', {})
        
        for name, config in providers.items():
            if not config.get('enabled', False):
                continue
            
            for model in config.get('models', []):
                models.append({
                    'id': model['id'],
                    'name': model.get('name', model['id']),
                    'provider': name,
                    'provider_name': config.get('name', name),
                    'context_window': model.get('context_window', 0),
                    'capabilities': model.get('capabilities', []),
                    'is_local': 'local' in model
                })
        
        # 添加自动发现的本地模型
        for model in self.local_cache.get('models', []):
            if not provider_id or provider_id.startswith('local'):
                models.append({
                    'id': f"local_{model['id']}",
                    'name': f"{model['name']} (本地)",
                    'provider': 'local',
                    'provider_name': '本地模型',
                    'context_window': model.get('context_window', 0),
                    'capabilities': ['text'],
                    'is_local': True
                })
        
        return models
    
    def scan_local_models(self) -> List[Dict]:
        """扫描本地模型服务"""
        discovered = []
        discovery_config = self.config.get('local_discovery', {})
        
        if not discovery_config.get('enabled', True):
            return discovered
        
        endpoints = discovery_config.get('endpoints', [])
        
        for endpoint in endpoints:
            try:
                url = endpoint['url']
                name = endpoint['name']
                etype = endpoint['type']
                
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if etype == 'ollama':
                        # Ollama API
                        for model in data.get('models', []):
                            discovered.append({
                                'id': model['name'],
                                'name': model['name'],
                                'provider': name,
                                'context_window': 8192,
                                'source': url
                            })
                    
                    elif etype == 'openai-compatible':
                        # OpenAI 兼容 API
                        for model in data.get('data', []):
                            discovered.append({
                                'id': model['id'],
                                'name': model['id'],
                                'provider': name,
                                'context_window': 4096,
                                'source': url
                            })
                
            except Exception as e:
                pass  # 静默失败，服务可能未运行
        
        # 更新缓存
        if discovered:
            self.local_cache = {
                'models': discovered,
                'last_scan': datetime.now().isoformat()
            }
            with open(LOCAL_MODELS_CACHE, 'w', encoding='utf-8') as f:
                json.dump(self.local_cache, f, indent=2, ensure_ascii=False)
        
        return discovered
    
    def add_provider(self, name: str, config: Dict) -> bool:
        """添加新厂商"""
        if 'providers' not in self.config:
            self.config['providers'] = {}
        
        self.config['providers'][name] = config
        
        with open(MODELS_CONFIG, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
        
        return True
    
    def remove_provider(self, name: str) -> bool:
        """删除厂商"""
        if name not in self.config.get('providers', {}):
            return False
        
        del self.config['providers'][name]
        
        with open(MODELS_CONFIG, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
        
        return True
    
    def enable_provider(self, name: str, enabled: bool) -> bool:
        """启用/禁用厂商"""
        if name not in self.config.get('providers', {}):
            return False
        
        self.config['providers'][name]['enabled'] = enabled
        
        with open(MODELS_CONFIG, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)
        
        return True


def main():
    """主函数 - 测试用"""
    print("=" * 70)
    print("🚀 用户自定义模型提供商管理器 v3.0")
    print("=" * 70)
    print()
    
    manager = ProviderManager()
    
    # 1. 扫描本地模型
    print("🔍 扫描本地模型服务...")
    local_models = manager.scan_local_models()
    if local_models:
        print(f"✅ 发现 {len(local_models)} 个本地模型:")
        for model in local_models:
            print(f"   - {model['name']} ({model['provider']})")
    else:
        print("⚠️  未发现本地模型服务")
    print()
    
    # 2. 列出所有提供商
    print("📊 已配置的提供商:")
    providers = manager.list_providers()
    for p in providers:
        local_tag = " (本地)" if p['is_local'] else ""
        print(f"  ✅ {p['name']}{local_tag} - {p['model_count']} 个模型")
    print()
    
    # 3. 列出所有模型
    print("📋 所有可用模型:")
    print("-" * 70)
    print(f"{'模型 ID':<40} {'提供商':<20} {'上下文':<12}")
    print("-" * 70)
    
    models = manager.list_models()
    for model in models:
        context = f"{model['context_window']:,}"
        provider = f"{model['provider_name']}"
        if model.get('is_local'):
            provider += " (本地)"
        print(f"{model['id']:<40} {provider:<20} {context:<12}")
    
    print()
    print("=" * 70)
    print("✅ 管理器测试完成")
    print("=" * 70)
    print()
    print("💡 提示:")
    print("  - 编辑 config/models.yaml 添加自定义厂商")
    print("  - 本地模型会自动发现（Ollama、LM Studio、vLLM 等）")
    print("  - 运行 'python scripts/provider_manager.py scan' 扫描本地模型")


if __name__ == "__main__":
    main()
