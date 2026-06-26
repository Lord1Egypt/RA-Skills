# Memory-OS 具体使用示例

## 方式 1: 在 Claude Code 中使用 Skill（推荐给普通用户）

### 安装

```bash
# 1. 安装 Skill
clawhub install openclaw-memory-os

# 2. 安装 npm 包（后端）
npm install -g openclaw-memory-os

# 3. 初始化
openclaw-memory-os init
```

### 使用示例

#### 示例 1: 保存选股规则

**您说：**
> "请帮我记住：我的选股标准是 PE<15, ROE>15%, 营收增长>20%, 偏好科技和医疗股"

**Claude 会：**
1. 使用 Memory-OS Skill 自动保存这条记忆
2. 提取关键词作为标签（stock, investment, rules）
3. 分类为 TEXT 类型
4. 存储到 `~/.memory-os/data/memories/`

**响应：**
```
✓ 已保存到记忆系统
记忆 ID: abc123...
标签: stock-selection, investment-rules
```

#### 示例 2: 回忆之前的规则

**您说（第二天）：**
> "我之前的选股标准是什么？"

**Claude 会：**
1. 自动从 Memory-OS 搜索相关记忆
2. 找到昨天保存的选股规则
3. 返回完整内容

**响应：**
```
根据您的记忆，您的选股标准是：
1. 市盈率 PE < 15
2. 净资产收益率 ROE > 15%
3. 营收增长率 > 20%
4. 行业偏好：科技、医疗

这是您在 2024-03-20 保存的规则。
```

#### 示例 3: 分析股票时自动应用规则

**您说：**
> "帮我分析中芯国际这只股票"

**Claude 会：**
1. 自动检索您的选股规则记忆
2. 应用规则分析股票
3. 给出符合您标准的分析

**响应：**
```
让我根据您的选股标准分析中芯国际：

根据您的规则（PE<15, ROE>15%, 营收增长>20%）：
- PE: 12.5 ✅ 符合
- ROE: 18.2% ✅ 符合
- 营收增长: 25.3% ✅ 符合
- 行业: 科技（半导体）✅ 符合偏好

综合评估：完全符合您的选股标准，建议关注。
```

---

## 方式 2: 使用 CLI 命令行

### 基本操作流程

#### 1. 保存笔记到记忆

```bash
# 创建测试笔记
mkdir ~/my-notes
echo "学习了 TypeScript 的高级类型系统" > ~/my-notes/typescript-notes.txt
echo "React Server Components 性能优化技巧" > ~/my-notes/react-notes.txt

# 采集到记忆系统
openclaw-memory-os collect --source ~/my-notes/

# 输出：
# ✓ 已采集 2 个文件
# ✓ 创建 2 条记忆
```

#### 2. 搜索记忆

```bash
# 搜索 TypeScript 相关笔记
openclaw-memory-os search "TypeScript"

# 输出：
# 找到 1 条记忆：
# [text] 学习了 TypeScript 的高级类型系统
#   来源: ~/my-notes/typescript-notes.txt
#   时间: 2024-03-20 10:30:15
```

#### 3. 查看时间线

```bash
# 查看今天的记忆
openclaw-memory-os timeline --date 2024-03-20

# 输出：
# 2024-03-20 的记忆：
# 10:30 - [text] TypeScript 学习笔记
# 10:35 - [text] React 性能优化笔记
# 总计: 2 条记忆
```

#### 4. 查看统计

```bash
openclaw-memory-os stats

# 输出：
# 记忆统计：
# 总记忆数: 2
# 按类型: {"text": 2}
# 按来源: {"file-collector": 2}
# 存储大小: 1.2 KB
```

---

## 方式 3: 编程 API

### 完整示例：构建选股助手

```typescript
import { MemoryOS, MemoryType } from 'openclaw-memory-os';

async function main() {
  // 1. 初始化
  const memory = new MemoryOS({
    storePath: '~/.memory-os'
  });
  await memory.init();

  // 2. 保存选股规则
  await memory.collect({
    type: MemoryType.TEXT,
    content: `
