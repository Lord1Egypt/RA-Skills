# health-git

把 Git 工作流语义（Issue → Branch → Commit → PR → Review → Merge）搬到健康干预场景的 AI 助手技能。

用户每次打卡/录入数据 = `care_commit`，健康管理师/医生 Review 后 `merge` 进下一周计划，所有事件可审计。

## 使用场景

- **患者/消费者**：记录每日饮食、运动、用药打卡，提交 PR，等待审核
- **健康管理师/医生**：查看待审 PR，运行安全检查，approve/reject 干预计划
- **数据分析**：查看依从率、merge 率等指标，作为 reward model 训练信号

## 前置条件

服务默认运行在 `http://localhost:8090`，可通过环境变量覆盖：

```bash
export HEALTH_GIT_BASE_URL=http://localhost:8090
# 如开启鉴权：
export AUTH_ENABLED=true
export CONSUMER_API_KEY=consumer-key
export REVIEWER_API_KEY=reviewer-key
```

启动服务：
```bash
cd <项目目录>
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8090
```

初始化示例数据：
```bash
curl -X POST http://localhost:8090/api/seed
```

## API 速查

| 操作 | 方法 | 路径 |
|------|------|------|
| 健康检查 | GET | /api/health |
| 初始化数据 | POST | /api/seed |
| 查看全局看板 | GET | /api/dashboard |
| 提交打卡（care commit） | POST | /api/commits |
| 开启干预 PR | POST | /api/prs |
| 审核 PR | POST | /api/prs/{pr_id}/review |
| 记录结果指标 | POST | /api/outcomes |
| 查看指标 | GET | /api/metrics |
| 查看事件日志 | GET | /api/events |
| 查看检查规则 | GET | /api/rules |
| 更新检查规则 | PATCH | /api/rules/{rule_id} |

## 对话示例

**用户**：帮我记录今天的打卡：步行8000步，依从度80分

**助手操作**：
```bash
curl -s -X POST http://localhost:8090/api/commits \
  -H "Content-Type: application/json" \
  -d '{"branch_id":1,"user_id":1,"task_type":"exercise","evidence_text":"步行8000步","metric_value":8000,"adherence_score":80}'
```

---

**用户**：帮我提交本周干预计划的 PR，低风险

**助手操作**：
```bash
curl -s -X POST http://localhost:8090/api/prs \
  -H "Content-Type: application/json" \
  -d '{"branch_id":1,"requested_by":1,"summary":"本周饮食控制+步行计划","risk_level":"low"}'
```

---

**用户**：审核一下 PR #1，批准通过

**助手操作**：
```bash
curl -s -X POST http://localhost:8090/api/prs/1/review \
  -H "Content-Type: application/json" \
  -H "x-api-key: reviewer-key" \
  -d '{"reviewer_id":2,"action":"approve","review_note":"依从良好，计划合理"}'
```

---

**用户**：把药物变更检查的关键词加上"adjust dose"

**助手操作**：
```bash
# 先获取当前规则
curl -s http://localhost:8090/api/rules | python3 -m json.tool

# 更新关键词
curl -s -X PATCH http://localhost:8090/api/rules/MEDICATION_CHANGE_REVIEW \
  -H "Content-Type: application/json" \
  -d '{"config_json":{"keywords":["increase medication","new drug","double dose","insulin","adjust dose"]}}'
```

---

**用户**：看一下当前指标怎么样

**助手操作**：
```bash
curl -s http://localhost:8090/api/metrics | python3 -m json.tool
```

返回字段：`commit_rate`（总打卡数）、`merge_rate`（审核通过率）、`blocked_rate`（被拦截率）、`avg_adherence`（平均依从分）

## 检查规则说明

系统内置两条可配置规则：

- **MEDICATION_CHANGE_REVIEW**：PR summary 含药物变更关键词时自动拦截，需人工 review
- **ADHERENCE_GATE**：最近一次打卡依从分低于阈值（默认50）时拦截

规则均可通过 `PATCH /api/rules/{rule_id}` 动态调整，无需重启服务。

## 注意事项

- `merge` = 用户+专家双重认可的正强化事件，适合作为 RL reward 信号
- 所有操作写入 `events` 表，可用 `GET /api/events?event_type=merge_completed` 过滤
- 鉴权默认关闭；生产环境请设置 `AUTH_ENABLED=true` 并配置 API key
