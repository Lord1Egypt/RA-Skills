# Link Transcriber Skill

**✨ 一键把抖音 / 小红书链接变成总结、Todo 和推荐提醒时间**

**普通用户直接安装 skill 即可使用。**
**不需要本地部署，不需要安装 Python / ffmpeg，不需要自己提供任何平台凭证。**

所需的平台访问由发布者托管的 hosted service 在服务端处理。
**粘贴链接 → 直接返回总结、Todo List 和推荐提醒时间**，不废话、不复制一大堆原始文案

专为 OpenClaw / Codex 用户设计，极大降低内容创作者、矩阵运营者的采集成本。

## 🎯 核心优势

- **零配置使用**：用户不需要输入任何平台凭证
- **服务端处理访问**：链接由发布者托管的 hosted service 处理
- **直接推进执行**：默认生成总结、Todo List 和推荐提醒时间
- **支持平台**：抖音、小红书（持续新增中）
- **默认直接可用**：面向普通用户默认使用托管公开服务
- **高级可选**：开发者或高级用户才需要考虑自部署
- **可继续确认提醒**：OpenClaw 中确认时间后可直接接入原生 `cron` 提醒

## 🚀 快速安装

### 方法一：在 OpenClaw / Codex 中直接说（推荐）
```
请为我安装 link-transcriber
```

### 方法二：使用 ClawHub CLI
```bash
npx clawhub@latest --workdir ~/.qclaw --dir skills install link-transcriber --force
```

安装完成后即可直接使用，无需再配置本地 Python、ffmpeg、平台凭证或后端服务。

如果你使用的是 Codex 而不是 QClaw / OpenClaw，也可以安装到 Codex skills 目录：

```bash
npx clawhub@latest --workdir ~/.codex --dir skills install link-transcriber --force
```

## 📖 使用示例

**输入**：
```
分析这个小红书笔记：https://www.xiaohongshu.com/explore/732xxxxxx
```

**输出示例**：
```
【总结】
通过稳定站姿、平稳抛球和核心控制，这条内容强调“先把发球动作框架做稳”，再去追求速度和力量。

【Todo List】
1. 先固定一套发球准备站姿，连续练习 20 次不变形。
2. 单独训练抛球动作，确认落点和高度稳定。
3. 用慢动作完成完整挥拍，优先保证动作连贯。
4. 每次练习后记录最不稳定的一环，下次先针对它练 10 分钟。

【推荐提醒时间】
推荐提醒时间：今晚 21:00
```

**批量示例**：
```
批量分析下面这些链接并生成选题建议：
1. https://v.douyin.com/xxxx
2. https://www.xiaohongshu.com/explore/yyyy
```

## 🛠️ 如何工作（技术原理）

1. 用户输入链接 → Skill 解析平台和视频/笔记 ID
2. 由发布者托管的 hosted service 在服务端处理所需的平台访问
3. 调用公开稳定接口 `POST /public/transcriptions`
4. 轮询 `GET /public/transcriptions/{task_id}` 直到拿到最终 `summary_markdown`
5. 输出总结、Todo List 和推荐提醒时间

如果用户希望继续设置提醒，OpenClaw 可以在当前会话里确认最终时间，然后直接调用原生 `cron` 创建提醒任务。

所有敏感操作均在服务端完成，用户端零风险。

## ⚙️ 配置与部署

### 默认使用方式

对普通用户：

- 直接安装 `link-transcriber`
- 粘贴抖音或小红书链接
- 等待返回总结、Todo List 和推荐提醒时间
- 如需提醒，再在 OpenClaw 对话里确认最终时间

不要把 GitHub 仓库、Python 环境、ffmpeg 安装、平台凭证配置或本地后端启动，当成默认使用步骤。

### Public API Contract

这个 skill 当前只依赖两条公开接口：

```text
POST /public/transcriptions
GET /public/transcriptions/{task_id}
```

公开返回里已经包含最终 `summary_markdown`，skill 会在此基础上生成默认的总结、Todo List 和推荐提醒时间，所以不再把内部 `api/service/summaries` 暴露为对外契约。

### 环境变量（推荐设置）
```env
LINK_SKILL_API_BASE_URL=https://linktranscriber.store
LINK_SKILL_POLL_MAX_ATTEMPTS=60
LINK_SKILL_POLL_INTERVAL_SECONDS=1.0
```

### 开发者路径（可选）

只有在你明确想做开发、调试或自部署时，才需要关心本地 Python、ffmpeg、服务端环境变量和仓库代码。
这些不是普通终端用户使用 skill 的前置条件。

### 提醒协作方式

- `link-transcriber` 默认只负责生成内容理解结果和初步执行计划
- 最终提醒时间由 OpenClaw 当前对话继续和用户确认
- 确认后由 OpenClaw 原生 `cron` 创建主会话提醒
- 到点后提醒内容应复用已有 todo，而不是重新跑一次转写

## 🔒 安全说明

- skill 会把用户主动提供的链接发送到 `https://linktranscriber.store` 进行处理
- hosted service 不要求终端用户提供平台账号密码、平台凭证、钱包或支付信息
- 支持本地完全私有部署
- 对隐私特别敏感的场景，建议自行部署上游服务后再使用

## 📈 更新计划

- [ ] 支持快手、视频号、B站
- [ ] 批量处理 + 自动生成笔记草稿
- [ ] 一键导出 Markdown / Word
- [ ] 更多输出模板（爆款笔记结构、竞品分析等）
- [ ] 更稳定的 reminder-confirmation flow

## ⭐ 支持一下

如果你觉得这个 Skill 有帮助，欢迎：

- 点个 Star ⭐
- 在 ClawHub 页面留下评价
- 分享给其他 OpenClaw 用户

有任何问题或功能建议，欢迎在 Issues 中提出！

---

**作者**：bobobo2026  
**版本**：v0.1.21
**协议**：MIT
