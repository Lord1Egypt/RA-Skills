# 🔍 漏洞验证 Checklist

**生成时间**: 2026-03-19 07:05:11
**总漏洞数**: 38

## 使用说明

- [ ] 未验证
- [✅] 已验证存在
- [❌] 误报/已修复
- [⚠️] 部分存在

## ⚪ py/full-ssrf (2处)

### ⚪ py/full-ssrf - #1

**位置**: `unknown:149`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/full-ssrf - #2

**位置**: `unknown:173`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/flask-debug (2处)

### ⚪ py/flask-debug - #1

**位置**: `unknown:139`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/flask-debug - #2

**位置**: `unknown:171`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/weak-sensitive-data-hashing (4处)

### ⚪ py/weak-sensitive-data-hashing - #1

**位置**: `unknown:28`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/weak-sensitive-data-hashing - #2

**位置**: `unknown:36`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/weak-sensitive-data-hashing - #3

**位置**: `unknown:101`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/weak-sensitive-data-hashing - #4

**位置**: `unknown:176`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/weak-cryptographic-algorithm (1处)

### ⚪ py/weak-cryptographic-algorithm - #1

**位置**: `unknown:56`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/code-injection (3处)

### ⚪ py/code-injection - #1

**位置**: `unknown:197`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/code-injection - #2

**位置**: `unknown:138`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/code-injection - #3

**位置**: `unknown:160`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/path-injection (1处)

### ⚪ py/path-injection - #1

**位置**: `unknown:154`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/command-line-injection (2处)

### ⚪ py/command-line-injection - #1

**位置**: `unknown:88`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/command-line-injection - #2

**位置**: `unknown:182`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl -X POST http://localhost/calculate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "__import__(\"os\").popen(\"id\").read()"}'
```

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/unsafe-deserialization (3处)

### ⚪ py/unsafe-deserialization - #1

**位置**: `unknown:43`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/unsafe-deserialization - #2

**位置**: `unknown:81`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/unsafe-deserialization - #3

**位置**: `unknown:125`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/stack-trace-exposure (14处)

### ⚪ py/stack-trace-exposure - #1

**位置**: `unknown:51`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #2

**位置**: `unknown:89`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #3

**位置**: `unknown:110`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #4

**位置**: `unknown:133`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #5

**位置**: `unknown:158`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #6

**位置**: `unknown:182`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #7

**位置**: `unknown:205`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #8

**位置**: `unknown:88`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #9

**位置**: `unknown:160`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #10

**位置**: `unknown:239`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #11

**位置**: `unknown:51`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #12

**位置**: `unknown:145`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #13

**位置**: `unknown:167`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/stack-trace-exposure - #14

**位置**: `unknown:188`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/clear-text-logging-sensitive-data (1处)

### ⚪ py/clear-text-logging-sensitive-data - #1

**位置**: `unknown:209`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**预期结果**: _______________

**实际结果**: _______________

---

## ⚪ py/sql-injection (5处)

### ⚪ py/sql-injection - #1

**位置**: `unknown:37`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost/search?username=' OR '1'='1"
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/sql-injection - #2

**位置**: `unknown:64`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost/search?username=' OR '1'='1"
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/sql-injection - #3

**位置**: `unknown:108`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost/search?username=' OR '1'='1"
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/sql-injection - #4

**位置**: `unknown:232`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost/search?username=' OR '1'='1"
```

**预期结果**: _______________

**实际结果**: _______________

---

### ⚪ py/sql-injection - #5

**位置**: `unknown:44`

**验证步骤**:
- [ ] 定位代码
- [ ] 构造 payload
- [ ] 发送请求
- [ ] 确认漏洞
- [ ] 截图记录

**测试 payload**:
```bash
curl "http://localhost/search?username=' OR '1'='1"
```

**预期结果**: _______________

**实际结果**: _______________

---


## 📊 验证汇总

| 严重程度 | 总数 | 已验证 | 误报 | 待验证 |
|----------|------|--------|------|--------|
| ⚪ none | 38 | [ ] | [ ] | [ ] |
| **总计** | **38** | [ ] | [ ] | [ ] |
