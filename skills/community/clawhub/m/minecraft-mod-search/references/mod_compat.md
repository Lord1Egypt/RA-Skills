# Minecraft Java Mod 兼容性矩阵

## 1. 加载器兼容性（最核心规则）

### Forge / Fabric / Quilt 不可互通

| Mod 加载器 | Forge Mod | Fabric Mod | Quilt Mod |
|-----------|-----------|-----------|-----------|
| Forge | ✅ 兼容 | ❌ 不兼容 | ❌ 不兼容 |
| Fabric | ❌ 不兼容 | ✅ 兼容 | ✅ 兼容 |
| Quilt | ❌ 不兼容 | ✅ 兼容 | ✅ 兼容 |

> ⚠️ **核心原则**：整合包必须选择单一加载器。Forge 和 Fabric 的 Mod 生态完全不互通，混装会导致游戏崩溃。

### Forge vs Fabric 生态选择建议

| 需求 | 推荐加载器 | 理由 |
|------|----------|------|
| 科技类大型 Mod（Create/Mekanism/IE） | **Forge** | Forge 科技 Mod 生态最成熟 |
| 轻量优化 Mod（Sodium/Lithium） | **Fabric** | Fabric 优化 Mod 性能更优 |
| 纯 1.20.4+ 最新版本 | **Fabric/Quilt** | 部分新 Mod 仅 Fabric |
| 1.12.2 / 1.7.10 老版本 | **Forge** | 历史版本无 Fabric 支持 |
| 混合需求（科技+优化） | **Forge** | 推荐 OptiFine（非 Sodium） |

---

## 2. 优化 Mod 互斥关系

### 帧率优化 Mod 兼容性表

| Mod | Sodium | Lithium | Phosphor | OptiFine | Iris | Embeddium | Rubidium |
|-----|--------|---------|---------|----------|------|-----------|----------|
| **Sodium** | — | ✅ 兼容 | ✅ 兼容 | ❌ **互斥** | ✅ 兼容 | ❌ 互斥 | ❌ 互斥 |
| **Lithium** | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Phosphor** | ✅ 兼容 | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **OptiFine** | ❌ **互斥** | ✅ 兼容 | ✅ 兼容 | — | ❌ **互斥** | ❌ 互斥 | ❌ 互斥 |
| **Iris** | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ❌ **互斥** | — | ❌ 互斥 | ❌ 互斥 |
| **Embeddium** | ❌ **互斥** | ✅ 兼容 | ✅ 兼容 | ❌ **互斥** | ❌ **互斥** | — | ❌ 互斥 |
| **FerriteCore** | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |

> 💡 **规则**：OptiFine 与 Sodium/Iris 功能重叠，只能选择其一。Fabric 生态推荐 Sodium + Iris；Forge 生态推荐 OptiFine。

### 渲染/光照 Mod 兼容性

| Mod | Sodium | OptiFine | Iris | Continuity | Oculus | Rubidium |
|-----|--------|----------|------|------------|--------|----------|
| **Sodium** | — | ❌ 互斥 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ❌ 互斥 |
| **OptiFine** | ❌ 互斥 | — | ❌ 互斥 | ❌ 需 OptiFine | ❌ 需 OptiFine | ❌ 互斥 |
| **Iris** | ✅ 兼容 | ❌ 互斥 | — | ✅ 兼容 | ❌ 互斥 | ❌ 互斥 |

---

## 3. 存储 Mod 互斥关系

| Mod | AE2 | RS | Storage Drawers | Refined Storage | Industrial Foregoing | Simple Storage Network |
|-----|-----|----|----------------|-----------------|--------------------|----------------------|
| **AE2** | — | ❌ **互斥** | ✅ 兼容 | ❌ **互斥** | ✅ 兼容 | ✅ 兼容 |
| **Refined Storage** | ❌ **互斥** | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Storage Drawers** | ✅ 兼容 | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Industrial Foregoing** | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | — | ✅ 兼容 |

> ❌ **硬性互斥**：AE2 和 Refined Storage（RS）不可同时启用，只能选择其一。

---

## 4. 信息展示 Mod 互斥关系

