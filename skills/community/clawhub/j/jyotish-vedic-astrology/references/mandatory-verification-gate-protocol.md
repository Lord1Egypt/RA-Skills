# 强制外部验证门控协议（Mandatory External Verification Gate, MEVG）

> **版本**：v1.0.0 | **创建日期**：2026-04-27
> **来源标签**: 【核心方法论·Skill整合】 — 强制外部验证门控协议
> **优先级**：⭐⭐⭐⭐⭐（与"不跳步"原则同级，违反即判定分析无效）
> **触发场景**：所有涉及星盘解读（静态/动态/预测）的分析输出

---

## ⚠️ 核心问题（本协议解决什么）

**AI 的训练数据中包含大量印度占星知识，但这些知识存在以下问题**：

1. **流派偏差**：训练数据偏重 Parashara 主流，对 Jaimini/Tajika/Nadi 等分支覆盖不足
2. **断章取义**：许多规则缺少前提条件（如"Malavya Yoga 一定好"忽略了落宫/相位/Dasha 的修正）
3. **缺乏具体性**：训练知识是通用描述，无法覆盖每个用户独特的行星配置组合
4. **过时信息**：部分训练数据可能是旧版规则或已被修正的误判
5. **文化偏见**：西方占星与印度占星混同，导致概念混淆

**本协议强制要求：所有解读结论必须经过外部权威来源验证，禁止仅凭 AI 训练记忆输出。**

---

## 一、门控触发条件

### 1.1 必须触发 MEVG 的场景

| 场景 | 触发时机 | 验证类型 |
|------|---------|---------|
| **Yoga 识别与解读** | 阶段三 Step 3.3 | 搜索该 Yoga 的经典定义+应用条件+案例 |
| **行星尊严判断** | 阶段三 Step 3.1 | 搜索特定行星+星座+宫位组合的权威解读 |
| **Transit 效应解读** | 阶段四 Step 4.3-4.4 | 搜索该 Transit 对特定上升的实际效应 |
| **Dasha 周期解读** | 阶段四 Step 4.1-4.2 | 搜索该行星组合 Dasha 的经典描述+案例 |
| **应期预测** | 阶段五全部 | 搜索相似命盘的真实事件案例 |
| **补救措施** | 阶段六 | 搜索该补救措施的权威来源+禁忌 |

### 1.2 可免 MEVG 的场景（纯计算/数据提取）

- 引擎数值计算（Shadbala 分数、SAV 点数、Dasha 时间线）
- PDF 数据提取（落宫、度数、Nakshatra）
- 数学验证（R1-R10 校验、SAV=337 检查）

---

## 二、验证协议（三步法）

### Step V1：构建检索查询

**查询模板**（每个主要解读点至少生成 1 个查询）：

```
# Yoga 解读
"[Yoga名] Vedic astrology effects [上升星座] ascendant"
"[Yoga名] formation conditions BPHS"
"[Yoga名] real case study celebrity"

# 行星组合解读
"[行星] in [星座] [宫位] house [上升星座] ascendant Vedic"
"[行星] [星座] transit 2026 effects career"
"[行星]-[行星] conjunction Vedic astrology interpretation"

# Dasha 解读
"[行星1]/[行星2] Dasha period effects Vedic astrology"
"[行星1] [行星2] Vimshottari antardasha results"

# 应期预测
"[事件类型] prediction timing Vedic astrology case study"
"[行星 transit] triggered [事件类型] real example"
```

**查询语言要求**：
- 核心查询用英文（Jyotish 英文资源最丰富）
- 补充查询可用中文（覆盖华语占星圈解读）
- 每个解读点至少 1 个英文查询

### Step V2：执行检索与收集

**最低检索量**（按分析等级）：

| 分析等级 | 最低检索次数 | 最低独立来源数 | 每个主要声明最低来源 |
|---------|------------|-------------|-------------------|
| Level 1 快速 | ≥2 次 web_search | ≥2 个 | 1 个 |
| Level 2 专项 | ≥4 次 web_search | ≥3 个 | 2 个 |
| Level 3 完整 | ≥8 次 web_search | ≥5 个 | 2 个 |

**权威来源优先级**（从高到低）：

