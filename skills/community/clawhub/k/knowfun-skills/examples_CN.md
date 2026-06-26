# Knowfun.io API 使用示例

[English](examples.md) | 简体中文

使用 Knowfun.io API 技能的综合示例。

## 设置

首先，设置你的 API key：
```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"
```

或创建 `.env` 文件：
```bash
echo 'KNOWFUN_API_KEY="kf_your_api_key_here"' >> .env
```

---

## 示例 1：创建简单课程

从文本创建课程：

```bash
/knowfun create course "Python 编程入门：Python 是一种高级编程语言，以其简单性和可读性而闻名。"
```

预期输出：
```
✅ 任务创建成功！
任务 ID: c3199fb3-350b-4981-858d-09b949bfae88
状态: pending
请求 ID: req_1234567890

使用以下命令检查状态：/knowfun status c3199fb3-350b-4981-858d-09b949bfae88
```

---

## 示例 2：从 URL 创建课程

从 PDF 文档创建课程：

```bash
/knowfun create course https://example.com/machine-learning-basics.pdf
```

---

## 示例 3：创建自定义风格的海报

创建具有特定样式的海报：

```bash
/knowfun create poster "气候变化：全球气温上升导致极地冰盖以惊人的速度融化。"
```

然后配置自定义选项（Claude 会提示这些）：
- 用途：信息图
- 风格：手绘
- 宽高比：16:9

---

## 示例 4：创建互动游戏

创建互动学习游戏：

```bash
/knowfun create game "学习 JavaScript：变量、函数和循环"
```

游戏类型将默认为"interactive"，提供动画演示风格。

---

## 示例 5：创建纪录片风格视频

创建纪录片风格的视频：

```bash
/knowfun create film "互联网的历史：从 ARPANET 到万维网"
```

---

## 示例 6：带完整配置的高级课程创建

直接使用 curl（Claude 可以帮助构建这个）：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-ml-intro-001",
    "taskType": "course",
    "material": {
      "text": "机器学习简介：ML 是 AI 的一个子集...",
      "type": "text"
    },
    "config": {
      "course": {
        "contentStyle": "detailed",
        "contentLanguage": "zh",
        "explainLanguage": "zh",
        "voiceType": "professional",
        "ttsStyle": "classroom"
      }
    },
    "language": "zh"
  }'
```

---

## 示例 7：检查任务状态

检查正在运行的任务状态：

```bash
/knowfun status c3199fb3-350b-4981-858d-09b949bfae88
```

预期输出：
```
📊 任务状态
任务 ID: c3199fb3-350b-4981-858d-09b949bfae88
状态: processing
进度: 45%
当前步骤: 生成幻灯片

创建于: 2026-03-01 10:00:00
```

---

## 示例 8：获取完整任务详情

获取包括结果的完整详情：

```bash
/knowfun detail c3199fb3-350b-4981-858d-09b949bfae88
```

已完成课程的预期输出：
```
✅ 任务完成！

任务 ID: c3199fb3-350b-4981-858d-09b949bfae88
类型: course
状态: completed

📚 课程详情：
- 标题: Python 编程入门
- URL: https://oss.knowfun.io/courses/xxx.html
- 幻灯片: 12
- 总时长: 3 分钟
- 封面: https://oss.knowfun.io/covers/xxx.png

💰 已使用积分: 100

⏱️ 时间线：
- 创建于: 2026-03-01 10:00:00
- 完成于: 2026-03-01 10:03:00
- 时长: 3 分钟
```

---

## 示例 9：列出最近的任务

列出你最近的任务：

```bash
/knowfun list
```

预期输出：
```
📋 最近的任务

1. 课程："Python 编程入门"
   ID: c3199fb3-350b-4981-858d-09b949bfae88
   状态: completed ✅
   创建于: 2026-03-01 10:00:00

2. 海报："气候变化事实"
   ID: a1b2c3d4-5678-90ab-cdef-1234567890ab
   状态: processing ⏳
   创建于: 2026-03-01 09:45:00

