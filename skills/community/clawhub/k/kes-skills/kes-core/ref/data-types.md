# KingbaseES 数据类型详解

包括数值、字符、日期时间、布尔、数组、JSON、几何、网络地址、位串、XML、UUID 和 Oracle 兼容类型。

## 1. 数值类型

### 整数类型

| 类型 | 别名 | 存储 | 范围 | 说明 |
|------|------|------|------|------|
| `SMALLINT` | - | 2字节 | -32768 ~ 32767 | 小范围整数 |
| `INTEGER` | `INT`, `INT4` | 4字节 | -2147483648 ~ 2147483647 | 常用整数 |
| `BIGINT` | `INT8`, `BIGSERIAL`基础 | 8字节 | -9223372036854775808 ~ 9223372036854775807 | 大范围整数 |

```sql
-- 使用示例
CREATE TABLE products (
    id              BIGSERIAL PRIMARY KEY,      -- 自动递增bigint
    category_code   SMALLINT,                   -- 分类编码
    stock_quantity  INTEGER DEFAULT 0,          -- 库存数量
    max_capacity    BIGINT                      -- 最大容量
);

-- 溢出检查
SELECT 2147483647::INTEGER + 1;  -- 错误：integer out of range
SELECT 2147483647::BIGINT + 1;   -- 正确：2147483648
```

### 精确小数

| 类型 | 存储 | 说明 |
|------|------|------|
| `DECIMAL(p, s)` | 可变 | 任意精度，p=总位数，s=小数位 |
| `NUMERIC(p, s)` | 可变 | 同DECIMAL，完全等价（SQLServer兼容模式默认精度18） |
| `SERIAL` | 4字节 | 自动递增INTEGER |
| `BIGSERIAL` | 8字节 | 自动递增BIGINT |

```sql
-- 精确小数（金融场景必须使用）
CREATE TABLE accounts (
    account_no    VARCHAR(20) PRIMARY KEY,
    balance       DECIMAL(15, 2) DEFAULT 0.00,    -- 余额：15位总长，2位小数
    daily_limit   DECIMAL(12, 2) DEFAULT 999999,  -- 日限额
    interest_rate NUMERIC(5, 4) DEFAULT 0.035,    -- 利率：0.0350
    fee_rate      DECIMAL(3, 2) DEFAULT 0.01      -- 手续费率
);

-- NUMERIC字面量
INSERT INTO accounts (account_no, balance, interest_rate)
VALUES ('A001', 1234567.89, 0.035);

-- 精度说明
-- DECIMAL(15, 2): 最大 9999999999999.99
-- DECIMAL(5, 4):  最大 9.9999
-- DECIMAL(10):    同 DECIMAL(10, 0)，最大 9999999999
```

### 近似小数

| 类型 | 别名 | 存储 | 精度 | 范围 |
|------|------|------|------|------|
| `REAL` | `FLOAT4` | 4字节 | 6位 | -3.40282E+38 to -1.17549E-38, 0, 1.17549E-38 to 3.40282E+38 |
| `DOUBLE PRECISION` | `FLOAT8` | 8字节 | 15位 | 1E-307 ~ 1E308 |

```sql
-- 近似小数（科学计算/地理坐标）
CREATE TABLE sensor_data (
    id          BIGSERIAL PRIMARY KEY,
    latitude    DOUBLE PRECISION,       -- 纬度
    longitude   DOUBLE PRECISION,       -- 经度
    temperature REAL,                   -- 温度
    humidity    REAL,                   -- 湿度
    reading_at  TIMESTAMP
);

-- 精度警告：不要用REAL/FLOAT存金额
-- 0.1 + 0.2 在FLOAT中 ≠ 0.3
SELECT 0.1::REAL + 0.2::REAL = 0.3::REAL;  -- false
SELECT 0.1::DECIMAL + 0.2::DECIMAL = 0.3::DECIMAL;  -- true
```

### SERIAL 序列类型

```sql
-- SERIAL 自动创建序列+约束
CREATE TABLE employees (
    id      SERIAL PRIMARY KEY,         -- 创建int序列emp_id_seq
    name    VARCHAR(100) NOT NULL
);

-- 等价于：
CREATE SEQUENCE employees_id_seq;
ALTER TABLE employees ALTER id SET DEFAULT nextval('employees_id_seq');
ALTER SEQUENCE employees_id_seq OWNED BY employees.id;

-- 使用
INSERT INTO employees (name) VALUES ('张三');
SELECT currval('employees_id_seq');  -- 当前值
SELECT lastval();                     -- 最后使用的序列值

-- SERIAL 变体
CREATE TABLE t1 (id SERIAL);          -- INT范围
CREATE TABLE t2 (id BIGSERIAL);       -- BIGINT范围

-- 手动控制序列
SELECT setval('employees_id_seq', 1000);  -- 设置当前值
SELECT nextval('employees_id_seq');       -- 1001

-- 查看序列状态
SELECT
    sequencename,
    sequenceowner,
    start_value,
    last_value,
    increment_by,
    max_value,
    min_value,
    cache_value,
    is_cycled
FROM sys_sequences
WHERE schemaname = 'public';
```

