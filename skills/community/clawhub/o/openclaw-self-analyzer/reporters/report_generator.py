#!/usr/bin/env python3
"""
OpenClaw 报告生成器
生成详细的架构分析报告
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, architecture_file='/root/.openclaw/workspace/openclaw_architecture.json'):
        self.architecture_file = Path(architecture_file)
        self.load_architecture()
        
    def load_architecture(self):
        """加载架构分析结果"""
        if self.architecture_file.exists():
            with open(self.architecture_file) as f:
                self.architecture = json.load(f)
        else:
            self.architecture = {}
    
    def generate_markdown_report(self) -> str:
        """生成Markdown报告"""
        report = []
        
        # 标题
        report.append("# OpenClaw 架构分析报告\n")
        report.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**版本:** {self.architecture.get('version', 'unknown')}\n")
        
        # 概览
        report.append("## 📊 概览\n")
        
        if 'pipeline' in self.architecture:
            report.append(f"- **流水线阶段:** {len(self.architecture['pipeline'])}")
        
        if 'hooks' in self.architecture:
            report.append(f"- **钩子点:** {len(self.architecture['hooks'])}")
        
        report.append("")
        
        # 流水线详情
        if 'pipeline' in self.architecture:
            report.append("## 🔄 流水线阶段\n")
            
            for stage_name, stage_info in self.architecture['pipeline'].items():
                report.append(f"### {stage_name}\n")
                report.append(f"- **文件:** {stage_info.get('file', 'unknown')}")
                report.append(f"- **行号:** {stage_info.get('line', 'unknown')}")
                
                if 'description' in stage_info:
                    report.append(f"- **描述:** {stage_info['description']}")
                
                if 'hooks' in stage_info and stage_info['hooks']:
                    report.append("\n**可用钩子:**")
                    for hook_type, hook_info in stage_info['hooks'].items():
                        report.append(f"- `{hook_type}`: {hook_info.get('function', 'unknown')}")
                
                report.append("")
        
        # 钩子详情
        if 'hooks' in self.architecture:
            report.append("## 🎣 钩子点详情\n")
            report.append("| 钩子 | 阶段 | 函数 | 签名 |")
            report.append("|------|------|------|------|")
            
            for hook_key, hook_info in self.architecture['hooks'].items():
                report.append(f"| `{hook_key}` | {hook_info.get('stage', 'unknown')} | {hook_info.get('function', 'unknown')} | `{hook_info.get('signature', 'unknown')}` |")
            
            report.append("")
        
        # 扩展信息
        if 'extensions' in self.architecture:
            report.append("## 🔌 扩展\n")
            for ext in self.architecture['extensions']:
                report.append(f"- `{ext}`")
            report.append("")
        
        # 使用建议
        report.append("## 💡 使用建议\n")
        report.append("### 创建自定义钩子\n")
        report.append("```python")
        report.append("from openclaw_self_analyzer.generators.hook_generator import HookGenerator")
        report.append("")
        report.append("generator = HookGenerator()")
        report.append("hook = generator.generate_hook_package(")
        report.append("    hook_name='my_custom_hook',")
        report.append("    hook_type='pre',")
        report.append("    stage='context_gather',")
        report.append("    logic='console.log(\"Custom logic\");'")
        report.append(")")
        report.append("```")
        report.append("")
        
        return "\n".join(report)
    
    def generate_json_report(self) -> Dict[str, Any]:
        """生成JSON报告"""
        return {
            'metadata': {
                'generated_at': str(datetime.now()),
                'version': self.architecture.get('version', 'unknown'),
                'analyzer_version': '1.0.0'
            },
            'summary': {
                'total_stages': len(self.architecture.get('pipeline', {})),
                'total_hooks': len(self.architecture.get('hooks', {})),
                'extensions': len(self.architecture.get('extensions', [])),
                'channels': len(self.architecture.get('channels', []))
            },
            'architecture': self.architecture
        }
    
    def save_reports(self, output_dir: Path):
        """保存报告"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown报告
        md_report = self.generate_markdown_report()
        md_file = output_dir / 'architecture_report.md'
        md_file.write_text(md_report, encoding='utf-8')
        
        # 生成JSON报告
        json_report = self.generate_json_report()
        json_file = output_dir / 'architecture_report.json'
        with open(json_file, 'w') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)
        
        return {
            'markdown': str(md_file),
            'json': str(json_file)
        }

if __name__ == '__main__':
    generator = ReportGenerator()
    
    print("=== 报告生成器 ===\n")
    
    # 生成并保存报告
    output_dir = Path('/root/.openclaw/workspace/skills/openclaw-self-analyzer/reports')
    files = generator.save_reports(output_dir)
    
    print("✅ 报告已生成:")
    print(f"  - Markdown: {files['markdown']}")
    print(f"  - JSON: {files['json']}")
