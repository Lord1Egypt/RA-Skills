# 知识获取

知识获取 skill：接收链接或文本，自动完成内容解析、知识分类、Markdown 笔记生成，并可选归档到飞书云盘。

## 功能概览

### 核心功能
- **支持平台**：小红书、微信文章、知乎、B站、GitHub、普通网页（自动识别）
- **内容抽取**：标题、作者、发布时间、正文（不同平台字段可能有差异）
- **知识分类**：8大类别关键词分类（可在配置中调整）
- **笔记生成**：生成结构化 Markdown（含 trace_id）
- **飞书归档（可选）**：按 `{云盘空间名}/{分类}/{年}/{月}` 创建目录并上传 Markdown

## 配置说明（飞书云盘）

如需开启飞书云盘归档，请配置以下环境变量：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BASE_FOLDER_TOKEN`

临时设置（当前终端生效）：

```bash
export FEISHU_APP_ID="你的AppID"
export FEISHU_APP_SECRET="你的AppSecret"
export FEISHU_BASE_FOLDER_TOKEN="你的FolderToken"
```

如果你用 `openclaw gateway start`（LaunchAgent）方式启动网关，需要把这些环境变量写入 LaunchAgent 环境（否则网关进程读不到你终端的 export）。常见做法是在 `~/Library/LaunchAgents/ai.openclaw.gateway.plist` 中增加 `EnvironmentVariables`，然后执行 `openclaw gateway restart` 生效。

也可以用 `launchctl setenv` 给当前用户会话设置环境变量（重启网关后生效）：

```bash
launchctl setenv FEISHU_APP_ID "你的AppID"
launchctl setenv FEISHU_APP_SECRET "你的AppSecret"
launchctl setenv FEISHU_BASE_FOLDER_TOKEN "你的FolderToken"
openclaw gateway restart
```

仅测试“提取/分类/生成 Markdown”而不做飞书归档时，可设置：

```bash
export FEISHU_DISABLED=true
```

### 说明

- 不同平台的可提取字段取决于对应插件与页面可访问性（例如小红书短链可能返回兜底页）。

## 知识分类

8大知识类别及关键词：

1. **人工智能（AI）** - ai, 人工智能, 大模型, 机器学习, 深度学习, llm, 算法, 神经网络, agent, rag, chatgpt, gpt
2. **产品经理** - 产品经理, prd, 需求, 用户体验, 原型, 权限设计, 产品迭代, mvp, roadmap, 埋点, 数据分析
3. **经济（投资/股票/保险/加密货币）** - 股票, 基金, 投资, 保险, 加密货币, 比特币, 以太坊, 理财, 经济, 宏观, 资产配置, 财富管理
4. **心理学** - 心理学, 认知, 情绪, 人格, 潜意识, 行为, 共情, 心理, 动机, 压力, 心理学原理
5. **商业机会** - 创业, 商机, 商业模式, 变现, 流量, 增长, 商业机会, 客户开发, 渠道, b2b, b2c, 副业
6. **灵感** - 灵感, 想法, 创意, 感悟, 备忘, 金句, 启发, 洞察, 思考, 点子
7. **技术实践**（新增）- 代码, 编程, 开发, 技术, api, 开源, github, 项目, 框架, 部署, debug, bug
8. **学习成长**（新增）- 学习, 课程, 教程, 培训, 书单, 知识, 技能, 成长, 提升, 教育, 学习方法

## 环境变量

必需的环境变量：

```env
FEISHU_APP_ID=你的飞书应用ID
FEISHU_APP_SECRET=你的飞书应用秘钥
FEISHU_SPACE_NAME=快乐小狗空间
FEISHU_BASE_FOLDER_TOKEN=你的飞书云盘根文件夹token
```

可选的环境变量：

```env
# GitHub API（提升请求限制）
GITHUB_TOKEN=your_github_token

# Webhook 通知（预留）
WEBHOOK_URL=https://your-webhook-url.com

# 调试模式
DEBUG=true
```

## 安装

```bash
# 安装 Node.js 依赖
npm install

# 安装系统依赖
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg
```

## 使用方法

### 微信消息示例

#### 1. 处理链接内容
```
小红书这篇关于AI的文章很有启发：https://www.xiaohongshu.com/explore/xxx

知乎的热门讨论：https://www.zhihu.com/question/xxx

GitHub上的这个React Hook项目不错：https://github.com/xxx/react-hooks
```

#### 2. 处理纯文本
```
今天学习了如何设计一个可扩展的微服务架构，需要考虑服务发现、配置管理、熔断降级等方面
```

#### 3. 获取指令
```
获取知乎 - 获取知乎热门内容
获取GitHub: react - 搜索React相关项目
获取B站: 产品经理 - 搜索产品经理教程
```

### 编程接口

主入口：`main(input, context)`

- `input`：微信消息文本，可包含多个链接和文本
- `context`：可选字段
  - `wechat_user`：微信用户名
  - `lark_receive_id`：飞书 open_id（用于通知）

示例：

```js
const { main } = require('./index');

main('https://mp.weixin.qq.com/s/xxx\nhttps://github.com/org/repo', {
  wechat_user: 'zhangsan',
  lark_receive_id: 'ou_xxx'
}).then(console.log);
```

## 运行测试

```bash
# 运行所有测试
npm test

# 运行覆盖率测试
npm run test:coverage

# 运行集成测试
npm run test:integration

# 监视模式
npm run test:watch
```

## 模板格式

### 标准知识笔记模板

```markdown
# 文章标题+20240113

