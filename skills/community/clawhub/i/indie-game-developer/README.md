# 独立游戏开发者技能库

> AI Agent Skills for Indie Game Developers —— 覆盖游戏开发、设计打磨、像素美术、Steam 发行

## 定位

为独立游戏开发者（特别是单人/小团队）提供一套可安装的 AI Agent 技能，让 Claude Code 成为你的游戏开发搭档。

## 架构说明（superpower）

本仓库采用 skills-repo 的 **superpower 架构**（五层）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（引擎选型、资源管线、Steam 发行、QA 性能、精致像素方法），按需加载
- `skills/` — L3 细粒度子技能（Three.js / 设计 / 像素美术 / Steam 发行），可单独安装
- `scripts/` — L4 确定性脚本（资源引用完整性、Steam 元数据校验）
- `assets/` — L5 可复用模板（商店元数据模板、资源清单示例、示例场景）

## 核心理念

> 用 AI 撬动创意，用技能加速交付，一人公司也能做完游戏。

- **每个技能聚焦一个环节**——不贪大求全，单个技能做到可落地
- **2 周可出 MVP**——技能设计匹配快节奏独立开发周期
- **一次交付，持续销售**——面向 Steam / itch.io / App Store 等买断制平台

## 技能清单

| 环节 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 🔧 编程 | [game-developer](skills/game-developer/SKILL.md) | Three.js 浏览器游戏开发：游戏循环、3D 资产、UI、QA 全流程 | [衍生](https://skills.sh/majidmanzarpour/threejs-game-skills/threejs-game-director) |
| 🎨 设计 | [game-designer](skills/game-designer/SKILL.md) | 游戏视觉打磨：调色板、粒子特效、动画、UI 评审 | [衍生](https://skills.sh/opusgamelabs/game-creator/design-game) |
| 👾 美术 | [pixel-art-studio](skills/pixel-art-studio/SKILL.md) | 像素艺术精灵生成与动画：16x16 像素、有限调色板、游戏集成 | [衍生](https://skills.sh/omer-metin/skills-for-antigravity/pixel-art-sprites) |
| ✨ 美术 | [refined-pixel-art](skills/refined-pixel-art/SKILL.md) | 精致手绘像素角色：参考图拆解、网格密度、色簇控制、提示词纠偏与验收 | 原创实践 |
| 📦 发行 | [steam-launch](skills/steam-launch/SKILL.md) | Steam 发行运营：商店页审计、愿望单诊断、Next Fest 规划 | [衍生](https://skills.sh/akillness/oh-my-skills/steam-store-launch-ops) |

## 安装

```bash
# 整库安装（推荐）—— 拿到路由层 + 全部 references/scripts/assets
npx skills add skills-repo/indie-game-developer -g -y

# 单技能安装 —— 只要某一个细粒度能力，例如只要游戏开发能力
npx skills add skills-repo/indie-game-developer@game-developer -g -y

# 单独安装精致手绘像素角色技能
npx skills add skills-repo/indie-game-developer@refined-pixel-art -g -y
```

## 内置脚本与模板

```bash
# 校验源码资源引用完整性（期望 0 error）
python3 scripts/check_asset_refs.py --scan src/ --root .

# 校验 Steam 商店元数据（期望 0 error）
python3 scripts/check_steam_metadata.py --metadata assets/steam-store-metadata-template.json
```

详见 `SKILL.md` 的「内置脚本」与「模板资源」两节。

## 推荐工作流

```
游戏开发 → 视觉打磨 → 像素美术 → Steam 发行
game-      game-       pixel-art-   steam-
developer  designer    studio       launch
```

## 许可

MIT
