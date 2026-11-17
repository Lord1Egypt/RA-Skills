# ADDING_A_PLATFORM — 新增一个房源平台扫描模板

对照 career-ops 的 `ADDING_A_PROVIDER.md`：本指南是 `scrapers/` 的模块契约。目标仍然是**零 token、零依赖、确定性**——模块只做 URL 识别与清单声明，抓取由 AI 按清单完成。

## 1. 建文件

`scrapers/<平台id>.mjs`，default export 满足：

```js
export default {
  id: 'myplatform',          // 全局唯一，注册表 key；与文件名一致
  name: '平台中文名',
  domains: ['myplatform.com'],  // 便于人读；识别逻辑以 detect() 为准
  fields: [/* AI 抓取清单，中文，一项一条 */],
  transaction: {
    pattern: 'https://…',    // 平台成交页 URL 模板；无公开成交明细则 null
    reliability: '成交数据', // 该成交源的最高可靠度档位；估算行情必须写「挂牌数据」
    coverage: '覆盖范围如实描述：覆盖谁、不覆盖谁',
  },
  notes: [/* 反爬强度、假房源风险、条款约束——scan 模式抓取前必读 */],
  detect(url) {
    // 返回 { page_type, city_code, listing_id } 或 null（不是本平台）
  },
};
```

`fields` 可复用 `_fields.mjs` 的 `COMMON_LISTING_FIELDS` 再追加平台特有项（如贝壳系的"房源核验码"）。

## 2. `detect()` 纪律

- **域名优先**：先判域名后缀，再按路径段分类页面类型 `listing / transaction / transaction_list / community / new_home / market / search / unknown`；
- **容错**：URL 解析包 try/catch（参考 `fang.mjs`），任何异常返回 null 而不是抛出（注册表会兜，但别依赖）；
- **不确定的路径语法宁可放宽**（匹配前缀），把精确性交给 `notes` 里的一句"以实际页面为准"；
- `city_code` 取子域名原样（`sh` / `shanghai`），城市名映射由 scan 模式做，模块不做；
- 同集团多域名（如贝壳系）：用 `_` 前缀工厂合并语法（参考 `_ke-group.mjs`），但**每个平台仍各建一个文件**，便于单独禁用。

## 3. `transaction` 纪律

- 平台没有公开成交明细就写 `pattern: null`，`reliability` 封顶「挂牌数据」——**宁可降档，不可虚标**；
- `coverage` 必须说清覆盖边界（如"仅该集团经手成交，非全市全量"）；
- 成交价交叉验证的另一个（通常更权威的）来源是政务平台：去 `templates/official-sources.cn.yml` 补条目，不写进平台模块。

## 4. 合规底线（写进 notes）

每家平台的 `notes` 必须包含：仅限个人购房研究、遵守平台条款、不批量抓取、不绕验证码/登录墙、不公开再分发页面内容。已知强反爬或假房源风险也要写明。

## 5. 测试清单（PR 前）

```bash
# 每种 page_type 至少 1 条真实样例 URL，逐条核对输出
node scripts/scan.mjs detect 'https://…'

# 未命中时必须优雅落到 generic
node scripts/scan.mjs detect 'https://example.com/x'

# 组装一条最小记录走通归一化 + 交叉验证（含一条故意单位错误）
node scripts/scan.mjs normalize /tmp/record.json
node scripts/scan.mjs crosscheck /tmp/record.json

# doctor 必须仍然全绿
node scripts/doctor.mjs
```

## 6. 同步文档

- `scrapers/README.md` 的「当前平台」表加一行；
- `modes/scan.md` Step 0 的已识别平台清单提及（如改动平台总数）；
- 涉及新数据源类型时检查 `modes/scan.md` 的 schema 是否需要扩展（schema SoT 在该文件，键名变更需同步 `_fields.mjs`）。
