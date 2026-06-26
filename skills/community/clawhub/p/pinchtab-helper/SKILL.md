# PinchTab Browser Control 🖱️

让 AI 通过 PinchTab 控制浏览器的 Skill。

## 什么是 PinchTab?

PinchTab 是一个轻量级的浏览器控制工具，比传统的浏览器自动化更高效：
- Token 高效：800 tokens/page（比截图便宜 5-13 倍）
- 稳定性好：使用稳定的 accessibility refs
- 支持多实例：可同时运行多个浏览器实例

## 使用前提

1. **安装 PinchTab**（需要先安装）：
   ```bash
   # macOS / Linux
   curl -fsSL https://pinchtab.com/install.sh | bash
   
   # 或 npm
   npm install -g pinchtab
   
   # 或 Docker
   docker run -d --name pinchtab -p 127.0.0.1:9867:9867 pinchtab/pinchtab
   ```

2. **启动服务**：
   ```bash
   pinchtab &
   ```

## 核心操作

### 1. 导航到网页
```bash
pinchtab nav https://example.com
```

### 2. 获取页面快照
```bash
pinchtab snap -i -c
# -i: interactive 模式（可交互元素）
# -c: 显示点击引用
```

### 3. 点击元素（通过 ref）
```bash
pinchtab click e5
```

### 4. 输入文字
```bash
pinchtab fill e3 "搜索内容"
```

### 5. 提交表单
```bash
pinchtab press e7 Enter
```

### 6. 截图
```bash
pinchtab screenshot
```

## 完整示例

### 搜索任务
```bash
# 1. 打开 Google
pinchtab nav https://google.com

# 2. 获取页面
pinchtab snap -i -c

# 3. 在搜索框输入（假设 ref 是 e5）
pinchtab fill e5 "什么是 AI"

# 4. 按回车
pinchtab press e5 Enter

# 5. 获取结果
pinchtab snap -i -c
```

## API 端点

如果直接用 HTTP：
- 基础 URL: http://localhost:9867
- 创建实例: POST /instances/launch
- 打开标签: POST /instances/{id}/tabs/open
- 快照: GET /tabs/{id}/snapshot
- 操作: POST /tabs/{id}/action

## Skill 触发词

- 打开浏览器
- 浏览网页
- 搜索xxx
- 访问xxx网站
- 帮我操作浏览器
- 用 pinchtab

## 注意事项

1. **安全**：PinchTab 默认只绑定 127.0.0.1
2. **Profile**：建议使用专门的自动化 profile
3. **Token**：如果需要远程访问，设置 BRIDGE_TOKEN

---

Made with ❤️ by 小溪
