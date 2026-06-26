# HRrule AI WebSocket API 参考文档

## 概述

HRrule AI 平台提供 WebSocket API 接口,支持实时聊天和流式响应。

## 连接信息

### WebSocket URL

```
ws://192.168.112.114:5000
```

### 认证方式

使用 API Key 进行认证,通过 query 参数传递:

```javascript
query: { api_key: 'your-api-key' }
```

## Socket.IO 配置

### 必需库

```html
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
```

### 连接选项

```javascript
const socketOptions = {
    transports: ['websocket', 'polling'],  // 支持的传输方式
    reconnection: false,  // 不自动重连
    query: { api_key: 'your-api-key' }  // API Key
};
```

## Socket.IO 事件

### 客户端发送事件

#### `open_chat_completion`

发送消息并获取 AI 响应。

**参数:**

| 参数名 | 类型 | 必需 | 说明 | 示例 |
|--------|------|------|------|------|
| content | string | 是 | 用户的问题或需求 | "帮我写员工手册" |
| page_session | string | 是 | 页面会话ID | "session_1234567890_abc123" |
| model | string | 否 | 使用的模型 | "deepseek-ai/DeepSeek-R1" |
| tag_id | number | 是 | 内容类型标识 | 2 |
| rt | string | 是 | 资源类型/模板名称 | "员工手册" |
| ua | string | 否 | 用户代理 | "web" |
| deep | number | 否 | 深度参数 | 1 |
| web | number | 否 | 网络搜索参数 | 1 |

**示例:**

```javascript
socket.emit('open_chat_completion', {
    content: '帮我生成一份员工手册',
    page_session: 'session_' + Date.now(),
    model: 'deepseek-ai/DeepSeek-R1',
    tag_id: 2,
    rt: '员工手册',
    ua: 'web',
    deep: 1,
    web: 1
});
```

### 服务器发送事件

#### `connect`

连接成功建立。

```javascript
socket.on('connect', () => {
    console.log('Connected with socket ID:', socket.id);
});
```

#### `chunk`

接收流式响应数据块。

**数据格式:**

```javascript
{
    choices: [{
        delta: {
            content: "文本内容",
            reasoning_content: "思考过程"
        }
    }]
}
```

**示例:**

```javascript
socket.on('chunk', (data) => {
    const chunkData = typeof data === 'string' ? JSON.parse(data) : data;
    const content = chunkData.choices?.[0]?.delta?.content || '';
    const thinking = chunkData.choices?.[0]?.delta?.reasoning_content || '';

    // 处理内容
    if (content) {
        console.log('AI 回复:', content);
    }

    // 处理思考过程
    if (thinking) {
        console.log('AI 思考:', thinking);
    }
});
```

#### `complete`

响应完成。

```javascript
socket.on('complete', (data) => {
    console.log('Response completed:', data);
    // 更新UI状态,启用发送按钮等
});
```

#### `error`

发生错误。

```javascript
socket.on('error', (data) => {
    console.error('Server error:', data.msg);
    // 显示错误信息给用户
});
```

#### `start`

开始处理。

```javascript
socket.on('start', (data) => {
    console.log('Processing started, history_id:', data.history_id);
});
```

#### `node_started`

工作流节点开始。

```javascript
socket.on('node_started', (data) => {
    console.log('Node started:', data.id);
});
```

#### `node_finished`

工作流节点完成。

```javascript
socket.on('node_finished', (data) => {
    console.log('Node finished:', data.id);
});
```

#### `disconnect`

连接断开。

```javascript
socket.on('disconnect', (reason) => {
    console.log('Disconnected:', reason);
});
```

#### `connect_error`

连接错误。

```javascript
socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
});
```

## Tag ID 和 RT 参数完整列表

### Tag ID: 2 - 制度类

| RT | 说明 |
|----|------|
| 员工手册 | 公司员工手册 |
| 招聘管理制度 | 招聘流程和管理制度 |
| 入职试用期管理制度 | 新员工入职和试用期管理 |
| 劳动合同管理制度 | 劳动合同管理规范 |
| 薪酬管理制度 | 薪酬体系和发放制度 |
| 考勤休假制度 | 考勤和假期管理 |
| 加班管理制度 | 加班申请和管理流程 |
| 绩效管理制度 | 绩效评估和管理制度 |
| 员工培训制度 | 员工培训和发展制度 |
| 离职管理制度 | 员工离职管理流程 |
| 员工竞聘制度 | 内部竞聘制度 |
| 病假管理制度 | 病假管理规范 |
| 奖惩制度 | 奖励和处罚制度 |
| 其他制度 | 其他管理制度 |

