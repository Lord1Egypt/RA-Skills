# okki-email-sync

> OKKI 双向同步：邮件和报价单自动写入 OKKI 跟进记录

## 快速上手

### 前置要求

- Node.js 18+
- OKKI CLI：`/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki.py`
- 向量索引：`/Users/wilson/.openclaw/workspace/vector_store/` (LanceDB)

### 测试连接

```bash
cd scripts
node okki-sync.js test
```

输出示例：
```
🧪 OKKI Sync Module - 测试模式

测试 1: 域名提取
  john@example.com → example.com (公共域：false)
  test@gmail.com → gmail.com (公共域：true)

测试 2: 去重机制
  创建测试记录：test-1234567890
  检查是否已处理：true

测试 3: OKKI CLI 连接
  ✓ OKKI CLI 正常，客户数量：...

测试 4: 向量搜索连接
  ✓ 向量搜索正常

✅ 测试完成
```

---

## 使用场景

### 场景 1：发送邮件后同步

邮件发送成功后，在 OKKI 对应客户下自动创建 `trail_type=102`（邮件）跟进记录。

**已集成到：** `imap-smtp-email/scripts/smtp.js`（自动触发，无需手动调用）

### 场景 2：生成报价单后同步

报价单生成后，在 OKKI 对应客户下自动创建 `trail_type=101`（报价单）跟进记录。

**已集成到：** `quotation-workflow/scripts/generate-all.sh`（自动触发，无需手动调用）

### 场景 3：在自定义 skill 中集成

```javascript
const { matchCustomer, createEmailTrail, syncEmailToOkki } = require('./okki-sync');

// 方法 1：完整流程（推荐）
const result = await syncEmailToOkki({
  uid: 'unique-email-id',
  from: 'customer@example.com',
  to: 'sale-9@farreach-electronic.com',
  subject: 'Product inquiry',
  date: new Date().toISOString(),
  body: 'We are interested in...',
  direction: 'in',
  attachments: []
});

// 方法 2：分步调用
const customer = await matchCustomer('customer@example.com', 'Product inquiry');
if (customer) {
  await createEmailTrail(customer.company_id, { /* ... */ });
}
```

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `scripts/okki-sync.js` | 核心模块（582行）|
| `/tmp/okki-sync-processed.json` | 去重记录 |
| `/tmp/okki-unmatched-emails.log` | 未匹配客户日志 |

---

## 客户匹配策略

1. **域名精确匹配**（confidence=0.95）：`customer@example.com` → 搜索 `example.com` 域名
2. **域名部分匹配**（confidence=0.7）：关键词命中
3. **向量语义搜索**（confidence=score）：基于邮箱+主题+正文内容
4. **匹配失败**：写入 unmatched log，主流程继续

**公共域名黑名单**（跳过域名匹配）：
`gmail.com`, `yahoo.com`, `hotmail.com`, `outlook.com`, `qq.com`, `163.com`, `126.com`, `sina.com`, `sohu.com`, `icloud.com`, `me.com`, `mac.com`, `live.com`, `msn.com`

---

## E2E 测试记录

```
✅ 链路A  邮件发送 → OKKI trail_type=102  trail: 88050591907961
✅ 链路B  报价单生成 → OKKI trail_type=101  trail: 88050865152265 (USD 9730.00)
✅ 链路C  公共域名匹配失败 → unmatched log 写入
✅ 去重  相同 UID 重复触发 → duplicate，不创建重复 trail
```

测试时间：2026-03-24 | 测试者：WILSON
