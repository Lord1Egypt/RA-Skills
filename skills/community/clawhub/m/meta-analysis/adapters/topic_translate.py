#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""topic_translate.py — 中文研究主题 → 英文检索词（供 Europe PMC 检索接地）。

WHY THIS EXISTS
---------------
Europe PMC 只索引**英文摘要**；把中文主题原样送去检索几乎必然 0 命中，而这会被
误读成「该方向没人做过（=新颖选题）」——一个足以带偏选题的**假信号**。

在**技能（Agent）上下文**里，LLM 就在回路中，翻译是天然能力；但网页端的 FastAPI
服务是**独立进程**，Agent 不在回路里，所以此前只能要求用户手填「英文题名」——等于
把机器该干的活推给用户。本模块把同一条能力补进服务端：复用 WorkBuddy 本机的
**OpenAI 兼容模型端点**（`~/.workbuddy/models.json`，或 `LLM_BASE_URL`/`OPENAI_BASE_URL`
环境变量）做一次极小的翻译调用，使网页端也能**自动翻译关键词**。

设计约束（与 literature_probe 一致）
------------------------------------
- **零第三方依赖**：只用标准库（urllib / json / hashlib / os / re / time）。
- **不臆造、可核对**：翻译结果回传给前端展示，用户可改；检索式随之可见。
- **失败即降级**：任何异常（无端点 / 超时 / 限流 / 输出不像英文）一律返回 None，
  由调用方回退到「显式索要英文检索词」路径，绝不抛错中断流程。
- **缓存**：同一主题只翻一次（进程内 + 磁盘），省 token、避开限流。

