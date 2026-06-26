---
name: miromind
description: "MiroMind Deep Research Skill - 使用 MiroThinker AI 进行深度研究。触发词：/miromind。当用户想对某个主题进行深度研究时使用。"
metadata:
  {
    openclaw:
      {
        emoji: "🔬",
        os: ["linux", "darwin", "win32"],
        skills: ["playwright-mcp"],
        requires: {
          bins: ["playwright-mcp"],
          env: ["MIROMIND_EMAIL", "MIROMIND_PASSWORD"]
        },
        primaryEnv: "MIROMIND_EMAIL",
        install: [
          {
            id: "skill-playwright-mcp",
            kind: "skill",
            label: "Install Playwright MCP Skill (browser automation)"
          }
        ]
      }
  }
---

# MiroMind Deep Research Skill

> 🔬 使用 MiroThinker AI 进行深度研究，支持长链推理与多轮验证。

**官网：** https://dr.miromind.ai/  
**模型：** MiroThinker-1.7 (235B)

---

## 安装 (Installation)

```bash
# 1. 安装 Playwright MCP Skill
clawhub install playwright-mcp

# 2. 确保 Playwright 浏览器已安装
npx playwright install chromium
```

---

## 配置 (Configuration)

### ⚠️ 首次使用必须配置

**OpenClaw 推荐使用 `openclaw.json` 的 `env` section 存储凭据。**

### 配置步骤

1. 编辑 OpenClaw 配置文件：

```bash
# 打开 openclaw.json
openclaw config edit
```

2. 在 `env` section 中添加凭据：

```json
{
  "env": {
    "MIROMIND_EMAIL": "your@email.com",
    "MIROMIND_PASSWORD": "your-password"
  }
}
```

3. 重启 OpenClaw Gateway：

```bash
openclaw gateway restart
```

### 首次配置提示

当检测到环境变量未配置时，显示以下提示：

```
🔬 首次使用 MiroMind Skill 需要配置！

请在 openclaw.json 中添加以下配置：

{
  "env": {
    "MIROMIND_EMAIL": "你的邮箱",
    "MIROMIND_PASSWORD": "你的密码"
  }
}

配置后重启 gateway: openclaw gateway restart
```

---

## 使用方法 (Usage)

```
/miromind [研究主题或问题]
```

### 示例

```bash
/miromind 预测2026年黄金价格走势
/miromind 分析英伟达最新财报的关键数据
/miromind 调查量子计算领域的最新突破
```

---

## 无输入提示 (Tips)

当用户只触发命令但没有输入研究主题时，显示：

```
🔬 MiroMind Deep Research Skill

使用 MiroThinker AI 进行深度研究！

📚 可研究的主题示例：
   • 金融分析：「比特币2026年价格走势」「黄金走势预测」
   • 新闻验证：「某事件是真的吗？」「调查某个新闻的真实性」
   • 趋势预测：「AI行业未来发展趋势」「某个技术的发展前景」
   • 学术研究：「量子计算最新突破」「某个科学领域的进展」
   • 商业分析：「某公司财务状况分析」「市场竞争格局研究」

🚀 使用方法：
   /miromind [你的研究问题]

⚡ 注意：研究过程可能需要 3-10 分钟，请耐心等待~
```

---

## 执行流程 (Execution Flow)

```
1. 你触发命令
          ↓
2. 检查环境变量配置
          ↓
3. Spawn sub-agent (isolated session)
          ↓
4. Sub-agent:
   a. 使用 browser tool 打开网站
   b. 检查登录状态（如未登录则登录）
   c. 使用 URL 直接提交研究（核心方法！）
   d. 获取 chat URL 并返回给 main session
   e. 轮询检查研究状态
   f. 研究完成 → 提取结论 + 保存报告
          ↓
5. 返回 chat URL 给用户，让他们可以查看进度
          ↓
6. 研究完成 → 返回结论 + 报告文件路径
```

---

## 🔑 核心发现：URL 直接提交法

**关键发现**：MiroMind 网站可以通过 URL 参数直接提交研究，避免按钮点击问题。

**格式**：
```
https://dr.miromind.ai/?noReleaseNotes&query=<URL编码的研究问题>
```

**示例**：
```
https://dr.miromind.ai/?noReleaseNotes&query=Claude%20Sonnet%205%20%E5%92%8C%E6%96%B0%E5%8A%9F%E8%83%BD
```

---

## Sub-Agent 执行流程

### Spawn 参数

```javascript
sessions_spawn({
  task: "执行 MiroMind 深度研究...",
  runtime: "subagent",
  runTimeoutSeconds: 900,  // 15 分钟
  mode: "run"  // 或 "session"
})
```

### Sub-Agent 返回值

**必须返回以下信息：**

```javascript
{
  sessionKey: "xxx",        // sub-agent session key
  chatUrl: "https://dr.miromind.ai/chat/019d0712-904f-7282-b0b5-1b6a438443b1",
  query: "研究问题",
  status: "running"  // 或 "completed"
}
```

**chatUrl 格式：**
```
https://dr.miromind.ai/chat/<UUID>
```
从 page.url() 获取。

**⚠️ 重要**：sub-agent spawn 时会返回 sessionKey，spawn 完成后立即返回 chatUrl 给 main session，让用户可以查看进度。

---

