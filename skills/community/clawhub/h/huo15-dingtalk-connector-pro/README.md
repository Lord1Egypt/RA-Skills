<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

**打破信息孤岛，用一套系统驱动企业增长**
**加速企业用户向全场景人工智能机器人转变**

</div>

<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

# 🔔 huo15-dingtalk-connector-pro

> **作者**: 火一五信息科技有限公司
> **版本**: v1.0.0
> **参考**: [dingtalk-openclaw-connector](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) v0.8.12
> **触发词**: 钉钉、钉钉连接器、dingtalk

---

## 一、简介

火一五定制版钉钉 OpenClaw 连接器，基于官方 dingtalk-openclaw-connector v0.8.12 定制，支持 huo15-memory-evolution 记忆系统集成和 Claude Code 能力增强。

---

## 二、核心特性

| 特性 | 说明 |
|------|------|
| 🤖 **记忆系统集成** | 支持 huo15-memory-evolution 记忆系统 |
| 💬 **AI Card 流式响应** | 打字机效果，实时流式显示回复 |
| 🔒 **会话持久化** | 同一用户的多轮对话共享上下文 |
| 🎯 **会话隔离** | 按单聊/群聊/群区分 session |
| ⏰ **超时自动新会话** | 默认 30 分钟无活动自动开启新对话 |
| 📁 **富媒体接收** | 支持 JPEG/PNG 图片、文件附件 |
| 🎵 **音频消息** | 支持发送多种格式音频 |
| 📄 **钉钉文档 API** | 支持创建、追加、搜索钉钉文档 |
| 🔗 **多 Agent 路由** | 支持一个连接器实例连接多个 Agent |

---

## 三、快速开始

### 3.1 前置要求

- OpenClaw 已安装并运行
- 钉钉企业账号

### 3.2 安装

```bash
# 克隆仓库
git clone https://github.com/huo15/huo15-dingtalk-connector-pro.git
cd huo15-dingtalk-connector-pro

# 安装依赖
npm install

# 以链接模式安装
openclaw plugins install -l .
```

### 3.3 配置

1. 获取钉钉凭证
   - 访问 [钉钉开放平台](https://open-dev.dingtalk.com/)
   - 创建企业内部应用
   - 获取 AppKey 和 AppSecret

2. 配置连接器

```bash
# 方式一：使用配置向导
openclaw channels add

# 方式二：直接编辑配置文件
# macOS: ~/.openclaw/openclaw.json
```

```json
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "你的AppKey",
      "clientSecret": "你的AppSecret"
    }
  }
}
```

### 3.4 重启验证

```bash
# 重启 Gateway
openclaw gateway restart

# 检查插件状态
openclaw plugins list

# 查看日志
openclaw logs --follow
```

---

## 四、完整功能列表

### 4.1 基础功能

- **AI Card 流式响应** - 打字机效果，实时显示 AI 回复
- **会话管理** - 多轮对话共享上下文
- **会话隔离** - 按单聊/群聊/群区分 session
- **手动/自动会话重置** - 发送 /new 或 30分钟无活动自动新会话
- **图片自动上传** - 自动上传到钉钉
- **富媒体接收** - JPEG/PNG 图片，支持视觉模型
- **文件附件** - 解析 .docx, .pdf, 文本, 二进制文件
- **音频消息** - 支持 mp3, wav, amr, ogg 格式
- **钉钉文档 API** - 创建、追加、搜索、列出文档
- **多 Agent 路由** - 多个 bot 连接不同 agent
- **Markdown 表格转换** - 自动转换为钉钉兼容格式

---

## 五、开发计划

### 5.1 融合火一五记忆进化系统

- [ ] 将 huo15-memory-evolution 集成到钉钉连接器
- [ ] 实现会话记忆持久化
- [ ] 支持 user/feedback/project/reference 四类记忆
- [ ] 实现 Auto Capture 自动捕获高光时刻
- [ ] 实现 Dream Agent 每日日志提炼

### 5.2 融合 Claude Code 能力

- [ ] 实现 findRelevantMemories 智能记忆检索
- [ ] 实现 CLAUDE.md 项目级指令注入
- [ ] 实现 Manifest pre-inject
- [ ] 实现 Forked extraction 后台提取
- [ ] 实现 Before recommending 规范

---

## 六、与官方版区别

| 功能 | 官方版 | 定制版 |
|------|--------|--------|
| 基础功能 | ✅ | ✅ |
| 记忆系统集成 | ❌ | ✅ huo15-memory-evolution |
| Claude Code 能力 | ❌ | ✅ 进行中 |
| AI Card 流式响应 | ✅ | ✅ |
| 多 Agent 路由 | ✅ | ✅ |

---

## 七、项目结构

```
huo15-dingtalk-connector-pro/
├── src/
│   ├── core/           # 核心连接器逻辑
│   ├── services/       # 钉钉 API 服务
│   ├── utils/         # 工具函数
│   └── types/          # TypeScript 类型定义
├── docs/
│   └── images/        # 文档图片
├── openclaw.plugin.json # 插件清单
├── package.json        # npm 依赖
└── LICENSE
```

---

## 八、相关链接

- **官方版**: https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector
- **OpenClaw**: https://openclaw.ai
- **火一五记忆系统**: https://clawhub.ai/jobzhao15/huo15-memory-evolution
- **钉钉开放平台**: https://open-dev.dingtalk.com/

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>
