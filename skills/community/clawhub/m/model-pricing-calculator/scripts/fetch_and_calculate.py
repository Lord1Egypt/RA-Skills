#!/usr/bin/env python3
"""
模型定价数据抓取与倍率计算脚本

从配置的网站 API 获取模型定价数据，计算模型倍率、补全倍率和分组倍率，
按统一格式输出，并自动保存快照用于下次对比变更。

用法:
    python fetch_and_calculate.py [--urls-file <path>] [--output-dir <path>]

无外部依赖，仅使用 Python 标准库。
"""

import argparse
import json
import os
import ssl
import sys
import urllib.request
import urllib.error
from collections import OrderedDict
from datetime import datetime

# 基准价格常量
BASE_PRICE_PER_1K = 0.002  # $0.002 / 1K tokens
QUOTA_PER_DOLLAR = 500000  # 1 USD = 500,000 quota

# 快照文件名
SNAPSHOT_FILENAME = "latest_snapshot.json"


def load_urls(urls_file):
    """从 JSON 文件加载网站 URL 配置"""
    with open(urls_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config.get("urls", [])


def fetch_pricing_data(api_endpoint, timeout=30):
    """从 API 端点获取定价数据"""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            api_endpoint,
            headers={"User-Agent": "ModelPricingCalculator/1.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        print(f"警告: 无法从 {api_endpoint} 获取数据: {e}", file=sys.stderr)
        return None


def extract_models(raw_data):
    """从原始 API 数据中提取模型列表"""
    if isinstance(raw_data, dict):
        return raw_data.get("data", [])
    if isinstance(raw_data, list):
        return raw_data
    return []


def extract_group_ratio(raw_data):
    """从原始 API 数据中提取分组倍率"""
    if isinstance(raw_data, dict):
        return raw_data.get("group_ratio", {})
    return {}


def calculate_ratios(models_list):
    """
    从模型列表中计算模型倍率和补全倍率。

    返回:
        model_ratios: {model_name: ratio}
        completion_ratios: {model_name: ratio}
        fixed_price_models: {model_name: price}
    """
    model_ratios = OrderedDict()
    completion_ratios = OrderedDict()
    fixed_price_models = OrderedDict()

    for m in models_list:
        name = m.get("model_name", "")
        if not name:
            continue

        quota_type = m.get("quota_type", 0)
        model_ratio = m.get("model_ratio", 0)
        completion_ratio = m.get("completion_ratio", 0)
        model_price = m.get("model_price", 0)

        if quota_type == 1 and model_price > 0:
            fixed_price_models[name] = model_price
        else:
            if model_ratio > 0:
                model_ratios[name] = model_ratio
                if completion_ratio > 0:
                    completion_ratios[name] = completion_ratio

    return model_ratios, completion_ratios, fixed_price_models


def compute_actual_prices(model_name, model_ratio, completion_ratio, group_ratio=1.0):
    """根据倍率计算实际价格"""
    input_price = BASE_PRICE_PER_1K * model_ratio * group_ratio
    output_price = input_price * completion_ratio
    return input_price, output_price


def reverse_calculate(input_price_per_1k, output_price_per_1k):
    """从目标售价反推配置值"""
    model_ratio = input_price_per_1k / BASE_PRICE_PER_1K
    completion_ratio = output_price_per_1k / input_price_per_1k if input_price_per_1k > 0 else 0
    return model_ratio, completion_ratio


def match_pattern(name, pattern):
    """支持通配符 * 的简单模式匹配"""
    import fnmatch
    return fnmatch.fnmatchcase(name, pattern) or fnmatch.fnmatchcase(name.lower(), pattern.lower())


def filter_by_patterns(data_dict, patterns_str):
    """
    根据逗号分隔的模式字符串过滤字典。
    支持通配符 *，如 'gpt-4*,claude-*'。
    返回过滤后的 OrderedDict。
    """
    if not patterns_str:
        return data_dict
    patterns = [p.strip() for p in patterns_str.split(",") if p.strip()]
    if not patterns:
        return data_dict
    filtered = OrderedDict()
    for key, value in data_dict.items():
        for pat in patterns:
            if match_pattern(key, pat):
                filtered[key] = value
                break
    return filtered


def format_output(model_ratios, completion_ratios, group_ratios):
    """严格按照指定格式输出三个 JSON 块"""
    output = []
    output.append("（1）模型倍率")
    output.append(json.dumps(model_ratios, indent=2, ensure_ascii=False))

    output.append("（2）模型补全倍率")
    output.append(json.dumps(completion_ratios, indent=2, ensure_ascii=False))

    output.append("（3）分组倍率")
    output.append(json.dumps(group_ratios, indent=2, ensure_ascii=False))

    return "\n".join(output)


# ============================================================
# 快照存储与差异对比
# ============================================================

def get_snapshot_path(skill_dir):
    """获取快照文件路径: data/latest_snapshot.json"""
    data_dir = os.path.join(skill_dir, "data")
    return os.path.join(data_dir, SNAPSHOT_FILENAME)


def load_snapshot(snapshot_path):
    """加载上一次保存的快照数据，不存在则返回 None"""
    if not os.path.exists(snapshot_path):
        return None
    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_snapshot(snapshot_path, model_ratios, completion_ratios, group_ratios):
    """保存当前数据为快照（覆盖旧文件）"""
    os.makedirs(os.path.dirname(snapshot_path), exist_ok=True)
    snapshot = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_ratios": dict(model_ratios),
        "completion_ratios": dict(completion_ratios),
        "group_ratios": dict(group_ratios),
    }
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)


