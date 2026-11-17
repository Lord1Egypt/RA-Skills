# 游戏引擎与技术栈选型（Game Engine & Tech Selection）

> 子技能 `game-developer`(Three.js) / `pixel-art-studio` / `game-designer` / `steam-launch`
> 各自讲"怎么做"，本篇讲"先选哪条路"——独立游戏最贵的错误是中途换引擎。
> 先决策树定性，再矩阵定量，最后用清单收口。

## 1. 决策树（先定性）

```
Q0 目标平台是浏览器/Web 吗？
├─ 是 → Q0a 需要 3D 吗？
│       ├─ 是 → Three.js（game-developer），注意 WebGL 性能天花板
│       └─ 否（2D）→ Phaser / PixiJS（轻量、省心），或 Three.js 正交相机
└─ 否（Steam/主机/移动）→ Q1

Q1 团队有编程基础吗？
├─ 是，且要 3D → Godot（GDScript 易上手）/ Unity（生态最大但有抽成）
├─ 是，且要 2D 精致 → Godot（2D 一流）/ Unity 2D
└─ 否（美术/设计驱动）→ GameMaker / Godot 可视化脚本

Q2 商业考量
├─ 介意 Unity Runtime Fee → 优先 Godot（MIT，无抽成）
├─ 要最大招聘池/资产商店 → Unity
└─ 要 Web+桌面一体发布 → Three.js + Electron/Tauri 或 Godot Web 导出
```

**口诀**：Web 小游戏 → Three.js/Phaser；想上 Steam 且轻量无抽成 → Godot；要生态与 3A 工具链 → Unity；纯美术驱动 → GameMaker。

## 2. 选型矩阵（定量）

| 维度 | Three.js (Web) | Phaser (Web 2D) | Godot | Unity |
|------|----------------|-----------------|-------|-------|
| 渲染 | WebGL/3D | Canvas/WebGL 2D | OpenGL/Vulkan 2D+3D | 多后端 2D+3D |
| 语言 | JS/TS | JS/TS | GDScript/C# | C# |
| 学习曲线 | 中（裸 API） | 低 | 低-中 | 中-高 |
| 包体积 | 小（库 ~600KB） | 小 | 小（引擎自带） | 大（运行时 MB 级） |
| 分发 | 网页/链接 | 网页/链接 | Steam/Web/移动 | Steam/全平台 |
| 商业 | 免费 | 免费 | MIT 免费 | 抽成（过阈值） |
| 生态/资产 | npm 海量 | 中 | 中（Asset Library） | 最大（Asset Store） |
| 物理 | 需 ammo/cannon | arcade/matter | 内置 | 内置(Unity Physics) |
| 适合 | 浏览器 3D 实验 | H5 小游戏 | 独立全平台 | 中大型/团队 |

## 3. 2D vs 3D 的隐性成本

- **2D 不等于简单**：精灵表管理、帧动画、图集打包、像素对齐都是真功夫（见 `pixel-art-studio` 与 [references/asset-pipeline.md](asset-pipeline.md)）
- **3D 的坑在性能与资产**：模型面数、骨骼、贴图尺寸、光照烘焙，WebGL 下尤甚；移动端 GPU 是硬约束
- **伪 3D / 2.5D**：用 2D 精灵 + 视差/缩放伪造景深，往往比真 3D 更快出货且性能友好（独立游戏常用）

## 4. Web(Three.js) 专项决策

选 Three.js 后还要定：
- **渲染后端**：WebGL2（默认）；考虑 WebGPU（新浏览器，性能更好但兼容差）
- **构建**：Vite + three；用 `tree-shaking` 只打用到的模块（Three 全量很大）
- **资源加载**：GLTFLoader（标准 `glb`），别用 OBJ（无材质/动画）
- **发布**：静态托管即可；上 Steam 用 Electron/Tauri 套壳或 Godot 重做

## 5. 典型坑与规避

- **坑：为"以后可能做 3D"选 Unity，结果 90% 是 2D 还背着引擎重量**。*规避*：按当下需求选，Godot 2D 更轻；真要 3D 再评估。
- **坑：Three.js 全量引入导致首屏几 MB**。*规避*：按需 import，配 Vite 分包；`three/examples/jsm` 按需引。
- **坑：跨平台输入不统一**（触屏/键鼠/手柄）。*规避*：抽象输入层，早点支持手柄（Steam 玩家用手柄）。
- **坑：Web 音频自动播放被浏览器拦截**。*规避*：用户首次交互后再 `AudioContext.resume()`。
- **坑：Godot/Unity 版本升级破坏性**。*规避*：锁版本，升级单列任务，不随缘更。

