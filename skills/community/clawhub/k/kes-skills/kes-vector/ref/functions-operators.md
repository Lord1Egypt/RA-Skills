# KES_Vector 函数与运算符详解

## 1. 距离函数

### 1.1 曼哈顿距离 l1_distance

```sql
l1_distance(parameter1, parameter2) → double
```

公式: `d = |x1-y1| + |x2-y2| + |x3-y3| + ...`

支持类型: vector, halfvec, sparsevec（同类型间计算）

```sql
SELECT l1_distance('[0,0]'::vector, '[3,4]'::vector);    -- 返回 7
SELECT l1_distance('[0,0] '::halfvec, '[3,4]'::halfvec); -- 返回 7
SELECT l1_distance('{}/2'::sparsevec, '{2:1}/2'::sparsevec); -- 返回 1
-- 维度不匹配时报错：
SELECT l1_distance('[1,2]'::vector, '[3]'::vector);       -- ERROR: different vector dimensions
```

### 1.2 欧氏距离 l2_distance

```sql
l2_distance(parameter1, parameter2) → double
```

公式: `d = sqrt(sum((xi-yi)^2))`

支持类型: vector, halfvec, sparsevec

```sql
SELECT l2_distance('[0,0]'::halfvec, '[3,4]'::halfvec);  -- 返回 5
SELECT l2_distance('{}/2'::sparsevec, '{1:3,2:4}/2'::sparsevec); -- 返回 5
```

### 1.3 内积距离 inner_product

```sql
inner_product(parameter1, parameter2) → double
```

公式: `Inner Product = sum(xi * yi)`

支持类型: vector, halfvec, sparsevec

```sql
SELECT inner_product('[1,2]'::halfvec, '[3,4]'::halfvec);  -- 返回 11
SELECT inner_product('{1:1,2:2}/2'::sparsevec, '{1:2,2:4}/2'::sparsevec); -- 返回 10
```

### 1.4 余弦距离 cosine_distance

```sql
cosine_distance(parameter1, parameter2) → double
```

公式: `Cosine Distance = 1 - (x·y) / (|x| * |y|)`

支持类型: vector, halfvec, sparsevec

```sql
SELECT cosine_distance('[1,1]'::halfvec, '[1,1]'::halfvec);  -- 返回 0（完全相同）
SELECT cosine_distance('[1,0]'::halfvec, '[0,2]'::halfvec);  -- 返回 1（正交）
```

### 1.5 汉明距离 hamming_distance

```sql
hamming_distance(parameter1, parameter2) → double
```

仅支持 bit 类型，计算两个位向量不同位的个数。

```sql
SELECT hamming_distance('111', '100');  -- 返回 2
SELECT hamming_distance(B'111', B'100'); -- 返回 2
-- 长度不匹配时报错：
SELECT hamming_distance('111', '00');    -- ERROR: different bit lengths 3 and 2
```

### 1.6 杰卡德距离 jaccard_distance

```sql
jaccard_distance(parameter1, parameter2) → double
```

仅支持 bit 类型，计算 `1 - |A∩B| / |A∪B|`。

```sql
SELECT jaccard_distance('1111', '1100');  -- 返回 0.5
SELECT jaccard_distance('1111', '0000');  -- 返回 1
```

### 1.7 距离函数总结

| 函数 | 入参类型 | 返回 | 描述 |
|------|---------|------|------|
| l1_distance | (vector,vector), (halfvec,halfvec), (sparsevec,sparsevec) | double | 曼哈顿距离 |
| l2_distance | (vector,vector), (halfvec,halfvec), (sparsevec,sparsevec) | double | 欧氏距离 |
| inner_product | (vector,vector), (halfvec,halfvec), (sparsevec,sparsevec) | double | 内积距离 |
| cosine_distance | (vector,vector), (halfvec,halfvec), (sparsevec,sparsevec) | double | 余弦距离 |
| hamming_distance | (bit,bit) | double | 汉明距离 |
| jaccard_distance | (bit,bit) | double | 杰卡德距离 |

