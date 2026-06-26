#!/usr/bin/env python3
"""火一五小红书创作者画像初始化 / 管理。

工作模式
========
1. **`init`** — 引导用户从 1~5 篇代表作建立 baseline，自动提取风格档案。
2. **`add`**  — 追加一篇 baseline（已有档案的情况下）。
3. **`show`** — 查看当前风格档案 + 规则覆盖。
4. **`rules`** — 编辑规则覆盖（disabled / weights / custom_sensitive）。
5. **`evolve`** — 根据历史 feedback 自动演进规则。
6. **`reset`** — 删除整个档案（需 --confirm）。

存档位置：`~/.xiaohongshu/profile/`（可被 XHS_PROFILE_DIR 覆盖）。

用法
----

    # 第一次：从已有的 .json 笔记建 baseline
    python3 profile_init.py init --persona "30+ 干皮女生" --voice casual \\
        --niche "护肤" --baseline note1.json note2.json note3.json

    # 也支持直接抓取（要 Cookie）
    python3 profile_init.py init --persona "..." --note-id 64abc...

    # 查看
    python3 profile_init.py show

    # 教助手一条规则（"我以后不要 emoji"）
    python3 profile_init.py rules --disable emoji

    # 加自定义敏感词
    python3 profile_init.py rules --add-sensitive "卷王" --add-sensitive "原谅色"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import (  # noqa: E402
    Feedback,
    ProfileStore,
    RuleOverride,
    StyleProfile,
    derive_style,
    evolve_rules,
)
from xhs_writer import load_draft  # noqa: E402

# ---------- 工具：把多种输入归一化成 baseline 用的 dict ----------


def _load_input(p: str) -> dict:
    path = Path(p)
    if not path.exists():
        raise FileNotFoundError(p)
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    # markdown 草稿
    draft = load_draft(p)
    return draft.to_dict()


# ---------- 子命令 ----------


def cmd_init(args: argparse.Namespace) -> int:
    store = ProfileStore()
    if store.style_path.exists() and not args.force:
        print(f"⚠️ 已存在档案：{store.style_path}")
        print("   要重新初始化加 --force；要追加用 `profile_init.py add`")
        return 1

    samples = []
    for p in args.baseline:
        try:
            samples.append(_load_input(p))
        except Exception as e:
            print(f"❌ 读不了 {p}: {e}", file=sys.stderr)
            return 1

    # 可选：直接从平台抓
    if args.note_id:
        try:
            from xhs_client import XHSClient, load_cookie_from_env
            from xhs_parser import note_to_dict, parse_note_page
            client = XHSClient(cookie=load_cookie_from_env())
            for nid in args.note_id:
                html = client.get_explore_page(note_id=nid, xsec_token=args.xsec_token or None)
                note = parse_note_page(html, note_id=nid)
                if note:
                    samples.append(note_to_dict(note))
        except Exception as e:
            print(f"⚠️ 抓取失败（继续用本地样本）：{e}", file=sys.stderr)

    if not samples:
        print("❌ 没有 baseline 样本（用 --baseline file1.json file2.md ... 或 --note-id ...）",
              file=sys.stderr)
        return 1

    # 持久化样本
    for s in samples:
        store.add_baseline(s)

    # 提取风格
    profile = derive_style(samples)
    if args.persona:
        profile.persona = args.persona
    if args.voice:
        profile.voice = args.voice
    if args.niche:
        profile.niche = args.niche
    store.save_style(profile)

    # 默认规则覆盖留空，让用户后续教
    if not store.rules_path.exists():
        store.save_rules(RuleOverride())

    print(f"✓ 初始化完成（{len(samples)} 篇样本）")
    print(f"  档案位置：{store.root}")
    _print_profile_summary(profile)
    print("\n下一步：")
    print("  python3 scripts/assistant.py        # 进入对话助手")
    print("  python3 scripts/profile_init.py show")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    store = ProfileStore()
    samples = []
    for p in args.baseline:
        try:
            samples.append(_load_input(p))
        except Exception as e:
            print(f"❌ 读不了 {p}: {e}", file=sys.stderr)
            return 1
    for s in samples:
        store.add_baseline(s)

    # 重新算
    all_baselines = store.load_baselines()
    profile = store.load_style()
    new_profile = derive_style(all_baselines)
    # 保留用户手填的字段
    new_profile.persona = profile.persona
    new_profile.voice = profile.voice
    new_profile.niche = profile.niche or new_profile.niche
    new_profile.avoid_words = profile.avoid_words
    store.save_style(new_profile)
    print(f"✓ 已追加 {len(samples)} 篇，重新提取风格档案。当前样本数：{new_profile.sample_count}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    store = ProfileStore()
    if not store.style_path.exists():
        print("（尚未初始化档案。先跑 `profile_init.py init` ）")
        return 0
    profile = store.load_style()
    rules = store.load_rules()

    if args.format == "json":
        print(json.dumps({
            "style": profile.to_dict(),
            "rules": rules.to_dict(),
            "baseline_count": len(store.load_baselines()),
            "feedback_count": len(store.load_feedback()),
        }, ensure_ascii=False, indent=2))
        return 0

    _print_profile_summary(profile)
    print()
    _print_rules_summary(rules)
    print(f"\n📁 档案位置：{store.root}")
    return 0


def cmd_rules(args: argparse.Namespace) -> int:
    store = ProfileStore()
    rules = store.load_rules()

    if args.disable:
        for k in args.disable:
            if k not in rules.disabled_checks:
                rules.disabled_checks.append(k)
    if args.enable:
        rules.disabled_checks = [k for k in rules.disabled_checks if k not in args.enable]
    if args.weight:
        for kv in args.weight:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            try:
                rules.weights[k.strip()] = float(v)
            except ValueError:
                continue
    if args.add_sensitive:
        for w in args.add_sensitive:
            if w not in rules.custom_sensitive:
                rules.custom_sensitive.append(w)
    if args.remove_sensitive:
        rules.custom_sensitive = [w for w in rules.custom_sensitive if w not in args.remove_sensitive]
    if args.allow:
        for w in args.allow:
            if w not in rules.allowed_words:
                rules.allowed_words.append(w)
    if args.unallow:
        rules.allowed_words = [w for w in rules.allowed_words if w not in args.unallow]
    if args.max_emoji is not None:
        rules.max_emoji_per_post = args.max_emoji
    if args.prefer_emoji is not None:
        rules.prefer_emoji = args.prefer_emoji

    store.save_rules(rules)
    _print_rules_summary(rules)
    print(f"\n✓ 已写入 {store.rules_path}")
    return 0


_PRESETS = {
    "allen": {
        "name": "Allen 流（品牌 / 情感共鸣赛道）",
        "rules": {
            "weights": {
                "compliance": 0.20,    # 合规权重微降
                "emoji": 0.05,         # emoji 工程指标权重降
            },
            "disabled_checks": [],     # 不禁用工程项，只是 Allen 美学加权
        },
        "aesthetic_weights": {
            "breath": 0.25,
            "ai_speak": 0.20,
            "teach_vs_lead": 0.20,
            "resonance": 0.20,
            "invitation": 0.15,
        },
        "merge_aesthetic_weight": 0.5, # 综合分时 Allen 美学占一半
        "phrases": ["其实", "我自己", "我体感", "亲测", "我之前以为"],
    },
    "engineer": {
        "name": "工程师流（干货 / 教程 / 工具）",
        "rules": {
            "disabled_checks": ["aesthetic:breath", "aesthetic:teach_vs_lead",
                               "aesthetic:resonance"],  # 关掉 Allen 美学维度
        },
        "merge_aesthetic_weight": 0.0,
    },
    "balanced": {
        "name": "平衡流（默认）",
        "rules": {},
        "merge_aesthetic_weight": 0.3,
    },
}


def cmd_preset(args: argparse.Namespace) -> int:
    """切换风格预设。"""
    if args.list:
        print("可用预设：")
        for k, v in _PRESETS.items():
            print(f"  {k:<10} — {v['name']}")
        return 0

    preset = _PRESETS.get(args.name)
    if not preset:
        print(f"❌ 未知预设：{args.name}（可用：{', '.join(_PRESETS)}）", file=sys.stderr)
        return 1

    store = ProfileStore()
    rules = store.load_rules()

    # 合并预设到当前 rules
    p_rules = preset.get("rules", {})
    if "weights" in p_rules:
        rules.weights = {**rules.weights, **p_rules["weights"]}
    if "disabled_checks" in p_rules:
        for k in p_rules["disabled_checks"]:
            if k not in rules.disabled_checks:
                rules.disabled_checks.append(k)
    if "phrases" in preset:
        rules.custom_phrases = preset["phrases"]

    # 把 aesthetic_weights 和 merge_aesthetic_weight 写进 rules.weights 的特殊键
    if "aesthetic_weights" in preset:
        for k, v in preset["aesthetic_weights"].items():
            rules.weights[f"aesthetic:{k}"] = v
    if "merge_aesthetic_weight" in preset:
        rules.weights["_merge_aesthetic_weight"] = preset["merge_aesthetic_weight"]

    store.save_rules(rules)
    print(f"✓ 已切换到预设：{preset['name']}")
    _print_rules_summary(rules)
    return 0


def cmd_evolve(args: argparse.Namespace) -> int:
    store = ProfileStore()
    changes = evolve_rules(store, threshold=args.threshold)
    if not isinstance(changes, dict):
        print("✓ 演进完成（无变化）")
        return 0

    added_disabled = changes.get("disabled_added", [])
    added_weak = changes.get("weak_dims_added", [])

    if added_disabled:
        print("✓ 自动禁用了：")
        for x in added_disabled:
            print(f"   • {x['key']}  ({x['reason']})")

    if added_weak:
        print("⚠️ 长期掉某维（已标记 weak_dims，不会自动禁用）：")
        for x in added_weak:
            print(f"   • {x['dim']}  尝试 {x['attempts']} 次 / 改进率 {x['rate']}%")
        print("   建议：跑 `practice.py rewrite-jarvis` 或读 data/allen_method.md 强化")

    weak = changes.get("weak_dims", [])
    if weak:
        print(f"\n当前 weak_dims：{weak}")

    if not added_disabled and not added_weak:
        print("（没有需要演进的规则。继续保持节奏）")
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    if not args.confirm:
        print("⚠️ 这会删除 ~/.xiaohongshu/profile/ 下所有档案。加 --confirm 真的要执行。",
              file=sys.stderr)
        return 1
    import shutil
    store = ProfileStore()
    if store.root.exists():
        shutil.rmtree(store.root)
    print(f"✓ 已删除 {store.root}")
    return 0


# ---------- 打印 ----------


def _print_profile_summary(profile: StyleProfile) -> None:
    print("=" * 60)
    print("📋 风格档案")
    print("=" * 60)
    print(f"  人设           : {profile.persona or '(未设置)'}")
    print(f"  语调           : {profile.voice}")
    print(f"  赛道           : {profile.niche or '(未设置)'}")
    print(f"  样本数         : {profile.sample_count}")
    print(f"  平均标题长     : {profile.avg_title_len} 字  范围 {profile.title_len_range}")
    print(f"  平均正文       : {profile.avg_content_len} 字 / {profile.avg_paragraphs} 段")
    print(f"  emoji/篇       : {profile.emoji_per_post}")
    if profile.favorite_emojis:
        print(f"  常用 emoji     : {' '.join(profile.favorite_emojis)}")
    if profile.favorite_formulas:
        items = sorted(profile.favorite_formulas.items(), key=lambda x: -x[1])
        print(f"  偏好公式       : {', '.join(f'{k}({v})' for k, v in items)}")
    if profile.favorite_skeletons:
        items = sorted(profile.favorite_skeletons.items(), key=lambda x: -x[1])
        print(f"  偏好骨架       : {', '.join(f'{k}({v})' for k, v in items)}")
    if profile.common_tags:
        print(f"  高频话题       : {' '.join('#' + t for t in profile.common_tags[:8])}")
    if profile.common_phrases:
        print(f"  口头禅         : {', '.join(profile.common_phrases)}")


def _print_rules_summary(rules: RuleOverride) -> None:
    print("=" * 60)
    print("🛠️  规则覆盖")
    print("=" * 60)
    print(f"  禁用的检查项   : {rules.disabled_checks or '(无)'}")
    if rules.weights:
        print(f"  权重覆盖       : {rules.weights}")
    if rules.custom_sensitive:
        print(f"  自定义敏感词   : {rules.custom_sensitive}")
    if rules.allowed_words:
        print(f"  解禁词         : {rules.allowed_words}")
    if rules.max_emoji_per_post is not None:
        print(f"  emoji 上限     : {rules.max_emoji_per_post}")
    if rules.prefer_emoji is not None:
        print(f"  偏好 emoji     : {rules.prefer_emoji}")
    if rules.custom_phrases:
        print(f"  自创口头禅     : {rules.custom_phrases}")


# ---------- 入口 ----------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="profile_init.py", description="创作者风格档案 / 规则管理")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="第一次建立风格档案")
    pi.add_argument("--persona", default="", help="人设，如：30+ 干皮女生")
    pi.add_argument("--voice", choices=["casual", "formal", "playful", "pro"], default="casual")
    pi.add_argument("--niche", default="", help="赛道，如：护肤")
    pi.add_argument("--baseline", nargs="*", default=[], help=".json 笔记 / .md 草稿（1~5 篇）")
    pi.add_argument("--note-id", nargs="*", default=[], help="或直接给 note_id（要 Cookie）")
    pi.add_argument("--xsec-token", default="")
    pi.add_argument("--force", action="store_true", help="覆盖已有档案")
    pi.set_defaults(func=cmd_init)

    pa = sub.add_parser("add", help="追加 baseline 样本")
    pa.add_argument("baseline", nargs="+", help="新样本路径")
    pa.set_defaults(func=cmd_add)

    ps = sub.add_parser("show", help="查看档案")
    ps.add_argument("--format", choices=["text", "json"], default="text")
    ps.set_defaults(func=cmd_show)

    pr = sub.add_parser("rules", help="编辑规则覆盖")
    pr.add_argument("--disable", nargs="*", default=[],
                    help="禁用的检查项（title/first_lines/layout/emoji/hashtags/compliance）")
    pr.add_argument("--enable", nargs="*", default=[], help="重新启用某个检查项")
    pr.add_argument("--weight", nargs="*", default=[], help="设置权重，如 emoji=0.05")
    pr.add_argument("--add-sensitive", nargs="*", default=[], help="加自定义敏感词")
    pr.add_argument("--remove-sensitive", nargs="*", default=[], help="移除自定义敏感词")
    pr.add_argument("--allow", nargs="*", default=[], help="解禁某些默认敏感词")
    pr.add_argument("--unallow", nargs="*", default=[], help="撤销解禁")
    pr.add_argument("--max-emoji", type=int, default=None, help="单篇 emoji 上限")
    pr.add_argument("--prefer-emoji", type=lambda x: x.lower() == "true", default=None,
                    help="是否偏好 emoji (true/false)")
    pr.set_defaults(func=cmd_rules)

    pe = sub.add_parser("evolve", help="基于 feedback 自动演进规则")
    pe.add_argument("--threshold", type=int, default=3, help="连续 reject N 次后自动禁用")
    pe.set_defaults(func=cmd_evolve)

    pp = sub.add_parser("preset", help="切换风格预设：allen / engineer / balanced")
    pp.add_argument("name", nargs="?", default="", help="预设名")
    pp.add_argument("--list", action="store_true")
    pp.set_defaults(func=cmd_preset)

    px = sub.add_parser("reset", help="删除整个档案")
    px.add_argument("--confirm", action="store_true")
    px.set_defaults(func=cmd_reset)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
