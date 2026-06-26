# 教学贴搜索结果

> 报告生成时间：2026-03-11  
> 搜索执行者：子代理 (depth 1/1)  
> 任务目标：为 CEO 香香的多 Agents 架构和自动化工作流提供参考

---

## OpenClaw 多 Agents 配置

### 找到的资源

| 标题 | 链接 | 来源 | 相关度 | 核心内容 |
|------|------|------|--------|----------|
| Multi-Agent Sandbox & Tools | https://docs.openclaw.ai/tools/multi-agent-sandbox-tools | OpenClaw 官方文档 | ⭐⭐⭐⭐⭐ | 官方多 Agent 配置文档，详解 sandbox 隔离、工具权限控制、agent 独立配置 |
| Multi-Agents in OpenClaw: Sub-Agents + Telegram Setup | https://blog.cdnsun.com/multi-agents-in-openclaw-sub-agents-and-telegram/ | CDNsun 博客 | ⭐⭐⭐⭐⭐ | 实战案例：main+coder+tester 三 agent 架构，子 agent _spawn 机制，binding 绑定 |
| OpenClaw multi-agent setup with multiple AI assistants | https://lumadock.com/tutorials/openclaw-multi-agent-setup | LumaDock VPS | ⭐⭐⭐⭐⭐ | 双模式详解：Persistent Agents(持久) vs Sub-agents(临时)，orchestrator 编排模式 |
| shenhao-stu/openclaw-agents | https://github.com/shenhao-stu/openclaw-agents | GitHub | ⭐⭐⭐⭐ | 9 个专用 agent 的预制配置包，开箱即用的多 agent 团队模板 |
| My Multi Agent Setup on OpenClaw | https://www.youtube.com/watch?v=LKjkYbT2M0Y | YouTube (David Alex) | ⭐⭐⭐⭐ | 23 分钟视频演示：Mac Mini 部署、agent 创建、工作流配置、问题排查 |
| My Multi-Agent Team with OpenClaw | https://www.youtube.com/watch?v=bzWI3Dil9Ig | YouTube (Brian Casel) | ⭐⭐⭐⭐ | 14 分钟实战：多 agent 团队协作配置 |
| OpenClaw Multi-Agent Deployment | https://medium.com/h7w/openclaw-multi-agent-deployment-from-single-agent-to-team-architecture-the-complete-path-353906414fca | Medium | ⭐⭐⭐⭐ | 从单 agent 到团队架构的完整路径，含 Gateway 进程内多 agent 隔离方案 |
| Any tips to run multi-agents in OpenClaw | https://www.reddit.com/r/openclaw/comments/1rjeisn/any_tips_to_run_multiagents_in_openclaw/ | Reddit r/openclaw | ⭐⭐⭐ | 社区讨论：multiple agents vs subagents 区别，最佳实践分享 |

### 关键发现

#### 官方文档链接
- **核心文档**：https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
- **Session 工具**：https://docs.openclaw.ai/concepts/session-tool (sessions_spawn)
- **Subagents 工具**：https://docs.openclaw.ai/tools/subagents

#### 社区案例
1. **CDNsun 三 agent 架构**：
   - `main` (总指挥) + `coder` (实现) + `tester` (验证)
   - 规则：coder 和 tester 不直接通信，main 作为 relay 中转
   - 优势：简单图结构，易于调试

2. **LumaDock 双模式**：
   - **Persistent Agents**：长期运行，绑定到特定渠道 (Slack/WhatsApp/Discord)
   - **Sub-agents**：后台临时任务，完成后自动归档

3. **GitHub 预制包**：9 个专用 agent 团队配置 (researcher/writer/coder/tester 等)

#### 代码示例

