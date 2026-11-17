# 配置参考 — 行业雷达 Industry Radar

全部配置走环境变量，启动时读取（改配置需重启服务）。导出示例：

```bash
export IR_LLM_BASE_URL="https://api.example.com/v1"
export IR_LLM_API_KEY="sk-xxxx"
python3 scripts/run_local.py
```

## LLM（可选 — 不配置自动降级为规则引擎）

| 变量             | 默认          | 说明                                                        |
| ---------------- | ------------- | ----------------------------------------------------------- |
| IR_LLM_BASE_URL  | `""`          | OpenAI 兼容网关地址，如华为云 ModelArts Studio 推理服务端点 |
| IR_LLM_API_KEY   | `""`          | API Key。**只通过环境变量注入，绝不写入文件或代码**         |
| IR_LLM_MODEL     | `deepseek-chat` | 模型名，按网关实际支持填写                                |
| IR_LLM_TIMEOUT   | `60`          | 单次 LLM 请求超时（秒）                                     |

两者（BASE_URL + API_KEY）同时非空才启用在线 LLM；`GET /api/config` 可查看当前模式。

## 采集

| 变量                    | 默认值 | 说明                             |
| ----------------------- | ------ | -------------------------------- |
| IR_HTTP_TIMEOUT         | `15`   | 单源 HTTP 超时（秒）             |
| IR_USER_AGENT           | Mozilla/5.0 (compatible; IndustryRadar/1.0; +weekly-briefing) | 抓取 UA |
| IR_MAX_PER_SOURCE       | `15`   | 每源单次最多采集条数             |
| IR_FETCH_FULLTEXT       | `1`    | `1`=抓取全文（摘要质量更高但更慢），`0`=仅用 RSS 摘要 |

## 出站安全与自定义源

| 变量                          | 默认值   | 说明                                                             |
| ----------------------------- | -------- | ---------------------------------------------------------------- |
| IR_ALLOWED_PORTS              | `80,443` | 出站端口白名单（逗号分隔）。放宽会扩大内网探测面，谨慎修改        |
| IR_MAX_FETCH_BYTES            | `3145728` | 单次响应体读取上限（字节，默认 3 MB），超出即截断，防止超大响应拖垮内存 |
| IR_ALLOW_PROXY_FAKEIP         | `0`      | `1`=放行解析到代理 fake-ip 段（198.18.0.0/15）的域名。**默认拒绝**；仅在挂 fake-IP 代理（如 Clash）且确需联网演示时临时开启 |
| IR_BLOCK_PROXY_FAKEIP         | `1`      | 旧开关，兼容用：显式置 `0` 等价于 `IR_ALLOW_PROXY_FAKEIP=1`。新部署请用新变量 |
| IR_ALLOW_CUSTOM_SOURCES       | `1`      | 自定义源总开关；`0` 时 `/api/custom-sources` 写操作返回 403       |
| IR_CUSTOM_MAX_PER_USER        | `10`     | 每用户自定义源数量上限                                           |
| IR_CUSTOM_MAX_PER_SUB         | `5`      | 单订阅最多引用的自定义源数量                                     |
| IR_CUSTOM_DISABLE_AFTER_FAILS | `3`      | 连续抓取失败多少次后自动停用该源                                 |
| IR_CUSTOM_PROBE_TIMEOUT       | `10`     | 录入/复检时的探活超时（秒）                                      |

## 生成策略

| 变量                  | 默认值 | 说明                                         |
| --------------------- | ------ | -------------------------------------------- |
| IR_TOP_K              | `12`   | 每份简报纳入的文章上限                       |
| IR_CLUSTER_THRESHOLD  | `0.18` | token Jaccard 聚类兜底阈值                   |
| IR_MAX_SECTIONS       | `5`    | 简报板块数上限（超出合并进「其他动态」）     |
| IR_DEDUP_HAMMING      | `3`    | simhash 汉明距离去重阈值                     |
| IR_CURATED_PICKS      | `5`    | 编辑精选模式下每期精选的文章条数             |

## 路径与演示账号

| 变量        | 默认值                        | 说明                 |
| ----------- | ----------------------------- | -------------------- |
| IR_DATA_DIR | `app/data`                    | 数据目录             |
| IR_DB_PATH  | `app/data/industry_radar.db`  | SQLite 文件路径      |
| IR_DEMO_USER | `demo`                       | 演示账号用户名       |
| IR_DEMO_PASS | `demo`                       | 演示账号密码         |

> 演示会话机制为演示级（内存 Token），生产使用请自行替换为 JWT + 存储。
