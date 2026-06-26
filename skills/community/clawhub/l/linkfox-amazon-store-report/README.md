# Amazon Store Report Skill

亚马逊店铺 **报告获取** Skill：端到端自动化拉取库存 / 订单 / 销售 / 财务 / FBA 等 95+ 种报告。

> ⚠️ **本 skill 依赖 `linkfox-amazon-store-auth`**（授权与令牌管理）。未安装时请先安装依赖 skill，`scripts/get_report.py` 启动时会做自动校验。

## 📋 目录结构

```
linkfox-amazon-store-report/
├── SKILL.md                          # Skill 主文档（含 Prerequisites）
├── _meta.json                        # Skill 元数据（声明依赖）
├── README.md                         # 本文件
├── references/
│   ├── api.md                        # Developer Proxy API 说明
│   ├── report-types.md               # 完整报告类型（95+ 种）
│   └── report-types-basic.md         # 常用报告精简版
└── scripts/
    ├── README.md                     # 脚本使用指南
    ├── check_auth_dependency.py      # 依赖探测脚本
    └── get_report.py                 # 报告获取（启动时自动跑依赖检查）
```

## 🔗 依赖关系

| 本 Skill | 依赖 |
|----------|------|
| `linkfox-amazon-store-report` | `linkfox-amazon-store-auth` |

**依赖未安装时的处置**：
1. `get_report.py` 启动时以 **exit code 42** 退出，并在 stderr 以 `DEPENDENCY_MISSING:` 开头输出 JSON 指引
2. 上层 agent 解析该信号后：优先调用本地 skill 安装工具自动装 `linkfox-amazon-store-auth`；否则引导用户手动安装
3. **安装完成后再重跑本 skill**

## 🚀 快速开始

> 前置条件：已通过 `linkfox-amazon-store-auth` 授权了至少一个店铺。

```bash
python scripts/get_report.py '{
  "sellerId": "A1EC6SZ7XAMURH",
  "region": "NA",
  "reportType": "GET_MERCHANT_LISTINGS_ALL_DATA",
  "marketplaceIds": ["ATVPDKIKX0DER"]
}'
```

成功结束后，脚本会启动短时 **本机 HTTP** 服务，在 **stderr** 与 **stdout JSON** 中给出 **`extractedFileHttpUrl`**，用于在浏览器下载**已解压**后的报告文件（默认保持 `serveSeconds` 秒，仅 `127.0.0.1` 可访问）；同时给出 **`downloadPath`** 与 **`localFileUri`**。详见 `scripts/README.md`。

## 🌍 支持的区域

- **NA**：美国、加拿大、墨西哥
- **EU**：英国、德国、法国、意大利、西班牙等
- **FE**：日本、澳大利亚、新加坡、印度

## 🔄 版本历史

- **v1.0.3**（2026-04-24）
  - 展示保存位置时同时明确输出**文件名**（stderr + JSON 字段 `fileName`）

- **v1.0.2**（2026-04-24）
  - `get_report.py`：默认启动本机临时 HTTP，生成 **`extractedFileHttpUrl`** 供浏览器下载**已解压**文件；不再默认暴露 Amazon 源 URL（可选 `includeAmazonSourceUrl`）

- **v1.0.1**（2026-04-24）
  - `get_report.py`：完成后明确展示本地保存路径，并在 JSON / stderr 中输出 Amazon 预签名直链与本机 `file://` URI

- **v1.0.0**（2026-04-24）
  - 从早期综合亚马逊 skill 拆分而来（报告部分）
  - 新增依赖探测脚本 `check_auth_dependency.py`
  - `get_report.py` 启动时自动进行依赖校验

## 📄 许可

本 Skill 是 LinkFoxAgent 项目的一部分。
