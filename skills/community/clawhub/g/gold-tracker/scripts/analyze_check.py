#!/usr/bin/env python3
"""分析日志硬校验器（反幻觉内容闸门，P0 核心价值 2）。

在智能体写完 logs/YYYY-MM-DD.yaml 后、宣布「分析完成」前 MUST 运行。
任意一条 ERROR 都以非零退出码拒绝本次分析。

校验内容:
  1. 结构：run_id / timestamp / price_data / summary.focus / key_factors / sources 齐全
  2. impact 枚举、factor 字段、factor 数量（config.output.constraints）
  3. sources URL 格式 + 命中 fetch_log + 域名多样性
  4. 反幻觉措辞（forbidden_phrases）+ 占位规范（no_data_marker）

用法:
    python3 scripts/analyze_check.py
    python3 scripts/analyze_check.py logs/2026-07-28.yaml
    python3 scripts/analyze_check.py --strict
"""

import sys
from pathlib import Path
from urllib.parse import urlparse

from common import paths, config, yamlmini

errors = []
warnings = []


def err(msg):
    errors.append(msg)
    print("  [✗] {}".format(msg))


def warn(msg):
    warnings.append(msg)
    print("  [!] {}".format(msg))


def is_valid_url(u):
    if not isinstance(u, str) or not u:
        return False
    try:
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def load_fetch_log():
    f = paths.resolve("cache") / "fetch_log.json"
    if not f.exists():
        return {"urls": set(), "domains": set()}
    try:
        import json
        data = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return {
                "urls": {e["url"] for e in data if e.get("url")},
                "domains": {e.get("domain", urlparse(e["url"]).netloc)
                            for e in data if e.get("url")},
            }
    except Exception:
        pass
    return {"urls": set(), "domains": set()}


