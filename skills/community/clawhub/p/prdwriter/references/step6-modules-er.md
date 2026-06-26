# Step 6 — 功能模块 + ER 模型 + 字段

## 6.1 ER 模型（吸收自 create-prd ch10 三步法）🆕

先于功能模块。从用户故事和状态机中提取实体：

**三步法**：
1. **识别实体**：流程中的核心名词（如 薪酬模板、工资单、员工、岗级）
2. **定义属性**：每个实体的字段
3. **定义关系**：1:1 / 1:N / N:N，标注关系名

输出 Mermaid `erDiagram`：
```
erDiagram
    SALARY_TEMPLATE ||--o{ PAY_SLIP : 适用于
    EMPLOYEE ||--o{ PAY_SLIP : 拥有
    EMPLOYEE }o--|| GRADE : 属于
    GRADE ||--o| SALARY_TEMPLATE : 启用模板
    SALARY_TEMPLATE { string id PK; string name; enum status; }
    PAY_SLIP { string id PK; string month; number actualAmount; enum status; }
```

→ `03-er-model.md`

## 6.2 功能模块（三层结构）

读取 `03.5-field-decisions.md` 用户决策，生成：

```
## 模块 MX: <模块名>
**关联用户故事**: US-XXX
**关联实体**: 引用 ER 模型中的实体名

### 操作节点 MX.Y: <操作名>
- **角色**: ...
- **触发**: 主动操作 / 系统触发 / 定时
- **前置条件**: ...
- **字段**:
  | 字段名 | 类型 | 必填 | 约束 | 关联实体 |
  |---|---|---|---|---|
- **后置结果**: ...（含状态机迁移）
```

字段类型限定: string/number/bool/enum/date/datetime/array/object/file/reference

→ `04-modules.md`，**STOP** 等用户确认。
