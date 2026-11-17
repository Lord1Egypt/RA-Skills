# KingbaseES PL/SQL 编程参考

包括过程化SQL基本语法、存储过程、函数、触发器、游标、包、异常处理和动态SQL。

**重要**：PL/SQL函数始终使用金仓原生语法，与Oracle兼容模式无关。

## 1. 基本语法

### 匿名块

```sql
-- 基本结构
BEGIN
    DECLARE v_count INT;
    DECLARE v_name VARCHAR(100) = 'Kingbase';
    SELECT count(*) INTO v_count FROM sys_tables;
    RAISE NOTICE '表数量: %, 数据库: %', v_count, v_name;
END;

-- 带异常处理
BEGIN
    DECLARE v_value DECIMAL(10, 2);
    v_value := 100 / 0;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE '除零错误: %', SQLERRM;
    WHEN OTHERS THEN
        RAISE NOTICE '未知错误: % - %', SQLSTATE, SQLERRM;
END;
```

### 变量声明

```sql
DECLARE
    -- 基本类型
    v_name    VARCHAR(100);
    v_age     INT;
    v_salary  DECIMAL(12, 2);
    v_hire    DATE;
    v_now     TIMESTAMP;

    -- 使用 DEFAULT
    v_status  VARCHAR(20) DEFAULT 'active';

    -- 使用 %TYPE（继承列类型）
    v_emp_name    employees.name%TYPE;
    v_emp_id      employees.id%TYPE;

    -- 使用 %ROWTYPE（整行类型）
    v_emp_row     employees%ROWTYPE;

    -- 记录类型
    TYPE rec_type IS RECORD (
        id      INT,
        name    VARCHAR(100),
        salary  DECIMAL(10, 2)
    );
    v_rec   rec_type;

    -- 数组
    v_ids   INT[];
    v_arr   INT[] := ARRAY[1, 2, 3];

    -- 常量
    c_tax   DECIMAL(3, 2) := 0.08;
```

### 数据类型速查

| 类型 | 说明 | 示例 |
|------|------|------|
| `INT` / `INTEGER` | 整数 | `v_count INT := 0` |
| `BIGINT` | 大整数 | `v_big BIGINT := 0` |
| `DECIMAL(p,s)` | 精确小数 | `v_price DECIMAL(10,2)` |
| `NUMERIC(p,s)` | 同DECIMAL | `v_amt NUMERIC(12,2)` |
| `VARCHAR(n)` | 变长字符串 | `v_name VARCHAR(100)` |
| `TEXT` | 长文本 | `v_desc TEXT` |
| `DATE` | 日期 | `v_date := CURRENT_DATE` |
| `TIMESTAMP` | 时间戳 | `v_ts := NOW()` |
| `BOOLEAN` | 布尔 | `v_flag BOOLEAN := TRUE` |
| `BYTEA` | 二进制 | `v_data BYTEA` |
| `UUID` | 唯一标识 | `v_uuid UUID` |
| `JSON` / `JSONB` | JSON数据 | `v_json JSONB` |
| `INT[]` | 整数数组 | `v_arr INT[] := ARRAY[1,2]` |
| `oid` | 对象ID | `v_oid oid` |

---

## 2. 控制结构

### 条件分支

```sql
-- IF/ELSIF/ELSE
IF v_salary > 20000 THEN
    v_grade := 'S';
ELSIF v_salary > 15000 THEN
    v_grade := 'A';
ELSIF v_salary > 10000 THEN
    v_grade := 'B';
ELSE
    v_grade := 'C';
END IF;

-- CASE
v_grade := CASE
    WHEN v_score >= 90 THEN '优秀'
    WHEN v_score >= 80 THEN '良好'
    WHEN v_score >= 60 THEN '及格'
    ELSE '不及格'
END;

-- 搜索CASE
CASE
    WHEN v_age < 18 THEN v_category := '未成年';
    WHEN v_age < 60 THEN v_category := '成年';
    ELSE v_category := '退休';
END CASE;
```

### 循环