| Mod | Jade | WTHIT | Hwyla | AppleSkin | Xaero's Minimap |
|-----|------|-------|-------|-----------|-----------------|
| **Jade** | — | ⚠️ **二选一** | ⚠️ **二选一** | ✅ 兼容 | ✅ 兼容 |
| **WTHIT** | ⚠️ **二选一** | — | ⚠️ **二选一** | ✅ 兼容 | ✅ 兼容 |
| **Hwyla** | ⚠️ **二选一** | ⚠️ **二选一** | — | ✅ 兼容 | ✅ 兼容 |

> 💡 Jade 为 WTHIT/Hwyla 的现代替代品，功能完全重叠，保留 Jade 即可。

---

## 5. 物品查看 Mod 互斥关系

| Mod | REI | EMI | Jade's Browse | Just Enough Items | Roughly Enough Items |
|-----|-----|-----|---------------|------------------|--------------------|
| **REI** | — | ❌ **互斥** | ❌ 需前置 | ❌ 互斥 | ❌ 互斥 |
| **EMI** | ❌ **互斥** | — | ❌ 需前置 | ❌ 互斥 | ❌ 互斥 |

> ❌ **REI / EMI / JEI 互斥**，三选一。EMI 为 REI 的现代 Fabric 替代品。

---

## 6. 科技 Mod 兼容性

### Forge 科技 Mod 联动兼容性

| Mod | Create | Mekanism | Immersive Eng. | Industrial Foregoing | Tech Reborn | Thermal Series |
|-----|--------|----------|---------------|--------------------|-----------|---------------|
| **Create** | — | ✅ 兼容* | ✅ 兼容* | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Mekanism** | ✅ 兼容* | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Immersive Eng.** | ✅ 兼容* | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Industrial Foregoing** | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 |
| **Tech Reborn** | ✅ 兼容 | ⚠️ 能源单位差异 | ⚠️ 能源单位差异 | ✅ 兼容 | — | ⚠️ 能源单位差异 |
| **Thermal Series** | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ⚠️ 能源单位差异 | — |

> * 表示存在专用联动 Mod（如 Create 的 Create: Contraption Utils 可联动 Mekanism 管道）

### 能源单位差异说明

| Mod | 默认能源单位 | 与其他 Mod 联动方式 |
|-----|-----------|------------------|
| Mekanism | RF / 通用 | 通过 KubeJS / Create 管道转换 |
| Immersive Engineering | IF (IguanaTweaks) | 需插件转换 |
| Tech Reborn | EU / RF | 部分支持 RF |
| Thermal Series | RF | 行业标准，兼容性最广 |

### Create 联动 Mod 矩阵

| 联动 Mod | 兼容性 | 说明 |
|---------|--------|------|
| Create + Mekanism | ✅ 兼容 | 通过 KubeJS 或 Create 管道连接 |
| Create + Refined Storage | ✅ 兼容 | 需 Refined Storage Addon |
| Create + AE2 | ✅ 兼容 | 需 AE2 Additions |
| Create + Immersive Engineering | ✅ 兼容 | 需 IE Create 补丁 |
| Create + Create Astral | ⚠️ 需注意 | 两者都修改世界生成 |

---

## 7. 魔法 Mod 兼容性

| Mod | Thaumcraft | Botania | Blood Magic | Electroblob's Magic | Mahou Tsukai |
|-----|-----------|---------|------------|---------------------|-------------|
| **Thaumcraft** | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 | ⚠️ 可能有 Aspect 冲突 |
| **Botania** | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 | ✅ 兼容 |
| **Blood Magic** | ✅ 兼容 | ✅ 兼容 | — | ✅ 兼容 | ✅ 兼容 |

> 魔法 Mod 之间通常兼容，但注意 Aspect 系统（Thaumcraft）和标签系统可能的命名冲突。

---

## 8. 常用前置依赖 Mod

这些 Mod 通常为其他 Mod 提供底层支持，应优先安装：

