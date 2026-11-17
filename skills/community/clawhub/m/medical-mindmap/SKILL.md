---
name: 医学知识图谱mindmap
description: 神经病学/脑电图医学知识图谱mindmap系统。适合管理疾病、症状、检查、药物等医学知识，支持脑电图波形分析，输出模板包含核心要点、对比、临床意义、鉴别诊断价值、异常提示、本质总结。
---

# 医学知识图谱mindmap 神经病学/脑电图知识库

适合神经病学、脑电图学习的知识管理系统，特别优化了脑电图输出格式。

## 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **实体** | 一个医学概念 | 癫痫、α波、脑电图、抽搐 |
| **关系** | 实体之间的连接 | 癫痫→需要→脑电图 |
| **事实** | 关于实体的具体信息 | "α波频率8-13Hz" |
| **分类** | 实体的归类 | 疾病、检查、症状、药物、解剖、波形 |

## 存储位置

```
memory/医学知识图谱mindmap/
├── graph.jsonl       # 实体和关系（结构化）
├── knowledge/        # 事实知识
│   ├── disease/      # 疾病知识
│   ├── examination/  # 检查知识
│   ├── symptom/      # 症状知识
│   ├── medication/   # 药物知识
│   ├── anatomy/      # 解剖知识
│   └── waveform/     # 波形知识（新增）
└── summary/          # 自动生成的摘要
```

## 适用场景

| 你说 | 动作 |
|------|------|
| "记住α波是8-13Hz" | 创建波形实体 |
| "癫痫和脑电图什么关系" | 查询关系 |
| "α波有什么特点" | 查询事实 |
| "添加一条：尖波提示癫痫" | 添加事实 |
| "总结一下脑电图的异常波形" | 生成摘要 |

## 实体类型

### 1. 疾病 (Disease)
```yaml
name: 疾病名称
category: 分类
symptoms: [相关症状]
treatments: [治疗方法]
eeg_features: [脑电图特征]
```

### 2. 检查 (Examination)
```yaml
name: 检查名称
purpose: 检查目的
procedure: 检查方法
indications: 适应症
findings: 常见发现
```

### 3. 症状 (Symptom)
```yaml
name: 症状名称
description: 描述
eeg_correlate: 脑电图关联
```

### 4. 药物 (Medication)
```yaml
name: 药物名称
dosage: 用量
indications: 适应症
eeg_effects: 对脑电图的影响
```

### 5. 解剖 (Anatomy)
```yaml
name: 结构名称
location: 位置
function: 功能
eeg_region: 脑电图关联区域
```

### 6. 波形 (Waveform) - 重点新增
```yaml
name: 波形名称
frequency: 频率范围
amplitude: 振幅
morphology: 形态特征
distribution: 分布部位
physiological: 生理性/病理性
clinical_significance: 临床意义
```

## 常用关系

```yaml
# 疾病相关
has_symptom: 疾病 -> 症状
needs_exam: 疾病 -> 检查
treated_by: 疾病 -> 治疗
shows_eeg: 疾病 -> 波形
has_eeg_feature: 疾病 -> 脑电图特征

# 检查相关
detects: 检查 -> 疾病/异常
shows: 检查 -> 波形
performed_by: 检查 -> 解剖部位

# 波形相关
belongs_to: 波形 -> 频段
seen_in: 波形 -> 疾病
differential_for: 波形 -> 鉴别疾病
```

## 脑电图输出模板（核心格式）

当查询脑电图相关知识时，使用以下结构化输出：

```
## [波形/疾病名称]

### 核心要点
- 频率：X-Y Hz
- 形态：描述
- 分布：部位
- 生理性：是/否

### 对比
| 波形 | 频率 | 形态 | 临床意义 |
|------|------|------|----------|
| α波 | 8-13Hz | ... | ... |
| β波 | 13-30Hz | ... | ... |

### 临床意义
- 主要提示：XXX
- 常见于：XXX

### 鉴别诊断价值
- 需要与XX鉴别
- 区别点：XXX

### 异常提示
- 异常表现：XXX
- 提示疾病：XXX

### 本质总结
一句话概括本质特征
```

## 快速使用

### 1. 创建实体

