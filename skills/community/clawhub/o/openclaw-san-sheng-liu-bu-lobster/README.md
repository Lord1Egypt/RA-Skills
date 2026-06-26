# 🦞 OpenClaw 三省六部虾群 - 一人公司完整部署技能

> **让新龙虾也能学会任务分解和分配的技能**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/jiebao360/openclaw-san-sheng-liu-bu-lobster)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Clawhub](https://img.shields.io/badge/clawhub-available-orange.svg)](https://clawhub.ai)

---

## 📖 简介

本技能让新龙虾能够：
- ✅ 接收主龙虾分配的任务
- ✅ 通过 sessions_spawn 创建子代理会话执行任务
- ✅ 通过 openid 直接@每个龙虾发送任务通知
- ✅ 创建飞书文档并记录链接
- ✅ 更新飞书多维表格
- ✅ 汇总所有成果交付

**适用场景**：一人公司、小团队、创业者、内容创作者、知识付费从业者

---

## 🚀 快速开始

### 1. 安装技能

```bash
# 通过 Clawhub 安装
clawhub install openclaw-san-sheng-liu-bu-lobster

# 或手动安装
git clone https://github.com/jiebao360/openclaw-san-sheng-liu-bu-lobster.git
cp -r openclaw-san-sheng-liu-bu-lobster ~/.openclaw/workspace-main/agents/main/skills/
```

### 2. 配置龙虾团队

编辑 `config/lobster-team.md`，填入你的龙虾 OpenID：

```markdown
| 编号 | 角色 | 飞书机器人名称 | OpenID |
|------|------|--------------|--------|
| 龙虾 1 号 | 资料收集专家 | 第二大脑笔记助手 | ou_xxx |
| 龙虾 2 号 | 内容创作高手 | 通用内容创作虾 | ou_xxx |
...
```

### 3. 使用技能

在飞书群中发送：

```
🦞 各位龙虾注意，主龙虾下达任务！

【任务主题】[任务名称]
【参考文档】[文档链接]

【任务分配】
1️⃣ 龙虾 1 号：资料收集（15 分钟）
2️⃣ 龙虾 2 号：写文章（30 分钟）
3️⃣ 龙虾 3 号：朋友圈文案（15 分钟）
4️⃣ 龙虾 4 号：视频提示词（15 分钟）
5️⃣ 龙虾 5 号：图片提示词（20 分钟）
6️⃣ 龙虾 6 号：汇总文档（15 分钟）

收到请回复各自编号 + "收到，开始执行"！
```

---

## 📋 目录结构

```
task-decomposition/
├── SKILL.md                        # 完整技能说明
├── README.md                       # 使用文档（本文件）
├── LICENSE                         # MIT 许可证
├── PUBLISH.md                      # 发布指南
├── clawhub.json                    # Clawhub 配置
├── config/
│   └── lobster-team.md            # 龙虾团队配置模板
├── templates/
│   └── task-templates.md          # 任务模板库
└── docs/
    ├── auto-create-feishu-doc.md  # 飞书文档自动创建指南
    └── task-tracking.md           # 任务追踪指南
```

---

## 🎯 核心功能

### 1. 任务接收与理解
- 理解主龙虾的任务分配指令
- 识别任务编号、任务类型、输出要求
- 识别截止时间和依赖关系

### 2. 任务执行（sessions_spawn）
```python
sessions_spawn(
    agentId="main",
    cleanup="keep",
    cwd="/Users/laihehuo/.openclaw/workspace-main/agents/main",
    label="龙虾 X 号 - 任务类型",
    mode="run",
    runtime="subagent",
    task="任务描述..."
)
```

### 3. 飞书通知（openid）
```python
feishu_im_user_message(
    action="send",
    msg_type="text",
    receive_id="ou_xxx",  # 龙虾的 openid
    receive_id_type="open_id",
    content='{"text":"🦞 龙虾 X 号，收到请执行！..."}'
)
```

### 4. 飞书文档创建
```python
feishu_create_doc(
    title="🦞 任务名称 - 日期",
    markdown="[Markdown 内容]",
    folder_token="[文件夹 token]"
)
```

### 5. 多维表格记录
```python
feishu_bitable_app_table_record(
    action="batch_create",
    app_token="HxULbN8KTaIkCxsTmvYcg4ldnhh",
    table_id="tblAAxJLFpXO7k1X",
    records=[...]
)
```

---

## 📝 使用示例

### 示例 1：朋友圈内容包

```
【任务类型】朋友圈内容包
【任务主题】AI 工具测评
【期望输出】文案 3 条 + 图片提示词 3 张 + 视频脚本 1 个
【参与龙虾】
- 龙虾 1 号：整理核心卖点
- 龙虾 3 号：生成朋友圈文案
- 龙虾 5 号：生成图片提示词
- 龙虾 4 号：生成视频脚本
【截止时间】今天 15:00 前
```

### 示例 2：推广文章 + 分发

```
【任务类型】推广文章创作
【任务主题】[文章主题]
【目标字数】3000 字
【期望输出】
1. 完整文章
2. 文章摘要
3. 社群分享文案（3 版本）
4. 公众号标题 10 个
5. 配图建议 3-5 张
【参与龙虾】
- 龙虾 1 号：资料整理
- 龙虾 2 号：撰写文章
- 龙虾 3 号：分享文案
- 龙虾 5 号：配图提示词
```

### 示例 3：直播/会议内容处理

```
【任务类型】直播内容处理
【直播主题】[主题名称]
【期望输出】
1. 核心要点 10-15 条
2. 金句合集 20 条
3. 行动清单
4. 社群分享文案
5. 短视频脚本 3 个
【参与龙虾】
- 龙虾 1 号：提取要点
- 龙虾 2 号：整理金句
- 龙虾 3 号：分享文案
- 龙虾 4 号：视频脚本
```

---

## 🦞 龙虾团队配置

### 标准配置（6 只龙虾）

| 编号 | 角色 | 专长 | 典型任务 |
|------|------|------|---------|
| 龙虾 1 号 | 资料收集专家 | 资料收集、信息提取 | 文档分析、重点提炼 |
| 龙虾 2 号 | 内容创作高手 | 文章写作、内容生成 | 推广文章、长文写作 |
| 龙虾 3 号 | 朋友圈文案王 | 短文案、社交内容 | 朋友圈文案、社群分享 |
| 龙虾 4 号 | 视频脚本导演 | 视频提示词 | 电商视频脚本、短视频 |
| 龙虾 5 号 | 图片素材达人 | 图片搜索、视觉设计 | 找素材、配图、保存 |
| 龙虾 6 号 | 飞书文档管家 | 飞书文档处理、会议纪要 | 文档整理、汇总、格式化 |

### 添加新龙虾

1. 在 `config/lobster-team.md` 中添加新龙虾信息
2. 获取新龙虾的 OpenID
3. 在飞书群中@新龙虾测试
4. 更新多维表格字段

---

## 📊 执行流程

```
1. 接收用户指令
    ↓
2. 拆解为 6 个子任务
    ↓
3. sessions_spawn 创建子代理会话（执行）
    ↓
4. feishu_im_user_message 通过 openid@每个龙虾（通知）
    ↓
5. 各子代理并行执行任务
    ↓
6. 子代理完成后：
   - 自动推送成果到主会话
   - 创建飞书文档
   - 回复飞书文档链接
    ↓
7. 主助手收集所有成果
    ↓
8. 龙虾 6 号创建汇总飞书文档
    ↓
9. 更新飞书多维表格（包含所有产出链接）
    ↓
10. 交付完整成果给用户
```

---

## 🔗 相关链接

- [技能文档](SKILL.md)
- [任务模板库](templates/task-templates.md)
- [龙虾团队配置](config/lobster-team.md)
- [飞书文档自动创建指南](docs/auto-create-feishu-doc.md)
- [任务追踪指南](docs/task-tracking.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 强大的 AI 个人助理框架
- [唐朝三省六部制](https://zh.wikipedia.org/wiki/三省六部制) - 灵感来源
- 所有贡献者和使用者

---

*技能创建时间：2026-03-19*  
*技能版本：v1.0*  
*维护人：主助手（总指挥）*
