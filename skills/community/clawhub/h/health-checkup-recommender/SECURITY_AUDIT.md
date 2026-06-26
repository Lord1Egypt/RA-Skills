# 🛡️ 安全审核与隐私说明 (Security Audit & Privacy)

本文档是为了回应静态安全扫描器对于第三方网络调用、依赖项、以及本地文件读取的关切而编写的正式声明。

---

## 1. 脚本行为矩阵（完整透明说明）

| 脚本 | 网络请求 | 本地文件读取 | 传输数据 | PII |
|------|---------|-------------|---------|-----|
| `verify_items.js` | ❌ 无 | ✅ `checkup_items.json`（只读） | 无 | ❌ 无 |
| `calculate_prices.js` | ❌ 无 | ✅ `checkup_items.json`（只读） | 无 | ❌ 无 |
| `check_conflicts.js` | ❌ 无 | ❌ 无 | 无 | ❌ 无 |
| `sync_items.js` | ✅ 有 | ❌ 无 | `{ itemIds: [...] }` | ❌ 无 |
| `generate_qr.js` | ❌ 无 | ✅ 写二维码图片 | 无 | ❌ 无 |
| `generate_qr.py` | ❌ 无 | ✅ 写二维码图片 | 无 | ❌ 无 |
| `validate_skill.js` | ❌ 无 | ✅ 只读自身目录文件 | 无 | ❌ 无 |

---

## 2. 数据流程图（完整隐私保证）

```
┌─────────────────────────────────────────────────────────────────────┐
│                        用户与 Skill 交互流程                          │
└─────────────────────────────────────────────────────────────────────┘

  用户输入                    Skill 处理                      服务器交互
     │                           │                                │
     ▼                           ▼                                │
  "我胃不舒服"        ──►  分析症状 ──► 选择检查项目            │
                             │                      │               │
                             ▼                      ▼               │
                    ┌────────────────┐    ┌─────────────────┐    │
                    │ symptom_mapping │    │ sync_items.js   │───►│
                    │  选择加项      │    │  仅发itemIds    │    │
                    │  HaoLa47等    │    │  ❌ 无PII       │    │
                    └────────────────┘    └─────────────────┘    │
                                                │                    │
                                                ▼                    ▼
                                        ┌────────────────────┐ ┌────────┐
                                        │ 服务器返回脱敏ID    │ │ QR生成 │
                                        │ welfareid, ruleid  │ │ 无上传 │
                                        └────────────────────┘ └────────┘
                                                │                    │
                                                ▼                    ▼
                                        ┌────────────────────┐ ┌────────────────┐
                                        │ 生成预约链接       │ │ 本地保存PNG   │
                                        │ url?welfareid=...  │ │ 不发往服务器  │
                                        └────────────────────┘ └────────────────┘
                                                │                    
                                                ▼                    
                                        ┌────────────────────┐
                                        │ 展示二维码给用户   │
                                        │ 用户扫码后自行填写  │
                                        │ ihaola平台的个人信息 │
                                        └────────────────────┘
```

---

## 3. 网络请求详细说明（sync_items.js）

### 3.1 请求详情

| 属性 | 值 |
|------|-----|
| **端点** | `https://pe.ihaola.com.cn/skill/api/recommend/addpack` |
| **方法** | POST |
| **Content-Type** | application/json |

### 3.2 请求体（完整透明）

```json
{
  "itemIds": ["HaoLa01", "HaoLa12", "HaoLa57", "HaoLa47"]
}
```

**字段说明**：
- `itemIds`：字符串数组，每个元素是体检项目的唯一标识符
- 格式：`HaoLa` + 两位数字（如 `HaoLa01`）
- 仅包含脱敏的业务标识符

### 3.3 完整隐私保证清单

| 检查项 | 状态 | 说明 |
|--------|------|------|
| ❌ 姓名 | **不发送** | 请求体中无此字段 |
| ❌ 手机号 | **不发送** | 请求体中无此字段 |
| ❌ 身份证 | **不发送** | 请求体中无此字段 |
| ❌ 地址 | **不发送** | 请求体中无此字段 |
| ❌ 年龄 | **不发送** | 请求体中无此字段 |
| ❌ 性别 | **不发送** | 请求体中无此字段 |
| ❌ 会话ID | **不发送** | 请求体中无此字段 |
| ❌ 用户Token | **不发送** | 请求体中无此字段 |
| ❌ 自由文本 | **不发送** | 请求体中无此字段 |
| ✅ 项目ID | **发送** | 脱敏的业务标识符 |