```sql
-- LOOP（无限循环）
v_sum := 0;
v_i := 1;
LOOP
    v_sum := v_sum + v_i;
    v_i := v_i + 1;
    EXIT WHEN v_i > 100;
END LOOP;

-- WHILE LOOP
v_i := 1;
WHILE v_i <= 100 LOOP
    v_sum := v_sum + v_i;
    v_i := v_i + 1;
END LOOP;

-- FOR LOOP（整数范围）
FOR v_i IN 1..100 LOOP
    v_sum := v_sum + v_i;
END LOOP;

-- 反向
FOR v_i IN REVERSE 100..1 LOOP
    -- 处理
END LOOP;

-- 自定义步长
FOR v_i IN 1..100..5 LOOP  -- 步长为5: 1, 6, 11, ...
    -- 处理
END LOOP;

-- FOR LOOP（游标）
FOR v_rec IN SELECT id, name, salary FROM employees LOOP
    RAISE NOTICE 'ID: %, Name: %, Salary: %', v_rec.id, v_rec.name, v_rec.salary;
END LOOP;

-- FOR LOOP（带WHERE条件）
FOR v_rec IN
    SELECT id, name FROM employees WHERE dept_id = v_dept_id
ORDER BY name
LOOP
    -- 处理
END LOOP;
```

### 标签

```sql
-- 标签循环
<<outer_loop>>
FOR v_dept IN SELECT id FROM departments LOOP
    FOR v_emp IN SELECT id FROM employees WHERE dept_id = v_dept.id LOOP
        -- 处理
    END LOOP;
END LOOP outer_loop;

-- LEAVE标签
<<process>>
LOOP
    IF v_condition THEN
        LEAVE process;
    END IF;
END LOOP process;

-- NEXT LOOP跳至下一轮
FOR v_i IN 1..100 LOOP
    IF v_i % 2 = 0 THEN
        NEXT LOOP;  -- 跳过偶数
    END IF;
    -- 处理奇数
END LOOP;
```

---

## 3. 存储过程

### 创建存储过程

```sql
-- 基本过程
CREATE OR ALTER PROCEDURE update_employee_salary(
    IN  p_emp_id   INT,
    IN  p_rate     DECIMAL(5, 2)
)
AS
DECLARE
    v_old_salary  DECIMAL(10, 2);
    v_new_salary  DECIMAL(10, 2);
BEGIN
    SELECT salary INTO v_old_salary
    FROM employees WHERE id = p_emp_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION '员工不存在: %', p_emp_id;
    END IF;

    v_new_salary := v_old_salary * (1 + p_rate / 100);

    UPDATE employees
    SET salary = v_new_salary,
        updated_at = NOW()
    WHERE id = p_emp_id;

    RAISE NOTICE '薪资调整: % -> %, 员工: %', v_old_salary, v_new_salary, p_emp_id;
END;


-- 调用
CALL update_employee_salary(1, 10.00);
```

### OUT参数

```sql
CREATE OR ALTER PROCEDURE get_employee_info(
    IN  p_emp_id   INT,
    OUT p_name     VARCHAR(100),
    OUT p_salary   DECIMAL(10, 2),
    OUT p_dept     VARCHAR(100)
)
AS
BEGIN
    SELECT e.name, e.salary, d.name
    INTO p_name, p_salary, p_dept
    FROM employees e
    JOIN departments d ON e.dept_id = d.id
    WHERE e.id = p_emp_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION '员工不存在: %', p_emp_id;
    END IF;
END;


-- 调用
CALL get_employee_info(1, NULL, NULL, NULL);
-- 或
BEGIN
DECLARE
    r_name   VARCHAR(100);
    r_salary DECIMAL(10, 2);
    r_dept   VARCHAR(100);
BEGIN
    CALL get_employee_info(1, r_name, r_salary, r_dept);
    RAISE NOTICE '%, %, %', r_name, r_salary, r_dept;
END;

```

### INOUT参数

```sql
CREATE OR ALTER PROCEDURE swap_values(
    INOUT p_a   INT,
    INOUT p_b   INT
)
AS
DECLARE
    v_temp INT;
BEGIN
    v_temp := p_a;
    p_a := p_b;
    p_b := v_temp;
END;

```

### 带事务的过程

