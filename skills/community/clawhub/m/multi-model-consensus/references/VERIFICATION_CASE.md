# 多模型决策委员会 — 端到端验证用例

## 验证目标

验证多模型决策委员会 skill 可完整执行多轮收敛流程，状态机正确流转，最终输出 6 段式报告。

---

## 验证环境

- **本地模型库**：通过 `openclaw models list` 动态获取可用模型列表
- **决策轮数**：3轮（默认）
- **通过阈值**：≥90%
- **测试任务**：方案A vs 方案B 简单二选一决策

---

## 验证步骤

### Step 1：阶段门控审查（6项检查）

执行前验证所有文件完整性和版本一致性：

| # | 检查项 | 通过标准 | 验证命令 |
|:---:|:---|:---|:---|
| 1 | Schema 有效性 | `references/SCHEMA.md` 存在且包含 state 字段 | `cat SCHEMA.md \| grep state \| head -1` |
| 2 | 状态机规范 | `references/STATE_MACHINE.md` 包含 6 状态（IDLE/ROUND_0/ROUND_1/ROUND_2/ROUND_3/COMPLETE）+ 收敛判定规则 | `grep -c "IDLE\\|ROUND_0\\|ROUND_1\\|ROUND_2\\|ROUND_3\\|COMPLETE" STATE_MACHINE.md` |
| 3 | 报告模板 | `references/OUTPUT_TEMPLATE.md` 含第1/2/3轮prompt模板 + 6段式报告 | `grep -c "投票记录\\|汇总说明\\|执行方案\\|未决清单\\|结论摘要\\|风险提示" OUTPUT_TEMPLATE.md` |
| 4 | 执行示例 | `references/EXECUTION_EXAMPLES.md` 含每轮操作步骤 | `grep -c "Step [1-6]" EXECUTION_EXAMPLES.md` |
| 5 | 端到端可执行 | 本验证用例覆盖完整流程 | 对照 Step 2-5 逐一验证 |
| 6 | 版本一致性 | 所有文件中 version 字段一致（V1.5.0） | `grep -r "V1\\.5\\.0" . \| grep -v Binary` |

---

### Step 2：动态模型扫描验证

```python
# 验证动态扫描逻辑
import subprocess

result = subprocess.run(["openclaw", "models", "list"], capture_output=True, text=True)
# 解析输出获取模型列表
models = []
for line in result.stdout.strip().split("\n")[1:]:  # 跳过表头
    parts = line.split()
    if parts:
        models.append({
            "id": parts[0],
            "name": parts[0]
        })

assert len(models) >= 3, "本地模型少于3个，无法组成委员会"
print(f"✅ 扫描到 {len(models)} 个模型: {[m['name'] for m in models]}")
```

---

### Step 3：状态机流转验证

```
[IDLE] → "确认配置" → [ROUND_1] → [ROUND_2] → ([ROUND_3]) → [COMPLETE] → [IDLE]
```

| 状态 | 预期动作 | 验证方法 |
|:---|:---|:---|
| IDLE | 接收任务，等待用户确认 | 初始状态检查 |
| ROUND_1 | 并行 spawn N 个子会话，各委员独立评审 | 进程数 = 委员数 |
| ROUND_2 | 汇总分歧点，二次表态，判断收敛性 | 分歧收敛则跳过ROUND_3 |
| ROUND_3 | 深层分歧最终表态（仅 ROUND_2 未收敛时触发） | 投票矩阵输出 |
| COMPLETE | 输出6段式共识报告 | 报告文件生成 |
| IDLE | 报告已输出，状态重置 | 状态文件重置 |

---

### Step 4：收敛判定规则验证

| 场景 | 条件 | 预期行为 |
|:---|:---|:---|
| 收敛 | ROUND_2 所有委员推荐顺序一致 | 跳过 ROUND_3，直接 COMPLETE |
| 分歧 | ROUND_2 存在推荐顺序冲突 | 触发 ROUND_3 |

---

### Step 5：6段式报告结构验证

| 章节 | 必含内容 |
|:---|:---|
| 投票记录 | 量化评分矩阵（每委员对方案A/B的评分） |
| 汇总说明 | 各委员核心论点，注明大模型提供商 |
| 执行方案 | 结论版 + 详细版 |
| 未决清单 | 待确认事项 + 负责人 |
| 结论摘要 | 一句话裁定 + 置信度百分比 |
| 风险提示 | 主要风险 + 缓解建议 |

---

### Step 6：版本一致性校验

验证所有文件版本号统一为 V1.2.1：

| 文件 | 预期版本 | 校验 |
|:---|:---:|:---|
| `_meta.json` | `1.2.1` | ✅ |
| `SKILL.md` (frontmatter) | `1.2.1` | ✅ |
| `docs/USER_GUIDE.md` | `V1.2.1` | ✅ |
| `references/SCHEMA.md` | `v1.0.0`（锁定不变） | ✅ |

---

## 验证通过标准

全部 6 项阶段门控审查通过，且：

1. ✅ 动态模型扫描返回 ≥3 个可用模型
2. ✅ 状态机正确流转（收敛时跳过 ROUND_3）
3. ✅ 6段式报告结构完整
4. ✅ 所有文件版本号一致（V1.2.1）
5. ✅ 状态文件每轮更新，无跳过

---

## 验证记录

| 验证日期 | 验证者 | 结果 | 备注 |
|:---|:---|:---|:---|
| 2026-04-24 | Zeekr0808 | ⬜ 待验证 | 首次完整验证 |
| 2026-04-25 | Zeekr0808 | ✅ 通过 | V1.2.1 版本更新后复验 |