---

## 2. 字符类型

### CHAR/VARCHAR

| 类型 | 存储 | 说明 |
|------|------|------|
| `CHAR(n)` / `CHARACTER(n)` | n字节+开销 | 定长，不足补空格 |
| `CHAR` / `CHAR(1)` | 1字节 | 单字符 |
| `VARCHAR(n)` / `CHARACTER VARYING(n)` | 实际长度+1字节 | 变长，n为最大长度 |
| `TEXT` | 实际长度+1字节 | 无长度限制 |

```sql
-- 字符类型选择
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    gender      CHAR(1),                 -- 固定长度：M/F
    status      CHAR(2),                 -- 固定编码：01/02/03
    username    VARCHAR(50) NOT NULL,    -- 有长度限制
    email       VARCHAR(200) UNIQUE,     -- 有长度限制
    nickname    VARCHAR(100),
    bio         TEXT,                    -- 无限制文本
    avatar_url  TEXT                     -- 长URL
);

-- CHAR注意事项
SELECT LENGTH('AB'::CHAR(5));           -- 5（含3个空格）
SELECT 'AB'::CHAR(5) = 'AB';            -- true（尾随空格比较时忽略）
SELECT 'AB'::CHAR(5) = 'AB   ';         -- true

-- VARCHAR vs TEXT
-- 性能：两者相同
-- 选择：有业务长度限制用VARCHAR，无限制用TEXT
```

### Oracle 兼容字符类型

```sql
-- Oracle兼容模式下的字符类型
CREATE TABLE oracle_style (
    col_char2       CHAR(20),            -- Oracle CHAR
    col_nvarchar2   NVARCHAR2(100),      -- Oracle National字符
    col_varchar2    VARCHAR2(200),       -- Oracle VARCHAR2
    col_clob        CLOB                 -- Oracle大文本
);

-- 差异说明
-- VARCHAR2 在Oracle兼容模式下 ≅ VARCHAR
-- NVARCHAR2 使用UCS2/UTF16存储
-- CLOB ≅ TEXT，但支持Oracle风格的DBMS_LOB操作
```

---

## 3. 日期时间类型

### 完整类型对照

| 类型 | 存储 | 输入格式 | 说明 |
|------|------|---------|------|
| `DATE` | 8字节 | `YYYY-MM-DD` | 仅日期 |
| `TIME[(p)]` | 8字节 | `HH:MI:SS` | 时间（无时区） |
| `TIME[(p)] WITH TIME ZONE` | 12字节 | `HH:MI:SS+ZZ` | 时间（有时区） |
| `TIMESTAMP[(p)]` | 8字节 | `YYYY-MM-DD HH:MI:SS` | 时间戳（无时区） |
| `TIMESTAMP[(p)] WITH TIME ZONE` | 8字节 | `YYYY-MM-DD HH:MI:SS+ZZ` | 时间戳（有时区） |
| `INTERVAL` | 12字节 | `Y-M DT` | 时间间隔 |

(p = 小数秒精度，0-6)

```sql
-- 日期时间使用
CREATE TABLE orders (
    id              BIGSERIAL PRIMARY KEY,
    order_date      DATE NOT NULL,                        -- 下单日期
    order_time      TIME,                                 -- 下单时间
    created_at      TIMESTAMP DEFAULT NOW(),              -- 创建时间戳
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(), -- 更新时间（带时区）
    ship_by         DATE DEFAULT CURRENT_DATE + 3,        -- 发货截止
    valid_interval  INTERVAL '30 days',                    -- 有效期限
    precision_ts    TIMESTAMP(3)                           -- 3位毫秒精度
);

-- 日期输入方式
INSERT INTO orders (order_date, order_time, created_at)
VALUES
    ('2026-01-15', '14:30:00', '2026-01-15 14:30:00'),
    (DATE '2026-01-16', TIME '09:00:00', TIMESTAMP '2026-01-16 09:00:00'),
    (CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP);

-- 日期函数
SELECT
    NOW(),                                    -- 当前事务开始时间
    CURRENT_TIMESTAMP,                        -- 同NOW()
    CURRENT_DATE,                             -- 当前日期
    CURRENT_TIME,                             -- 当前时间
    LOCALTIMESTAMP,                           -- 本地时间戳（无时区）
    LOCALTIMESTAMP(3),                        -- 3位精度
    STATEMENT_TIMESTAMP(),                    -- 当前语句开始时间
    TRANSACTION_TIMESTAMP(),                  -- 事务提交时间
    CLOCK_TIMESTAMP();                        -- 真实当前时间

-- 日期运算
SELECT
    CURRENT_DATE + 7,                         -- 7天后
    CURRENT_DATE - INTERVAL '30 days',        -- 30天前
    order_date + INTERVAL '1 month',          -- 加1个月
    AGE(NOW(), created_at),                   -- 时间差（年-月格式）
    EXTRACT(YEAR FROM created_at),            -- 提取年份
    EXTRACT(MONTH FROM created_at),           -- 提取月份
    EXTRACT(DOW FROM created_at),             -- 星期几（0=周日）
    EXTRACT(WEEK FROM created_at),            -- 年第几周
    DATE_TRUNC('month', created_at),          -- 截断到月初
    DATE_PART('hour', created_at);            -- 提取小时

-- 日期间隔计算
SELECT
    '2026-03-01'::DATE - '2026-01-15'::DATE,           -- 45（天数）
    AGE('2026-03-01'::DATE, '2026-01-15'::DATE),       -- 1 mon 15 days
    '2 hours 30 minutes'::INTERVAL,                     -- 间隔字面量
    INTERVAL '3 days' + INTERVAL '5 hours';             -- 间隔相加
```