| 优先级 | 来源类型 | 示例 |
|--------|---------|------|
| ⭐⭐⭐ | 经典文本/学院 | BPHS 译文、B.V. Raman 著作引用、ICAS/BVRI 教材 |
| ⭐⭐⭐ | 知名占星师 | K.N. Rao、Sanjay Rath、Hart de Fouw、Marc Boney 的文章/视频 |
| ⭐⭐ | 专业占星网站 | AstroVed、Cosmic Insights、Vedic Astrology Journal、AstroSage |
| ⭐⭐ | 专业占星博客 | Jyotish Vidya、MyJyotish、Agni Astrology |
| ⭐ | 综合占星网站 | Astrology.com、CafeAstrology（注意可能混入西方占星） |
| ⚠️ | AI 生成内容 | 仅作参考，不能作为独立来源 |
| ❌ | 无署名/无来源 | 不计为有效来源 |

### Step V3：交叉验证与仲裁

**验证逻辑**：

```
对于每个主要解读声明：
  ├─→ 所有来源一致 → ✅ 验证通过，正常输出
  ├─→ 来源有分歧（不同流派）→ ⚠️ 标注分歧，列出不同观点+来源
  ├─→ 来源有冲突（同一流派不同结论）→ ⚠️ 标注冲突，评估权重
  └─→ 无法找到来源 → ❌ 必须标注"未验证声明"，置信度降级

仲裁原则：
1. 经典文本 > 现代演绎
2. 多案例验证 > 单案例
3. 同一学派内多数观点 > 少数观点
4. 有前提条件的规则 > 无条件的泛化规则
```

---

## 三、输出格式规范

### 3.1 验证状态标记

每个分析章节（静态分析/动态分析/预测输出）末尾必须附加验证状态：

```markdown
### 📋 MEVG 验证状态

| 检索项 | 查询关键词 | 来源数 | 状态 | 关键来源 |
|--------|-----------|--------|------|---------|
| Malavya Yoga 解读 | "Malavya Yoga Leo ascendant Venus Taurus" | 3 | ✅ 验证通过 | MyJyotish, Jyotish Vidya, AstroAnanta |
| Saturn Ashtama Shani | "Ashtama Shani Leo 2026 Pisces" | 2 | ✅ 验证通过 | AtriAstrology, Vinayak Bhatt |
| Ketu Transit Leo | "Ketu transit Leo 2025 2026 effects" | 1 | ⚠️ 部分验证 | 仅 Astromitra 单源，建议补充 |

**总检索次数**：[N] 次
**总独立来源**：[M] 个
**验证通过率**：[X]%
**降级声明**：[列出被降级的解读点]
```

### 3.2 来源引用格式

在正文中引用外部来源时：

```markdown
**Malavya Rajyog**（Panch Mahapurush Yoga）— 金星在 Taurus 10 宫入庙形成
> 📖 来源：MyJyotish（确认 Malavya Yoga 对 Leo 上升的形成条件）+ Jyotish Vidya（确认 10 宫入庙 Venus 的事业效应）

或内联格式：
"...Saturn 在 Pisces 对 Leo 上升构成 Ashtama Shani（8 宫过境，2026 全年）[AtriAstrology 确认]"
```

### 3.3 禁止行为清单

| 禁止行为 | 正确做法 |
|---------|---------|
| ❌ 仅凭 AI 记忆说"Venus 在 Taurus 10 宫是 Malavya Yoga" | ✅ 先搜索确认形成条件，引用来源 |
| ❌ 直接说"Ashtama Shani 很糟糕" | ✅ 搜索 Ashtama Shani 的具体效应+案例+缓解因素 |
| ❌ 说"Jupiter 入 Cancer 对 Leo 是好事" | ✅ 搜索 Jupiter 入 Cancer 对各上升的效应，特别关注 12 宫 |
| ❌ 跳过 MEVG 直接输出解读 | ✅ 每个分析阶段末尾附验证状态表 |
| ❌ 用模糊表述回避验证（"传统认为"） | ✅ 明确写出"根据 [来源]，该规则的条件是..." |

---

## 四、门控位置与执行时机

### 4.1 在工作流中的嵌入点

```
阶段三（静态分析）
  ├─ Step 3.1-3.10（分析执行）
  └─ Step 3.11 ⭐ MEVG-静态门控（验证所有静态解读声明）
       → web_search × N
       → 交叉验证
       → 输出验证状态表
       → ❌ 未通过 → 重做解读（降级置信度或修正结论）

阶段四（动态推运）
  ├─ Step 4.1-4.9（分析执行）
  └─ Step 4.10 ⭐ MEVG-动态门控（验证所有 Transit/Dasha 解读）
       → web_search × N
       → 交叉验证
       → 输出验证状态表
       → ❌ 未通过 → 重做解读

阶段五（应期输出）
  ├─ Step 5.0-5.4（输出执行）
  └─ Step 5.5 ⭐ MEVG-预测门控（验证所有预测声明的来源支撑）
       → 确认每条预测有来源支撑
       → 确认置信度标注与验证结果一致
       → 输出最终验证状态
```