3. 游戏："学习 JavaScript"
   ID: f1e2d3c4-b5a6-9788-6543-210fedcba987
   状态: completed ✅
   创建于: 2026-03-01 09:30:00
```

---

## 示例 10：检查积分余额

检查你的可用积分：

```bash
/knowfun credits
```

预期输出：
```
💰 积分余额

可用: 1,000 积分
总获得: 1,500 积分
总使用: 400 积分
锁定: 100 积分

💡 定价：
- 课程: 100 积分
- 海报: 100 积分
- 游戏: 100 积分
- 视频: 100 积分

获取更多积分: https://www.knowfun.io/api-platform
```

---

## 示例 11：获取配置架构

获取所有可用的配置选项：

```bash
/knowfun schema
```

这会返回每种任务类型的所有可用选项的完整架构。

---

## 示例 12：创建所有选项的海报

创建高度自定义的海报：

使用技能（Claude 会构建 curl 命令）：
```bash
/knowfun create poster "AI 革命" --usage marketing --style photorealistic --ratio 16:9
```

或直接使用 curl：
```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "poster-ai-rev-001",
    "taskType": "poster",
    "material": {
      "text": "AI 革命：人工智能如何改变行业",
      "type": "text"
    },
    "config": {
      "poster": {
        "usage": "marketing",
        "style": "photorealistic",
        "aspectRatio": "16:9",
        "posterTitle": "AI 革命"
      }
    }
  }'
```

---

## 示例 13：创建自定义风格海报

创建具有自定义风格的海报：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "poster-custom-001",
    "taskType": "poster",
    "material": {
      "text": "现代 Web 开发：React、Vue 和 Angular",
      "type": "text"
    },
    "config": {
      "poster": {
        "usage": "infographic",
        "style": "custom",
        "customStylePrompt": "极简现代设计，柔和的色彩和几何形状",
        "aspectRatio": "1:1"
      }
    }
  }'
```

---

## 示例 14：创建基于故事的游戏

创建故事驱动的游戏：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "game-story-001",
    "taskType": "game",
    "material": {
      "text": "古埃及：了解金字塔、法老和象形文字",
      "type": "text"
    },
    "config": {
      "game": {
        "gameType": "story"
      }
    }
  }'
```

---

## 示例 15：创建教程视频

创建分步教程视频：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "film-tutorial-001",
    "taskType": "film",
    "material": {
      "text": "如何部署网站：部署你的第一个网站的分步指南",
      "type": "text"
    },
    "config": {
      "film": {
        "filmStyle": "tutorial",
        "aspectRatio": "16:9"
      }
    }
  }'
```

---

## 示例 16：从 YouTube URL 创建课程

从 YouTube 视频创建课程：

```bash
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "course-yt-001",
    "taskType": "course",
    "material": {
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "type": "youtube"
    },
    "config": {
      "course": {
        "contentStyle": "concise",
        "contentLanguage": "zh",
        "explainLanguage": "zh"
      }
    }
  }'
```

---

## 示例 17：使用轮询监控任务

创建简单的监控脚本：

```bash
#!/bin/bash
TASK_ID="c3199fb3-350b-4981-858d-09b949bfae88"

while true; do
  STATUS=$(curl -s "https://api.knowfun.io/api/openapi/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $KNOWFUN_API_KEY" | python3 -m json.tool | grep '"status"' | cut -d'"' -f4)

  echo "当前状态: $STATUS"

  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
    echo "任务完成，状态: $STATUS"
    break
  fi

  sleep 5
done
```

---

## 示例 18：批量创建多个任务

按顺序创建多个任务：

```bash
#!/bin/bash

TOPICS=("Python 基础" "JavaScript 基础" "CSS Flexbox" "Git 工作流")

for topic in "${TOPICS[@]}"; do
  echo "正在创建课程: $topic"

  curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
    -H "Authorization: Bearer $KNOWFUN_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"requestId\": \"course-$(date +%s)\",
      \"taskType\": \"course\",
      \"material\": {
        \"text\": \"学习 $topic：综合指南\",
        \"type\": \"text\"
      }
    }"

  sleep 2
done
```

