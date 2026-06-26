# 一个skills在OpenClaw上丝滑创建多个独立的飞书机器人Agent

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

仓库地址：https://github.com/itzhouq/openclaw-new-agent

介绍视频：https://www.bilibili.com/video/BV16fXLBkEwo

演示视频：https://www.bilibili.com/video/BV1cUXaBsEM1

## 痛点：官方配置太复杂，容易改错

在 OpenClaw 上新增一个独立的飞书机器人，官方流程需要：

1. **手动编辑 `openclaw.json`** — 复杂的嵌套 JSON，改错一点就崩
2. **多账号模式配置繁琐** — 需要理解 `channels.feishu.accounts` 的结构
3. **allowFrom 白名单容易遗漏** — 配错了消息就收不到
4. **备份恢复麻烦** — 改坏了不知道怎么回滚
5. **Gateway 重启时机不确定** — 不知道什么时候配置生效

**核心痛点**：配置改错一次，可能需要花半小时排查问题。

---

## 解决方案

`openclaw-new-agent` Skill 核心能力：

- ✅ **自动备份** — 每次变更前自动备份，坏了随时回滚
- ✅ **分步骤引导** — 每一步做什么清清楚楚，不会迷路
- ✅ **allowFrom 自动获取** — 不需要用户记 open_id，发条消息自动识别
- ✅ **配置 patch 化** — 只改需要改的部分，不碰其他配置
- ✅ **验证三步曲** — 创建完自动确认是否成功

---

## 一、安装

### 安装方式一：clawhub 安装 （推荐）

```bash
# 执行下面命令或者告诉Openclaw：通过clawhub 安装 openclaw-new-agent 这个 skills。
npx clawhub@latest install openclaw-new-agent
# 安装完成实际会下载到 skills 目录下： ~/.openclaw/workspace/skills
```

### 安装方式二：手动下载

```bash
git clone https://github.com/itzhouq/openclaw-new-agent.git ~/.openclaw/workspace/skills
# 手动安装完最好重启下网关，在终端执行：openclaw gateway restart
```

### 安装方式三：联系我发你安装包

如果确实安装失败或者网络问题无法下载，可以联系我发你，有问题也欢迎call我或者提交issue。

<img src="assets/wechat.png" alt="wechat" width="25%" height="25%" />

## 二、一键创建飞书机器人

👉 https://open.feishu.cn/page/openclaw?form=multiAgent

直接生成包含 WebSocket 事件订阅的模板应用，无需手动配置权限。生成完后显示 AppId 和 appSecret 页面不要关闭后面要用。

<img src="https://github.com/itzhouq/openclaw-new-agent/blob/master/assets/image-20260326175903868.png" alt="创建飞书机器人" style="zoom:50%;" />

<img src="https://github.com/itzhouq/openclaw-new-agent/blob/master/assets/image-20260326180114565.png" alt="创建飞书机器人2" style="zoom:50%;" />

## 三：确认基本信息

直接在现有飞书机器人聊天界面告诉 AI 助手："创建一个新机器人：[名称]，[用途]"

示例："创建一个新机器人：码字精，用于写作辅助"

<img src="https://github.com/itzhouq/openclaw-new-agent/blob/master/assets/image-20260326180008946.png" alt="确认机器人" style="zoom:50%;" />

AI 会自动询问：App ID & App Secret（没有？点击上面链接创建）

## 四、提供飞书机器人的信息

核心是把这两个信息发给机器人。机器人名称、职责、工作区文件夹名称等是可选调整项目，默认即可。

<img src="https://github.com/itzhouq/openclaw-new-agent/blob/master/assets/image-20260326180234755.png" alt="确认机器人" style="zoom:100%;" />

到这里，Openclaw 已经在自动创建新的 Agent，备份，修改配置文件。下面列举的是 AI 做的事你不需要改动。

- AI 自动备份文件：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.before{agentId}bak`
- AI 自动创建新工作区：`~/.openclaw/`workspace-{name}/ 
- AI 自动使用 `gateway config.patch` 局部更新，**不会覆盖你的其他配置**。

稍微等待一会儿，等待创建完成。



## 五、新机器人创建完成

你会收到一条类似消息。

<img src="assets/image-20260329015924649.png" alt="image-20260329015924649" width="50%" height="50%" />

可能稍微有点出入（跟具体你使用的模型有关系）。

你只需要关心的是：向新创建的机器人发个消息。

## 六、给新机器人发送消息

飞书有个通知，你点进去就能跟新机器人对话。

<img src="assets/image-20260329020142441.png" alt="image-20260329020142441" width="50%" height="50%" />

随便跟新机器人发个消息。这部分目的是让机器人自动配置 allowFrom 。

**如果这一步失败（发了很多次消息也没收到回复），看后续的常见问题。**

---

## 七、验证

稍微等待一会儿，给主机器人（不是新的）发个消息：我已经向新机器人发了消息，完成后后续配置。

<img src="https://github.com/itzhouq/openclaw-new-agent/blob/master/assets/image-20260326180334922.png" alt="验证" style="zoom:50%;" />

类似这样的消息，说明主机器人完成了配置。

如果到这一步你给新的机器人发消息能得到回复，那么恭喜你完成了多机器人配置。

你可以继续创建更多的 Agent。如果能帮到你，帮我打个 star 非常感谢！。

如果你遇到机器人没回复，继续往后看（模型执行有一定的随机性）。

<img src="assets/image-20260329021244794.png" alt="image-20260329021244794" width="50%" height="50%" />

## 常见问题：新机器人不回你

大概率是新机器人的 allowlist 没有配置对。在终端命令行执行：`openclaw logs --follow`

再给新的机器人随便发个消息。观察终端，如果能看到下面的关键信息：

![image-20260329021611819](assets/image-20260329021611819.png)

复制这个 OU 开头的标识码手动放在 `~/openclaw/openclaw.json`中。

新启动一个终端执行：`cd .openclaw && open .` 最终打开 `openclaw.json`

![image-20260329022140372](assets/image-20260329022140372.png)

操作：

![image-20260329022431694](assets/image-20260329022431694.png)

保存后终端中执行：`openclaw gateway restart` 重启网关。

再给新机器人发送消息，能收到回复就是成功了！

如果还是没有成功，可以参考演示视频重试。再有问题你就联系我看看吧。

## 常见问题：新机器人不回你老机器人也挂了

懒得写，看我演示视频介绍怎么排查吧。

## 其他问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 消息被拒绝 "not in DM allowlist" | 发送者 ID 不在白名单 | AI 自动从日志获取并补充 |
| 配置后没反应 | Gateway 未重启 | 等待 2-3 秒 |
| 消息发到了别的机器人 | 账号混淆 | 确认用正确的机器人对话 |
| 飞书机器人没响应 | 未开启事件订阅 | 用一键创建链接 |



## 发布日志

### v1.2.0 (2026-03-29)

- 说明文档&常见问题

### v1.1.0 (2026-03-28)

- 安装方式更新

---

### v1.0.0 (2026-03-26)
- 初始版本
- 支持多飞书机器人创建
- 自动备份和白名单获取
- 完整流程引导

---

## 许可证

MIT License

---

## 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub Skill 市场](https://clawhub.com)
- [飞书开放平台](https://open.feishu.cn/)