```sql
CREATE OR ALTER PROCEDURE transfer_funds(
    IN  p_from_id   INT,
    IN  p_to_id     INT,
    IN  p_amount    DECIMAL(12, 2)
)
AS
DECLARE
    v_from_balance  DECIMAL(12, 2);
BEGIN
    -- 检查余额
    SELECT balance INTO v_from_balance
    FROM accounts WHERE id = p_from_id
    FOR UPDATE;

    IF v_from_balance < p_amount THEN
        RAISE EXCEPTION '余额不足: %, 需要: %', v_from_balance, p_amount;
    END IF;

    -- 扣款
    UPDATE accounts
    SET balance = balance - p_amount,
        updated_at = NOW()
    WHERE id = p_from_id;

    -- 入账
    UPDATE accounts
    SET balance = balance + p_amount,
        updated_at = NOW()
    WHERE id = p_to_id;

    -- 记录流水
    INSERT INTO transactions (from_id, to_id, amount, trans_time)
    VALUES (p_from_id, p_to_id, p_amount, NOW());

    COMMIT;  -- 注意：在过程中COMMIT/ROLLBACK会创建子事务边界
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END;

```

### 管理存储过程

```sql
-- 查看过程定义
SELECT routine_name, routine_definition
FROM sys_information_schema.routines
WHERE routine_schema = 'public'
  AND routine_type = 'PROCEDURE';

-- 查看过程依赖
SELECT * FROM sys_dependent WHERE refobjid = 'update_employee_salary()'::regproc;

-- 删除过程
DROP PROCEDURE IF EXISTS update_employee_salary(INT, DECIMAL);
```

---

## 4. 函数

### 标量函数

```sql
CREATE OR ALTER FUNCTION calc_bonus(
    p_salary   DECIMAL(10, 2),
    p_grade    CHAR(1)
) RETURNS DECIMAL(10, 2)
AS
DECLARE
    v_rate    DECIMAL(3, 2);
BEGIN
    v_rate := CASE p_grade
        WHEN 'S' THEN 0.30
        WHEN 'A' THEN 0.20
        WHEN 'B' THEN 0.10
        ELSE 0.05
    END;

    RETURN p_salary * v_rate;
END;


-- 调用
SELECT calc_bonus(15000, 'A');
```

### 表返回函数

```sql
-- 返回表
CREATE OR ALTER FUNCTION get_employees_by_dept(
    p_dept_id   INT
) RETURNS TABLE (
    emp_id      INT,
    emp_name    VARCHAR(100),
    salary      DECIMAL(10, 2),
    hire_date   DATE
)
AS
BEGIN
    RETURN QUERY
    SELECT e.id, e.name, e.salary, e.hire_date
    FROM employees e
    WHERE e.dept_id = p_dept_id
    ORDER BY e.name;
END;


-- 调用
SELECT * FROM get_employees_by_dept(10);
```

### SETOF函数

```sql
CREATE OR ALTER FUNCTION get_top_earners(
    p_count   INT DEFAULT 10
) RETURNS SETOF employees
AS
BEGIN
    RETURN QUERY
    SELECT * FROM employees
    ORDER BY salary DESC
    LIMIT p_count;
END;


-- 调用
SELECT * FROM get_top_earners(5);
```

### 游标返回函数

```sql
CREATE OR ALTER FUNCTION query_employees(
    p_dept_id   INT
) RETURNS CURSOR
AS
DECLARE
    v_cur   CURSOR;
BEGIN
    OPEN v_cur FOR
        SELECT * FROM employees WHERE dept_id = p_dept_id;
    RETURN v_cur;
END;


-- 调用
BEGIN;
SELECT query_employees(10);
FETCH ALL IN cursor_name;
COMMIT;
```

### 聚合计算函数

```sql
CREATE OR ALTER FUNCTION dept_salary_stats(
    p_dept_id   INT,
    OUT p_avg   DECIMAL(10, 2),
    OUT p_max   DECIMAL(10, 2),
    OUT p_min   DECIMAL(10, 2),
    OUT p_count INT
)
AS
BEGIN
    SELECT avg(salary), max(salary), min(salary), count(*)
    INTO p_avg, p_max, p_min, p_count
    FROM employees
    WHERE dept_id = p_dept_id;
END;

```

### 管理函数

```sql
-- 查看函数
SELECT routine_name, data_type, routine_definition
FROM sys_information_schema.routines
WHERE routine_schema = 'public'
  AND routine_type = 'FUNCTION';

-- 删除函数
DROP FUNCTION IF EXISTS calc_bonus(DECIMAL, CHAR);
```