### 时区处理

```sql
-- 查看/设置时区
SHOW timezone;
SET timezone = 'Asia/Shanghai';

-- WITH TIME ZONE 自动转换
CREATE TABLE global_events (
    id      BIGSERIAL,
    event_at TIMESTAMP WITH TIME ZONE
);

INSERT INTO global_events (event_at)
VALUES ('2026-01-15 10:00:00+08'),   -- 北京时间
       ('2026-01-15 01:00:00-00');   -- UTC时间

-- 查询时自动转换为session时区
SELECT
    event_at,
    event_at AT TIME ZONE 'UTC',              -- 转为UTC
    event_at AT TIME ZONE '+08' AT TIME ZONE '-05'  -- 时区转换
FROM global_events;

-- 最佳实践：存储用 WITH TIME ZONE，显示时转换
```

---

## 4. 布尔类型

```sql
-- 定义
CREATE TABLE tasks (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    is_completed    BOOLEAN DEFAULT FALSE,
    is_priority     BOOLEAN DEFAULT FALSE,
    is_archived     BOOLEAN DEFAULT FALSE
);

-- 输入方式
INSERT INTO tasks (title, is_completed, is_priority)
VALUES
    ('任务1', TRUE, TRUE),
    ('任务2', FALSE, FALSE),
    ('任务3', 't', '1'),           -- 字符串形式
    ('任务4', 'yes', 'on');        -- 文本形式

-- 布尔运算
SELECT * FROM tasks
WHERE is_completed = FALSE
  AND is_priority IS TRUE
  AND NOT is_archived;

-- 逻辑运算
SELECT * FROM tasks
WHERE (is_completed AND is_priority) OR NOT is_archived;

-- 布尔值存储：1字节
-- 真值：true, true, yes, on, 1, t
-- 假值：false, false, no, off, 0, f
```

---

## 5. 数组类型

### 基础用法

```sql
-- 数组定义
CREATE TABLE products (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100),
    tags            TEXT[],                     -- 文本数组
    prices_history  DECIMAL(10,2)[],            -- 价格历史
    dimensions      INT[3],                     -- 长宽高
    ratings         REAL[]
);

-- 数组字面量
INSERT INTO products (name, tags, prices_history, dimensions)
VALUES
    ('产品A', '{"电子", "数码", "热销"}', '{999.99, 899.99, 799.99}', ARRAY[10, 20, 30]),
    ('产品B', ARRAY['服装', '新品'], ARRAY[199.99, 179.99], ARRAY[1, 2, 3]);

-- 数组操作
SELECT
    array_length(tags, 1),                      -- 数组长度
    tags[1],                                    -- 第一个元素（从1开始！）
    tags[1:2],                                  -- 切片：第1-2个元素
    tags || ARRAY['推荐'],                      -- 数组拼接
    array_append(tags, '新品'),                  -- 追加元素
    array_prepend('最新', tags),                 -- 前置元素
    array_remove(tags, '热销'),                  -- 删除元素
    array_position(tags, '数码'),                -- 查找位置
    array_to_string(tags, ', '),                 -- 转字符串
    string_to_array('a,b,c', ','),              -- 字符串转数组
    unnest(tags),                               -- 展开为行
    tags && ARRAY['热销', '清仓'],               -- 有交集
    '电子' = ANY(tags),                          -- 包含某元素
    '电子' = ALL(ARRAY['电子', '数码']),         -- 等于所有元素
    ARRAY[1, 2, 3] @> ARRAY[2],                 -- 包含子数组
    ARRAY[1, 2, 3] <@ ARRAY[1, 2, 3, 4];        -- 是被包含方

-- 多维数组
CREATE TABLE matrix (
    id    SERIAL,
    data  INT[][]
);

INSERT INTO matrix (data) VALUES ('{{1, 2}, {3, 4}}');

SELECT
    array_ndims(data),                           -- 维度数
    array_upper(data, 1),                       -- 第1维上界
    data[1][1],                                 -- 访问元素
    data[1:1][1:2];                             -- 切片
```

