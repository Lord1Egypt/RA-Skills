# plan-generator — 训练计划生成

## 触发场景
- 用户要求训练计划："帮我排计划""下周练什么""调整训练计划""给我设计训练"
- App数据报告末尾要求JSON输出（含 "Output ONLY valid JSON"）
- 主skill分流到此子skill

## 操作规范

### 1. 需求分析（如用户信息不完整）
确认以下要素，缺什么问什么（每次不超过2-3个问题）：
- 训练经验（新手<6月 / 进阶6-24月 / 高阶>24月）
- 训练目标（增肌 / 减脂 / 力量 / 塑形）
- 可用器械（哑铃 / 杠铃 / 器械 / 徒手 / 混合）
- 每周训练天数（3-6天）
- 伤病或限制条件

### 2. 训练模式选择（经验 × 频率矩阵）

| 经验 | 3天/周 | 4天/周 | 5-6天/周 |
|------|--------|--------|----------|
| 新手 | 全身训练 | 上下分化 | — |
| 进阶 | PPL | 上下分化 | PPL双循环 |
| 高阶 | PPL | PPL | PPL/分化定制 |

选择原则：器械不足时优先全身或上下分化；时间充裕且器械齐全可考虑更高频分化。

### 3. 动作选择（数据库驱动 — 强制工具调用）
从 free-exercise-db 选动作，**禁止凭记忆编造动作名**。**每次生成计划都必须实际调用数据库查询脚本**，不允许仅凭记忆或App报告中的动作名直接使用。

**强制流程（不可跳过）：**
1. 先用 `--name` 模式模糊匹配候选动作
2. 如果匹配结果为空或名称不完全一致，必须用 `--name` 换关键词重查
3. 确认精确匹配后，使用查询结果中的精确 `name` 字段作为 exerciseName
4. 计划中**所有**动作名都必须经过此流程

```bash
# 脚本路径（注意不在scripts/根目录，而在skill目录下）
python skills/kaiji-fitness-coach/scripts/query_exercises.py --name "候选动作名" --format json
# 按肌群+器械查询可用动作列表（--muscle/--equipment组合在部分数据库有null值时会报错，优先用--name）
python skills/kaiji-fitness-coach/scripts/query_exercises.py --name "Row" --format json
```

⚠️ **已知限制：**
- `--muscle` + `--equipment` 组合查询在数据库有 null equipment 值时会报 AttributeError，优先用 `--name` 模糊匹配
- 输出编码在 PowerShell 下有乱码问题，用 `--format json` 或 `cmd /c` 包裹解决
- 如果数据库中不存在某个动作（如标准哑铃深蹲），说明该动作不在数据库中，保留合理常用名但标注说明

选择原则：
- **动作轮换**：与上一周期相比，替换 1-2 个辅助/孤立动作为数据库中的新动作（同肌群、同动作模式），主力复合动作保持稳定。替换前先查数据库确认新动作存在且器械匹配，并在计划备注中标注新增/替换的动作
- 每个训练日先排复合动作（mechanic=compound），再排孤立动作
- 每个大肌群1-2个复合动作 + 1个孤立动作
- 小肌群（二头、三头、小腿等）1-2个动作
- 动作数控制：每训练日 5-7 个动作

### 4. 训练日动态排序
**不使用固定顺序**，按肌肉恢复状态排列：

1. 根据用户上次训练日期，计算各肌群恢复天数
2. 恢复最久的肌群所在训练日排最前
3. 同一肌群至少间隔 48 小时
4. 用户有固定偏好（如周一必须推日）时，在满足恢复前提下尽量配合

### 5. App数据报告处理
当用户发送App训练数据报告时（特征：含"训练数据报告""每肌群组数""恢复状态"段落）：

1. 解析趋势：容量下降的肌群需调整，持续增长的保持
2. 参考1RM：用Mayhew估算值判断力量水平
3. 检查每肌群组数：🔴不足（<0.5×MEV）优先补量，⚠️偏低关注
4. 尊重恢复状态：🔴今日刚练的肌群不排当天，⚠️的排后面
5. 应用用户画像中的目标/经验/设备/重点肌群

### 6. 计划校验（生成后必做 — 强制工具调用）
**本步骤不可仅凭肉眼检查，必须实际调用数据库验证每个动作名：**

```bash
# 单个验证（调试或 ≤4 个动作时）
python skills/kaiji-fitness-coach/scripts/query_exercises.py --name "动作名" --format json
```

**批量验证（5+ 动作时必须用，2026-08-16 实测 18 动作一次通过，比逐个查询快 10 倍+）：**
写临时脚本到 workspace `temp/`，用 subprocess 循环调用查询脚本，一次 exec 输出全部动作的状态表：

```python
# temp/verify_plan_names.py 核心结构
import json, subprocess, sys
SCRIPT = r"C:\...\skills\kaiji-fitness-coach\scripts\query_exercises.py"  # 绝对路径
for name in NAMES:  # 所有待验证 exerciseName
    p = subprocess.run([sys.executable, SCRIPT, "--name", name, "--format", "json"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    data = json.loads(p.stdout)
    # 汇总输出: EXACT(精确匹配) / PARTIAL:近似名 / NOT_FOUND
```

⚠️ **Windows/KaijiBot 环境注意**：exec preflight 会拒绝 `cd && python ...` 链式调用（报 "complex interpreter invocation detected"）。必须用脚本**绝对路径**直接调用：`python "C:\...\query_exercises.py" --name "..." --format json`。批量脚本内部用 `sys.executable` + 绝对路径不受此限制。

- [ ] **每个 exerciseName 必须在数据库中精确匹配**（用 `--name` 查询，确认返回结果中有完全一致的名字）
- [ ] **不匹配的动作必须替换为数据库中的标准名**，不能保留未验证的名字
- [ ] 总组数合理：每肌群每周10-20组
- [ ] 推拉平衡：push日和pull日数量大致对等
- [ ] 无重复动作出现在同一计划中
- [ ] 应用用户私人约束（如有）

⚠️ 如果校验发现动作名不匹配，修正后重新保存JSON文件，再输出给用户。

### 7. 输出格式

**聊天场景** → Markdown表格（含动作、组数、次数、休息、备注）

**App数据报告要求JSON** → 只输出纯JSON，格式如下：
```json
{
  "name": "计划名称",
  "days": [
    {
      "dayOfWeek": 1,
      "targetMuscles": ["chest", "shoulders", "triceps"],
      "exercises": [
        {"exerciseName": "Incline Dumbbell Press", "targetSets": 4}
      ]
    }
  ]
}
```
- `exerciseName` 使用 free-exercise-db 标准英文名
- `targetMuscles` 使用英文肌群名
- `dayOfWeek` 1=周一 ... 7=周日
- **不加markdown包裹，不加额外解释**

## 依赖
- [assets/plan-template.json](../assets/plan-template.json) — JSON标准模板
- [references/workout-timer-integration.md](../references/workout-timer-integration.md) — App集成与MEV体系
- [references/muscle-reference.md](../references/muscle-reference.md) — 肌群参考
- [references/plan-design-principles.md](../references/plan-design-principles.md) — 计划设计原则
