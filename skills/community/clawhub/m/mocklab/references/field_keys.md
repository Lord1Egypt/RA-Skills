# 字段 Key 命名规范（必须严格遵守）

## 铁律

**Schema 里的 field.name 必须与文档中完全一致，大小写/下划线/驼峰都不能改。**

Python 代码生成的 JSON 响应中，key 的名字就是 Schema 里 field.name 的值。

---

## 命名风格

| 风格 | 示例 | 使用场景 |
|------|------|---------|
| snake_case | `apply_no` `cust_name` `id_card` | 当前项目使用，字段全用下划线 |
| camelCase | `custName` `applyNo` | 部分接口可能使用 |
| 纯大写 | `ID_CARD` `MOBILE` | 少见 |

**必须从接口文档里直接提取 key 名，不要自己转换风格。**

---

## 常见错误（禁止这样写）

| ❌ 错误写法 | ✅ 正确写法 | 说明 |
|-----------|-----------|------|
| `applyNo` | `apply_no` | 文档是下划线就写下划线 |
| `cust_name` | `custName` | 文档是驼峰就写驼峰 |
| `IdCard` | `identityCard` | 以文档为准 |
| `PhoneNumber` | `mobileNumber` | 以文档为准 |
| `user_name` | `userName` | 文档写 userName 就不能写成 user_name |

---

## 正确流程

```
1. 读取接口文档（Markdown / Word 等）
       ↓
2. 找到"请求参数"或"响应参数"表格
       ↓
3. 第一列"参数名"/"字段名"就是 key
       ↓
4. 原封不动抄下来，写入 field.name
       ↓
5. 对照 references/demo__实际返回示例.json 确认格式
```

---

## 典型混淆字段（重点核对）

以下字段在文档中最容易出现命名混淆，必须严格对照文档：

| 易混淆字段 | 检查点 |
|-----------|-------|
| `apply_no` vs `applyNo` vs `applicationNo` | 对照文档表格第一列 |
| `cust_name` vs `custName` vs `customerName` | 注意 cust / customer 拼写 |
| `id_card` vs `idCard` vs `certNo` vs `identityCard` | 身份证号各种写法 |
| `mobile` vs `mobileNumber` vs `phone` vs `phoneNo` | 手机号字段 |
| `car_license` vs `vehicleLicense` vs `licenseNo` | 车牌号字段 |
| `province` vs `provinceCode` vs `province_name` | 注意 code 后缀 |
| `city` vs `cityCode` vs `city_name` | 同上 |

---

## 如何验证 key 是否正确

生成 Schema 后，对照 demo__实际返回示例.json 中相同接口的实际返回，检查：

```json
// demo__实际返回示例.json 中的样子：
"out_apply_no": "20260402000003"
"apply_no": "20260402000002"

// Schema 里必须写成：
{ "name": "out_apply_no", "rule": "..." }
{ "name": "apply_no", "rule": "..." }
```

**如果你写的 Schema 里 key 是 `outApplyNo` 而不是 `out_apply_no`，Python 生成的 JSON 里 key 就变成 `outApplyNo`，与真实 API 不符，前端调不通。**

---

## snake_case vs camelCase 自动转换规则（参考）

```
文档 key 是 snake_case → Schema 写 snake_case
文档 key 是 camelCase → Schema 写 camelCase
文档 key 是 kebab-case → Schema 写 kebab-case

绝对禁止：文档是 snake_case，Schema 写成 camelCase
绝对禁止：自己发明一个文档里没有的字段名
```

---

## 结论

**唯一正确做法：照抄文档第一列，一字不差。**