**基础多 Agent 配置 (openclaw.json)**：
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace",
        "sandbox": { "mode": "off" }
      },
      {
        "id": "family",
        "name": "Family Bot",
        "workspace": "~/.openclaw/workspace-family",
        "sandbox": { "mode": "all", "scope": "agent" },
        "tools": {
          "allow": ["read"],
          "deny": ["exec", "write", "edit", "browser"]
        }
      }
    ]
  }
}
```

**Sub-agent  spawning**：
```bash
# 主 agent 生成子 agent 执行任务
openclaw subagents spawn --task "研究竞品分析" --model "cheaper-model"
```

#### 最佳实践
1. **隔离原则**：每个 agent 独立 workspace、memory、auth-profiles、sessions
2. **工具权限**：按最小权限原则配置 allow/deny lists
3. **通信模式**：Hub-and-Spoke (总指挥 + 员工)，避免 agent 间直接通信
4. **成本控制**：主 agent 用强模型，子 agent 用便宜模型/本地模型
5. **调试友好**：每个 agent 的 session 文件独立，便于追踪问题

### 可借鉴的模式

#### 总指挥 + 员工架构
```
┌─────────────────┐
│   Main Agent    │ ← 用户交互入口
│   (Conductor)   │   决策/分发/汇总
└────────┬────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌──────┐ ┌──────┐ ┌──────┐
│Coder │ │Tester│ │Researcher│
│Agent │ │Agent │ │Agent     │
└──────┘ └──────┘ └──────┘
```

**特点**：
- Main agent 作为唯一用户接口
- 专业 agent 各司其职
- Main 负责任务分解和结果整合

#### 会话分发机制
- **Bindings**：将不同渠道消息路由到不同 agent
- **匹配规则**：provider + accountId + peer(kind/id)
- **示例**：WhatsApp 家庭群 → family agent，Slack 工作区 → work agent

#### 结果汇总方式
1. **子 agent 完成后**：将结果写入共享文件或返回给主 agent
2. **主 agent 整合**：收集所有子 agent 输出，生成统一回复
3. **Session 可见性**：配置 `sessions_spawn` 让主 agent 可查看子 agent 会话

---

## 飞书 Excel 工作流自动化

### 找到的资源

| 标题 | 链接 | 来源 | 相关度 | 核心内容 |
|------|------|------|--------|----------|
| 使用多维表格工作流 | https://www.feishu.cn/hc/zh-CN/articles/170735237222 | 飞书官方帮助中心 | ⭐⭐⭐⭐⭐ | 官方工作流功能说明，触发条件 + 执行操作详解 |
| 多维表格工作流介绍 | https://www.feishu.cn/hc/zh-CN/articles/908751305974 | 飞书官方帮助中心 | ⭐⭐⭐⭐⭐ | 工作流核心概念，与自动化流程的关系 |
| 飞书多维表格自动化（Bitable Automation） | https://openclawmp.cc/asset/s-eca11fa89f7a449d | 水产市场 | ⭐⭐⭐⭐⭐ | 完整教程：7 种触发 +12 种操作 +10 个实战场景 + 最佳实践 |
| 飞书多维表格 (Bitable) 技能 | https://lobehub.com/skills/openclaw-skills-feishu-api-bitable | LobeHub | ⭐⭐⭐⭐ | OpenClaw 技能：通过 API 操作飞书多维表格，支持 CRUD 和批量处理 |
| 解锁自动化新境界：n8n 与飞书多维表格的完美融合 | https://www.itsolotime.com/archives/16061 | 鲸林向海 | ⭐⭐⭐⭐ | n8n+ 飞书集成案例，数据采集→处理→存储→状态更新全流程 |
| Dify 与飞书多维表格数据交互的 7 个关键节点解析 | https://opc.csdn.net/696dfffd437a6b4033693c12.html | CSDN | ⭐⭐⭐ | AI 应用 (Dify) 与飞书数据打通，API 对接/同步/场景配置 |
| 手把手教你学会搭建复杂 n8n 工作流 | https://juejin.cn/post/7567678315265949705 | 稀土掘金 | ⭐⭐⭐ | 飞书多维表格 +n8n 批量生成小红书内容，自动化发布 |

### 关键发现

#### 飞书自动化能力

**7 种触发条件**：
| 触发条件 | 适用场景 | 特点 |
|----------|----------|------|
| 添加记录时 | 表单收集后自动处理 | 实时，常用于通知/分配 |
| 修改记录时 | 状态变更时触发 | 监控关键字段变化 |
| 满足条件时 | 新增或修改满足规则 | 灵活，支持多条件 |
| 到达时间时 | 截止日期提醒 | 基于日期字段，准点触发 |
| 定时触发 | 每日/每周汇总 | 固定时间，不依赖记录 |
| 点击按钮时 | 手动触发复杂流程 | 完全人工控制 |
| 接收 Webhook | 外部系统集成 | 跨系统自动化 |

**12+ 种执行操作**：
| 操作 | 功能 | 典型用途 |
|------|------|----------|
| 发送消息 | 通知人员或群组 | 提醒/周报/预警 |
| 发送邮件 | 自动邮件 | 正式通知/带附件 |
| 创建记录 | 新建数据 | 关联多表/日志记录 |
| 修改记录 | 更新字段 | 自动填充/状态流转 |
| 发送 HTTP 请求 | 调用外部 API | 系统集成/AI 调用 |
| AI 分类 | 自动文本分类 | 客服反馈分类 |
| AI 生成 | 文本生成/总结/翻译 | 内容处理 |
| 循环 | 批量处理 | 遍历多条记录 |
| 条件判断 | If/Else 分支 | 不同情况不同处理 |
| 多分支 | Switch 多路分支 | 多值匹配 |
| 延迟 | 等待 | 避免风控/间隔控制 |
| 创建日程/任务/群 | 飞书应用操作 | 自动创建资源 |

#### 工作流设计模式

**模式 1：触发器→查找→循环→动作**
```
定时触发 (每天 09:00)
  ↓
