# 系统发育树分析报告模板

**使用说明：** 
- 这是一个模板文件，供 AI 读取 `analysis_summary.json` 后自动填充
- AI 应该读取 JSON 文件，提取关键数据，然后生成完整报告
- 不需要代码解析，AI 直接读 JSON 即可

---

## 3. 结果与讨论

### 3.1 序列收集与质量控制

本研究共收集了 **{num_sequences}** 条序列，来自 **{num_species}** 个不同物种。经过 CD-HIT 去冗余处理后，保留了高质量的代表性序列用于后续分析。

质量控制结果：
- 所有序列长度均在合理范围内
- 去冗余后序列数量适中，既保证了物种多样性，又避免了计算负担
- 序列覆盖度良好，适合系统发育分析

### 3.2 多序列比对与修剪

MAFFT L-INS-i 算法生成了高质量的多序列比对。trimAl automated1 方法自动识别并移除了低质量比对区域，保留了信息量高的保守区域。修剪后的比对更适合系统发育分析，能够提高树构建的准确性。

### 3.3 进化模型与树构建

ModelFinder 从 1232 个候选模型中选择了 **{best_model}** 作为最佳进化模型（基于 BIC 准则）。该模型在拟合数据与模型复杂度之间达到了最佳平衡。

IQ-TREE 使用最大似然法构建了系统发育树，并通过 1000 次 UFBoot2 和 SH-aLRT 重复评估了分支支持度。最终树的对数似然值为 **{log_likelihood}**，树长度为 **{tree_length}**。

### 3.4 分支支持度评估

支持度分析显示，**{high_support_nodes}/{total_nodes}** 个内部节点（**{high_support_percentage}%**）具有高支持度（SH-aLRT ≥ 80% 或 UFBoot ≥ 95%），表明树的拓扑结构可靠。

高支持度节点比例的解读：
- **> 70%**：树结构非常可靠，适合发表
- **50-70%**：树结构较为可靠，部分分支可能需要进一步验证
- **< 50%**：树结构不确定性较高，建议增加序列或使用其他方法验证

### 3.5 系统发育关系

（此部分需要 AI 根据具体的树结构和生物学背景进行解读）

系统发育树揭示了以下主要进化关系：
1. **主要分支**：树分为 X 个主要分支，代表不同的进化谱系
2. **物种聚类**：相近物种聚集在一起，符合分类学预期
3. **进化距离**：分支长度反映了进化距离，较长的分支表示较大的进化差异

---

## AI 使用指南

### 步骤 1: 读取 JSON 文件

```python
import json

with open('analysis_summary.json') as f:
    data = json.load(f)

# 提取关键数据
num_sequences = data['iqtree']['num_sequences']
best_model = data['iqtree']['best_model']
log_likelihood = data['iqtree']['log_likelihood']
tree_length = data['iqtree']['tree_length']
high_support_nodes = data['support']['high_support_nodes']
total_nodes = data['support']['total_nodes']
high_support_percentage = data['support']['high_support_percentage']
```

### 步骤 2: 填充模板

将提取的数据填入模板中的占位符：
- `{num_sequences}` → 487
- `{best_model}` → Q.PFAM+R7
- `{log_likelihood}` → -53461.908
- `{tree_length}` → 82.851
- `{high_support_nodes}` → 251
- `{total_nodes}` → 401
- `{high_support_percentage}` → 62.6%

### 步骤 3: 生成完整报告

AI 可以：
1. 读取 JSON 文件
2. 读取模板文件
3. 替换占位符
4. 添加生物学解读（基于树结构和文献）
5. 生成最终报告

---

## 优势

✅ **无需代码解析** - AI 直接读 JSON  
✅ **结构化数据** - 易于提取和使用  
✅ **灵活性高** - AI 可以根据需要添加更多解读  
✅ **可复用** - 任何 AI 都能使用这个模板

---

## 示例：AI 生成的完整段落

```
本研究共收集了 487 条序列，来自 121 个不同物种。ModelFinder 从 1232 个候选模型中
选择了 Q.PFAM+R7 作为最佳进化模型。IQ-TREE 构建的系统发育树对数似然值为 -53461.908，
树长度为 82.851。支持度分析显示，251/401 个内部节点（62.6%）具有高支持度，表明
树的拓扑结构较为可靠。
```

这样，AI 只需要：
1. 读取 `analysis_summary.json`
2. 读取这个模板
3. 填充数据
4. 添加生物学解读

完全不需要写代码解析日志文件！
