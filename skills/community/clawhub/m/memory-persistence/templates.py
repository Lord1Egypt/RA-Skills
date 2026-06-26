"""
Memory Templates - Predefined formats for quick memory creation
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class MemoryTemplate:
    """A memory template definition"""
    name: str
    description: str
    fields: List[Dict[str, str]]  # [{"name": "field_name", "label": "Display Label", "type": "text|select|checkbox"}]
    default_tags: List[str] = field(default_factory=list)
    generate_content: Callable = None  # Function to generate content from filled fields


class MemoryTemplates:
    """
    Predefined templates for common memory types
    """
    
    TEMPLATES = {
        "user_preference": MemoryTemplate(
            name="user_preference",
            description="用户偏好设置",
            fields=[
                {"name": "item", "label": "偏好项目", "type": "text"},
                {"name": "value", "label": "偏好值", "type": "text"},
                {"name": "reason", "label": "原因（可选）", "type": "text"}
            ],
            default_tags=["偏好"],
            generate_content=lambda f: f"用户偏好：{f.get('item', '')} = {f.get('value', '')}{'（' + f['reason'] + '）' if f.get('reason') else ''}"
        ),
        
        "user_fact": MemoryTemplate(
            name="user_fact",
            description="用户事实信息",
            fields=[
                {"name": "fact", "label": "事实内容", "type": "text"},
                {"name": "category", "label": "类别", "type": "select", "options": ["个人信息", "工作", "技术", "其他"]},
                {"name": "confidence", "label": "确信程度", "type": "select", "options": ["确定", "大概", "不确定"]}
            ],
            default_tags=["事实"],
            generate_content=lambda f: f"{f.get('category', '用户')}：{f.get('fact', '')}（{f.get('confidence', '确定')}）"
        ),
        
        "task": MemoryTemplate(
            name="task",
            description="任务或待办事项",
            fields=[
                {"name": "title", "label": "任务标题", "type": "text"},
                {"name": "deadline", "label": "截止时间", "type": "text"},
                {"name": "priority", "label": "优先级", "type": "select", "options": ["高", "中", "低"]},
                {"name": "status", "label": "状态", "type": "select", "options": ["待处理", "进行中", "已完成"]}
            ],
            default_tags=["任务"],
            generate_content=lambda f: f"任务：{f.get('title', '')}\n截止：{f.get('deadline', '未指定')}\n优先级：{f.get('priority', '中')}\n状态：{f.get('status', '待处理')}"
        ),
        
        "decision": MemoryTemplate(
            name="decision",
            description="决策记录",
            fields=[
                {"name": "decision", "label": "决定内容", "type": "text"},
                {"name": "reason", "label": "决定原因", "type": "text"},
                {"name": "alternatives", "label": "备选方案", "type": "text"}
            ],
            default_tags=["决策"],
            generate_content=lambda f: f"决定：{f.get('decision', '')}\n原因：{f.get('reason', '')}\n备选：{f.get('alternatives', '无')}"
        ),
        
        "meeting_note": MemoryTemplate(
            name="meeting_note",
            description="会议记录",
            fields=[
                {"name": "topic", "label": "会议主题", "type": "text"},
                {"name": "date", "label": "日期时间", "type": "text"},
                {"name": "attendees", "label": "参与者", "type": "text"},
                {"name": "summary", "label": "会议纪要", "type": "text"},
                {"name": "action_items", "label": "行动项", "type": "text"}
            ],
            default_tags=["会议"],
            generate_content=lambda f: f"会议：{f.get('topic', '')}\n时间：{f.get('date', '')}\n参与者：{f.get('attendees', '')}\n纪要：{f.get('summary', '')}\n行动项：{f.get('action_items', '')}"
        ),
        
        "bug_report": MemoryTemplate(
            name="bug_report",
            description="Bug 报告",
            fields=[
                {"name": "bug_description", "label": "Bug 描述", "type": "text"},
                {"name": "severity", "label": "严重程度", "type": "select", "options": ["Critical", "High", "Medium", "Low"]},
                {"name": "steps", "label": "复现步骤", "type": "text"},
                {"name": "expected", "label": "期望行为", "type": "text"},
                {"name": "actual", "label": "实际行为", "type": "text"}
            ],
            default_tags=["bug", "技术"],
            generate_content=lambda f: f"Bug：{f.get('bug_description', '')}\n严重程度：{f.get('severity', 'Medium')}\n复现步骤：{f.get('steps', '')}\n期望：{f.get('expected', '')}\n实际：{f.get('actual', '')}"
        ),
        
        "code_decision": MemoryTemplate(
            name="code_decision",
            description="技术决策记录",
            fields=[
                {"name": "topic", "label": "决策主题", "type": "text"},
                {"name": "decision", "label": "最终决定", "type": "text"},
                {"name": "pros", "label": "优点", "type": "text"},
                {"name": "cons", "label": "缺点", "type": "text"},
                {"name": "alternatives", "label": "考虑的替代方案", "type": "text"}
            ],
            default_tags=["技术", "决策"],
            generate_content=lambda f: f"技术决策：{f.get('topic', '')}\n决定：{f.get('decision', '')}\n优点：{f.get('pros', '')}\n缺点：{f.get('cons', '')}\n替代方案：{f.get('alternatives', '')}"
        ),
    }
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List all available template names"""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def get_template(cls, name: str) -> Optional[MemoryTemplate]:
        """Get a template by name"""
        return cls.TEMPLATES.get(name)
    
    @classmethod
    def list_all(cls) -> Dict[str, MemoryTemplate]:
        """Get all templates"""
        return cls.TEMPLATES
    
    @classmethod
    def generate_from_template(
        cls,
        template_name: str,
        field_values: Dict[str, str]
    ) -> Optional[Dict[str, any]]:
        """
        Generate memory content from a filled template
        
        Args:
            template_name: Name of the template
            field_values: Dict of field_name -> value
        
        Returns:
            Dict with 'content', 'tags', or None if template not found
        """
        template = cls.TEMPLATES.get(template_name)
        if not template:
            return None
        
        content = template.generate_content(field_values) if template.generate_content else ""
        
        # Collect filled tags
        tags = list(template.default_tags)
        
        return {
            "content": content,
            "tags": tags,
            "template": template_name,
            "fields": field_values
        }
    
    @classmethod
    def render_template_cli(cls, template_name: str) -> Optional[str]:
        """
        Render template fields for CLI input
        
        Returns a guide string for manual input
        """
        template = cls.TEMPLATES.get(template_name)
        if not template:
            return None
        
        lines = [
            f"Template: {template.description}",
            f"Usage: memory add \"[content]\" --tags {','.join(template.default_tags)}",
            "",
            "Fields:"
        ]
        
        for field in template.fields:
            field_type = field.get('type', 'text')
            if field_type == 'select':
                opts = ', '.join(field.get('options', []))
                lines.append(f"  {field['label']} ({field['name']}): {opts}")
            else:
                lines.append(f"  {field['label']} ({field['name']})")
        
        return '\n'.join(lines)
