---
name: mysql-schema-best-practice-generator
description: "基于MySQL 8.0 的数据库建表最佳实践规范生成与审校，输出规范化DDL、索引策略与校验清单。"
---

用途：根据用户的业务表需求，生成符合 MySQL 8.0 最佳实践的建表DDL、索引与约束策略、字符集/排序规则、安全与性能设置，并提供审校清单与风险提示。支持对现有DDL进行审查与修正建议。

输入格式：
- 模式A（生成）：
  {
    "mode": "generate",
    "db_name": "业务库名",
    "tables": [
      {
        "table": "表名",
        "comment": "表用途简述",
        "columns": [
          {"name": "列名", "type": "业务数据类型或范围", "nullable": true/false, "default": "默认值或null", "comment": "说明", "enum": [可选枚举], "length": 可选长度, "precision": 可选精度, "scale": 可选小数位, "pk": true/false, "auto_increment": true/false, "unique": true/false }
        ],
        "unique_keys": [["列1","列2"], ...],
        "indexes": [{"name":"idx_name","columns":["列1","列2"], "type": "btree", "comment": "用途"}],
        "foreign_keys": [{"columns":["本表列"], "ref_table":"引用表", "ref_columns":["主表列"], "on_update":"RESTRICT|CASCADE|SET NULL", "on_delete":"RESTRICT|CASCADE|SET NULL"}],
        "partition": {"type": "RANGE|HASH|LIST", "expr": "表达式", "partitions": 4},
        "engine": "InnoDB",
        "extras": {"soft_delete": true/false, "tenant_id": true/false}
      }
    ],
    "naming": {"table_prefix": "可选", "snake_case": true, "lowercase": true},
    "collation": {"charset": "utf8mb4", "collate": "utf8mb4_0900_ai_ci"}
  }
- 模式B（审查）：
  {
    "mode": "review",
    "ddl": "原始DDL字符串",
    "context": {"workload": "OLTP|OLAP|混合", "data_size": "预计规模", "qps": "峰值QPS"}
  }

输出格式：
- 对于 generate：
  {
    "ddl": "可直接执行的DDL(包含CREATE DATABASE/CREATE TABLE/索引/约束/注释)",
    "checklist": ["规范检查项..."],
    "rationale": "关键设计取舍说明",
    "migration_notes": ["上线与回滚建议"],
    "risk_warnings": ["潜在风险"]
  }
- 对于 review：
  {
    "issues": [{"level":"ERROR|WARN|INFO","item":"问题点","detail":"说明","fix":"修复建议","example":"示例SQL"}],
    "fixed_ddl": "修正后的DDL（若可自动修复）",
    "checklist": ["核对清单"],
    "risk_warnings": ["风险"]
  }

实施步骤与逻辑：
1) 预设全局最佳实践（MySQL 8.0）：
   - 存储引擎：默认 InnoDB；禁用 MyISAM。
   - 字符集/排序规则：utf8mb4 与 utf8mb4_0900_ai_ci（或按业务要求使用 utf8mb4_0900_bin 用于精确比较/大小写敏感场景）。
   - 时区：以UTC存储，业务层转换；时间列使用 TIMESTAMP（需要自动时区转换）或 DATETIME（仅存储时间，不涉时区），统一NOT NULL并设置默认值策略。
   - 主键：推荐单列无业务含义的 BIGINT UNSIGNED 自增或 UUID（prefer UUIDv7，通过BINARY(16)存储以减少索引膨胀）。所有表必须有主键。
   - 列类型选择：
     - 文本：VARCHAR(N) 优先，长文本用 TEXT（避免在频繁索引字段使用TEXT/JSON）。
     - 金额：DECIMAL(p,s)，避免FLOAT/DOUBLE导致精度误差。
     - 状态：TINYINT/SMALLINT 或 ENUM（升级成本考虑，倾向TINYINT 配字典表）。
     - JSON：仅在需灵活半结构化数据时使用，并辅以生成列+函数索引。
   - 约束：NOT NULL 明确化；默认值显式声明；唯一约束替代唯一索引（语义更明确）。
   - 外键：强一致业务可用外键；高并发或分库分表场景可用应用侧约束并保留命名规范的逻辑外键列与索引。
   - 索引：覆盖常用查询的条件、排序、连接列；遵循最左前缀原则；谨慎为低选择性列建索引；避免过多索引影响写性能。
   - 命名规范：
     - 数据库/表/列/索引/约束统一小写snake_case。
     - 主键pk_表名，唯一键uk_表名_列1_列2，普通索引idx_表名_列1_列2，外键fk_表名_列。
   - 表选项：ROW_FORMAT=DYNAMIC；行压缩按需；innodb_file_per_table=ON（依赖实例级）。
   - 审计列：created_at、updated_at、created_by、updated_by；可选 deleted_at 实现软删除（并建立索引）。
   - 分区：仅在明确数据裁剪或查询加速收益时使用，避免过度分区；主键包含分区键。

