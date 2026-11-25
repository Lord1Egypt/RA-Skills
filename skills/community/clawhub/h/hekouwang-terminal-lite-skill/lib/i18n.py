"""运行时语言层 · Python 侧（bash 那半边在 lib/i18n.sh，规则一模一样）。

    优先级：HKW_LANG > ~/.config/hekouwang-terminal/lang > en

用法：
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[N] / "lib"))
    from i18n import t, LANG

⚠️ 两边的词条**不共用文件**：bash 那边是 .sh 变量，Python 这边是 dict，
   语言解析规则必须保持一致（改一边记得改另一边）。release.sh --check 会
   同时校验 en/zh 两侧的 key 是否对齐，漏翻会被拦下。
"""
import os
import pathlib

_ALIASES = {
    "zh": "zh", "zh-cn": "zh", "zh_cn": "zh", "zh-hans": "zh", "zh_hans": "zh",
    "cn": "zh", "chinese": "zh", "中文": "zh",
    "en": "en", "en-us": "en", "en_us": "en", "english": "en",
}
LANG_FILE = pathlib.Path(
    os.environ.get("HKW_LANG_FILE", "~/.config/hekouwang-terminal/lang")
).expanduser()


def _normalize(v):
    v = (v or "").strip().lower().replace(" ", "")
    if v == "auto":                     # auto 是显式选项，不是默认行为
        loc = os.environ.get("LC_ALL") or os.environ.get("LANG") or ""
        return "zh" if loc.lower().startswith("zh") else "en"
    return _ALIASES.get(v, "")


def resolve_lang():
    lang = _normalize(os.environ.get("HKW_LANG"))
    if not lang and LANG_FILE.is_file():
        try:
            lang = _normalize(LANG_FILE.read_text(encoding="utf-8"))
        except OSError:
            lang = ""
    return lang or "en"


LANG = resolve_lang()

