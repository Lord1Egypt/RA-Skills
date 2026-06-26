---
name: legal-research
description: 法律检索专家。法条检索、类案检索、学术观点整理、知识库查询。
metadata:
  { "openclaw": { "requires": { "bins": [] }, "install": [] } }
---

# 法律检索专家 `/legal-research`

## 功能

1. **法条检索** - 检索相关法律法规、司法解释
2. **类案检索** - 检索相似案例、裁判观点
3. **学术观点** - 整理学界/实务界观点
4. **知识库查询** - 查询陈律的知识库

## 用法

```
/legal-research [法律问题描述]
/legal-research --article [法条名称]
/legal-research --case-type [案由]
```

## 输出结构

```markdown
## 检索问题
[问题描述]

## 相关法条
1. 《XXX 法》第 X 条
2. 《XXX 司法解释》第 X 条

## 类案参考
- (202X) XX 刑初 XX 号：[裁判要点]
- (202X) XX 民终 XX 号：[裁判要点]

## 实务观点
[学界/实务界观点整理]

## 知识库链接
- 陈律的知识库/法律知识/[相关文件]
```

## 文件位置

- 知识库：`~/Documents/陈律的知识库/法律知识/`
- 输出：`~/Documents/01_案件管理/进行中/[案件名]/法律检索报告.md`

## 示例

```
/legal-research 危险驾驶罪中血液酒精含量的认定标准
/legal-research --article 刑法第 264 条
/legal-research --case-type 交通事故人身损害赔偿
```

---

*优先级：P1 | 使用频率：高*
