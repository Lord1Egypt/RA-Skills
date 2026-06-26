# 改写记录 — Round 1

## 目标模式
- P01: 档案系统未生效
- P02: 欢迎语和隐私告知缺失

## 改动清单

### 1. 档案加载机制（SKILL.md → 执行流程）

**旧写法**（伪代码，无法执行）：
```bash
if [ -f "$PROFILE_PATH" ]; then
    cat "$PROFILE_PATH"
fi
```

**新写法**（明确调用文件工具）：
```markdown
**档案加载步骤**（每次对话前必须执行）：
1. 从上下文获取 user_id（如：ou_edd5093957e635ba596629b2ae18ba1a）
2. 检查文件：`~/.openclaw/workspace/memory/intj-users/{user_id}-profile.md`
3. 如果存在 → 用 `read` 工具读取，加载到上下文
4. 如果不存在 → 标记为"新用户"，触发欢迎流程
```

### 2. 档案保存机制（SKILL.md → 执行流程）

**旧写法**（伪代码）：
```bash
echo "## $(date +%Y-%m-%d)" >> "$PROFILE_PATH"
```

**新写法**（明确调用文件工具）：
```markdown
**档案保存步骤**（每次对话后必须执行）：
1. 用 `write` 或 `edit` 工具追加到 `{user_id}-sessions.md`
2. 用 `edit` 工具更新 `{user_id}-actions.md`（新增行动项）
3. 用 `edit` 工具更新 `{user_id}-profile.md`（最后更新时间）
```

### 3. 首次对话欢迎语（新增模板）

```markdown
**首次对话欢迎语**（仅新用户）：
```
你好，我是 INTJ Coach，专门帮 INTJ 解决成长/职业/创业问题。

对话会保存到你的个人档案（位置：~/.openclaw/workspace/memory/intj-users/），方便下次继续聊。

今天想聊点啥？随便说，想到啥说啥。
```
```

### 4. 隐私告知（新增）

```markdown
**隐私告知**（首次对话必说）：
- 对话内容会保存到本地档案
- 档案只属于你的 user_id
- 随时可以要求删除档案
```

## 预期效果

- **Prompt 1**：新用户会看到欢迎语 + 隐私告知，档案自动创建
- **Prompt 2**：老用户会加载历史，追问上次行动进展
- **评分提升**：Prompt 1 从 6→9，Prompt 2 从 3→9

## 不改动的

- P03（参考案例）— Round 2 处理
- P04（身份说明）— Round 2 处理
