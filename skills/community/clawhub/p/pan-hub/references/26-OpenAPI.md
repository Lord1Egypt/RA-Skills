# OpenAPI / Agent 稳定接口（v0.6.1-R6~R8）

本技能不内置 HTTP API 服务，但 CLI 的 --json 输出等价于稳定语义，供上层 Agent/脚本消费。所有响应不带账号明文凭据。

## 端点映射（CLI JSON = 只读接口）

| 语义 | CLI 命令 | 响应概要 |
|---|---|---|
| health | pan.py doctor --json | checks、config(打码)、hints、建议命令 |
| detect | pan.py detect <url> --json | drive/key、推荐引擎、reference |
| dirs | pan.py dirs --json | default_root、example_task_dir |
| plans | pan.py get <url> --dry-run --json | 下载计划（只读）、missing、warnings |
| reports | pan.py serve 后 /api/reports | 已生成 下载报告.json 汇总 |
| 事件流 | pan.py get <url> --events | 逐步 NDJSON，每行含 rc/耗时 |
| notify | pan.py notify send ... | 通知 dry-run/发送结果 |

## 任务状态模型

每次下载产生 下载报告.json：ok / url / drive / engine / tier / target / started / finished / elapsed / steps / missing / warnings。steps[] 每项含 index/engine/rc/elapsed/error。

## 认证与安全

- 认证发生在网盘侧（系统凭据库 / AList / 官方授权），这里只传引用与分享提取码，不回传密码/Token。
- MCP 工具与 serve 只读，不暴露系统凭据。
- 公司数据不通过本接口上传。