端点解析优先级：META_WB_TRANSLATE_* / LLM_* 环境变量 → models.json（按候选梯队）→ 无。
"""
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request

# 候选模型梯队（本地开发：models.json 里按「快 + 稳定 + 便宜」排序）。实测 2026-09-22：
# 三者均能给出完全一致的高质量英文检索式；deepseek-v4-flash 最快（~1.3s）。
# 注意：部分模型是 reasoning 模型，max_tokens 太小会把预算耗在思考上导致
# content 为空 —— 故 _MAX_TOKENS 必须留足（见下）。
# ⚠️ 发布为应用时（云端 sandbox 无 models.json）改走 ct-base §12 的 LongCat-2.0 兜底
#    （见 _longcat_candidate），家族统一收敛到该模型 + 共享混淆 key。
_CANDIDATE_IDS = ("deepseek-v4-flash", "qwen3.8-max", "LongCat-2.0")
_MAX_TOKENS = 512          # 不是 80：reasoning 模型会先吃掉预算，80 会返回空串
_TIMEOUT = 25
_MAX_INPUT = 600           # 超长主题不翻（保护 token / 属异常输入）

# ct-base §12：发布后应用后台大模型统一 LongCat-2.0 的固定端点（OpenAI 兼容）。
# apiKeyEnv / apiKeyFile 契约见 ct-base/workbench/workbench.config.schema.json backend.llm。
_LC_BASE = "https://api.longcat.chat/openai"
_LC_MODEL = "LongCat-2.0"
_LC_KEY_ENV = "LONGCAT_API_KEY"
# config/llm_key.py 相对本文件（adapters/topic_translate.py）的位置。
_LC_KEY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "llm_key.py")
_LC_MEM = {"tried": False, "value": ""}   # 进程内缓存解码结果（含失败），避免每次重试磁盘 IO


def _longcat_candidate():
    """返回 LongCat-2.0 的 (base, key, model) 或 None。

    key 经 ct-base load_llm_key()：环境变量 LONGCAT_API_KEY 优先（生产注入），
    否则读混淆 config/llm_key.py（随载荷走）。解码一次即缓存，失败不反复重试。
    """
    if _LC_MEM["tried"]:
        return (_LC_BASE.rstrip("/") + "/chat/completions", _LC_MEM["value"], _LC_MODEL) \
            if _LC_MEM["value"] else None
    _LC_MEM["tried"] = True
    try:
        from llm_loader import load_llm_key      # 与 topic_translate 同目录（adapters/）
        _LC_MEM["value"] = load_llm_key(env_name=_LC_KEY_ENV, key_path=_LC_KEY_FILE) or ""
    except Exception:  # noqa: BLE001 - 无 key → 不产出该候选，交由其它候选/降级
        _LC_MEM["value"] = ""
    return (_LC_BASE.rstrip("/") + "/chat/completions", _LC_MEM["value"], _LC_MODEL) \
        if _LC_MEM["value"] else None

_SYS = ("You are a medical librarian. Translate the given Chinese research topic "
        "into a concise English literature-search query: key medical terms only, "
        "no quotes, no explanation, no trailing period. "
        "Output ONLY the query on a single line.")


def has_cjk(text):
    """True 若 text 含中日韩（CJK）字符 —— 用于判断是否需要翻译。"""
    if not text:
        return False
    return bool(re.search(r"[\u3400-\u9fff\uf900-\ufaff\uff00-\uffef\u3040-\u30ff]", text))


def _local_dir():
    base = os.environ.get("META_WB_LOCAL_DIR")
    if base:
        return os.path.abspath(base)
    la = (os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP")
          or os.path.expanduser("~"))
    return os.path.join(la, "meta-analysis-wb")


def _cache_path():
    return os.path.join(_local_dir(), "translate_cache.json")


def _load_cache():
    try:
        with open(_cache_path(), "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save_cache(cache):
    try:
        p = _cache_path()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        pass  # 缓存写失败不影响功能


_MEM_CACHE = {}


def _cache_key(text):
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()


def _models():
    """读 WorkBuddy 自定义模型列表（~/.workbuddy/models.json）。"""
    path = os.environ.get("WORKBUDDY_MODELS_JSON") or os.path.expanduser(
        "~/.workbuddy/models.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("models"), list):
        return data["models"]
    return []


def _endpoint_of(m):
    url = (m.get("url") or "").strip()
    if not url:
        return None
    base = url if url.endswith("/chat/completions") else url.rstrip("/") + "/chat/completions"
    return base, m.get("apiKey") or "", m.get("id") or m.get("name") or ""


def _candidates():
    """按优先级返回候选端点 [(base, key, model_id), ...]。"""
    out = []
    # 1) 环境变量显式指定（最高优先）
    env_base = os.environ.get("META_WB_TRANSLATE_BASE_URL") or os.environ.get("LLM_BASE_URL") \
        or os.environ.get("OPENAI_BASE_URL")
    env_key = os.environ.get("META_WB_TRANSLATE_API_KEY") or os.environ.get("LLM_API_KEY") \
        or os.environ.get("OPENAI_API_KEY")
    env_model = os.environ.get("META_WB_TRANSLATE_MODEL") or os.environ.get("LLM_MODEL")
    if env_base and env_model:
        b = env_base if env_base.endswith("/chat/completions") else env_base.rstrip("/") + "/chat/completions"
        out.append((b, env_key or "", env_model))
    # 2) models.json：先按候选梯队，再补充其余有 url 的模型
    ms = _models()
    by_id = {}
    for m in ms:
        ep = _endpoint_of(m)
        if ep:
            by_id[m.get("id") or m.get("name")] = ep
    for mid in _CANDIDATE_IDS:
        if mid in by_id:
            out.append(by_id.pop(mid))
    for mid, ep in by_id.items():
        out.append(ep)
    # 3) ct-base §12：LongCat-2.0 兜底候选 —— 排在最后，本地（models.json 命中更快源）
    #    行为不变；但发布为应用后 sandbox 无 models.json，models.json 那两路都空，
    #    只剩这一个 → 后台翻译自动收敛到 LongCat-2.0（家族统一约定）。
    _lc = _longcat_candidate()
    if _lc:
        out.append(_lc)
    # 去重（同 base+model）
    seen, uniq = set(), []
    for base, key, model in out:
        k = (base, model)
        if k not in seen:
            seen.add(k)
            uniq.append((base, key, model))
    return uniq


def _strip_noise(text):
    """清掉模型常见的包装：引号、`English:` 前缀、多余换行/句点。"""
    s = (text or "").strip()
    # 取第一行非空内容（模型偶尔带解释行）
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    if lines:
        s = lines[0]
    s = re.sub(r'^(english|query|translation|search query)\s*[:：]\s*', '', s, flags=re.I)
    s = s.strip().strip('"\'“”‘’`')
    s = s.rstrip("。.").strip()
    return s


def _looks_english(s):
    """输出必须真像英文检索式：非空、有拉丁字母、无 CJK、不是拒答。"""
    if not s or len(s) < 2 or len(s) > 300:
        return False
    if has_cjk(s):
        return False
    if not re.search(r"[A-Za-z]{2,}", s):
        return False
    low = s.lower()
    for bad in ("sorry", "cannot", "can't", "unable", "as an ai"):
        if low.startswith(bad):
            return False
    return True


def _call(base, key, model, text, timeout=_TIMEOUT, system=None, raw=False):
    """调一次 chat/completions。

    system：覆盖默认的检索式翻译提示词（界面文案批量翻译用，见 translate_ui_texts）。
    raw=True：**原样返回** content —— 批量 JSON 输出绝不能再过 _strip_noise
      （它会去引号 / 只取首行，会把 JSON 对象切坏）。
    """
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system or _SYS},
                     {"role": "user", "content": text}],
        "temperature": 0,
        "max_tokens": (_UI_MAX_TOKENS if raw else _MAX_TOKENS),
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(base, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    content = (j.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    return content if raw else _strip_noise(content)


def translate_to_english(text, timeout=_TIMEOUT, use_cache=True):
    """把中文研究主题翻成英文检索式。

    Returns:
        str  英文检索式（已清洗、已校验）
        None 无可用端点 / 全部候选失败 / 输出不合规 → 调用方降级（索要英文检索词）
    """
    t = (text or "").strip()
    if not t or not has_cjk(t) or len(t) > _MAX_INPUT:
        return None

    ck = _cache_key(t)
    if use_cache:
        if ck in _MEM_CACHE:
            return _MEM_CACHE[ck]
        cache = _load_cache()
        hit = cache.get(ck)
        if hit and _looks_english(hit.get("en") or ""):
            _MEM_CACHE[ck] = hit["en"]
            return hit["en"]

    for base, key, model in _candidates():
        try:
            out = _call(base, key, model, t, timeout=timeout)
        except Exception:  # noqa: BLE001 - 逐个候选降级，绝不抛错
            continue
        if _looks_english(out):
            _MEM_CACHE[ck] = out
            if use_cache:
                cache = _load_cache()
                cache[ck] = {"en": out, "model": model, "ts": int(time.time())}
                _save_cache(cache)
            return out
    return None


# ---------------------------------------------------------------------------
# 界面文案批量翻译（2026-09-22，一致性审计 P2-10）
#
# 背景：网页语言开关原本只替换顶栏 11 个框架串，EN 模式下节点标题 / intro / 面板标签
# 全是中文；而 CLI 侧（flow_menu._T + form_schema.TITLE_EN）是真双语 → 两侧不对等。
# 与其手写上百条英文（且必然与中文原文漂移），不如复用**已有的翻译通道**：
# 同一批端点、同一套磁盘缓存；失败则整体回落中文并由前端显式提示（不静默半翻译）。
# ---------------------------------------------------------------------------
_UI_SYS = (
    "You are a professional localizer for a scientific desktop application: a systematic-review / "
    "meta-analysis workbench used by medical researchers. You receive a JSON object whose values "
    "are Simplified-Chinese UI strings. Translate EVERY value into concise, natural, professional "
    "English.\n"
    "Rules:\n"
    "  - Preserve Markdown emphasis (**bold**), list markers, numbering and line breaks.\n"
    "  - Keep numbers, units, statistical symbols and proper names unchanged "
    "(I², τ², OR, RR, SMD, RoB, GRADE, PRISMA, PICOS, PDF, Excel, DOI, R, metafor, netmeta, coze).\n"
    "  - Keep file extensions, file paths and code identifiers unchanged.\n"
    "  - Do not add explanations, do not omit information, do not merge or split entries.\n"
    "Return ONLY the JSON object with the SAME keys and translated values. "
    "No prose, no code fences."
)
_UI_BATCH = 40          # 单次请求最多翻多少条
_UI_KEY = "ui:"         # 缓存键命名空间：与主题检索式翻译分开，互不覆盖
# 批量 JSON 输出的 token 预算。实测 40 条约 3300 completion tokens —— 旧的 3000
# 会**截断成残缺 JSON**（finish_reason=length），解析必然失败，白跑一轮候选。
_UI_MAX_TOKENS = 8000
_UI_MAX_CHARS = 1600    # 单批字符预算（长 intro 段落会把输出撑长，光限条数不够）
_UI_BUDGET = 90.0       # 整次调用的时间预算（秒）：无论怎么失败都不会卡住语言开关


def _loads_json_obj(raw):
    """把模型输出解析成 dict；容忍 ```json 围栏与前后寒暄。失败返回 {}。"""
    s = (raw or "").strip()
    if not s:
        return {}
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*", "", s)
        s = re.sub(r"```\s*$", "", s).strip()
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j <= i:
        return {}
    try:
        d = json.loads(s[i:j + 1])
    except Exception:  # noqa: BLE001
        return {}
    return d if isinstance(d, dict) else {}


