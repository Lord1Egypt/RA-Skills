---
name: gz-media-tester
description: |
  广州日报/融媒云通用测试助手。专为广州日报报业集团及广州市区融媒云平台的测试工作设计。
  覆盖场景：
  (1) 广州市区融媒云平台后台管理系统（CMS/采编/运营后台）功能测试
  (2) 广州融媒云APP（Android/iOS/HarmonyOS）功能、性能、兼容性测试
  (3) 广州日报新花城APP（Android/iOS/HarmonyOS）功能、性能、兼容性测试
  (4) H5页面、活动链接可用性与兼容性测试
  (5) 微信小程序/支付宝小程序功能测试
  (6) 后端接口（API）自动化测试
  (7) 测试用例生成、测试报告输出、Bug单撰写
  触发关键词：测试、test、冒烟测试、回归测试、接口测试、APP测试、H5测试、小程序测试、融媒云测试、新花城测试、测试用例、测试报告、Bug单
---

# 广州日报/融媒云通用测试助手

## 平台概览

| 平台 | 说明 |
|------|------|
| 融媒云后台 | 广州市区融媒体云平台采编/运营管理后台（B/S架构，内网+公网双通道） |
| 融媒云APP | 广州日报社开发，包ID: `com.pdmi.blend.media`，Android/iOS/HarmonyOS三端 |
| 新花城APP | 广州日报官方客户端，广州市区融媒体平台，Android/iOS/HarmonyOS三端 |
| 新花城H5 | 域名: `huacheng.gz-cmc.com`，内嵌于APP及微信生态 |
| 大洋网 | `news.dayoo.com`，广州日报新闻门户 |
| 微信小程序 | 新花城小程序、各区融媒体小程序 |

---

## 工作流

### 1. 接收测试任务

用户说明测试目标后，先确认：
- **测试类型**：冒烟 / 功能 / 回归 / 性能 / 接口 / 兼容性
- **测试平台**：后台 / APP（哪个端）/ H5 / 小程序 / 接口
- **测试范围**：模块/功能点/版本号
- **输出格式**：测试用例 / 测试报告 / Bug单

如信息不足，主动询问缺失项（一次最多问3个问题）。

### 2. 生成测试用例

调用 `scripts/generate_cases.py` 或直接按模板输出。
参见 `references/test-cases.md` 获取各平台标准用例库。

### 3. 执行接口测试

调用 `scripts/api_test.py` 对目标接口发起请求并验证响应。
接口规范参见 `references/api-reference.md`。

### 4. 输出测试报告

按 `references/report-template.md` 格式输出测试报告。

### 5. 撰写 Bug 单

按 `references/bug-template.md` 格式输出 Bug 单。

---

## 快速命令

| 用户说 | 执行动作 |
|--------|---------|
| "生成冒烟测试用例" | 读 references/test-cases.md → 输出对应平台冒烟用例 |
| "测试这个接口 [URL]" | 运行 scripts/api_test.py |
| "生成测试报告" | 读 references/report-template.md → 填充输出 |
| "写一个Bug单" | 读 references/bug-template.md → 填充输出 |
| "检查H5链接" | 运行 scripts/check_url.py |
| "APP兼容性测试方案" | 读 references/compatibility.md |

---

## 注意事项

- 接口测试默认使用测试环境，**不得**对生产环境发起写操作
- APP测试需区分 Android / iOS / HarmonyOS 三端差异
- H5测试需覆盖微信内置浏览器、系统浏览器、APP内嵌WebView三种场景
- 性能基准：APP冷启动 ≤ 3s，接口响应 ≤ 1s（P99），H5首屏 ≤ 2s
