---
name: amazon-aba-kw-snapshot
description: "ABA关键词周快照。单精确词最新周或指定周SFR+Top ASIN点击/转化份额速查导出。"
---

# amazon-aba-kw-snapshot · 关键词周快照

> ABA **薄场景壳**（Shell B）。取数唯一依赖 L3：`linkfox-aba-data-explorer`。  
> 不重拆 API；只固化入参 schema、preset 与 analysisDescription 模板。

## 专家角色

**ABA关键词速查分析师**

## 目标

- 将用户的「关键词周快照」意图稳定映射为 ABA 智能查询
- 输出可表格化的 SFR / 份额 / ASIN 结果；可选 CSV 下载
- 越界需求明确拒做并导流

## 输入

| 参数 | 必填 | 说明 |
|------|------|------|
| region | 否 | 默认 US |
| keyword | 是 | 单个精确关键词 |
| week | 否 | latest 或周起始日 |
| top_k_asin | 否 | 默认 3 |
| download | 否 | 是否 createDownloadUrl |
| preset | 否 | preset 名 |

### Preset（展示场景名）

关键词ABA速查、精确词最新周快照、Top3导出(精确)

## 工作流程

1. 校验必填参数；`region` 默认 `US`
2. 若用户要绝对搜索量/销量/BSR/上架日 → **拒做**，导流 Keepa / Jungle Scout / 前台 SERP
3. 按 Shell B + preset 拼装 `analysisDescription`（见 `scripts/aba_common.py`）
4. 调用网关 `aba/intelligentQuery`（脚本封装）
5. 展示 `tables`；若有 `downloadUrl` 明确告知；提醒 **SFR 数值越小越热**
6. 失败时展示 `msg`/`errmsg`，建议收紧条件后重试

## 脚本

```bash
export LINKFOXAGENT_API_KEY=...
python3 scripts/shell_b.py '<JSON>'
```

示例见 `references/examples.json`。

## 输出

- `tables[].data` 行数据（searchTerm / searchFrequencyRank / clickedAsin / clickShare / conversionShare / …）
- 可选 `downloadUrl`（≤10000 行）
- `_meta.analysisDescription` 便于复盘

## 限制 / 边界

- 仅周粒度 ABA 搜索词；约 3 年、15 站点
- **无**绝对搜索量、销量、价格、BSR、上架日
- `contains` ≠ 语义相关词
- 站点是参数不是 skill；默认 US
- 禁止在 skill 内写死密钥

## 与其它 skill

| 需求 | 用 |
|------|-----|
| 自由/复杂 ABA 自然语言 | `linkfox-aba-data-explorer` |
| 前台 SERP 竞争 | `linkfox-amazon-search-competition` |
| 销量/价格史 | Keepa / Jungle Scout 系 |

## 契约

见工厂 `references/aba-six/contracts/B-amazon-aba-kw-snapshot.json`
