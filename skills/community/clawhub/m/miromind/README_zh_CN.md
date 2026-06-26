# 🔬 MiroMind Deep Research Skill

> 为 [OpenClaw](https://openclaw.ai) 打造的深度研究 Skill，调用 MiroMind 网页 (使用 playwright-mcp) 自动帮你完成 DeepResearch 任务.
> 
> MiroMind 使用他们最新推出的 MiroThinker-1.7（235B 参数大模型）对任意主题进行长链推理与多轮验证式深度研究，并自动保存完整 Markdown 报告。

[![Platform](https://img.shields.io/badge/platform-OpenClaw-blue)](https://openclaw.ai)
[![Model](https://img.shields.io/badge/model-MiroThinker--1.7%20235B-purple)](https://dr.miromind.ai)
[![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-green)](#)

---

## 功能亮点

- **一句话触发深度研究**：输入 `/miromind 你的问题` 即可启动研究
- **MiroThinker-1.7（235B）**：超大规模推理模型，长链思维链 + 多轮自我验证
- **URL 直接提交法**：无需点击按钮，通过 URL 参数直接提交研究任务，稳定可靠
- **异步轮询 + 实时反馈**：研究期间返回进度链接，支持在浏览器中实时查看
- **自动保存报告**：研究完成后自动生成 Markdown 报告文件，保存至本地
- **跨平台支持**：Windows / macOS / Linux 全平台兼容

---

## 前置依赖

| 依赖 | 说明 |
|------|------|
| [OpenClaw](https://openclaw.ai) | 运行环境 |
| `playwright-mcp` Skill | 浏览器自动化，用于控制 MiroMind 网站 |
| [MiroMind 账号](https://dr.miromind.ai) | 用于登录并使用 MiroThinker AI |

---

## 安装

```bash
# 1. 安装本 Skill
clawhub install miromind

# 2. 安装 Playwright MCP Skill（浏览器自动化依赖）
clawhub install playwright-mcp

# 3. 安装 Playwright 浏览器内核
npx playwright install chromium
```

---

## 配置

### 第一步：获取 MiroMind 账号

前往 [https://dr.miromind.ai](https://dr.miromind.ai) 注册账号。

### 第二步：配置凭据

打开 OpenClaw 配置文件：

```bash
openclaw config edit
```

在 `env` 节点中添加以下内容：

```json
{
  "env": {
    "MIROMIND_EMAIL": "your@email.com",
    "MIROMIND_PASSWORD": "your-password"
  }
}
```

### 第三步：重启 Gateway

```bash
openclaw gateway restart
```

> ⚠️ 未配置凭据时，Skill 会输出友好的引导提示，不会静默失败。

---

## 使用方法

```
/miromind [研究主题或问题]
```

### 示例

```bash
# 金融分析
/miromind 预测2026年黄金价格走势

# 科技研究
/miromind 调查量子计算领域的最新突破

# 公司分析
/miromind 分析英伟达最新财报的关键数据

# 新闻验证
/miromind 某个新闻事件的真实性调查

# 趋势预测
/miromind AI行业2026年的发展趋势
```

---

## 执行流程

```
用户输入 /miromind [问题]
       ↓
检查 MIROMIND_EMAIL / MIROMIND_PASSWORD 环境变量
       ↓
Spawn 子 Agent（隔离 Session，超时 15 分钟）
       ↓
子 Agent 执行：
  1. 打开 https://dr.miromind.ai/
  2. 检查登录状态，未登录则自动登录
  3. 通过 URL 参数直接提交研究任务
     → https://dr.miromind.ai/?noReleaseNotes&query=<编码后的问题>
  4. 捕获研究 Chat URL，立即返回给用户
  5. 每 10 秒轮询一次研究状态（最长等待 20 分钟）
  6. 研究完成 → 提取完整内容
  7. 保存 Markdown 报告到本地
       ↓
返回：研究摘要 + 本地报告路径 + Chat URL
```

---

## 输出说明

研究完成后，报告自动保存至：

```
~/.openclaw/workspace/skills/mirothinker/outputs/
└── mirothinker-<timestamp>.md
```

报告格式：

```markdown
# MiroMind Deep Research Report

**研究主题**: 你的问题
**研究时间**: 2026-03-20 12:34:56

---

（MiroThinker 完整研究内容）
```

---

## 技术说明

| 技术点 | 说明 |
|--------|------|
| URL 提交法 | 通过 `?noReleaseNotes&query=` 参数直接创建研究，绕过按钮点击的不稳定性 |
| 异步子 Agent | 使用 `sessions_spawn` 在独立 Session 中运行，不阻塞主会话 |
| 轮询策略 | 每 10 秒检查一次页面状态，最长等待 20 分钟 |
| 内容提取 | 使用 `page.evaluate()` 获取页面 `innerText`，兼容动态渲染内容 |
| 跨平台 | 在 Windows / macOS / Linux 上均通过测试 |

---

## 常见问题

**Q: 研究需要多长时间？**  
A: 通常 3–10 分钟，复杂问题可能更长。Skill 会实时返回 Chat URL，你可以在浏览器中查看进度。

**Q: 提交后没有跳转到 `/chat/` 页面怎么办？**  
A: 可能是网络问题或账号登录态失效，Skill 会自动报错提示，重新运行即可。

**Q: 报告保存在哪里？**  
A: 默认保存在 `~/.openclaw/workspace/skills/mirothinker/outputs/` 目录，Skill 执行结束后会输出完整路径。

**Q: 是否支持英文问题？**  
A: 支持，MiroThinker 支持中英文双语研究。

---

## 相关链接

- **MiroMind 官网**：[https://dr.miromind.ai](https://dr.miromind.ai)
- **OpenClaw 官网**：[https://openclaw.ai](https://openclaw.ai)
- **ClawHub Skill 市场**：[https://clawhub.ai](https://clawhub.ai)

---

## License

MIT