def diff_dict(old_dict, new_dict):
    """
    对比两个字典，返回差异:
        added:   新增的 key -> new_value
        removed: 删除的 key -> old_value
        changed: 值变化的 key -> (old_value, new_value)
    """
    old_keys = set(old_dict.keys())
    new_keys = set(new_dict.keys())

    added = {k: new_dict[k] for k in sorted(new_keys - old_keys)}
    removed = {k: old_dict[k] for k in sorted(old_keys - new_keys)}
    changed = {}
    for k in sorted(old_keys & new_keys):
        if old_dict[k] != new_dict[k]:
            changed[k] = (old_dict[k], new_dict[k])

    return added, removed, changed


def format_diff_section(title, old_data, new_data):
    """格式化单个类别的差异输出"""
    added, removed, changed = diff_dict(old_data, new_data)

    if not added and not removed and not changed:
        return f"  {title}: 无变化\n"

    lines = [f"  {title}:"]

    if added:
        lines.append(f"    【新增 {len(added)} 项】")
        for k, v in added.items():
            lines.append(f"      + {k}: {v}")

    if removed:
        lines.append(f"    【删除 {len(removed)} 项】")
        for k, v in removed.items():
            lines.append(f"      - {k}: {v}")

    if changed:
        lines.append(f"    【数值变化 {len(changed)} 项】")
        for k, (old_v, new_v) in changed.items():
            lines.append(f"      * {k}: {old_v} → {new_v}")

    return "\n".join(lines) + "\n"