**注意**:
1. 运算时只能对相同维度的向量计算，否则报错
2. 实际上只对同类型向量计算，不同类型会通过类型转换规则先转换

## 2. 功能函数

### 2.1 vector_dims — 求向量维度

```sql
vector_dims(parameter) → integer
```

```sql
SELECT vector_dims('[1,2,3]'::halfvec);                    -- 返回 3
SELECT vector_dims('[1,2,3,5,4,1,0,0,8]'::halfvec);       -- 返回 9
```

### 2.2 vector_norm — 欧氏范数

```sql
vector_norm(parameter) → double
```

### 2.3 subvector — 取子向量

```sql
subvector(parameter1, parameter2, parameter3) → parameter1
```

- parameter1: vector 或 halfvec
- parameter2: 起始索引（从1开始）
- parameter3: 长度（>=1）

```sql
SELECT subvector('[1,2,3,4,5]'::vector, 3, 2);    -- 返回 [3,4]
SELECT subvector('[1,2,3,4,5]'::vector, -1, 3);   -- 返回 [1]（从负索引取）
SELECT subvector('[1,2,3,4,5]'::vector, 3, 9);    -- 返回 [3,4,5]（超过长度截断）
-- 错误情况：
SELECT subvector('[1,2,3,4,5]'::vector, 1, 0);    -- ERROR: must have at least 1 dimension
SELECT subvector('[1,2,3,4,5]'::vector, 3, -1);   -- ERROR: must have at least 1 dimension
```

### 2.4 l2_normalize — L2 标准化

```sql
l2_normalize(parameter) → parameter
```

使向量模（长度）为 1。支持 vector, halfvec, sparsevec。

```sql
SELECT l2_normalize('[3,4]'::vector);         -- 返回 [0.6, 0.8]
SELECT l2_normalize('[3,0]'::vector);         -- 返回 [1, 0]
SELECT l2_normalize('[0,0]'::vector);         -- 返回 [0, 0]
SELECT l2_normalize('{2:0.1}/2'::sparsevec);  -- 返回 '{2:1}/2'
SELECT l2_normalize('{} '/2'::sparsevec);     -- 返回 '{} '/1'（空向量标准化）
```

### 2.5 binary_quantize — 二值化量化

```sql
binary_quantize(parameter) → bit
```

规则：每位 > 0 赋值为 1，<= 0 赋值为 0。支持 vector 和 halfvec。

```sql
SELECT binary_quantize('[1,0,-1]'::vector);           -- 返回 100
SELECT binary_quantize('[0,0.1,-0.2,...]'::vector);   -- 返回 0100110101
```

可以将全精度向量存储减少到 1/32，半精度减少到 1/16，并使用汉明距离加速计算。

### 2.6 功能函数总结

| 函数 | 入参 | 返回 | 描述 |
|------|------|------|------|
| vector_dims | vector/halfvec | integer | 向量维度 |
| vector_norm | vector | double | 欧氏范数 |
| subvector | vector/halfvec, int, int | vector/halfvec | 求子向量 |
| l2_normalize | vector/halfvec/sparsevec | 同入参 | L2标准化 |
| binary_quantize | vector/halfvec | bit | 二值化量化 |

## 3. 运算符

### 3.1 元素加减乘

| 符号 | 左类型 | 右类型 | 返回 | 描述 |
|------|--------|--------|------|------|
| + | vector | vector | vector | 元素相加 |
| + | halfvec | halfvec | halfvec | 元素相加 |
| - | vector | vector | vector | 元素相减 |
| - | halfvec | halfvec | halfvec | 元素相减 |
| * | vector | vector | vector | 元素相乘 |

