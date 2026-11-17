# KES_Vector 索引与性能调优

## 1. ivfflat 索引

基于倒排索引的方法，将全体向量划分为几个聚类，查询时在最有可能的类中查找。

### 1.1 创建语法

```sql
CREATE INDEX ON table_name USING ivfflat (vector_name distance_function) WITH (lists = lists_num);
```

- `table_name`: 表名
- `vector_name`: 向量列名
- `distance_function`: 距离函数操作符
- `lists_num`: 聚类数（可选）

### 1.2 支持的距离操作符

| 向量类型 | 距离操作符 | 描述 |
|---------|-----------|------|
| vector | vector_l1_ops | 曼哈顿距离 |
| vector | vector_l2_ops | 欧氏距离 |
| vector | vector_ip_ops | 负内积距离 |
| vector | vector_cosine_ops | 余弦距离 |
| halfvec | halfvec_l1_ops | 曼哈顿距离 |
| halfvec | halfvec_l2_ops | 欧氏距离 |
| halfvec | halfvec_ip_ops | 负内积距离 |
| halfvec | halfvec_cosine_ops | 余弦距离 |
| bit | bit_hamming_ops | 汉明距离 |

**注意**: sparsevec 不支持 ivfflat 索引。

### 1.3 查询使用

```sql
-- 关闭全表扫描
SET enable_seqscan = off;

-- 设置查询选项（可选）
SET ivfflat.probes = 2;  -- 查询聚类数（默认1）

-- 执行查询（运算符必须与索引距离函数对应）
SELECT * FROM t ORDER BY val <-> '[3,3,3]'::halfvec LIMIT 10;
```

`ivfflat.probes` 越大，召回率越高，但耗时越多。设置方式：
```sql
-- 全局设置
SET ivfflat.probes = 2;

-- 局部设置
BEGIN;
SET LOCAL ivfflat.probes = 2;
SELECT ...;
COMMIT;
```

### 1.4 完整示例

```sql
SET enable_seqscan = off;

CREATE TABLE t (val halfvec(3));
INSERT INTO t (val) VALUES ('[0,0,0]'), ('[1,2,3]'), ('[1,1,1]'), (NULL);

-- 创建 ivfflat 索引（欧氏距离）
CREATE INDEX ON t USING ivfflat (val halfvec_l2_ops) WITH (lists = 1);

INSERT INTO t (val) VALUES ('[1,2,4]');

-- 使用索引查询（必须用 <-> 运算符，与 halfvec_l2_ops 对应）
SELECT * FROM t ORDER BY val <-> '[3,3,3]' LIMIT 10;

DROP TABLE t;
```

## 2. hnsw 索引

基于图的层级导航小世界算法，构建多层导航图加速查询。

### 2.1 创建语法

```sql
CREATE INDEX ON table_name USING hnsw (vector_name distance_function)
    WITH (m = mNum, ef_construction = efConstructionNum);
```

参数说明：

| 参数 | 默认值 | 范围 | 描述 |
|------|--------|------|------|
| mNum | 16 | [2, 100] | 每层最大连接数 |
| efConstructionNum | 64 | [4, 1000] | 构建时动态候选列表大小 |

约束: `efConstructionNum >= 2 * mNum`，否则报错。输入 double 会自动向下取整。

### 2.2 支持的距离操作符

| 向量类型 | 距离操作符 | 描述 |
|---------|-----------|------|
| vector | vector_l1_ops | 曼哈顿距离 |
| vector | vector_l2_ops | 欧氏距离 |
| vector | vector_ip_ops | 负内积距离 |
| vector | vector_cosine_ops | 余弦距离 |
| halfvec | halfvec_l1_ops | 曼哈顿距离 |
| halfvec | halfvec_l2_ops | 欧氏距离 |
| halfvec | halfvec_ip_ops | 负内积距离 |
| halfvec | halfvec_cosine_ops | 余弦距离 |
| bit | bit_hamming_ops | 汉明距离 |
| bit | bit_jaccard_ops | 杰卡德距离 |
| sparsevec | sparsevec_l1_ops | 曼哈顿距离 |
| sparsevec | sparsevec_l2_ops | 欧氏距离 |
| sparsevec | sparsevec_ip_ops | 负内积距离 |
| sparsevec | sparsevec_cosine_ops | 余弦距离 |

### 2.3 查询使用