2) 模式A生成流程：
   a. 规范化输入：补全缺失的 engine、charset、collation、行格式、审计列与主键策略。
   b. 字段映射与类型选型：根据业务类型/范围推导合适的 MySQL 类型与长度；金额映射为DECIMAL；布尔映射为TINYINT(1)。
   c. 主键策略：优先BIGINT UNSIGNED AUTO_INCREMENT；如用户指定UUID则使用 BINARY(16) 并提供插入示例（通过UUID_TO_BIN/ BIN_TO_UUID，v7优先）。
   d. 约束与默认值：所有必要列NOT NULL，显式默认值；时间列默认CURRENT_TIMESTAMP并配置ON UPDATE。
   e. 索引设计：
      - 根据查询场景（若提供）设计复合索引；
      - 为外键列、唯一约束列建立索引；
      - 对软删除/多租户列（deleted_at, tenant_id）建立前缀索引组合。
   f. 外键与参照完整性：根据输入生成外键或给出应用侧约束建议。
   g. 分区检查：若定义分区，验证分区键包含在主键/唯一键前缀内，并给出示例。
   h. DDL 生成：包含 CREATE DATABASE IF NOT EXISTS、每表 CREATE TABLE、COMMENT、索引/约束、必要的触发器或生成列语句；统一使用 ENGINE=InnoDB, DEFAULT CHARSET, COLLATE, ROW_FORMAT=DYNAMIC。
   i. 清单与说明：输出检查清单、设计原因、上线/回滚建议与风险提示。

3) 模式B审查流程：
   a. 解析DDL：检查是否使用InnoDB、字符集/排序、是否存在隐式NULL、缺失主键、未命名约束/索引。
   b. 类型与长度：识别过大类型（如VARCHAR(1000)+频繁索引）、不合理FLOAT金额、TEXT/JSON滥用、低选择性列索引。
   c. 时间与时区：DATETIME/TIMESTAMP混用问题、默认值不一致、ON UPDATE 缺失。
   d. 索引策略：重复/冗余索引、未覆盖查询关键列、复合索引顺序不当、唯一约束缺失。
   e. 外键与分区：外键命名/索引缺失、分区键错误或与主键不一致。
   f. 命名规范：是否小写snake_case、索引/约束命名是否符合前缀规范。
   g. 安全与性能：未设置行格式、缺少审计列、过多触发器、未设置合适的默认值、潜在锁升级风险。
   h. 给出修复建议与可自动修复的 fixed_ddl。

4) 错误处理：
   - 若输入缺少关键字段（如表名/列定义），返回 ERROR 并附示例输入。
   - 解析DDL失败时，提示编码或语法问题，要求提供更完整DDL或去除厂商特性。
   - 若要求使用不受支持的引擎/排序规则，给出替代方案与风险说明。

MCP工具使用：本Skill以静态规范生成与审校为主，不依赖外部MCP工具；若运行环境提供SQL格式化MCP工具（例如 sql-formatter），可选执行：
   1) 检查是否存在名为 sql-formatter 的MCP：调用 tools.list 或 capability 查询；
   2) 若未安装且提供了mcpServers配置，则按照配置添加到本地mcpServers并重载；
   3) 安装后调用 format_sql 工具对输出DDL进行格式化；
   4) 工具不可用时，回退到内置简易格式化，不影响主流程。

返回要求：严格使用上述输出格式，DDL应可在 MySQL 8.0+ 执行，避免使用已废弃语法。