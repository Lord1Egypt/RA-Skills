# KES_Vector 向量数据类型详解

## 1. vector（全精度向量）

每个元素为 float32 的稠密向量。

### 输入格式
- 字符串: `'[x1, x2, x3, ...]'` — 单引号包裹，方括号内逗号分隔
- 带维度: `'[1,2,3]'::vector(3)` — 显式指定维度
- NULL

### 约束
- 最大存储维度：16,000
- 最大索引维度：2,000
- 元素间、括号与逗号间可添加空格

### 示例
```sql
SELECT '[1,2,3]'::vector;
SELECT '[1,2,3]'::vector(3);          -- 正确：维度匹配
SELECT '[1,2,3]'::vector(2);          -- 错误：expected 2 dimensions, not 3
```

## 2. halfvec（半精度向量）

每个元素为 float16 的稠密向量，存储空间为 vector 的一半。

### 输入格式
- 字符串: `'[x1, x2, ...]'::halfvec`
- 带维度: `'[1,2,3]'::halfvec(3)`

### 约束
- 最大存储维度：16,000
- 最大索引维度：4,000

### 示例
```sql
SELECT '[1,2,3]'::halfvec(3);
SELECT '[1,2,3]'::halfvec(16001);    -- 错误：cannot exceed 16000
SELECT '[1,2,3]'::halfvec(0);         -- 错误：must be at least 1
```

## 3. sparsevec（稀疏向量）

只存储非零元素的索引和值，适合大多数位为 0 的场景。

### 输入格式
- `'{index1:value1, index2:value2}/dimensions'`
- 索引从 1 开始，为正整数
- value 为 float32 类型
- dimensions 为总维度，不超过 1,000,000,000

### 约束
- 最大非零元素数：16,000（存储），1,000（索引）
- 不支持 ivfflat 索引

### 示例
```sql
SELECT '{2:1}/2'::sparsevec;          -- 维度2，索引2的值为1
SELECT '{1:1,2:2,3:3}/3'::sparsevec;  -- 维度3
SELECT '{}/3'::sparsevec(3);          -- 空稀疏向量，维度3
SELECT '{0:1}/1'::sparsevec;          -- 错误：index out of bounds（索引从1开始）
```

## 4. bit（二进制位向量）

由 0 和 1 组成的向量，每位占 1bit 内存。

### 输入格式
- `B'00011'` — 以 B 开头
- `'0001'` — 纯字符串形式

### 约束
- 最大存储维度：83,886,080
- 最大索引维度：64,000
- 主要用于汉明距离和杰卡德距离计算

### 示例
```sql
SELECT B'111';
SELECT hamming_distance('111', '110');    -- 返回 1
SELECT jaccard_distance('111', '110');    -- 返回 0.333...
```

## 5. 类型转换矩阵

### 隐式转换 (implicit)
```
vector ↔ vector
halfvec ↔ halfvec
halfvec → vector
vector → halfvec
sparsevec → vector
sparsevec → halfvec
vector → sparsevec
halfvec → sparsevec
```

### 赋值转换 (assignment)
```
integer[] → vector / halfvec
float4[] → vector / halfvec
float8[] → vector / halfvec
numeric[] → vector / halfvec
vector → float4[]
halfvec → float4[]
```

### 重要规则
当混合运算 `halfvec + vector` 时，因为 `vector→halfvec` 是隐式转换，而 `halfvec→vector` 是赋值转换，优先级上隐式转换更强，所以 `vector` 会被转换为 `halfvec` 后再运算。这意味着精度会下降到 halfvec。

## 6. 类型总结表

| 向量类型 | 存储最大维度 | 索引最大维度 | 形式 | 有效位类型 |
|---------|------------|------------|------|-----------|
| vector | 16,000 | 2,000 | [x1,x2,...,xn] | float32 |
| halfvec | 16,000 | 4,000 | [x1,x2,...,xn] | float16 |
| sparsevec | 16,000 非零元素 | 1,000 非零元素 | {idx1:val1,idx2:val2}/dims | float32 |
| bit | 83,886,080 | 64,000 | B'100010100' | bit |