## 6. 收口清单

- [ ] 用 §1 决策树定出引擎，并写下"为何不选其它两个"的反向论证
- [ ] 用 §2 矩阵确认 3 个最关键维度（平台/团队/商业）与现状匹配
- [ ] 明确 2D / 3D / 2.5D 路线与性能预算
- [ ] Web 路线已定渲染后端、构建工具、资源加载格式
- [ ] 商业模型确认（抽成阈值、定价空间）
- [ ] 输入层抽象与手柄支持计划已列
- [ ] 引擎版本已锁定，升级路径单列
- [ ] 选型结论同步给 `game-developer` / `pixel-art-studio` / `steam-launch`

## 7. 与子技能衔接

- Web 3D → `game-developer`（Three.js 全流程）
- 像素美术 → `pixel-art-studio`（精灵/调色板/精灵表）
- 视觉打磨 → `game-designer`（调色板/粒子/手感/UI）
- 上 Steam → `steam-launch`（商店页/愿望单/Next Fest）
- 资源管线 → 见 [references/asset-pipeline.md](asset-pipeline.md)
- 发布 QA → 见 [references/game-qa-perf.md](game-qa-perf.md)

## 8. 发布路径：Web → Steam 的几种走法

选定引擎后，分发路径决定打包方式：

| 目标 | Web 直发 | Steam(套壳) | Steam(原生引擎) |
|------|----------|-------------|-----------------|
| Three.js | 静态托管，链接即玩 | Electron/Tauri 套壳 | 不适用 |
| Phaser | 静态托管 | Electron/Tauri | 不适用 |
| Godot | 导出 HTML5 | 导出的 HTML5 + 套壳 | 直接导 Windows/Mac/Linux |
| Unity | WebGL 导出 | WebGL + 套壳 | 直接导三端 |

**关键决策**：若核心市场是 Steam，且游戏偏重，直接 Godot/Unity 原生导出比"Web 套壳"体验好得多（套壳体积大、启动慢、手柄支持别扭）。Web 套壳适合"先试玩引流 → 引导去 Steam 买完整版"的组合打法。

## 9. 团队规模与长期维护成本

- **1 人 solo**：优先低维护成本（Godot/Phaser），引擎更新别追新，锁版本
- **2–5 人小队**：Godot 或 Unity 均可，重视协作（版本控制、资产管线规范）
- **需招人扩张**：Unity 招聘池最大，但抽成与复杂度上升
- **美术主导无程序**：GameMaker/Godot 可视化，但要接受能力天花板

维护隐性成本别忽略：引擎大版本升级、第三方插件停更、构建环境漂移。锁版本 + 容器化构建环境能省大量复活时间。

## 10. 引擎迁移的止损信号

出现 ≥2 条，考虑换引擎（成本高风险大，慎）：

- 现引擎在目标平台性能天花板无法绕过，且非业务层可调
- 关键能力（如手柄/某平台导出）引擎不支持且无插件
- 抽成/许可变更导致商业模型不可行
- 团队技能与引擎严重错配，招聘长期无解

迁移顺序（渐进式，参考 [references/asset-pipeline.md](asset-pipeline.md) 的资源解耦）：先抽离资源与数据格式（glb/精灵表/配置 JSON），再换渲染层，业务逻辑最后迁。资源解耦做得好，换引擎主要重写渲染与输入。

## 11. 反向论证模板（收口必写）

> 我选〔引擎〕不选〔A〕/〔B〕：① 〔A〕在〔维度〕不满足〔约束〕；
> ② 团队有〔技能〕可立刻上手；③ 〔风险〕有〔缓解〕。若未来〔触发〕，则回到 §10 评估迁移。

## 相关子技能与层次边界

> 本文属**引擎选型方法层**（决策树 + 矩阵 + 发布路径）；具体开发与视觉打磨交给子技能。

- 落地「Three.js 浏览器游戏开发」→ [`skills/game-developer/SKILL.md`](../skills/game-developer/SKILL.md)
- 落地「游戏视觉设计与打磨」→ [`skills/game-designer/SKILL.md`](../skills/game-designer/SKILL.md)
- 兄弟参考：资源解耦与可迁移性 → [references/asset-pipeline.md](asset-pipeline.md) §12
- 兄弟参考：选型后的 QA / 性能基线 → [references/game-qa-perf.md](game-qa-perf.md)

