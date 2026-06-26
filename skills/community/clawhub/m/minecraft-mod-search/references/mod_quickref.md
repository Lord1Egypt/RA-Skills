# Mod 快查表 (mod_quickref.md)

> **用途**：AI 优先在此表中匹配用户意图，命中即直接推荐，无需调用 API。
>
> **格式**：`- 英文名 [| 中文名] | slug: xxx | 功能描述 | 支持加载器和版本`
>
> **数据来源**：Modrinth 热门榜（2025-05 更新）+ 社区经典 Mod 整理
>
> **维护说明**：按 `## 分类` 组织，每行一个 Mod。如需更新，在对应分类下追加条目。

---

## 前置库 / API

- Fabric API | slug: fabric-api | Fabric 生态核心前置库，绝大多数 Fabric Mod 必须安装 | fabric 全版本
- Cloth Config API | slug: cloth-config | Mod 配置界面前置库，多数 Fabric/Forge Mod 需要 | fabric/forge 全版本
- Architectury API | slug: architectury-api | 跨平台 Mod 开发框架，支持 Fabric/Forge/NeoForge | fabric/forge/neoforge 全版本
- Fabric Language Kotlin | slug: fabric-language-kotlin | Kotlin 语言支持库，部分 Fabric Mod 需要 | fabric 全版本
- Yet Another Config Lib (YACL) | slug: yacl | 基于 Builder 的配置库 | fabric/forge 全版本
- Patchouli | slug: patchouli | Mod 内置手册/书籍系统前置库 | fabric/forge 全版本
- GeckoLib | slug: geckolib | 高级生物动画前置库 | fabric/forge 全版本
- Moonlight Lib | slug: moonlight | 多功能 Mod 开发库 | fabric/forge 全版本
- Puzzles Lib | slug: puzzles-lib | Fabric/Forge 跨平台工具库 | fabric/forge 全版本
- Trinkets | slug: trinkets | 扩展装备栏槽位的前置 API | fabric 全版本
- Curios API | slug: curios | 扩展装备栏槽位的前置 API（Forge 版） | forge/neoforge 全版本
- Quilted Fabric API (QFAPI/QSL) | slug: qsl | Quilt 生态核心前置库 | quilt 全版本

---

## 性能优化

- Sodium | slug: sodium | 最快速的 Minecraft 渲染优化，大幅提升 FPS | fabric/neoforge 1.16.5+
- Iris Shaders | slug: iris | 现代着色器加载器，兼容 OptiFine 光影包 | fabric 1.16.5+
- Lithium | slug: lithium | 游戏逻辑优化，提升服务器 TPS | fabric/neoforge 全版本
- FerriteCore | slug: ferrite-core | 内存占用优化 | fabric/forge 全版本
- Entity Culling | slug: entityculling | 异步路径追踪隐藏不可见实体，提升 FPS | fabric/forge 全版本
- ImmediatelyFast | slug: immediatelyfast | 即时渲染优化，提升 UI 和粒子效果帧率 | fabric/forge 全版本
- Sodium Extra | slug: sodium-extra | Sodium 的扩展功能（云、粒子等开关） | fabric 全版本
- Reese's Sodium Options | slug: reeses-sodium-options | Sodium 的备选选项界面 | fabric/neoforge 全版本
- ModernFix | slug: modernfix | 综合性能优化，减少内存占用，修复多个 Bug | fabric/forge 全版本
- Mobtimizations | slug: mobtimizations | 生物 AI 性能优化 | fabric/forge 全版本

---

## 信息显示 / UI / 辅助

- Jade 🔍 | slug: jade | 显示所指方块和实体的信息（HWYLA/WAILA 继任者） | fabric/forge 全版本
- Just Enough Items (JEI) | slug: jei | 物品配方查看 | fabric/forge 1.12+
- Roughly Enough Items (REI) | slug: rei | 物品配方查看（Fabric 主流选择）| fabric/forge 全版本
- EMI | slug: emi | 物品配方查看（功能最全的新一代工具）| fabric 全版本
- Xaero's Minimap | slug: xaeros-minimap | 小地图（支持实体、玩家显示）| fabric/forge 全版本
- Xaero's World Map | slug: xaeros-world-map | 全屏世界地图 | fabric/forge 全版本
- AppleSkin | slug: appleskin | 食物/饥饿值相关 HUD 改进 | fabric/forge 全版本
- Mod Menu | slug: modmenu | 游戏内 Mod 列表菜单 | fabric/quilt 全版本
- AmbientSounds | slug: ambientsounds | 根据生物群系播放环境音效 | fabric/forge 全版本
- Not Enough Animations | slug: not-enough-animations | 第一人称动作在第三人称显示 | fabric/forge 全版本