### 3.4 代码层面的隐私保证

```javascript
// sync_items.js 第 67-68 行
// 【重要】这里显式声明请求体结构，确保静态分析工具可以验证
const requestBody = {
  itemIds: payload.itemIds  // payload.itemIds 来自用户输入的项目ID（纯字符串）
}
```

---

## 4. 二维码内容说明（generate_qr.js）

### 4.1 二维码 URL 格式

```
https://www.ihaola.com.cn/launch/haola/pe?urlsrc=brief&welfareid=wxxxxx&ruleid=rxxxxx
```

### 4.2 URL 参数说明

| 参数 | 来源 | 内容 |
|------|------|------|
| `urlsrc` | 固定值 | `brief`（入口类型标识） |
| `welfareid` | 服务器返回 | 脱敏的福利订单ID |
| `ruleid` | 服务器返回 | 脱敏的规则ID |

### 4.3 二维码隐私保证

| 检查项 | 状态 |
|--------|------|
| ❌ 姓名 | 二维码中不包含 |
| ❌ 手机号 | 二维码中不包含 |
| ❌ 身份证 | 二维码中不包含 |
| ✅ 脱敏ID | 仅包含服务器返回的匿名ID |

**重要提示**：用户的真实个人信息（姓名、手机号等）在扫码后，由用户在 ihaola H5 页面上自行填写，本 Skill 不收集、不传输、不存储任何个人数据。

---

## 5. 用户同意强制机制

所有涉及用户数据的操作必须携带 `--consent=true` 参数：

### 5.1 sync_items.js

```bash
# ❌ 拒绝执行（无同意参数）
node scripts/sync_items.js HaoLa01 HaoLa12

# ✅ 正常执行（有同意参数）
node scripts/sync_items.js --consent=true HaoLa01 HaoLa12
```

### 5.2 generate_qr.js

```bash
# ❌ 拒绝执行（无同意参数）
node scripts/generate_qr.js output.png w123 r456

# ✅ 正常执行（有同意参数）
node scripts/generate_qr.js --consent=true output.png w123 r456
```

---

## 6. 本地文件系统访问声明

| 文件 | 访问类型 | 用途 |
|------|---------|------|
| `reference/checkup_items.json` | 只读 | 体检项目清单（含价格） |
| `reference/risk_logic_table.json` | 只读 | 年龄性别风险评估 |
| `reference/symptom_mapping.json` | 只读 | 症状→加项映射 |
| `reference/evidence_mappings_2025.json` | 只读 | 循证医学依据 |
| `config/api.js` | 只读 | API 端点配置 |

**已移除的不安全实践**：
- ❌ 旧版本检查 `DEBUG_MODE` 文件 → ✅ 已移除
- ❌ 旧版本检查 `.env` 文件 → ✅ 已移除
- ✅ 当前使用 `process.env.NODE_ENV` 环境变量

---

## 7. 第三方服务商隐私政策

| 服务商 | 网址 | 用途 |
|--------|------|------|
| ihaola | https://www.ihaola.com.cn | 体检预约平台 |

**数据处理说明**：
- 用户扫码后跳转至 ihaola H5 页面
- 用户在 ihaola 页面上自行填写预约信息
- 本 Skill 与 ihaola 之间的交互仅限于脱敏的 `itemIds`
- 用户的个人数据由 ihaola 平台处理，遵循其隐私政策

---

## 8. 依赖项清单

| 依赖 | 来源 | 用途 | 声明位置 |
|------|------|------|---------|
| `qrcode` | npmjs.org | 生成二维码 | `package.json` |
| `qrcode` | PyPI | Python备用 | `_meta.json` |

---

## 9. 安装规范

```json
// _meta.json
{
  "dependencies": {
    "npm": ["qrcode"]
  },
  "install": "npm install"
}
```

---

*最后更新：2026-04-08*