### 4.2 门控通过标准

| 门控 | 通过条件 | 失败处理 |
|------|---------|---------|
| Step 3.11 | ≥80% 主要声明有≥2 个独立来源 | 未验证声明全部降级为 [C]，标注"验证不足" |
| Step 4.10 | ≥80% Transit/Dasha 解读有来源支撑 | 未验证解读全部标注"未经验证" |
| Step 5.5 | 100% 预测有置信度+验证状态+精度声明 | 缺少任何一项即阻止输出，补全后重新检查 |

---

## 五、快速参考：每阶段必检索关键词模板

### 5.1 阶段三（静态分析）必检索

```python
# 伪代码：每个用户命盘，以下检索必须在 Phase 3 完成前执行

mandatory_searches_phase3 = [
    # 1. 上升星座整体格局
    f"{ascendant} ascendant Vedic astrology complete guide",
    
    # 2. 每个 Yoga
    *[f"{yoga_name} Vedic astrology {ascendant} ascendant conditions effects" for yoga_name in identified_yogas],
    
    # 3. 关键行星组合（落陷/入庙/Yogakaraka）
    *[f"{planet} in {sign} {house} house {ascendant} ascendant" for planet, sign, house in key_configurations],
    
    # 4. Shadbala 异常（极强/极弱行星）
    *[f"{planet} weak Shadbala Vedic astrology remedies" for planet in weak_planets],
    *[f"{planet} strongest planet Shadbala effects" for planet in strong_planets],
    
    # 5. SAV 关键宫位
    f"SAV Ashtakavarga {house_number} house low score effects {ascendant}",
]
```

### 5.2 阶段四（动态推运）必检索

```python
mandatory_searches_phase4 = [
    # 1. 当前 Dasha 解读
    f"{maha_dasha}/{antardasha} Vimshottari Dasha period effects",
    
    # 2. 关键 Transit
    *[f"{planet} transit {sign} {year} Vedic astrology effects" for planet, sign, year in key_transits],
    
    # 3. 特殊 Transit 现象
    f"Ashtama Shani {moon_sign} {year}" if is_ashtama_shani else None,
    f"Sade Sati {moon_sign} phase {year}" if is_sade_sati else None,
    f"Jupiter transit {sign} {year} all ascendants" if jupiter_sign_change else None,
]
```

---

## 六、反思：为什么这个门控会被跳过

### 6.1 历史问题诊断

| 日期 | 问题描述 | 根因分析 | 本协议的对应措施 |
|------|---------|---------|----------------|
| 2026-04-27 | 5 月运势分析全凭 AI 记忆，未搜索验证 | 工作流无强制验证步骤 | Step 3.11/4.10 强制门控，不可跳过 |
| 2026-04-27 | Malavya Yoga 判定过于笼统 | 未搜索该 Yoga 的精确形成条件 | V1 查询模板强制搜索 Yoga 条件 |
| 2026-04-27 | Rahu-Moon 合相只提负面 | 训练数据偏重负面解读 | V2 要求搜索正面效应来源 |
| 多次反复 | AI 每次都"忘记"要搜索验证 | 工作流中搜索是"建议"而非"强制门控" | 本协议设为与"不跳步"同级的硬性规则 |

### 6.2 执行纪律

**本协议与 SKILL.md 中的「不跳步」原则具有同等强制力。**

违反本协议的判定：
- 输出的解读章节缺少验证状态表 → **判定为未完成，必须补全**
- 主要解读声明无来源引用 → **判定为无效声明，必须降级**
- 整个分析过程无 web_search 调用 → **判定为严重违反流程，分析无效**

---

**版本**：1.0.0
**创建日期**：2026-04-27
**触发原因**：一楠多次强调"不要根据经验和固有认知去判断分析"，要求全网检索验证后综合分析。v4.1.0 的 Transit Actionable Output 仅覆盖 Transit 预测，缺少对静态分析和其他解读环节的外部验证要求。本协议将外部验证扩展至所有解读环节。
