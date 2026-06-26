# 规格信息查询 — `temu.local.goods.spec.info.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_manage_spec_info_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=7e396281b713436c93363864b6b826aa |
| **网关** | `POST /temu/proxy`，`type`=`temu.local.goods.spec.info.get`，业务载荷放在 Body 的 `params` |

**Description:** 按规格 ID 列表查询规格信息（可配合 `language` 取多语言展示）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── language
    └── specIdList          ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| language | STRING | 否 | Language |
| specIdList | LONG[] | **是** | Specification Id List |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "specIdList": [1001, 1002]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "language": "en",
    "specIdList": [1001]
  }
}
```

> **勿**使用旧文档中的 `parentSpecId`、`languages`（单数/复数混用）；官方入参仅为 **`language`** + **`specIdList`**（LONG[]，必填）。

---

## Response（Temu `body` 解析后）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information（子字段在 Partner 文档中展开） |

官方 Response 表中 **`result` 未在提供的片段中展开**，具体规格信息字段名与结构以 Partner 后台为准。

---

## 示例

```bash
python scripts/eu_manage_spec_info_get.py '{
  "accessToken": "TOKEN",
  "request": {
    "specIdList": [1001, 1002],
    "language": "en"
  }
}'
```
