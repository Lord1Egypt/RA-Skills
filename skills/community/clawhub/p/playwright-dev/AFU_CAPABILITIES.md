# 阿福能力清单

_所有阿福能做的事，按类别整理_

---

## 🎯 核心能力

### 1️⃣ 豆包会话处理

**能力：** 自动从豆包读取会话历史，生成专家点评网页

**脚本：**
- `fetch-doubao-history.ps1` - 从豆包读取会话历史
- `fetch-doubao-auto.ps1` - 自动获取豆包内容
- `fetch-doubao-simple.ps1` - 简化版获取脚本
- `save-doubao-automation.ps1` - 保存自动化配置
- `save-doubao-conversation.ps1` - 保存豆包会话

**输出：**
- `doubao-history-*.md` - 保存的会话记录
- `bom-expert-review.html` - 专家点评网页
- 多个迭代版本（v2~v9）

**网页特点：**
- Mermaid 知识架构图
- 专家深度洞察
- 对比表格
- 行动建议
- 记忆口诀
- 专业配色和布局

**使用场景：**
- 从豆包对话中提取知识
- 生成结构化的专家点评
- 创建可分享的 HTML 报告

---

### 2️⃣ 周报管理

**能力：** 日常工作记录 + 每周三自动生成周报

**文件：**
- `worklog.txt` - 日常工作日志
- `workreport.txt` - 正式周报模板
- `generate-workreport.ps1` - 周报生成脚本

**Cron 任务：**
- **名称：** 周三周报生成
- **时间：** 每周三 15:00 (Asia/Shanghai)
- **动作：** 自动运行生成脚本

**使用方式：**
```
### 2026-03-06 (周五)
- [完成] xxx
- [进行中] xxx
- [待办] xxx
```

**流程：**
1. 每天在 worklog.txt 记录工作
2. 每周三 15:00 自动生成 workreport.txt
3. 手动完善措辞
4. 发送给领导

---

### 3️⃣ 飞书集成

**能力：** 消息发送、任务管理、OAuth 待办

**已实现：**
- ✅ 飞书消息发送（文字 + 语音）
- ✅ 语音自动播放（0 步操作）
- ✅ 飞书多维表格任务管理
- ✅ 定时提醒（每小时优先级提醒）

**待完成：**
- 🔄 飞书 OAuth 配置（获取 user_access_token）
- 🔄 飞书原生待办集成
- 🔄 自动刷新 token 机制

**Cron 任务：**
- 每小时优先级提醒 + 语音
- 每小时知识库索引更新

---

### 4️⃣ 语音功能

**能力：** TTS 语音生成 + 自动播放

**实现方式：**
1. 调用 TTS 生成 MP3
2. 发送到飞书（文件附件）
3. 本地自动播放（Start-Process）

**使用场景：**
- 优先级提醒
- 重要通知
- 故事讲述
- 语音消息

**脚本：**
- `play-latest-voice.ps1` - 播放最新语音

---

### 5️⃣ 知识库管理

**能力：** 文件组织、索引更新、知识关联

**结构：**
```
knowledge-base/
├── README.md
├── _模板/
├── AI 助手使用/
├── 供应链管理/
├── 地理知识库/
└── 每日豆包/
```

**Cron 任务：**
- 每小时知识库索引更新
- 每天 23:00 晚安记忆同步（OneDrive）

**脚本：**
- `update-knowledge-index.ps1` - 更新索引
- `sync-goodnight.ps1` - 晚安同步
- `sync-to-onedrive.ps1` - 同步到 OneDrive

---

### 6️⃣ 地理知识库

**能力：** KML 解析、地点关联、可视化

**项目位置：** `projects/地理知识库/项目章程.md`

**核心功能：**
1. 导入 Google Earth KML/KMZ 地标
2. 关联个人回忆、工作事件、学习内容
3. 生成地点详情页（含人文知识）
4. 地图/时间线/热力图可视化

**项目阶段：** 阶段 1（基础建设中）

**待办：**
- [ ] Thomas 导出测试 KML 文件
- [ ] 阿福解析并生成示例
- [ ] 确认地点记录模板
- [ ] 批量导入全部地标

---

### 7️⃣ HTML 报告生成

**能力：** 生成专业 HTML 报告、可视化页面

**已生成：**
- `bom-expert-review.html` - BOM 专家点评
- `bom-material-flow.html` - 物料流程图
- `claw-architecture.html` - 架构图
- `milestone-report-*.html` - 里程碑报告

**特点：**
- 专业配色和布局
- Mermaid 图表集成
- 响应式设计
- 可打印格式

---

### 8️⃣ Cron 定时任务

**已配置的定时任务：**

| 名称 | 时间 | 频率 | 说明 |
|------|------|------|------|
| 知识库索引更新 | :34 | 每小时 | 更新知识库索引 |
| 每小时优先级提醒 | :35 | 每小时 | 文字 + 语音提醒 |
| Qwen API 监控 | :42 | 每小时 | 监控 API 调用次数 |
| 周三周报生成 | 15:00 | 每周三 | 自动生成周报 |
| 晚安记忆同步 | 23:00 | 每天 | 同步到 OneDrive |
| 周五里程碑报告 | 23:30 | 每周五 | 生成周报 |

---

## 📊 技术栈

**脚本语言：**
- PowerShell - 自动化脚本
- HTML/CSS/JS - 网页生成
- Mermaid - 图表绘制

**集成平台：**
- 飞书 - 消息、任务、待办
- 豆包 - 会话历史读取
- OneDrive - 文件同步
- Google Earth - 地理数据

**定时系统：**
- OpenClaw Cron - 定时任务调度

---

## 🎯 使用指南

### 快速开始

**1. 日常工作记录**
```
打开 worklog.txt → 添加今日工作 → 保存
```

**2. 生成专家点评**
```
运行 fetch-doubao-history.ps1 → 获取会话 → AI 分析 → 生成 HTML
```

**3. 查看任务列表**
```
打开飞书多维表格：https://scns3ak4jrto.feishu.cn/base/ACmYbQE7kaieWzsuwhccf38inFf
```

**4. 手动生成周报**
```
powershell -ExecutionPolicy Bypass -File generate-workreport.ps1
```

---

## 📝 待扩展能力

**计划中：**
- [ ] 飞书原生待办集成（OAuth 配置中）
- [ ] 地理知识库批量导入
- [ ] 更多专家点评模板
- [ ] 自动化报告生成
- [ ] 更多定时任务

**想法：**
- 月度总结报告
- 项目进度追踪
- 人际关系管理
- 学习计划制定

---

## 🔗 相关文件

- `MEMORY.md` - 长期记忆
- `memory/YYYY-MM-DD.md` - 每日记忆
- `worklog.txt` - 工作日志
- `workreport.txt` - 周报
- `knowledge-index.md` - 知识库索引

---

_最后更新：2026-03-06_  
_维护者：阿福 🐾_