---

## 纹理 / 着色器 / 视觉

- [ETF] Entity Texture Features | slug: entitytexturefeatures | 支持资源包中的实体随机/自发光纹理 | fabric/forge 全版本
- [EMF] Entity Model Features | slug: entity-model-features | OptiFine 格式自定义实体模型替代 | fabric/forge 全版本
- Continuity | slug: continuity | 连接纹理（CTM）支持 | fabric 全版本
- BSL Shaders | slug: bsl-shaders | 高性能高质量光影包 | fabric/forge（需 Iris 或 OptiFine）
- Complementary Shaders | slug: complementary-shaders | 高性能光影包，适合低配机器 | fabric/forge（需 Iris）

---

## 存储 / 物流

- Tom's Simple Storage Mod | slug: toms-storage | 简单的类原版风格存储系统 | fabric/forge 全版本
- Applied Energistics 2 (AE2) | slug: ae2 | ME 网络存储系统，自动化物流核心 | fabric/forge 全版本
- Sophisticated Storage | slug: sophisticated-storage | 多层级升级箱子系统 | forge/neoforge 全版本
- Sophisticated Storage (Fabric) | slug: sophisticated-storage-(unofficial-fabric-port) | Sophisticated Storage 非官方 Fabric 版 | fabric 全版本
- Storage Drawers | slug: storagedrawers | 交互式批量存储抽屉 | fabric/forge 全版本
- Iron Chests: Restocked | slug: ironchests | 各种金属材质的大容量箱子 | fabric/forge 全版本

---

## 机械动力 / 自动化 / 科技

- Create (机械动力) | slug: create | 美观的机械自动化 Mod，齿轮传送带为核心 | forge 1.14.4-1.20.1
- Create Fabric (机械动力 Fabric 版) | slug: create-fabric | Create 官方 Fabric 版 | fabric 1.18.2-1.20.1
- Create: Steam 'n' Rails | slug: create-steam-n-rails | Create 铁路与蒸汽系统扩展 | forge/fabric 1.18.2+
- Create: Crafts & Additions | slug: createaddition | 为 Create 添加电力能源系统 | forge 1.16.5-1.20.1
- Create: Connected | slug: create-connected | Create 连接升级，新机械零件 | forge 1.18.2+
- Mekanism | slug: mekanism | 高科技机械、能源生产、自动化 | forge/neoforge 1.12+
- Mekanism Generators | slug: mekanism-generators | Mekanism 高级能源发电机 | forge/neoforge 全版本
- Thermal Expansion | slug: thermal-expansion | 科技能源 Mod 经典之作 | forge 全版本
- Applied Energistics 2 (AE2) | slug: ae2 | ME 网络自动化物流系统 | fabric/forge 全版本
- Industrial Foregoing | slug: industrial-foregoing | 工业自动化 Mod，大量机械 | forge 全版本
- Tinkers' Construct | slug: tinkers-construct | 工具冶炼改造系统，自定义工具属性 | forge 1.12.2-1.20.1

---

## 魔法 / 法术

- Botania | slug: botania | 自然魔法科技 Mod，花卉驱动的自动化 | fabric/forge 全版本
- Blood Magic | slug: blood-magic | 以血为代价的黑魔法系统 | forge 全版本
- Ars Nouveau | slug: ars-nouveau | 自定义咒语魔法系统 | fabric/forge 1.16.5+
- Iron's Spells 'n Spellbooks | slug: irons-spells-n-spellbooks | RPG 风格魔法书和法术系统 | forge 1.19.2+
- Electroblob's Wizardry | slug: wizardry | 经典魔杖法术系统 | forge 1.7-1.16
- Occultism | slug: occultism | 神秘学/召唤魔法 Mod | forge/neoforge 1.16.5+

---

## 冒险 / 地下城 / Boss

- Dungeons and Taverns | slug: dungeons-and-taverns | 大量新结构，地下城、酒馆等 | fabric/forge 1.19+
- Dungeons Arise | slug: dungeons-arise | 精心设计的地下城和建筑结构 | fabric/forge 1.16.5+
- Twilight Forest (黄昏森林) | slug: the-twilight-forest | 全新的黄昏维度，多个 Boss | forge 全版本
- Alex's Mobs | slug: alexs-mobs | 85+ 种高质量新生物 | forge 1.16.5+
- Vampirism | slug: vampirism | 成为吸血鬼或猎人的 RPG Mod | forge 全版本
- Mine and Slash | slug: mine-and-slash | 地牢类 RPG 系统，刷装备 | forge 1.18.2+
- L_Ender's Cataclysm | slug: cataclysm-mod | 史诗级 Boss 战斗 Mod | forge 1.18.2+
- AdventureZ | slug: adventurez | 新末地 Boss 和生物 | fabric 全版本

