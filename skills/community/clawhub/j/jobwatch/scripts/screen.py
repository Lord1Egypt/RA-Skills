#!/usr/bin/env python3
"""Stage-1 标题筛 —— 借鉴 AI Digest 三段渐进打分的第一段。

抓 JD 之前，先用 LLM 对 title/company/location **批量**打分（0-10）对照 JOB_PROFILE，
低于阈值的岗位直接淘汰——避免为明显不合的岗位花 Firecrawl/Jina 抓取 + 全量判级。
这是最省钱的一段：大多数岗位在 title 就能判死，不必抓 JD。

设计要点：
- **后端无关**：复用 judge 的 OpenAI 兼容端点解析（LLM_BASE_URL / OpenRouter / 本地 Ollama）；
  Ollama 无需 key，可零成本跑。
- **批量**：一次调用筛一批标题（默认 18 个），省往返。
- **fail-open**：端点或解析失败时**保留该批全部**，绝不因筛选故障误杀岗位。
- **记用量**：每次调用回传 token 数，写进 pipeline summary，供成本核算（P1 成本项打底）。

只在 config.json 的 `screen.enabled=true` 时启用；默认关闭，行为与旧版一致。
"""
import json
import os

from common import (CONFIG, credential_for_endpoint, http_json,
                    require_egress_consent)
from judge import llm_endpoint, PROFILE

BATCH = 18  # 每次 LLM 调用筛多少个标题

SCREEN_SYS = """You are the fast title-screen of JobWatcher. For EACH job listed, score 0-10 how likely
the FULL posting is a strong match for the user's profile, judging from the TITLE / COMPANY / LOCATION alone.
Be strict: score 4+ only if plausibly relevant to the profile's core direction and target level; if it
clearly hits a red line or is unrelated, score 0-2. Do NOT fetch anything; judge from the given text only.
Return ONLY a JSON array, one object per job in the SAME order, no prose, no markdown fences:
[{"i": <index>, "score": <0-10>}]"""


def _screen_cfg():
    return CONFIG.get("screen", {}) or {}


def _profile_brief(maxchars=1200):
    """标题筛只需画像要点，截断以压低 prompt 成本。"""
    return (PROFILE or "")[:maxchars]


def _resolve_endpoint():
    """screen 端点：默认复用 judge 的解析；screen.base_url / screen.model 可单独覆盖
    （例如把 screen 指向本地 Ollama 做免费筛，judge 仍走云端）。

    覆盖了 base_url 就是**另一个端点**，不会把 judge/OpenRouter 的 key 顺手带过去：
    要凭证就单独配 SCREEN_LLM_API_KEY，指向本地模型则本来就不需要 key。
    """
    base, key = llm_endpoint()
    cfg = _screen_cfg()
    if cfg.get("base_url"):
        base = cfg["base_url"].rstrip("/")
        key = credential_for_endpoint(base, purpose="screen")
    model = cfg.get("model") or CONFIG["judge"]["model"]
    return base, key, model


def _screen_batch(items, base, key, model):
    lines = [f'{i}. {it["company"]} | {it["title"]} | {it.get("location", "")}'
             for i, it in enumerate(items)]
    user = f"USER PROFILE (brief):\n{_profile_brief()}\n\nJOBS:\n" + "\n".join(lines)
    require_egress_consent(
        "llm",
        f"a brief of your job profile plus {len(items)} company/title/location lines, to {base}",
    )
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    resp = http_json(
        f"{base}/chat/completions", method="POST", headers=headers,
        json_body={
            "model": model,
            "messages": [{"role": "system", "content": SCREEN_SYS},
                         {"role": "user", "content": user}],
            "temperature": 0,
            "max_tokens": 24 * len(items) + 60,
        },
        timeout=120,
    )
    text = resp["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.strip("`").lstrip("json").strip()
    arr = json.loads(text)
    scores = {int(o["i"]): float(o.get("score", 0)) for o in arr if "i" in o}
    return scores, resp.get("usage", {}) or {}


def screen_titles(items):
    """对候选岗位做 stage-1 标题筛。

    Returns (survivors, screened_out, usage_records)。
    - 未启用或空输入 → 原样返回全部为 survivors（向后兼容）。
    - 端点/解析失败 → 该批 fail-open 保留（不误杀）。
    每个 item 会被打上 `_screen`={"score":..,"threshold":..} 便于日志追溯。
    """
    cfg = _screen_cfg()
    if not cfg.get("enabled") or not items:
        return list(items), [], []

    threshold = float(cfg.get("threshold", 4))
    try:
        base, key, model = _resolve_endpoint()
    except Exception as e:  # noqa: BLE001
        for it in items:
            it["_screen"] = {"score": None, "note": f"endpoint-error: {str(e)[:80]}"}
        return list(items), [], []  # fail-open

    survivors, screened_out, usage_records = [], [], []
    for start in range(0, len(items), BATCH):
        chunk = items[start:start + BATCH]
        try:
            scores, usage = _screen_batch(chunk, base, key, model)
        except Exception as e:  # noqa: BLE001 —— fail-open：保留该批
            for it in chunk:
                it["_screen"] = {"score": None, "note": f"screen-error: {str(e)[:80]}"}
                survivors.append(it)
            usage_records.append({"stage": "screen", "n": len(chunk), "error": str(e)[:120]})
            continue
        usage_records.append({
            "stage": "screen", "n": len(chunk), "model": model,
            "input_tokens": usage.get("prompt_tokens"),
            "output_tokens": usage.get("completion_tokens"),
        })
        for j, it in enumerate(chunk):
            sc = scores.get(j)
            it["_screen"] = {"score": sc, "threshold": threshold}
            if sc is None or sc >= threshold:  # 无分数也保留（fail-open）
                survivors.append(it)
            else:
                screened_out.append(it)
    return survivors, screened_out, usage_records
