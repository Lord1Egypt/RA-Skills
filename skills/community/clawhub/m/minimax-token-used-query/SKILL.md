# MiniMax Token Used Query

查询 MiniMax Coding Plan 的剩余 token 使用量及刷新时间。

## 重要说明

**本技能通过本地浏览器自动化方式查询 Token 使用量，而非调用 API 接口。**

技术实现：使用 browser-use CLI 控制本地 Chrome 浏览器，模拟用户手动访问 MiniMax 开发者平台，自动化完成登录和页面数据提取操作。

## 使用场景

当需要检查当前模型使用百分比时使用，确保不会因 token 耗尽而影响思考能力。

## 使用方法

### 快速查询
```bash
/home/allen/.openclaw/workspace/skills/minimax-token-used-query/quick.sh
```

### 触发方式

当用户问以下问题时使用此技能：
- "token 还剩多少"
- "minimax 使用量"
- "还有多少 token"
- "查询 minimax 额度"
- "token 百分比"
- "MiniMax 还能用多久"

## 技能逻辑

1. **打开页面**：使用本地浏览器打开 MiniMax Coding Plan 管理页面
   ```
   https://platform.minimaxi.com/user-center/payment/coding-plan
   ```

2. **登录检测**：检查页面是否显示登录界面
   - 如果需要登录，进入登录流程
   - 点击"手机验证码登录"标签
   - 输入手机号（国家码默认 +86）
   - 勾选用户协议
   - 点击"获取验证码"
   - 输入验证码后点击登录

3. **提取数据**：从页面 DOM 中提取以下信息：
   - 已使用百分比（如：13%）
   - 重置剩余时间（如：4小时24分钟后重置）
   - 可用额度（如：40 prompts / 5小时）
   - 时间窗口（如：00:00-05:00 UTC+8）

4. **返回结果**：返回结构化数据

## 页面元素参考（2026-03-12 实测 V8）

### 🔑 关键发现

1. **Shadow DOM 输入框** - 必须用 `click + type` 组合
2. **协议勾选** - 使用 JavaScript 方式更可靠：`document.querySelector('#register_protocol').click()`
3. **动态 ID** - 每次页面加载元素 ID 都会变化，需要动态获取
4. **等待时间** - 减少不必要的 sleep，提高速度

### 优化后的登录流程

1. 打开页面
2. 动态获取手机号输入框 ID
3. click 输入框 → type 手机号
4. 动态获取密码输入框 ID  
5. click 输入框 → type 密码
6. 使用 JavaScript 勾选协议
7. 点击登录按钮
8. 检查登录结果
9. 保存凭据到 memory

### 登录方式

#### 方式1：密码登录（默认）
- 优先使用
- 凭据保存在 memory 中
- 速度快，无需交互

#### 方式2：手机验证码登录
- 当没有保存密码时自动使用
- 需要用户输入手机号和验证码
- 登录成功后不保存密码

### 凭据管理

- 首次使用：提示用户输入手机号（验证码登录）或手机号+密码（密码登录）
- 登录成功后：自动保存到 `~/.openclaw/workspace/memory/minimax-login.txt`
- 下次使用：自动从 memory 读取
- 登录失败：删除保存的凭据，提示重新输入

## 输出格式

返回 JSON 格式：
```json
{
  "used_percent": 13,
  "reset_minutes": 264,
  "total_prompts": 40,
  "total_hours": 5,
  "reset_time": "00:00-05:00(UTC+8)"
}
```

## 技术特点

- **本地浏览器**：依赖本地 Chrome 浏览器（需要已登录 MiniMax 账号）
- **无 API 调用**：不调用任何后端 API，完全模拟用户操作
- **自动登录**：支持自动手机验证码登录
- **实时数据**：每次查询前自动刷新页面，确保数据最新

## 依赖

- browser-use CLI
- 本地 Chrome 浏览器 (profile: Default)
- 已登录的 MiniMax 账号（或需要手动输入验证码）

## 注意事项

- 首次使用或登录状态失效时，需要用户配合输入手机号和验证码完成登录
- 浏览器窗口会被打开并自动操作
- 查询完成后浏览器会停留在结果页面，方便下次查询（保持登录状态）
