# 火一五小红书创作伙伴

> 一个**有记忆、能学习、会教方法**的小红书创作助手。
> 调研→选题→创作→优化→发布→复盘 全流程闭环。
> 青岛火一五信息科技有限公司

完整说明：
- 命令速查与典型场景：`SKILL.md`
- 详细教程与历史：本文件
- 设计原则与版本变更：[docs/changelog.md](docs/changelog.md)
- Allen 文案体系：[data/allen_method.md](data/allen_method.md)

---

## 一、五分钟上手

### 1.1 安装依赖

```bash
pip install requests
pip install jieba pandas anthropic   # 全部可选
```

### 1.2 抓取要 Cookie（仅调研用）

浏览器登录 https://www.xiaohongshu.com → DevTools → Cookies → 拼成完整字符串：

```bash
export XHS_COOKIE='web_session=...; a1=...; webId=...; xsecappid=xhs-pc-web; ...'
```

可选 LLM 增强：

```bash
export XHS_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

### 1.3 第一次跑

```bash
# 自检 Cookie + 风控
python3 scripts/safety_check.py

# 用 1~5 篇代表作建立你的风格档案
python3 scripts/assistant.py init \
    --persona "30+ 干皮女生" --voice casual --niche "护肤" \
    --baseline note1.md note2.json

# 看状态 + 推荐下一步
python3 scripts/assistant.py status
```

---

## 二、整体工作流

```
  调研 ─ scrape-{search,note,user}.py / safety_check.py
   ↓
  分析 ─ analyze-notes.py
   ↓
  选题 ─ brainstorm.py / topic_ideas.py / today.py
   ↓
  对标 ─ reverse_engineer.py（爆款 URL → 公式/骨架/钩子）
   ↓
  创作 ─ write_post.py / drafts new
   ↓
 ┌── 教练 ─ coach.py / coach_iterate.py（一次只 focus 一维）
 │  ↓
 │ 美学 ─ critique.py（Allen 6 维）
 │  ↓
 │ 工程 ─ polish_post.py（标题/排版/合规）
 │  ↓
 │ 合规 ─ compliance_check.py
 │  ↓
 └── 改稿 → drafts diff（6 维分变化追踪）
   ↓
  封面 ─ cover_brief.py（3 套版式 brief）
   ↓
  发布 ─ publish_helper.py（剪贴板 + 检查表）
   ↓
  跟踪 ─ track_post.py（24h/3d/7d 互动快照）
   ↓
  复盘 ─ weekly_review.py / practice.py / ab_test.py
   ↓
  学习 ─ assistant.py learn / evolve / preset
```

每个脚本独立可用，也可以全部走 `assistant.py` 主入口路由。

---

## 三、防封号原则（先读）

1. **用自己的 Cookie**，脚本不做登录自动化
2. **不共享 Cookie**，多账号不能在同一台设备混用
3. 每次请求随机 3~7 秒延时，单会话 30 次封顶
4. 会话间隔 10~30 分钟
5. 日请求不超过 100 次
6. 不自动 post / like / follow / comment
7. 460 / 461 / 403 / "captcha" / 重定向登录 → 立刻停 30 分钟
8. 不翻页批量抓（搜索只取首页，主页只取 preview）

---

## 四、典型场景

### A. 第一次用助手

```bash
# 准备 1~5 篇你的代表作（json/md 都行）
python3 scripts/assistant.py init --persona "30+" --niche "护肤" \
    --baseline note1.json note2.md
python3 scripts/assistant.py status
```

### B. 让助手主导整周创作

```bash
# 周一
python3 scripts/assistant.py status      # 看推荐
python3 scripts/assistant.py today       # 今日选题（节气 + 栏目 + 历史空缺）
python3 scripts/assistant.py drafts new --topic "下班后副业"

# 周内每篇
python3 scripts/assistant.py write 干皮护肤
python3 scripts/assistant.py coach-iterate <draft>   # 一次只 focus 一维改
python3 scripts/assistant.py drafts diff <id>        # 看 6 维分变化
python3 scripts/assistant.py critique <draft>        # 全维诊断
python3 scripts/assistant.py publish <draft>

# 周末
python3 scripts/assistant.py review
python3 scripts/assistant.py learn disable=emoji
python3 scripts/assistant.py evolve
```

### C. 看到爆款想"我也写一条"

```bash
# 反向拆解 + 加进 baseline
python3 scripts/assistant.py reverse \
    --url "https://www.xiaohongshu.com/explore/..." --add-baseline

# 用同公式起草 + 改写
python3 scripts/assistant.py write 我的主题 --formula <T?> --skeleton <S?>
python3 scripts/assistant.py coach-iterate draft.md
```

### D. 写完一篇笔记，从 48 → 80 分

```bash
# v1 草稿
python3 scripts/assistant.py drafts new --topic 副业 --from /tmp/v1.md
python3 scripts/assistant.py critique <draft>      # 看分

# coach-iterate 一次只 focus 最差的那一维
python3 scripts/assistant.py coach-iterate <draft> # 给当前 focus 维度的 4 件套

# 用户根据反馈写 v2
python3 scripts/assistant.py drafts add <draft> /tmp/v2.md
python3 scripts/assistant.py drafts diff <draft>   # 自动对比 v1 vs v2 的 6 维