### 数组在WHERE中的使用

```sql
-- 元素匹配
SELECT * FROM products WHERE '热销' = ANY(tags);

-- 交集匹配
SELECT * FROM products WHERE tags && ARRAY['热销', '新品'];

-- 包含匹配
SELECT * FROM products WHERE tags @> ARRAY['电子', '数码'];

-- 数组聚合
SELECT
    array_agg(name ORDER BY name),               -- 聚合成数组
    array_agg(DISTINCT tags[1]),                 -- 去重聚合
    string_agg(name, ', ')                       -- 字符串聚合
FROM products;
```

---

## 6. JSON 类型

### JSON vs JSONB

| 特性 | JSON | JSONB |
|------|------|-------|
| 存储格式 | 原始文本 | 二进制解析 |
| 写入速度 | 快 | 稍慢（需解析） |
| 读取速度 | 慢（每次解析） | 快（已解析） |
| 索引支持 | 不支持 | 支持GIN/GIST |
| 重复键 | 保留所有 | 保留最后一个 |
| 键顺序 | 保留 | 不保留 |
| 推荐度 | 特殊场景 | **默认选择** |

```sql
-- JSONB使用
CREATE TABLE articles (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    content     JSONB,
    metadata    JSONB NOT NULL DEFAULT '{}'::jsonb,
    tags        JSONB DEFAULT '[]'::jsonb
);

-- 写入JSON
INSERT INTO articles (title, content, metadata)
VALUES ('文章标题',
    '{"author": "张三", "body": "正文内容", "score": 95}',
    '{"created_by": "admin", "category": "技术", "version": 1}');

-- 操作符
-- -> 获取JSON对象/数组元素
SELECT content->'author' FROM articles WHERE id = 1;  -- "张三"（带引号）

-- ->> 获取文本值
SELECT content->>'author' FROM articles WHERE id = 1;  -- 张三（无引号）

-- #> 按路径获取
SELECT metadata #> '{tags, 0}' FROM articles;

-- #>> 按路径获取文本
SELECT metadata #>> '{created_by}' FROM articles;

-- @> 包含检查
SELECT * FROM articles WHERE metadata @> '{"category": "技术"}';

-- ? 键存在检查
SELECT * FROM articles WHERE content ? 'author';

-- ?| 任一键存在
SELECT * FROM articles WHERE content ?| ARRAY['author', 'editor'];

-- ?& 所有键存在
SELECT * FROM articles WHERE content ?& ARRAY['author', 'body'];

-- #- 删除键/路径
SELECT metadata - 'version' FROM articles;
SELECT metadata - '{created_by}' FROM articles;

-- || 合并
SELECT '{"a": 1}'::jsonb || '{"b": 2}';  -- {"a": 1, "b": 2}

-- - 对象删除
SELECT '{"a": 1, "b": 2}'::jsonb - '"b"';  -- {"a": 1}
```

### JSONB函数

```sql
-- 构建JSON
SELECT
    json_build_object('id', 1, 'name', '张三', 'active', true),
    json_build_array(1, 'abc', true, NULL),
    json_object '{"a": 1, "b": 2}',
    json_array(1, 2, 3);

-- JSONB操作
SELECT
    jsonb_set(metadata, '{version}', '2', true),        -- 设置值（true=不存在则创建）
    jsonb_insert(metadata, '{tags}', '"新品"'),          -- 写入值
    jsonb_object_keys(metadata),                          -- 所有键
    jsonb_array_elements(tags),                           -- 数组展开
    jsonb_each(content),                                  -- 键值对展开
    jsonb_typeof(content),                                -- 类型检查
    jsonb_array_length(tags),                             -- 数组长度
    jsonb_pretty(content),                                -- 格式化输出
    jsonb_strip_nulls(content),                           -- 去除null
    to_jsonb(products)                                    -- 行转JSON
FROM articles;

-- JSON验证
SELECT
    '{"a": 1}'::json,                                    -- 合法JSON
    json_valid('{"a": 1}'),                               -- 验证JSON字符串
    cast('{"a": 1}' AS jsonb);                            -- 转JSONB
```

### JSONB索引

```sql
-- GIN索引（最常用）
CREATE INDEX idx_article_metadata ON articles USING GIN(metadata);

-- 支持的操作：@>, ?, ?|, ?&
-- 查询可利用索引
SELECT * FROM articles WHERE metadata @> '{"category": "技术"}';
SELECT * FROM articles WHERE metadata ? 'author';

-- 表达式索引
CREATE INDEX idx_metadata_category ON articles USING GIN((metadata->'category'));

-- 具体字段索引
CREATE INDEX idx_metadata_created_by ON articles ((metadata->>'created_by'));

-- GIST索引（用于相邻搜索）
CREATE INDEX idx_article_metadata_gist ON articles USING GIST(metadata);
```

