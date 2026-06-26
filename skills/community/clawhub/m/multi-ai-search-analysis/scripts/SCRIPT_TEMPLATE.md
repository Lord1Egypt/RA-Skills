# Multi-AI Search Analysis - 自动化脚本

**版本**：v1.1  
**功能**：并行询问多家 AI，自动汇总生成对比报告  
**预计耗时**：3-5 分钟（并行模式）

---

## 脚本结构

```
multi-ai-search-analysis/
├── SKILL.md              # 技能说明
├── README.md             # 快速开始
├── EXAMPLE.md            # 使用案例
├── scripts/
│   ├── run-parallel.ps1     # 并行执行主脚本（PowerShell）
│   ├── run-serial.ps1       # 串行执行脚本（备用）
│   ├── extract-data.ps1     # 数据提取工具
│   └── generate-report.ps1  # 报告生成工具
└── config/
    └── ai-platforms.json    # AI 平台配置
```

---

## 核心脚本：run-parallel.ps1

### 功能说明

- 同时打开多个浏览器标签页访问各家 AI
- 自动检查登录状态
- 并行发送问题并等待响应
- 提取各家回复内容
- 调用汇总脚本生成报告

### 使用方式

```powershell
# 基本用法
.\scripts\run-parallel.ps1 -Topic "伊朗局势分析"

# 指定 AI 平台（可选）
.\scripts\run-parallel.ps1 -Topic "全球油价预测" -Platforms @("DeepSeek", "Qwen", "Kimi")

# 自定义分析维度
.\scripts\run-parallel.ps1 -Topic "AI 行业发展" -Dimensions @("技术", "市场", "投资", "政策")

# 指定输出路径
.\scripts\run-parallel.ps1 -Topic "伊朗局势" -OutputPath "C:\reports\iran-analysis.md"
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `-Topic` | string | ✅ | - | 分析主题 |
| `-Platforms` | string[] | ❌ | @("DeepSeek","Qwen","豆包","Kimi") | AI 平台列表 |
| `-Dimensions` | string[] | ❌ | @("政治","经济","军事","外交") | 分析维度 |
| `-OutputPath` | string | ❌ | 自动生成 | 输出文件路径 |
| `-Timeout` | int | ❌ | 120 | 每家 AI 等待超时（秒） |
| `-Mode` | string | ❌ | "parallel" | 执行模式：parallel/serial |

### 执行流程

```powershell
# 1. 初始化
Load-Config ai-platforms.json
Initialize-Browser

# 2. 并行打开标签页
$tabs = @()
foreach ($platform in $Platforms) {
    $tabs += Open-BrowserTab -Url $platform.Url -Name $platform.Name
}

# 3. 检查登录状态
foreach ($tab in $tabs) {
    $loginStatus = Check-LoginStatus -Tab $tab
    if (-not $loginStatus.IsLoggedIn) {
        Write-Warning "[$($tab.Name)] 未登录，请手动完成登录后按回车继续"
        Read-Host "按回车继续"
    }
}

# 4. 构建统一问题
$question = Build-Question -Topic $Topic -Dimensions $Dimensions

# 5. 并行发送问题
foreach ($tab in $tabs) {
    Send-Message -Tab $tab -Text $question -Async
}

# 6. 并行等待响应
Wait-AllResponses -Tabs $tabs -Timeout $Timeout

# 7. 提取回复内容
$responses = @()
foreach ($tab in $tabs) {
    $responses += Extract-Response -Tab $tab -Platform $tab.Name
}

# 8. 生成综合报告
Generate-Report -Responses $responses -Topic $Topic -OutputPath $OutputPath

# 9. 清理
Close-BrowserTabs -Tabs $tabs
```

---

## 备用脚本：run-serial.ps1

### 使用场景

- 浏览器不支持多标签页
- 某家 AI 需要验证码
- 网络不稳定需要逐家确认

### 使用方式

```powershell
.\scripts\run-serial.ps1 -Topic "伊朗局势分析"
```

### 执行流程

```powershell
foreach ($platform in $Platforms) {
    # 打开标签页
    $tab = Open-BrowserTab -Url $platform.Url
    
    # 检查登录
    Check-LoginStatus -Tab $tab
    
    # 发送问题并等待
    Send-Message -Tab $tab -Text $question
    Wait-Response -Tab $tab -Timeout $Timeout
    
    # 提取回复
    $response = Extract-Response -Tab $tab
    
    # 关闭标签页
    Close-BrowserTab -Tab $tab
    
    # 保存中间结果
    Save-IntermediateResult -Platform $platform.Name -Response $response
}

# 生成报告
Generate-Report -AllResponses $allResponses
```

---

## 数据提取工具：extract-data.ps1

### 功能

从 AI 回复中提取结构化数据：

- 关键数值（油价、通胀率、GDP 等）
- 时间线事件
- 引用来源
- 预测结论

### 使用示例

```powershell
# 提取单家 AI 数据
Extract-DataFromResponse -Response $response -Platform "DeepSeek"

# 提取并对比多家数据
Compare-DataAcrossPlatforms -Responses $allResponses -DataType "油价"
```

### 输出格式

```json
{
  "platform": "DeepSeek",
  "timestamp": "2026-03-16T23:30:00+08:00",
  "keyData": {
    "oilPrice": "103.14 美元/桶",
    "inflation": "4.1%",
    "霍尔木兹影响": "97% 下降"
  },
  "timeline": [
    {"date": "2026-02-28", "event": "美以突袭"},
    {"date": "2026-03-08", "event": "新领袖就任"}
  ],
  "sources": ["路透社", "彭博社", "高盛报告"],
  "predictions": [
    "美联储降息预期推迟至 9 月",
    "Q2 全球 GDP 增速下调 0.5%"
  ]
}
```

---

## 报告生成工具：generate-report.ps1

### 功能

根据提取的数据生成 Markdown 格式综合报告

### 模板结构

```markdown
# [主题] 综合分析报告
## 四家 AI 对比分析

