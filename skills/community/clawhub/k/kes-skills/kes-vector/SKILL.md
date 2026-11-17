---
name: kes-vector
name_for_command: kes-vector
description: KingbaseES KES_Vector 向量扩展指南。当用户提到向量数据库、embedding、向量相似度搜索、vector/halfvec/sparsevec/bit 类型、ivfflat/hnsw 索引、向量距离计算、向量插件安装时，必须使用此技能。
---

# KingbaseES KES_Vector 向量扩展指南

本技能提供 KingbaseES KES_Vector 扩展的完整参考，涵盖安装部署、向量数据类型、距离函数、运算符、索引以及性能调优。

> **核心 SQL** → 见 `kes-core` 技能
> **索引设计** → 见 `kes-index-design` 技能

## 快速导航

| 主题 | 参考文件 |
|------|---------|
| 安装与配置 | 本节第 1 部分 |
| 向量数据类型 | `ref/data-types.md` |
| 距离函数与运算符 | `ref/functions-operators.md` |
| 索引与性能调优 | `ref/indexes.md` |

## 1. 安装与配置

### 1.1 扩展文件部署

KES_Vector 扩展包含以下文件：

```
KES_Vector-x86_64/
├── lib/
│   └── vector.so                    # 共享库
└── share/extension/
    ├── vector.control               # 扩展控制文件
    ├── vector--0.7.2.sql            # 主扩展脚本
    └── vector--X.Y.Z--A.B.C.sql     # 升级脚本链
```

部署步骤：将 `lib/vector.so` 拷贝至 KingbaseES 的 `lib/` 目录，将 `share/extension/` 下的文件拷贝至 KingbaseES 的 `share/extension/` 目录。

### 1.2 创建扩展

```sql
-- 创建扩展
CREATE EXTENSION [IF NOT EXISTS] vector;

-- 删除扩展（如果表已使用 vector 类型，需加 CASCADE）
DROP EXTENSION vector [CASCADE];
```

### 1.3 验证安装

```sql
-- 查看扩展状态
SELECT extname, extversion FROM sys_extension WHERE extname = 'vector';

-- 测试基本功能
SELECT '[1,2,3]'::vector;
```

## 2. 向量数据类型速览

### 2.1 四种向量类型

| 类型 | 元素类型 | 存储最大维度 | 索引最大维度 | 输入格式 |
|------|---------|------------|------------|---------|
| `vector` | float32 | 16,000 | 2,000 | `'[x1,x2,...,xn]'` |
| `halfvec` | float16 | 16,000 | 4,000 | `'[x1,x2,...,xn]'` |
| `sparsevec` | float32（稀疏） | 16,000 个非零元素 | 1,000 个非零元素 | `'{idx1:val1,idx2:val2}/dims'` |
| `bit` | bit | 83,886,080 | 64,000 | `B'10010100'` |

### 2.2 快速示例

```sql
-- 创建向量表
CREATE TABLE documents (
    id        SERIAL PRIMARY KEY,
    title     VARCHAR(200),
    embedding vector(768)
);

-- 写入数据
INSERT INTO documents (title, embedding)
VALUES ('示例文档', '[0.1, 0.2, 0.3, ...]'::vector(768));

-- 相似度搜索（欧氏距离）
SET enable_seqscan = off;
SELECT title, embedding <-> '[0.5, 0.6, 0.7, ...]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 10;
```

## 3. 类型转换规则

### 3.1 隐式转换（implicit）
- `vector` → `vector`
- `halfvec` → `halfvec`
- `halfvec` → `vector`（提升精度）
- `vector` → `halfvec`
- `sparsevec` → `sparsevec`
- `vector` → `sparsevec`
- `halfvec` → `sparsevec`
- `sparsevec` → `vector`
- `sparsevec` → `halfvec`

### 3.2 数组转换（assignment）
- `integer[]` → `vector` / `halfvec`
- `float4[]` → `vector` / `halfvec`
- `float8[]` → `vector` / `halfvec`
- `numeric[]` → `vector` / `halfvec`
- `vector` → `float4[]`
- `halfvec` → `float4[]`

### 3.3 运算类型规则
> 当输入 `halfvec + vector` 组合时，`vector` 会隐式转换为 `halfvec`，因为 `vector→halfvec` 是隐式转换，而 `halfvec→vector` 是赋值转换。最终按 `halfvec + halfvec` 运算。

## 4. 距离计算

### 4.1 距离函数

| 函数 | 支持类型 | 描述 |
|------|---------|------|
| `l1_distance(a, b)` | vector, halfvec, sparsevec | 曼哈顿距离 |
| `l2_distance(a, b)` | vector, halfvec, sparsevec | 欧氏距离 |
| `inner_product(a, b)` | vector, halfvec, sparsevec | 内积距离 |
| `cosine_distance(a, b)` | vector, halfvec, sparsevec | 余弦距离 |
| `hamming_distance(a, b)` | bit | 汉明距离 |
| `jaccard_distance(a, b)` | bit | 杰卡德距离 |

