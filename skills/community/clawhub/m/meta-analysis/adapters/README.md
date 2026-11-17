# adapters/ — 计算出口层（ct-base §16.9 架构预留）

> 本目录是 **meta-analysis 技能** 的分析计算出口层。**发布形态为 coze-only**（2026-08-19 决策）：
> 所有数值计算经 coze 元分析工作流，本地 LLM 仅做需求标准化/数据整理/结果呈现，**最终用户无需安装 R**。
> 回退逻辑已于 2026-08-26 取消：coze 不可达 / 未授权时直接返回结构化错误，**不再兜底本地引擎**。

## 路由策略（coze 唯一路径，无回退）

```
                 ┌─────────────────────────────────────────────┐
   分析请求 ──────▶│ adapters/run_analysis.py  (统一入口)         │
 (task/data/…)    │   唯一对外路径 = coze                         │
                 └───────────────┬─────────────────────────────┘
                                 │
                   coze_client.run_meta ── 成功 ──▶ _source="coze"
                                 │ 失败（网络/HTTP/空响应/未授权）
                                 ▼
                          返回结构化错误（不再回退本地）
```

- **发布形态**：唯一路径 = `coze`。coze 失败时直接返回 `{status:"error", ...}`，由上层决定如何提示用户。
- **`_source` 字段**：仅 `"coze"`（成功）或缺失（结构化错误，不标 local_fallback）。
- **开发者/复现**：本地无独立计算引擎。所有数值计算由 coze 端 R 引擎完成；`_dev/` 仅作开发调试占位（历史本地 R 引擎 `local_engine.py` 已于 2026-09-01 按架构终态原则删除）。

## 文件

```
adapters/
├── run_analysis.py        # 统一前端：唯一对外路径 = coze
├── literature_probe.py    # ★ 选题去重自包含探针：Europe PMC REST（Cochrane+PubMed 层真实 hit_count），零依赖、不依赖其他技能
├── coze_client.py         # Coze /run 客户端（唯一路径）：信封打包 / 响应解析
├── coze_cases/            # 3 个冒烟案例（快速自测）
├── coze/          # ★ coze 项目本地镜像（与 coze 远端双向同步的唯一源，2026-08-19 统一放置）
│   ├── coze_contract.md   #   接口契约（§16.7 红线：不随技能发布，已 ignore）
│   ├── src/r_engine/*.R   #   R 引擎（run_task.R 等，coze 端运行本体）
│   ├── scripts/           #   部署脚本（http_run.sh / setup.sh 等）
│   └── docker/ assets/    #   镜像/依赖清单
├── _dev/                  # ★ 开发调试用，已 ignore（不随发布包分发）；历史本地 R 引擎已删除
└── README.md              # 本文件
```

## coze 项目镜像：双向同步约定（2026-08-19 统一）

> **`adapters/coze/` 是 coze 远端代码在本地唯一的同步源。** 所有 coze 端代码变更都从这里进出：
> 本地改代码 → 打包部署 coze；coze 平台导出 → 覆盖回此目录。**不再使用工作区 `coze_meta_project/` 作为主镜像**（保留为历史快照）。

- **本地 → coze**：改 `adapters/coze/` 内文件 → `tar -czf coze_final_YYYYMMDD.tar.gz .`（在镜像目录内）→ 上传 coze 平台 → vefaas 重部署 → 线上 96 例复测。
- **coze → 本地**：coze 平台导出 project → 解包覆盖 `adapters/coze/` → `diff -r` 与镜像内 `src/r_engine/` 比对确认。
- **发布排除**：`adapters/coze/` 已加入 `.gitignore` / `.clawhubignore`，**不随技能发布**（coze_contract.md 属 §16.7 红线）。
- **一致性基准**：`adapters/coze/src/r_engine/` 为唯一本地引擎（技能根 `r_engine/` 已删），与 coze 远端同步。

## 配置（环境变量）

| 变量 | 说明 | 默认 |
|------|------|------|
| `COZE_META_ENDPOINT` | coze 工作流 `/run` 地址（2026-08-26 改造，主工作流回切 ct-meta） | `https://ct-meta.coze.site/run` |
| `COZE_META_TOKEN` | 可选 Bearer 鉴权令牌 | 空（不带 Authorization） |
| `COZE_META_TIMEOUT` | 请求超时（秒） | `600` |

## 用法

```python
import sys; sys.path.insert(0, "adapters")
from run_analysis import run_analysis

# 唯一路径：coze 云端 R 计算
out = run_analysis(
    task="pairwise_meta",
    data={"rows": [{"study": "A", "event_exp": 12, "n_exp": 100,
                    "event_ctrl": 20, "n_ctrl": 100}]},
    params={"sm": "OR", "model": "REML"},
    figure={"plots": ["forest"]},
)
# 成功：out["_source"] == "coze"
# 失败：out["status"] == "error"（coze 不可达/未授权），无 _source 回退
```

CLI 等价：`python adapters/run_analysis.py request.json`

> **🚫 调用方约束（2026-08-30）**：请**始终经 `run_analysis` / `scripts/run_meta.py` 调用**——它们自动注入有效 `query_origin`（主机名 SHA-256，`[debug:]sha256:<64hex>`）。**不要**用 curl / Postman 直接 POST `/run`；如确需裸调，请求体**必须带合法 `query_origin`**（`coze_client._assert_query_origin` 已在客户端出站层硬拦截空归因，但裸 POST 不经该守卫）。空归因会绕过按 `query_origin` 计的限流，且飞书日志无法溯源。

## 红线

- **数值判断红线**：R 计算的数值结论（合并效应、I²、排序等）由 coze 端 R 产出，
  本层仅解析结构（status/stats/figures[].svg/warnings/notes），绝不读取或改写数值。
- **接口契约**：见 coze 项目的 `coze_contract.md`（不随技能发布，遵循 ct-base §16.7）。
  镜像内 `src/r_engine/` 是 coze 远端引擎的字节级镜像，靠该契约保持同步。
- **发布红线**：coze 接口契约 / system prompt / ops 文档一律不随技能发布（ct-base §16.7）。
- **回退红线（2026-08-26 起）**：运行路径不再调用任何本地计算引擎；
  历史本地 R 引擎 `adapters/_dev/local_engine.py` 已于 2026-09-01 删除，无本地回退。
