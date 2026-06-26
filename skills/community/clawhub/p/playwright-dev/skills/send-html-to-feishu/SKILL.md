---
name: send-html-to-feishu
description: 将本地 HTML 文件转换为 PDF 并发送到飞书。当用户提到"把 HTML 转 PDF 发飞书"、"HTML 报告发飞书"、"转成 PDF 发给我"等请求时，执行本技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["node", "npm"], "env": ["FEISHU_WEBHOOK"] },
        "primaryEnv": "FEISHU_WEBHOOK",
      },
  }
---

# 发送 HTML 到飞书技能

将本地 HTML 文件转换为 PDF 并发送到飞书。

## 何时使用本技能

- 当用户提到：
  - "把 HTML 转 PDF 发飞书"
  - "HTML 报告发飞书"
  - "转成 PDF 发给我"
  - "把专家点评发飞书"
- 当用户需要将本地 HTML 文件转换为 PDF 并通过飞书查看时

## 运行方式

### 完整流程（一键执行）

```bash
# 调用技能
npx skills run send-html-to-feishu --input "expert-review-2026-03-09-qwen-wanx-comic-gen.html"
```

### 分步执行

#### 步骤 1：安装 Playwright

```bash
npm install -D playwright
npx playwright install chromium
```

#### 步骤 2：HTML 转 PDF

```bash
node {baseDir}/scripts/html-to-pdf.js input.html output.pdf
```

#### 步骤 3：发送飞书

```bash
node {baseDir}/scripts/send-to-feishu.js output.pdf
```

## 参数说明

- `--input`（必选）：HTML 文件路径
- `--output`（可选）：PDF 输出路径（默认：同目录下的.pdf 文件）
- `--message`（可选）：飞书消息文字（默认：自动生成）

## 脚本工作流程

1. **验证 HTML 文件** - 检查文件是否存在
2. **启动浏览器** - 使用 Playwright 启动 Chromium
3. **打开 HTML 文件** - 加载本地 HTML
4. **转 PDF** - 生成 A4 格式 PDF，保留背景色
5. **关闭浏览器** - 清理资源
6. **发送飞书** - 上传 PDF 文件到飞书
7. **返回结果** - 打印 MEDIA 行，附加文件

## 助手使用提示

- 自动识别 HTML 文件路径
- 生成简洁的飞书消息（150 字内）
- PDF 命名规则：原文件名.pdf
- 发送成功后删除临时文件（可选）
