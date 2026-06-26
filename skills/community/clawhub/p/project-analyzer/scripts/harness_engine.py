"""
Harness Engine - 核心引擎
基于 Harness Engineering 模式，控制文档生成的整个流程
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional


class HarnessEngine:
    """
    Harness Engineering 核心引擎
    
    包含四大组件：
    1. 缰绳 (Constraints) - 架构约束
    2. 马车 (Context) - 上下文工程
    3. 镜子 (Feedback) - 反馈循环
    4. 车夫 (Entropy) - 熵管理
    """
    
    def __init__(self, project_path: str, config_path: Optional[str] = None):
        self.project_path = Path(project_path)
        self.config = self._load_config(config_path)
        self.context = {}
        self.constraints = self.config.get('constraints', {})
        self.quality_rules = self.config.get('quality_rules', {})
        
    def _load_config(self, config_path: Optional[str]) -> dict:
        """加载配置文件"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # 默认配置
        return {
            'constraints': {
                'output_format': 'markdown',
                'encoding': 'utf-8',
                'language': 'zh-CN',
                'forbidden_patterns': ['TODO', '待补充', '...'],
            },
            'quality_rules': {
                'min_length': 1000,
                'required_sections': {
                    'srs': ['引言', '功能需求', '非功能需求'],
                    'sad': ['架构概述', '技术选型', '模块设计'],
                    'sdd': ['模块详细设计', '接口设计', '数据结构'],
                    'dbd': ['数据库概述', '表结构', '索引设计'],
                    'apid': ['接口列表', '错误码'],
                    'tsd': ['测试策略', '测试用例'],
                }
            }
        }
    
    def initialize(self) -> None:
        """初始化 Harness 环境"""
        print("🎯 初始化 Harness Engine...")
        
        # 1. 加载约束（缰绳）
        self._load_constraints()
        print("   ✅ 缰绳 (Constraints) 已加载")
        
        # 2. 构建上下文（马车）
        self._build_context()
        print("   ✅ 马车 (Context) 已构建")
        
        # 3. 准备反馈循环（镜子）
        self._setup_feedback()
        print("   ✅ 镜子 (Feedback) 已准备")
        
        # 4. 初始化熵管理（车夫）
        self._init_entropy_manager()
        print("   ✅ 车夫 (Entropy) 已初始化")
        
    def _load_constraints(self) -> None:
        """加载约束"""
        # 约束已在初始化时加载
        pass
    
    def _build_context(self) -> None:
        """构建上下文"""
        self.context = {
            'project': {},
            'tech_stack': {},
            'database': {},
            'api': {},
        }
    
    def _setup_feedback(self) -> None:
        """准备反馈循环"""
        self.feedback_enabled = True
    
    def _init_entropy_manager(self) -> None:
        """初始化熵管理"""
        self.entropy_config = {
            'remove_extra_newlines': True,
            'remove_trailing_spaces': True,
            'normalize_whitespace': True,
        }
    
    def validate_constraints(self, content: str) -> tuple:
        """
        验证约束
        
        Returns:
            tuple: (是否通过, 内容)
        """
        passed = True
        fixed_content = content
        
        # 检查禁止模式
        for pattern in self.constraints.get('forbidden_patterns', []):
            if pattern in content:
                passed = False
                fixed_content = fixed_content.replace(pattern, f'【{pattern}】')
        
        # 检查最小长度
        min_length = self.quality_rules.get('min_length', 1000)
        if len(content) < min_length:
            passed = False
            print(f"   ⚠️ 内容长度不足: {len(content)} < {min_length}")
        
        return passed, fixed_content
    
    def feedback(self, content: str, doc_type: str) -> dict:
        """
        反馈循环
        
        检查文档质量并提供反馈
        """
        issues = []
        
        # 检查必需章节
        required_sections = self.quality_rules.get('required_sections', {}).get(doc_type, [])
        for section in required_sections:
            if section not in content:
                issues.append({
                    'type': 'missing_section',
                    'section': section,
                    'severity': 'error'
                })
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def clean(self, content: str) -> str:
        """
        熵管理 - 清理内容
        """
        # 移除多余空行
        if self.entropy_config.get('remove_extra_newlines'):
            while '\n\n\n' in content:
                content = content.replace('\n\n\n', '\n\n')
        
        # 移除行尾空白
        if self.entropy_config.get('remove_trailing_spaces'):
            lines = content.split('\n')
            lines = [line.rstrip() for line in lines]
            content = '\n'.join(lines)
        
        return content
    
    def get_context(self) -> dict:
        """获取上下文"""
        return self.context
    
    def set_context(self, key: str, value: any) -> None:
        """设置上下文"""
        self.context[key] = value


# 导出主要类
__all__ = ['HarnessEngine']
