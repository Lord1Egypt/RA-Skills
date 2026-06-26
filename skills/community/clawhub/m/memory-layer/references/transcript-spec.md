# Transcript 层规范

## 位置

`memory/transcripts/YYYY-MM/DD.log`

---

> ⚠️ **数据边界**
>
> Transcript 设计用于存储**操作日志和决策摘要**，不是加密存储。
>
> **禁止存储**：
> - ❌ 账号、密码、API Key
> - ❌ 银行卡号、身份证号
> - ❌ 健康记录、病历
> - ❌ 其他需要加密的敏感数据
>
> **正确做法**：
> - ✅ 存储决策摘要（"买入 ETF1 100 股"）
> - ✅ 存储阈值和规则（"VIX>25 时减仓"）
> - ✅ 存储时间戳和状态（"2026-04-02 18:52 执行成功"）
> - 🔐 敏感数据应存储在加密系统，Transcript 仅引用 ID

---

## 格式规范

```
[TRANSCRIPT] 2026-04-02 18:52:15
[TYPE] monitor
[ID] 20260402-185215
[TAGS] 投资，日常监控
[IMPORTANCE] 0.6

[DATA]
监控时间：2026-04-02 18:52
ETF1: 1.675, -4.23%, 🟢正常
决策：维持配置

[METADATA]
source: cron
status: success
```

---

## 字段规范

### 头部字段

| 字段 | 说明 | 必填 |
|------|------|------|
| TRANSCRIPT | 时间戳 | 是 |
| TYPE | 类型标识 | 是 |
| ID | 唯一 ID | 是 |
| TAGS | 逗号分隔标签 | 可选 |
| IMPORTANCE | 0.0-1.0 分数 | 自动计算 |

### DATA 部分

自由格式，完整日志内容。

### METADATA 部分

| 字段 | 说明 |
|------|------|
| source | 来源（cron/user/auto-dream） |
| duration_ms | 执行时长（毫秒） |
| status | 状态（success/failed） |
| related_topics | 相关 Topic 列表 |
| contradictions_detected | 是否检测到矛盾 |

---

## 约束

| 规则 | 值 | 违规处理 |
|------|-----|----------|
| 写入模式 | 仅追加 | 禁止修改/删除 |
| 加载策略 | 永不加载 | 仅 grep 访问 |
| 归档策略 | >90 天压缩 | gzip 到 archive/ |
| 分割方式 | 按日 | 便于管理 |

---

## 归档机制

超过 90 天的 Transcripts：

1. 压缩为 `.gz` 格式
2. 移动到 `memory/transcripts/archive/`
3. 保留索引记录

### 归档结构

```
memory/transcripts/archive/
├── 2026-01/
│   ├── 2026-01-01.log.gz
│   └── ...
├── 2026-02/
│   └── ...
└── 2026-03/
    └── ...
```

---

## 访问模式

### grep 搜索

```bash
# 搜索关键词
grep -r "关键词" memory/transcripts/

# 按日期范围搜索
grep -l "2026-04-0[1-5]" memory/transcripts/2026-04/

# 按类型计数
grep -c "\[TYPE\] monitor" memory/transcripts/2026-04/*.log
```

---

*最后更新：2026-04-03*
