#!/usr/bin/env python3
"""
思源笔记读写模块
提供与思源笔记（SiYuan Note）进行交互的接口
"""

import json
import requests
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class SiYuanConfig:
    """思源笔记配置"""
    api_url: str = "http://localhost:6806"
    token: str = ""
    
@dataclass
class SyncConfig:
    """同步配置"""
    notebook_name: str = "其他"
    document_name: str = "openchat"
    auto_sync: bool = True
    sync_interval_minutes: int = 5
    include_timestamps: bool = True
    format_markdown: bool = True
    
@dataclass
class ConversationData:
    """对话数据结构"""
    summary: str
    messages: List[Dict[str, str]]
    conclusion: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {
                'source': 'OpenClaw',
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0'
            }

class SiYuanNote:
    """思源笔记读写主类"""
    
    def __init__(self, api_url: str = None, token: str = None, config_path: str = None):
        """
        初始化思源笔记连接
        
        Args:
            api_url: 思源笔记API地址，如 http://localhost:6806
            token: 思源笔记API token
            config_path: 配置文件路径
        """
        # 从环境变量读取默认配置
        env_api_url = os.environ.get('SIYUAN_API_URL')
        env_token = os.environ.get('SIYUAN_API_TOKEN')
        
        self.config_path = config_path or os.path.expanduser("~/.openclaw/workspace/siyuan-openchat-sync/config.json")
        self.siyuan_config = SiYuanConfig()
        self.sync_config = SyncConfig()
        
        # 从环境变量覆盖默认值
        if env_api_url:
            self.siyuan_config.api_url = env_api_url
        if env_token:
            self.siyuan_config.token = env_token
        
        # 加载配置
        self.load_config()
        
        # 覆盖配置（如果提供了参数）
        if api_url:
            self.siyuan_config.api_url = api_url
        if token:
            self.siyuan_config.token = token
        
        # 初始化API连接
        self.headers = {
            'Authorization': f'Token {self.siyuan_config.token}',
            'Content-Type': 'application/json'
        }
        
        # 缓存
        self.notebook_cache = {}
        self.document_cache = {}
        
        # 状态跟踪
        self.last_operation_time = None
        self.operation_count = 0
        self.error_count = 0
    
    def load_config(self):
        """加载配置文件"""
        config_path = Path(self.config_path)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 更新配置
                if 'siyuan' in config_data:
                    siyuan_data = config_data['siyuan']
                    self.siyuan_config.api_url = siyuan_data.get('api_url', self.siyuan_config.api_url)
                    self.siyuan_config.token = siyuan_data.get('token', self.siyuan_config.token)
                
                if 'sync' in config_data:
                    sync_data = config_data['sync']
                    self.sync_config.notebook_name = sync_data.get('notebook_name', self.sync_config.notebook_name)
                    self.sync_config.document_name = sync_data.get('document_name', self.sync_config.document_name)
                    self.sync_config.auto_sync = sync_data.get('auto_sync', self.sync_config.auto_sync)
                    self.sync_config.sync_interval_minutes = sync_data.get('sync_interval_minutes', self.sync_config.sync_interval_minutes)
                    self.sync_config.include_timestamps = sync_data.get('include_timestamps', self.sync_config.include_timestamps)
                    self.sync_config.format_markdown = sync_data.get('format_markdown', self.sync_config.format_markdown)
                    
                print(f"✅ 配置已从 {self.config_path} 加载")
                
            except Exception as e:
                print(f"❌ 加载配置失败: {e}")
                print("使用默认配置")
        else:
            print("⚠️  配置文件不存在，使用默认配置")
            self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        config_data = {
            'siyuan': asdict(self.siyuan_config),
            'sync': asdict(self.sync_config)
        }
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已保存到 {self.config_path}")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
    
    def update_config(self, new_config: Dict[str, Any]):
        """更新配置"""
        try:
            if 'siyuan' in new_config:
                for key, value in new_config['siyuan'].items():
                    if hasattr(self.siyuan_config, key):
                        setattr(self.siyuan_config, key, value)
            
            if 'sync' in new_config:
                for key, value in new_config['sync'].items():
                    if hasattr(self.sync_config, key):
                        setattr(self.sync_config, key, value)
            
            self.save_config()
            return True
        except Exception as e:
            print(f"❌ 更新配置失败: {e}")
            return False
    
    def test_connection(self) -> bool:
        """测试思源笔记连接"""
        try:
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/notebook/lsNotebooks',
                headers=self.headers,
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    notebooks = result.get('data', {}).get('notebooks', [])
                    print(f"✅ 连接成功！找到 {len(notebooks)} 个笔记本")
                    return True
                else:
                    print(f"❌ 连接失败: {result.get('msg')}")
                    return False
            else:
                print(f"❌ 连接失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def get_notebooks(self) -> List[Dict]:
        """获取所有笔记本"""
        try:
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/notebook/lsNotebooks',
                headers=self.headers,
                json={},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    notebooks = result.get('data', {}).get('notebooks', [])
                    
                    # 更新缓存
                    for notebook in notebooks:
                        self.notebook_cache[notebook['name']] = notebook['id']
                    
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    return notebooks
            
            return []
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 获取笔记本失败: {e}")
            return []
    
    def get_notebook_id(self, notebook_name: str) -> Optional[str]:
        """获取笔记本ID"""
        # 检查缓存
        if notebook_name in self.notebook_cache:
            return self.notebook_cache[notebook_name]
        
        # 获取所有笔记本
        notebooks = self.get_notebooks()
        for notebook in notebooks:
            if notebook['name'] == notebook_name:
                self.notebook_cache[notebook_name] = notebook['id']
                return notebook['id']
        
        print(f"❌ 未找到笔记本: {notebook_name}")
        return None
    
    def get_documents(self, notebook_id: str) -> List[Dict]:
        """获取笔记本中的文档"""
        try:
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/filetree/listDocsByPath',
                headers=self.headers,
                json={
                    'notebook': notebook_id,
                    'path': '/'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    files = result.get('data', {}).get('files', [])
                    
                    # 更新缓存
                    for file in files:
                        file_name = file.get('name', '').replace('.sy', '')
                        self.document_cache[file_name] = file.get('id')
                    
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    return files
            
            return []
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 获取文档失败: {e}")
            return []
    
    def get_document_content(self, document_id: str) -> Optional[str]:
        """获取文档内容"""
        try:
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/block/getBlockKramdown',
                headers=self.headers,
                json={
                    'id': document_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    content = result.get('data', {}).get('kramdown', '')
                    
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    return content
            
            return None
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 获取文档内容失败: {e}")
            return None
    
    def search_content(self, query: str, notebook_name: str = None) -> List[Dict]:
        """搜索内容"""
        try:
            # 构建搜索请求
            search_params = {
                'k': query,
                'method': 0  # 0: 关键字搜索
            }
            
            if notebook_name:
                notebook_id = self.get_notebook_id(notebook_name)
                if notebook_id:
                    search_params['notebook'] = notebook_id
            
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/search/fullTextSearchBlock',
                headers=self.headers,
                json=search_params,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    blocks = result.get('data', {}).get('blocks', [])
                    
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    return blocks
            
            return []
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 搜索内容失败: {e}")
            return []
    
    def create_document(self, notebook_name: str, document_name: str, content: str = "") -> Optional[str]:
        """创建新文档 - 使用更好的方法"""
        try:
            # 获取笔记本ID
            notebook_id = self.get_notebook_id(notebook_name)
            if not notebook_id:
                print(f"❌ 未找到笔记本: {notebook_name}")
                return None
            
            # 构建完整内容
            full_content = f"# {document_name}\n\n{content}"
            
            # 使用createDocWithMd API创建真正的独立文档
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/filetree/createDocWithMd',
                headers=self.headers,
                json={
                    'notebook': notebook_id,
                    'path': f'/{document_name}',
                    'markdown': full_content,
                    'withMath': False,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    document_id = result.get('data')
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    print(f"✅ 文档创建成功: {document_name}")
                    print(f"📄 文档ID: {document_id}")
                    return document_id
                else:
                    print(f"❌ API错误: {result.get('msg')}")
                    # 如果createDocWithMd失败，回退到旧方法
                    return self._create_document_fallback(notebook_id, document_name, content)
            
            print(f"❌ HTTP错误: {response.status_code}")
            return self._create_document_fallback(notebook_id, document_name, content)
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 创建文档失败: {e}")
            print("💡 尝试回退到旧方法...")
            notebook_id = self.get_notebook_id(notebook_name)
            if notebook_id:
                return self._create_document_fallback(notebook_id, document_name, content)
            return None
    
    def _create_document_fallback(self, notebook_id: str, document_name: str, content: str) -> Optional[str]:
        """回退方法：在现有文档中创建内容块"""
        try:
            # 获取笔记本中的第一个文档作为父文档
            documents = self.get_documents(notebook_id)
            if not documents:
                print(f"❌ 笔记本中没有文档: 无法使用回退方法")
                return None
            
            parent_doc_id = documents[0].get('id')
            
            # 构建完整内容
            full_content = f"# {document_name}\n\n{content}"
            
            # 追加内容（创建新块）
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/block/appendBlock',
                headers=self.headers,
                json={
                    'data': full_content,
                    'dataType': 'markdown',
                    'parentID': parent_doc_id,
                    'nextID': '',
                    'previousID': ''
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    print(f"✅ 内容已添加到现有文档: {documents[0].get('name')}")
                    return parent_doc_id
            
            return None
            
        except Exception as e:
            print(f"❌ 回退方法也失败: {e}")
            return None
    
    def append_to_document(self, document_id: str, content: str) -> bool:
        """向文档追加内容"""
        try:
            response = requests.post(
                f'{self.siyuan_config.api_url}/api/block/appendBlock',
                headers=self.headers,
                json={
                    'data': content,
                    'dataType': 'markdown',
                    'parentID': document_id,
                    'nextID': '',
                    'previousID': ''
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    self.last_operation_time = datetime.now()
                    self.operation_count += 1
                    
                    return True
            
            return False
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ 追加内容失败: {e}")
            return False
    
    def format_conversation(self, conversation_data: Dict) -> str:
        """格式化对话内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 基础格式
        if self.sync_config.format_markdown:
            formatted = f"""
## 🗣️ OpenClaw对话记录

### 📋 摘要
- **时间**: {timestamp}
- **主题**: {conversation_data.get('summary', '未指定主题')}
- **消息数**: {len(conversation_data.get('messages', []))}
- **同步时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 💬 对话内容
"""
        else:
            formatted = f"\nOpenClaw对话记录\n时间: {timestamp}\n主题: {conversation_data.get('summary', '未指定主题')}\n消息数: {len(conversation_data.get('messages', []))}\n\n对话内容:\n"
        
        # 添加消息
        messages = conversation_data.get('messages', [])
        for i, message in enumerate(messages):
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            
            if self.sync_config.format_markdown:
                if role == 'user':
                    formatted += f"\n#### 👤 用户 (消息 {i+1})\n\n{content}\n\n---\n"
                else:
                    formatted += f"\n#### 🤖 助手 (消息 {i+1})\n\n{content}\n\n---\n"
            else:
                formatted += f"\n[{role.upper()}] {content}\n"
        
        # 添加总结
        conclusion = conversation_data.get('conclusion', '对话已完成。')
        if self.sync_config.format_markdown:
            formatted += f"""
### 📝 总结
{conclusion}

---
"""
        else:
            formatted += f"\n总结: {conclusion}\n\n---\n"
        
        return formatted
    
    def sync_conversation(self, conversation_data: Dict, notebook_name: str = None, document_name: str = None) -> bool:
        """
        同步对话到思源笔记
        
        Args:
            conversation_data: 对话数据
            notebook_name: 目标笔记本名称（默认使用配置）
            document_name: 目标文档名称（默认使用配置）
        """
        try:
            # 使用配置或参数
            target_notebook = notebook_name or self.sync_config.notebook_name
            target_document = document_name or self.sync_config.document_name
            
            print(f"开始同步对话到思源笔记: {target_notebook}/{target_document}")
            
            # 1. 获取笔记本ID
            notebook_id = self.get_notebook_id(target_notebook)
            if not notebook_id:
                print(f"❌ 无法找到笔记本: {target_notebook}")
                return False
            
            # 2. 查找文档
            documents = self.get_documents(notebook_id)
            document_id = None
            
            for doc in documents:
                doc_name = doc.get('name', '').replace('.sy', '')
                if target_document.lower() in doc_name.lower():
                    document_id = doc.get('id')
                    break
            
            # 3. 如果文档不存在，创建新文档
            if not document_id:
                print(f"文档不存在，创建新文档: {target_document}")
                
                initial_content = f"""# {target_document} - OpenClaw对话记录

## 简介
此文档用于记录OpenClaw对话内容。

---
"""
                document_id = self.create_document(target_notebook, target_document, initial_content)
                
                if not document_id:
                    print("❌ 创建文档失败")
                    return False
                
                print(f"✅ 文档创建成功: {document_id}")
            else:
                print(f"✅ 找到现有文档: {document_id}")
            
            # 4. 格式化对话内容
            formatted_content = self.format_conversation(conversation_data)
            
            # 5. 追加到文档
            success = self.append_to_document(document_id, formatted_content)
            
            if success:
                self.last_operation_time = datetime.now()
                self.operation_count += 1
                
                print(f"✅ 对话同步成功！")
                return True
            else:
                self.error_count += 1
                print(f"❌ 对话同步失败")
                return False
                
        except Exception as e:
            self.error_count += 1
            print(f"❌ 同步时出错: {e}")
            return False