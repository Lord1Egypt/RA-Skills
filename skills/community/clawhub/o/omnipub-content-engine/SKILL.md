# omnipub-content-engine

> 全平台内容同步发布引擎 v2 — 从选题到复盘的 AI 驱动闭环

## 定位

omnipub-content-engine 是一个 **AI 驱动的内容生命周期管理技能**，覆盖从选题讨论、内容生成、数据查证、图表设计、风格选择、GEO 优化、多平台发布到数据复盘迭代的完整闭环。

**与市面工具的差异**：融媒宝/易撰侧重分发效率，本技能侧重 **AI 驱动的完整内容生命周期管理**，核心差异化在于 Gate 制度（人工把关不盲发）和 GEO 闭环（内容优化 + AI 可见度）。

**v2 更新**（2026-08-21）：公众号推送新增 `--verify`（draft/get 回读验证）、`--force-upload`（强制重传图片）、`--retry`（IP 白名单自动重试）；头条推送生成完整脚本套件（inject + batch_upload + check_cover + check_missing + insert_fallback）；converter 的列表布局从 flex 改为 table（微信渲染器不执行 flexbox）。

## 支持平台

| 平台 | 方案 | 状态 |
|------|------|------|
| 微信公众号 | API 直推草稿箱（v2: 带回读验证 + IP 重试） | 已实现 |
| 今日头条 | playwright 自动化（v2: 5 脚本套件） | 已实现 |

## 10 阶段闭环工作流

```
选题 → 生成 → 查证 → 图表 → 文末 → 风格 → 信息图 → GEO → 发布 → 复盘
  G1            G3                        G4     G5
                                              ↓
                                    复盘结论回流选题库
```

### 阶段总览

| # | 阶段 | Gate | 脚本 | 说明 |
|---|------|------|------|------|
| 1 | 选题讨论 | G1 | topic_research.py | 搜索热点话题，HCTFD 五维评分，输出候选选题等待用户确认 |
| 2 | 内容生成 | G2 | (AI 生成) | 双平台适配：公众号版（ABBB 结构）+ 头条版（派生稿） |
| 3 | 数据查证 | — | fact_check.py | 提取数据声明，三源交叉验证，输出核查报告 |
| 4 | 图表设计 | — | (AI 生成 Chart.js) | 数据可视化图表设计规范 |
| 5 | 文末模板 | G3 | footer_builder.py | 组装文末 5 块：推荐/介绍/社群/CTA/签名 |
| 6 | 风格选择 | — | gallery / preview / themes | 3 套主题 + 画廊预览 + 单篇预览 |
| 7 | AI 信息图 | — | infographic.py | 8 要素布局 + 4 引擎适配（即梦/LOVART/ChatGPT/Midjourney） |
| 8 | GEO 优化 | — | geo_check.py | 7 项 GEO 就绪度检查，满分 100，>=80 通过 |
| 9 | 双平台发布 | G4 | publish / toutiao | 公众号推草稿箱 + 头条 playwright 发布 |
| 10 | 数据复盘 | G5 | analyze_article_data.py | 4 类归因诊断 + 迭代建议 + HTML 报告 |

### Gate 制度（人工把关）

| Gate | 名称 | 用户需提交 | 未提交时 |
|------|------|-----------|---------|
| G1 | 选题确认 | 从候选选题中选择方向 | 输出候选后停止，不得进入生成 |
| G2 | 初稿审阅 | 对正文的修改意见 | 生成初稿后等待，用户说"改"则修改 |
| G3 | 文末素材 | 二维码图、介绍文案、过往文章列表 | 用占位符并标红提示，不得编造 |
| G4 | 发布授权 | 确认终稿和平台 | 未确认不得推送 |
| G5 | 复盘数据 | 后台粘贴真实数据 | 未粘贴不得运行分析 |

**核心规则**：AI 自主完成调研/生成/查证/排版/检查；Gate 未通过则流程停止。

