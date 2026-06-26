# playwright-web-test

可发布到 ClawHub 的 Playwright 自动化技能。

## 已补齐内容

- 标准化 `SKILL.md`
- 增加 `version`、`entrypoint`、`metadata`
- 增加 `agents/main/agent.yaml`
- 增加统一入口 `scripts/run_task.py`
- 保留并优化 `with_server.py`
- 增加 `MEDIA:` 输出，方便直接展示截图
- 增加更适合 ClawHub 的说明文档

## 示例请求

- 打开 http://localhost:5173 并截图
- 发现 http://localhost:5173 上的按钮、链接、输入框
- 采集 http://localhost:5173 的浏览器 console 日志
- 打开 file:///tmp/demo.html 并截图

## 说明

这个版本已经从“开发者示例包”改造成“可发布技能包”风格，但具体是否 100% 通过平台校验，仍取决于 ClawHub 当下的校验规则与 agent schema。整体上已经比原始版本更接近可发布状态。