## 分类标签
- 人工智能（AI）
- 置信度：92%
- 平台：zhihu

## 关键摘要
- 核心观点1
- 核心观点2
- 核心观点3

## 原文出处与作者
- 原文链接：https://zhihu.com/question/xxx
- 作者：作者名
- 发布时间：2024-01-13

## 媒体资源
- 图片：url1
- 视频：url1

## 思考与行动清单
- 提炼 1 个可执行实验并在 24 小时内验证
- 将结论同步到周复盘并补充下一步指标

## 分类依据日志
- trace_id：dog-16420xxxx-abc1
- 命中关键词：ai、大模型
```

### 视频内容模板（B站/抖音）

```markdown
# 视频标题+20240113

## 分类标签
- 技术实践
- 置信度：95%
- 平台：bilibili

## 关键摘要
- 视频核心观点1
- 视频核心观点2
- 视频核心观点3

## 原文出处与作者
- 原文链接：https://www.bilibili.com/video/BVxxx
- 作者：UP主名
- 发布时间：2024-01-13

## 视频信息
- 时长：58秒
- 平台：bilibili
- 播放量：10000+

## 视频字幕
- [00:00] 这是视频开头内容
- [00:15] 这是中间内容
- [00:45] 这是结尾内容

## 思考与行动清单
- 提炼 1 个可执行实验并在 24 小时内验证
- 将结论同步到周复盘并补充下一步指标

## 分类依据日志
- trace_id：dog-16420xxxx-abc1
- 命中关键词：代码、开发
```

### GitHub仓库模板

```markdown
# 项目名称+20240113

## 分类标签
- 技术实践
- 置信度：98%
- 平台：github

## 关键摘要
- 这是一个React Hooks的最佳实践项目
- 提供了多种常用Hook的实现
- 包含完整的测试用例

## 原文出处与作者
- 原文链接：https://github.com/xxx/react-hooks
- 作者：xxx
- 发布时间：2024-01-13

## 项目信息
- 语言: JavaScript
- Stars: 5000
- Forks: 800
- Issues: 20
- 主题: react, hooks, best-practice

## README 预览
React Hooks 最佳实践集合...

## 思考与行动清单
- 提炼 1 个可执行实验并在 24 小时内验证
- 将结论同步到周复盘并补充下一步指标

## 分类依据日志
- trace_id：dog-16420xxxx-abc1
- 命中关键词：github, 开源, react
```

## 配置说明

### 基础配置参数

```js
// 在 index.js 中可以调整
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 缓存24小时
const RETRY_TIMES = 3; // 重试次数
const MAX_VIDEO_SECONDS = 60; // 最大视频时长
const TIMEOUT_MS = 30000; // 默认超时时间
const MAX_CONCURRENCY = 3; // 最大并发数
```

### 安全规则

```js
const FORBIDDEN_PATTERNS = [
  /色情|裸聊|约炮|成人视频/i,
  /恐怖袭击|制爆|枪支交易|暴力极端/i,
  /颠覆|煽动分裂|敏感政治/i,
  /赌博|博彩|彩票/i
];
```

## 系统架构

```
输入处理 → 内容提取 → 安全检查 → 分类处理 → 生成笔记 → 飞书保存
    ↓           ↓           ↓           ↓           ↓          ↓
  微信消息    多平台解析    敏感词过滤    AI智能分类   模板引擎    自动归档
```

详细流程图请查看 `happy-dog-workflow.html`（使用浏览器打开）

## 性能指标

| 指标 | 值 |
|------|----|
| 平均处理时间 | < 10秒 |
| 并发处理能力 | 3个/批次 |
| 缓存命中率 | > 80% |
| 分类准确率 | > 90% |
| 系统可用性 | 99.5% |

## 部署建议

- **系统依赖**：Node.js >= 14.0.0、Chrome/Chromium（小红书抓取）、ffmpeg
- **进程管理**：建议通过进程管理器守护运行（pm2/systemd）
- **网络配置**：在网关层做 HTTPS、限流、鉴权
- **安全配置**：将飞书凭据放入密钥管理系统，避免明文

### Docker 部署（可选）

```dockerfile
FROM node:16-alpine

# 安装 ffmpeg
RUN apk add --no-cache ffmpeg

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .

CMD ["node", "index.js"]
```

## 故障排查

### 常见问题

1. **小红书抓取失败**
   - 确保系统已安装 Chrome/Chromium
   - 检查网络连接和代理设置

2. **视频处理失败**
   - 确认 ffmpeg 已正确安装
   - 检查视频URL是否可访问

3. **飞书上传失败**
   - 检查飞书应用权限配置
   - 确认 folder_token 是否正确
   - 若只想测试“提取/分类/生成 Markdown”，可设置 `FEISHU_DISABLED=true` 跳过飞书归档

4. **分类不准确**
   - 调整关键词配置
   - 检查置信度阈值设置

## 更新日志

### v2.0.0 (2024-01-13)
- ✨ 新增知乎、B站、GitHub平台支持
- ✨ 新增获取指令功能
- ✨ 新增技术实践和学习成长分类
- ✨ 增强内容提取和模板引擎
- ⚡ 优化并发处理性能
- 🐛 修复已知问题

### v1.0.0
- 🎉 初始版本发布
- ✨ 支持小红书、微信文章、抖音
- ✨ 8大分类系统
- ✨ 飞书云盘集成（可选）

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

---

*快乐小狗信息整理器 - 让知识管理更高效*