def _ui_chunks(items):
    """按「条数上限 + 字符预算」切批：两者任一超了就断开。

    只限条数不够 —— 40 条里要塞进几条 400 字的长 intro，输出 token 会翻倍。
    """
    cur, n = [], 0
    for t in items:
        if cur and (n + len(t) > _UI_MAX_CHARS or len(cur) >= _UI_BATCH):
            yield cur
            cur, n = [], 0
        cur.append(t)
        n += len(t)
    if cur:
        yield cur


def _ui_translate_chunk(chunk, timeout, deadline):
    """翻一批 → `(got, model)`；全候选失败返回 `({}, "")`。

    关键：若**拿到了内容却解析不出 JSON**，最可能是被 max_tokens 截断 —— 换模型
    多半同样截断，徒增耗时（旧实现因此一次 EN 切换要 603 秒）。此时直接返回失败，
    由上层二分重试；只有「请求本身出错」才继续换候选。
    """
    user = json.dumps({str(n): v for n, v in enumerate(chunk)}, ensure_ascii=False)
    for base, key, model in _candidates():
        if time.time() > deadline:
            return {}, ""
        try:
            raw = _call(base, key, model, user, timeout=timeout,
                        system=_UI_SYS, raw=True)
        except Exception:  # noqa: BLE001 - 逐个候选降级
            continue
        got = _loads_json_obj(raw)
        if got:
            return got, model
        if (raw or "").strip():
            return {}, ""       # 有内容但解析失败（截断）→ 交给上层二分
    return {}, ""


