---
title: SELECT
description: When generating the select query for KaiwuDB/KWDB, following this template.
---
## 语法格式
SELECT [ { ALL | DISTINCT [ ON ( a_expr [, a_expr ... ] ) ] } ]
       target_elem [, target_elem ... ]
FROM table_name [ alias_clause ] [, table_name [ alias_clause ] ... ]
     [ as_of_clause ]
[ WHERE a_expr ]
[ GROUP BY { a_expr [, a_expr ... ] | 
             primary_tag [, primary_tag ... ] | 
             group_window_func } ]
[ HAVING a_expr ]
[ order_by_clause ]
[ ( limit_clause [ offset_clause ] | offset_clause [ limit_clause ] ) ]

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `order_by_clause` | `ORDER BY` 子句由一个或多个排序规范组成，每个规范可以是标量表达式。系统通过给定的排序规范对结果集进行排序，可以指定 `ASC`（升序，默认）或 `DESC`（降序）关键字来控制排序顺序。|
| `limit_clause` | `LIMIT` 子句指定返回结果的最大行数。例如，`LIMIT 10` 表示限制查询结果最多为 10 行。支持设置为 `LIMIT ALL`，表示返回所有行。KWDB 也支持使用 `sql.auto_limit.quantity` 集群参数配置 SQL 查询结果的返回行数。但是，`Limit` 子句的优先级大于 `sql.auto_limit.quantity` 集群参数。 |
| `offset_clause` | `OFFSET` 子句用于跳过前面的偏移量行数。`OFFSET` 子句通常与 `LIMIT` 组合使用，通过限制结果的数量，实现分页显示结果，避免一次性检索所有数据。|
| `DISTINCT` | 当使用 `DISTINCT` 关键字时，系统删除返回结果中重复的行。 |
| `target_elem` | `target_elem` 可以是标量表达式，也可以是星号（`*`）。<br >- 当 `target_elem` 是标量表达式时，系统使用标量表达式计算每个结果行的值，然后将计算结果作为结果集中的一列返回。<br >- 当 `target_elem` 为星号（`*`）时，系统自动从 `FROM` 子句中检索所有列。如果 `target_elem` 包含聚合函数，可以使用 `GROUP BY` 子句进一步控制聚合。 |
| `alias_clause` | 别名子句，用于为表名或子查询结果集指定别名，使查询更易读和易于理解。|
| `as_of_clause` | 用于检索指定时间点的数据。<br >**说明** <br >由于系统时间返回的是历史数据，读取的结果可能会过时。|
| `WHERE` | `WHERE` 子句用于指定过滤条件，筛选出符合条件的行。格式为 `WHERE <column> <operator> <value>`，其中 `<operator>` 支持 `=`、`<>`、`<`、`<=`、`>`、`>=`、`LIKE` 操作符。`WHERE` 语句只检索表达式返回值为 `TRUE` 的行。列可以是数据列或标签列。 |
| `GROUP BY` | `GROUP BY` 子句根据表达式或分组窗口函数将数据集划分成小组，然后对这些小组进行数据处理。聚合查询与 `GROUP BY` 连用时，应避免 `GROUP BY` 后的结果集行数过大。关于分组窗口函数的详细信息，参见[分组窗口查询](#分组窗口查询)。 |
| `HAVING` | 当 `WHERE` 关键字无法与聚合函数一起使用时，`HAVING` 子句可以用来筛选分组后的各组数据。通常情况下，`HAVING` 子句与 `GROUP BY` 子句联用，只检索 `a_expr` 表达式返回值为 `TRUE` 的聚合函数组。`a_expr` 必须是使用聚合函数返回布尔值的标量表达式（例如 `<聚合函数> = <value>`）。`HAVING` 子句的作用类似于 `WHERE` 子句，但适用于聚合函数。|

## 时间窗口过滤

KWDB 支持在查询中对列类型为时间戳、时间戳常量以及结果类型为时间戳的函数和表达式按最高精度进行加减运算并返回运算结果。运算结果支持使用大于号（`>`）、小于号（`<`）、等号（`=`）、大于等于号（`>=`）、小于等于号（`<=`）进行比较。运算中可以包含 `interval` 常量、其他时间戳列以及结果类型为 interval、timestamp 或 timstamptz 的函数和表达式。如果运算符两边均为 timestamp 或 timestamptz 类型，则只支持减法运算。

加减运算中，`interval` 常量支持的单位包括纳秒（ns）、微秒（us）、毫秒（ms）、秒（s）、分（m）、小时（h）、天（d）、周（w）、月（mon）、年（y）。目前，KWDB 不支持复合时间格式，如 `1d1h`。

毫秒、秒、分、小时的取值范围受纳秒最大值（INT64）范围限制。下表列出具体支持的取值范围：

| 单位      | 取值范围                                |
| --------- | --------------------------------------- |
| 纳秒（ns） | [0, 9,214,646,400,000,000,000] |
| 微秒（us） | [-62,167,219,200,000, 31,556,995,200,000] |
| 毫秒（ms） | [-9,223,372,036,854, 9,223,372,036,854] |
| 秒（s）    | [-9,223,372,036, 9,223,372,036]         |
| 分（m）    | [-153,722,867, 153,722,867]             |
| 小时（h）  | [-2,562,047, 2,562,047]                 |

天、周、月、年的取值范围受加减计算结果的限制。计算结果对应的毫秒数不得超过 INT64 范围。

::: warning 说明
时间加减表达式支持出现在以下位置：

- `SELECT` 列表：例如 `SELECT ts+1h FROM table1;` 将返回表中时间戳列加上 1 小时后的结果。
- `WHERE` 子句：例如 `SELECT * FROM table1 WHERE ts+1h > now();` 将返回表中时间戳列加上 1 小时后大于当前时间的数据。
- `ORDER BY` 子句：例如 `SELECT * FROM table1 ORDER BY ts+1h;` 将按时间戳列加上 1 小时后的值进行排序。
- `HAVING` 子句：例如 `SELECT MAX(ts) FROM table1 GROUP BY ts HAVING ts+1h > now();` 将筛选出满足条件的分组结果。
- 参数类型为 timestamp 的函数调用：例如 `SELECT CAST(ts+1h AS timestamp) FROM table1;` 可以将时间戳列加上 1 小时后的结果转换为 timestamp 类型。
- 使用比较运算符的表示连接条件：例如 `SELECT * FROM table1,table2 WHERE table1.ts+1h > table2.ts;` 表示在连接两个表时使用时间加减条件。

## 语法示例

- 查询时序表的数据。
    SELECT * FROM t1;

- 查询指定的数据列并求和。
    SELECT sum(a) FROM ts_db.t1;
  
- 去重查询。
    SELECT DISTINCT a FROM ts_db.t1;

- 使用 `WHERE` 语句过滤标签列。
    SELECT tag1 FROM ts_db.t1 WHERE a =11;

- 使用 `GROUP BY` 和 `ORDER BY` 语句对数据列进行分类和排序。
    SELECT a, max(b) FROM ts_db.t1 GROUP BY a ORDER BY a;

## 分组窗口查询

- 目前，分组窗口查询必须与 `GROUP BY` 子句搭配使用，且分组列需置于窗口函数之前。分组列支持主标签、普通标签和数据列，以及上述列的任意组合。
- 分组窗口查询目前仅支持单表查询，不支持嵌套查询、关联查询、联合查询。分组条件仅支持数据列或标签列，不支持表达式（如 `a+b`、`abs(a)` 等）。

### 语法格式

GROUP BY
    [ column_list [, column_list ... ] ]
  | COUNT_WINDOW ( row_limit [, sliding_row ] )
  | EVENT_WINDOW ( start_condition , end_condition )
  | SESSION_WINDOW ( ts_column , session_threshold )
  | STATE_WINDOW ( column_name | case_when_expr )
  | TIME_WINDOW ( ts_column , interval [, sliding_interval ] )

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `column_list` | 可选参数，指定一个或多个分组列，包括主标签、普通标签和数据列，列名之间用逗号分隔。 |
| `row_limit` | 计数窗口中，指定分组的数据行数。 |
| `sliding_rows` | 计数窗口中，指定相邻窗口起始点间的差距，以控制窗口的重叠程度，值必须小于或等于 `row_limit`。|
| `start_condition` | 事件窗口中，指定窗口开始的条件，可以是任意表达式，也可以涉及不同的列。 |
| `end_condition` | 事件窗口中，指定窗口结束的条件，可以是任意表达式，也可以涉及不同的列。  |
| `ts_column` | 会话窗口和时间窗口中，指定第一列时间戳列。|
| `session_threshold` | 会话窗口中，指定最大连续时间间隔。如果两条相邻数据的时间间隔超过会话允许的最大时间间隔时，则数据分属于不同窗口。支持的单位包括 `s`（秒）、`m` (分)、`h` (时)、`d` (天)和 `w` (周) ，不支持复合时间格式，例如 `1m2s`。 |
| `column_name` | 状态窗口中，指定表的数据列或标签列。<br>- 当指定列为数据列时，其数据类型必须为整数、布尔值或除 GEOMETRY 之外的字符类型。<br>- 当指定列为标签列时，其数据类型必须为整数、布尔值或除 GEOMETRY 和 NVARCHAR 之外的字符类型。|
| `case_when_expr` | 状态窗口中，表示满足指定条件后状态开始或结束的表达式，例如，`STATE_WINDOW (CASE WHEN voltage >= 225 AND voltage <= 235 THEN 1 ELSE 0 END)` 表示当电压在 225 至 235 之间时，状态为 1，否则为 0。|
| `interval` | 时间窗口中，指定时间间隔, 单位包括毫秒、秒、分、小时、天、周、月、年，不支持复合时间格式，如 `1d1h`。时间间隔必须不小于 10 毫秒。<br> 各时间单位支持的输入格式如下所示：<br>- 毫秒：`ms`、`msec`、`msecs`、`millisecond`、`milliseconds` <br> - 秒：`s`、`sec`、`secs`、`second`、`seconds` <br> - 分：`m`、`min`、`mins`、`minute`、`minutes` <br> - 小时：`h`、`hr`、`hrs`、`hour`、`hours`<br> - 天：`d`、`day`、`days` <br> - 周：`w`、`week`、`weeks` <br> - 月：`mon`、`mons`、`month`、`months` <br> - 年：`y`、`yr`、`yrs`、`year`、`years` |
| `sliding_interval` | 时间窗口函数中，指定滑动偏移间隔。支持的单位包括毫秒、秒、分、小时、天、周，不支持复合时间格式，如 `1d1h`。  <br> 各时间单位支持的输入格式如下所示：<br>- 毫秒：`ms`、`msec`、`msecs`、`millisecond`、`milliseconds` <br> - 秒：`s`、`sec`、`secs`、`second`、`seconds` <br> - 分：`m`、`min`、`mins`、`minute`、`minutes` <br> - 小时：`h`、`hr`、`hrs`、`hour`、`hours`<br> - 天：`d`、`day`、`days` <br> - 周：`w`、`week`、`weeks` <br> **注意**：时间间隔与滑动偏移间隔不宜相差太大，否则可能会影响查询性能，如果窗口过多，还会导致内存不足。|

### 语法示例
- 使用时间窗口进行聚合查询，各窗口间不重叠
    SELECT count(ts) as records, avg(speed) as avg_speed FROM vehicles GROUP BY TIME_WINDOW (ts,'10m');

## 嵌套查询
KWDB 支持以下嵌套查询：
- 相关子查询（Correlated Subquery）：内部查询依赖于外部查询的结果，每次外部查询都触发内部查询。
- 非相关子查询（Non-Correlated Subquery）：内部查询独立于外部查询，只执行一次内部查询并返回固定的结果。
- 相关投影子查询（Correlated Scalar Subquery）：内部查询依赖于外部查询的结果，并且只返回一个单一的值作为外部查询的结果。
- 非相关投影子查询（Non-Correlated Scalar Subquery）：内部查询独立于外部查询，并且只返回一个单一的值作为外部查询的结果。
- `FROM` 子查询：将一个完整的 SQL 查询嵌套在另一个查询的 `FROM` 子句中，作为临时表格使用。

### 语法格式

select_clause [ ( select_clause ) ]

### 参数说明

无

### 语法示例

- 非相关子查询
    SELECT e1 FROM ts_stable1 WHERE e1 = (SELECT avg (e1) FROM t1.stable);
    
- 非相关投影子查询
    SELECT first (e1) = (SELECT e1 FROM ts_stable2 limit 1) FROM ts_stable1;
  
- 相关子查询
    SELECT e1 FROM t1.stable WHERE e1 in (SELECT e1 FROM t1.stable2 WHERE stable.e2=stable2.e2);

- 相关投影子查询
    SELECT sum(e1) = (SELECT e1 FROM ts_stable2 WHERE ts_stable2.e1=e1) FROM ts_stable1;

- `FROM` 子查询
    SELECT avg (a) FROM (SELECT e1 as a FROM t1.ts_stable1);

## 关联查询

KWDB 支持以下关联类型:
- 内连接（INNER JOIN）
- 左连接（LEFT JOIN）
- 右连接（RIGHT JOIN）
- 全连接（FULL JOIN）

### 语法格式

joined_table
    : '(' joined_table ')'
    | table_ref
        ( CROSS [ opt_join_hint ] JOIN table_ref
        | NATURAL [ ( FULL | LEFT | RIGHT ) [ OUTER ] | INNER ] [ opt_join_hint ] JOIN table_ref
        | [ ( FULL | LEFT | RIGHT ) [ OUTER ] | INNER ] [ opt_join_hint ] JOIN table_ref
            ( ON a_expr
            | USING ( name [, name ... ] )
            )
        )
    ;

- `opt_join_hint`

  opt_join_hint
    : HASH
    | MERGE
    | LOOKUP
    | INVERTED
  ;

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `joined_table` | 连接表达式。|
| `table_ref` | 表的表达式。 |
| `opt_join_hint` | 可选项，连接提示。 |
| `a_expr` | ON 连接条件的标量表达式。 |
| `name` | USING 连接条件的列名。|

### 语法示例
SELECT ts_table1.e1, ts_table2.e1 FROM ts_table1 LEFT JOIN ts_table2 ON ts_table1.e1 = ts_table2.e1;