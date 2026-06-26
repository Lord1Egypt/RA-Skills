# 领星 OpenAPI — 调用说明（LinkFox 包装入口）

本页对应 LinkFox skill **`linkfox-lingxing-erp`**：由 LinkFox 仓库收录领星官方材料并做路径说明，**请求仍直连领星**（非 LinkFox 工具网关）。完整接口清单、参数与返回字段见同目录下各专题文档；本页仅汇总认证、域名与脚本用法。

## Base URL

- **Host**: `https://openapi.lingxing.com`
- 具体路径由 `scripts/lingxing.py` 内 `SPECIAL_PATHS` 与各模块约定决定，详见 `SKILL.md` 与各 `references/*.md`。

## 认证与凭证

| 变量 | 必填 | 说明 |
|------|------|------|
| `LINGXING_APP_ID` | 是 | 领星开放接口 AppID |
| `LINGXING_APP_SECRET` | 是 | 领星开放接口 AppSecret |
| `LINGXING_SID` | 否 | 默认店铺 SID；未在 `--params` 中写 `sid` 时由脚本注入 |

在领星 ERP → **开放接口** 中创建应用并获取密钥；IP 白名单按领星文档配置。

## 推荐执行方式

在 skill 根目录 `skills/linkfox-lingxing-erp/` 下：

```bash
export LINGXING_APP_ID=...
export LINGXING_APP_SECRET=...

python3 scripts/lingxing.py --list-stores
python3 scripts/lingxing.py --api help
python3 scripts/lingxing.py --api <接口名> --params '<JSON>'
```

支持 `--all`、`--page-size` 等，见 `SKILL.md`「使用方式」与 `scripts/lingxing.py` 头部说明。

## 依赖

脚本需 **`requests`** 与 **`pycryptodome`**：

```bash
pip install requests pycryptodome
```

## 分模块参考索引

| 文档 | 内容 |
|------|------|
| `newad-report.md` | 新广告报表 SP/SB/SD 等 |
| `basedata.md` | 广告基础数据 |
| `basicdata-full.md` | 基础数据全量 |
| `sale-ops.md` / `sale-full.md` | 销售订单、Listing、促销等 |
| `product.md` | 产品 |
| `finance.md` | 财务利润、结算、发票等 |
| `statistics.md` | 统计报表 |
| `fba.md` / `fbasug.md` / `fbalimit.md` | FBA 发货、补货建议与限制 |
| `sourcedata.md` | 亚马逊源表 |
| `purchase.md` | 采购 |
| `warehouse.md` | 仓库库存 |
| `service.md` | 客服、Review 等 |
| `logistics.md` | 物流 |
| `tools.md` | 工具类 |
| `vc.md` | VC |
| `targetmanage.md` | 目标管理 |
| `multiplatform-ads.md` / `multiplatform-v2.md` | 多平台广告与订单 |

## Feedback

若需向 LinkFox 反馈本 skill 使用体验，可按仓库内其他 skill 的约定调用 Feedback API（`skillName` 使用 `linkfox-lingxing-erp`）。
