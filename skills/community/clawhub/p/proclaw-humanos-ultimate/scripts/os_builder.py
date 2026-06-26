#!/usr/bin/env python3
"""
HumanOS构建器：根据框架生成HumanOS Skill
"""

import json
from pathlib import Path
from typing import Dict, List


class HumanOSBuilder:
    """HumanOS构建器"""

    # 4种HumanOS类型
    OS_TYPES = {
        'human': {
            'name': 'HumanType',
            'template': 'human-template.md',
            'description': '人物型，蒸馏特定人物的思维框架'
        },
        'theme': {
            'name': 'ThemeType',
            'template': 'theme-template.md',
            'description': '主题型，综合多人视角的主题框架'
        },
        'scenario': {
            'name': 'ScenarioType',
            'template': 'scenario-template.md',
            'description': '场景型，特定场景的决策系统'
        },
        'methodology': {
            'name': 'MethodologyType',
            'template': 'methodology-template.md',
            'description': '方法论型，完整的方法论实施框架'
        }
    }

    def __init__(self):
        self.built_os = {}

    def build_humanos(self, framework: Dict, os_type: str,
                      template_dir: str, output_file: str) -> Dict:
        """构建HumanOS"""

        # 加载模板
        template_path = Path(template_dir) / self.OS_TYPES[os_type]['template']
        if not template_path.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 填充模板
        skill_content = self._fill_template(template_content, framework, os_type)

        # 生成Agentic Protocol
        agentic_protocol = self._generate_agentic_protocol(framework)

        # 整合到Skill内容中
        skill_content = self._integrate_agentic_protocol(skill_content, agentic_protocol)

        # 写入输出文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(skill_content)

        # 生成构建结果
        build_result = {
            'os_type': os_type,
            'target': framework.get('target', ''),
            'output_file': str(output_path),
            'framework_summary': framework.get('summary', {}),
            'agentic_protocol': agentic_protocol,
            'build_status': 'success'
        }

        self.built_os = build_result

        return build_result

    def _fill_template(self, template: str, framework: Dict,
                       os_type: str) -> str:
        """填充模板"""

        # 准备替换变量
        variables = {
            'TARGET': framework.get('target', ''),
            'OS_TYPE': self.OS_TYPES[os_type]['name'],
            'DESCRIPTION': self.OS_TYPES[os_type]['description'],
            'MENTAL_MODELS': self._format_mental_models(
                framework.get('mental_models', [])
            ),
            'DECISION_HEURISTICS': self._format_decision_heuristics(
                framework.get('decision_heuristics', [])
            ),
            'EXPRESSION_DNA': self._format_expression_dna(
                framework.get('expression_dna', {})
            ),
            'VALUES': self._format_values(
                framework.get('values', [])
            ),
            'TOOLKIT': self._format_toolkit(
                framework.get('toolkit', [])
            ),
            'INTERNAL_TENSIONS': self._format_internal_tensions(
                framework.get('internal_tensions', [])
            ),
            'HONEST_BOUNDARIES': self._format_honest_boundaries(
                framework.get('honest_boundaries', [])
            )
        }

        # 替换变量
        content = template
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            content = content.replace(placeholder, str(var_value))

        return content

    def _format_mental_models(self, models: List[Dict]) -> str:
        """格式化心智模型"""

        formatted = []
        for model in models:
            name = model.get('name', '')
            description = model.get('description', '')
            validation = model.get('validation', {})

            # 只包含通过验证的模型
            if validation.get('passed'):
                formatted.append(f"- **{name}**: {description}")

        return '\n'.join(formatted) if formatted else '无通过验证的心智模型'

    def _format_decision_heuristics(self, heuristics: List[str]) -> str:
        """格式化决策启发式"""

        formatted = []
        for heuristic in heuristics[:10]:
            formatted.append(f"- {heuristic}")

        return '\n'.join(formatted) if formatted else '无决策启发式'

    def _format_expression_dna(self, dna: Dict) -> str:
        """格式化表达DNA"""

        formatted = []

        if dna.get('sentence_patterns'):
            formatted.append("**句式模式**:")
            for pattern in dna['sentence_patterns'][:5]:
                formatted.append(f"  - {pattern}")

        if dna.get('vocabulary'):
            formatted.append("**特色词汇**:")
            for vocab in dna['vocabulary'][:10]:
                formatted.append(f"  - {vocab}")

        if dna.get('rhythm'):
            formatted.append(f"**节奏**: {dna['rhythm']}")

        return '\n'.join(formatted) if formatted else '无表达DNA'

    def _format_values(self, values: List[str]) -> str:
        """格式化价值观"""

        formatted = []
        for value in values[:5]:
            formatted.append(f"- {value}")

        return '\n'.join(formatted) if formatted else '无价值观'

    def _format_toolkit(self, tools: List[str]) -> str:
        """格式化工具箱"""

        formatted = []
        for tool in tools[:10]:
            formatted.append(f"- {tool}")

        return '\n'.join(formatted) if formatted else '无工具'

    def _format_internal_tensions(self, tensions: List[Dict]) -> str:
        """格式化内在张力"""

        formatted = []
        for tension in tensions[:5]:
            tension_desc = tension.get('tension', '')
            description = tension.get('description', '')
            formatted.append(f"- **{tension_desc}**: {description}")

        return '\n'.join(formatted) if formatted else '无内在张力'

    def _format_honest_boundaries(self, boundaries: List[str]) -> str:
        """格式化诚实边界"""

        formatted = []
        for boundary in boundaries[:5]:
            formatted.append(f"- {boundary}")

        return '\n'.join(formatted) if formatted else '无诚实边界'

    def _generate_agentic_protocol(self, framework: Dict) -> Dict:
        """生成Agentic Protocol"""

        # 从心智模型推导研究维度
        mental_models = framework.get('mental_models', [])
        validated_models = [m for m in mental_models if m.get('validation', {}).get('passed')]

        # 生成研究步骤
        research_steps = self._generate_research_steps(validated_models)

        agentic_protocol = {
            'version': '1.0',
            'target': framework.get('target', ''),
            'description': f'{framework.get("target", "")}的研究和回答协议',
            'steps': [
                {
                    'step': 1,
                    'name': '问题分类',
                    'description': '识别用户问题的类型和维度',
                    'actions': [
                        '分析问题的领域',
                        '识别相关的决策维度',
                        '确定问题的复杂度'
                    ]
                },
                {
                    'step': 2,
                    'name': '研究',
                    'description': f'应用{framework.get("target", "")}的心智模型进行深入分析',
                    'actions': research_steps
                },
                {
                    'step': 3,
                    'name': '回答',
                    'description': '生成结构化的回答，体现独特的思维框架',
                    'actions': [
                        '使用决策启发式推导结论',
                        '体现表达DNA的风格',
                        '标注诚实边界和局限性'
                    ]
                }
            ],
            'mental_models_used': [m.get('name', '') for m in validated_models],
            'decision_heuristics_used': framework.get('decision_heuristics', [])[:5]
        }

        return agentic_protocol

    def _generate_research_steps(self, mental_models: List[Dict]) -> List[str]:
        """生成研究步骤"""

        steps = []

        # 基于心智模型生成研究步骤
        for model in mental_models:
            model_name = model.get('name', '')
            steps.append(f"应用{model_name}心智模型分析问题")

        # 添加通用步骤
        steps.extend([
            "识别问题的核心矛盾",
            "应用决策启发式进行推理",
            "评估不同方案的优劣势"
        ])

        return steps

    def _integrate_agentic_protocol(self, skill_content: str,
                                     agentic_protocol: Dict) -> str:
        """整合Agentic Protocol到Skill内容"""

        # 将Agentic Protocol转换为Markdown格式
        protocol_md = self._format_agentic_protocol(agentic_protocol)

        # 替换模板中的Agentic Protocol占位符
        skill_content = skill_content.replace('{{AGENTIC_PROTOCOL}}', protocol_md)

        return skill_content

    def _format_agentic_protocol(self, protocol: Dict) -> str:
        """格式化Agentic Protocol"""

        formatted = f"""## Agentic Protocol

{protocol.get('description', '')}

### 步骤
"""

        for step_info in protocol.get('steps', []):
            formatted += f"""
#### 步骤 {step_info['step']}: {step_info['name']}

{step_info['description']}

**行动**:
"""
            for action in step_info.get('actions', []):
                formatted += f"- {action}\n"

        formatted += f"""
### 应用心智模型
"""
        for model_name in protocol.get('mental_models_used', []):
            formatted += f"- {model_name}\n"

        formatted += f"""
### 决策启发式
"""
        for heuristic in protocol.get('decision_heuristics_used', []):
            formatted += f"- {heuristic}\n"

        return formatted


def main():
    import argparse

    parser = argparse.ArgumentParser(description='HumanOS构建器')
    parser.add_argument('--framework', type=str, required=True,
                       help='框架JSON文件路径')
    parser.add_argument('--template-dir', type=str, required=True,
                       help='模板目录')
    parser.add_argument('--os-type', type=str, required=True,
                       choices=['human', 'theme', 'scenario', 'methodology'],
                       help='HumanOS类型')
    parser.add_argument('--output', type=str, required=True,
                       help='输出SKILL.md文件路径')

    args = parser.parse_args()

    # 读取框架
    with open(args.framework, 'r', encoding='utf-8') as f:
        framework = json.load(f)

    # 构建HumanOS
    builder = HumanOSBuilder()
    result = builder.build_humanos(
        framework,
        args.os_type,
        args.template_dir,
        args.output
    )

    print(f"HumanOS构建完成: {args.output}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