---

## 7. 枚举类型

```sql
-- 创建枚举
CREATE TYPE order_status AS ENUM (
    'pending',
    'confirmed',
    'processing',
    'shipped',
    'delivered',
    'cancelled',
    'refunded'
);

CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high', 'urgent');

-- 使用枚举
CREATE TABLE orders (
    id          BIGSERIAL PRIMARY KEY,
    status      order_status DEFAULT 'pending',
    priority    priority_level DEFAULT 'medium',
    order_at    TIMESTAMP DEFAULT NOW()
);

-- 枚举操作
INSERT INTO orders (status, priority)
VALUES ('pending', 'high'), ('confirmed', 'medium');

-- 枚举有排序（按定义顺序）
SELECT * FROM orders WHERE priority > 'medium' ORDER BY priority;

-- 查看枚举值
SELECT unnest(enum_range(NULL::order_status)) AS status;

-- 修改枚举（只能在首尾添加）
ALTER TYPE order_status ADD VALUE 'returned' AFTER 'delivered';
ALTER TYPE order_status ADD VALUE 'archived' AFTER 'refunded';

-- 不能删除枚举值，不能中间写入
```

---

## 8. 网络地址类型

```sql
-- CIDR地址
CREATE TABLE networks (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100),
    ipv4_net        CIDR,
    ipv6_net        CIDR,
    gateway         INET,
    dns_servers     INET[]
);

INSERT INTO networks (name, ipv4_net, gateway, dns_servers)
VALUES
    ('办公网', '192.168.1.0/24', '192.168.1.1', ARRAY['8.8.8.8'::inet, '8.8.4.4'::inet]),
    ('DMZ', '10.0.0.0/16', '10.0.0.1', ARRAY['10.0.0.2'::inet]),
    ('IPv6网', NULL, NULL, NULL);

-- 操作符
SELECT '192.168.1.100'::inet << '192.168.1.0/24'::cidr;   -- 包含于
SELECT '192.168.1.0/24'::cidr && '192.168.0.0/16'::cidr;  -- 有交集
SELECT '10.0.0.1'::inet = '10.0.0.1'::inet;                -- 相等
SELECT '192.168.1.0/24'::cidr < '192.168.2.0/24'::cidr;   -- 排序

-- 函数
SELECT
    host('192.168.1.0/24'::inet),          -- 192.168.1.0
    netmask('192.168.1.0/24'::inet),       -- 255.255.255.0
    broadcast('192.168.1.0/24'::inet),     -- 192.168.1.255
    network('192.168.1.100/24'::inet),     -- 192.168.1.0/24
    family('192.168.1.1'::inet),           -- 4
    family('::1'::inet),                   -- 6
    inet_same_family('192.168.1.1'::inet, '10.0.0.1'::inet);  -- true

-- MAC地址
CREATE TABLE devices (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100),
    mac     MACADDR
);

INSERT INTO devices (name, mac) VALUES ('交换机', '08:00:2b:4c:5e:fa');
```

---

## 9. 位串类型

```sql
-- 定义
CREATE TABLE bit_data (
    id          SERIAL PRIMARY KEY,
    permissions BIT(8),              -- 固定长度位串
    features    VARBIT(64),          -- 可变长度位串
    flags       BIT(4) DEFAULT B'0000'
);

-- 输入方式
INSERT INTO bit_data (permissions, features, flags)
VALUES
    (B'11010101', B'1010', B'1001'),
    ('11010101'::bit, '1010'::bit varying, '1001'::bit);

-- 操作
SELECT
    permissions | B'00001111',          -- 按位或
    permissions & B'11110000',          -- 按位与
    permissions # B'11110000',          -- 按位异或
    ~permissions,                       -- 按位非
    permissions << 2,                   -- 左移
    permissions >> 2,                   -- 右移
    permissions || B'1111',             -- 拼接
    octet_length(permissions),          -- 字节长度
    bit_length(permissions);            -- 位长度

-- 应用场景：权限位图
-- bit0: 读, bit1: 写, bit2: 执行, bit3: 删除, ...
SELECT * FROM bit_data
WHERE (permissions & B'00000001') = B'00000001';  -- 有读权限
```

---

## 10. XML 类型

```sql
-- 使用
CREATE TABLE documents (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200),
    content     XML
);

-- 写入
INSERT INTO documents (title, content)
VALUES ('文档1', '<root><item id="1">内容</item></root>');

-- XML操作
SELECT
    content -> 0,                              -- 第0个子元素
    content -> 'item',                          -- 命名子元素
    content ->> 'item',                         -- 文本内容
    xml_exists(content, '/root/item');          -- XPath存在检查

-- XML函数
SELECT
    xmlpi(xml 'root'),                          -- 处理指令
    xmlagg(xmlforest(title, content)),          -- XML聚合
    xmlexists('/root/item' PASSING content),    -- XPath查询
    xpath('/root/item', content);               -- XPath提取
```

