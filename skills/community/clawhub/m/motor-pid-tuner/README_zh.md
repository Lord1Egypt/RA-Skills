# 电机PID调参器

输入电机参数自动算FOC电流/速度/位置三环PI参数、抗饱和、Q格式定点化、直接出STM32/GD32/C2000的C代码。

> 这是一个跨平台的 **Agent Skill（智能体技能）包**，不是独立软件。把它装进任意支持「Agent Skills / 技能」标准的 AI 助手（如 Claude Code、扣子Coze、Cursor、各类兼容Agent平台），AI 就能在对话中自动调用它。

---

## 包内容
- `SKILL.md` —— 技能说明书（AI 读这个来决定何时、如何调用）
- `scripts/` 或根目录 `.py` —— 实际功能脚本，纯 Python 3
- `references/` / `templates/` —— 参考资料或代码模板（部分技能有）

## 系统要求
- Python 3.8+（命令行 `python3 --version` 能看到版本即可）
- 无需任何第三方库

## 安装方法

### 方式一：在支持的 Agent 平台里导入
- **扣子 Coze**：技能/技能草稿 → 上传技能 → 选择本 zip（或解压后的文件夹）→ 发布到「我的技能」
- **Claude Code / Cursor 等**：把解压后的整个文件夹放进 Agent 的 skills 目录（各平台位置见其文档，通常为 `~/.claude/skills/` 或工作区 `.skills/`），重启会话即可
- **其它兼容 Agent Skills 标准的平台**：导入 zip 或把文件夹加入技能目录，平台识别到 `SKILL.md` 即自动加载

### 方式二：当命令行工具直接用（不需要任何 AI）
脚本可脱离 Agent 单独运行，例如：

```
python3 main.py --mode current --rs 0.5 --ls 0.002 --bw 1000   # 算电流环PI
python3 main.py --mode code --rs 0.5 --ls 0.002         # 直接出C代码
```

## 使用
装好后，直接用自然语言跟 AI 说需求即可，例如：「帮我算电流环PI参数，Rs=0.5Ω Ls=2mH 开关频率20kHz」。
AI 会自动读取 SKILL.md 并调用脚本，你无需记命令。

## 兼容性说明
- 所有脚本为**纯 Python 3**，仅用标准库，不依赖任何 API Key、不联网、不消耗 AI 额度。
- 已在 Python 3.13 实测通过；不依赖特定操作系统（Windows / macOS / Linux 均可）。
- 各平台导入入口名称略有差异，但包结构（SKILL.md + 脚本）是开放标准，通用。

---
*本技能包可自由分发。AI 生成结果请人工复核后再用于生产。*
