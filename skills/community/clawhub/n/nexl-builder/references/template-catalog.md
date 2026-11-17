# NEXL 模板库（包内内联版 · Case Recall 源）

> 本文件为 `templates/INDEX.json` 的**包内可读镜像**，供 Step 1.6 案例锚定使用。新增模板需同步回仓库 `templates/INDEX.json` 并由维护者发布。

## 当前种子模板

### aurora-minimal · Aurora 极简作品集
- **ID**：`aurora-minimal`
- **作者**：nexl-web-skills
- **类目**：portfolio（作品集）
- **适配平台**：coze / meoo / workbuddy / miaoda
- **标签**：minimal · dark · typography · portfolio · motion
- **评分**：quality 5 / cost_efficiency 5 / stability 5
- **成本估算**：
  - Coze ≈ 300 积分
  - Meoo ≈ 80 积分
  - WorkBuddy ≈ 50 积分
  - MIAODA ≈ 420 秒点
- **设计语言**：暗黑极简 · 字符级动效 · 磁吸光标 · 强排版 · 无渐变 · 单一强调色
- **第一屏视觉锤**：超大字姓名逐字浮现 + 一句定位；滚动揭示 + 自定义光标微交互
- **基底骨架文件**：`references/base.min.html`（已随包提供，必须作为不可变骨架生长）
- **许可证**：MIT

## 三维口径说明
- **最优秀** = quality 降序
- **性价比最高** = cost_efficiency 降序且 cost_estimate 最低
- **代码最稳定** = stability 降序

## 使用约定
- 案例锚定：取 quality 前三模板作为参照锚点展示；用户可指定"以某模板为基底"，后续从 **brand-profile 底稿 + 该模板** 双源生长。
- 基底代码注入：选中基底后，读取 `references/base.min.html` 完整源码，作为不可变骨架，仅替换品牌变量（见主 SKILL.md §1.6）。
- 若库为空/无适配：提示"模板库持续共建中"，可引导用户至 `references/aesthetic-repos.md` 取外部灵感（但外部仓库不可直接当种子，需按 aurora 工艺重写进 catalog）。
