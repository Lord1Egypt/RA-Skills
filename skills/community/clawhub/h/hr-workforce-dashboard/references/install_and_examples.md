# 安装说明与使用实例

## 一、安装说明

根据 CodeBuddy Skills 官方文档，这个 Skill 支持以下两种使用方式。

### 方式 A：通过 CodeBuddy 界面导入已打包 ZIP（推荐交付方式）

适合把 Skill 交给其他同事直接安装使用。

步骤：
1. 打开 CodeBuddy 设置页。
2. 进入 Skill 管理区域。
3. 点击右上角 **导入 Skill**。
4. 选择打包产物 `hr-workforce-dashboard.zip`。
5. 导入成功后，在 Skill 列表中确认 `hr-workforce-dashboard` 已出现并启用。

适用场景：
- 交付给业务同事或其他项目组。
- 希望直接安装成可复用 Skill。
- 不想手动维护目录结构。

### 方式 B：本地目录安装（推荐开发调试）

适合持续修改 `SKILL.md`、脚本和参考文档。

可选位置：
- **用户级**：`~/.codebuddy/skills/hr-workforce-dashboard/`
- **项目级**：`<workspace>/.codebuddy/skills/hr-workforce-dashboard/`

推荐目录结构：

```text
hr-workforce-dashboard/
├── SKILL.md
├── README.md
├── scripts/
│   ├── build_dashboard_bundle.py
│   └── build_upload_templates.py
├── references/
│   ├── data_spec.md
│   ├── field_mapping.md
│   ├── install_and_examples.md
│   ├── layout_spec.md
│   └── metric_definitions.md
└── assets/
    └── dashboard_style.css
```

适用场景：
- 需要继续迭代脚本或口径。
- 想在本地直接调试真实 Excel 附件。
- 希望把 Skill 跟项目一起管理。

## 二、快速开始

### 1. 触发 Skill 的典型方式

用户可以直接说：
- "请用这个 Skill 根据我上传的人力明细生成标准看板，并打包下载。"
- "我上传了在职和离职 Excel，请生成 workforce dashboard。"
- "请基于附件输出 HTML 看板。"

### 2. 附件上传要求

在调用 Skill 时，用户应上传一组 Excel 文件，建议包含：
- 最新月份在职快照（**必需**）
- 上个月在职快照
- 上上个月在职快照
- 去年同月在职快照
- attrition 统计周期内的离职明细（**建议**）
- 外包人员报表（**可选**，用于生成看板 5）

说明：
- Skill 通过第 1 行报表名称自动识别文件类型
- 不能根据文件名猜测文件类型
- Active 文件：第 1-6 行元数据，第 7 行表头，第 8 行起数据
- Termination 文件：第 1-7 行元数据，第 8 行表头，第 9 行起数据
- Contingent Worker 文件：第 1 行报表名，第 2 行表头，第 3 行起数据

### 3. 生成后的标准输出

成功执行后，输出目录内至少包含：
- `dashboard.html`（主交付物，单页交互式看板）

如需完整交付包，还包含：
- `png/dashboard_1.png` ~ `png/dashboard_4.png`
- `excel/workforce_dashboard.xlsx`
- `ppt/workforce_dashboard.pptx`
- `summary.md`
- `workforce_dashboard.zip`

## 三、使用实例

### 示例 1：标准 5 看板生成

#### 用户输入

"请使用 `hr-workforce-dashboard` Skill，基于我上传的 Excel 附件生成所有标准看板，并输出 HTML。"

#### Skill 预期行为

- 读取所有附件第 1 行报表名称
- 自动识别 active / termination / contingent 文件
- 选择最新 active 月份作为主月份
- 生成看板 1-4（固定），如有 contingent 文件则追加看板 5
- 导出 `dashboard.html`
- 输出 `summary.md` 说明生成月份、附件清单和数据完整性情况

### 示例 2：附件不完整但继续生成

#### 用户输入

"请根据这些人力明细先生成看板，缺少月份也先继续输出。"

#### 已上传附件情况

- 有最新月 active
- 有上个月 active
- 缺少上上个月 active
- 缺少去年同月 active
- 有 termination 明细
- 无 contingent worker 文件

#### Skill 预期行为

- 不中止任务
- 在看板 1 标注 **数据不完整**
- 在 `summary.md` 中说明缺失了哪些月份
- 继续输出能完成的看板 1-4（不含看板 5）和 HTML
- 提醒用户补传后可重新生成完整版本

### 示例 3：在标准看板之外追加自定义看板

#### 用户输入

"先按默认看板输出，再额外增加一个按 BG 看 latest month regular headcount 的补充页。"

#### Skill 预期行为

- 先完整生成固定标准看板（1-5，视附件而定）
- 再基于同一批清洗后的数据追加自定义看板
- 在 `summary.md` 中说明新增了一个自定义看板

### 示例 4：命令行调试脚本

适合在本地直接验证脚本产物。

```bash
python3 scripts/build_dashboard_bundle.py \
  --files /path/to/active_2025_03.xlsx /path/to/active_2026_01.xlsx /path/to/active_2026_02.xlsx /path/to/active_2026_03.xlsx /path/to/termination_2026.xlsx /path/to/contingent_worker.xlsx \
  --output-dir /path/to/workforce_dashboard_output \
  --bundle-name workforce_dashboard \
  --title "人力数据看板"
```

执行成功后，可重点检查：
- `dashboard.html` 是否可预览
- 看板 1-4 图表是否正常显示
- 看板 3 和 5 的表格数据是否正确
- 看板 5 是否出现（需要有 contingent worker 文件）

## 四、常见交付话术示例

适合 Skill 执行完成后回复用户。

### 成功完成

"已根据上传附件生成所有标准看板，输出 HTML 看板可直接在浏览器中查看。如果需要，我也可以继续基于同一批数据追加自定义看板或导出 PNG/Excel/PPT。"

### 数据不完整但已降级输出

"已根据当前附件生成可完成的看板版本，但由于缺少部分对比月份，部分图表已标注'数据不完整'。我已在摘要中列出缺失月份，补传后可重新生成完整版本。"

## 五、补充建议

- 对外正式交付时，优先分发打包好的 `hr-workforce-dashboard.zip`
- 团队内部持续迭代时，优先使用目录安装方式
- 如果业务口径未来可能扩展，优先把新口径追加到 `references/`，避免把 `SKILL.md` 写得过长