# ============================================================
# 词条表。en 是**打底那份**：zh 缺哪条就落回英文，永远不会打出空串。
# ============================================================
MESSAGES = {
    "en": {
        # ---- _generate.py ----
        "GEN_NO_PALETTE": "⚠ no palettes under palettes/, writing minimal.json only (no colors)",
        "GEN_COUNT": "{} palettes ({})",
        "GEN_WITH_BRAND": "brand pack included",
        "GEN_COMMUNITY_ONLY": "community pack only",
        "GEN_ENGINE": "generator: {}\n",
        "GEN_ENGINE_PRO": "iTerm2 + other terminals + ecosystem (paid module loaded)",
        "GEN_ENGINE_OSS": "iTerm2 only (open-source build: colors + blur + Triggers all included)",
        "GEN_TIER_PAID": "paid",
        "GEN_TIER_OSS": "free",
        "GEN_TONE_LIGHT": "light",
        "GEN_TONE_DARK": "dark",
        "GEN_PRO_EXTRA": "\n  + Ghostty / Warp / macOS Terminal / bat / fzf / eza / git diff / tmux / VS Code",
        "GEN_SWEPT": "\nremoved {} orphaned artifacts (their palette is gone):",
        "GEN_SWEPT_MORE": "  … and {} more",
        "GEN_DEFAULT": "\ndefault theme: {}",
        "GEN_MISSING_HEAD": "\nnot generated — these belong to the paid pack:",
        "GEN_MISSING_TAIL": "  unzip the paid pack into this folder and they all appear.",
        "GEN_MISSING_BRAND": "brand themes ({}, two of them light)",
        "GEN_MISSING_MULTI": "multi-terminal sync: Ghostty / Warp / macOS Terminal",
        "GEN_MISSING_ECO": "one palette everywhere: bat / fzf / eza / git diff / tmux / VS Code",
        "GEN_MISSING_FONT": "font priority table (config/font.conf)",
        "GEN_MISSING_AUTO": "follow the system light/dark switch (needs a light theme)",
        "GEN_ADJUSTED": "\nnormalized / vivid-boosted {} palette(s):",
        "GEN_ADJUSTED_MORE": " … +{}",
        "GEN_DONE": "done",
        # ---- _preview.py ----
        "PRE_TITLE": "hekouwang · terminal themes",
        "PRE_COUNT": "{} themes",
        "PRE_BRAND": " · {} brand",
        "PRE_CURRENT_SUM": " · current {}",
        "PRE_CURRENT": "← current",
        "PRE_TONE_LIGHT": "light",
        "PRE_TONE_DARK": "dark",
        "PRE_CODE_COMMENT": "    # one palette drives the whole tool chain",
        "PRE_LOG_ERROR": " connection timed out, retried 3 times",
        "PRE_LOG_WARN": " certificate expires in 30 days",
        "PRE_LOG_OK": " deployed · 1.2s",
        "PRE_USAGE": "usage: _preview.py --gallery|--card <name>|--cli-diff <name>|--banner <name>|--strip <name>|--snapshot <dir>|--regress <dir>",
        "PRE_NO_THEMES": "  (nothing to preview: run python3 _generate.py first)",
        "PRE_NEED_DIR": "  missing the directory",
        "PRE_SNAP_DONE": "  wrote {} snapshots to {}",
        "PRE_REGRESS_OK": "  {} themes match the golden snapshots",
        "PRE_REGRESS_BAD": "  {} theme(s) drifted — re-run --snapshot if the change was intended",
        "PRE_GOLDEN_MISSING": "golden file missing",
        "PRE_DRIFT_LINES": "{} line(s) changed",
        "PRE_NEED_NAME": "  missing the theme name",
        "PRE_NO_SUCH": "  no theme called '{}'",
        # ---- _audit.py ----
        "AUDIT_HEAD": "visual audit — contrast / selection / search / cursor / surfaces / neutral ramp",
        "AUDIT_NONE": "  (no generated themes: run python3 _generate.py first)",
        "AUDIT_PASS": "  all {} themes pass",
        "AUDIT_FAIL": "  {} theme(s) below the visual floor",
        "AUDIT_SUM": "  avg score {} · lowest {} ({})",
        "AUDIT_USAGE": "usage: _audit.py [--table|--json] [--theme NAME] [--gate]",
    },
    "zh": {
        # ---- _generate.py ----
        "GEN_NO_PALETTE": "⚠ palettes/ 下没有色板，只出 minimal.json（无配色）",
        "GEN_COUNT": "色板 {} 套（{}）",
        "GEN_WITH_BRAND": "含品牌包",
        "GEN_COMMUNITY_ONLY": "仅社区包",
        "GEN_ENGINE": "生成器：{}\n",
        "GEN_ENGINE_PRO": "iTerm2 + 多终端 + 生态（付费模块已加载）",
        "GEN_ENGINE_OSS": "仅 iTerm2（开源版：配色 + 毛玻璃 + Triggers 全都有）",
        "GEN_TIER_PAID": "付费",
        "GEN_TIER_OSS": "开源",
        "GEN_TONE_LIGHT": "亮底",
        "GEN_TONE_DARK": "暗底",
        "GEN_PRO_EXTRA": "\n  + Ghostty / Warp / macOS 自带终端 / bat / fzf / eza / git diff / tmux / VS Code",
        "GEN_SWEPT": "\n清掉 {} 项没主的旧产物（色板已移除）：",
        "GEN_SWEPT_MORE": "  … 其余 {} 项",
        "GEN_DEFAULT": "\n默认主题：{}",
        "GEN_MISSING_HEAD": "\n以下属付费包，当前不生成：",
        "GEN_MISSING_TAIL": "  把付费包解压进本目录即自动全出。",
        "GEN_MISSING_BRAND": "品牌主题（{}，含 2 套亮色）",
        "GEN_MISSING_MULTI": "多终端同步：Ghostty / Warp / macOS 自带终端",
        "GEN_MISSING_ECO": "全生态同色：bat / fzf / eza / git diff / tmux / VS Code",
        "GEN_MISSING_FONT": "字体优先级表（config/font.conf）",
        "GEN_MISSING_AUTO": "跟随系统深浅色（需亮色主题）",
        "GEN_ADJUSTED": "\n按视觉地板归一化 / 提彩了 {} 套色板：",
        "GEN_ADJUSTED_MORE": " … 另 {} 处",
        "GEN_DONE": "done",
        # ---- _preview.py ----
        "PRE_TITLE": "会勇禾口王 · 终端主题",
        "PRE_COUNT": "{} 套",
        "PRE_BRAND": " · 品牌 {}",
        "PRE_CURRENT_SUM": " · 当前 {}",
        "PRE_CURRENT": "← 当前",
        "PRE_TONE_LIGHT": "亮底",
        "PRE_TONE_DARK": "暗底",
        "PRE_CODE_COMMENT": "    # 一份色板管住整条工具链",
        "PRE_LOG_ERROR": " 连接超时，已重试 3 次",
        "PRE_LOG_WARN": " 证书 30 天后过期",
        "PRE_LOG_OK": " 部署完成 · 1.2s",
        "PRE_USAGE": "用法: _preview.py --gallery|--card <名字>|--cli-diff <名字>|--banner <名字>|--strip <名字>|--snapshot <目录>|--regress <目录>",
        "PRE_NO_THEMES": "  （没有可预览的主题：先跑 python3 _generate.py）",
        "PRE_NEED_DIR": "  缺少目录参数",
        "PRE_SNAP_DONE": "  已写入 {} 份金标到 {}",
        "PRE_REGRESS_OK": "  {} 套主题与金标一致",
        "PRE_REGRESS_BAD": "  有 {} 套主题漂移 —— 若是预期改动，重跑 --snapshot",
        "PRE_GOLDEN_MISSING": "缺少金标文件",
        "PRE_DRIFT_LINES": "{} 行发生变化",
        "PRE_NEED_NAME": "  少了主题名字",
        "PRE_NO_SUCH": "  没有主题 '{}'",
        # ---- _audit.py ----
        "AUDIT_HEAD": "视觉审计 — 对比度 / 选区 / 搜索 / 光标 / 语义表面 / 中性梯",
        "AUDIT_NONE": "  （没有已生成的主题：先跑 python3 _generate.py）",
        "AUDIT_PASS": "  {} 套主题全部达标",
        "AUDIT_FAIL": "  有 {} 套低于视觉地板",
        "AUDIT_SUM": "  平均分 {} · 最低 {}（{}）",
        "AUDIT_USAGE": "用法: _audit.py [--table|--json] [--theme 名字] [--gate]",
    },
}


def t(key, *args):
    """取词条并套参数。缺词条时原样返回 key —— 静默变空串比看见 key 难查得多。"""
    s = MESSAGES.get(LANG, {}).get(key) or MESSAGES["en"].get(key, key)
    return s.format(*args) if args else s


def theme_display(name, palette=None, names_file=None):
    """主题显示名，按当前语言取。

    真相源优先级：色板里的 display/display_zh > 生成时落的 names.json > 主题 key 本身。
    ⚠️ 仓库里生成好的 .json / .terminal 一律烧**英文名**（公开仓要对英文用户成立），
       中文名靠这里在**部署时**注入，所以两种语言不需要两套产物。
    """
    if palette:
        if LANG != "en" and palette.get(f"display_{LANG}"):
            return palette[f"display_{LANG}"]
        if palette.get("display"):
            return palette["display"]
    if names_file:
        import json
        try:
            data = json.loads(pathlib.Path(names_file).read_text(encoding="utf-8"))
            entry = data.get(name) or {}
            return entry.get(LANG) or entry.get("en") or name
        except (OSError, ValueError):
            pass
    return name
