---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304402203e494f87230d1a50ff89c740a1dcf262f851f797f89d5f8719660f13f962ef46022057029d5d3e6ccb4e2572d3e1e89eb36d9dcd689854aa14c8d73caca8c9088fee
    ReservedCode2: 3045022044c1b49bfaef40d0093443964c1d345ff898cfecc13fe642a183061ecb19110c022100c9b81f2818d1675763d1d57f1b4303c39994acda2357687849bc53debb05d077
description: |-
    检查心理学学术期刊是否被 SCI 或 SSCI 索引。在评估文献质量时使用，帮助筛选符合条件的期刊文章。
    触发场景：
    - 用户要求检查某期刊是否被 SCI/SSCI 索引
    - 在评估非预印本文献质量时自动调用
    - 构建心理学语料库时作为期刊筛选工具
    不适用于预印本平台的文章（直接跳过，使用 PaperClaw 评估）。
name: journal-sci/ssci-checker
---

# Journal SCI/SSCI Checker

## 功能描述

检查给定期刊是否被 SCI（Science Citation Index）或 SSCI（Social Sciences Citation Index）索引。

## 使用场景

在论文质量评估流程中：
1. **判断文章类型** → 预印本？→ 直接 PaperClaw
2. **非预印本** → 检查期刊是否在 SCI/SSCI → 通过后 → PaperClaw

## 数据来源

- **Web of Science** (WoS)
- **Journal Citation Reports** (JCR)
- 更新频率：每年一次

## 期刊列表文件

- 路径：`/workspace/skills/journal-sci-ssci-checker/data/journals.txt`
- 格式：每行一个期刊名（支持模糊匹配）

## 检查流程

### 输入
- 期刊名称（journal_name）

### 处理逻辑
1. 加载期刊列表（journals.txt）
2. 模糊匹配输入的期刊名
3. 返回匹配结果：
   - `SCI` - 被 SCI 索引
   - `SSCI` - 被 SSCI 索引
   - `BOTH` - 同时被 SCI 和 SSCI 索引
   - `NOT_FOUND` - 不在列表中

### 输出
```json
{
  "journal_name": "输入的期刊名",
  "matched_name": "匹配到的期刊名",
  "indexed_in": ["SCI", "SSCI"],
  "result": "PASS" | "FAIL"
}
```

## 示例

**输入：**
```
Journal of Personality and Social Psychology
```

**输出：**
```json
{
  "journal_name": "Journal of Personality and Social Psychology",
  "matched_name": "Journal of Personality and Social Psychology",
  "indexed_in": ["SCI", "SSCI"],
  "result": "PASS"
}
```

## 更新期刊列表

运行更新脚本：
```bash
python3 /workspace/skills/journal-sci-ssci-checker/scripts/update_journals.py
```

该脚本会：
1. 从 Web of Science 获取最新期刊列表
2. 更新 JCR 数据
3. 合并去重
4. 保存到 journals.txt

## 注意事项

- 预印本文章不需要执行此检查
- 建议每年更新一次期刊列表
- 匹配采用模糊匹配（忽略大小写、空格差异）