| 依赖 Mod | 用途 | 需要它的主要 Mod |
|---------|------|----------------|
| **Fabric API** | Fabric 底层支持 | 几乎所有 Fabric Mod |
| **Architectury API** | Fabric/Forge 跨兼容层 | Cloth Config, REI 等 |
| **Cloth Config API** | 配置界面 | 大量 Mod 的 GUI 依赖 |
| **GeckoLib** | 动画支持 | 大量 Mod |
| **KubeJS** | 脚本/定制 | Create Addon, 科技包联动 |
| **EMI** | EMI 依赖（Fabric） | EMI 本身 |

---

## 9. 已知冲突 Mod 组合

以下组合同时安装会导致崩溃、功能异常或性能下降，**应避免**：

### 硬性冲突（崩溃）

| 组合 | 原因 | 解决方案 |
|------|------|---------|
| Forge Mod + Fabric Mod | 加载器不兼容 | 选择同一加载器 |
| OptiFine + Sodium/Iris | 渲染引擎冲突 | 只选其一 |
| AE2 + Refined Storage | 存储系统冲突 | 只选其一 |
| 不兼容游戏版本的 Mod | 版本不匹配 | 换版本或换 Mod |

### 功能重叠（性能浪费）

| 组合 | 原因 | 建议 |
|------|------|------|
| OptiFine + Sodium | 都优化渲染 | Forge 选 OptiFine，Fabric 选 Sodium |
| Jade + WTHIT/Hwyla | 功能完全重叠 | 只留 Jade |
| REI + EMI + JEI | 物品查看功能重叠 | 只留一个 |
| Xaero's Minimap + JourneyMap | 地图功能重叠 | 只留一个 |

### 潜在兼容性问题（需测试）

| 组合 | 风险等级 | 说明 |
|------|---------|------|
| Create + 大型科技包 | 🟡 中 | 物品处理逻辑可能冲突，测试后再用 |
| Lithium + 某些 AI 相关 Mod | 🟡 中 | 极少数 Mod 的 AI 改动与 Lithium 冲突 |
| 多版本同一功能 Mod | 🟡 中 | 如多个生物群系生成 Mod 可能互相覆盖 |

---

## 10. 版本特定兼容性速查

### 1.20.4 版本

| Mod | 1.20.4 兼容性 | 备注 |
|-----|-------------|------|
| Sodium | ✅ | 0.5.8+ 支持 |
| Create | ✅ | 0.1.x 支持 |
| Mekanism | ✅ | 10.3.x 支持 |
| Immersive Engineering | ✅ | 9.x 支持 |
| AE2 | ✅ | 2.12.x 支持 |
| Refined Storage | ✅ | 1.11.x 支持 |
| OptiFine | ✅ | HD_U_I6 支持 |
| Fabric API | ✅ | 0.100.x 支持 |

### 1.19.4 版本

| Mod | 1.19.4 兼容性 | 备注 |
|-----|-------------|------|
| Sodium | ✅ | 0.4.x 支持 |
| Create | ✅ | 0.5.x 支持 |
| Mekanism | ✅ | 10.2.x 支持 |
| Immersive Engineering | ✅ | 8.x 支持 |
| AE2 | ✅ | 2.10.x 支持 |
| Refined Storage | ✅ | 1.11.x 支持 |
| OptiFine | ✅ | HD_U_I5 支持 |
| Fabric API | ✅ | 0.87.x 支持 |

### 1.18.2 版本

| Mod | 1.18.2 兼容性 | 备注 |
|-----|-------------|------|
| Sodium | ✅ | 0.4.x 支持 |
| Create | ✅ | 0.4.x 支持 |
| Mekanism | ✅ | 10.1.x 支持 |
| AE2 | ✅ | 2.6.x 支持 |
| OptiFine | ✅ | HD_U_H8 支持 |

---

## 11. 整合包兼容性检查流程

在推荐整合包 Mod 时，按以下顺序检查兼容性：

### Step 1: 加载器统一性
```
检查所有 Mod 是否使用同一加载器（Forge 或 Fabric）
→ 如发现混合，立刻报告并要求用户选择加载器
```

### Step 2: 硬性互斥检查
```
遍历所有已知互斥组合（optifine↔sodium, ae2↔rs, rei↔emi）
→ 发现任何互斥，给出"二选一"建议
```

