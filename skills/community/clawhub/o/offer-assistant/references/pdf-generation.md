# PDF 生成方法论

从 HTML 简历生成干净 PDF 的唯一可靠方式。

## 核心流程

```
Agent 生成定制简历 HTML → 调用脚本 → 输出 PDF
```

## 唯一路径

```bash
node scripts/generate-pdf.js ./resume.html ./resume.pdf
```

脚本执行：
1. 启动 Chrome headless（`--remote-debugging-port=9225`）
2. 启动本地 HTTP Server 服务 HTML
3. 通过 CDP 创建空标签页 → 导航到 HTML → 5s 等待渲染
4. 调用 `Page.printToPDF` 参数：
   - `displayHeaderFooter: false`（关键——确保无页眉页脚）
   - `printBackground: true`
   - 边距：上下 0.4in，左右 0.6in
   - A4 纸张大小

## ❌ 禁止使用的方式

| 方式 | 问题 |
|------|------|
| Chrome 命令行 `--print-to-pdf-no-header` | flag 无效，PDF 仍然有页眉页脚 |
| 浏览器内置「打印」功能 | 效果不一致 |
| wkhtmltopdf / puppeteer | 依赖未声明，可能缺失 |

## 常见问题

| 症状 | 原因 | 解法 |
|------|------|------|
| PDF 1KB | Chrome 残留进程占用端口或页面未渲染 | kill 残余 Chrome 进程，重试 |
| PDF 有页眉页脚 | 用了命令行而非 CDP 脚本 | 只用 generate-pdf.js |
| 脚本报错 | CDP 连接方式不对 | 先连 Browser WS 创建 target，再连 target WS 调 printToPDF |
| Chrome 找不到 | 路径不对 | 脚本会在多个常见路径寻找 chrome，如缺失需安装 |
| HTML 编码问题 | 中文简历未指定 charset | 确保 HTML 中有 `<meta charset="utf-8">` |
