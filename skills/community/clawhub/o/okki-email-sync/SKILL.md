---
name: okki-email-sync
description: "Synchronize email activities and quotation events with OKKI CRM as follow-up trail records. Automatically matches emails to CRM customers via domain lookup and vector search, creates trail records (email type=102, quotation type=101), and deduplicates entries. Requires OKKI CRM API access and optional vector search setup. Use when you need to automatically log email communications and quotation events in your CRM."
---

# okki-email-sync

## Description

**OKKI 双向同步**：邮件和报价单自动写入 OKKI CRM 跟进记录。

这是一个**集成模块**，不作为独立 skill 运行，而是 hook 到现有的 `imap-smtp-email` 和 `quotation-workflow` skills 中，实现：

- 发送邮件后自动在 OKKI 对应客户下创建 `trail_type=102`（邮件类型）跟进记录
- 生成报价单后自动在 OKKI 对应客户下创建 `trail_type=101`（报价单类型）跟进记录
- 客户匹配策略：域名精确匹配 → 公共域名黑名单过滤 → 向量搜索回退
- 去重机制：以 UID 为 key，防止重复写入跟进记录
- 未匹配客户写日志，不阻断主流程

---

## Core Module

**主文件：** `scripts/okki-sync.js`（同步镜像至 `$WORKSPACE/skills/imap-smtp-email/okki-sync.js`）

### 导出 API

```javascript
const okkiSync = require('./scripts/okki-sync');

// 客户匹配（两阶段：域名 → 向量搜索）
const customer = await okkiSync.matchCustomer(email, subject, body);
// → { company_id, name, match_type, confidence } | null

// 创建邮件跟进记录（trail_type=102）
const result = await okkiSync.createEmailTrail(companyId, {
  uid,        // 去重 key
  from,       // 发件人
  to,         // 收件人
  subject,    // 主题
  date,       // 时间
  body,       // 正文摘要
  direction,  // 'in' | 'out'
  attachments // [{ filename }]
});

// 创建报价单跟进记录（trail_type=101）
const result = await okkiSync.createQuotationTrail(companyId, {
  uid,          // 去重 key
  quotationNo,  // 报价单编号
  date,         // 日期
  products,     // [{ name, quantity, unit_price }]
  totalAmount,  // "USD 9730.00"
  validUntil    // 有效期
});

// 完整邮件同步流程（匹配 + 创建 trail）
const result = await okkiSync.syncEmailToOkki(emailData);
```

### CLI 入口

```bash
# 测试模式（检查 OKKI CLI 和向量搜索连接）
node scripts/okki-sync.js test

# 报价单同步（由 generate-all.sh 调用）
node scripts/okki-sync.js quotation '{"dataFile":"/path/to/data.json","quotationNo":"QT-xxx"}'
```

---

## Trail Type Enum

| 类型 | 编号 | 说明 |
|------|------|------|
| QUOTATION | 101 | 快速记录 / 报价单 |
| EMAIL | 102 | 邮件 |
| PHONE | 103 | 电话 |
| MEETING | 104 | 会面 |
| SOCIAL | 105 | 社交平台 |

---

## Dependencies

| 依赖 | 路径 | 说明 |
|------|------|------|
| OKKI CLI | `$WORKSPACE/xiaoman-okki/api/okki.py` | OKKI API 客户端（`trail add` 命令） |
| 向量搜索 | `$WORKSPACE/vector_store/search-customers.py` | LanceDB 客户向量索引 |
| Python venv | `python3` 或自定义 venv | 向量搜索依赖（nomic-embed-text） |
| imap-smtp-email | `$WORKSPACE/skills/imap-smtp-email/` | 邮件 skill（集成点） |
| quotation-workflow | `$WORKSPACE/skills/quotation-workflow/` | 报价单 skill（集成点） |

---

## Integration Points

### 邮件发送（smtp.js）

```javascript
// $WORKSPACE/skills/imap-smtp-email/scripts/smtp.js
// L13: require('../okki-sync')
// L131+: 发送成功后异步调用
const { syncEmailToOkki } = require('../okki-sync');

syncEmailToOkki({
  uid: `smtp-${Date.now()}-${toHash}`,
  from, to, subject, date,
  body: text,
  direction: 'out',
  attachments
}).then(r => console.log('OKKI sync:', r))
  .catch(e => console.warn('OKKI sync failed:', e.message));
```

