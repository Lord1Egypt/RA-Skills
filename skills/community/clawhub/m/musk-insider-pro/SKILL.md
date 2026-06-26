# MuskInsider Pro

## 简介
提供一个最小可运行的 HTTP 技能服务，返回演示用的马斯克资讯简报数据与支付链接样例。无外部爬虫与模型推理，纯演示接口。

## 接口
- GET `/` 或 `/health`：服务健康检查，返回 `{"status":"ok","project":"MuskInsider"}`
- GET `/invoke`：返回当日简报预览的演示 JSON
- POST `/invoke`：返回支付链接的演示 JSON（SkillPay 样例 URL）

## 运行
- 启动：`python bare.py`
- 监听：默认 `0.0.0.0:8080`（若平台未注入端口变量，将同时尝试 8080/8000/3000）

## 版本
- v1.0.1