## CLI 命令

```bash
# 统一入口
python scripts/cli.py <command> [args]

# 选题搜索
python scripts/cli.py topic "AI医疗" --verbose

# 数据查证
python scripts/cli.py fact-check article.md

# AI 信息图提示词
python scripts/cli.py infographic "标题" --engine jimeng --data "76%->52%"

# 文末组装
python scripts/cli.py footer --config config.yaml --format html

# GEO 检查
python scripts/cli.py geo-check article.md

# HTML 兼容转换
python scripts/cli.py convert --src design.html --dst wechat.html

# 主题列表
python scripts/cli.py themes

# 主题画廊
python scripts/cli.py gallery

# 单篇预览
python scripts/cli.py preview article.md -t xinming-lab

# 发布到公众号（标准推送 + 验证）
python scripts/cli.py publish article.md --cover cover.png -t xinming-lab --verify

# 发布到公众号（IP 白名单自动重试 + 验证）
python scripts/cli.py publish article.md --cover cover.png --retry --verify

# 发布到公众号（强制重传所有图片，含旧 mmbiz 链接）
python scripts/cli.py publish article.md --cover cover.png --force-upload --verify

# 头条发布准备（生成完整脚本套件）
python scripts/cli.py toutiao prepare article.md --output prep/ --images images/

# 数据复盘
python scripts/cli.py analytics --csv data.csv
```

## 主题系统

| 主题 | 风格 | 配色 | 适用 |
|------|------|------|------|
| xinming-lab | 品牌紫绿蓝 | #534AB7 / #639922 / #2196F3 | 调研报告、行业分析（默认） |
| xinming-minimal | 极简黑白灰 | #1a1a1a / #666 | 随笔、短文、思考 |
| xinming-warm | 暖橙古铜 | #C0392B / #8B5E3C | 成长故事、案例拆解、人物 |

所有主题 CSS 已过微信兼容性清洗（无 border-radius / box-shadow / gradient / flex / grid 等无效属性）。列表布局使用 `<table>` 而非 flexbox（微信渲染器不执行 flex 布局引擎）。

## 公众号样式安全（v2 核心改进）

微信渲染器有独立的 CSS 白名单过滤层，以下属性**存储无损但渲染时被忽略**：
- `border-radius` / `box-shadow` / `text-shadow` → 用 `border` 代替
- `linear-gradient` / `radial-gradient` → 用纯色 `background` 代替
- `letter-spacing` / `opacity` → 无替代
- `display: flex` / `flex` / `flex-shrink` / `align-items` / `justify-content` / `gap` → 用 `<table>` 布局代替

converter.py 内置 `_sanitize_style()` 自动剥离所有不安全属性，并将 `display:flex/grid` 替换为 `display:block`。详细约束见 `references/wechat-css-constraints.md`。

### v2 推送验证

| 功能 | 参数 | 说明 |
|------|------|------|
| 回读验证 | `--verify` | 推送后自动 draft/get 回读，统计 border-radius/box-shadow/flex 等属性数量（应全为 0） |
| IP 重试 | `--retry` | 中国移动等动态 IP 自动重试获取 token（最多 30 次） |
| 强制重传 | `--force-upload` | 检测并重新上传所有本地图片，含已失效的 mmbiz 旧链接 |
| 旧链接检测 | 自动 | `detect_mmbiz_images()` 扫描 Markdown 中的 mmbiz.qpic.cn URL 并警告 |

## AI 信息图提示词

8 要素布局：页码 → 主标题 → 副标题 → 数据卡片 → 3D 等距主视觉 → 底部洞察 → 数据来源 → 品牌署名

4 引擎适配：
- 即梦：中文文字渲染最强
- LOVART：设计质感最佳
- ChatGPT/DALL-E：语义理解最强
- Midjourney：视觉冲击力最强

## GEO 优化