def check(doc, cfg, fetch, file_name):
    prefix = "{}: ".format(file_name)
    constr = cfg.get("output", {}).get("constraints", {})
    src_cfg = constr.get("sources", {})
    min_factors = cfg.get("output", {}).get("min_factors_per_analysis", 2)
    max_factors = cfg.get("output", {}).get("max_factors_per_analysis", 6)
    allowed_impacts = constr.get("allowed_impacts", [])
    required_fields = constr.get("required_factor_fields", [])
    forbidden = constr.get("forbidden_phrases", [])
    no_data = constr.get("no_data_marker", "no_data")

    # 1. 顶层必填字段
    for f in ["run_id", "timestamp", "price_data", "summary", "key_factors", "sources"]:
        if f not in doc:
            err("{}缺少顶层字段: {}".format(prefix, f))

    if isinstance(doc.get("summary"), dict) and not doc["summary"].get("focus"):
        err("{}summary.focus 不能为空".format(prefix))

    # 2. key_factors 数量与字段
    factors = doc.get("key_factors")
    if not isinstance(factors, list):
        err("{}key_factors 必须是列表".format(prefix))
        factors = []
    else:
        n = len(factors)
        if n < min_factors:
            err("{}key_factors 数量 {} < 最小 {}".format(prefix, n, min_factors))
        if n > max_factors:
            err("{}key_factors 数量 {} > 最大 {}".format(prefix, n, max_factors))

    all_sources_urls = []
    for idx, fac in enumerate(factors):
        if not isinstance(fac, dict):
            err("{}key_factors[{}] 不是 dict".format(prefix, idx))
            continue
        fp = "{}key_factors[{}]".format(prefix, idx)
        for field in required_fields:
            if field not in fac:
                err("{}: 缺少字段 {}".format(fp, field))

        impact = fac.get("impact")
        if impact and impact not in allowed_impacts:
            err("{}: impact='{}' 不在允许枚举内 {}".format(fp, impact, allowed_impacts))

        reasoning = fac.get("reasoning", "")
        if reasoning and no_data not in str(reasoning):
            for phrase in forbidden:
                if phrase in str(reasoning):
                    err("{}: reasoning 含禁用措辞 '{}'".format(fp, phrase))

        fac_sources = fac.get("sources", [])
        if isinstance(fac_sources, str):
            fac_sources = [fac_sources]
        if not isinstance(fac_sources, list):
            fac_sources = []
        min_per = src_cfg.get("min_count_per_factor", 1)
        if len(fac_sources) < min_per:
            err("{}: sources 数量 {} < 最小 {}".format(fp, len(fac_sources), min_per))
        all_sources_urls.extend(fac_sources)

    # 3. 顶层 sources
    top_sources = doc.get("sources", [])
    if isinstance(top_sources, str):
        top_sources = [top_sources]
    if not isinstance(top_sources, list):
        top_sources = []
    all_sources_urls.extend(top_sources)

    if not all_sources_urls:
        err("{}整篇分析没有任何 source URL".format(prefix))
    else:
        valid_urls = []
        for s in all_sources_urls:
            if src_cfg.get("must_be_http_url", True) and not is_valid_url(s):
                err("{}非法 source URL: {!r}".format(prefix, s))
            else:
                valid_urls.append(s)

        if src_cfg.get("must_be_in_fetch_log", True):
            fetch_urls = fetch["urls"]
            if not fetch_urls:
                warn("{}fetch_log 为空 —— 请确认已用 log_fetch.py 记录 web_fetch".format(prefix))
            for s in valid_urls:
                if s not in fetch_urls:
                    err("{}source URL 未出现在 fetch_log 中（即未实际抓取过）: {}".format(prefix, s))

        domains = set()
        for s in valid_urls:
            try:
                domains.add(urlparse(s).netloc)
            except Exception:
                pass
        min_domains = src_cfg.get("min_unique_domains", 2)
        if len(domains) < min_domains:
            err("{}来源覆盖 {} 个独立域名 < 最小 {}（防止单源依赖）".format(
                prefix, len(domains), min_domains))

    # 4. summary.focus 反幻觉
    summary = doc.get("summary", {})
    if isinstance(summary, dict):
        focus = str(summary.get("focus", ""))
        for phrase in forbidden:
            if phrase in focus:
                err("{}summary.focus 含禁用措辞 '{}'".format(prefix, phrase))


def find_latest_log():
    d = paths.resolve("logs")
    if not d.exists():
        return None
    candidates = sorted([f for f in d.iterdir() if f.suffix in (".yaml", ".yml")],
                        key=lambda f: f.name, reverse=True)
    return candidates[0] if candidates else None


def main():
    paths.ensure_env()
    strict = "--strict" in sys.argv
    target = None
    for a in sys.argv[1:]:
        if not a.startswith("--"):
            target = a
            break

    if target:
        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = paths.ROOT / target_path
    else:
        target_path = find_latest_log()

    print("=" * 56)
    print("黄金追踪 - 分析日志硬校验")
    print("=" * 56)

    if not target_path or not target_path.exists():
        print("[错误] 未找到待校验日志: {}".format(target))
        sys.exit(2)

    print("校验目标: {}\n".format(target_path.relative_to(paths.ROOT)))

    cfg = config.load()
    fetch = load_fetch_log()

    text = target_path.read_text(encoding="utf-8")
    docs = yamlmini.load_all(text)
    last_doc = docs[-1] if docs else {}

    if not last_doc:
        err("解析结果为空")
    else:
        check(last_doc, cfg, fetch, target_path.name)

    print()
    print("=" * 56)
    print("结果: {} 个错误, {} 个警告".format(len(errors), len(warnings)))
    print("=" * 56)

    if errors or (strict and warnings):
        print("[拒绝] 本次分析未通过硬校验 —— 修复后重新写日志并再次运行")
        sys.exit(1)
    print("[通过] 所有硬约束满足，可以宣布分析完成")


if __name__ == "__main__":
    main()