### 报价单生成（generate-all.sh）

```bash
# $WORKSPACE/skills/quotation-workflow/scripts/generate-all.sh
# 末尾调用（|| true 不阻断流程）
node /path/to/okki-sync.js quotation \
  "{\"dataFile\":\"${DATA_FILE}\",\"quotationNo\":\"${QUOTATION_NO}\"}" \
  && echo "✓ OKKI trail created" || true
```

---

## Runtime Files

| 文件 | 说明 |
|------|------|
| `/tmp/okki-sync-processed.json` | 去重记录（已处理的 UID → metadata） |
| `/tmp/okki-unmatched-emails.log` | 未匹配客户日志（email | domain | 原因） |

---

## Customer Matching Logic

```
matchCustomer(email, subject?, body?)
  ├── 提取域名（extractDomain）
  ├── 是否公共域名？（gmail/yahoo/hotmail/outlook/qq/163/126 等）
  │     ├── YES → 跳过域名匹配，直接向量搜索
  │     └── NO  → 域名精确匹配（OKKI CLI company list -k <domain>）
  │               ├── 精确命中 → confidence=0.95，返回
  │               ├── 部分匹配 → confidence=0.7，返回
  │               └── 无匹配  → 向量搜索
  └── 向量搜索（search-customers.py <email+subject+body>）
        ├── 命中 → confidence=topMatch.score，返回
        └── 无匹配 → 写入 unmatched log，返回 null
```

---

## E2E Test Results (2026-03-24)

| 链路 | 命令 | Trail ID | 结果 |
|------|------|----------|------|
| 链路A 邮件→OKKI | smtp.js send --to service@tkscable.com | 88050591907961 | ✅ PASS |
| 链路B 报价单→OKKI | generate-all.sh cable-germany.json QT-E2E-002 | 88050865152265 | ✅ PASS |
| 链路C 公共域名 | test@gmail.com 匹配失败 | — | ✅ PASS（unmatched 日志写入） |
| 去重验证 | 相同 UID 重复触发 | — | ✅ PASS（返回 duplicate） |

---

## Setup Instructions

如需将此模块集成到新 skill 中：

1. **复制模块**
   ```bash
   cp scripts/okki-sync.js /path/to/your-skill/okki-sync.js
   ```

2. **确认依赖路径**（通过环境变量配置）
   - `OKKI_CLI_PATH`：OKKI CLI 脚本路径
   - `VECTOR_SEARCH_PATH`：向量搜索脚本路径
   - `PYTHON_VENV_PATH`：Python 虚拟环境路径（可选，默认 `python3`）

3. **测试连接**
   ```bash
   node okki-sync.js test
   ```

4. **集成到发送流程**（发送成功后异步调用 `syncEmailToOkki`）

5. **集成到生成流程**（生成成功后调用 `quotation` CLI 入口）

---

## Development History

| 时间 | 操作 | Agent | 备注 |
|------|------|-------|------|
| 2026-03-24 09:56 | review_completed | WILSON | 任务审阅完成，批准执行 |
| 2026-03-24 11:30 | iteration_1_executed | IRON | Trail type enum 确认：email=102, quotation=101 |
| 2026-03-24 12:21 | iteration_2_executed | IRON | okki-sync.js 创建完成（582行/15873字节） |
| 2026-03-24 12:24 | iteration_3_executed | IRON | 集成到 smtp.js 发件流程 |
| 2026-03-24 12:40 | iteration_4_executed | IRON | 集成到 quotation-workflow/generate-all.sh |
| 2026-03-24 12:51 | iteration_5_executed | WILSON | E2E 测试全部通过（3条链路），任务 COMPLETE |
| 2026-03-24 12:54 | packaged | WILSON | 打包为 okki-email-sync skill |

---

**Skill 版本：** 1.0.0  
**创建日期：** 2026-03-24  
**维护者：** WILSON / IRON
