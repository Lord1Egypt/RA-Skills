# human-path.md — 人伴型 Agent（员工型）Workspace 构造步骤

> 本文件是 SKILL.md Phase 2 路径 A 的完整步骤。
> 仅当 Agent 类型确认为人伴型时读取本文件。

---

## A-1：创建目录结构

```bash
bash scripts/create_workspace.sh <agentId> --type human --notify-open-id <调度者飞书open_id>
```

脚本创建：
```
~/.openclaw/agency-agents/<agentId>/
├── memory/
└── skills/
```

---

## A-2：生成 IDENTITY.md

```markdown
# IDENTITY.md - Who Am I?

- **Name:** [名字]
- **Creature:** AI助手
- **Vibe:** [根据职责和性格，一句话气质描述]
- **Emoji:** [emoji]
- **Avatar:** （可选）
```

---

## A-3：生成 SOUL.md 骨架

**此时 BOOTSTRAP 还没执行，SOUL.md 只写骨架。**

骨架必须包含：
- 名字（第一句话的锚点）
- 公司背景预埋（填入公司名称和主营业务）
- 语言默认值（中文）
- 基本存在感描述（根据 Phase 1 的职责信息写 1-2 句）

⚠️ **骨架里不写具体性格细节**——那是 BOOTSTRAP 阶段的事。
⚠️ 写完后通读检查：有没有规则句式混入（有的话移到 AGENTS.md）。

参考：`references/soul-writing-guide.md`

---

## A-4：生成 AGENTS.md

必须包含三个部分：

**① 每次对话开始时的规则**（由脚本模板自动生成，不需修改）

**② 职责与场景规则**（根据 Phase 1 收集的信息生成）
- 使用场景触发式，不用通用指令
- 必须有"不做什么"的边界，至少 3 条

**③ 记忆规则**（写入引用句，记忆规则模板由 create_workspace.sh 生成到独立文件 memory-rules.md）

⚠️ 字数控制（先写完再剪枝）：
1. 先完整写入所有内容，不限制字数
2. 统计总字数（不含标题和空行），超过 500 时执行剪枝
3. 优先保留：场景触发规则 + 边界声明 + 记忆规则引用
4. 优先压缩：通用性描述、重复说明、可从上下文推断的内容
5. 剪枝后重新统计，仍超 500 → 压缩场景规则的粒度（合并相似场景）

---

## A-5：自动生成 TOOLS.md

根据 Phase 1 的 alsoAllow 列表自动生成，不进入 BOOTSTRAP 对话。

每个工具写三项：用途、什么时候用、什么时候不用（比"什么时候用"更重要）。

受限工具（需用户明确授权）单独列出。

参考：`references/file-formats.md` 中 TOOLS.md 部分。

---

## A-6：预埋 MEMORY.md

```markdown
# MEMORY.md - 长期记忆

## 关于公司
- 公司：[从 org-context.md 读取]
- 业务：[从 org-context.md 读取]

## 关于这个 Agent 的定位
- agentId: <agentId>
- 类型: 人伴型（员工型）
- 核心职责: <Phase 1 收集的职责>
- 调度者: <父 Agent id>

## 关于用户
（BOOTSTRAP.md 执行后填写）
```

---

## A-7：生成 HEARTBEAT.md

由 `create_workspace.sh --notify-open-id` 自动生成。检查生成内容，确认：
- 精炼频率判断逻辑正确
- 闲置通知目标 open_id 已填入
- 如有 Agent 特有的定期检查项，补充在 `[FILL]` 处

---

## A-8：生成 BOOTSTRAP.md

**读取 `references/bootstrap-protocol.md`，按协议生成完整的 BOOTSTRAP.md，覆盖脚本生成的占位符。**

BOOTSTRAP.md 内部结构：
```
1. 执行声明（此文件存在时优先执行）
2. 引用声明（去哪里读格式规范）
3. 信息槽位地图
4. 信息→文件映射表
5. 提问协议（第一轮规则 + 后续轮次 + 停止条件）
6. 写入执行步骤
7. 完成收尾（发送欢迎消息 + 删除本文件）
```

员工 Agent 的 BOOTSTRAP.md 开头第一步：
```
调用 feishu_get_user 获取用户飞书姓名，用于个性化开场。
```

---

## A-9：生成 USER.md 骨架

```markdown
# USER.md - About Your Human

## 基本信息
- **称呼：**（BOOTSTRAP 执行后填写）
- **岗位：**（BOOTSTRAP 执行后填写）
- **核心工作：**（BOOTSTRAP 执行后填写）

## 偏好
（随对话积累）

## 背景
（BOOTSTRAP 执行后填写）
```
