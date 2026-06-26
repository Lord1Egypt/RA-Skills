# 色彩理论知识库 (Color Theory)

**用途**: IMA Studio AI 内容生成的色彩选择依据  
**版本**: v2.0 (2026-03-04)  
**贡献者**: 李鹤（资深设计师）  
**基于**: 色彩心理学、品牌设计实践、全球文化研究

---

## 📖 索引

本知识库按**知识模块**拆分，Agent 可按需加载相关内容：

### 🎨 核心知识

1. **[色彩心理学与应用](./color-psychology.md)** (~6KB)
   - 11种主要色彩的心理学分析
   - 情感效应、行业应用、色调变化
   - **适用**: 所有设计任务的基础

2. **[色彩搭配原则](./color-combinations.md)** (~1KB)
   - 5种搭配方法（单色、类比、互补、分裂互补、三色）
   - **适用**: 需要多色配色方案

3. **[行业色彩偏好速查表](./industry-guide.md)** (~1KB)
   - 10大行业的主色调和原因
   - **适用**: 特定行业设计

4. **[IMA Studio 应用策略](./application-strategy.md)** (~1KB)
   - 设计请求分析流程
   - 目标市场识别、文化冲突避免
   - **适用**: 所有设计任务

### 🌍 文化敏感性

5. **[文化差异速查](./cultural-differences.md)** (~1KB)
   - 5个主要地区的基础色彩文化（中国/美国/日本/印度/中东）
   - **适用**: 快速文化检查

6. **[全球地区色彩详解](./global-regions.md)** (~2KB)
   - 撒哈拉以南非洲、拉美、东南亚、东欧/俄罗斯
   - 详细的地区色彩禁忌和偏好
   - **适用**: 面向特定地区的设计

7. **[宗教色彩符号系统](./religious-systems.md)** (~3KB)
   - 5大宗教的色彩体系（基督教/佛教/犹太教/印度教/伊斯兰教）
   - 礼仪色彩、节日色彩、禁忌
   - **适用**: 宗教相关或文化敏感设计

---

## 🎯 快速导航

### 按任务类型

| 任务类型 | 推荐加载 |
|---------|---------|
| **通用设计** | color-psychology + color-combinations + application-strategy |
| **特定行业** | + industry-guide |
| **全球市场** | + cultural-differences + global-regions |
| **宗教/节日** | + religious-systems |
| **文化敏感** | 全部加载 |

### 按地区/宗教

| 地区/宗教 | 文档 |
|----------|------|
| 中国 | cultural-differences (基础) |
| 美国/西方 | cultural-differences (基础) |
| 日本/印度/中东 | cultural-differences (基础) |
| 非洲/拉美/东南亚 | global-regions (详细) |
| 基督教/佛教/犹太教/印度教/伊斯兰教 | religious-systems (详细) |

---

## 📊 知识库统计

| 模块 | 大小 | 核心内容 |
|------|------|---------|
| 色彩心理学 | ~6KB | 11种色彩详解 |
| 搭配原则 | ~1KB | 5种方法 |
| 行业速查 | ~1KB | 10大行业 |
| 应用策略 | ~1KB | 决策流程 |
| 文化速查 | ~1KB | 5个地区（基础） |
| 全球详解 | ~2KB | 4个地区（详细） |
| 宗教系统 | ~3KB | 5大宗教 |
| **总计** | **~15KB** | 模块化索引 |

---

## 🚀 Agent 使用指南

### 按需加载策略

**用户请求** → **识别需求** → **加载对应模块**

```
示例1: "设计一个科技公司 Logo"
→ 加载: color-psychology + industry-guide + application-strategy
→ 关注: 蓝色（信任、专业）

示例2: "为印度婚礼设计邀请函"
→ 加载: color-psychology + cultural-differences + religious-systems
→ 关注: 红色+金色（印度婚礼=红色，不是白色！）

示例3: "全球化品牌配色方案"
→ 加载: 全部模块
→ 关注: 文化中立色彩（蓝色、灰色）

示例4: "中东市场的电商设计"
→ 加载: color-psychology + cultural-differences + religious-systems
→ 关注: 绿色（伊斯兰教神圣）+ 避免不敬场合
```

### 快速决策流程

1. **识别行业** → 加载 `industry-guide.md`
2. **识别地区** → 加载 `cultural-differences.md` 或 `global-regions.md`
3. **检查宗教** → 加载 `religious-systems.md`（如需要）
4. **选择色彩** → 加载 `color-psychology.md`
5. **配色方案** → 加载 `color-combinations.md`
6. **执行策略** → 加载 `application-strategy.md`

---

## 📋 设计前检查清单

Agent 在选择色彩前应检查：

- [ ] 目标市场是哪里？
- [ ] 主要宗教是什么？
- [ ] 选用的色彩在该文化中意味着什么？
- [ ] 是否与葬礼/哀悼相关？
- [ ] 是否与宗教核心色彩冲突？
- [ ] 节日期间是否有特殊色彩规定？
- [ ] 国旗色彩是否有法律规定？

---

## 📚 扩展阅读

- 设计禁忌 → [../design-pitfalls/README.md](../design-pitfalls/README.md)
- 年度流行趋势 → [../color-trends-2026.md](../color-trends-2026.md)
- 视觉一致性 → [../visual-consistency.md](../visual-consistency.md)

---

## 🔄 维护说明

### 定期更新内容

- **年度流行趋势** (每年1月): 更新 Pantone/WGSN 主流色
- **新兴市场** (按需): 添加新地区的色彩文化
- **宗教节日** (按需): 补充重要节日色彩系统

### 贡献方式

本知识库基于李鹤（资深设计师）的专业经验凝练，欢迎持续补充：
- 新的文化差异案例
- 行业最佳实践
- 失败案例教训

---

**版本历史**:
- v1.0 (2026-03-03): 单文件版本 (37KB)
- v2.0 (2026-03-04): 模块化拆分，按需加载

**最后更新**: 2026-03-04
