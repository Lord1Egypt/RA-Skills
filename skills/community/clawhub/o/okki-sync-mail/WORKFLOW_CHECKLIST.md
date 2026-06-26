# ✅ 开发信发送完整工作流检查清单

> **版本：** 1.0 (2026-03-15 修复后)  
> **适用范围：** Farreach 外贸开发信发送  
> **脚本状态：** ✅ 已修复字段兼容性问题

---

## 🎯 完整工作流（6 步）

### Step 1: 收集客户信息 ⭐
**来源：** OKKI CRM / 名片 / 网站

```markdown
- [ ] 公司名称（英文全称）
- [ ] 详细地址
- [ ] 国家/地区
- [ ] 联系人姓名（如有）
- [ ] 邮箱地址
- [ ] 电话（如有）
- [ ] 行业/业务类型
```

**OKKI 查询命令：**
```bash
cd /Users/wilson/.openclaw/workspace/xiaoman-okki/api
python3 okki_cli.py query_company <company_id>
```

---

### Step 2: 创建报价单数据文件 ⭐⭐⭐

**位置：** `/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/<客户简称>.json`

**模板：** 复制 `examples/template-standard.json` 后修改

**必填字段：**
```json
{
  "quotationNo": "QT-20260315-003",
  "date": "2026-03-15",
  "validUntil": "2026-04-14",
  "customer": {
    "name": "客户公司名",
    "address": "客户地址",
    "country": "国家",
    "email": "客户邮箱"
  },
  "products": [
    {
      "description": "产品描述",
      "specification": "规格参数",
      "quantity": 1000,
      "unitPrice": 3.50
    }
  ],
  "terms": {
    "moq": "500 pcs (negotiable)",
    "delivery": "7-15 days",
    "payment": "T/T, L/C, PayPal",
    "packaging": "Gift box, kraft box, PE bag"
  }
}
```

**✅ 脚本已兼容多种字段名：**
- `customer.name` 或 `customer.company_name` ✅
- `product.unitPrice` 或 `product.unit_price` ✅
- `terms` 字典或列表 ✅
- `quotationNo` 或 `quotation.quotation_no` ✅

---

### Step 3: 生成专属报价单 ⭐⭐⭐

**命令：**
```bash
cd /Users/wilson/.openclaw/workspace/skills/quotation-workflow
bash scripts/generate-all.sh data/<客户数据>.json QT-<日期>-<客户简称>
```

**示例：**
```bash
bash scripts/generate-all.sh data/specialized-computers-usa.json QT-20260315-002-SpecializedComputersUSA
```

**生成文件：**
- `QT-xxx.xlsx` - Excel 版本
- `QT-xxx.docx` - Word 版本
- `QT-xxx.html` - HTML 版本（现代设计）
- `QT-xxx-HTML.pdf` - HTML 转 PDF
- `QT-xxx-Excel.pdf` - Excel 转 PDF

---

### Step 4: 添加页码并检查 ⭐⭐⭐

**添加页码：**
```bash
python3 scripts/add-pagenumbers.py \
  data/QT-xxx-HTML.pdf \
  data/QT-xxx-Final.pdf
```

**✅ 必须检查的内容（打开 PDF 确认）：**
```markdown
- [ ] 客户公司名正确显示（不是 `_________________`）
- [ ] 客户地址正确显示
- [ ] 产品单价正确显示（不是 `$0.00`）
- [ ] 总金额计算正确
- [ ] 贸易条款完整显示（不是空白）
- [ ] 报价单号正确
```

**❌ 如发现空白，检查：**
1. 数据文件字段名是否正确
2. JSON 格式是否有效（用 JSON 验证器）
3. 脚本是否为最新版（已修复字段映射）

---

### Step 5: 生成个性化邮件正文 ⭐⭐⭐

**原则：** 模板只参考结构，内容必须定制

