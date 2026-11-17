---
name: pixel-art-studio
description: 像素艺术精灵生成与动画：16x16 精灵、有限调色板、sprite sheet 管理、游戏集成
source:
  type: derived
  repo: skills-repo/indie-game-developer
  path: skills/pixel-art-studio/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/omer-metin/skills-for-antigravity/pixel-art-sprites
metadata:
  category: 游戏美术
  platform: Web
  difficulty: 入门
---

# 像素艺术工坊

> 像素艺术精灵生成：每个像素都是设计决策，关注可读剪影、有限调色板、游戏场景下的视觉清晰度。

## 能力

- **角色精灵设计**：16×16 ~ 32×32 精灵的程序化生成，每个像素有意放置
- **动画原理**：4 帧动画比 8 帧更好——帧数越少设计决策越强
- **调色板设计**：有限色调色板（12 色），少即是多
- **Sprite Sheet 管理**：精灵表组织、分辨率与缩放考量
- **游戏引擎集成**：React + Canvas API，精灵在游戏场景中的实际表现

## 使用方式

```
/pixel-art-studio 生成一组像素角色精灵
/pixel-art-studio 为这个角色设计 4 帧行走动画
/pixel-art-studio 设计一个 12 色调色板用于暗色像素风游戏
```

## 设计哲学

- 可读剪影 > 美丽细节——缩小到 32px 时细节会丢失
- 硬边缘 > 抗锯齿——拥抱像素的硬边美学
- 少帧 > 多帧——最佳动画用最少的帧传达最多的信息
- 在 1x 缩放下如果认不出来，精灵就失败了

## 适用场景

- 像素风角色和精灵资源
- 游戏 tile 和 tileset
- 像素动画设计
- 复古/独立游戏美术

## 限制

- 仅覆盖像素风（16×16 ~ 32×32），不涉及其它美术风格
- 不涉及 3D 渲染
- 不涉及音频设计

> 本子技能属**像素美术执行层**（16×16~32×32 精灵 / 调色板 / sprite sheet）；方法层见 reference。

- 资源管线（精灵表打包 / 引用完整性）→ [`references/asset-pipeline.md`](../../references/asset-pipeline.md)
- 精致手绘像素角色方法 → [`references/refined-pixel-art-playbook.md`](../../references/refined-pixel-art-playbook.md)