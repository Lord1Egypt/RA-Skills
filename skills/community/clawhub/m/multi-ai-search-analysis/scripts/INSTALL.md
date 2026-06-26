# 自动化脚本安装与使用指南

**版本**：v1.1  
**最后更新**：2026-03-16

---

## 📦 快速安装

### 步骤 1：安装依赖

```powershell
# 进入技能目录
cd skills\multi-ai-search-analysis

# 运行安装脚本
.\scripts\install-dependencies.ps1
```

或手动安装：

```powershell
# 选项 A：使用 Selenium（推荐新手）
Install-Module -Name Selenium -Force -Scope CurrentUser

# 选项 B：使用 Playwright（更强大）
npm install -g playwright
playwright install chrome
```

### 步骤 2：下载 WebDriver

```powershell
# Selenium 用户
.\scripts\install-webdriver.ps1

# Playwright 用户（已在上面安装）
```

### 步骤 3：测试浏览器

```powershell
.\scripts\test-browser.ps1
```

应该会自动打开 Chrome 浏览器并关闭。

---

## 🔐 首次登录配置

### 方式 A：手动登录（推荐）

```powershell
# 打开所有 AI 平台登录页面
.\scripts\login-all.ps1
```

然后依次在打开的浏览器中完成登录：

1. **DeepSeek** - 微信扫码或手机号
2. **Qwen** - GitHub/Google/Apple 账号
3. **豆包** - 手机号 + 验证码
4. **Kimi** - 手机号 + 验证码

登录后**不要关闭浏览器**，脚本会复用登录状态。

### 方式 B：自动登录（高级）

需要配置凭据管理器：

```powershell
# 保存登录凭据（不推荐，有安全风险）
.\scripts\save-credentials.ps1
```

---

## 🚀 开始使用

### 基本用法

```powershell
# 并行模式（推荐）
.\scripts\run-parallel.ps1 -Topic "伊朗局势分析"

# 串行模式（备用，遇到验证码时使用）
.\scripts\run-serial.ps1 -Topic "伊朗局势分析"
```

### 自定义参数

```powershell
# 指定 AI 平台
.\scripts\run-parallel.ps1 `
  -Topic "全球油价预测" `
  -Platforms @("DeepSeek", "Qwen", "Kimi")

# 自定义分析维度
.\scripts\run-parallel.ps1 `
  -Topic "AI 行业发展" `
  -Dimensions @("技术", "市场", "投资", "政策")

# 指定输出路径
.\scripts\run-parallel.ps1 `
  -Topic "伊朗局势" `
  -OutputPath "C:\reports\iran-analysis.md"

# 调整超时时间（某家 AI 响应慢时）
.\scripts\run-parallel.ps1 `
  -Topic "复杂分析" `
  -Timeout 180
```

### 完整示例

```powershell
.\scripts\run-parallel.ps1 `
  -Topic "2026 年中东局势对全球经济的影响" `
  -Platforms @("DeepSeek", "Qwen", "豆包", "Kimi") `
  -Dimensions @("政治", "经济", "军事", "外交", "能源") `
  -OutputPath "C:\reports\middle-east-2026.md" `
  -Timeout 150 `
  -Mode "parallel"
```

---

## 📊 查看报告

报告自动生成在 `reports/` 目录下：

```
reports/
└── 伊朗局势分析 -2026-03-16-2330.md
```

文件名格式：`{主题}-{日期}-{时间}.md`

用任意 Markdown 编辑器打开查看，或用浏览器预览：

```powershell
# 用默认应用打开最新报告
.\scripts\open-latest-report.ps1
```

---

## 🔧 故障排查

### 问题 1：浏览器无法打开

**症状**：
```
错误：浏览器初始化失败
```

**解决**：
```powershell
# 检查 Chrome 是否安装
chrome --version

# 重新安装 WebDriver
.\scripts\install-webdriver.ps1 -Force

# 检查 WebDriver 路径
Get-WebdriverPath
```

### 问题 2：登录状态检测失败

**症状**：
```
[DeepSeek] 未登录，请手动完成登录
```

**解决**：
```powershell
# 手动打开登录
.\scripts\login-all.ps1

# 清除缓存后重试
.\scripts\clear-cache.ps1

# 检查登录状态
.\scripts\check-login.ps1 -Platform "DeepSeek"
```

### 问题 3：响应提取失败

**症状**：
```
错误：无法找到回复内容
```

**解决**：
```powershell
# 测试选择器
.\scripts\test-selector.ps1 -Platform "Qwen"

# 如果平台更新了 UI，需要更新配置
notepad config\ai-platforms.json
# 修改 selectors 部分
```

### 问题 4：超时错误

**症状**：
```
[豆包] 等待超时（120 秒）
```

**解决**：
```powershell
# 增加超时时间
.\scripts\run-parallel.ps1 -Topic "xxx" -Timeout 180

# 或单独配置某家平台的超时
# 编辑 config\ai-platforms.json
# "豆包": { "timeout": 180 }
```

### 问题 5：验证码拦截

**症状**：
```
[豆包] 检测到验证码
```

**解决**：
1. 切换到串行模式
2. 手动完成验证码
3. 按回车继续

```powershell
.\scripts\run-serial.ps1 -Topic "xxx"
```

---

## 📝 日志与调试

### 查看详细日志

```powershell
# 启用调试模式
$env:DEBUG = "true"
.\scripts\run-parallel.ps1 -Topic "xxx" -Verbose
```

### 查看日志文件

```powershell
# 日志位置
logs\multi-ai-2026-03-16.log

# 实时查看日志
Get-Content logs\multi-ai-*.log -Tail 50 -Wait
```

### 保存中间结果

```powershell
# 保存每家 AI 的原始回复
.\scripts\run-parallel.ps1 -Topic "xxx" -SaveRawResponses
```

原始回复保存在 `raw-responses/` 目录。

---

## 🎯 最佳实践

### 1. 选择合适的时间

- ✅ 网络空闲时段（深夜/清晨）
- ❌ 避免高峰期（工作日 9-11 点、14-16 点）

### 2. 提前登录

运行前 5 分钟完成所有平台登录，避免脚本等待。

### 3. 使用并行模式

除非遇到验证码，否则优先使用并行模式，节省 60-75% 时间。

### 4. 合理设置超时

- 简单问题：60-90 秒
- 复杂分析：120-180 秒
- 深度研究：180-300 秒

### 5. 保存报告

重要分析及时备份：

```powershell
Copy-Item reports\*.md -Destination "D:\备份\AI 分析报告\"
```

---

## 🔐 安全提醒

1. **不要硬编码凭据**：使用环境变量或凭据管理器
2. **遵守平台条款**：不要高频调用触发反爬
3. **数据隐私**：敏感主题分析注意本地存储
4. **合理使用**：避免对单一平台造成压力

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能详细说明
- [README.md](../README.md) - 快速开始
- [EXAMPLE.md](../EXAMPLE.md) - 使用案例
- [SCRIPT_TEMPLATE.md](./SCRIPT_TEMPLATE.md) - 脚本设计文档

---

## 💡 反馈与改进

遇到问题或有改进建议？

1. 检查故障排查章节
2. 查看日志文件
3. 更新到最新版本
4. 提交 Issue 或 PR

---

*最后更新：2026-03-16 23:30*  
*维护者：小呱 🐸*
