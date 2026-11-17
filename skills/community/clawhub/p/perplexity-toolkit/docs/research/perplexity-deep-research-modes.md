# Perplexity 浏览器自动化 — Deep Research + 搜索模式

> 2026-08-29 实操测绘

## 搜索模式激活

### 方法：输入 "/" 触发模式选择器

```
1. 点击 textbox 聚焦
2. 输入 "/" (CDP Input.insertText)
3. 等待弹出菜单出现
4. 选择模式（默认高亮 Deep Research）
5. 按 Enter 确认
6. 输入查询内容
7. 三事件 Enter 提交
```

### 可用搜索模式

| 模式 | 图标 | 说明 |
|------|------|------|
| **深度研究** | 🔭 | 多步骤深度研究，4+ 步骤，答案更长更详细 |
| **模型委员会** | 🔨 | 多模型对比/共识模式 |
| **逐步学习** | 📖 | 引导式学习模式 |
| **Computer** | 🖥️ | 更强大的工具和技能 |

### 代码实现

```bash
# 1. 聚焦输入框
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","args":{"selector":"@eNN"},"session":"pplx-session"}'

# 2. 输入 "/" 触发模式选择器
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"cdp","args":{"method":"Input.insertText","params":{"text":"/"}},"session":"pplx-session"}'
sleep 1

# 3. 按 Enter 选择默认高亮的 Deep Research
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"cdp","args":{"method":"Input.dispatchKeyEvent","params":{"type":"keyDown","key":"Enter","code":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13}},"session":"pplx-session"}'
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"cdp","args":{"method":"Input.dispatchKeyEvent","params":{"type":"keyUp","key":"Enter","code":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13}},"session":"pplx-session"}'
sleep 1

# 4. 验证 Deep Research 模式已激活（输入区应显示"🔍 深度研究"标签）
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"screenshot","args":{},"session":"pplx-session"}'
```

## Deep Research vs 普通搜索

| 维度 | 普通搜索 | Deep Research |
|------|---------|---------------|
| 步骤数 | 1 步 | 4+ 步 |
| 答案长度 | ~3000 字符 | ~5500 字符 |
| 源数量 | 15-20 个 | 4 个（但更深入） |
| 等待时间 | 10-15 秒 | 60-120 秒 |
| 个性化 | 通用 | 个性化（基于用户历史） |
| 展开按钮 | 常见 | 较少见（答案本身已展开） |

## 模型委员会 (Model Council)

- 多模型同时回答同一问题
- 比较不同模型的输出
- 适用于需要多角度分析的场景

## 逐步学习 (Step-by-step Learning)

- 引导式学习模式
- 将复杂主题分解为步骤
- 适用于教学/学习场景

## 图片生成模式

- 通过 "添加文件或工具" 按钮 (@e48) 访问
- 需要进一步探索

## Focus 模式（历史）

- 2026 年版本已不再有独立的 Academic/Writing/Math Focus 模式
- 由搜索模式选择器 "/" 统一管理
- Deep Research 替代了原来的 Academic Focus

## 完整自动化流程（含模式选择）

```
navigate → snapshot → click textbox → 输入 "/" → Enter 选择模式 → 输入查询 → 三事件 Enter → wait → extract
```

### 等待时间参考

- 普通搜索: 10-15 秒
- Deep Research: 60-120 秒（建议用 heartbeat 每 30 秒检查一次）
- 模型委员会: 20-30 秒
