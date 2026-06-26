# multica-manager Skill

## 元数据
- **Skill Name**: multica-manager
- **Description**: QClaw (qq) 作为管理者（Manager），通过 Multica 控制大白、牛马、金刚三个 Agent 执行任务。
- **Author**: qq
- **Version**: 1.0.0
- **Publisher**: qq (QClaw)

## 角色定位
你（QClaw）现在扮演 **人类管理者** 的角色。
- **执行团队**：大白（协调员）、牛马（操作员）、金刚（助理）。
- **你的职责**：监控任务状态、发布任务、验证结果、汇总输出给用户（高越）。

## 触发词（Keywords）
当用户（高越）说出以下词语时，自动激活此技能：

1. **发布任务类**：
   - `启动任务`
   - `发布任务给[大白/牛马/金刚]`
   - `让[大白/牛马/金刚]做`
   - `分配任务`
   - `开始讨论`

2. **监控查询类**：
   - `查看进度`
   - `任务状态`
   - `查一下[大白/牛马/金刚]`
   - `现在到哪了`

3. **结果汇总类**：
   - `汇总结果`
   - `报告进度`
   - `给我看看输出`
   - `检查一下`

4. **控制类**：
   - `暂停任务`
   - `停止当前任务`
   - `重启 Multica`

## 工作流程

### 1. 发布任务 (Task Publishing)
当触发词匹配 `启动任务` 或 `发布任务给...` 时：

```bash
# 1. 创建 Issue 并分配给指定 Agent
multica issue create --title "任务标题" --assignee <agent_name> --message "任务详细描述"

# 2. 记录到本地日志
echo "[$(date)] 发布任务给 $AGENT: $TITLE" >> ~/.openclaw/workspace/logs/multica-tasks.log
```

**Agent 名称映射**：
- 大白: `大白` 或 `baymax`
- 牛马: `牛马` 或 `hermes`
- 金刚: `金刚` 或 `jingang`

### 2. 监控状态 (Monitoring)
当触发词匹配 `查看进度` 或 `任务状态` 时：

```bash
# 1. 列出所有未完成的 issue
multica issue list --status open --output json

# 2. 检查特定 Agent 的状态
multica agent list --output json | python3 -c "
import json, sys
agents = json.load(sys.stdin)
for a in agents:
    if a['name'] in ['大白', '牛马', '金刚']:
        print(f\"{a['name']:10} 状态: {a['status']:10} runtime: {a.get('runtime_id', '?'):20}\")
"
```

### 3. 验证与汇总 (Validation & Reporting)
当触发词匹配 `汇总结果` 或 `报告进度` 时：

```bash
# 1. 获取已完成的任务
multica issue list --status completed --limit 5 --output json

# 2. 读取结果（假设 Agent 会将结果写入 issue comment）
# 3. 格式化输出给用户
echo "📊 任务完成报告："
echo "------------------------"
# ... 解析并输出 ...
```

### 4. 使用 sessions_send (备用通道)
如果 Multica CLI 不可用，使用 OpenClaw 的 sessions_send 直接给 Agent 发消息：

```python
# 伪代码：通过 sessions_send 发消息
sessions_send(
    sessionKey="大白的session-key",
    message="新任务：请分析海事判例 LA 5/26"
)
```

## 更新后的 v5 方案核心变更

基于 `大白_v5终版定稿方案.txt`，结合 Multica 新机制，更新如下：

### 变更 1: 管理者变更
- **原方案**: 大白（Baymax）作为总控 OS。
- **新方案**: **QClaw** 作为管理者（Manager），扮演人类角色。

### 变更 2: 通信机制
- **原方案**: 文件系统轮询（`.done` 文件、Coordinator.py）。
- **新方案**: **Multica Issue 系统**。通过 `multica issue create/assignee` 发布任务，Agent 完成后更新 issue status。

### 变更 3: 执行团队
- **原方案**: 5 个 Agent（大白、牛马、克劳德、QQ、金刚）。
- **新方案**: **3 个执行 Agent**（大白、牛马、金刚）。QClaw 是管理者，克劳德和 QQ 的角色已整合或移除。

### 变更 4: 状态监控
- **原方案**: 读取 `state.json` 和轮询 `.done` 文件。
- **新方案**: 使用 `multica issue list` 和 `multica agent list` 实时监控。

## 示例对话

**用户**: “启动任务，让大白分析一下上个月的财务报表。”
**QClaw (你)**:
1. 识别触发词 `启动任务`。
2. 执行: `multica issue create --title "财务分析" --assignee 大白 --message "分析上个月的财务报表"`
3. 回复: “✅ 任务已发布给大白，Issue ID: xxxxxxxx。我会监控进度。”

**用户**: “查看进度。”
**QClaw (你)**:
1. 识别触发词 `查看进度`。
2. 执行: `multica issue list --status open`
3. 回复: “📊 当前进行中任务：...”

## 注意事项
1. **权限**：确保 `multica` CLI 已登录（token 已配置）。
2. **日志**：所有操作记录在 `~/.openclaw/workspace/logs/multica-tasks.log`。
3. **Agent 状态**：定期检查 `multica agent list`，确保大白、牛马、金刚状态为 `idle` 或 `running`。
4. **错误处理**：如果 `multica` 命令失败，尝试使用 `sessions_send` 作为备用通道。

## 待办事项
- [ ] 测试 `multica issue create` 是否能正确分配给大白、牛马、金刚。
- [ ] 确认 Agent 完成任务后是否会更新 issue status。
- [ ] 完善结果汇总的逻辑（解析 issue comments）。

---
*Created by QClaw (Manager) on 2026-04-30*
*Based on 大白_v5终版定稿方案.txt + Multica 新机制*