### 执行摘要
[200 字以内核心结论]

### 一、核心事实
- 事件时间线
- 关键数据汇总

### 二、分维度分析
[按主题划分]

### 三、预测与情景
[基准/风险/极端]

### 四、数据对比表
[关键数据横向对比]

### 五、各家特色
[AI 优势对比]

### 六、参考来源
[列出主要引用]
```

### 使用示例

```powershell
Generate-Report `
  -Responses $allResponses `
  -Topic "伊朗局势分析" `
  -OutputPath "C:\reports\iran-2026-03-16.md" `
  -IncludeCharts $true `
  -Format "markdown"
```

---

## 配置文件：ai-platforms.json

```json
{
  "platforms": [
    {
      "name": "DeepSeek",
      "url": "https://chat.deepseek.com",
      "loginMethod": "wechat",
      "avgResponseTime": 15,
      "selector": {
        "input": "textarea[placeholder*='输入']",
        "send": "button[aria-label*='发送']",
        "response": "div.markdown-body"
      }
    },
    {
      "name": "Qwen",
      "url": "https://chat.qwen.ai",
      "loginMethod": "github",
      "avgResponseTime": 12,
      "selector": {
        "input": "#chat-input",
        "send": "#send-button",
        "response": ".response-content"
      }
    },
    {
      "name": "豆包",
      "url": "https://www.doubao.com",
      "loginMethod": "phone",
      "avgResponseTime": 20,
      "selector": {
        "input": "textarea",
        "send": ".send-btn",
        "response": ".answer-content"
      }
    },
    {
      "name": "Kimi",
      "url": "https://kimi.moonshot.cn",
      "loginMethod": "phone",
      "avgResponseTime": 18,
      "selector": {
        "input": "#input-box",
        "send": "#submit-btn",
        "response": ".message-ai"
      }
    }
  ],
  "defaultDimensions": ["政治", "经济", "军事", "外交"],
  "defaultTimeout": 120,
  "browser": {
    "type": "chrome",
    "headless": false,
    "width": 1280,
    "height": 800
  }
}
```

---

## 依赖安装

### 系统要求

- PowerShell 7.0+
- .NET 6.0+
- Chrome/Edge 浏览器
- Selenium WebDriver 或 Playwright

### 安装脚本

```powershell
# 安装 Selenium
Install-Module -Name Selenium -Force

# 或安装 Playwright
npm install -g playwright
playwright install

# 下载 WebDriver
.\scripts\install-webdriver.ps1
```

---

## 快速开始

### 1. 首次设置

```powershell
# 克隆技能目录
cd skills\multi-ai-search-analysis

# 安装依赖
.\scripts\install-dependencies.ps1

# 测试浏览器
.\scripts\test-browser.ps1
```

### 2. 登录各家 AI

```powershell
# 打开所有平台登录页面
.\scripts\login-all.ps1

# 手动完成登录后关闭
```

### 3. 运行分析

```powershell
# 并行模式（推荐）
.\scripts\run-parallel.ps1 -Topic "伊朗局势分析"

# 串行模式（备用）
.\scripts\run-serial.ps1 -Topic "伊朗局势分析"
```

### 4. 查看报告

报告自动生成在 `reports/` 目录下，文件名格式：
```
{主题}-{日期}-{时间}.md
```

---

## 故障排查

### 常见问题

#### 1. 浏览器无法打开

```powershell
# 检查 WebDriver 路径
Get-WebdriverPath

# 重新安装 WebDriver
.\scripts\install-webdriver.ps1 -Force
```

#### 2. 登录状态检测失败

```powershell
# 手动检查登录
.\scripts\check-login.ps1 -Platform "DeepSeek"

# 清除缓存后重试
.\scripts\clear-cache.ps1
```

#### 3. 响应提取失败

```powershell
# 检查选择器配置
.\scripts\test-selector.ps1 -Platform "Qwen"

# 更新选择器配置
Edit config\ai-platforms.json
```

#### 4. 超时错误

```powershell
# 增加超时时间
.\scripts\run-parallel.ps1 -Topic "xxx" -Timeout 180
```

---

## 扩展开发

### 添加新 AI 平台

1. 编辑 `config\ai-platforms.json`
2. 添加平台配置
3. 测试选择器
4. 更新文档

### 自定义报告模板

1. 复制 `templates\report-template.md`
2. 修改模板结构
3. 在 `generate-report.ps1` 中引用新模板

### 增加数据可视化

```powershell
# 安装图表库
Install-Module -Name PSChart

# 在 generate-report.ps1 中添加
Add-Chart -Data $oilPriceData -Type "line" -Output "oil-trend.png"
```

---

## 性能优化建议

1. **并行度控制**：根据网络情况调整并发数
2. **缓存机制**：保存登录状态，避免重复登录
3. **增量更新**：支持对同一主题多次追踪分析
4. **异步处理**：使用异步 I/O 提升响应速度

---

## 安全注意事项

1. **不要硬编码凭据**：使用环境变量或凭据管理器
2. **遵守平台条款**：不要高频调用触发反爬
3. **数据隐私**：敏感主题分析注意本地存储
4. **合理使用**：避免对单一平台造成压力

---

*本脚本由小呱（🐸）设计，待实现。欢迎贡献代码！*