---

## NPC / 村民 / 幸存者 / 同伴

- Easy NPC | slug: easy-npc | 自定义 NPC 和对话系统，可用于世界构建 | fabric/forge 1.19.2+
- CustomNPC+ | slug: customnpc-plus | 可高度自定义的 NPC 添加 Mod | forge 1.16.5+
- Human Companions | slug: human-companions | 添加中立幸存者 NPC，可自然生成于世界中 | fabric 1.20.1
- Guard Villagers | slug: guard-villagers | 防御村庄的卫兵 NPC | fabric/datapack 全版本
- Villager Guards | slug: villager-guards | 自动生成卫兵保护村民 | datapack 全版本
- NPC Variety | slug: npc-variety | 为村民添加不同外貌肤色多样性 | fabric/forge 全版本
- Player2 AI NPC | slug: player2npc | AI 驱动的 NPC 同伴 | fabric 1.20.1
- Companion | slug: companion | 添加可跟随的同伴 NPC | fabric 1.19.2+
- Illager Invasion | slug: illager-invasion | 加强灾厄袭击，更多灾厄变种 | fabric/forge 1.16.5+

---

## 食物 / 农业 / 烹饪

- Farmer's Delight | slug: farmers-delight | 温馨的农业和烹饪扩展 | forge 1.16.5+
- Farmer's Delight Refabricated | slug: farmers-delight-refabricated | Farmer's Delight 的 Fabric 移植版 | fabric 1.18.2+
- Pam's HarvestCraft 2 - Food Core | slug: pams-harvestcraft-2-food-core | 大量食物和作物（Forge 经典之作） | forge 1.16.5+
- Croptopia | slug: croptopia | 80+ 种新作物和食物 | fabric/forge 全版本
- Cooking for Blockheads | slug: cookingforblockheads | 厨房家具和烹饪辅助系统 | fabric/forge 全版本
- Better Foods | slug: better-foods | 食物益处增强 | fabric 全版本

---

## 生物群系 / 世界生成

- Biomes O' Plenty | slug: biomesoplenty | 75+ 种新生物群系（Forge 经典） | forge 全版本
- Oh The Biomes You'll Go | slug: biomesyougo | 独特神奇的新生物群系 | fabric/forge 全版本
- Terralith | slug: terralith | 大幅改造原版地形生成，无新方块 | fabric/forge 1.18.2+
- William Wythers' Overhauled Overworld | slug: wwoo | 极其精细的主世界地形改造 | fabric/forge 1.18.2+
- Alex's Caves | slug: alexs-caves | 5 种全新地下洞穴生物群系 | forge 1.20.1
- Tectonic | slug: tectonic | 改善地形生成，更壮观的山脉和峡谷 | fabric/forge 1.18.2+

---

## 装饰 / 建筑 / 家具

- Macaw's Furniture | slug: macaws-furniture | 精美的现代家具集合 | fabric/forge 全版本
- Macaw's Roofs | slug: macaws-roofs | 各种形态的屋顶方块 | fabric/forge 全版本
- Supplementaries | slug: supplementaries | 大量原版风格的装饰性方块 | fabric/forge 全版本
- Decocraft | slug: decocraft | 300+ 种装饰物和家具 | forge 全版本
- MrCrayfish's Furniture Mod | slug: mrcrays-furniture-mod | 经典家具 Mod（Forge 传统选择） | forge 全版本
- Chipped | slug: chipped | 900+ 种方块材质变体 | fabric/forge 全版本
- Quark | slug: quark | 大量小型原版风格增强 | forge 全版本

---

## 传送 / 交通

- Waystones | slug: waystones | 石碑传送点，可设置家和传送网络 | fabric/forge 全版本
- Wraith Waystones | slug: fwaystones | 轻量级传送点系统 | fabric 全版本
- Create: Steam 'n' Rails | slug: create-steam-n-rails | Create 火车铁路系统 | forge/fabric 1.18.2+
- Immersive Railroading | slug: immersive-railroading | 逼真的铁路系统 | forge 1.10.2+

---

## 背包 / 装备扩展

- Traveler's Backpack | slug: travelersbackpack | 功能全面的旅行背包，含工具槽 | forge/neoforge 全版本
- Sophisticated Backpacks | slug: sophisticated-backpacks | 多级升级背包系统 | forge/neoforge 全版本
- Baubles | slug: baubles | 扩展佩戴槽（戒指、项链等） | forge 1.8-1.12
- Trinkets API | slug: trinkets | 饰品槽 API（Fabric 版） | fabric 全版本
- Curios API | slug: curios | 饰品槽 API（Forge/NeoForge 版） | forge/neoforge 全版本

