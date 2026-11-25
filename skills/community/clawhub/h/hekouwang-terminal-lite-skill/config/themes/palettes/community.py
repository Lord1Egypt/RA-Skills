# ============================================================
# 社区色板（开源版自带）
#
# 三套广为人知的社区配色，色值取自各自上游官方仓库。
# ⚠️ 上游并不遵守本仓的视觉约束：这三套原样就有 6–7 对 normal 与 bright 同色
#    （`ls` / `git diff` 的强调层会被静默吞掉），ANSI 8 在 tokyo-night 上只有 1.91:1。
#    所以 palettes/__init__.py 在 load() 时按 _audit.py 的约束归一化一次：
#    **只改 OKLab 明度，色相与彩度尽量保持**；想保留上游原值给某套加 "normalize": False。
#    生成器打印的改动清单就是归一化的结果，不是手改的。
# 这三套的作用是「让开源版开箱就是完整可用的产品」，不是凑数：
# 生成器对它们和品牌主题一视同仁，同样吐出 iTerm2 / Ghostty / bat /
# fzf / eza / delta / tmux / starship / VS Code 全套。
#
# 色板字段：
#   display     主题显示名 · **英文**（iTerm2 Profile 名、Warp/Ghostty 注释都用它）
#               仓库里生成好的产物一律烧这个英文名。
#   display_zh  中文显示名，可选。装成中文时由 theme.sh 在**部署那一刻**注入，
#               所以两种语言共用同一套生成产物，不需要各生成一份。
#   light    True=亮底主题（生成器据此翻转 selection、Ghostty details 等）
#   bg fg cursor selbg selfg   背景/前景/光标/选中底/选中字
#   ansi     16 色，顺序 = black red green yellow blue magenta cyan white
#            前 8 个是 normal，后 8 个是 bright
# ============================================================

PALETTES = {
    "catppuccin-mocha": {
        "display": "hekouwang · Catppuccin Mocha",
        "display_zh": "会勇禾口王 · Catppuccin Mocha",
        "light": False,
        "bg": "1e1e2e", "fg": "cdd6f4", "cursor": "fab387", "accent": "fab387", "selbg": "585b70", "selfg": "cdd6f4",
        "ansi": ["45475a", "f38ba8", "a6e3a1", "f9e2af", "89b4fa", "f5c2e7", "94e2d5", "bac2de",
                 "585b70", "f38ba8", "a6e3a1", "f9e2af", "89b4fa", "f5c2e7", "94e2d5", "a6adc8"],
    },
    "tokyo-night": {
        "display": "hekouwang · Tokyo Night",
        "display_zh": "会勇禾口王 · Tokyo Night",
        "light": False,
        "bg": "1a1b26", "fg": "c0caf5", "cursor": "7dcfff", "accent": "7dcfff", "selbg": "283457", "selfg": "c0caf5",
        "ansi": ["15161e", "f7768e", "9ece6a", "e0af68", "7aa2f7", "bb9af7", "7dcfff", "a9b1d6",
                 "414868", "f7768e", "9ece6a", "e0af68", "7aa2f7", "bb9af7", "7dcfff", "c0caf5"],
    },
    "gruvbox-dark": {
        "display": "hekouwang · Gruvbox Dark",
        "display_zh": "会勇禾口王 · Gruvbox Dark",
        "light": False,
        "bg": "282828", "fg": "ebdbb2", "cursor": "fe8019", "accent": "fe8019", "selbg": "504945", "selfg": "ebdbb2",
        "ansi": ["282828", "cc241d", "98971a", "d79921", "458588", "b16286", "689d6a", "a89984",
                 "928374", "fb4934", "b8bb26", "fabd2f", "83a598", "d3869b", "8ec07c", "ebdbb2"],
        # 经典 Gruvbox 语法：关键字/标签用红，函数用蓝，类型用 aqua
        "syntax": {
            "keyword": {"slot": 1, "l": 0.010, "style": "bold"},
            "tag": {"slot": 1, "l": 0.010, "style": "bold"},
            "type": {"slot": 6, "l": -0.020},
        },
    },
}
