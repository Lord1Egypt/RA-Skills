# 搜索参数模板

## 可用参数

### 1. 时间范围
- `近一年`: (("2025/01/01"[Date - Publication] : "3000"[Date - Publication]))
- `近三年`: (("2023/01/01"[Date - Publication] : "3000"[Date - Publication]))
- `近五年`: (("2021/01/01"[Date - Publication] : "3000"[Date - Publication]))
- `自定义`: (("开始日期"[Date - Publication] : "结束日期"[Date - Publication]))

### 2. 文章类型
- `Review`: review[pt]
- `Clinical Trial`: clinical trial[pt]
- `Meta-Analysis`: meta-analysis[pt]
- `Randomized Controlled Trial`: randomized controlled trial[pt]
- `Case Reports`: case reports[pt]

### 3. 物种
- `Human`: humans[mesh]
- `Animal`: animals[mesh]
- `Male`: male[mesh]
- `Female`: female[mesh]

### 4. 年龄组
- `Infant`: infant[mesh]
- `Child`: child[mesh]
- `Adult`: adult[mesh]
- `Aged`: aged[mesh]

### 5. 期刊筛选
- `影响因子>10`: journal impact factor > 10
- `核心期刊`: core clinical journal

### 6. 语言
- `English`: english[la]
- `Chinese`: chinese[la]
- `Japanese`: japanese[la]

### 7. 可用全文
- `Free Full Text`: free full text[sb]
- `Full Text`: full text[pt]
- `Abstract`: abstract[pt]

## 组合搜索示例

### 示例1: 近年综述
```
machine learning[Title/Abstract] AND review[pt] AND ("2023/01/01"[Date - Publication] : "3000"[Date - Publication])
```

### 示例2: 临床试验
```
diabetes[Title/Abstract] AND clinical trial[pt] AND humans[mesh]
```

### 示例3: 高影响因子期刊
```
cancer[Title/Abstract] AND ("2024"[Date - Publication] : "3000"[Date - Publication])
```

## 高级搜索语法

| 操作符 | 含义 | 示例 |
|--------|------|------|
| AND | 同时包含 | A AND B |
| OR | 任一包含 | A OR B |
| NOT | 排除 | A NOT B |
| [Title/Abstract] | 标题/摘要 | cancer[Title/Abstract] |
| [MeSH Terms] | MeSH词 | diabetes[MeSH Terms] |
| [Author] | 作者 | smith[Author] |
| [Journal] | 期刊 | nature[Journal] |
| [Date - Publication] | 发表日期 | 2024[Date - Publication] |
