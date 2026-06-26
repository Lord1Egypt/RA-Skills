#!/usr/bin/env python3
"""
OpenClaw 钩子生成器
根据架构分析生成自定义钩子
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class HookGenerator:
    """钩子生成器"""
    
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
    
    def generate_pre_hook(self, stage: str, hook_name: str, logic: str) -> str:
        """生成前置钩子"""
        hook_code = f'''/**
 * Pre-hook for {stage}
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */
async function {hook_name}(context, next) {{
    // Your pre-processing logic here
    {logic}
    
    // Call next stage
    await next(context);
}}

module.exports = {{ {hook_name} }};
'''
        return hook_code
    
    def generate_post_hook(self, stage: str, hook_name: str, logic: str) -> str:
        """生成后置钩子"""
        hook_code = f'''/**
 * Post-hook for {stage}
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */
async function {hook_name}(context, result) {{
    // Your post-processing logic here
    {logic}
    
    // Return result
    return result;
}}

module.exports = {{ {hook_name} }};
'''
        return hook_code
    
    def generate_replace_hook(self, stage: str, hook_name: str, logic: str) -> str:
        """生成替换钩子"""
        hook_code = f'''/**
 * Replace-hook for {stage}
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */
async function {hook_name}(context) {{
    // Your custom implementation here
    {logic}
    
    // Return result (replaces original stage)
    return {{
        success: true,
        data: context
    }};
}}

module.exports = {{ {hook_name} }};
'''
        return hook_code
    
    def generate_hook_package(self, hook_name: str, hook_type: str, stage: str, logic: str) -> Dict[str, str]:
        """生成完整的钩子包"""
        if hook_type == 'pre':
            code = self.generate_pre_hook(stage, hook_name, logic)
        elif hook_type == 'post':
            code = self.generate_post_hook(stage, hook_name, logic)
        elif hook_type == 'replace':
            code = self.generate_replace_hook(stage, hook_name, logic)
        else:
            raise ValueError(f"Unknown hook type: {hook_type}")
        
        return {
            'name': hook_name,
            'type': hook_type,
            'stage': stage,
            'code': code,
            'generated_at': str(datetime.now())
        }
    
    def generate_all_hooks(self) -> List[Dict[str, str]]:
        """为所有阶段生成示例钩子"""
        hooks = []
        
        if 'pipeline' not in self.architecture:
            print("Warning: No pipeline data found in architecture")
            return hooks
        
        for stage_name, stage_info in self.architecture['pipeline'].items():
            # 为每个阶段生成一个pre-hook示例
            hook = self.generate_hook_package(
                hook_name=f"pre_{stage_name}_custom",
                hook_type='pre',
                stage=stage_name,
                logic='// Custom pre-processing logic\nconsole.log("Pre-processing:", context);'
            )
            hooks.append(hook)
        
        return hooks
    
    def save_hooks(self, hooks: List[Dict], output_dir: Path):
        """保存钩子到文件"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for hook in hooks:
            file_name = f"{hook['name']}.js"
            file_path = output_dir / file_name
            
            with open(file_path, 'w') as f:
                f.write(hook['code'])
        
        # 生成清单文件
        manifest = {
            'version': '1.0.0',
            'generated_at': str(datetime.now()),
            'hooks': [
                {
                    'name': h['name'],
                    'type': h['type'],
                    'stage': h['stage'],
                    'file': f"{h['name']}.js"
                }
                for h in hooks
            ]
        }
        
        with open(output_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return len(hooks)

if __name__ == '__main__':
    generator = HookGenerator()
    
    print("=== 钩子生成器 ===\n")
    
    # 生成所有钩子
    hooks = generator.generate_all_hooks()
    print(f"生成了 {len(hooks)} 个钩子")
    
    # 保存钩子
    output_dir = Path('/root/.openclaw/workspace/skills/openclaw-self-analyzer/generated_hooks')
    count = generator.save_hooks(hooks, output_dir)
    print(f"已保存 {count} 个钩子到 {output_dir}")
    
    print("\n生成的钩子:")
    for hook in hooks:
        print(f"  - {hook['name']}: {hook['type']} hook for {hook['stage']}")