---

## 枪械 / 武器 / 战斗

- Timeless and Classics Zero (TaCZ) | slug: timeless-and-classics-zero | 最沉浸的现代 FPS 枪械 Mod，支持枪包扩展 | forge 1.18.2-1.20.1
- Flintlock's Weapon Overhaul | slug: flintlock | 燧发枪/黑火药时代枪械（西部/历史风格）| forge 1.16.5+
- Epic Knights: Shields, Armor and Weapons | slug: epic-knights | 中世纪风格盾牌、盔甲、武器 | forge 1.16.5+
- Better Combat | slug: bettercombat | 武器动作系统，不同武器有不同攻击动作 | fabric/forge 1.18.2+
- Parry or Die | slug: parry-or-die | 格挡反击战斗系统 | fabric 1.20.1
- Epic Fight | slug: epicfight | 动作 RPG 战斗系统重制 | forge 1.16.5-1.20.1

---

## 多维度 / 探索

- Twilight Forest | slug: the-twilight-forest | 黄昏森林维度，完整 Boss 线 | forge 1.7.10+
- The Aether | slug: aether | 天空维度经典 Mod | forge 全版本
- The Bumblezone | slug: the-bumblezone | 蜜蜂维度 | fabric/forge 1.16.5+
- Undergarden | slug: undergarden | 神秘的地下新维度 | fabric/forge 1.16.5+
- Ad Astra | slug: ad-astra | 太空探索维度 | fabric/forge 1.19.2+

---

## 整合包常用前置 / 工具类

- Forge | slug: (loader) | Forge 加载器本体 | forge 全版本
- Fabric Loader | slug: (loader) | Fabric 加载器本体 | fabric 全版本
- Just Enough Resources (JER) | slug: just-enough-resources | 在 JEI 中显示资源生成概率 | forge/neoforge 全版本
- Clumps | slug: clumps | 将经验球合并，减少实体数量 | fabric/forge 全版本
- LazyDFU | slug: lazydfu | 减少启动时间（1.16-1.18 常用）| fabric 1.16-1.18
- Spark | slug: spark | 性能分析器，找出游戏卡顿来源 | fabric/forge 全版本
- No Chat Reports | slug: no-chat-reports | 禁用聊天举报功能（适用于私服）| fabric/forge 1.19+

---

## 语音 / 音频 / 视觉增强

- AmbientSounds | slug: ambientsounds | 生物群系环境音效 | fabric/forge 全版本
- Sound Physics Remastered | slug: sound-physics-remastered | 物理音效回音效果 | fabric/forge 全版本
- Presence Footsteps | slug: presence-footsteps | 根据地面材质播放不同脚步声 | fabric 全版本
- Dynamic Surroundings | slug: dynamic-surroundings | 动态天气、音效和视觉效果 | forge 1.12-1.16

---

## 关键词同义词对照表（AI 专用）

> 此表供快查表关键词匹配扩展使用：当用户输入以下关键词时，优先在上方分类中查找。

| 用户关键词 | 对应分类/Mod |
|-----------|-------------|
| 中立幸存者、幸存者 NPC、友好 NPC | NPC / 村民 / 幸存者 — Human Companions |
| 卫兵、护卫、守卫 | NPC / 村民 — Guard Villagers, Villager Guards |
| 光影、着色器 | 纹理 / 着色器 — Iris Shaders, BSL/Complementary Shaders |
| 小地图、地图 | 信息显示 — Xaero's Minimap, Xaero's World Map |
| 合成查看、配方 | 信息显示 — JEI / REI / EMI |
| 枪、枪械、枪包 | 枪械 / 武器 — TaCZ |
| 机械动力、自动化传送带 | 机械动力 — Create |
| 存储系统、ME | 存储 — AE2, Tom's Storage |
| 地下城、副本 | 冒险 / 地下城 — Dungeons Arise, Dungeons and Taverns |
| 新维度、维度 | 多维度 — Twilight Forest, Aether |
| 背包 | 背包 / 装备 — Traveler's Backpack, Sophisticated Backpacks |
| 西部枪械、历史枪 | 枪械 — Flintlock's Weapon Overhaul |
| 魔法、法术 | 魔法 — Botania, Ars Nouveau, Blood Magic |
| 农业、烹饪、食物 | 食物 / 农业 — Farmer's Delight |
| 传送、路点 | 传送 — Waystones |
| 新生物、怪物 | 冒险 — Alex's Mobs |
| 建筑、装饰、家具 | 装饰 / 建筑 — Macaw's, Supplementaries |
| 生物群系 | 世界生成 — Biomes O' Plenty, Terralith |
