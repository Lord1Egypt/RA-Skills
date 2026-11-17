"""
翰林学士 - 学术论文润色技能
调用 DeepSeek API 实现中英文论文润色、语法校对、降重改写。
"""
import os
import json
from coze_workload_identity import requests


# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
SKILL_ID = 7665153655141580854


def _get_credential():
    """获取 DeepSeek API Key"""
    key = os.getenv("COZE_DEEPSEEK_KEY_7665153655141580854")
    if not key:
        raise ValueError("缺少 DeepSeek API Key 配置，请检查凭证设置")
    return key


def _build_system_prompt(mode: str, language: str) -> str:
    """根据模式和语言构建系统提示词"""
    prompts = {
        "polish": {
            "zh": (
                "你是一位精通中文学术写作的编辑。请将以下文本润色为更学术化的表达，"
                "提升正式度和流畅度，但保持原意不变。不要添加新观点或数据，不要随意替换专业术语。"
                "按以下格式输出：\n"
                "【问题】指出原文存在的问题\n"
                "【修改建议】给出2-3个改写版本\n"
                "【解释】简要说明修改理由"
            ),
            "en": (
                "You are an expert academic editor. Polish the following text to improve "
                "academic tone, clarity, and formality. Preserve the original meaning. "
                "Do not add new ideas or data. Do not replace technical terms. "
                "Output in this format:\n"
                "[Issues] Point out problems in the original\n"
                "[Suggestions] Provide 2-3 revised versions\n"
                "[Explanation] Briefly explain the changes"
            ),
        },
        "proofread": {
            "zh": (
                "你是一位中文学术校对专家。请仅修正以下文本中的语法错误、标点错误和用词不当，"
                "不要改变表达风格和学术水平。按以下格式输出：\n"
                "【问题】指出语法/用词错误\n"
                "【修改建议】给出修正后的版本\n"
                "【解释】说明修正理由"
            ),
            "en": (
                "You are an academic proofreader. Correct only grammar, punctuation, "
                "and word choice errors in the following text. Do not change the writing "
                "style or academic level. Output in this format:\n"
                "[Issues] Point out grammar/word choice errors\n"
                "[Suggestions] Provide the corrected version\n"
                "[Explanation] Explain the corrections"
            ),
        },
        "paraphrase": {
            "zh": (
                "你是一位学术降重专家。请改写以下文本，在保持原意的前提下降低重复率。"
                "使用不同的句式结构、同义词替换和语序调整，但不要改变核心观点和专业术语。"
                "按以下格式输出：\n"
                "【问题】指出可能重复的表述\n"
                "【修改建议】给出2-3个改写版本\n"
                "【解释】说明改写策略"
            ),
            "en": (
                "You are an academic paraphrasing expert. Rewrite the following text to "
                "reduce similarity while preserving the original meaning. Use different "
                "sentence structures, synonyms, and word order. Do not change core ideas "
                "or technical terms. Output in this format:\n"
                "[Issues] Identify repetitive expressions\n"
                "[Suggestions] Provide 2-3 paraphrased versions\n"
                "[Explanation] Explain the paraphrasing strategy"
            ),
        },
    }
    return prompts.get(mode, prompts["polish"]).get(language, prompts["polish"]["zh"])


def polish_text(text: str, mode: str = "polish", language: str = "auto") -> dict:
    """
    润色论文文本。

    参数:
        text: 需要润色的文本
        mode: 润色模式 - "polish"(润色) / "proofread"(校对) / "paraphrase"(降重)
        language: 语言 - "zh"(中文) / "en"(英文) / "auto"(自动检测)

    返回:
        dict: {"original": str, "result": str, "mode": str}
    """
    # 自动检测语言
    if language == "auto":
        # 简单判断：如果文本中英文字符占比超过50%则为英文
        en_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())
        language = "en" if total_chars > 0 and en_chars / total_chars > 0.5 else "zh"

    system_prompt = _build_system_prompt(mode, language)
    api_key = _get_credential()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL, headers=headers, json=payload, timeout=60
        )
        if response.status_code >= 400:
            raise Exception(
                f"DeepSeek API 请求失败 (HTTP {response.status_code}): {response.text}"
            )

        data = response.json()
        result_text = data["choices"][0]["message"]["content"]

        return {
            "original": text,
            "result": result_text,
            "mode": mode,
            "language": language,
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")


def main(params: dict) -> dict:
    """
    技能入口函数。

    参数:
        params: {"text": str, "mode": str, "language": str}

    返回:
        dict: 润色结果
    """
    text = params.get("text", "")
    mode = params.get("mode", "polish")
    language = params.get("language", "auto")

    if not text.strip():
        return {"error": "请提供需要润色的文本"}

    if mode not in ("polish", "proofread", "paraphrase"):
        mode = "polish"

    return polish_text(text, mode, language)