# Morning Radar - 晨间资讯简报

通用资讯自动收集与推送工具，支持自定义关键词和主题

## 功能

- 使用百度AI搜索获取最新资讯
- 自定义关键词和搜索主题
- 自动过滤、去重、排序
- 生成Markdown格式简报
- 定时推送到飞书

## 安装

```bash
# 1. 复制skill到OpenClaw skills目录
cp -r skills/morning-radar ~/.openclaw/skills/

# 2. 配置环境变量
export BAIDU_API_KEY="your-baidu-api-key"
export FEISHU_APP_ID="your-feishu-app-id"
export FEISHU_APP_SECRET="your-feishu-app-secret"
export FEISHU_RECEIVER_OPEN_ID="your-open-id"

# 3. （可选）自定义搜索主题
export RADAR_QUERIES="AI人工智能,科技新闻,行业动态"
export RADAR_KEYWORDS="大模型,科技,创新"

# 4. 设置定时任务
openclaw cron add --name "morning-radar" --schedule "0 7 * * *" --command "morning-radar"
```

## 配置

### 方式1：环境变量（推荐）

```bash
# 必需
export BAIDU_API_KEY="your-baidu-api-key"
export FEISHU_APP_ID="cli-xxxxx"
export FEISHU_APP_SECRET="your-secret"
export FEISHU_RECEIVER_OPEN_ID="ou-xxxxx"

# 可选 - 自定义搜索
export RADAR_QUERIES="AI人工智能,科技新闻,行业动态,财经资讯"
export RADAR_KEYWORDS="大模型,科技,创新,投资,市场"
export RADAR_MAX_RESULTS="10"
export RADAR_MAX_ITEMS="15"

# 可选 - 自定义标题
export RADAR_TITLE="🌅 我的晨间资讯简报"
export RADAR_SOURCE_NAME="自定义搜索"
```

### 方式2：配置文件

复制 `config.example.json` 为 `config.json`：

```json
{
  "baidu": {
    "apiKey": "your-baidu-api-key"
  },
  "feishu": {
    "appId": "cli-xxxxx",
    "appSecret": "your-secret",
    "receiverOpenId": "ou-xxxxx"
  },
  "search": {
    "queries": ["AI人工智能", "科技新闻", "行业动态"],
    "keywords": ["大模型", "科技", "创新"],
    "maxResults": 10
  },
  "output": {
    "title": "🌅 我的晨间资讯简报",
    "sourceName": "自定义搜索",
    "maxItems": 15
  }
}
```

## 使用场景示例

### 场景1：AI资讯（默认）
```bash
export RADAR_QUERIES="AI人工智能,大模型,智能体"
export RADAR_KEYWORDS="AI,大模型,Agent,OpenAI,GPT"
node index.js
```

### 场景2：财经资讯
```bash
export RADAR_QUERIES="股市行情,投资理财,宏观经济"
export RADAR_KEYWORDS="A股,基金,投资,理财,市场"
export RADAR_TITLE="📈 晨间财经简报"
node index.js
```

### 场景3：科技资讯
```bash
export RADAR_QUERIES="科技新闻,互联网,新产品发布"
export RADAR_KEYWORDS="科技,互联网,产品,创新,发布"
export RADAR_TITLE="🔬 晨间科技简报"
node index.js
```

### 场景4：综合资讯
```bash
export RADAR_QUERIES="今日热点,社会新闻,国际动态"
export RADAR_KEYWORDS="热点,新闻,社会,国际"
export RADAR_TITLE="📰 晨间综合简报"
node index.js
```

## 获取配置信息

### 1. 百度API Key

1. 访问 [百度千帆平台](https://qianfan.baidubce.com)
2. 注册/登录百度账号
3. 创建应用，获取API Key

### 2. 飞书应用配置

1. 访问 [飞书开放平台](https://open.feishu.cn)
2. 创建企业自建应用
3. 获取 **App ID** 和 **App Secret**

### 3. 获取 Receiver Open ID

**方式A：飞书管理后台**
1. 登录 [飞书管理后台](https://admin.feishu.cn)
2. 进入「组织架构」→「成员与部门」
3. 找到自己的账号，复制 **Open ID**

**方式B：API查询**
```bash
curl -X GET "https://open.feishu.cn/open-apis/contact/v3/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 使用

### 手动运行

```bash
# 使用环境变量
morning-radar

# 或使用配置文件
morning-radar /path/to/config.json
```

### 定时运行

```bash
# 添加到cron（每天7:00）
openclaw cron add morning-radar "0 7 * * *"

# 查看定时任务
openclaw cron list

# 删除定时任务
openclaw cron remove morning-radar
```

## 输出格式

```
🌅 晨间资讯简报 - 2026/3/13
━━━━━━━━━━━━━━━━━━━━━━

1. 【来源】
标题：xxx
链接：https://xxx.com/xxx
日期：2026-03-13
摘要：一句话要点
优先级：🔴高

...

━━━━━━━━━━━━━━━━━━━━━━
💡 共 X 条资讯
⏰ 每日早7点自动推送
```

## 环境变量清单

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `BAIDU_API_KEY` | ✅ | - | 百度API Key |
| `FEISHU_APP_ID` | ✅ | - | 飞书App ID |
| `FEISHU_APP_SECRET` | ✅ | - | 飞书App Secret |
| `FEISHU_RECEIVER_OPEN_ID` | ✅ | - | 接收者Open ID |
| `RADAR_QUERIES` | ❌ | AI相关 | 搜索查询，逗号分隔 |
| `RADAR_KEYWORDS` | ❌ | AI关键词 | 过滤关键词，逗号分隔 |
| `RADAR_MAX_RESULTS` | ❌ | 10 | 每次搜索最大结果数 |
| `RADAR_MAX_ITEMS` | ❌ | 15 | 最终输出最大条数 |
| `RADAR_TITLE` | ❌ | 晨间资讯简报 | 消息标题 |
| `RADAR_SOURCE_NAME` | ❌ | 百度智能搜索 | 来源名称 |

## 依赖

- Node.js 18+
- OpenClaw 2025+
- 百度千帆AI搜索API Key
- 飞书开放平台应用

## 隐私说明

本Skill不会收集或存储任何用户数据。所有配置信息仅保存在用户本地。

## 许可证

MIT