查找记录 (截止日期=今天 AND 状态≠已完成)
  ↓
循环每条记录
  ├→ 发送消息给负责人
  └→ 更新状态=逾期
```

**模式 2：条件分支**
```
修改记录 (状态字段)
  ↓
条件判断
  ├→ 状态="已完成" → 发送庆祝消息
  ├→ 状态="进行中" → 记录进度日志
  └→ 状态="已取消" → 通知相关人员
```

**模式 3：Webhook 集成**
```
外部系统 POST Webhook
  ↓
解析请求数据
  ↓
创建/更新飞书记录
  ↓
发送确认消息
```

#### 原子动作固化方法

**原子动作定义**：不可再分的最小执行单元
- 发送一条消息
- 创建一条记录
- 更新一个字段
- 调用一个 API

**固化方式**：
1. **模板化**：将常用流程保存为模板，重复使用
2. **参数化**：用变量替代具体值，提高复用性
3. **模块化**：将复杂流程拆分为多个子流程
4. **API 封装**：通过 OpenClaw 技能封装为可调用命令

**示例**：
```yaml
# 任务逾期提醒模板
trigger:
  type: scheduled
  time: "09:00"
actions:
  - find_records:
      table: tasks
      filter: "due_date=today AND status!=completed"
  - loop:
      foreach: records
      actions:
        - send_message:
            to: "{{record.owner}}"
            content: "⚠️ 任务【{{record.name}}】今天截止！"
        - update_record:
            id: "{{record.id}}"
            fields: {status: "overdue"}
