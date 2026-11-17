# 测试骨架模板规范（v1.0）

对应 PRD v2 §3.2 P0-02（V-01~V-04）。本规范定义 impl-guide 如何将"一致性测试要求"升级为**可执行测试骨架**，以及 audit-trace 如何**核对测试执行结果**，用真实运行结果替代模型主观判定。

## 1. 目标

- **V-01 测试骨架生成**：impl-guide 输出语言无关的测试骨架（断言 + 用例框架，不含业务实现），可按框架适配表落为可运行文件
- **V-02 测试运行与结果采集**：audit-trace 读取标准化测试结果（通过/失败、覆盖率），作为审计判定依据
- **V-03 证据自动核对**：任务清单"证据要求"支持"测试结果文件路径"类型，audit-trace 自动核对
- **V-04 未执行测试降级**：测试未执行/无法执行时，相关维度标注"未验证"，交付状态不得为"可交付"

## 2. 映射规则：Spec 元素 → 测试用例

| Spec 元素 | 测试映射 | 示例 |
|----------|---------|------|
| 验收标准 AC（Given/When/Then） | 每个 AC 至少 1 个测试用例；多分支 AC 用参数化 | AC-01 → `test_ac01_login_success` |
| API 定义（输入/输出/状态码） | API 测试用例（请求构造 + 响应断言） | `POST /register` → 断言 201 + 响应体 |
| 性能约束（C-XX） | 基准测试（阈值/超时断言） | 响应 < 200ms → `assert elapsed < 0.2` |
| 安全约束（S-XX） | 安全检查用例 | 密码加密 → 断言存储值 ≠ 明文 |
| 数据完整性（DM-XX） | 唯一性/约束验证 | 邮箱唯一 → 重复插入断言失败 |

## 3. 测试骨架通用结构（语言无关）

每个测试骨架文件包含：

1. **文件头注释**：来源映射（Spec 版本、关联 AC ID 列表）、用途说明
2. **测试夹具（fixtures）**：从 Given 部分派生测试数据准备
3. **测试用例**（每个 AC 至少一个）：
   - Arrange（Given）— 前置条件准备
   - Act（When）— 执行动作
   - Assert（Then）— 断言
4. **边界用例（可选）**：异常路径、边界值（从已确认的模糊项答案派生）

骨架只生成断言与用例框架，**不编写业务逻辑实现**（桩函数体留空或抛 NotImplementedError/占位）。

## 4. 命名规范（AC 可回溯）

- 测试文件：按目标语言惯例命名（`test_<模块>.py`、`<模块>.test.ts`、`<模块>Test.java`）
- 测试用例：`test_ac{AC-ID}_{场景名}`，保证 AC ID 可回溯（如 `test_ac01_login_success`）
- 无 AC 来源的测试（API/性能/安全）用 `test_{类型}{编号}_{场景}`（如 `test_perf01_response_time`）

## 5. 框架适配表（语言无关规则 → 具体模板）

| 语言/框架 | 用例模板要点 | 断言风格 |
|----------|-------------|---------|
| Python pytest | `def test_ac01_xxx():` + fixture | `assert 实际 == 预期` / `pytest.raises` |
| JS/TS Vitest/Jest | `test('ac01 xxx', () => {...})` | `expect(实际).toBe(预期)` |
| Java JUnit 5 | `@Test void testAc01Xxx()` | `Assertions.assertEquals` |
| Go testing | `func TestAc01Xxx(t *testing.T)` | `t.Errorf` / `require` |
| Rust | `#[test] fn test_ac01_xxx()` | `assert_eq!` / `assert!` |

生成规则：impl-guide 检测架构设计中的技术选型 → 选择对应框架 → 输出该框架语法的骨架；技术选型未知时输出语言无关伪代码并在头部注明"需按目标框架适配"。

## 6. 测试结果输出格式（audit-trace 核对契约）

测试运行后必须产出标准化结果记录，两种格式任选其一：

### 格式 A：JSON（推荐）

```json
{
  "suite": "tests/test_auth.py",
  "source": { "spec": "PRD-2026-001", "ac_ids": ["AC-01", "AC-02"] },
  "run_at": "2026-08-09T10:00:00+08:00",
  "result": { "passed": 5, "failed": 0, "skipped": 0, "coverage": 87.5 },
  "cases": [
    { "id": "test_ac01_login_success", "status": "passed", "duration_ms": 12 },
    { "id": "test_ac01_login_wrong_pwd", "status": "passed", "duration_ms": 8 }
  ]
}
```

### 格式 B：Markdown 报告

```markdown
## 测试结果报告
- 套件：tests/test_auth.py
- 来源：Spec PRD-2026-001，AC-01~AC-02
- 结果：5 通过 / 0 失败 / 0 跳过
- 覆盖率：87.5%
| 用例 | 状态 | 关联 AC | 耗时 |
|------|------|---------|------|
| test_ac01_login_success | ✅ | AC-01 | 12ms |
```

**契约要求**：`cases[].status` 取值限 `passed` / `failed` / `skipped`；`source.ac_ids` 必须与骨架头注释一致；覆盖率字段可缺省（标注 `null`），缺省时审计按"无覆盖率数据"处理。

## 7. audit-trace 核对规则（V-02/V-03/V-04）

**核对流程**：

1. 按任务清单的证据要求字段定位测试结果文件（路径或对话中提供）
2. 解析结果记录，按 `source.ac_ids` 关联到 Spec 功能点
3. 逐 AC 判定：

| 测试结果 | 判定 | 说明 |
|---------|------|------|
| 该 AC 全部用例 passed | ✅ 测试验证通过 | 替代纯代码阅读判定 |
| 存在 failed 用例 | ❌ 存在失败用例 | 失败清单列入报告 |
| 无结果文件/未执行 | ⚠️ 未验证（V-04 降级） | 不默认判定达标 |

**降级规则（V-04）**：

- 任一 P0 功能点"未验证"→ 交付状态不得为"可交付"（最高 ⚠️ 有条件交付）
- "未验证"条目必须在报告中显式标注，不得与"✅ 测试验证通过"混同
- 覆盖率 < 80% 时在报告中提示"覆盖率不足，建议补充测试"

## 8. 集成位置

| 环节 | 落点 |
|------|------|
| 生成测试骨架 | impl-guide 步骤 D（升级：一致性测试要求 → 测试要求 + 可执行骨架） |
| 证据要求支持结果文件 | task-planner 证据要求字段（新增"测试结果文件路径"类型） |
| 结果核对与降级 | audit-trace 新增"测试执行结果核对"维度（V-02） |

## 9. 验收标准（对应 P0-02）

- Given 一份含 N 条一致性测试要求的实现指导，When 执行 impl-guide，Then 输出 N 条可运行的测试骨架（含断言与用例框架）
- Given 测试骨架已运行且全部通过，When 执行 audit-trace，Then 对应功能点判定为"✅ 测试验证通过"
- Given 测试未运行，When 执行 audit-trace，Then 相关条目标注"未验证"且交付状态不得为"可交付"