**邮件结构：**
```markdown
1. 问候 + 寒暄（提及客户公司名、所在地、行业）
2. 公司介绍（Farreach 核心优势）
3. 附件说明（产品目录 + 报价单）
4. 行动号召（邀请询价、提供免费样品）
5. 签名（联系方式 + 核心优势摘要）
```

**禁止：**
- ❌ 直接照抄模板中的其他客户信息
- ❌ 使用 `development-email.html` 直接发送

**方法：**
- 方法 A：修改 HTML 模板后使用 `--body-file`
- 方法 B：直接用 `--body` 参数发送定制 HTML

---

### Step 6: 发送完整邮件 ⭐⭐⭐

**确认附件：**
```bash
# 产品目录
ls -lh "/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf"

# 报价单（必须是 HTML 转的 PDF）
ls -lh /Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/QT-*-Final.pdf
```

**发送命令：**
```bash
cd /Users/wilson/.openclaw/workspace/skills/imap-smtp-email

node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "🔌 Premium Cable Solutions - Farreach Electronic" \
  --html \
  --body-file "/path/to/customized-email.html" \
  --attach "/Users/wilson/.openclaw/workspace/obsidian-vault/Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf,/Users/wilson/.openclaw/workspace/skills/quotation-workflow/data/QT-xxx-Final.pdf"
```

**路径有空格时必须用引号包裹！**

---

### Step 7: 更新 OKKI 跟进记录

**命令：**
```bash
cd /Users/wilson/.openclaw/workspace/xiaoman-okki/api
python3 okki_cli.py add_trail <company_id> "发送开发信 - 附上产品目录和专属报价单 QT-xxx。等待客户回复。"
```

---

## 🚫 禁止事项（血泪教训）

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| ❌ 使用 `examples/` 目录的示例报价单 | 客户名/价格空白，不专业 | 必须为客户生成专属报价单 |
| ❌ 直接照抄模板内容 | 其他客户信息泄露，像垃圾邮件 | 根据客户信息定制内容 |
| ❌ 生成后不检查 PDF | 空白内容已发送 | 必须打开 PDF 检查关键字段 |
| ❌ 分多次发送邮件 | 客户体验差，显得混乱 | 一次性发送完整邮件 |
| ❌ 附件路径不用引号 | 路径解析失败 | 有空格时用双引号包裹 |

---

## ✅ 记忆口诀

```
开发信三件套：
1. 个性化正文（定制寒暄）
2. 产品目录（SKW 2026）
3. 专属报价单（生成后检查）

发送前检查：
客户名 ✅  价格 ✅  条款 ✅  附件 ✅

脚本已兼容：
unitPrice / unit_price ✅
customer.name / company_name ✅
terms 字典 / 列表 ✅
```

---

## 📁 相关文件位置

| 文件 | 位置 |
|------|------|
| 报价单模板 | `quotation-workflow/examples/template-standard.json` |
| 报价单数据 | `quotation-workflow/data/<客户>.json` |
| 生成的报价单 | `quotation-workflow/data/QT-*.pdf` |
| 产品目录 | `Farreach 知识库/02-产品目录/SKW 2026 catalogue-15M.pdf` |
| 邮件模板 | `mail-templates/development-email.html`（仅参考结构） |
| 教训文档 | `imap-smtp-email/LESSONS_LEARNED.md` |

---

## 🔧 脚本修复记录 (2026-03-15)

**修复文件：** `quotation-workflow/scripts/generate_quotation_html.py`

**修复内容：**
1. ✅ 支持 `customer.name` 和 `customer.company_name`
2. ✅ 支持 `product.unitPrice` 和 `product.unit_price`
3. ✅ 支持 `terms` 字典格式和列表格式
4. ✅ 支持 `quotationNo` 和 `quotation.quotation_no`

**修复前问题：** 字段名不匹配导致客户名/价格/条款空白

---

**创建时间：** 2026-03-15 10:00  
**创建者：** WILSON  
**目的：** 确保每次开发信发送都遵循正确流程，避免重复犯错
