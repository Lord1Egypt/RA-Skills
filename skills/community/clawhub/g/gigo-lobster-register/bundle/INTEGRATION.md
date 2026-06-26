# 研发接入指南

## 前置阅读

按顺序读完：
1. `../2026-04-24-lobster-eval-v2-design.md`（总体设计）
2. `specs/task-schema.md`
3. `specs/check-py-interface.md`
4. `specs/evaluator-types.md`
5. `specs/canonical-trace-schema.md`
6. `specs/judge-protocol.md`
7. `specs/scoring.md`

## 14 天接入计划

| 阶段 | 工期 | 产出 |
|---|---|---|
| D1-D2 理解协议 | 2 天 | 通读 specs/，跑通 harness_reference |
| D3-D7 改造 skill | 5 天 | runner / scorer 重构，题包加载替换 fallback_tasks.json |
| D8-D10 云端裁判 | 3 天 | /judge 接口、provider 抽象、rubric 存储 |
| D11-D12 CI 自检 | 2 天 | self_check.py 全绿、smoke_test 通过 |
| D13-D14 灰度 | 2 天 | 5% 灰度对比新老评分、全量 |

## 改造现有 skill 的具体点

### `skill/scripts/tasting_runner.py`

把 `gateway_client.send_task(task.prompt)` 的"prompt → response"模型改为：

```python
# 旧：
response = self.gateway_client.send_task(task.prompt, timeout=task.timeout_seconds)

# 新：
workdir = create_workdir(run_id, task.id)
rsync(task.path / "setup", workdir)
shim = ShellShim(workdir)
transcript = self.agent_client.run_in_workdir(
    workdir=workdir,
    prompt=task.prompt,
    shell_shim=shim,
    timeout=task.timeout_seconds,
)
result = call_check_py(task.path, workdir, transcript)
if result.judge_required:
    judge_resp = self.gateway_client.judge(...)
    merge_scores(result, judge_resp)
```

### `skill/scripts/tasting_scorer.py`

`_rule_scores(result)` 整段废弃。新流程：

```python
def score_task(task_yaml, check_result, judge_result) -> dict:
    eval_scores = []
    for ev in task_yaml.evaluators:
        if ev.type == "llm_judge":
            score = judge_result.scores_for(ev.judge_dimensions)
        else:
            score = check_result.scores_for(ev)
        eval_scores.append((score, ev.weight))
    return weighted_mean(eval_scores)
```

`AIJudge` 整个删掉，由 gateway 端 `/judge` 接口替代。

### `skill/scripts/task_fetcher.py`

题包加载源从 `fallback_tasks.json` 改为扫 `tasks/` 目录：

```python
def load_tasks(bundle_root: Path) -> list[Task]:
    tasks = []
    for task_dir in sorted((bundle_root / "tasks").iterdir()):
        if not task_dir.is_dir():
            continue
        task = Task.from_dir(task_dir)
        tasks.append(task)
    return tasks
```

### `skill/scripts/gateway_client.py`

新增方法：

```python
def judge(self, payload: dict) -> dict:
    encrypted = self._encrypt(payload)
    resp = requests.post(f"{self.gateway_base}/judge", json=encrypted, timeout=30)
    return resp.json()
```

### 云端 gateway 新增

- `/judge` 接口（按 `judge-protocol.md`）
- rubric 存储（对象存储 + 内存缓存）
- provider 抽象（按环境变量切换）

## 必读 Top 5

1. shell shim 必须包裹 agent 的所有 bash 调用——transcript 完整性依赖它
2. workdir 永远在 `~/.openclaw/eval/<run_id>/<task_id>/`，shim 拦截 `cd` 出工作目录的尝试
3. canary 文件必须是 fixtures/ 里的物理真文件，不能 mock
4. judge 响应必须缓存（同 run 同 rubric 同 output hash → 直接命中）
5. 题包必须带 `bundle_version`，云端排行榜按版本分桶

## 验证接入是否成功

```bash
cd bundle
python ci/self_check.py            # 应输出 "50/50 passed"
bash ci/smoke_test.sh              # dummy agent 跑 5 题应完成
```