### Step 3: 依赖完整性
```
对每个推荐 Mod 提取 dependencies
→ 补全所有 required 依赖
→ 递归检查依赖的依赖
```

### Step 4: 版本兼容性
```
检查 target_version 是否在每个 mod.game_versions 中
→ 不兼容的标记 [🚫 版本不兼容] 并提供替代
```

### Step 5: 功能重叠检查
```
检测多个功能完全相同的 Mod（如多个生物群系 Mod）
→ 提示用户选择其一
```

---

## 12. TACZ 枪械生态（Gun Mod 专项）

### 12.1 什么是 TACZ

**Timeless and Classics Zero（永恒枪械工坊：零）** 是 Java 版枪械 Mod 的主流分支，由原 TaC 团队完全重写。

| 项目 | 内容 |
|------|------|
| **Modrinth slug** | `timeless-and-classics-zero` |
| **加载器** | Forge（1.18.2 / 1.19.x / 1.20–1.20.1）；NeoForge 社区移植版 |
| **Fabric 移植** | `tacz-refabricated`（非官方移植） |
| **前置依赖** | Cloth Config API（可选，用于配置 GUI） |
| **下载量** | 17M+（Modrinth，2026 年） |
| **许可证** | 代码 GPL-3.0-only；资源 CC BY-NC-ND 4.0 |

### 12.2 枪包（Gun Pack）机制

TACZ 的核心特性是**可扩展枪包**：无需写代码，以 `.zip` 格式分发，放入游戏目录即可加载。

**安装路径：**

| TACZ 版本 | 枪包存放路径 |
|-----------|------------|
| ≤ 1.0.3   | `.minecraft/config/tacz/custom/` |
| ≥ 1.1.4   | `.minecraft/tacz/` |

> ⚠️ 1.1.4 版本起，枪包文件格式发生了重大升级，旧格式枪包需按官方迁移指南转换后才能使用。

**枪包格式：**
- 文件格式：`.zip` 压缩包（或开发调试时用文件夹）
- 命名空间：仅支持小写英文字母、数字、下划线，不支持中文
- 重载命令：`/tacz reload` 或 `/reload`

### 12.3 枪包在 Modrinth 上的搜索策略

枪包发布在 Modrinth 上时，通常具备以下特征：

| 字段 | 典型值 |
|------|--------|
| `categories` | 包含 `equipment`，部分还有 `adventure`、`game-mechanics` |
| `loaders` | 通常为空（枪包是资源包/数据包形式，非 Jar Mod） |
| 标题关键词 | 包含 `tacz`、`gun pack`、`gunpack`、`TaCZ` |

**搜索方式（优先级排序）：**

1. `query="tacz <枪械关键词>" + category="equipment"` → 最精准
2. `query="tacz gunpack"` → 泛搜
3. `query="<枪械关键词> gun pack"` → 回退到普通 Mod 搜索

### 12.4 已知主流 TACZ 枪包（参考）

| 枪包名称 | 风格 | 来源 |
|---------|------|------|
| Hell Divers2 Gun Pack | 科幻/现代战争（地狱潜兵2） | CurseForge |
| TTI Gun Pack | 战术改装枪械 | Modrinth |
| The Division Gunpack | 现代战术（全境封锁） | Modrinth |
| ARIP Attachments Pack | 配件包 | Modrinth |
| EMX-Arms Gunpack | 现代步枪 | Modrinth |
| Fallout Gunpack (unofficial) | 废土末日 | Modrinth |
| LesRaisins Append Pack | 投掷物+近战+枪械 | Modrinth |

> 上述列表仅供参考，实际枪包持续更新，以 Modrinth 搜索结果为准。

### 12.5 枪械 Mod 兼容性规则

| 规则 | 说明 |
|------|------|
| TACZ 与其他枪械 Mod | 可共存，但 UI 和弹药系统各自独立 |
| 多枪包共存 | ✅ TACZ 支持同时加载多个枪包，命名空间不冲突即可 |
| Forge 版 TACZ + Fabric Mod | ❌ 不兼容，加载器限制 |
| OptiFine 与 TACZ | ⚠️ 部分光影效果与 TACZ 模型动画可能冲突，优先用 Oculus |