---

## 11. UUID 类型

```sql
-- 需要扩展
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 使用
CREATE TABLE events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trace_id    UUID DEFAULT gen_random_uuid(),
    event_data  JSONB,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- 写入
INSERT INTO events (event_data) VALUES ('{"type": "login"}');

-- 生成UUID
SELECT
    gen_random_uuid(),                          -- 随机UUID (v4)
    uuid_generate_v1(),                        -- 时间戳UUID (v1，需要uuid-ossp)
    uuid_generate_v4();                        -- 随机UUID (v4，需要uuid-ossp)

-- UUID运算
SELECT
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid,
    uuid IN ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid, 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid);

-- 索引
CREATE INDEX idx_events_trace ON events(trace_id);
```

---

## 12. 几何类型

```sql
-- 基本类型
CREATE TABLE geometry_data (
    id          SERIAL PRIMARY KEY,
    point_val   POINT,
    line_val    LINE,
    segment_val LSEG,
    box_val     BOX,
    path_val    PATH,
    polygon_val POLYGON,
    circle_val  CIRCLE
);

-- 写入
INSERT INTO geometry_data (point_val, line_val, box_val, circle_val)
VALUES
    ('(1, 2)', '((0, 0), (1, 1))', '((0, 0), (10, 10))', '<(5, 5), 3>');

-- 操作符
SELECT
    '(1, 2)'::POINT <@ '((0, 0), (10, 10))'::BOX,    -- 点在框内
    '(1, 2)'::POINT << '(0, 0)'::POINT,               -- 点在左下方
    '((0, 0), (10, 10))'::BOX && '((5, 5), (15, 15))'::BOX;  -- 框相交

-- 函数
SELECT
    point '(1, 2)',
    _point ARRAY['(1, 2)', '(3, 4)'],
    line '((0, 0), (1, 1))',
    segment '((0, 0), (1, 1))',
    box '((0, 0), (10, 10))',
    circle '<(5, 5), 3>',
    diameter(circle '<(5, 5), 3>'),
    center(box '((0, 0), (10, 10))');
```

---

## 13. 范围类型

```sql
-- 内置范围类型
| 范围类型 | 元素类型 | 说明 |
|----------|---------|------|
| INT4RANGE | integer | 整数范围 |
| INT8RANGE | bigint | 大整数范围 |
| NUMRANGE | numeric | 数值范围 |
| TSRANGE | timestamp | 时间范围（无时区） |
| TSTZRANGE | timestamp with time zone | 时间范围（有时区） |
| DATERANGE | date | 日期范围 |

-- 使用
CREATE TABLE bookings (
    id              BIGSERIAL PRIMARY KEY,
    room_id         INTEGER,
    book_name       TEXT,
    price_range     NUMRANGE,
    valid_period    DATERANGE,
    time_slot       TSRANGE
);

-- 写入
INSERT INTO bookings (room_id, book_name, price_range, valid_period, time_slot)
VALUES
    (1, '标准间', numrange(200, 500, '[]'),
     daterange('2026-01-01', '2026-12-31', '[]'),
     tsrange('2026-01-15 14:00', '2026-01-16 11:00', '[)')),
    (2, '豪华间', numrange(500, NULL, '[)'),
     daterange('2026-06-01', NULL),
     tsrange('2026-06-01 14:00', '2026-06-02 11:00', '[)'));

-- 操作符
SELECT * FROM bookings WHERE price_range @> 300;           -- 包含值
SELECT * FROM bookings WHERE price_range && numrange(400, 600);  -- 有重叠
SELECT * FROM bookings WHERE price_range <@ numrange(0, 1000);   -- 被包含
SELECT * FROM bookings WHERE price_range || numrange(500, 800);  -- 合并

-- 边界函数
SELECT
    lower(price_range),                                   -- 下界
    upper(price_range),                                   -- 上界
    lower_inf(price_range),                               -- 下界无穷
    upper_inf(price_range),                               -- 上界无穷
    isempty(price_range),                                 -- 是否为空
    range_merge(price_range) OVER (ORDER BY room_id);     -- 合并相邻范围

-- 自定义范围类型
CREATE TYPE age_range AS RANGE (
    subtype = integer,
    subtype_opclass = int4_ops
);
```

---

## 14. 货币类型