---

## 5. 触发器

### 行级触发器

```sql
-- 创建触发器函数
CREATE OR ALTER FUNCTION trg_audit_employee()
RETURNS TRIGGER
AS
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO employee_audit (emp_id, action, action_time, old_data, new_data)
        VALUES (NEW.id, 'INSERT', NOW(), NULL, row_to_json(NEW)::TEXT);
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE THEN
        INSERT INTO employee_audit (emp_id, action, action_time, old_data, new_data)
        VALUES (NEW.id, 'UPDATE', NOW(), row_to_json(OLD)::TEXT, row_to_json(NEW)::TEXT);
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO employee_audit (emp_id, action, action_time, old_data, new_data)
        VALUES (OLD.id, 'DELETE', NOW(), row_to_json(OLD)::TEXT, NULL);
        RETURN OLD;
    END IF;

    RETURN NULL;
END;


-- 创建触发器
CREATE TRIGGER trg_employee_audit
AFTER INSERT OR UPDATE OR DELETE ON employees
FOR EACH ROW
EXECUTE FUNCTION trg_audit_employee();
```

### BEFORE触发器（数据校验）

```sql
CREATE OR ALTER FUNCTION trg_validate_salary()
RETURNS TRIGGER
AS
BEGIN
    IF NEW.salary <= 0 THEN
        RAISE EXCEPTION '薪资必须大于0: %', NEW.salary;
    END IF;

    IF NEW.salary > 1000000 THEN
        RAISE WARNING '薪资异常高: %, 请确认', NEW.salary;
    END IF;

    -- 自动更新时间戳
    NEW.updated_at := NOW();

    RETURN NEW;
END;


CREATE TRIGGER trg_validate_salary
BEFORE INSERT OR UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION trg_validate_salary();
```

### INSTEAD OF触发器（视图）

```sql
-- 创建可更新视图的触发器
CREATE OR ALTER FUNCTION trg_view_insert()
RETURNS TRIGGER
AS
BEGIN
    INSERT INTO employees (name, dept_id, salary, hire_date)
    VALUES (NEW.name, NEW.dept_id, NEW.salary, NEW.hire_date);
    RETURN NEW;
END;


CREATE TRIGGER trg_view_insert
INSTEAD OF INSERT ON emp_view
FOR EACH ROW
EXECUTE FUNCTION trg_view_insert();
```

### 语句级触发器

```sql
CREATE OR ALTER FUNCTION trg_log_changes()
RETURNS TRIGGER
AS
BEGIN
    IF TG_OP = 'INSERT' THEN
        RAISE NOTICE '批量写入触发: % 行', TG_TABLE_NAME;
    END IF;
    RETURN NULL;
END;


CREATE TRIGGER trg_log_changes
AFTER TRUNCATE ON employees
FOR EACH STATEMENT
EXECUTE FUNCTION trg_log_changes();
```

### 触发器管理

```sql
-- 查看触发器
SELECT trigger_name, event_manipulation, action_timing, action_statement
FROM sys_information_schema.triggers
WHERE event_object_table = 'employees';

-- 禁用触发器
ALTER TABLE employees DISABLE TRIGGER trg_employee_audit;

-- 启用触发器
ALTER TABLE employees ENABLE TRIGGER trg_employee_audit;

-- 所有触发器
ALTER TABLE employees ENABLE TRIGGER ALL;

-- 删除触发器
DROP TRIGGER IF EXISTS trg_employee_audit ON employees;
```

---

## 6. 游标

### 隐式游标

```sql
-- FOR循环自动管理
FOR v_rec IN SELECT id, name FROM employees WHERE dept_id = v_dept_id LOOP
    RAISE NOTICE '% - %', v_rec.id, v_rec.name;
END LOOP;
```

### 显式游标

```sql
DECLARE
    -- 声明游标
    CURSOR emp_cursor(p_dept_id INT) IS
        SELECT id, name, salary FROM employees
        WHERE dept_id = p_dept_id
        ORDER BY name;

    v_rec   RECORD;
BEGIN
    -- 打开
    OPEN emp_cursor(10);

    -- 获取
    FETCH emp_cursor INTO v_rec;

    WHILE FOUND LOOP
        RAISE NOTICE '% - % - %', v_rec.id, v_rec.name, v_rec.salary;
        FETCH emp_cursor INTO v_rec;
    END LOOP;

    -- 关闭
    CLOSE emp_cursor;
END;
```