---

## 示例 19：错误处理

优雅地处理常见错误：

```bash
response=$(curl -s -w "\n%{http_code}" https://api.knowfun.io/api/openapi/v1/tasks \
  -X POST \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requestId": "test-001",
    "taskType": "course",
    "material": {
      "text": "测试内容"
    }
  }')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

case $http_code in
  200)
    echo "✅ 成功: $body"
    ;;
  401)
    echo "❌ 认证失败。检查你的 API key。"
    ;;
  402)
    echo "❌ 积分不足。访问 https://www.knowfun.io/api-platform 充值"
    ;;
  429)
    echo "⚠️ 超出速率限制。请等待后重试。"
    ;;
  *)
    echo "❌ 错误 ($http_code): $body"
    ;;
esac
```

---

## 示例 20：获取使用统计

获取详细的使用统计：

```bash
curl -s "https://api.knowfun.io/api/openapi/usage?page=1&pageSize=20" \
  -H "Authorization: Bearer $KNOWFUN_API_KEY" | python3 -m json.tool
```

---

## 提示和最佳实践

### 1. 使用唯一的请求 ID
始终为幂等性使用唯一的请求 ID：
```bash
REQUEST_ID="course-$(date +%s)-$(uuidgen)"
```

### 2. 负责任地轮询
轮询状态时，使用合理的间隔：
```bash
# 好：5-10 秒间隔
sleep 5

# 避免：过于频繁的轮询
# sleep 1  # 不要这样做
```

### 3. 处理回调
对于生产使用，设置回调端点：
```json
{
  "callbackUrl": "https://your-server.com/api/knowfun-callback"
}
```

### 4. 先检查积分
批量操作前始终检查积分余额：
```bash
/knowfun credits
```

### 5. 保存任务 ID
跟踪你的任务 ID 以供将来参考：
```bash
TASK_ID=$(curl ... | python3 -m json.tool | grep taskId | cut -d'"' -f4)
echo "$TASK_ID" >> task_history.txt
```

### 6. 使用详细模式进行调试
故障排除时，使用详细模式：
```bash
curl -v https://api.knowfun.io/api/openapi/v1/tasks/...
```

### 7. 设置超时
为长时间运行的操作设置适当的超时：
```bash
curl --max-time 300 ...
```

---

## 常见工作流

### 工作流 1：快速内容生成

1. 创建任务：`/knowfun create course "你的主题"`
2. 从响应中获取任务 ID
3. 等待 2-3 分钟
4. 检查详情：`/knowfun detail <taskId>`
5. 访问生成的内容 URL

### 工作流 2：生产流水线

1. 检查积分：`/knowfun credits`
2. 创建带回调 URL 的任务
3. 接收回调通知
4. 获取详细结果
5. 处理和存储结果
6. 记录使用情况以进行计费

### 工作流 3：批处理

1. 准备内容项目列表
2. 检查总积分需求
3. 按顺序创建任务，中间有延迟
4. 在数据库中存储任务 ID
5. 轮询或等待回调
6. 收集和处理结果

---

## 故障排除

### 问题：任务卡在 "processing"

```bash
# 检查详细状态
/knowfun detail <taskId> --verbose

# 如果卡住超过 10 分钟，联系支持
```

### 问题："积分不足"

```bash
# 检查余额
/knowfun credits

# 访问 https://www.knowfun.io/api-platform 充值
```

### 问题："超出速率限制"

```bash
# 等待并使用指数退避重试
sleep 60
/knowfun create ...
```

### 问题：认证失败

```bash
# 验证 API key
echo $KNOWFUN_API_KEY

# 如果需要，在 https://www.knowfun.io/api-platform 重新生成
```