```sql
-- MONEY类型
CREATE TABLE invoices (
    id              SERIAL PRIMARY KEY,
    invoice_no      VARCHAR(50),
    amount          MONEY,
    tax             MONEY DEFAULT '0',
    currency_code   CHAR(3) DEFAULT 'CNY'
);

-- 设置货币符号
SET lc_monetary = 'zh_CN.UTF-8';

-- 写入
INSERT INTO invoices (invoice_no, amount, tax)
VALUES
    ('INV-001', '1000.50', '130.06'),
    ('INV-002', '¥2000.00', '260.00');

-- 注意：MONEY精度有限，金融系统推荐用DECIMAL
-- MONEY存储：8字节，2位小数
-- 替代方案：DECIMAL(15, 2) + currency_code列
```

---

## 15. Oracle 兼容类型

```sql
-- Oracle兼容数据类型映射
| Oracle类型 | KingbaseES等价类型 | 说明 |
|-----------|------------------|------|
| NUMBER | NUMERIC | 可指定精度 |
| NUMBER(p) | NUMERIC(p) | 整数 |
| NUMBER(p, s) | NUMERIC(p, s) | 小数 |
| INT / INTEGER | INTEGER | 等价 |
| SMALLINT | SMALLINT | 等价 |
| FLOAT | DOUBLE PRECISION | 近似小数 |
| FLOAT(n) | REAL 或 DOUBLE PRECISION | n决定精度 |
| BINARY_FLOAT | REAL | IEEE 754单精度 |
| BINARY_DOUBLE | DOUBLE PRECISION | IEEE 754双精度 |
| VARCHAR2(n) | VARCHAR(n) | 变长字符 |
| NVARCHAR2(n) | NVARCHAR(n) | National字符 |
| CHAR(n) | CHAR(n) | 定长字符 |
| NCHAR(n) | NCHAR(n) | National定长 |
| LONG | TEXT | 大文本（不推荐） |
| CLOB | CLOB | 字符大对象 |
| BLOB | BLOB | 二进制大对象 |
| RAW(n) | BYTEA | 原始字节 |
| LONG RAW | BYTEA | 原始字节（不推荐） |
| DATE | DATE | Oracle DATE含时间，KES用TIMESTAMP |
| TIMESTAMP | TIMESTAMP | 时间戳 |
| INTERVAL YEAR TO MONTH | INTERVAL | 间隔 |
| INTERVAL DAY TO SECOND | INTERVAL | 间隔 |

-- Oracle风格建表
CREATE TABLE oracle_emp (
    emp_no        NUMBER(4) PRIMARY KEY,
    emp_name      VARCHAR2(100) NOT NULL,
    salary        NUMBER(10, 2),
    commission    NUMBER(5, 2) DEFAULT 0,
    hire_date     DATE,
    resume        CLOB,
    photo         BLOB,
    card_hash     RAW(2000),
    notes         NVARCHAR2(500)
);

-- NUMBER类型的灵活使用
CREATE TABLE number_demo (
    col_int       NUMBER,             -- 同INTEGER
    col_small     NUMBER(3),          -  -3 ~ 999
    col_decimal   NUMBER(10, 2),      -- 99999999.99
    col_big       NUMBER(38),         -- Oracle最大精度
    col_mONEY     NUMBER(15, 2)       -- 金融精度
);
```

---

## 16. SQLServer 兼容类型

```sql
-- SQLServer兼容模式下的额外数据类型
| SQLServer类型 | KingbaseES等价类型 | 存储 | 范围 |
|--------------|------------------|------|------|
| TINYINT | TINYINT | 1字节 | 0 ~ 255 |
| SMALLMONEY | SMALLMONEY | 4字节 | -214,748.3648 ~ 214,748.3647 |
| MONEY | MONEY | 8字节 | 同MONEY类型 |
| BIT | BOOLEAN | 1字节 | 0/1 |
| UNIQUEIDENTIFIER | UUID | 16字节 | 标准UUID |

-- TINYINT使用示例
CREATE TABLE status_table (
    id SERIAL PRIMARY KEY,
    status_code TINYINT,          -- 0-255范围的状态码
    priority TINYINT DEFAULT 0    -- 优先级0-255
);

-- SMALLMONEY使用示例
CREATE TABLE small_amounts (
    id SERIAL PRIMARY KEY,
    amount SMALLMONEY             -- 小额金钱（4字节，4位小数）
);
```

---

## 17. 二进制类型

```sql
-- BYTEA使用
CREATE TABLE files (
    id              SERIAL PRIMARY KEY,
    filename        VARCHAR(200),
    content_type    VARCHAR(100),
    data            BYTEA,
    file_size       BIGINT
);

-- 写入方式
INSERT INTO files (filename, data)
VALUES
    ('test.bin', '\xdeadbeef'),                    -- 十六进制
    ('test2.bin', decode('deadbeef', 'hex'));      -- decode函数

-- 读取
SELECT
    encode(data, 'hex'),                            -- 转十六进制
    encode(data, 'base64'),                         -- 转base64
    length(data),                                   -- 字节长度
    data LIKE '\xdead%'                            -- 模式匹配
FROM files;

-- 大文件用LOB
CREATE TABLE large_files (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200),
    binary_data     BLOB,
    text_data       CLOB
);

-- BLOB操作（通过大对象）
INSERT INTO large_files (name, binary_data)
VALUES ('document.pdf', LO_FROM_BYTEA(sys_read_binary_file('/path/file.pdf')));
```