# 一直循环到 6 维都 ≥ 7 分
```

---

## 五、所有命令速查

### 主入口
- `assistant.py status` — 状态 + 推荐
- `assistant.py next` — 直接执行最优推荐
- `assistant.py today` — 今日选题推荐 ⭐ v3.2
- `assistant.py preset allen|engineer|balanced` — 风格预设

### 调研 / 分析
- `safety_check.py` — Cookie + 风控自检
- `scrape-note.py` / `scrape-user.py` / `scrape-search.py` — 抓
- `analyze-notes.py` — 互动 / 关键词 / 时段 / 爆款特征

### 选题 / 对标
- `topic_ideas.py` — 一次性 N 条选题清单
- `brainstorm.py` — 5 轮对话式选题
- `reverse_engineer.py` — 爆款 URL 反向拆解
- `today.py` — 今日推荐

### 创作 / 改稿
- `write_post.py draft|titles|skeleton` — 起草
- `drafts.py list|new|add|diff|show` ⭐ v3.2 — 草稿版本管理
- `coach.py` — 全维教练
- `coach_iterate.py` ⭐ v3.2 — 一次只 focus 一维
- `polish_post.py` — 工程打分
- `critique.py` — Allen 6 维（含 Jarvis 陷阱）
- `critique.py --rewrite` — LLM 自动改写
- `critique.py --watch` — 流式深度分析
- `compliance_check.py` — 合规扫描

### 配套工具
- `coin_word.py` — 造词（谐音/概念迁移/形式包装）
- `series_design.py` — 栏目化 + 互动阶梯
- `reader_simulate.py` — 6 种读者画像走全文
- `cover_brief.py` — 封面文案 + 版式 3 套方案

### 发布 / 复盘
- `publish_helper.py` — 剪贴板 + 10 项检查表
- `track_post.py register|snapshot|report` — 互动快照
- `weekly_review.py` — 周/月复盘
- `practice.py prompt|rewrite|rewrite-jarvis` — 写作训练
- `ab_test.py plan|register|compare` — A/B 测试

### 风格档案 / 规则
- `profile_init.py init|add|show|rules|preset|evolve` — 档案管理
- `assistant.py learn key=value` — 短语法教助手
- `assistant.py evolve` — 自动演进规则

---

## 六、Python API

```python
import sys; sys.path.insert(0, 'scripts')

from xhs_writer import Draft, generate_titles, score_post, make_draft, load_draft
from xhs_aesthetic import aesthetic_score
from xhs_coach import coach
from xhs_profile import ProfileStore, StyleProfile, derive_style

# 风格档案
store = ProfileStore()
profile = store.load_style()
rules = store.load_rules()

# 工程打分
draft = load_draft("draft.md")
score = score_post(draft.title, draft.content, draft.tags, rules=rules)

# Allen 6 维美学
aes = aesthetic_score(draft.title, draft.content)
print(aes.total, aes.by_dim)

# 完整教练（含 Allen）
report = coach(draft, profile=profile, rules=rules)
```

---

## 七、数据资产（data/）

| 文件 | 内容 |
|---|---|
| `title_templates.md` | 11 种爆款标题公式（T1~T11）+ 适用 + 踩坑 + 示例 |
| `content_structures.md` | 7 种正文骨架（S1~S7）+ 字段说明 |
| `emoji_palette.md` | emoji 调色板 + 类目向 + 用量建议 |
| `hashtag_topics.md` | 话题标签库（大词/中词/小词）+ 选词工作流 |
| `community_rules.md` | 平台社区规则要点 + 红线清单 + 发布前 checklist |
| `sensitive_words.txt` | 敏感词列表（广告法 + 平台风控） |
| `allen_method.md` | Allen 三课 + 五技法 + 11 案例 + 关键认知转变 + Jarvis 陷阱 5 维 |
| `ai_speak_patterns.json` | AI 腔黑名单 + 替换库（80+ 条） |
| `seasonal_themes.md` | 24 节气 + 节日 + 小红书伪节日的"已存在画面"清单 |

这些文件不止给脚本读，也是 Claude 在调用时的"参考手册"。

---

## 八、闭环数据资产（用户私有）

```
~/.xiaohongshu/
├── posts.jsonl              # 起草历史（publish_helper 写）
├── snapshots.jsonl          # 互动快照（track_post 写）
├── drafts/                  ⭐ v3.2 草稿版本库
│   └── 2026-04-28-fuye/
│       ├── meta.json
│       ├── v01.md / v02.md / v03.md
└── profile/
    ├── style.json           # 风格档案
    ├── rules.json           # 规则覆盖
    ├── feedback.jsonl       # 对建议的反馈
    ├── practice.jsonl       # 写作训练
    ├── ab_tests.jsonl       # A/B 测试
    ├── iter_sessions/       ⭐ v3.2 渐进式教练历程
    ├── baseline/            # 1~5 篇代表作
    └── reviews/             # 周/月复盘报告
```

---

## 九、常见错误对照

| 错误 | 含义 | 处理 |
|---|---|---|
| `LoginRequired: HTTP 401` | Cookie 过期 | 重新浏览器登录 + export |
| `RateLimited: HTTP 460/461` | 频率风控 | **立即停止**，至少等 30 分钟 |
| `BlockedByCaptcha: HTTP 403` | 滑块验证 | 浏览器过验证 + 等 30 分钟 |
| `polish 退出码 2` | 文案分 < 60 | 看 suggestions 修改 |
| `compliance 退出码 2` | 高风险违规 | 必须改（联系方式 / 绝对化词） |

---

## 十、不做的事

❌ 自动发布 / 定时发布 / 多平台分发 — 违背"不自动化"
❌ 多账号矩阵 — 违背"个人号 + 单一声音"
❌ AI 生图 / 封面直出 — 不是 CLI 合适载体
❌ 一键全文生成 — 违背 Allen "范本范"哲学
❌ 达人投放分析 — 个人号不需要

---

**重要免责：** 本技能仅用于合规、针对公开可见内容的个人调研与创作辅助。
请尊重 xiaohongshu.com 的服务条款和当地法律法规。

**技术支持：** 青岛火一五信息科技有限公司