```bash
# 创建波形实体
python3 scripts/mindmap.py create Waveform --name "α波" --frequency "8-13Hz" --physiological "是"

# 创建疾病实体
python3 scripts/mindmap.py create Disease --name "癫痫" --category "神经系统疾病"

# 创建检查实体
python3 scripts/mindmap.py create Examination --name "脑电图" --purpose "检测大脑电活动"
```

### 2. 创建关系

```bash
# 癫痫需要脑电图检查
python3 scripts/mindmap.py relate --from "癫痫" --rel "needs_exam" --to "脑电图"

# 癫痫显示尖波
python3 scripts/mindmap.py relate --from "癫痫" --rel "shows_eeg" --to "尖波"
```

### 3. 添加事实（支持脑电图模板）

```bash
# 添加波形知识
python3 scripts/mindmap.py fact add --entity "α波" --fact "频率8-13Hz，正常成人安静闭眼时出现在后头部" --category "核心要点"

python3 scripts/mindmap.py fact add --entity "尖波" --fact "频率2-5Hz，振幅100-200μV，突发突止" --category "形态特征"

# 添加临床意义
python3 scripts/mindmap.py fact add --entity "尖波" --fact "高度提示癫痫" --category "临床意义"

# 添加鉴别诊断
python3 scripts/mindmap.py fact add --entity "尖波" --fact "需与慢波、δ波鉴别" --category "鉴别诊断"
```

### 4. 查询

```bash
# 查询实体（自动按脑电图模板输出）
python3 scripts/mindmap.py get 尖波

# 查询相关关系
python3 scripts/mindmap.py related 尖波

# 查询所有事实
python3 scripts/mindmap.py facts 尖波
```

### 5. 生成摘要（脑电图格式）

```bash
# 生成脑电图格式摘要
python3 scripts/mindmap.py summarize 尖波
```

## 简化命令（推荐）

**直接用中文告诉小社：**

### 实体操作
- "创建一个波形：β波，频率13-30Hz，生理性"
- "创建一个疾病：失神发作"
- "列出所有波形"

### 关系操作
- "癫痫和脑电图什么关系？"
- "把失神发作和3Hz棘慢波关联起来"

### 事实操作（脑电图模板）
- "在尖波下添加：临床意义是高度提示癫痫"
- "在α波下添加：对比β波13-30Hz，临床意义是清醒时出现"
- "添加异常提示：尖波异常提示癫痫发作"

### 摘要（自动用模板）
- "总结一下尖波的知识" → 自动输出脑电图模板格式

## 脑电图模板示例：尖波

### 核心要点
- **频率**：2-5 Hz
- **振幅**：100-200 μV
- **形态**：突发突止，尖锐
- **分布**：局部或广泛
- **生理性**：否（病理性）

### 对比
| 波形 | 频率 | 振幅 | 时程 |
|------|------|------|------|
| 尖波 | 2-5Hz | 高 | <200ms |
| 棘波 | >5Hz | 高 | <50ms |
| 慢波 | 0.5-4Hz | 不等 | 长 |

### 临床意义
- 高度提示癫痫
- 常见于部分性发作
- 是癫痫的特异性放电

### 鉴别诊断价值
- 需与伪差鉴别（肌电、眼动）
- 需与发作性睡病鉴别
- 需与心源性晕厥鉴别

### 异常提示
- 尖波出现 = 异常
- 提示癫痫灶定位
- 反映神经元过度同步化

### 本质总结
尖波是癫痫的特异性放电标志，反映大脑神经元异常同步化放电，是诊断癫痫的重要依据。

---

## 重要规则

1. **只追加不删除**：更新时标记旧事实为superseded
2. **ID自动生成**：创建实体时自动生成唯一ID
3. **脑电图模板优先**：查询波形/脑电图相关时，必须使用上述六要素模板
4. **事实可追溯**：所有事实记录来源和时间

---

## 神经病学知识库联动

本技能可与神经病学知识库联动：
- 神经病学Skill位置：`~/.openclaw/workspace/skills/neurology/`
- 脑电图OCR数据：`~/.openclaw/workspace/neuro_redistill/eeg_ocr/`

---

**记住：直接用中文告诉小社！**

示例：
- "创建波形：δ波，频率0.5-4Hz"
- "尖波和棘波有什么区别？"（自动对比）
- "总结3Hz棘慢波的知识"（输出完整模板）
- "这个波形是癫痫吗？"（鉴别诊断价值）
