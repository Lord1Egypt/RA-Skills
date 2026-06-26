#!/usr/bin/env python3
"""
lobster-novel: Chapter generator using SenseNova API
"""
import json, os, re, sys
from pathlib import Path
from typing import Optional, List, Dict

sys.path.insert(0, str(Path(__file__).parent))
from bible import ChapterSpec

# ── Token estimation ────────────────────────────────────────

try:
    import tiktoken
    _ENCODING = tiktoken.get_encoding("cl100k_base")
    def count_tokens(text: str) -> int:
        return len(_ENCODING.encode(text))
except ImportError:
    def count_tokens(text: str) -> int:
        """Fallback: 中文≈1.8字/token, 英文≈0.75词/token
        cl100k_base 实测：中文小说平均每token 1.7-2.0汉字"""
        ch = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        en = len(re.findall(r'[a-zA-Z]+', text))
        punts = len(re.findall(r'[，。！？、；：""''（）【】《》—…·]', text))
        return int(ch / 1.8 + en / 0.75 + punts / 3)


# ── 中文上下文压缩 ────────────────────────────────────────

def compress_context(text: str, max_chars: int = 3000) -> str:
    """智能压缩中文上下文：保留核心信息，丢弃冗余"""
    if len(text) <= max_chars:
        return text

    # 保留前x字符，后y字符，中间摘要
    head_chars = max_chars // 2
    tail_chars = max_chars - head_chars

    head = text[:head_chars]
    tail = text[-tail_chars:] if tail_chars > 100 else ""

    return head + "\n\n[...中间内容压缩省略...]\n\n" + tail


# ── 中文Token成本估算 ──────────────────────────────────────

# SenseNova 日日新 6.7 Flash Lite 官方定价（参考）
# 注意：实际价格以官方为准，这里做参考估算
SENSENOVA_PRICE = {
    "input_per_1k": 0.002,     # 输入 ￥0.002/1K tokens
    "output_per_1k": 0.005,    # 输出 ￥0.005/1K tokens
}

def estimate_cost(input_tokens: int, output_tokens: int = 0, model: str = "flash-lite") -> dict:
    """估算生成成本（人民币）"""
    if model == "flash-lite":
        prices = SENSENOVA_PRICE
    else:
        prices = {"input_per_1k": 0.002, "output_per_1k": 0.005}
    cost_in = input_tokens / 1000 * prices["input_per_1k"]
    cost_out = output_tokens / 1000 * prices["output_per_1k"]
    return {
        "input_cost": round(cost_in, 4),
        "output_cost": round(cost_out, 4),
        "total_cost": round(cost_in + cost_out, 4),
        "currency": "CNY",
    }


def token_report(messages: list, response: str = "") -> dict:
    """Return a token usage breakdown for a request."""
    prompt_tokens = sum(count_tokens(m.get("content", "")) for m in messages)
    output_tokens = count_tokens(response) if response else 0
    total = prompt_tokens + output_tokens
    return {
        "prompt_tokens": prompt_tokens,
            "output_tokens": output_tokens,
        "total_tokens": total,
    }


