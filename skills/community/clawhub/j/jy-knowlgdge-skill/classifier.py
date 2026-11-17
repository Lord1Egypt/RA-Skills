"""
智能分类器
使用 LLM 进行文件价值评估和自动分类。
"""

import json
import re
from typing import Optional, Dict, Any, List, Tuple


class LLMClassifier:
    """
    基于 LLM 的文件价值评估与智能分类器
    支持 OpenAI 兼容 API
    """

    VALUE_PROMPT_TEMPLATE = """你是一位知识库质检专家。请评估以下文件内容是否具有制作知识库的价值。

评估维度：
1. 信息密度：内容是否包含实质性信息
2. 专业性：内容是否具有专业知识
3. 结构化程度：内容是否有良好的组织结构
4. 可复用性：内容是否适合作为微调数据集

输出严格 JSON 格式（不要包含其他文字）：
{{
  "has_value": true/false,
  "score": 0.0-1.0,
  "reason": "评估理由（简短）",
  "suggested_category": "建议的一级分类名称"
}}

文件内容（前2000字符）：
---
{content}
---"""

    CLASSIFY_PROMPT_TEMPLATE = """你是一位文档分类专家。请将以下文件内容归类到现有分类体系中。

现有分类树：
{category_tree}

文件内容（前2000字符）：
---
{content}
---

请判断该文件应归属于哪个分类。输出严格 JSON 格式：
{{
  "matched": true/false,
  "category_path": "/一级分类/二级分类",
  "category_slug": "匹配分类的slug",
  "confidence": 0.0-1.0,
  "reasoning": "归类理由",
  "new_category_name": null,
  "new_category_description": null,
  "new_category_keywords": null,
  "new_parent_path": null,
  "suggest_ga": false,
  "ga_genre": null,
  "ga_audience": null
}}

如果 matched 为 false（即无匹配分类），请设置 new_category_name 为新分类名称，
new_category_description 为描述，new_category_keywords 为关键词数组，
new_parent_path 为父分类路径（如果适合放在某现有分类下）或 null（作为一级分类）。

此外，请判断该文件是否适合使用 GA（Genre-Audience，体裁-受众）增强模式生成问题。
GA 增强适用于：标准/规范（可切换起草者/审核者视角）、教材/培训材料（可切换讲师/学员视角）、
政策文件（可切换制定者/执行者视角）等有多角色解读价值的文档。
如果不适合，请设置 suggest_ga 为 false。
如果适合，设置 suggest_ga 为 true，并给出一个推荐的体裁(ga_genre)和受众(ga_audience)名称。"""

    def __init__(self, base_url: str, api_key: str, model: str,
                 temperature: float = 0.3, max_tokens: int = 4096):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _call_llm(self, prompt: str) -> str:
        """调用 LLM API（兼容思考模型：提取 content，忽略 reasoning_content）"""
        import requests

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        resp = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60
        )
        resp.raise_for_status()
        msg = resp.json()["choices"][0]["message"]
        # 兼容思考模型：content 可能为空，此时从 reasoning_content 提取
        content = msg.get("content", "")
        if not content or not content.strip():
            content = msg.get("reasoning_content", "")

        # 清理思考模型可能残留的  response 等标记
        content = self._clean_thinking_tags(content)
        return content

    def _clean_thinking_tags(self, text: str) -> str:
        """清理思考模型输出中可能残留的特殊标记"""
        import re
        # 移除  和  标记
        text = re.sub(r'<\|?im_end\|?>', '', text)
        text = re.sub(r'<\|?im_start\|?>[^\n]*\n?', '', text)
        # 移除  标记
        text = re.sub(r'^<｜end▁of▁thinking｜>\s*', '', text.strip())
        text = re.sub(r'\s*$', '', text.strip())
        # 移除  标记（有的思考模型会用）
        text = re.sub(r'^ thinking\s*', '', text.strip())
        return text.strip()

    def _extract_json(self, text: str) -> dict:
        """从 LLM 回复中提取 JSON（多策略容错）"""
        # 打印调试信息
        print(f"  [LLM RAW] first 300: {repr(text[:300])}")

        strategies = []

        # Strategy 1: 直接解析
        strategies.append(("direct", lambda: json.loads(text.strip())))

        # Strategy 2: 提取 ```json ... ``` 代码块
        def extract_code_block():
            match = re.search(r'```(?:json)?\s*\n(.*?)\n\s*```', text, re.DOTALL)
            if not match:
                match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                return json.loads(match.group(1).strip())
            raise ValueError("no code block")
        strategies.append(("code_block", extract_code_block))

        # Strategy 3: 从第一个 { 到最后一个 } 提取
        def extract_braces():
            start = text.find('{')
            end = text.rfind('}')
            if start >= 0 and end > start:
                return json.loads(text[start:end+1])
            raise ValueError("no braces")
        strategies.append(("braces", extract_braces))

        # Strategy 4: 修复常见 JSON 问题后重试
        def extract_fixed():
            start = text.find('{')
            end = text.rfind('}')
            if start >= 0 and end > start:
                json_str = text[start:end+1]
                for fix_fn in [self._fix_trailing_comma, self._fix_comments, str.strip]:
                    try:
                        return json.loads(fix_fn(json_str))
                    except (json.JSONDecodeError, ValueError):
                        continue
            raise ValueError("cannot fix")
        strategies.append(("fixed", extract_fixed))

        # Strategy 5: LLM 没输出 {}，手动包装
        def wrap_braces():
            # 查找 JSON 键值对模式
            clean = text.strip()
            # 移除所有注释和非JSON前缀
            for marker in ['```json', '```', 'JSON:', 'json:']:
                idx = clean.lower().find(marker.lower())
                if idx >= 0:
                    clean = clean[idx + len(marker):].strip()
            # 如果以 "key": value 开头（缺少外层{），包装
            if re.match(r'^\s*"[^"]+"\s*:', clean):
                clean = '{' + clean.rstrip().rstrip(',').rstrip('}') + '}'
            return json.loads(clean)
        strategies.append(("wrap", wrap_braces))

        for name, fn in strategies:
            try:
                result = fn()
                print(f"  [LLM JSON] parsed via {name}")
                return result
            except (json.JSONDecodeError, ValueError, KeyError):
                continue

        raise ValueError(f"无法从 LLM 回复中提取 JSON，原始回复: {text[:500]}")

    def _fix_trailing_comma(self, s: str) -> str:
        return re.sub(r',\s*([}\]])', r'\1', s)

    def _fix_comments(self, s: str) -> str:
        s = re.sub(r'//.*?\n', '\n', s)
        s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
        return s

    def evaluate_value(self, content: str) -> Dict[str, Any]:
        """
        评估文件价值
        返回: { has_value, score, reason, suggested_category }
        """
        sample = content[:2000]
        prompt = self.VALUE_PROMPT_TEMPLATE.format(content=sample)
        response = self._call_llm(prompt)
        return self._extract_json(response)

    def classify(self, content: str, category_tree: dict,
                 threshold: float = 0.7) -> Dict[str, Any]:
        """
        智能分类文件
        返回:
        {
            matched: bool,          # 是否匹配现有分类
            category_path: str,     # 分类路径
            confidence: float,      # 置信度
            reasoning: str,         # 理由
            is_new: bool,           # 是否需要创建新分类
            new_category: dict,     # 新分类信息（仅 is_new=True 时有值）
        }
        """
        tree_json = json.dumps(category_tree, ensure_ascii=False, indent=2)
        sample = content[:2000]
        prompt = self.CLASSIFY_PROMPT_TEMPLATE.format(
            category_tree=tree_json,
            content=sample
        )
        response = self._call_llm(prompt)
        result = self._extract_json(response)

        is_new = not result.get("matched") or result.get("confidence", 1.0) < threshold

        if is_new and result.get("new_category_name"):
            result["is_new"] = True
            result["new_category"] = {
                "name": result["new_category_name"],
                "description": result.get("new_category_description", ""),
                "keywords": result.get("new_category_keywords", []),
                "parent_path": result.get("new_parent_path")
            }
        else:
            result["is_new"] = False

        return result

    def test_connection(self) -> bool:
        """测试 LLM 连接"""
        try:
            self._call_llm("Hello, please reply with just 'OK'.")
            return True
        except Exception:
            return False