def translate_ui_texts(texts, timeout=_TIMEOUT, use_cache=True):
    """批量把界面文案（zh → en）翻译，**键值一一对应**。

    Args:
        texts: 待翻译的串序列（可含英文串 —— 无 CJK 的直接原样返回，不占额度）。

    Returns:
        dict{原文: 英文}。只收「成功翻到且合规」的条目（译者没翻好 / 译文仍含中文 → 不收）。
        无可用端点或整批失败 → 该批键缺失（调用方回落中文，并据此提示用户，不静默半翻译）。
    """
    out, todo = {}, []
    for t in dict.fromkeys(texts or []):
        if not isinstance(t, str) or not t.strip():
            continue
        if not has_cjk(t):                 # 已是英文 → 无需翻译
            out[t] = t
            continue
        todo.append(t)

    cache = _load_cache() if use_cache else {}
    pending = []
    for t in todo:
        ck = _UI_KEY + _cache_key(t)
        rec = cache.get(ck)
        if use_cache and isinstance(rec, dict) and isinstance(rec.get("en"), str):
            out[t] = rec["en"]
        else:
            pending.append(t)

    deadline = time.time() + _UI_BUDGET
    queue = list(_ui_chunks(pending))
    guard = 0
    while queue and guard < 512 and time.time() < deadline:
        guard += 1
        chunk = queue.pop(0)
        got, used = _ui_translate_chunk(chunk, timeout, deadline)
        if not got:
            if len(chunk) > 1:
                # 二分重试：截断的批切半后就能塞进预算（取序号键的好处：切批不破坏对应）
                mid = len(chunk) // 2
                queue.insert(0, chunk[mid:])
                queue.insert(0, chunk[:mid])
            continue                        # 单条仍失败 → 该串回落中文
        for n, src in enumerate(chunk):
            en = got.get(str(n))
            if not isinstance(en, str) or not en.strip() or has_cjk(en):
                continue                    # 译文仍含中文 / 空 = 没翻干净 → 宁可回落
            en = en.strip()
            out[src] = en
            if use_cache:
                cache[_UI_KEY + _cache_key(src)] = {
                    "en": en, "model": used, "ts": int(time.time())}
    if use_cache and pending:
        _save_cache(cache)
    return out


if __name__ == "__main__":
    import sys
    arg = " ".join(sys.argv[1:]) or "SGLT2 抑制剂在慢性肾脏病（CKD）中的肾保护与心血管获益"
    print("input :", arg)
    print("candidates:", [(m, b) for b, k, m in _candidates()])
    print("output:", translate_to_english(arg, use_cache=False))
