# Prompt-Router 持续优化机制

**版本：** 1.0.0  
**创建时间：** 2026-04-06 00:05

---

## 🎯 目标

建立自动化的反馈收集、分析和优化闭环，让 Prompt-Router 能够"自行进化"。

---

## 📊 反馈收集系统

### 1. 自动日志

**位置：** `~/.openclaw/workspace/output/prompt-router/logs/`

**日志格式：**
```json
{
  "timestamp": "2026-04-06T00:00:00Z",
  "prompt": "搜索 Python 教程",
  "matched_skill": "multi-search-engine",
  "confidence": 0.35,
  "decision": "invoke",
  "latency_ms": 7.38,
  "user_accepted": true,
  "user_corrected": false
}
```

**收集内容：**
- 用户查询
- 匹配结果
- 置信度
- 路由决策
- 响应时间
- 用户反馈（接受/纠正）

### 2. 用户反馈渠道

| 渠道 | 类型 | 频率 | 负责人 |
|------|------|------|--------|
| GitHub Issues | Bug/建议 | 实时 | 自动监控 |
| 虾评评论 | 评分/心得 | 每日检查 | 自动收集 |
| ClawHub 评价 | 评分/下载 | 每日检查 | 自动收集 |
| Discord 讨论 | 实时反馈 | 实时监控 | 自动监听 |

### 3. 使用统计

**指标：**
- 总调用次数
- 匹配成功率
- 平均置信度
- 平均延迟
- 用户接受率
- 技能分布

**收集方式：**
```python
# 在 integration.py 中添加统计
stats = {
    "total_calls": 0,
    "matched": 0,
    "high_confidence": 0,
    "fallback": 0,
    "avg_latency": 0.0,
}
```

---

## 🔍 自动分析系统

### 1. 误匹配检测

**检测规则：**

```python
def detect_mismatches(logs):
    """检测误匹配案例"""
    mismatches = []
    for log in logs:
        # 规则 1: 高置信度但用户纠正
        if log['confidence'] > 0.5 and log['user_corrected']:
            mismatches.append({
                'type': 'false_positive',
                'prompt': log['prompt'],
                'matched': log['matched_skill'],
                'confidence': log['confidence']
            })
        
        # 规则 2: 低置信度但用户接受
        if log['confidence'] < 0.2 and log['user_accepted']:
            mismatches.append({
                'type': 'false_negative',
                'prompt': log['prompt'],
                'matched': log['matched_skill'],
                'confidence': log['confidence']
            })
    
    return mismatches
```

### 2. 性能瓶颈分析

**分析维度：**

```python
def analyze_performance(logs):
    """分析性能瓶颈"""
    # 1. 延迟分布
    latency_percentiles = {
        'p50': np.percentile(latencies, 50),
        'p90': np.percentile(latencies, 90),
        'p99': np.percentile(latencies, 99),
    }
    
    # 2. 慢查询分析
    slow_queries = [l for l in logs if l['latency_ms'] > 20]
    
    # 3. 技能加载时间
    load_time = measure_skill_load_time()
    
    return {
        'latency': latency_percentiles,
        'slow_queries': slow_queries,
        'load_time': load_time
    }
```

### 3. 热词发现

**发现新触发词：**

```python
def discover_hot_terms(logs):
    """从高频查询中发现新触发词"""
    # 1. 统计高频查询
    query_freq = Counter([l['prompt'] for l in logs])
    
    # 2. 提取未匹配的查询
    unmatched = [l['prompt'] for l in logs if not l['matched_skill']]
    
    # 3. 分词统计
    all_terms = []
    for prompt in unmatched:
        tokens = tokenizer.tokenize(prompt)
        all_terms.extend(tokens)
    
    term_freq = Counter(all_terms)
    
    # 4. 返回高频词（建议添加为 triggers）
    return term_freq.most_common(20)
```

---

## 🔄 自动优化流程

### 1. Triggers 自动更新

**流程：**

```
每周日凌晨 2 点执行
    ↓
分析过去 7 天日志
    ↓
发现高频未匹配词
    ↓
生成 triggers 建议
    ↓
创建 Pull Request
    ↓
等待人工审核
    ↓
合并后自动部署
```

**实现：**

```python
def auto_update_triggers():
    """自动生成 triggers 更新建议"""
    logs = load_logs(days=7)
    hot_terms = discover_hot_terms(logs)
    
    updates = []
    for term, freq in hot_terms:
        if freq >= 5:  # 出现 5 次以上
            # 找到最相关的技能
            related_skill = find_related_skill(term)
            updates.append({
                'skill': related_skill,
                'new_trigger': term,
                'frequency': freq
            })
    
    # 生成更新脚本
    generate_update_script(updates)
    create_pr(title=f"feat: Auto-update triggers based on usage data")
```

### 2. 置信度阈值优化

**自适应调整：**

```python
def optimize_threshold(logs):
    """根据历史数据优化置信度阈值"""
    # 1. 统计不同阈值下的准确率
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5]
    results = []
    
    for t in thresholds:
        accepted = sum(1 for l in logs if l['confidence'] >= t and l['user_accepted'])
        total = sum(1 for l in logs if l['confidence'] >= t)
        accuracy = accepted / total if total > 0 else 0
        results.append((t, accuracy))
    
    # 2. 选择准确率>90% 的最低阈值
    optimal_t = min([t for t, acc in results if acc > 0.9], default=0.25)
    
    return optimal_t
```

### 3. 评分权重调优

**机器学习优化：**