### 游标属性

```sql
DECLARE
    CURSOR c_emp IS SELECT id, name FROM employees;
BEGIN
    OPEN c_emp;
    FETCH c_emp;

    -- %FOUND: 最后获取是否成功
    IF c_emp%FOUND THEN
        RAISE NOTICE '找到记录';
    END IF;

    -- %NOTFOUND: 是否无更多记录
    EXIT WHEN c_emp%NOTFOUND;

    -- %ISOPEN: 游标是否打开
    IF c_emp%ISOPEN THEN
        CLOSE c_emp;
    END IF;

    -- %ROWCOUNT: 已获取的行数
    RAISE NOTICE '已获取 % 行', c_emp%ROWCOUNT;
END;
```

### 动态游标

```sql
DECLARE
    v_sql     TEXT;
    v_refcur  REFCURSOR;
    v_rec     RECORD;
BEGIN
    v_sql := FORMAT(
        'SELECT id, name, salary FROM employees WHERE dept_id = %s ORDER BY name',
        p_dept_id
    );

    OPEN v_refcur FOR v_sql;

    LOOP
        FETCH v_refcur INTO v_rec;
        EXIT WHEN NOT FOUND;
        -- 处理 v_rec
    END LOOP;

    CLOSE v_refcur;
END;
```

### REF CURSOR参数传递

```sql
CREATE OR ALTER FUNCTION fetch_department(
    p_dept_id   INT,
    OUT out_cur REFCURSOR
)
AS
BEGIN
    out_cur := CURSOR FOR
        SELECT * FROM employees WHERE dept_id = p_dept_id;
    -- 注意：不自动打开，调用方负责FETCH和CLOSE
END;


-- 调用
BEGIN;
SELECT * FROM fetch_department(10, 'dept_cursor');
FETCH ALL IN dept_cursor;
COMMIT;
```

---

## 7. 包 (Package)

### 包规范

```sql
CREATE OR ALTER PACKAGE pkg_employee
AS
    -- 公共变量
    g_dept_id   INT := 1;

    -- 公共常量
    c_max_salary  DECIMAL(10, 2) := 1000000;

    -- 类型声明
    TYPE emp_record IS RECORD (
        id      INT,
        name    VARCHAR(100),
        salary  DECIMAL(10, 2)
    );

    TYPE emp_cursor_type IS REF CURSOR;

    -- 函数声明
    FUNCTION hire_employee(
        p_name    VARCHAR(100),
        p_dept    INT,
        p_salary  DECIMAL(10, 2)
    ) RETURNS INT;

    FUNCTION fire_employee(p_emp_id INT) RETURNS BOOLEAN;

    FUNCTION get_salary_stats(p_dept_id INT)
    RETURNS TABLE (avg_sal DECIMAL, max_sal DECIMAL, min_sal DECIMAL, emp_count INT);

    -- 过程声明
    PROCEDURE raise_salary(p_emp_id INT, p_rate DECIMAL);
    PROCEDURE transfer_employee(p_emp_id INT, p_new_dept INT);

    -- 初始化块
BEGIN
    -- 包首次加载时执行
    g_dept_id := 1;
    RAISE NOTICE 'Employee package initialized';
END pkg_employee;
```

### 包体

