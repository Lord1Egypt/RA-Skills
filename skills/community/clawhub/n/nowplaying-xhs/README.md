# NowPlaying - 当前院线电影推荐

## 功能

实时检索当前公映影片，提供：
- 🎬 正在热映的电影列表
- 🌟 烂番茄评分聚合
- 📅 上映日期信息
- 📰 票房新闻动态
- 💡 高评分推荐

## 触发方式

- **手动触发**: "现在有什么好看的电影"、"最近上映了什么"、"帮我选一部电影"
- **定时任务**: 每周五下午 18:00（周末观影推荐）

## 执行流程

### 1. 数据获取
- Rotten Tomatoes: 获取正在热映电影及评分
- Variety: 获取票房新闻

### 2. 筛选排序
- 高评分优先（烂番茄评分）
- 新片优先（本周上映）
- 去重处理

### 3. 格式化输出

```markdown
# 🎬 当前院线热映 (2026-04-16)

## 🌟 高评分推荐
1. **Wasteman** ⭐⭐⭐⭐⭐
   - 评分：100% | 上映：Apr 17, 2026

## 🎥 本周新片
- **Mother Mary** (75%)
- **Normal** (79%)

## 📰 票房新闻
- 本周票房数据...
```

## 文件结构

```
nowplaying/
├── SKILL.md           # Skill 定义
├── nowplaying.py      # 核心脚本
├── run.sh            # 执行脚本
├── CONFIG.md         # 配置说明
└── _meta.json        # 元数据
```

## 使用方法

### 手动执行
```bash
cd /home/admin/.openclaw/workspace/skills/nowplaying
python3 nowplaying.py
```

### Cron 定时
```bash
# 每周五 18:00（周末观影推荐）
0 18 * * 5 /home/admin/.openclaw/workspace/skills/nowplaying/run.sh
```

## 输出示例

```
🎬 当前院线热映 (2026-04-16)

🌟 高评分推荐
1. Wasteman ⭐⭐⭐⭐⭐ (100%)
2. Blue Heron ⭐⭐⭐⭐⭐ (100%)
3. Amrum ⭐⭐⭐⭐ (94%)

🎥 本周新片
- Mother Mary (75%) - Apr 17
- Normal (79%) - Apr 17

📰 票房新闻
- The Super Mario Galaxy Movie: $6.29 亿全球票房
```

## 数据源

| 来源 | 用途 |
|------|------|
| Rotten Tomatoes | 电影评分、上映日期 |
| Variety | 票房新闻、行业动态 |

## 依赖

- Python 3.6+
- 无需 API Key

---

**版本**: 1.1.0  
**作者**: seeu1688  
**最后更新**: 2026-04-16