class ChapterGenerator:
    """Generate chapter text using SenseNova API (stateless)."""

    API_URL = "https://token.sensenova.cn/v1/chat/completions"
    MODEL = "sensenova-6.7-flash-lite"

    def __init__(self, api_key: Optional[str] = None, bible_dir: Optional[Path] = None):
        self.api_key = api_key or os.environ.get("SENSENOVA_API_KEY", "")
        self.last_token_usage: dict = {}
        self.bible_dir = bible_dir  # 用于加载风格模板
        # 移除 _style_template_content，直接每次加载（避免缓存过期问题）

    def load_style_template(self, template_name: str = None) -> Optional[str]:
        """加载风格模板内容"""
        if self.bible_dir is None:
            return None
        
        from bible import BibleManager
        manager = BibleManager(self.bible_dir)
        return manager.load_style_template(template_name)

    def _call_api(self, messages: list, temp: float = 0.7, max_tokens: int = 8192) -> str:
        import urllib.request
        payload = json.dumps({
            "model": self.MODEL,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tokens,
        }).encode("utf-8")
        req = urllib.request.Request(
            self.API_URL, data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            })
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        # Token tracking from API response or estimation
        usage = data.get("usage", {})
        if usage:
            self.last_token_usage = usage
        else:
            self.last_token_usage = token_report(messages, content)
        return content

    @property
    def last_tokens(self) -> dict:
        return self.last_token_usage

    def token_cost_report(self, detail: bool = False) -> str:
        """Token用量+成本报告"""
        u = self.last_token_usage
        if not u:
            return "no API calls yet"
        inp = u.get("prompt_tokens", u.get("input_tokens", 0))
        out = u.get("output_tokens", u.get("completion_tokens", 0))
        total = u.get("total_tokens", inp + out)
        cost = estimate_cost(inp, out)

        lines = [
            f"Token 用量:",
            f"  输入:  {inp:>8,} tokens",
            f"  输出:  {out:>8,} tokens",
            f"  总计:  {total:>8,} tokens",
            f"  成本:  ￥{cost['total_cost']:.4f}",
        ]
        if detail:
            lines += [
                f"  输入费: ￥{cost['input_cost']:.4f}",
                f"  输出费: ￥{cost['output_cost']:.4f}",
                f"  约合   {u.get('estimated_chars', 0):,} 汉字",
            ]
        return "\n".join(lines)

    def write_chapter(self, spec: ChapterSpec, context: str,
                      roster_block: str = "", style_block: str = "",
                      style_template: Optional[str] = None) -> str:
        """Generate a single chapter from spec + context + 风格模板"""
        # 风格模板长度限制（避免占用过多 prompt token）
        MAX_STYLE_TEMPLATE_CHARS = 4000
        
        system = ("你是一个优秀的长篇中文网文作者。根据设定和上下文写作章节。\n"
                  "要求：1) 保持叙事节奏和张力 2) 章节末留钩子 3) 推进至少一个角色弧")

        # 上下文压缩（中文写作特有优化：只送关键信息）
        compressed = compress_context(context, max_chars=4000) if len(context) > 4000 else context[:4000]

        # 角色状态注入（告诉作者当前配角使用情况）
        char_block = roster_block if roster_block else ""

        # 风格模板注入（如果提供了风格模板）
        if style_template is None and self.bible_dir is not None:
            # 尝试从 bible.json 加载默认风格模板
            style_template = self.load_style_template()

        prompt = (
            f"# Chapter {spec.number} Writing\n\n"
            f"Title: {spec.title or '(auto)'}\n"
            f"Summary: {spec.summary or '(from context)'}\n"
            f"Scenes: {', '.join(spec.scene_beats) if spec.scene_beats else '(follow narrative flow)'}\n"
            f"POV: {spec.pov or 'third-person limited'}\n\n"
            f"## Context\n{compressed}\n\n"
        )
        if char_block:
            prompt += f"## 当前角色状态\n{char_block}\n\n"
        if style_template:
            # 截断过长的风格模板
            style_content = style_template[:MAX_STYLE_TEMPLATE_CHARS]
            if len(style_template) > MAX_STYLE_TEMPLATE_CHARS:
                style_content += f"\n\n[...风格模板内容已截断（共{len(style_template)}字符），完整内容见 templates/目录...]"
            prompt += f"## 写作风格模板\n{style_content}\n\n"
            prompt += f"请严格遵循上述风格模板的要求进行写作。\n\n"
        prompt += (
            "Output format:\n"
            f"# Chapter {spec.number}: [Title]\n\n"
            "(text here)"
        )
        return self._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], temp=0.7)

    def write_batch(self, specs: List[ChapterSpec], context_template: str) -> List[str]:
        """Generate multiple chapters sequentially."""
        chapters = []
        current_context = context_template
        for spec in specs:
            text = self.write_chapter(spec, current_context)
            chapters.append(text)
            # Update context with new chapter summary
            first_line = text.split("\n")[0] if text else f"Ch{spec.number}"
            current_context += f"\n--- Ch{spec.number} written: {first_line[:80]} ---"
        return chapters

    def review_chapter(self, role: str, chapter_num: int, text: str,
                       bible_context: str) -> dict:
        """Single-role review using SubAgent-style API call.
        5 roles: Reader, Editor, Storyteller, Stylist, Critic.
        Returns structured JSON: {score, issues[], suggestions[]}
        """
        prompts = {
            "Reader": "你是一名资深网文读者。评估章节的阅读体验：开篇吸引力、节奏、画面感、章节末钩子。",
            "Editor": "你是一名专业编辑。检查：错别字、病句、标点、段落节奏、AI味。",
            "Storyteller": "你是一名故事架构师。评估：剧情逻辑、角色一致性、伏笔、世界观一致性。",
            "Stylist": "你是一名文学顾问。评估：叙事技巧、语言风格、人物刻画深度、场景氛围渲染。注意评价文字的艺术性而非正确性。",
            "Critic": "你是一名毒舌读者。专门找缺点：套路化桥段、水文注水、毒点雷点、逻辑硬伤、人设崩塌。不留情面。",
        }
        role_prompt = prompts.get(role, prompts["Reader"])

        system = (
            f"{role_prompt}\n"
            "返回JSON格式：{'score': 0-100, 'issues': [{'severity':'P0/P1/P2','desc':'...','fix':'...'}], "
            "'strengths': ['...'], 'suggestions': ['...']}\n"
            "只返回JSON，不要额外文字。"
        )
        user_msg = (
            f"## Chapter {chapter_num}\n\n"
            f"{text[:6000]}\n\n"
            f"## Context\n{bible_context[:2000]}"
        )

        result = self._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ], temp=0.3, max_tokens=2048)

        # Parse JSON from response
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        return {"score": 50, "issues": [{"severity": "P1", "desc": "parse failed"}],
                "strengths": [], "suggestions": []}
