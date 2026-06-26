# NowPlaying Skill 配置说明

## 搜索工具配置

### 必需配置

| 工具 | 配置项 | 状态 | 说明 |
|------|--------|------|------|
| **博查 API** | `BOCHA_API_KEY` | ✅ 已配置 | 用于实时排片/票房搜索 |
| **Tavily** | `TAVILY_API_KEY` | ✅ 已配置 | 用于口碑/影评搜索 |

### 可选配置

| 工具 | 配置项 | 状态 | 说明 |
|------|--------|------|------|
| **Agent Browser** | npm 安装 | ⚠️ 需安装 | 直接抓取猫眼/淘票票网页 |
| **Brave Search** | `BRAVE_API_KEY` | ❌ 未配置 | 备用搜索引擎 |
| **SearXNG** | `SEARXNG_URL` | ❌ 未部署 | 自建免费搜索引擎 |

---

## Agent Browser 安装（推荐）

用于直接访问猫眼/淘票票获取实时排片数据：

```bash
# 安装
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps

# 测试
agent-browser --version
```

---

## 搜索策略

### 数据类型与工具选择

| 数据类型 | 首选工具 | 备用工具 |
|----------|----------|----------|
| 实时排片 | Agent Browser | 博查 API |
| 今日票房 | 博查 API | Tavily |
| 豆瓣评分 | Tavily | 博查 API |
| 影评口碑 | Tavily | 博查 API |

### 降级策略

```
Agent Browser 失败 → 博查 API → Tavily → 标注"数据可能非实时"
```

---

## 数据时效性

| 数据类型 | 更新频率 | 延迟 |
|----------|----------|------|
| 排片场次 | 实时 | 1-2 小时 |
| 当日票房 | 每小时 | <1 小时 |
| 豆瓣评分 | 实时 | 准实时 |
| 累计票房 | 每小时 | <1 小时 |

---

## 测试命令

```bash
# 测试博查 API
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"猫眼电影 上海 今日排片"}'

# 测试 Tavily
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "飞驰人生 3 豆瓣评分" -n 5

# 测试 Agent Browser（如已安装）
agent-browser open "https://piaofang.maoyan.com/"
agent-browser snapshot -i
```

---

## 故障排查

### 博查 API 失败

```bash
# 检查 API Key
echo $BOCHA_API_KEY

# 测试余额
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"测试"}'
```

### Tavily 失败

```bash
# 检查 API Key
echo $TAVILY_API_KEY

# 测试
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "测试" -n 3
```

### Agent Browser 失败

```bash
# 检查安装
which agent-browser

# 重新安装
npm install -g agent-browser
agent-browser install --with-deps
```

---

## 输出规范

每次报告必须包含：

1. ✅ 检索信息（位置、时间、数据来源）
2. ✅ 推荐榜（Top 5-10）
3. ✅ 评分对比图（文本条形图，适配飞书）
4. ✅ 附近排片（如定位成功）
5. ✅ **数据时效声明**（必须）

---

最后更新：2026-03-14