```sql
CREATE OR ALTER PACKAGE BODY pkg_employee
AS
    -- 私有变量
    v_log_count   INT := 0;

    -- 私有函数
    FUNCTION validate_salary(p_salary DECIMAL) RETURNS BOOLEAN
    AS
    BEGIN
        RETURN p_salary > 0 AND p_salary <= c_max_salary;
    END;

    -- 公开函数实现
    FUNCTION hire_employee(
        p_name    VARCHAR(100),
        p_dept    INT,
        p_salary  DECIMAL(10, 2)
    ) RETURNS INT
    AS
    DECLARE
        v_new_id  INT;
    BEGIN
        IF NOT validate_salary(p_salary) THEN
            RAISE EXCEPTION '薪资无效: %', p_salary;
        END IF;

        INSERT INTO employees (name, dept_id, salary, hire_date)
        VALUES (p_name, p_dept, p_salary, CURRENT_DATE)
        RETURNING id INTO v_new_id;

        v_log_count := v_log_count + 1;
        RETURN v_new_id;
    END;

    FUNCTION fire_employee(p_emp_id INT) RETURNS BOOLEAN
    AS
    BEGIN
        DELETE FROM employees WHERE id = p_emp_id;
        IF FOUND THEN
            v_log_count := v_log_count + 1;
            RETURN TRUE;
        END IF;
        RETURN FALSE;
    END;

    FUNCTION get_salary_stats(p_dept_id INT)
    RETURNS TABLE (avg_sal DECIMAL, max_sal DECIMAL, min_sal DECIMAL, emp_count INT)
    AS
    BEGIN
        RETURN QUERY
        SELECT
            avg(salary),
            max(salary),
            min(salary),
            count(*)::INT
        FROM employees
        WHERE dept_id = p_dept_id;
    END;

    PROCEDURE raise_salary(p_emp_id INT, p_rate DECIMAL)
    AS
    DECLARE
        v_current   DECIMAL(10, 2);
        v_new       DECIMAL(10, 2);
    BEGIN
        SELECT salary INTO v_current FROM employees WHERE id = p_emp_id;
        v_new := v_current * (1 + p_rate / 100);

        IF v_new > c_max_salary THEN
            RAISE WARNING '调整后薪资超过上限: %', v_new;
        END IF;

        UPDATE employees SET salary = v_new WHERE id = p_emp_id;
    END;

    PROCEDURE transfer_employee(p_emp_id INT, p_new_dept INT)
    AS
    BEGIN
        UPDATE employees SET dept_id = p_new_dept WHERE id = p_emp_id;
    END;

BEGIN
    -- 包体初始化
    v_log_count := 0;
END pkg_employee;
```

### 使用包

```sql
-- 调用包函数
SELECT pkg_employee.hire_employee('张三', 10, 15000);

-- 调用包过程
CALL pkg_employee.raise_salary(1, 10.0);

-- 访问包变量
SELECT pkg_employee.g_dept_id;

-- 删除包
DROP PACKAGE IF EXISTS pkg_employee;
```

---

## 8. 异常处理

### 内置异常

```sql
CREATE OR ALTER FUNCTION safe_divide(
    p_a   DECIMAL,
    p_b   DECIMAL
) RETURNS DECIMAL
AS
BEGIN
    RETURN p_a / p_b;
EXCEPTION
    WHEN division_by_zero THEN
        RAISE NOTICE '除数不能为零';
        RETURN NULL;
END;

```

### 常用内置异常

| 异常名 | SQLSTATE | 说明 |
|--------|----------|------|
| `division_by_zero` | 22012 | 除零 |
| `invalid_cursor_name` | 42601 | 无效游标名 |
| `invalid_cursor_state` | 24000 | 游标状态错误 |
| `invalid_grant_operator` | 0L013 | 无效授权 |
| `not_null_violation` | 23502 | 违反非空约束 |
| `unique_violation` | 23505 | 违反唯一约束 |
| `foreign_key_violation` | 23503 | 违反外键约束 |
| `check_violation` | 23514 | 违反检查约束 |
| `too_many_rows` | 21000 | SELECT INTO返回多行 |
| `no_data_found` | 02000 | 未找到数据 |
| `duplicate_cursor_name` | 42710 | 游标名重复 |
| `data_exception` | 22000 | 数据异常 |
| `others` | - | 所有其他异常 |

### 自定义异常

