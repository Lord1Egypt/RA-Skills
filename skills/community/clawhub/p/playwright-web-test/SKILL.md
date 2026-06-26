---
name: playwright-web-test
description: 使用 Playwright 对本地网页、静态 HTML 或在线页面执行自动化测试、元素发现、控制台日志采集与截图。
version: 1.0.0
entrypoint: agents/main/agent.yaml
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    capability:
      - web-automation
      - screenshot
      - ui-testing
      - dom-inspection
      - console-capture
---

# Playwright Web Test

这是一个面向 ClawHub / OpenClaw 的网页自动化技能，适合以下场景：

- 打开网页并截图
- 自动发现按钮、链接、输入框等元素
- 采集浏览器 console 日志
- 测试本地静态 HTML 文件
- 在启动本地服务后执行自动化脚本

## 推荐触发方式

你可以直接对 agent 说：

- 打开 `http://localhost:5173` 并截图
- 分析这个页面上有哪些按钮和输入框：`http://localhost:3000`
- 访问 `file:///tmp/demo.html`，点击按钮后截图
- 采集 `http://localhost:5173` 的 console 日志

## 目录说明

- `agents/main/agent.yaml`：技能入口
- `scripts/run_task.py`：统一执行入口
- `scripts/with_server.py`：先启动服务再执行自动化
- `examples/`：示例脚本

## 使用建议

1. 动态页面先等待 `networkidle`
2. 优先先做元素发现，再编写精确操作
3. 需要启动本地服务时，优先使用 `with_server.py`
4. 截图输出会使用 `MEDIA:` 规范，便于网关直接展示

## 注意事项

- 需要本地 Python 环境可用
- 首次运行前需安装 Playwright：
  `python3 -m pip install playwright && python3 -m playwright install chromium`
- 如果目标页面依赖本地服务，请确认端口可访问