7 项核心检查：
1. 首段直接给答案（60 字内）
2. H2 语义结构清晰
3. FAQ 段落覆盖
4. 实体密度充足
5. 来源引用可追溯
6. 段落短促（<=4 行）
7. 品牌归因明确

## 数据复盘

4 类归因诊断树：
- 有热度没浏览量 → 标题/封面/关键词不匹配
- 整体没数据 → 发布时机/平台算法/账号权重
- 点开没读完 → 开头冗长/内容质量/排版
- 读完不转化 → CTA 不清晰/用户画像偏差

复盘结论回流选题库，形成迭代闭环。

## 配置

复制 `config.example.yaml` 为 `config.yaml`，填入：
- 品牌信息（名称、口号、作者、简介）
- 文末素材（二维码路径、过往文章）
- 微信公众号凭据（AppID、AppSecret）
- 头条发布设置
- 禁用词清单
- 可选：红狐数据 API Key（用于选题阶段爆款数据）

## 文件结构

```
omnipub-content-engine/
├── SKILL.md                          # 本文档（编排层主入口）
├── config.example.yaml               # 配置模板
├── scripts/
│   ├── cli.py                        # 统一 CLI 入口（12 个命令）
│   ├── converter.py                  # Markdown→HTML 转换（含 CSS 清洗）
│   ├── wechat_api.py                 # 微信 API 封装（token/upload/delete）
│   ├── wechat_publish.py             # 公众号草稿创建
│   ├── toutiao_publish.py            # 头条发布（playwright 自动化）
│   ├── theme.py                      # 主题加载器
│   ├── topic_research.py             # 选题搜索 + HCTFD 评分
│   ├── fact_check.py                 # 数据声明提取 + 三源验证
│   ├── infographic.py                # AI 信息图提示词生成
│   ├── footer_builder.py             # 文末模板组装
│   ├── geo_check.py                  # GEO 就绪度检查
│   ├── analyze_article_data.py       # 数据复盘分析
│   └── wechat_compat.py              # 微信 CSS 兼容转换
├── themes/
│   ├── xinming-lab.yaml              # 品牌紫（默认）
│   ├── xinming-minimal.yaml          # 极简黑白灰
│   └── xinming-warm.yaml             # 暖色人文
├── templates/
│   ├── footers/                      # 文末模板
│   └── infographic-prompts/          # 信息图提示词模板
└── references/
    ├── 01-topic-research.md          # 选题方法论
    ├── 02-content-generation.md      # 内容生成规范
    ├── 03-fact-checking.md           # 数据查证规范
    ├── 04-charts-infographics.md     # 图表与信息图规范
    ├── 05-footer-styles.md           # 文末模板+风格规范
    ├── 06-geo-optimization.md        # GEO 优化规范
    ├── 07-publishing.md              # 双平台发布规范
    ├── 08-analytics.md               # 数据复盘规范
    └── wechat-css-constraints.md     # 微信 CSS 兼容性约束
```

## 触发词

内容发布、公众号发布、头条发布、内容同步、选题讨论、爆款选题、GEO优化、数据复盘、内容引擎、omnipub、推送公众号、推草稿箱、发头条号

## 技术栈

- Python 3.11+
- PyYAML（配置解析）
- BeautifulSoup4 + lxml（HTML 解析与兼容转换）
- cssutils（主题 CSS 解析）
- markdown（Markdown → HTML）
- requests（微信 API 调用）
- playwright-cli（头条发布自动化）

## 版本历史

| 版本 | 日期 | 关键更新 |
|------|------|---------|
| v1.0.0 | 2026-08-14 | 初始版本：10 阶段闭环 + 3 主题 + 双平台发布 |
| v2.0.0 | 2026-08-21 | converter flex→table 布局修复；公众号 --verify/--force-upload/--retry；头条 5 脚本套件；CSS 约束文档完善；UNSAFE_CSS_PROPS 扩展 |

## 作者

心明增长实验室