```

### 可借鉴的模式

#### 触发器设计
- **事件驱动**：记录变化实时响应
- **时间驱动**：定时任务固定执行
- **人工驱动**：按钮触发复杂流程
- **外部驱动**：Webhook 接收外部系统信号

#### 动作执行
- **顺序执行**：按配置顺序依次执行
- **条件分支**：根据条件走不同路径
- **并行执行**：循环内批量处理
- **错误处理**：失败时重试或通知

#### 结果反馈
- **消息通知**：执行结果发送到飞书群/个人
- **记录更新**：将执行状态写入表格
- **日志记录**：创建执行日志便于追踪
- **汇总报告**：定时生成执行汇总

---

## 综合建议

### OpenClaw 多 Agents 实施建议

1. **起步架构 (推荐)**
   ```
   Main Agent (总指挥)
   ├── Coder Agent (代码实现)
   ├── Researcher Agent (信息搜集)
   └── Reviewer Agent (质量审核)
   ```

2. **配置要点**
   - 每个 agent 独立 workspace 和 agentDir
   - Main agent 不 sandbox，子 agent 根据风险级别配置 sandbox
   - 使用 bindings 将不同渠道消息路由到对应 agent
   - 配置 sessions_spawn 让主 agent 可查看子 agent 会话

3. **成本控制**
   - Main agent：用强模型 (如 qwen-plus)
   - 子 agent：用便宜模型或本地模型 (如 Ollama)
   - 简单任务：直接主 agent 处理，不 spawn 子 agent

4. **调试策略**
   - 每个 agent 的 session 文件独立保存
   - 配置日志级别，记录 agent 间通信
   - 使用 `openclaw agents list` 查看 agent 状态

### 飞书工作流固化建议

1. **技能封装路径**
   ```
   OpenClaw 技能
   ├── feishu-bitable (已有)
   │   ├── 创建/读取/更新/删除记录
   │   ├── 批量导入/导出
   │   └── 字段/视图管理
   └── feishu-workflow (建议新增)
       ├── 创建工作流
       ├── 触发工作流
       └── 查询执行状态
   ```

2. **原子动作固化**
   - 将常用工作流保存为模板
   - 通过 OpenClaw 技能封装为 CLI 命令
   - 支持参数化调用 (如 `feishu workflow run --template task-reminder`)

3. **与 OpenClaw 集成**
   ```
   用户请求
     ↓
   OpenClaw Main Agent
     ↓
   调用 feishu-bitable 技能
     ↓
   执行飞书 API 操作
     ↓
   返回结果给用户
   ```

4. **最佳实践**
   - 避免高频请求 (触发风控)
   - 使用批量接口减少 API 调用次数
   - 配置错误处理和重试机制
   - 记录执行日志便于追踪

### 下一步行动

#### 优先参考的资源
1. **OpenClaw 官方文档** - https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
2. **CDNsun 实战案例** - https://blog.cdnsun.com/multi-agents-in-openclaw-sub-agents-and-telegram/
3. **飞书自动化教程** - https://openclawmp.cc/asset/s-eca11fa89f7a449d

#### 需要实验验证的点
1. OpenClaw sessions_spawn 的实际使用方式
2. 飞书工作流 Webhook 触发与 OpenClaw 的集成
3. 多 agent 间的通信效率和一致性
4. 飞书 API 的 rate limit 和批量操作优化

#### 需要规避的坑
1. **OpenClaw**
   - ❌ 不要复用 agentDir (credentials 会混乱)
   - ❌ 不要让子 agent 直接通信 (保持 hub-and-spoke)
   - ❌ 不要给所有 agent 相同工具权限 (按最小权限原则)

2. **飞书**
   - ❌ 避免高频请求 (触发风控)
   - ❌ 不要自动化违规操作 (点赞/评论/关注)
   - ❌ 不要忽略错误处理 (工作流会静默失败)

---

## 附录：相关技能推荐

### OpenClaw 技能
- `openclaw-skills-feishu-api-bitable` - 飞书多维表格 API 操作
- 建议新增：`openclaw-skills-feishu-workflow` - 飞书工作流管理

### 外部工具
- **n8n** - 可视化工作流编排，可与飞书集成
- **Dify** - AI 应用平台，可与飞书数据交互

---

*报告结束*  
*生成时间：2026-03-11 14:35 GMT+8*