### 4.2 距离运算符

| 运算符 | 描述 | 适用类型 |
|--------|------|---------|
| `<+>` | 曼哈顿距离 | vector, halfvec, sparsevec |
| `<->` | 欧氏距离 | vector, halfvec, sparsevec, bit |
| `<#>` | 负内积距离 | vector, halfvec, sparsevec |
| `<=>` | 余弦距离 | vector, halfvec, sparsevec |
| `<->` | 汉明距离 | bit |
| `<%>` | 杰卡德距离 | bit |

### 4.3 使用示例

```sql
-- 欧氏距离
SELECT l2_distance('[1,2,3]'::vector, '[4,5,6]'::vector);
SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector;

-- 余弦距离
SELECT cosine_distance('[1,2]'::halfvec, '[3,4]'::halfvec);

-- 汉明距离（bit 类型）
SELECT hamming_distance('111', '100');
SELECT B'000' <-> B'111';

-- 注意：向量必须同维度，否则报错
SELECT l2_distance('[1,2]'::vector, '[3]'::vector);
-- ERROR: different vector dimensions 2 and 1
```

## 5. 功能函数

| 函数 | 入参 | 返回 | 描述 |
|------|------|------|------|
| `vector_dims(v)` | vector/halfvec | integer | 向量维度 |
| `vector_norm(v)` | vector | double | 欧氏范数 |
| `subvector(v, start, len)` | vector/halfvec | vector/halfvec | 取子向量（下标从1开始） |
| `l2_normalize(v)` | vector/halfvec/sparsevec | 同入参类型 | L2标准化（单位化） |
| `binary_quantize(v)` | vector/halfvec | bit | 二值化量化 |

## 6. 运算符

### 6.1 算术运算符
- `+` 元素相加（vector/halfvec）
- `-` 元素相减（vector/halfvec）
- `*` 元素相乘（vector）

### 6.2 拼接运算符
- `||` 拼接两个同类型向量（vector/halfvec），超过最大维度会截断

### 6.3 聚合函数
- `SUM(v)` - 向量求和（支持 vector/halfvec）
- `AVG(v)` - 向量平均（支持 vector/halfvec）

```sql
-- 聚合示例
SELECT SUM(embedding) FROM documents WHERE category = 'tech';
SELECT AVG(embedding) FROM documents GROUP BY category;
```

## 7. 索引

### 7.1 ivfflat 索引（倒排索引）

```sql
-- 创建 ivfflat 索引
CREATE INDEX ON table_name USING ivfflat (col distance_ops) WITH (lists = 100);

-- 支持的类型与距离
-- vector: vector_l2_ops, vector_ip_ops, vector_cosine_ops
-- halfvec: halfvec_l1_ops, halfvec_l2_ops, halfvec_ip_ops, halfvec_cosine_ops
-- bit: bit_hamming_ops
-- 注意：sparsevec 不支持 ivfflat 索引
```

查询调优：
```sql
SET ivfflat.probes = 5;  -- 查询聚类数（默认1，越大召回率越高但越慢）
```

### 7.2 hnsw 索引（分层导航小世界）

```sql
-- 创建 hnsw 索引
CREATE INDEX ON table_name USING hnsw (col distance_ops)
    WITH (m = 16, ef_construction = 64);

-- 支持的距离操作符（完整矩阵）
-- vector:    vector_l1_ops, vector_l2_ops, vector_ip_ops, vector_cosine_ops
-- halfvec:   halfvec_l1_ops, halfvec_l2_ops, halfvec_ip_ops, halfvec_cosine_ops
-- sparsevec: sparsevec_l1_ops, sparsevec_l2_ops, sparsevec_ip_ops, sparsevec_cosine_ops
-- bit:       bit_hamming_ops, bit_jaccard_ops
```

参数说明：
- `m`: 每层最大连接数（默认16，范围[2,100]）
- `ef_construction`: 构建时动态候选列表大小（默认64，范围[4,1000]）
- 约束: `ef_construction >= 2 * m`

查询调优：
```sql
SET hnsw.ef_search = 100;  -- 搜索候选数（默认40，越大召回率越高）
```

### 7.3 索引选择建议

| 场景 | 推荐索引 | 原因 |
|------|---------|------|
| 数据量大、需要高召回 | hnsw | 召回率更高 |
| 内存受限、简单场景 | ivfflat | 占用内存少 |
| 稀疏向量 | hnsw | sparsevec 仅支持 hnsw |
| bit 向量 | hnsw 或 ivfflat | 两者都支持 |

## 8. 注意事项

1. **维度必须一致**：距离计算和算术运算要求向量维度相同
2. **索引与运算符对应**：建索引时使用的距离操作符必须与查询时使用的运算符一致
3. **关闭顺序扫描**：使用索引查询时需设置 `SET enable_seqscan = off`
4. **NULL 值处理**：NULL 向量可以存储，但参与距离查询时需特别注意
5. **halfvec + vector 运算**：最终按 halfvec 计算（精度可能损失）
