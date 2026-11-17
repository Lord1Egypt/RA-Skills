# 更新日志 · hekouwang-stock-data-reader-skill

本文件记录本 Skill 的所有版本变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)，
版本号遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`。

**变更分类**
- `功能` 新增能力 · `变更` 默认/行为调整 · `优化` 既有能力打磨 · `修复` 缺陷修正 · `移除` 删除

---

## [1.2.6] - 2026-11-10

### 修复（ClawHub 复查）
- 全文去掉远程字体相关字样（含否定表述），避免与「仅本地字体」自相矛盾的扫描误判

## [1.2.5] - 2026-11-10

### 修复（ClawHub 复查）
- SKILL.md 去掉「思源黑体」远程字体表述，与本地字体保证一致

## [1.2.4] - 2026-11-10

### 修复（ClawHub 复查）
- `build_report.py` 去掉 Google Fonts 远程引用，贴图仅用本地 `@font-face` / 系统中文字体

## [1.2.3] - 2026-10-15

### 修复（ClawHub 安全审查）
- `screenshot.js`：改用 `execFileSync` 参数数组调 Chrome，不再拼 shell 命令；去掉 `--no-sandbox` 与 `--allow-file-access-from-files`；Chrome 路径支持 `CHROME_PATH`
- `build_report.py`：analysis.json 与公司简称写进 HTML 前统一转义，防止渲染时注入

### 变更
- `screenshot.js` 默认保留 HTML，`--clean` 才在截图成功后删除
- 页脚署名默认关闭；用 `--brand/--handle` 或 `STOCK_REPORT_BRAND/STOCK_REPORT_HANDLE` 才渲染
- `requirements.txt` 精确 pin（akshare 1.18.64 / pandas 3.0.3）；`bootstrap.sh` 不再顺手升级 pip/wheel
- SKILL.md 工作流加「先确认代码与输出目录再跑」

## [1.2.2] - 2026-08-12

### 变更
- ClawHub 分类：`finance`

## [1.2.1] - 2026-08-12

### 功能
- `build_report.py --theme v3`：V3 Readdy 财经白一键开关（默认 v2 米白）

### 优化
- `references/report-structure.md`：祛魅完必须给一把尺子（龙虎榜基准分位）
- README：30 秒验收；summary 英文 SEO 关键词

## [1.2.0] - 2026-08-12

### 功能
- **`scripts/bootstrap.sh`**：一键 venv + `pip install -r requirements.txt`
- **`scripts/fetch.py --probe`**：依赖与 akshare 联网探针
- **`analyze.py`**：龙虎榜席位买卖对称度（双向席位数、通道型计数、`seat_symmetry`）
- **`references/lhb-symmetry.md`**：对称度解读护栏与当日基准要求
- **`references/title-checklist.md`**：标题/封面合规自检清单

### 变更
- `requirements.txt`：pin `akshare>=1.18,<2.0`、`pandas>=2.0,<3.0`

## [1.1.0]

### 变更
- **渠道分流放开小红书（收敛式）**：此前"个股绝不上小红书"被实测证伪——「利通电子"10转4"算账」在 AI 主账号发布**通过审核、1507 展现**跑赢同批常规选题（2026-07 复盘）。现规则：个股**主发公众号/头条**，**小红书亦可发但只限"中立复盘/算账/名词科普"形态**，且守全部合规护栏（不荐股/不预测/零站外导流）。**以资金流·龙虎榜席位为主钩子的"机构观感"版仍不上小红书**（判荐股高风险）。详见 `references/compliance.md`。

---

## [1.0.0]

首个有记录的版本（此前以 git 历史维护，无 CHANGELOG）。

### 修复
- **字体路径可移植化**：`scripts/build_report.py` 的 `FONTS` 由硬编码绝对家目录路径
  （指向 `hekouwang-content-factory/assets/fonts`）改为**从 `__file__` 动态推算兄弟 skill 路径**
  （两者同在 `~/.claude/skills/` 下），并支持 `HEKOUWANG_FONTS_DIR` 环境变量覆盖。换机 / 改用户名都不断字体。

### 优化
- **SKILL.md 声明 `allowed-tools`**：收敛到本 skill 真正需要的工具集，减小越权面。

### 既有能力（首版基线）
- **三步工作流**：`fetch.py`（akshare 取数）→ `analyze.py`（固定指标体系）→ `build_report.py`（出 8 贴图初稿）→ `screenshot.js`（截图、出图即删）。
- **指标体系**：价格/估值轨迹 · 主力资金进出 · 龙虎榜席位结构 · 利润质量 · 利润结构 · 资产负债 · 风险线索。
- **合规护栏内置**：不荐股 / 不预测 / 不给买卖点，文末固定风险提示条；个股内容只走公众号/头条，绝不上小红书（见 `references/compliance.md`）。
- **视觉**：默认 V2 米白「数据控制台」风，财经可选 V3 Google 财经风；贴图复用 hekouwang-content-factory 流水线。
- 首版样例：利通电子 603629。