选股规则：
1. PE < 15
2. ROE > 15%
3. 营收增长 > 20%
4. 偏好：科技、医疗
    `,
    metadata: {
      tags: ['stock', 'rules'],
      source: 'user-input',
      category: 'investment'
    }
  });

  console.log('✓ 规则已保存');

  // 3. 分析股票时回忆规则
  async function analyzeStock(stockName: string, stockData: any) {
    // 检索规则
    const rules = await memory.search({
      tags: ['stock', 'rules']
    });

    if (rules.length > 0) {
      console.log('应用规则:', rules[0].memory.content);

      // 应用规则分析
      const pe = stockData.pe;
      const roe = stockData.roe;

      const result = {
        stock: stockName,
        peCheck: pe < 15 ? '✓' : '✗',
        roeCheck: roe > 15 ? '✓' : '✗',
        recommendation: (pe < 15 && roe > 15) ? '推荐' : '不推荐'
      };

      return result;
    }
  }

  // 4. 使用
  const analysis = await analyzeStock('中芯国际', {
    pe: 12.5,
    roe: 18.2
  });

  console.log(analysis);
  // {
  //   stock: '中芯国际',
  //   peCheck: '✓',
  //   roeCheck: '✓',
  //   recommendation: '推荐'
  // }
}

main();
```

---

## 实际场景：从零开始使用

### 场景：管理投资笔记

#### Day 1: 设定规则

```bash
# 1. 初始化
openclaw-memory-os init

# 2. 创建投资规则文件
cat > ~/investment-rules.txt << 'EOF'
我的投资原则：
1. 只投资自己理解的行业
2. PE < 15, ROE > 15%
3. 长期持有，不追涨杀跌
4. 单只股票仓位 < 10%
EOF

# 3. 采集规则
openclaw-memory-os collect --source ~/investment-rules.txt
```

#### Day 7: 分析新股票

```bash
# 搜索之前的规则
openclaw-memory-os search "投资原则"

# 输出会显示 Day 1 保存的规则
# 然后根据规则分析新股票
```

#### Day 30: 回顾投资决策

```bash
# 查看整个月的投资相关记忆
openclaw-memory-os timeline --range "last 30 days"

# 搜索所有分析过的股票
openclaw-memory-os search "股票"
```

---

## 数据查看和验证

### 查看原始数据

```bash
# 1. 查看记忆文件
ls -la ~/.memory-os/data/memories/

# 2. 查看单个记忆（JSON 格式）
cat ~/.memory-os/data/memories/abc123.json | jq '.'

# 输出示例：
{
  "id": "abc123-...",
  "type": "text",
  "content": "我的选股标准是 PE<15...",
  "metadata": {
    "source": "user-input",
    "timestamp": "2024-03-20T10:30:00Z",
    "tags": ["stock", "rules"]
  },
  "createdAt": "2024-03-20T10:30:00Z",
  "updatedAt": "2024-03-20T10:30:00Z"
}
```

### 验证零网络调用

```bash
# Terminal 1: 监控网络
sudo tcpdump -i any port 443 or port 80

# Terminal 2: 使用 Memory-OS
openclaw-memory-os collect --source ~/test-data/
openclaw-memory-os search "test"

# 应该看到：ZERO 网络流量（v0.1.0 完全本地）
```

---

## 常见问题

### Q: Skill 会自动保存所有对话吗？
**A:** 不会。只有当您明确要求"记住XXX"或使用关键词时才会保存。

### Q: 数据存储在哪里？
**A:** `~/.memory-os/data/` - 您的本地机器，JSON 格式，人类可读。

### Q: 如何删除某条记忆？
**A:**
```bash
# 找到记忆 ID
openclaw-memory-os search "要删除的内容"

# 删除文件
rm ~/.memory-os/data/memories/<memory-id>.json

# 或删除所有
rm -rf ~/.memory-os/
```

### Q: v0.1.0 需要 API key 吗？
**A:** 不需要。完全本地运行，零外部 API 调用。

### Q: 如何备份记忆？
**A:**
```bash
# 备份整个目录
cp -r ~/.memory-os ~/backups/memory-os-backup-$(date +%Y%m%d)

# 或导出（如果实现了）
openclaw-memory-os export ~/backups/memories.json
```

---

## 最佳实践

1. **明确路径**：使用 `~/specific-folder/` 而不是 `~/Documents/`
2. **定期检查**：`ls ~/.memory-os/data/memories/` 查看收集了什么
3. **测试先行**：先在 `~/test-data/` 测试，再用真实数据
4. **备份重要记忆**：定期备份 `~/.memory-os/` 目录
5. **使用标签**：保存时添加有意义的标签，方便后续搜索

---

**总结：**
- ClawHub Skill = 最简单（自然语言）
- CLI = 最灵活（批量操作）
- API = 最强大（自定义应用）

选择适合您的方式开始使用！