```python
def optimize_weights(logs):
    """使用梯度下降优化评分权重"""
    # 特征：各字段匹配分
    # 标签：用户是否接受
    # 目标：最大化准确率
    
    from sklearn.linear_model import LogisticRegression
    
    X = []  # 特征矩阵
    y = []  # 标签
    
    for log in logs:
        features = [
            log['name_score'],
            log['triggers_score'],
            log['keywords_score'],
            log['description_score']
        ]
        X.append(features)
        y.append(1 if log['user_accepted'] else 0)
    
    # 训练模型
    model = LogisticRegression()
    model.fit(X, y)
    
    # 提取最优权重
    optimal_weights = {
        'name': model.coef_[0][0],
        'triggers': model.coef_[0][1],
        'keywords': model.coef_[0][2],
        'description': model.coef_[0][3]
    }
    
    return optimal_weights
```

---

## 📈 版本迭代机制

### 1. 版本号规则

遵循 SemVer 2.0.0：

```
主版本号。次版本号。修订号
  ↑      ↑      ↑
  |      |      └─ Bug 修复
  |      └─ 新功能（向后兼容）
  └─ 重大变更（不兼容）

示例：
1.0.0 → 初始发布
1.0.1 → Bug 修复
1.1.0 → 新功能
2.0.0 → 重大更新
```

### 2. 发布节奏

| 版本类型 | 节奏 | 触发条件 |
|----------|------|----------|
| 修订版 (x.x.1) | 随时 | Bug 修复 |
| 次版本 (x.1.0) | 每 2 周 | 新功能、优化 |
| 主版本 (2.0.0) | 每季度 | 重大变更 |

### 3. Changelog 自动生成

```python
def generate_changelog(from_version, to_version):
    """自动生成更新日志"""
    # 1. 获取 Git commits
    commits = get_commits_between(from_version, to_version)
    
    # 2. 分类
    features = [c for c in commits if c.startswith('feat')]
    fixes = [c for c in commits if c.startswith('fix')]
    docs = [c for c in commits if c.startswith('docs')]
    
    # 3. 生成 Markdown
    changelog = f"""
## [{to_version}] - {date.today()}

### Features
{format_commits(features)}

### Bug Fixes
{format_commits(fixes)}

### Documentation
{format_commits(docs)}
"""
    return changelog
```

---

## 🤖 自动化脚本

### 1. 每日任务（Cron: 0 2 * * *）

```bash
# 每日凌晨 2 点执行
0 2 * * * python ~/.openclaw/workspace/skills/prompt-router/scripts/daily_analysis.py
```

**内容：**
- 收集前一天日志
- 计算统计指标
- 检测异常（误匹配率突增）
- 发送日报

### 2. 每周任务（Cron: 0 3 * * 0）

```bash
# 每周日凌晨 3 点执行
0 3 * * 0 python ~/.openclaw/workspace/skills/prompt-router/scripts/weekly_optimization.py
```

**内容：**
- 分析一周数据
- 生成 triggers 更新建议
- 优化置信度阈值
- 创建 Pull Request

### 3. 每月任务（Cron: 0 4 1 * *）

```bash
# 每月 1 号凌晨 4 点执行
0 4 1 * * python ~/.openclaw/workspace/skills/prompt-router/scripts/monthly_report.py
```

**内容：**
- 生成月度报告
- 统计下载量/用户数
- 分析趋势
- 规划下月目标

---

## 📊 监控告警

### 告警规则

| 指标 | 阈值 | 动作 |
|------|------|------|
| 误匹配率 | >15% | 邮件通知 |
| 平均延迟 | >20ms | Discord 告警 |
| 降级率 | >60% | 检查阈值配置 |
| 错误率 | >5% | 立即修复 |

### 告警方式

```python
def send_alert(metric, value, threshold):
    """发送告警"""
    message = f"""
🚨 Prompt-Router 告警

指标：{metric}
当前值：{value}
阈值：{threshold}
时间：{datetime.now()}

请立即检查！
"""
    # 1. Discord webhook
    send_to_discord(message)
    
    # 2. 邮件通知
    send_email(subject=f"Alert: {metric}", body=message)
    
    # 3. GitHub Issue
    create_issue(title=f"Alert: {metric} exceeded threshold", body=message)
```

---

## 🎯 自行进化路线图

### Phase 1: 数据收集（当前）

- [x] 基础日志系统
- [x] GitHub 仓库
- [ ] ClawHub 发布
- [ ] 虾评发布

### Phase 2: 自动分析（v1.1.0）

- [ ] 误匹配检测
- [ ] 性能分析
- [ ] 热词发现
- [ ] 日报生成

### Phase 3: 自动优化（v1.2.0）

- [ ] Triggers 自动更新
- [ ] 阈值自适应
- [ ] 权重优化
- [ ] PR 自动生成

### Phase 4: 机器学习（v2.0.0）

- [ ] 神经网络评分
- [ ] 个性化路由
- [ ] 预测性缓存
- [ ] 多语言支持

---

## 📝 贡献指南

### 报告问题

```markdown
**问题类型：** Bug / 功能建议 / 文档改进

**描述：**
简要描述问题

**复现步骤：**
1. ...
2. ...

**期望行为：**
...

**实际行为：**
...

**环境：**
- OpenClaw 版本：
- Python 版本：
- OS:
```

### 提交 PR

```bash
# 1. Fork 仓库
# 2. 创建分支
git checkout -b feature/amazing-feature

# 3. 提交更改
git commit -m "feat: add amazing feature"

# 4. 推送
git push origin feature/amazing-feature

# 5. 创建 Pull Request
```

### 代码审查清单

- [ ] 代码符合 PEP 8
- [ ] 添加单元测试
- [ ] 更新文档
- [ ] 测试通过
- [ ] Changelog 更新

---

## 🙏 致谢

感谢所有贡献者让 Prompt-Router 变得更好！

每一位提交 Issue、PR、分享心得的用户都是项目进化的动力。

---

*持续优化机制版本：1.0.0*
*最后更新：2026-04-06 00:05*
