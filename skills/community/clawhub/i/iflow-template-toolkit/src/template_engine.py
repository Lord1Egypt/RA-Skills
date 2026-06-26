#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iFlow Template Engine - Simple, dependency-free template rendering

Features:
- Variable substitution: {{variable}} and {{obj.field}}
- Conditional blocks: {% if condition %}...{% elif %}...{% else %}...{% endif %}
- For loops: {% for item in items %}...{% endfor %}
- Nested expressions: variable == "value"
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, Union


class TemplateEngine:
    """Simple template engine using regex, no external dependencies"""
    
    def __init__(self, template_dir: Optional[str] = None):
        self.template_dir = Path(template_dir) if template_dir else None
    
    def load_template(self, template_name: str) -> str:
        if self.template_dir:
            template_path = self.template_dir / template_name
        else:
            template_path = Path(template_name)
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def render(self, template_content: str, context: Dict[str, Any]) -> str:
        result = template_content
        result = self._process_loops(result, context)
        result = self._process_conditionals(result, context)
        result = self._process_variables(result, context)
        return result
    
    def render_file(self, template_name: str, context: Dict[str, Any]) -> str:
        template_content = self.load_template(template_name)
        return self.render(template_content, context)
    
    def _get_value(self, key: str, context: Dict[str, Any]) -> Any:
        """Get value from context, supporting dot notation"""
        keys = key.split('.')
        value = context
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            elif hasattr(value, k):
                value = getattr(value, k)
            else:
                return None
        return value
    
    def _process_variables(self, content: str, context: Dict[str, Any]) -> str:
        """Replace {{variable}} and {{obj.field}} with context values"""
        def replace_var(match):
            key = match.group(1).strip()
            value = self._get_value(key, context)
            return str(value) if value is not None else ''
        
        # Match {{variable}} and {{obj.field}}
        pattern = r'\{\{\s*([\w.]+)\s*\}\}'
        return re.sub(pattern, replace_var, content)
    
    def _process_conditionals(self, content: str, context: Dict[str, Any]) -> str:
        def evaluate_condition(condition: str, ctx: Dict[str, Any]) -> bool:
            condition = condition.strip()
            
            # Handle: variable == "value"
            eq_match = re.match(r"([\w.]+)\s*==\s*['\"](.+?)['\"]", condition)
            if eq_match:
                val = self._get_value(eq_match.group(1), ctx)
                return str(val) == eq_match.group(2)
            
            # Handle: variable != "value"
            neq_match = re.match(r"([\w.]+)\s*!=\s*['\"](.+?)['\"]", condition)
            if neq_match:
                val = self._get_value(neq_match.group(1), ctx)
                return str(val) != neq_match.group(2)
            
            # Handle: variable in ['a', 'b']
            in_match = re.match(r"([\w.]+)\s+in\s+\[(.+?)\]", condition)
            if in_match:
                val = self._get_value(in_match.group(1), ctx)
                values = re.findall(r"['\"](.+?)['\"]", in_match.group(2))
                return str(val) in values
            
            # Simple truthy check
            value = self._get_value(condition, ctx)
            if value is None:
                return False
            if isinstance(value, bool):
                return value
            if isinstance(value, (list, dict, str)):
                return len(value) > 0
            return bool(value)
        
        def find_endif(text: str, start: int) -> int:
            depth, pos = 1, start
            while depth > 0 and pos < len(text):
                tag_start = text.find('{%', pos)
                if tag_start == -1:
                    return -1
                tag_end = text.find('%}', tag_start)
                if tag_end == -1:
                    return -1
                tag_content = text[tag_start+2:tag_end].strip()
                if tag_content.startswith('if '):
                    depth += 1
                elif tag_content == 'endif':
                    depth -= 1
                pos = tag_end + 2
                if depth == 0:
                    return tag_start
            return -1
        
        result = content
        for _ in range(100):
            if_match = re.search(r'\{%\s*if\s+(.+?)\s*%\}', result)
            if not if_match:
                break
            if_pos, if_cond = if_match.start(), if_match.group(1)
            content_start = if_match.end()
            endif_pos = find_endif(result, content_start)
            if endif_pos == -1:
                result = result[:if_pos] + result[content_start:]
                break
            endif_end = result.find('%}', endif_pos) + 2
            block_text = result[content_start:endif_pos]
            branches, tag_positions = [], []
            for m in re.finditer(r'\{%\s*(elif\s+.+?|else)\s*%\}', block_text):
                tag_positions.append((m.start(), m.end(), m.group(1).strip()))
            if tag_positions:
                branches.append((if_cond, block_text[:tag_positions[0][0]]))
                for i, (start, end, tag) in enumerate(tag_positions):
                    branch_content = block_text[end:tag_positions[i+1][0]] if i + 1 < len(tag_positions) else block_text[end:]
                    cond = tag[5:].strip() if tag.startswith('elif ') else 'else'
                    branches.append((cond, branch_content))
            else:
                branches.append((if_cond, block_text))
            selected_content = ''
            for cond, branch_content in branches:
                if cond == 'else':
                    selected_content = branch_content
                    break
                if evaluate_condition(cond, context):
                    selected_content = branch_content
                    break
            result = result[:if_pos] + selected_content + result[endif_end:]
        return result
    
    def _process_loops(self, content: str, context: Dict[str, Any]) -> str:
        for_pattern = r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}'
        
        def replace_for(match):
            item_name, list_name, template_block = match.group(1), match.group(2), match.group(3)
            items = context.get(list_name, [])
            if not isinstance(items, (list, tuple)):
                return ''
            result_parts = []
            for i, item in enumerate(items):
                item_context = context.copy()
                item_context[item_name] = item
                item_context['index'] = i
                item_context['index1'] = i + 1
                item_context['first'] = i == 0
                item_context['last'] = i == len(items) - 1
                result_parts.append(self.render(template_block, item_context))
            return ''.join(result_parts)
        
        return re.sub(for_pattern, replace_for, content, flags=re.DOTALL)


def render_template(template: Union[str, Path], context: Dict[str, Any], 
                   template_dir: Optional[str] = None) -> str:
    """Convenience function to render a template"""
    engine = TemplateEngine(template_dir)
    if isinstance(template, Path) or (isinstance(template, str) and '{%' not in template and '{{' not in template):
        return engine.render_file(str(template), context)
    return engine.render(template, context)