---

## 18. 数据类型选择指南

### 选择原则

```
┌─────────────────────────────────────────────────────────┐
│  数值                                                   │
│  · 计数器/ID → INTEGER / BIGINT                        │
│  · 金额/金融 → DECIMAL(p,2)                            │
│  · 科学计算 → DOUBLE PRECISION                         │
│  · 百分比 → DECIMAL(5,2)                               │
├─────────────────────────────────────────────────────────┤
│  字符串                                                  │
│  · 有长度限制 → VARCHAR(n)                             │
│  · 无限制文本 → TEXT                                   │
│  · 固定编码 → CHAR(n)                                  │
│  · 结构数据 → JSONB                                    │
├─────────────────────────────────────────────────────────┤
│  日期时间                                                │
│  · 仅日期 → DATE                                       │
│  · 需精确时间 → TIMESTAMP WITH TIME ZONE               │
│  · 持续时间 → INTERVAL                                 │
├─────────────────────────────────────────────────────────┤
│  特殊类型                                                │
│  · 分布式ID → UUID                                     │
│  · 标签/分类 → TEXT[] 或 JSONB                         │
│  · 状态 → ENUM                                         │
│  · IP地址 → INET                                       │
│  · 权限位图 → BIT(n)                                   │
└─────────────────────────────────────────────────────────┘
```

### 存储效率对比

| 场景 | 推荐类型 | 存储 | 避免 |
|------|---------|------|------|
| 用户ID | BIGINT (BIGSERIAL) | 8字节 | VARCHAR |
| 金额 | DECIMAL(12,2) | 变量 | REAL/FLOAT |
| 长文本 | TEXT | 实际长度 | VARCHAR(99999) |
| 配置项 | JSONB | 可索引 | 拆成多列 |
| 布尔标志 | BOOLEAN | 1字节 | SMALLINT |
| 固定状态 | ENUM | 4字节 | VARCHAR+CHECK |
| 多标签 | TEXT[] | 可变 | VARCHAR拼接 |
| 时间戳 | TIMESTAMPTZ | 8字节 | VARCHAR |

### 常见错误

```sql
-- 错误1：用VARCHAR存数字
CREATE TABLE bad (phone VARCHAR(20));    -- OK：电话号码不是数字运算
CREATE TABLE bad (amount VARCHAR(20));    -- BAD：应该用DECIMAL

-- 错误2：用FLOAT存金额
CREATE TABLE bad (price FLOAT);           -- BAD：精度丢失
CREATE TABLE good (price DECIMAL(10, 2)); -- GOOD

-- 错误3：用TIMESTAMP代替DATE
CREATE TABLE bad (birthday TIMESTAMP);    -- BAD：不需要时间部分
CREATE TABLE good (birthday DATE);        -- GOOD

-- 错误4：用VARCHAR存布尔
CREATE TABLE bad (is_active VARCHAR(1));  -- BAD
CREATE TABLE good (is_active BOOLEAN);    -- GOOD

-- 错误5：不定长用CHAR
CREATE TABLE bad (name CHAR(200));        -- BAD：浪费空间
CREATE TABLE good (name VARCHAR(200));    -- GOOD
```

---

## 19. 类型转换

```sql
-- 显式转换
SELECT
    '123'::INTEGER,                           -- 强制转换
    CAST('123' AS INTEGER),                   -- SQL标准
    '123.45'::DECIMAL(5,2),                   -- 小数转换
    123::TEXT,                                -- 转文本
    TRUE::INTEGER,                            -- 1
    FALSE::INTEGER,                           -- 0
    NOW()::DATE,                              -- 时间戳转日期
    NOW()::TIMESTAMP,                         -- 去时区
    '{"a": 1}'::jsonb,                        -- 字符串转JSONB
    to_jsonb(ROW(1, 'abc'));                  -- 行转JSON

-- 隐式转换
SELECT '123' + 1;                            -- '123'自动转INTEGER
SELECT 1 || 'abc';                           -- 1自动转TEXT

-- JSONB类型转换
SELECT
    to_jsonb('hello'::TEXT),                  -- "hello"
    to_jsonb(123::INTEGER),                   -- 123
    to_jsonb(ROW(1, 'abc', TRUE)),           -- [1, "abc", true]
    '{"name": "张三", "age": 30}'::jsonb ->> 'age';  -- "30"（文本）

-- 数组类型转换
SELECT
    array[1, 2, 3]::INT[],
    string_to_array('a,b,c', ',')::TEXT[],
    array_agg(id)::INT[] FROM (SELECT generate_series(1, 5) AS id) t;
```