## 完整执行步骤

### 步骤 1：检查环境变量

```javascript
const email = process.env.MIROMIND_EMAIL;
const password = process.env.MIROMIND_PASSWORD;

if (!email || !password) {
  return { error: "❌ 请先配置环境变量 MIROMIND_EMAIL 和 MIROMIND_PASSWORD" };
}
```

### 步骤 2：打开网站

```javascript
await browser.navigate("https://dr.miromind.ai/");
await page.waitForTimeout(2000);
```

### 步骤 3：检查登录状态

```javascript
// 查找右上角用户名按钮（不写死用户名）
// 中英文双重检查
const loginBtnZh = await page.$('button:has-text("登录")');
const loginBtnEn = await page.$('button:has-text("Sign in")');
const loginBtn = loginBtnZh || loginBtnEn;

if (loginBtn) {
  // 需要登录
  const email = process.env.MIROMIND_EMAIL;
  const password = process.env.MIROMIND_PASSWORD;
  // ... 登录逻辑
} else {
  // 已登录
}
```

### 步骤 4：使用 URL 提交研究（核心！）

```javascript
// 构建 URL
const query = encodeURIComponent("你的研究问题");
const submitUrl = `https://dr.miromind.ai/?noReleaseNotes&query=${query}`;

// 导航到 URL
await page.goto(submitUrl);
await page.waitForTimeout(3000);

// 验证 URL 变化（表示成功创建研究）
const currentUrl = page.url();
if (!currentUrl.includes("/chat/")) {
  throw new Error("研究提交失败");
}

// URL 应该是类似：/chat/019d0705-xxx-xxx
// 这个 URL 就是 chatUrl，需要返回给 main session
const chatUrl = page.url(); // 例如: https://dr.miromind.ai/chat/019d0712-904f-7282-b0b5-1b6a438443b1
```

### 步骤 5：轮询等待研究完成

```javascript
const startTime = Date.now();
const maxWait = 20 * 60 * 1000; // 20 分钟

while (Date.now() - startTime < maxWait) {
  const status = await page.evaluate(() => {
    const bodyText = document.body.innerText;
    
    // 运行中
    if (bodyText.includes("任务在后台运行")) {
      return "running";
    }
    
    // 完成 - 查找"显示思考过程 总结"按钮
    const completeBtn = document.querySelector("button:has-text('显示思考过程')");
    if (completeBtn) {
      return "complete";
    }
    
    return "unknown";
  });
  
  if (status === "complete") {
    console.log("研究完成！");
    break;
  }
  
  console.log("研究进行中...");
  await page.waitForTimeout(10000); // 每 10 秒检查
}
```

### 步骤 6：提取研究结果

```javascript
// 点击"显示思考过程 总结"展开完整内容（如有）
const showBtn = await page.$("button:has-text('显示思考过程')");
if (showBtn) {
  await showBtn.click();
  await page.waitForTimeout(2000);
}

// 提取主内容
const content = await page.evaluate(() => {
  const main = document.querySelector("main main") || document.querySelector("main");
  return main ? main.innerText : "";
});

// 保存报告
const filename = `mirothinker-${Date.now()}.md`;
const filepath = path.join(outputDir, filename);

const report = `# MiroMind Deep Research Report

**研究主题**: ${query}
**研究时间**: ${new Date().toLocaleString()}

---

${content}
`;

fs.writeFileSync(filepath, report);
return filepath;
```

---

## 完整代码模板

```javascript
async function runMiroResearch(query) {
  // 1. 检查环境变量
  const email = process.env.MIROMIND_EMAIL;
  const password = process.env.MIROMIND_PASSWORD;
  
  if (!email || !password) {
    return { error: "请配置 MIROMIND_EMAIL 和 MIROMIND_PASSWORD 环境变量" };
  }
  
  // 2. 打开网站
  await page.goto("https://dr.miromind.ai/");
  await page.waitForTimeout(2000);
  
  // 3. 检查登录状态（如需要则登录）
  // ...登录逻辑...
  
  // 4. 使用 URL 提交研究
  const encodedQuery = encodeURIComponent(query);
  const submitUrl = `https://dr.miromind.ai/?noReleaseNotes&query=${encodedQuery}`;
  await page.goto(submitUrl);
  await page.waitForTimeout(3000);
  
  // 5. 验证成功
  if (!page.url().includes("/chat/")) {
    return { error: "研究提交失败" };
  }
  
  // 6. 轮询等待完成
  await pollForCompletion(page);
  
  // 7. 提取结果
  const content = await extractContent(page);
  
  // 8. 保存
  const filepath = await saveReport(query, content);
  
  return { success: true, filepath, content };
}
```

---

## 目录结构

```
~/.openclaw/workspace/skills/mirothinker/
├── SKILL.md              # 本文件
├── outputs/              # 研究结果
│   └── *.md             # 完整 Markdown 报告
└── session/             # Session 持久化
    └── cookies.json     # Cookies 数据（可选）
```

---

## 技术要点

- **URL 提交法**：直接用 URL 参数提交，绕过按钮点击问题
- **noReleaseNotes 参数**：跳过发布说明弹窗
- **轮询检查**：每 10 秒检查一次状态
- **超时处理**：20 分钟超时
- **提取内容**：使用 page.evaluate() 获取 innerText