def print_diff_report(old_snapshot, new_model_ratios, new_completion_ratios, new_group_ratios):
    """输出与上次快照的完整差异报告"""
    old_mr = old_snapshot.get("model_ratios", {})
    old_cr = old_snapshot.get("completion_ratios", {})
    old_gr = old_snapshot.get("group_ratios", {})
    saved_at = old_snapshot.get("saved_at", "未知时间")

    # 检查是否有任何变化
    mr_added, mr_removed, mr_changed = diff_dict(old_mr, dict(new_model_ratios))
    cr_added, cr_removed, cr_changed = diff_dict(old_cr, dict(new_completion_ratios))
    gr_added, gr_removed, gr_changed = diff_dict(old_gr, dict(new_group_ratios))

    has_any_diff = any([
        mr_added, mr_removed, mr_changed,
        cr_added, cr_removed, cr_changed,
        gr_added, gr_removed, gr_changed,
    ])

    report = []
    report.append("=" * 60)
    report.append(f"与上次数据对比（上次保存时间: {saved_at}）")
    report.append("=" * 60)

    if not has_any_diff:
        report.append("  所有数据与上次完全一致，无任何变化。")
    else:
        report.append(format_diff_section("模型倍率", old_mr, dict(new_model_ratios)))
        report.append(format_diff_section("模型补全倍率", old_cr, dict(new_completion_ratios)))
        report.append(format_diff_section("分组倍率", old_gr, dict(new_group_ratios)))

    print("\n".join(report))


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="模型定价数据抓取与倍率计算")
    parser.add_argument(
        "--urls-file",
        default=None,
        help="网站 URL 配置文件路径（JSON）。默认使用 references/pricing_urls.json"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="输出目录。如指定，结果会额外保存为独立 JSON 文件"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="打印价格验证表"
    )
    parser.add_argument(
        "--no-snapshot",
        action="store_true",
        help="不保存快照、不对比差异"
    )
    parser.add_argument(
        "--models",
        default=None,
        help="按模型名称过滤，多个用逗号分隔，支持通配符 *（如 'gpt-4*,claude-*'）"
    )
    parser.add_argument(
        "--groups",
        default=None,
        help="按分组名称过滤，多个用逗号分隔，支持通配符 *（如 'default,aws*'）"
    )
    parser.add_argument(
        "--source",
        default=None,
        help="按数据来源名称过滤，多个用逗号分隔，支持通配符 *（如 'PackyAPI' 或 '12AI,Packy*'）。"
             "名称对应 pricing_urls.json 中的 name 字段"
    )
    args = parser.parse_args()

    # 定位目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)

    if args.urls_file:
        urls_file = args.urls_file
    else:
        urls_file = os.path.join(skill_dir, "references", "pricing_urls.json")

    if not os.path.exists(urls_file):
        print(f"错误: 找不到 URL 配置文件: {urls_file}", file=sys.stderr)
        sys.exit(1)

    urls_config = load_urls(urls_file)
    if not urls_config:
        print("错误: URL 配置文件为空", file=sys.stderr)
        sys.exit(1)

    # 汇总所有来源数据
    all_model_ratios = OrderedDict()
    all_completion_ratios = OrderedDict()
    all_fixed_price_models = OrderedDict()
    all_group_ratios = OrderedDict()

    # 解析 --source 过滤模式
    source_patterns = None
    if args.source:
        source_patterns = [p.strip() for p in args.source.split(",") if p.strip()]

    for site in urls_config:
        name = site.get("name", "Unknown")
        api_url = site.get("api_endpoint", "")
        if not api_url:
            print(f"跳过 {name}: 无 API 端点", file=sys.stderr)
            continue

        # 按来源名称过滤
        if source_patterns:
            matched = any(match_pattern(name, pat) for pat in source_patterns)
            if not matched:
                print(f"跳过 {name}: 不匹配 --source 过滤条件", file=sys.stderr)
                continue

        print(f"正在从 {name} ({api_url}) 获取数据...", file=sys.stderr)
        raw = fetch_pricing_data(api_url)
        if raw is None:
            continue

        models_list = extract_models(raw)
        group_ratio = extract_group_ratio(raw)
        mr, cr, fp = calculate_ratios(models_list)

        for k, v in mr.items():
            if k not in all_model_ratios:
                all_model_ratios[k] = v
        for k, v in cr.items():
            if k not in all_completion_ratios:
                all_completion_ratios[k] = v
        for k, v in fp.items():
            if k not in all_fixed_price_models:
                all_fixed_price_models[k] = v
        for k, v in group_ratio.items():
            if k not in all_group_ratios:
                all_group_ratios[k] = v

    # 按名称排序
    sorted_model_ratios = OrderedDict(sorted(all_model_ratios.items()))
    sorted_completion_ratios = OrderedDict(sorted(all_completion_ratios.items()))
    sorted_group_ratios = OrderedDict(sorted(all_group_ratios.items()))

    # ---- 按指定模型/分组过滤 ----
    is_filtered = bool(args.models or args.groups or args.source)
    if args.models:
        sorted_model_ratios = filter_by_patterns(sorted_model_ratios, args.models)
        sorted_completion_ratios = filter_by_patterns(sorted_completion_ratios, args.models)
    if args.groups:
        sorted_group_ratios = filter_by_patterns(sorted_group_ratios, args.groups)

    # ---- 输出三个 JSON 块 ----
    result = format_output(sorted_model_ratios, sorted_completion_ratios, sorted_group_ratios)
    print(result)

    # ---- 差异对比 + 快照保存（仅在非过滤模式下执行） ----
    if not args.no_snapshot and not is_filtered:
        # 过滤模式下不做快照和对比，避免部分数据覆盖完整快照
        snapshot_path = get_snapshot_path(skill_dir)
        old_snapshot = load_snapshot(snapshot_path)

        if old_snapshot is not None:
            print_diff_report(old_snapshot, sorted_model_ratios, sorted_completion_ratios, sorted_group_ratios)
        else:
            print("\n（首次运行，无历史快照可供对比）")

        save_snapshot(snapshot_path, sorted_model_ratios, sorted_completion_ratios, sorted_group_ratios)
        print(f"\n最新数据已保存至快照: {snapshot_path}", file=sys.stderr)

    # ---- 可选: 价格验证表 ----
    if args.verify and sorted_group_ratios:
        print("\n" + "=" * 80)
        print("价格验证表（单位：$/1K tokens）")
        print("=" * 80)
        sample_models = list(sorted_model_ratios.keys())[:10]
        sample_groups = list(sorted_group_ratios.keys())[:5]
        header = f"{'模型':<40} {'倍率':>6} {'补全':>6}"
        for g in sample_groups:
            header += f" | {g+'(入)':>12} {g+'(出)':>12}"
        print(header)
        print("-" * len(header))
        for model in sample_models:
            mr = sorted_model_ratios[model]
            cr = sorted_completion_ratios.get(model, 0)
            line = f"{model:<40} {mr:>6.3f} {cr:>6.2f}"
            for g in sample_groups:
                gr = sorted_group_ratios.get(g, 1.0)
                inp, outp = compute_actual_prices(model, mr, cr, gr)
                line += f" | ${inp:>10.6f} ${outp:>10.6f}"
            print(line)

    # ---- 可选: 额外保存为独立文件 ----
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, "model_ratios.json"), "w", encoding="utf-8") as f:
            json.dump(sorted_model_ratios, f, indent=2, ensure_ascii=False)
        with open(os.path.join(args.output_dir, "completion_ratios.json"), "w", encoding="utf-8") as f:
            json.dump(sorted_completion_ratios, f, indent=2, ensure_ascii=False)
        with open(os.path.join(args.output_dir, "group_ratios.json"), "w", encoding="utf-8") as f:
            json.dump(sorted_group_ratios, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存至: {args.output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