### Tag ID: 7 - 岗位类

| RT | 说明 |
|----|------|
| 岗位说明书(word) | Word 格式的岗位说明书 |
| 岗位说明书(excel) | Excel 格式的岗位说明书 |
| 工作饱和度评估表 | 工作量评估表 |
| 任职资格标准 | 岗位任职资格要求 |
| 职位图谱 | 组织架构职位图谱 |

### Tag ID: 3 - 绩效类

| RT | 说明 |
|----|------|
| 360考核表 | 360度绩效考核表 |
| BSC考核表 | 平衡计分卡考核表 |
| KPI考核表 | 关键绩效指标考核表 |
| OKR考核表 | 目标与关键成果考核表 |
| 绩效承诺书 | 绩效目标承诺书 |
| 绩效改进计划 | 绩效提升改进计划 |
| 绩效面谈表 | 绩效面谈记录表 |
| 绩效诊断报告 | 绩效管理诊断报告 |

### Tag ID: 4 - 招聘类

| RT | 说明 |
|----|------|
| 人才画像 | 候选人画像分析 |
| 面试评估表 | 面试评估打分表 |
| 面试题库 | 各岗位面试题库 |
| 招聘需求表 | 招聘需求申请表 |
| 招聘JD | 招聘职位描述 |
| 背景调查表 | 候选人背景调查 |
| 录用条件说明书 | 录用条件说明 |
| 录用通知书 | 员工录用通知 |
| 入职承诺书 | 入职承诺声明 |
| 劳动合同 | 劳动合同模板 |

### Tag ID: 5 - 薪酬类

| RT | 说明 |
|----|------|
| 薪酬等级表 | 薪酬等级体系表 |
| 薪酬面谈表 | 薪酬谈判面谈表 |
| 薪酬诊断报告 | 薪酬体系诊断报告 |
| 岗位价值评估表 | 岗位价值评估打分表 |

### Tag ID: 8 - 培训类

| RT | 说明 |
|----|------|
| 新员工培训计划 | 新员工入职培训计划 |
| 年度培训计划 | 年度培训计划表 |

### Tag ID: 13 - 报告类

| RT | 说明 |
|----|------|
| 年终总结 | 年度工作总结 |
| 月度报告 | 月度工作报告 |
| 周报 | 周工作报告 |
| 日报 | 日报表 |

### Tag ID: 14 - 风控类

| RT | 说明 |
|----|------|
| 风险自测 | HR风险自查表 |

## 完整示例

### HTML 页面示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>HRrule AI Chat</title>
    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
</head>
<body>
    <div>
        <input type="text" id="apiKey" placeholder="API Key">
        <input type="text" id="tagId" value="2">
        <input type="text" id="rt" value="员工手册">
        <textarea id="userInput" placeholder="输入您的问题..."></textarea>
        <button onclick="sendMessage()">发送</button>
    </div>
    <div id="chatMessages"></div>

    <script>
        let socket = null;

        function sendMessage() {
            const content = document.getElementById('userInput').value.trim();
            if (!content) return;

            const socketOptions = {
                transports: ['websocket', 'polling'],
                reconnection: false,
                query: { api_key: document.getElementById('apiKey').value }
            };

            socket = io('ws://192.168.112.114:5000', socketOptions);

            socket.on('connect', () => {
                console.log('Connected');

                socket.emit('open_chat_completion', {
                    content: content,
                    page_session: 'session_' + Date.now(),
                    model: 'deepseek-ai/DeepSeek-R1',
                    tag_id: parseInt(document.getElementById('tagId').value),
                    rt: document.getElementById('rt').value,
                    ua: 'web',
                    deep: 1,
                    web: 1
                });
            });

            socket.on('chunk', (data) => {
                const chunkData = typeof data === 'string' ? JSON.parse(data) : data;
                const content = chunkData.choices?.[0]?.delta?.content || '';
                if (content) {
                    appendMessage(content);
                }
            });

            socket.on('complete', () => {
                console.log('Completed');
                socket.disconnect();
            });

            socket.on('error', (data) => {
                console.error('Error:', data.msg);
            });
        }

        function appendMessage(content) {
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.textContent = content;
            chatMessages.appendChild(messageDiv);
        }
    </script>