```sql
SELECT '[1,2,3]'::vector + '[4,5,6]'::vector;   -- 返回 [5,7,9]
SELECT '[1,2,3]'::vector - '[4,5,6]'::vector;   -- 返回 [-3,-3,-3]
SELECT '[1,2,3]'::vector * '[4,5,6]'::vector;   -- 返回 [4,10,18]
-- 维度不同报错：
SELECT '[1,2]'::vector + '[3]'::vector;          -- ERROR: different vector dimensions
-- 溢出报错：
SELECT '[3e38]'::vector + '[3e38]'::vector;      -- ERROR: value out of range: overflow
```

### 3.2 拼接运算符 ||

```sql
SELECT '[1,2,3]'::vector || '[1,2,3]'::vector;    -- 返回 [1,2,3,1,2,3]
SELECT '[1,2,3]'::halfvec || '[1,2,3]'::halfvec;  -- 返回 [1,2,3,1,2,3]
```

注意：拼接后超过最大维度会截断。与 text 类型拼接时会先转换为 text。

### 3.3 距离运算符

| 符号 | 描述 | 左类型 | 右类型 | 返回 |
|------|------|--------|--------|------|
| <+> | 曼哈顿距离 | vector/halfvec/sparsevec | 同左 | double |
| <-> | 欧氏距离 | vector/halfvec/sparsevec | 同左 | double |
| <-> | 汉明距离 | bit | bit | double |
| <#> | 负内积距离 | vector/halfvec/sparsevec | 同左 | double |
| <=> | 余弦距离 | vector/halfvec/sparsevec | 同左 | double |
| <%> | 杰卡德距离 | bit | bit | double |

```sql
-- 欧氏距离
SELECT '[0,0]'::vector <-> '[3,4]'::vector;    -- 返回 5
-- 负内积距离（结果与 inner_product 互为相反数）
SELECT '[1,2]'::vector <#> '[3,4]'::vector;    -- 返回 -11
-- 汉明距离
SELECT B'000' <-> B'111';                       -- 返回 3
-- 杰卡德距离
SELECT '1111' <%> '0100';                       -- 返回 0.75
```

### 3.4 运算符总结

| 类型 | 符号 | 描述 | 左类型 | 右类型 | 返回 |
|------|------|------|--------|--------|------|
| 加减乘 | + | 元素相加 | vector/halfvec | 同左 | 同左 |
| 加减乘 | - | 元素相减 | vector/halfvec | 同左 | 同左 |
| 加减乘 | * | 元素相乘 | vector | vector | vector |
| 拼接 | \|\| | 拼接 | vector/halfvec | 同左 | 同左 |
| 距离 | <-> | 欧氏距离 | vector/halfvec/sparsevec/bit | 同左 | double |
| 距离 | <+> | 曼哈顿距离 | vector/halfvec/sparsevec | 同左 | double |
| 距离 | <#> | 负内积距离 | vector/halfvec/sparsevec | 同左 | double |
| 距离 | <=> | 余弦距离 | vector/halfvec/sparsevec | 同左 | double |
| 距离 | <-> | 汉明距离 | bit | bit | double |
| 距离 | <%> | 杰卡德距离 | bit | bit | double |

**注意**: 元素加减乘与距离计算要求维度相等。拼接操作可能截断。

## 4. 聚合函数

### 4.1 SUM — 向量求和

```sql
SUM(vector_name) → vector/halfvec
```

对每个对应维度的向量元素进行算数求和。

```sql
SELECT sum(embedding) FROM test;
-- 如果表中有 [1,2,3], [1,2,3], [1,2,3]，返回 [3,6,9]
```

### 4.2 AVG — 向量平均

```sql
AVG(vector_name) → vector/halfvec
```

```sql
SELECT avg(embedding) FROM test;
-- 如果表中有 [1,2,3], [1,2,3], [1,2,3]，返回 [1,2,3]
```

### 4.3 聚合函数总结

| 功能 | 入参 | 返回 | 描述 |
|------|------|------|------|
| AVG | vector | vector | 相同维度向量每维平均值 |
| AVG | halfvec | halfvec | 相同维度向量每维平均值 |
| SUM | vector | vector | 相同维度每元素相加的和 |
| SUM | halfvec | halfvec | 相同维度每元素相加的和 |