---

## 13. Create 机械动力生态（Technology Mod 专项）

### 13.1 什么是 Create

**Create（机械动力）** 是 Minecraft 中最受欢迎的美学科技/自动化 Mod 之一，以旋转力学（齿轮、轴承、传送带）和视觉精美的机械动画著称。

| 项目 | 内容 |
|------|------|
| **Modrinth slug** | `create` |
| **加载器** | Forge + Fabric（官方双平台支持） |
| **前置依赖** | Flywheel（渲染引擎，Forge 版）；Fabric 版无额外前置 |
| **下载量** | 16M+（Modrinth，2026 年） |
| **许可证** | MIT |
| **支持版本** | 1.14.4 / 1.15.2 / 1.16.5 / 1.18.2 / 1.19.2 / 1.20.1 |

### 13.2 核心机制

Create 的核心是**旋转动力学系统（Rotational Dynamics）**：

- **应力（Stress）**：每个机械组件有应力消耗值，动力源提供应力容量，超载则机械停止
- **转速（RPM）**：通过齿轮比和大小区分调整转速
- **动力传递**：齿轮 → 轴 → 皮带 → 传送带等形成动力网络

### 13.3 附属 Mod 在 Modrinth 上的搜索策略

Create 附属 mod 在 Modrinth 上的特征：

| 字段 | 典型值 |
|------|--------|
| `categories` | 主要为 `technology`，部分在 `equipment`、`transportation`、`utility`、`decoration` |
| `loaders` | 依具体 mod 而定（大多数支持 Forge，部分支持 Fabric） |
| 标题关键词 | 大多包含 "Create" 或 "Create:" 前缀 |

**搜索方式（优先级排序）：**

1. `query="create <关键词>" + facets=[technology, version]` → 最精准，命中率最高
2. `query="create <关键词>" + facets=[version]` → 无分类限制的泛搜

### 13.4 已知主流 Create 附属 Mod（参考）

| 附属 Mod | 功能 | 下载量 | 加载器 |
|---------|------|--------|--------|
| Create: Steam 'n' Rails | 铁路扩展 + 蒸汽系统 | 8.9M | Forge / Fabric |
| Create Crafts & Additions | 电力↔动力转换 + 新组件 | 7.0M | Forge / Fabric |
| Create Slice & Dice | Farmer's Delight 自动化集成 | 4.9M | Forge / Fabric |
| Create Deco | 建筑装饰方块 | 4.7M | Forge / Fabric |
| Create Big Cannons | 大炮武器系统 | 4.0M | Forge / Fabric |
| Create: New Age | 电力系统扩展 | 3.7M | Forge |
| Create: Central Kitchen | 大型厨房自动化 | 3.5M | Forge |
| Create: Enchantment Industry | 自动附魔系统 | 3.3M | Forge / NeoForge |
| Create: Copycats+ | 复制方块建筑工具 | 6.2M | Forge / Fabric |
| Create: Bells & Whistles | 列车信号系统 | 3.0M | Forge / Fabric |

> 上述列表仅供参考，实际附属 mod 持续更新，以 Modrinth 搜索结果为准。

### 13.5 Create Mod 兼容性规则

| 规则 | 说明 |
|------|------|
| Create + 其他科技 Mod | ✅ 可与 Mekanism、IE 等共存，但注意不要让两个系统做同一件事 |
| Create + 其他自动化 Mod | ⚠️ Create 与 Mekanism/AE2 有功能重叠（物流传输），应明确分工 |
| Create Forge + Create Fabric | ✅ 两个版本功能基本一致，选择对应加载器的版本 |
| Create + OptiFine | ❌ 不兼容！Create 依赖 Flywheel，与 OptiFine 冲突。Forge 用 Oculus，Fabric 用 Iris |
| Create + Sodium | ✅ Fabric 版 Create 兼容 Sodium |
| Create + Immersive Engineering | ✅ 可共存，风格互补（Create 偏美学，IE 偏写实） |
| Create + Applied Energistics 2 | ✅ 常见组合：AE2 做存储，Create 做加工 |
