# 行业雷达 Industry Radar

输入「行业词 × 技术词」，输出一份编辑精选式的行业情报周报。

自带 FastAPI 后端 + Vue 前端（免构建静态托管）+ SQLite 落库，一条命令启动，浏览器开箱即用；LLM 可选，不配置也能跑通全流程。

## 能力链路

```
行业词 × 技术词 → 14 源 RSS 采集 → 清洗 / 全文抽取 → simhash 去重
              → 相关性打分 → 主题聚类 → LLM 摘要（可降级）
              → 编辑精选式 Markdown 周报
```

- 两种周报风格：`standard` 标准周报 / `curated` 编辑精选（精选 5 篇 + 上榜理由 + 星级）
- 自定义 RSS 源：录入即探活，配额与连续失败自动停用
- LLM 可选：配置任意 OpenAI 兼容网关（含华为云 ModelArts Studio）即用在线摘要

## 快速开始

```bash
python3 scripts/run_local.py
# Web 界面 http://127.0.0.1:8000   演示账号 demo / demo
# API 文档 http://127.0.0.1:8000/docs
```

首次启动自动建 venv、装依赖、初始化 SQLite，并预置示例订阅「新能源汽车 × 固态电池」。

## 目录结构

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | Skill 入口：工作流、关键陷阱、安全与数据边界 |
| `app/backend/` | FastAPI 后端（采集 / 去重 / 打分 / 聚类 / 摘要 / 存储 / 出站防护） |
| `app/frontend/` | Vue 前端（无需构建，直接静态托管） |
| `references/` | API 参考、配置参考、架构说明 |
| `demo/` | 两份真实生成的编辑精选式周报样例 |
| `scripts/run_local.py` | 一键启动器（建 venv / 装依赖 / 起 uvicorn） |

## 安全设计

- 所有出站请求统一走 `app/backend/net_guard.py`：仅 http/https，禁回环 / 私网 / 链路本地（含 `169.254.169.254`）/ 组播 / 保留段，重定向逐跳复检，响应体上限 3MB
- DNS 校验结果固定到连接层（Host 头与 TLS SNI/证书照旧校验），连接建立后再复核对端 IP，杜绝 DNS 重绑定（TOCTOU）
- Fake-IP 网段 `198.18.0.0/15` 默认拒绝，需显式 `IR_ALLOW_PROXY_FAKEIP=1` 放行
- 不读取 `HTTP_PROXY` / `HTTPS_PROXY`，避免流量被环境变量劫持
- LLM 返回内容按不可信输入处理：结构化解析失败或字段类型不符时整体回落规则合成，不抛错
- LLM API Key 仅经环境变量 `IR_LLM_API_KEY` 注入，不落盘、不写日志

完整环境变量见 `references/config-reference.md`。

## 数据外发提示

启用 LLM 即外发：文章标题 / 正文与订阅关键词会发送到 `IR_LLM_BASE_URL` 指定的第三方服务商。涉密或未公开情报场景请保持 LLM 未配置状态（自动降级为本地规则引擎）。删除订阅不会清理 `app/data/briefings/*.md` 历史简报文件。

## License

MIT，见 `LICENSE`。
