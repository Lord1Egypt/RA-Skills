# OpenRouter 注册与 API Key 获取指南

## 第一步：注册账号

1. 打开浏览器访问 **https://openrouter.ai**
2. 点击右上角 **「Sign Up」** 按钮
3. 选择注册方式：
   - Google 账号一键注册（推荐，最快）
   - GitHub 账号注册
   - 邮箱注册
4. 完成注册后自动登录

```
┌─────────────────────────────────┐
│         openrouter.ai           │
│                                 │
│   ┌───────────────────────┐     │
│   │    Welcome to          │     │
│   │    OpenRouter           │     │
│   │                        │     │
│   │  [Sign up with Google] │     │
│   │  [Sign up with GitHub] │     │
│   │  [Sign up with Email]  │     │
│   │                        │     │
│   └───────────────────────┘     │
│                                 │
└─────────────────────────────────┘
```

## 第二步：获取 API Key

1. 登录后，点击左侧菜单 **「Keys」** 或访问 **https://openrouter.ai/keys**
2. 点击 **「Create Key」** 按钮
3. 输入 Key 名称（随便填，如 "freeswitch"）
4. 点击 **「Create」**
5. **立即复制** 生成的 Key（格式：`sk-or-v1-...`）
6. Key 只显示一次，务必保存好

```
┌─────────────────────────────────┐
│  Keys                           │
│                                 │
│  [+ Create Key]                 │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Name: freeswitch          │  │
│  │ Key:  sk-or-v1-abc123...  │  │
│  │       [📋 Copy]           │  │
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

## 第三步：使用 Key

运行 FreeSwitch 时粘贴你的 Key：

```bash
freeswitch setup
# 提示输入时粘贴 Key：
# OpenRouter Key 1: sk-or-v1-你复制的Key
```

## 多 Key 获取（翻倍额度）

每个 OpenRouter 账号有独立的免费额度。注册多个账号可以翻倍：

1. 用不同邮箱注册第 2 个 OpenRouter 账号
2. 同样创建 API Key
3. 在 FreeSwitch setup 时输入第 2 个 Key

```
2 个 Key = 2 倍免费额度
3 个 Key = 3 倍免费额度
```

## 免费额度说明

- OpenRouter 对免费模型（带 `:free` 后缀）有每日请求限制
- 限制是按 Key 独立计算的
- 超过限制会返回 429 错误，FreeSwitch 会自动切换到下一个 Key/模型
- 通常每个 Key 每天可以免费使用数百次

## 常见问题

**Q: 需要绑定信用卡吗？**
A: 不需要。免费模型完全免费，无需付费。

**Q: Key 泄露了怎么办？**
A: 去 Keys 页面删除旧 Key，创建新的。

**Q: 免费模型质量怎么样？**
A: Step 3.5 Flash、Qwen3 Coder 等免费模型质量很好，日常使用完全够用。