```sql
CREATE OR ALTER FUNCTION update_salary(
    p_emp_id   INT,
    p_new_sal  DECIMAL(10, 2)
) RETURNS VOID
AS
DECLARE
    -- 声明自定义异常
    salary_too_high     EXCEPTION;
    emp_not_found       EXCEPTION;
    v_old_sal           DECIMAL(10, 2);
    v_diff              DECIMAL(10, 2);
BEGIN
    SELECT salary INTO v_old_sal FROM employees WHERE id = p_emp_id;

    IF NOT FOUND THEN
        RAISE emp_not_found USING MESSAGE = '员工不存在: %', p_emp_id;
    END IF;

    v_diff := p_new_sal - v_old_sal;

    IF v_diff > 50000 THEN
        RAISE salary_too_high
            USING MESSAGE = '调薪幅度过大: %', v_diff,
                  HINT = '单次调薪不能超过50000';
    END IF;

    UPDATE employees SET salary = p_new_sal WHERE id = p_emp_id;
EXCEPTION
    WHEN emp_not_found THEN
        -- 重抛
        RAISE;
    WHEN salary_too_high THEN
        -- 记录后重抛
        INSERT INTO salary_log (emp_id, old_sal, new_sal, status)
        VALUES (p_emp_id, v_old_sal, p_new_sal, 'REJECTED');
        RAISE;
    WHEN OTHERS THEN
        -- 记录所有其他异常
        RAISE LOG '更新薪资失败 - 员工: %, 错误: %, 状态: %',
                  p_emp_id, SQLERRM, SQLSTATE;
        RAISE;
END;

```

### RAISE级别

```sql
-- NOTICE：发送到客户端
RAISE NOTICE '处理记录: %', v_count;

-- WARNING：警告级别
RAISE WARNING '数据可能不准确';

-- LOG：仅写入服务器日志
RAISE LOG '调试信息: %', v_value;

-- DEBUG：调试级别（需启用debug打印）
RAISE DEBUG '中间值: %', v_temp;

-- EXCEPTION：抛出异常
RAISE EXCEPTION '错误消息: %', detail;

-- 使用SQLSTATE
RAISE EXCEPTION USING
    MESSAGE = '自定义错误',
    ERRCODE = '22000',
    DETAIL = '详细错误信息',
    HINT = '建议的解决方案';

-- 使用RAISE_APPLICATION_ERROR（Oracle兼容）
RAISE_APPLICATION_ERROR(-20001, '应用错误消息');
```

### 诊断信息

```sql
EXCEPTION
    WHEN OTHERS THEN
        -- 异常消息
        RAISE LOG 'Error: %', SQLERRM;

        -- 错误码
        RAISE LOG 'SQLSTATE: %', SQLSTATE;

        -- 错误码（数值）
        RAISE LOG 'SQLCODE: %', SQLCODE;

        -- 堆栈跟踪
        GET STACKED DIAGNOSTICS v_msg := MESSAGE_TEXT,
                                v_state := RETURNED_SQLSTATE,
                                v_context := PG_EXCEPTION_CONTEXT;

        RAISE LOG 'Message: %, State: %, Context: %', v_msg, v_state, v_context;
END;
```

---

## 9. 动态SQL

### EXECUTE基本用法

```sql
DECLARE
    v_table   TEXT := 'employees';
    v_sql     TEXT;
    v_count   INT;
BEGIN
    -- 基本动态SQL
    v_sql := FORMAT('SELECT count(*) FROM %I', v_table);
    EXECUTE v_sql INTO v_count;

    -- 带参数
    v_sql := 'SELECT name FROM employees WHERE id = $1';
    EXECUTE v_sql USING p_emp_id;

    -- 带多参数
    v_sql := 'UPDATE employees SET salary = $1 WHERE dept_id = $2';
    EXECUTE v_sql USING p_salary, p_dept_id;
END;
```

### format()函数

```sql
-- %s - 字符串替换（需手动处理引号）
-- %I - 标识符（自动加引号）
-- %L - 字面量（自动加引号并转义）

v_sql := FORMAT(
    'INSERT INTO %I (%I, %I, %I) VALUES ($1, $2, $3)',
    v_table_name, col1, col2, col3
);
EXECUTE v_sql USING val1, val2, val3;

-- 安全处理标识符
v_sql := FORMAT('SELECT * FROM %I WHERE %I = %L', p_table, p_column, p_value);
EXECUTE v_sql;
```

### quote_ident / quote_literal

```sql
-- 手动引用标识符
v_sql := 'SELECT * FROM ' || quote_ident(p_table)
       || ' WHERE ' || quote_ident(p_column)
       || ' = ' || quote_literal(p_value);
EXECUTE v_sql;
```

### 动态查询返回结果

```sql
CREATE OR ALTER FUNCTION dynamic_query(
    p_table   TEXT,
    p_column  TEXT,
    p_value   TEXT
) RETURNS SETOF RECORD
AS
DECLARE
    v_sql     TEXT;
    v_result  RECORD;
BEGIN
    v_sql := FORMAT(
        'SELECT * FROM %I WHERE %I = %L',
        p_table, p_column, p_value
    );

    FOR v_result IN EXECUTE v_sql LOOP
        RETURN NEXT v_result;
    END LOOP;
END;

```