```sql
-- 关闭全表扫描
SET enable_seqscan = off;

-- 设置查询选项（可选）
SET hnsw.ef_search = 100;  -- 搜索候选数（默认40）

-- 或使用局部设置
BEGIN;
SET LOCAL hnsw.ef_search = 100;
SELECT ...;
COMMIT;
```

`hnsw.ef_search` 越大，召回率越高，但耗时越多。

### 2.4 加速索引构建

```sql
-- 增加并行工作者数量
SET max_parallel_maintenance_workers = 7;
-- 增加最大并行数量
SET max_parallel_workers = 8;
```

### 2.5 完整示例

```sql
SET enable_seqscan = off;

-- 示例1：vector 类型 + 欧氏距离
CREATE TABLE t (val vector(3));
INSERT INTO t (val) VALUES ('[0,0,0]'), ('[1,2,3]'), ('[1,1,1]'), (NULL);
CREATE INDEX ON t USING hnsw (val vector_l2_ops);
INSERT INTO t (val) VALUES ('[1,2,4]');
SELECT * FROM t ORDER BY val <-> '[3,3,3]';
SELECT * FROM t ORDER BY val <-> (SELECT NULL::vector);  -- NULL 值处理
DROP TABLE t;

-- 示例2：sparsevec 类型 + 曼哈顿距离
CREATE TABLE t (val sparsevec(3));
INSERT INTO t (val) VALUES ('{}/3'), ('{1:1,2:2,3:3}/3'), ('{1:1,2:1,3:1}/3'), (NULL);
CREATE INDEX ON t USING hnsw (val sparsevec_l1_ops);
INSERT INTO t (val) VALUES ('{1:1,2:2,3:4}/3');
SELECT * FROM t ORDER BY val <+> '{1:3,2:3,3:3}/3';
DROP TABLE t;

-- 示例3：bit 类型 + 汉明距离
CREATE TABLE t (val bit(3));
INSERT INTO t (val) VALUES (B'000'), (B'100'), (B'111'), (NULL);
CREATE INDEX ON t USING hnsw (val bit_hamming_ops);
INSERT INTO t (val) VALUES (B'110');
SELECT * FROM t ORDER BY val <-> B'111';
DROP TABLE t;

-- 示例4：bit 类型 + 杰卡德距离
CREATE TABLE t (val bit(4));
INSERT INTO t (val) VALUES (B'0000'), (B'1100'), (B'1111'), (NULL);
CREATE INDEX ON t USING hnsw (val bit_jaccard_ops);
INSERT INTO t (val) VALUES (B'1110');
SELECT * FROM t ORDER BY val <%> B'1111';
DROP TABLE t;
```

## 3. 索引与运算符对应关系

**关键规则**: 建索引时使用的距离操作符必须与查询时使用的运算符一致，否则无法使用索引扫描。

| 操作符 | 对应的距离操作符后缀 | 描述 |
|--------|---------------------|------|
| <+> | _l1_ops | 曼哈顿距离 |
| <-> | _l2_ops | 欧氏距离 |
| <#> | _ip_ops | 负内积距离 |
| <=> | _cosine_ops | 余弦距离 |
| <-> | _hamming_ops | 汉明距离(bit) |
| <%> | _jaccard_ops | 杰卡德距离(bit) |

## 4. 索引选择指南

### ivfflat vs hnsw

| 对比维度 | ivfflat | hnsw |
|---------|---------|------|
| 算法原理 | 倒排索引 + 聚类 | 层次导航小世界图 |
| 内存占用 | 较少 | 较多 |
| 召回率 | 较低 | 较高 |
| 构建速度 | 快 | 较慢（可并行加速） |
| 查询速度 | 快 | 更快（高召回下） |
| sparsevec 支持 | 不支持 | 支持 |
| 适用场景 | 内存受限、简单场景 | 大数据量、高召回需求 |

### 调优建议

1. **数据量小时**: ivfflat 即可满足
2. **需要高召回**: 使用 hnsw，增大 `ef_search`
3. **稀疏向量**: 只能用 hnsw
4. **构建 hnsw 索引慢**: 增加 `max_parallel_maintenance_workers`
5. **查询召回不足**: 增加 `ivfflat.probes` 或 `hnsw.ef_search`
6. **内存紧张**: 选择 ivfflat 或减小 hnsw 的 `m` 参数
