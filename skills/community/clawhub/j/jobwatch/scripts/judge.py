#!/usr/bin/env python3
"""推理层：去重后的新岗位 → 硬过滤（script）→ LLM 对照 JOB_PROFILE 分级（Agent 判断）。

输出 Judgment: {doc_id, priority: P1/P2/P3, match, visa_risk, summary_zh, tags, reasons,
               judged_by, jd_tool}
分级映射由 script 钉死：kill_shot→P1（visa_risk=high 降 P2）、comfort_zone→P2、wrong_scene→P3。
LLM 判断失败 → 降级 P2 进日摘要（宁多看一眼，不漏 Kill Shot）。
"""
import json
import sys

from common import (CONFIG, ROOT, credential_for_endpoint, http_json,
                    require_egress_consent)


def llm_endpoint():
    """api 模式的 LLM 端点：任意 OpenAI 兼容服务（OpenRouter/OpenAI/vLLM/Ollama…）。

    base url: env LLM_BASE_URL > config judge.base_url > OpenRouter
    api key : 由 common.credential_for_endpoint() 按端点决定——LLM_API_KEY 是你为这个
              端点配的，会发过去；OPENROUTER_API_KEY / 宿主 OpenClaw 的 OpenRouter key
              只发给 OpenRouter，绝不跟着自定义 base_url 走。本地端点无 key 照常工作。
    """
    import os
    base = (os.environ.get("LLM_BASE_URL")
            or CONFIG["judge"].get("base_url")
            or "https://openrouter.ai/api/v1").rstrip("/")
    return base, credential_for_endpoint(base, purpose="judge")
from enrich_jd import fetch_jd

def _load_profile():
    from common import SKILL_DIR
    for p in (ROOT / "profile" / "JOB_PROFILE.md", SKILL_DIR / "profile.template.md"):
        if p.exists():
            return p.read_text()
    raise RuntimeError("profile not found")


PROFILE = _load_profile()

SYSTEM_PROMPT = f"""You are the judgment core of JobWatcher, a job-monitoring agent serving its user.
Evaluate ONE job posting against the user's profile below. Be decisive.

<job_profile>
{PROFILE}
</job_profile>

Classification rules:
- "kill_shot": strong overlap with the profile's Core Competencies AND no red lines hit
  (also respect the profile's Target Level / role-type preferences).
- "comfort_zone": related direction but partial match (generic backend/SRE/platform-adjacent),
  or kill-shot-level match with uncertain visa sponsorship.
- "wrong_scene": hits any red line listed in the profile or clearly unrelated to the profile.
- visa_risk: "high" only if the posting explicitly rules out sponsorship; "unknown" if silent.
- Posting age matters: if the posting has been open for over ~90 days, treat it as a
  possible ghost job / hard-to-fill role — cap at "comfort_zone" unless the match is
  exceptional, and mention the age concern in reasons.

Respond with ONLY a JSON object, no markdown fences:
{{"match": "kill_shot|comfort_zone|wrong_scene",
  "visa_risk": "low|medium|high|unknown",
  "summary_zh": "简体中文摘要，≤150字：这是什么岗位、核心要求、与用户画像的匹配点/差距",
  "tags": ["#3-5个标签，如 #MLInfra #K8s #Anthropic"],
  "reasons": "1-2句判断依据（中文）"}}"""


def prefilter(item):
    """Hard filter (script 侧确定性过滤). Returns True if worth LLM judgment."""
    t = item["title"].lower()
    pf = CONFIG["prefilter"]
    if any(k in t for k in pf["exclude_keywords"]):
        return False
    return any(k in t for k in pf["title_keywords"])


def posting_age_days(item):
    """从 posted_at/updated_at 估算岗位挂出天数（script 侧确定性计算）。"""
    import datetime, re
    raw = item.get("posted_at") or item.get("updated_at") or ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(raw))
    if not m:
        return None
    try:
        dt = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        return (datetime.date.today() - dt).days
    except ValueError:
        return None


def llm_judge(item, jd_text):
    age = posting_age_days(item)
    age_line = f"Posting age: {age} days\n" if age is not None else ""
    user = (age_line + f"Company: {item['company']}\nTitle: {item['title']}\n"
            f"Location: {item['location']}\nURL: {item['detail_url']}\n\n"
            f"Job description (may be truncated):\n{jd_text or '(JD unavailable — judge from title/location only)'}")
    base, key = llm_endpoint()
    require_egress_consent(
        "llm",
        f"the full job-description text and the full text of your JOB_PROFILE.md "
        f"(resume highlights, visa needs, seniority, red lines), to {base}",
    )
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    resp = http_json(
        f"{base}/chat/completions",
        method="POST",
        headers=headers,
        json_body={
            "model": CONFIG["judge"]["model"],
            "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                         {"role": "user", "content": user}],
            "temperature": 0.1,
            "max_tokens": 600,
        },
        timeout=120,
    )
    text = resp["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = text.strip("`").lstrip("json").strip()
    out = json.loads(text)
    assert out["match"] in ("kill_shot", "comfort_zone", "wrong_scene")
    return out


def to_priority(match, visa_risk):
    if match == "kill_shot":
        return "P2" if visa_risk == "high" else "P1"
    return "P2" if match == "comfort_zone" else "P3"


def judge_item(item):
    """Returns a Judgment dict. Never raises."""
    jd_text, jd_tool = fetch_jd(item["detail_url"]) if item.get("detail_url") else ("", "none")
    last_err = None
    for _ in range(2):  # one retry
        try:
            out = llm_judge(item, jd_text)
            return {
                "doc_id": item["doc_id"],
                "priority": to_priority(out["match"], out.get("visa_risk", "unknown")),
                "match": out["match"],
                "visa_risk": out.get("visa_risk", "unknown"),
                "summary_zh": out.get("summary_zh", ""),
                "tags": out.get("tags", []),
                "reasons": out.get("reasons", ""),
                "judged_by": CONFIG["judge"]["model"],
                "jd_tool": jd_tool,
                "jd_text": jd_text,
            }
        except Exception as e:  # noqa: BLE001
            last_err = str(e)[:300]
    return {  # 判断失败不静默：降级 P2
        "doc_id": item["doc_id"], "priority": "P2", "match": "judgment_failed",
        "visa_risk": "unknown",
        "summary_zh": f"（AI 判断失败，请人工确认）{item['company']} - {item['title']}",
        "tags": ["#JudgmentFailed"], "reasons": f"LLM error: {last_err}",
        "judged_by": CONFIG["judge"]["model"], "jd_tool": jd_tool, "jd_text": jd_text,
    }


if __name__ == "__main__":
    items = json.load(sys.stdin)
    results = [dict(judge_item(i), jd_text="<omitted>") for i in items]
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
