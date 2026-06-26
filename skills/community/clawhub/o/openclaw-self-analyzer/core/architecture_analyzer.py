#!/usr/bin/env python3
"""
OpenClaw 架构分析器
深度分析OpenClaw代码结构和钩子点
"""
import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class HookPoint:
    """钩子点定义"""
    stage: str
    type: str  # pre, post, replace
    file_path: str
    line_number: int
    function_name: str
    signature: str
    description: str = ""
    
@dataclass
class PipelineStage:
    """流水线阶段"""
    name: str
    file_path: str
    line_number: int
    hooks: Dict[str, HookPoint]
    dependencies: List[str]
    description: str = ""

@dataclass
class ArchitectureMap:
    """架构映射"""
    version: str
    analyzed_at: str
    pipeline_stages: List[PipelineStage]
    hook_points: List[HookPoint]
    extensions: List[str]
    channel_integrations: List[str]
    tool_implementations: List[str]

class OpenClawArchitectureAnalyzer:
    """OpenClaw架构分析器"""
    
    def __init__(self, openclaw_path='/root/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw'):
        self.openclaw_path = Path(openclaw_path)
        self.workspace_path = Path('/root/.openclaw/workspace')
        
    def analyze_full_architecture(self) -> ArchitectureMap:
        """分析完整架构"""
        print("🔍 开始分析OpenClaw架构...")
        
        # 分析流水线阶段
        stages = self._analyze_pipeline_stages()
        print(f"✅ 发现 {len(stages)} 个流水线阶段")
        
        # 分析钩子点
        hooks = self._extract_hook_points(stages)
        print(f"✅ 发现 {len(hooks)} 个钩子点")
        
        # 分析扩展
        extensions = self._analyze_extensions()
        print(f"✅ 发现 {len(extensions)} 个扩展")
        
        # 分析通道集成
        channels = self._analyze_channels()
        print(f"✅ 发现 {len(channels)} 个通道")
        
        # 分析工具实现
        tools = self._analyze_tools()
        print(f"✅ 发现 {len(tools)} 个工具")
        
        return ArchitectureMap(
            version=self._detect_version(),
            analyzed_at=str(datetime.now()),
            pipeline_stages=stages,
            hook_points=hooks,
            extensions=extensions,
            channel_integrations=channels,
            tool_implementations=tools
        )
    
    def _detect_version(self) -> str:
        """检测OpenClaw版本"""
        package_json = self.openclaw_path / 'package.json'
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
                return data.get('version', 'unknown')
        return 'unknown'
    
    def _analyze_pipeline_stages(self) -> List[PipelineStage]:
        """分析流水线阶段"""
        stages = []
        
        # 扫描核心文件
        core_files = [
            'gateway/index.js',
            'core/pipeline.js',
            'agents/manager.js',
            'agents/context.js'
        ]
        
        for file_path in core_files:
            full_path = self.openclaw_path / file_path
            if full_path.exists():
                stages.extend(self._extract_stages_from_file(full_path, file_path))
        
        # 从已知配置推断阶段
        default_stages = [
            'input_receive',
            'context_gather', 
            'memory_retrieve',
            'prompt_assemble',
            'token_check',
            'context_compress',
            'llm_submit',
            'response_process',
            'memory_store'
        ]
        
        for stage in default_stages:
            if not any(s.name == stage for s in stages):
                stages.append(PipelineStage(
                    name=stage,
                    file_path='inferred',
                    line_number=0,
                    hooks={},
                    dependencies=[],
                    description=f'Inferred stage: {stage}'
                ))
        
        return stages
    
    def _extract_stages_from_file(self, file_path: Path, relative_path: str) -> List[PipelineStage]:
        """从文件提取阶段"""
        stages = []
        
        try:
            content = file_path.read_text()
            
            # 查找异步函数定义
            pattern = r'async\s+(\w+)\s*\([^)]*\)\s*\{'
            matches = re.finditer(pattern, content)
            
            for match in matches:
                func_name = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                
                # 检查是否是流水线相关的函数
                if any(keyword in func_name.lower() for keyword in 
                      ['process', 'handle', 'execute', 'run', 'submit', 'receive']):
                    stages.append(PipelineStage(
                        name=func_name,
                        file_path=relative_path,
                        line_number=line_num,
                        hooks={},
                        dependencies=[],
                        description=f'Detected stage: {func_name}'
                    ))
        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")
        
        return stages
    
    def _extract_hook_points(self, stages: List[PipelineStage]) -> List[HookPoint]:
        """提取钩子点"""
        hooks = []
        
        for stage in stages:
            # 为每个阶段生成可能的钩子
            for hook_type in ['pre', 'post', 'replace']:
                hook = HookPoint(
                    stage=stage.name,
                    type=hook_type,
                    file_path=stage.file_path,
                    line_number=stage.line_number,
                    function_name=f"{hook_type}_{stage.name}",
                    signature=f"async {hook_type}_{stage.name}(context, next) => {{...}}",
                    description=f"Hook point: {hook_type} {stage.name}"
                )
                hooks.append(hook)
                stage.hooks[hook_type] = hook
        
        return hooks
    
    def _analyze_extensions(self) -> List[str]:
        """分析扩展"""
        extensions_dir = self.openclaw_path / 'extensions'
        extensions = []
        
        if extensions_dir.exists():
            for ext_dir in extensions_dir.iterdir():
                if ext_dir.is_dir():
                    extensions.append(ext_dir.name)
        
        return extensions
    
    def _analyze_channels(self) -> List[str]:
        """分析通道集成"""
        channels = []
        
        # 扫描文档目录
        docs_channels = self.openclaw_path / 'docs' / 'channels'
        if docs_channels.exists():
            for channel_file in docs_channels.glob('*.md'):
                channels.append(channel_file.stem)
        
        return channels
    
    def _analyze_tools(self) -> List[str]:
        """分析工具实现"""
        tools = []
        
        # 扫描文档
        docs_tools = self.openclaw_path / 'docs' / 'tools'
        if docs_tools.exists():
            for tool_file in docs_tools.glob('*.md'):
                tools.append(tool_file.stem)
        
        return tools
    
    def generate_hook_map(self) -> Dict[str, Any]:
        """生成钩子映射"""
        architecture = self.analyze_full_architecture()
        
        hook_map = {
            'version': architecture.version,
            'generated_at': architecture.analyzed_at,
            'pipeline': {},
            'hooks': {}
        }
        
        # 构建流水线映射
        for stage in architecture.pipeline_stages:
            hook_map['pipeline'][stage.name] = {
                'file': stage.file_path,
                'line': stage.line_number,
                'description': stage.description,
                'hooks': {
                    hook_type: {
                        'function': hook.function_name,
                        'signature': hook.signature,
                        'description': hook.description
                    }
                    for hook_type, hook in stage.hooks.items()
                }
            }
        
        # 构建钩子列表
        for hook in architecture.hook_points:
            key = f"{hook.type}.{hook.stage}"
            hook_map['hooks'][key] = {
                'stage': hook.stage,
                'type': hook.type,
                'function': hook.function_name,
                'signature': hook.signature,
                'file': hook.file_path,
                'line': hook.line_number
            }
        
        return hook_map

if __name__ == '__main__':
    analyzer = OpenClawArchitectureAnalyzer()
    
    print("=== OpenClaw 架构分析 ===\n")
    
    # 完整分析
    architecture = analyzer.analyze_full_architecture()
    print(f"\n版本: {architecture.version}")
    print(f"分析时间: {architecture.analyzed_at}")
    print(f"流水线阶段: {len(architecture.pipeline_stages)}")
    print(f"钩子点: {len(architecture.hook_points)}")
    print(f"扩展: {len(architecture.extensions)}")
    print(f"通道: {len(architecture.channel_integrations)}")
    
    # 生成钩子映射
    hook_map = analyzer.generate_hook_map()
    
    # 保存结果
    output_file = Path('/root/.openclaw/workspace/openclaw_architecture.json')
    with open(output_file, 'w') as f:
        json.dump(hook_map, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 架构分析完成")
    print(f"📄 结果已保存到: {output_file}")