</body>
</html>
```

### Node.js 示例

```javascript
const io = require('socket.io-client');

const socket = io('ws://192.168.112.114:5000', {
    transports: ['websocket', 'polling'],
    reconnection: false,
    query: { api_key: 'your-api-key' }
});

socket.on('connect', () => {
    console.log('Connected');

    socket.emit('open_chat_completion', {
        content: '帮我生成员工手册',
        page_session: 'session_' + Date.now(),
        model: 'deepseek-ai/DeepSeek-R1',
        tag_id: 2,
        rt: '员工手册',
        ua: 'web',
        deep: 1,
        web: 1
    });
});

socket.on('chunk', (data) => {
    const content = data.choices?.[0]?.delta?.content || '';
    console.log(content);
});

socket.on('complete', () => {
    console.log('Done');
    socket.disconnect();
});
```

## 错误处理

### 常见错误

| 错误类型 | 说明 | 解决方法 |
|----------|------|----------|
| Unauthorized | API Key 无效 | 检查 API Key 是否正确 |
| Connection refused | 连接被拒绝 | 检查 WebSocket URL 和网络连接 |
| Timeout | 连接超时 | 检查网络和防火墙设置 |
| Invalid parameters | 参数无效 | 检查 tag_id 和 rt 是否正确 |

### 错误处理示例

```javascript
socket.on('connect_error', (error) => {
    console.error('Connection error:', error);

    if (error.message.includes('Unauthorized') ||
        error.message.includes('401')) {
        console.error('API Key 无效,请检查您的 API Key');
    } else if (error.message.includes('Connection refused')) {
        console.error('连接被拒绝,请检查 WebSocket URL');
    } else {
        console.error('未知错误:', error.message);
    }
});

socket.on('error', (data) => {
    console.error('Server error:', data.msg);
    // 显示错误信息给用户
    alert('错误: ' + data.msg);
});
```

## 最佳实践

### 1. 页面会话管理

每次发送消息生成唯一的 session_id:

```javascript
const pageSession = 'session_' + Date.now() + '_' +
    Math.random().toString(36).substr(2, 9);
```

### 2. 流式响应处理

正确处理流式响应以提供更好的用户体验:

```javascript
let currentMessageContent = '';

socket.on('chunk', (data) => {
    const chunkData = typeof data === 'string' ? JSON.parse(data) : data;
    const content = chunkData.choices?.[0]?.delta?.content || '';

    if (content) {
        currentMessageContent += content;
        // 实时更新UI
        updateCurrentMessage(content);
        // 滚动到底部
        scrollToBottom();
    }
});
```

### 3. 连接生命周期管理

在响应完成后断开连接以释放资源:

```javascript
socket.on('complete', () => {
    console.log('Response completed');
    setTimeout(() => {
        if (socket) {
            socket.disconnect();
        }
    }, 500);
});
```

### 4. 错误恢复

提供重试机制:

```javascript
let retryCount = 0;
const maxRetries = 3;

function sendMessageWithRetry(data) {
    socket.emit('open_chat_completion', data);

    socket.on('error', (error) => {
        if (retryCount < maxRetries) {
            retryCount++;
            console.log('Retrying... (' + retryCount + '/' + maxRetries + ')');
            setTimeout(() => {
                sendMessageWithRetry(data);
            }, 1000 * retryCount);
        }
    });
}
```

## 测试

使用 `test_open_chat.html` 页面测试 API 功能:

1. 打开 `test_open_chat.html` 文件
2. 输入 WebSocket URL 和 API Key
3. 选择合适的 tag_id 和 rt
4. 输入问题并点击发送
5. 查看响应是否正常

## 支持

如有问题,请联系:
- HRrule AI 平台: https://ai.hrrule.com
- WorkBuddy 支持团队
