# VERIFICATION_PROTOCOL.md — human-ai-closed-loop

## 验证目标

确保人机闭环 Skill 真正实现双向进化（而非单向 AI 输出），置信度 ≥ 95%。

## 五步自验证流程

### Step 1 — 清单结构验证（已知/未知分离）
- [ ] `generate_checklist()` 输出是否包含三类条目：`verified_facts` / `hypotheses` / `blind_spots`？
- [ ] 假设是否明确标注「待证伪」而非「已确认」？
- **通过标准**：三类分离覆盖率 100%，无混淆条目

### Step 2 — 闭环记忆持久化
- [ ] 每轮 `inject()` 调用是否写入 `loop_log/session_{id}_round_{n}.json`？
- [ ] 是否可从日志恢复任意一轮的状态？
- **通过标准**：所有轮次可溯源，数据完整率 100%

### Step 3 — 四向碰撞 in 清单生成
- [ ] `generate_checklist()` 是否从四个视角生成条目（正/反/侧/整体）？
- [ ] 最终清单是否合并四个视角并去重？
- **通过标准**：四向覆盖率 100%，合并后无重复条目

### Step 4 — 人类输入真正影响输出
- [ ] `inject(falsified=...)` 后，相关假设是否从下一轮清单中移除或修正？
- [ ] `inject(imagination=...)` 后，新思路是否出现在 `synthesize()` 输出中？
- **通过标准**：注入后输出变化率 ≥ 40%（证明闭环有效）

### Step 5 — 置信度动态更新 + 红线
- [ ] 每轮 `synthesize()` 的置信度是否随人类反馈动态更新（而非固定值）？
- [ ] 是否拦截将用户私有数据（注入内容）发往外部服务？
- **通过标准**：置信度动态性验证通过；数据外泄拦截率 100%

## 验证结论模板

```
验证日期: YYYY-MM-DD
Step 1 清单结构:        PASS / FAIL  (置信度: XX%)
Step 2 闭环记忆写入:    PASS / FAIL  (置信度: XX%)
Step 3 四向碰撞:        PASS / FAIL  (置信度: XX%)
Step 4 人类输入影响:    PASS / FAIL  (置信度: XX%)
Step 5 置信度动态+红线: PASS / FAIL  (置信度: XX%)
综合置信度: XX%  →  [APPROVED / REJECTED]
```