---

## 10. 日志与调试

### 日志记录

```sql
-- 创建日志表
CREATE TABLE plsql_log (
    id          BIGSERIAL PRIMARY KEY,
    log_time    TIMESTAMP DEFAULT NOW(),
    level       VARCHAR(10),
    function    VARCHAR(200),
    message     TEXT,
    context     TEXT
);

-- 日志函数
CREATE OR ALTER FUNCTION log_message(
    p_level     VARCHAR(10),
    p_msg       TEXT,
    p_func      VARCHAR(200) DEFAULT NULL
) RETURNS VOID
AS
BEGIN
    INSERT INTO plsql_log (level, function, message, context)
    VALUES (
        p_level,
        COALESCE(p_func, CURRENT_FUNCTION),
        p_msg,
        (SELECT PG_EXCEPTION_CONTEXT)
    );
END;

```

### 调试技巧

```sql
-- 启用调试输出
SET plpgsql.extra_errors TO ON;

-- 在过程中使用RAISE DEBUG
RAISE DEBUG '变量值: %, %, %', v_a, v_b, v_c;

-- 查看执行计划
EXPLAIN ANALYZE SELECT calc_bonus(15000, 'A');
```

---

## 11. 最佳实践

### 命名规范

```
前缀约定：
  v_    - 局部变量
  p_    - 参数
  c_    - 常量
  g_    - 全局变量（包级）
  r_    - 记录变量
  cur_  - 游标

对象命名：
  fn_     - 函数
  proc_   - 存储过程
  trg_    - 触发器函数
  pkg_    - 包
  view_   - 视图
  idx_    - 索引
```

### 性能建议

1. **避免在循环中查询**：批量操作替代逐行处理
2. **使用RETURN QUERY**：直接返回查询结果而非逐行写入
3. **限制游标FETCH**：一次FETCH适量记录，避免内存溢出
4. **使用FOR UPDATE**：防止并发修改导致的数据不一致
5. **避免SELECT ***：只选择需要的列
6. **批量INSERT**：使用INSERT ... SELECT替代循环INSERT

### 安全建议

1. **使用USING参数**：防止SQL注入
2. **使用quote_ident**：处理动态表名/列名
3. **SECURITY DEFINER慎用**：明确权限边界
4. **最小权限原则**：函数执行者仅有必要权限

---

## 12. Oracle兼容性说明

### 语法差异

| Oracle语法 | KingbaseES语法 |
|-----------|---------------|
| `CREATE OR ALTER PROCEDURE` | 同（支持） |
| `CREATE OR ALTER FUNCTION` | 同（支持） |
| `PRAGMA AUTONOMOUS_TRANSACTION` | 使用`BEGIN; ... COMMIT; END;`子事务 |
| `DBMS_OUTPUT.PUT_LINE` | `RAISE NOTICE` |
| `SQLCODE` / `SQLERRM` | 同（支持） |
| `RAISE_APPLICATION_ERROR` | 同（支持） |
| `TYPE ... IS TABLE OF` | 使用`RETURNS TABLE`或数组 |
| `PIPELINED`函数 | 使用`RETURNS SETOF` |
| `SYS_REFCURSOR` | 使用`REFCURSOR` |
| `COMMIT`在函数中 | KES函数中不允许COMMIT/ROLLBACK |

### Oracle风格包

```sql
-- Oracle风格（兼容模式支持）
CREATE OR ALTER PACKAGE pkg_utils
IS
    PROCEDURE log_msg(p_msg VARCHAR2);
    FUNCTION fmt_date(p_date DATE) RETURN VARCHAR2;
END;
/

CREATE OR ALTER PACKAGE BODY pkg_utils
IS
    PROCEDURE log_msg(p_msg VARCHAR2)
    IS
    BEGIN
        RAISE NOTICE '%', p_msg;
    END;

    FUNCTION fmt_date(p_date DATE) RETURN VARCHAR2
    IS
    BEGIN
        RETURN TO_CHAR(p_date, 'YYYY-MM-DD');
    END;
END;
/
```
