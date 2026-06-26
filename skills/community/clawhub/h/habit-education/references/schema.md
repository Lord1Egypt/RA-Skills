# 数据库 Schema 参考

## habits（习惯定义表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 序号 |
| `name` | TEXT | UNIQUE NOT NULL | 习惯名称（唯一值） |
| `type` | TEXT | NOT NULL CHECK(type IN ('good', 'bad')) | 习惯类型 |
| `created_by` | TEXT | NULL | 建立人（如"父亲"、"母亲"等） |
| `cause` | TEXT | NULL | 产生原因（仅坏习惯） |
| `status` | TEXT | DEFAULT 'active' CHECK(status IN ('active', 'archived')) | 状态 |
| `created_at` | TEXT | NOT NULL | 创建时间（ISO 8601） |
| `archived_at` | TEXT | NULL | 归档时间 |
| `subject` | TEXT | NULL | 习惯主体（孩子名字） |
| `memory_level` | TEXT | CHECK(memory_level IN ('短期习惯', '长期习惯', '终身习惯')) | 记忆等级 |
| `intrinsic_motivation` | INTEGER | DEFAULT 0 | 是否内驱力相关（1=是，0=否）。判断标准：孩子是否自发发起、是否有真实兴趣驱动、是否不需要外部监督即可完成 |

## intervention_records（干预与打卡记录表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 记录序号 |
| `habit_id` | INTEGER | NOT NULL REFERENCES habits(id) | 对应习惯序号 |
| `event_time` | TEXT | NOT NULL | 行为实际发生时间（YYYY-MM-DD HH:MM:SS） |
| `status_description` | TEXT | NOT NULL | 当时状态描述 |
| `action_taken` | TEXT | NOT NULL | 采取的处理方式或打卡动作 |
| `result` | TEXT | NOT NULL CHECK(result IN ('improved', 'worsened', 'unchanged', 'maintained', 'failed')) | 效果 |
| `handled_by` | TEXT | NOT NULL | 执行干预的人 |
| `notes` | TEXT | NULL | 备注 |
| `recorded_at` | TEXT | NOT NULL | 系统录入时间（自动生成） |

## archived_habits_summary（已归档习惯总结表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 归档记录序号 |
| `habit_id` | INTEGER | NOT NULL UNIQUE REFERENCES habits(id) | 原习惯序号 |
| `original_type` | TEXT | NOT NULL CHECK(original_type IN ('good', 'bad')) | 原类型 |
| `archived_at` | TEXT | NOT NULL | 归档时间 |
| `days_tracked` | INTEGER | NOT NULL | 累计追踪天数 |
| `final_success_rate` | REAL | NOT NULL | 最终成功率（百分比） |
| `summary` | TEXT | NULL | 总结（好习惯：养成经验；坏习惯：纠正经验） |
| `notes` | TEXT | NULL | 原始备注（家长描述原文） |
| `subject` | TEXT | NULL | 习惯主体 |
| `memory_level` | TEXT | CHECK(memory_level IN ('短期习惯', '长期习惯', '终身习惯')) | 记忆等级 |

## education_contributions（教育付出记录表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 付出记录序号 |
| `contributor` | TEXT | NOT NULL | 付出者（如"父亲"、"母亲"等） |
| `category` | TEXT | NOT NULL | 类别 |
| `description` | TEXT | NOT NULL | 具体描述 |
| `effort_level` | TEXT | CHECK(effort_level IN ('low', 'medium', 'high')) | 投入程度 |
| `happened_at` | TEXT | NOT NULL | 发生时间 |
| `notes` | TEXT | NULL | 备注 |
| `created_at` | TEXT | NOT NULL | 记录创建时间 |

### 常用 category 类别

- `习惯干预` — 直接干预孩子习惯的行为
- `思想教育` — 讲述道理、心法
- `习惯养成引导` — 引导孩子建立习惯
- `教育基础设施` — 搭建平台、工具
- `生涯规划` — 未来规划类教育
- `内容管控` — 内容审查与管控
- `金融教育` — 财商相关
- `兴趣引导` — 引导兴趣发展
- `健康土壤提供` — 提供健康环境、优质内容、情感支持（内驱力培育的核心投入）
- `其他` — 不属于以上类别

### 常用 effort_level

- `low` — 低投入
- `medium` — 中等投入
- `high` — 高投入
