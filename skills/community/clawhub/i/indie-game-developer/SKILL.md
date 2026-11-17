---
name: indie-game-developer
description: >-
  独立游戏开发者技能库：覆盖游戏引擎选型（Three.js/Phaser/Godot/Unity）、游戏开发全流程、
  像素美术、视觉打磨与 Steam 发行。提供引擎/技术栈决策、资源管线、发行深玩、QA 与性能的
  方法论，并用脚本固化资源引用完整性与 Steam 商店元数据校验。
  触发词："独立游戏"、"游戏开发"、"Three.js"、"Phaser"、"Godot"、"Unity"、"像素美术"、
  "Steam 发行"、"愿望单"、"Next Fest"、"游戏性能"、"资源管线"。
agent_created: true
metadata:
  version: 1.0.0
  category: 游戏开发
  difficulty: 进阶
  architecture: superpower
---

# 独立游戏开发者 (Indie Game Developer)

> 把 AI 编程助手变成一名能扛下独立游戏交付链路（选型→开发→美术→资源→发行→QA）的搭档：从引擎决策到 Steam 上架，并用确定性脚本守住资源引用与商店元数据这两类硬门槛。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 需要**选引擎/技术栈**：Three.js / Phaser / Godot / Unity 怎么选、2D/3D/Web 怎么定
- 用 **Three.js** 做浏览器 3D 游戏、或用 **像素美术**生产精灵与动画
- 需要**资源管线**：精灵表打包、glb 优化、音频转码、引用对齐
- 需要**Steam 发行**：商店页、愿望单漏斗、Next Fest、定价与区域
- 需要**游戏性能与 QA**：帧预算、Draw Call、GC 卡顿、移动端/Deck 适配
- 需要**校验资源引用**或**校验 Steam 商店元数据**（确定性脚本）

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 引擎与技术栈选型（决策树 + 矩阵 + 发布路径） | [references/decision-engine-tech.md](references/decision-engine-tech.md) | 选型, 引擎, Three.js, Godot, Unity, 2D, 3D |
| 资源管线（精灵表/glb/音频/引用完整性） | [references/asset-pipeline.md](references/asset-pipeline.md) | 资源, 精灵表, glb, 贴图, 音频, 引用完整性 |
| Steam 发行深玩（商店页/愿望单/Next Fest/定价） | [references/steam-launch-playbook.md](references/steam-launch-playbook.md) | Steam, 愿望单, Next Fest, 定价, 区域, 折扣 |
| 游戏 QA 与性能（帧预算/GC/移动适配） | [references/game-qa-perf.md](references/game-qa-perf.md) | QA, 性能, 帧预算, DrawCall, GC, Deck |
| Three.js 游戏开发（细粒度调用） | [skills/game-developer/SKILL.md](skills/game-developer/SKILL.md) | three.js, 游戏循环, 物理, 3D, 后处理 |
| 游戏视觉与打磨（细粒度调用） | [skills/game-designer/SKILL.md](skills/game-designer/SKILL.md) | 视觉, 粒子, 手感, UI, 调色板 |
| 像素美术工坊（细粒度调用） | [skills/pixel-art-studio/SKILL.md](skills/pixel-art-studio/SKILL.md) | 像素, 精灵, 调色板, 精灵表, 动画 |
| 精致像素角色方法（密度/色簇/白底 icon/纠偏） | [references/refined-pixel-art-playbook.md](references/refined-pixel-art-playbook.md) | 精致像素, hand-drawn pixel, 网格密度, 色簇, 白底 |
| 精致手绘像素角色（细粒度调用） | [skills/refined-pixel-art/SKILL.md](skills/refined-pixel-art/SKILL.md) | refined pixel, 参考图, 角色 icon, prompt, 验收 |
| Steam 发行操作（细粒度调用） | [skills/steam-launch/SKILL.md](skills/steam-launch/SKILL.md) | steam, 商店页, Demo, 发行, 清单 |

> 路由规则：先判断任务属于「选型 / 资源 / 发行 / QA」哪类方法论 → 读 `references/`；要落地某个具体能力 → 直接调 `skills/` 对应子技能。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/check_asset_refs.py --scan src/ --root .` — 扫描源码资源引用，校验被引文件存在，防运行时缺图
- `scripts/check_steam_metadata.py --metadata assets/steam-store-metadata-template.json` — 校验 Steam 商店元数据字段齐备合规

运行示例：

```bash
python3 scripts/check_asset_refs.py --scan src/ --root .
python3 scripts/check_steam_metadata.py --metadata assets/steam-store-metadata-template.json
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/steam-store-metadata-template.json](assets/steam-store-metadata-template.json) — Steam 商店元数据模板（脚本自检 0 错误）
- [assets/asset-manifest-example.json](assets/asset-manifest-example.json) — 资源清单示例（驱动 check_asset_refs 的清单模式）
- `assets/sample-game/` — 示例游戏场景，演示资源引用解析（扫描模式自检 0 错误）
- [assets/refined-pixel-character-prompt.md](assets/refined-pixel-character-prompt.md) — 精致像素角色与白底 icon 提示词模板

## 核心原则（始终遵循）

1. **选型先行**：先定引擎再写代码，用决策树论证，避免中途换引擎的毁灭性成本。
2. **资源解耦**：资源用引擎无关格式（glb/精灵表/JSON），CI 校验引用完整性，换引擎主要重写渲染层。
3. **先量后优**：性能结论来自最低目标设备实测，不信开发机高帧率。
4. **发行前移**：Steam 成败在发布前 6 个月的愿望单，不是发布日。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜引擎 API。
6. **明确边界**：定价/上线时机等商业拍板由人做，本技能出方案与报告，不替代决策。

## 与其他技能协作

- 需要**动画/动效**设计 → 调用 `animation-engineer`
- 需要**移动端适配**细节 → 调用 `mobile-developer`
- 需要**测试**（自动化/E2E）→ 调用 `software-tester`
- 需要**文档**（商店文案/更新日志）→ 调用 `docs-writer`
- 需要**安全审计**（密钥/依赖）→ 调用 `security-guardian`
