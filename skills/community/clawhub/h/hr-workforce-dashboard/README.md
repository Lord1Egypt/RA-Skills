### HR Workforce Dashboard 使用手册

### 一、这个 Skill 是做什么的
`hr-workforce-dashboard` 用于把**人力在职明细**、**离职明细**和**外包人员明细**自动生成固定口径的 **5 个标准看板**，并输出一个可下载的交付包。

输出包默认包含：
- `dashboard.html`（单页交互式看板，内嵌图表与表格）

如需完整交付包，可要求额外输出：
- `png/dashboard_1.png` ~ `png/dashboard_4.png`
- `excel/workforce_dashboard.xlsx`
- `ppt/workforce_dashboard.pptx`
- `summary.md`
- `workforce_dashboard.zip`

### 二、你需要准备什么文件
建议至少上传以下三类 Excel：
- **在职明细文件（必需）**：可上传 1 份或多份，不同月份可同时上传
- **离职明细文件（建议）**：用于生成看板 4 的离职分析
- **外包人员明细文件（可选）**：用于生成看板 5 的 Contractor & Partner 分布

如果缺少离职明细，Skill 仍会继续生成，但看板 4 会提示数据不完整。
如果缺少外包人员明细，看板 5 不会生成。

### 三、Excel 填写规则
所有上传 Excel 都必须满足以下结构：
- **只读取第一个工作表**
- **第 1 行是报表名称或元数据，不是表头**
- Skill 根据第 1 行内容自动识别文件类型

#### 1）在职明细文件
- 第 1-6 行为元数据，第 7 行为表头，第 8 行起为数据
- 第 1 行：报表名称，固定值 `Overseas Active Employee Report`
- 第 4 行：切片时间，格式为 `Effective Date | <日期>`

#### 2）离职明细文件
- 第 1-7 行为元数据，第 8 行为表头，第 9 行起为数据
- 第 1 行：报表名称，固定值 `Overseas Terminated Employee Report`
- 第 4 行：统计开始日期，格式为 `Termination Date From | <日期>`
- 第 5 行：统计结束日期，格式为 `Termination Date To | <日期>`

#### 3）外包人员明细文件
- 第 1 行为报表名称（包含 `Contingent Worker` 字样）
- 第 2 行为表头，第 3 行起为数据
- 数据永远是最新切片，无需指定快照日期

### 四、字段要求
#### 1）在职明细必填字段
- `WD Employee ID`
- `Employee Type`
- `Region`
- `Country/Territory`
- `BG`

常用补充字段，可按实际情况填写：
- `Work Location`
- `Line`
- `Department`
- `Tencent Organization`
- `Hire Date`

#### 2）离职明细必填字段
- `WD Employee ID`
- `Employee Type`
- `Region`
- `Country/Territory`
- `BG`
- `Termination Date`
- `Termination Category`

常用补充字段：
- `Hire Date`
- `Last Day of Work`

#### 3）外包人员明细必填字段
- `HQ Employee ID`（或含 Employee ID 的列）
- `WeCom Name`（用于区分 Contractor / Partner，`v_` 前缀 = Contractor，`p_` 前缀 = Partner）
- `Country/Territory`（中文国家名，Skill 内置中英文映射）
- `BG`

### 五、枚举值要求
#### Employee Type
仅支持：
- `Regular`
- `Intern`

#### Region
建议统一填写：
- `Americas`
- `APAC`
- `EMEA`
- `Greater China`

#### Termination Category
仅支持：
- `Terminate Employee > Voluntary`
- `Terminate Employee > Involuntary`
- `Terminate Employee > Others`
- `Terminate Employee > Statutory Termination`

### 六、推荐使用方式
#### 场景 1：生成完整 5 个标准看板
1. 准备至少 1 份在职明细 Excel
2. 如需离职分析，再准备 1 份离职明细 Excel
3. 如需外包人员分布，再准备 1 份 Contingent Worker Excel
4. 在 CodeBuddy 中调用本 Skill
5. 上传 Excel 附件并说明"按默认看板生成"

可直接对 Skill 说：
- "请根据我上传的明细生成标准人力看板。"
- "请输出 HTML 看板。"
- "请输出 HTML、PNG、Excel、PPT 和 ZIP。"

#### 场景 2：补充历史月份做同比/环比
如果你希望看板 1 的同比/环比更完整，建议同时上传多个不同月份的在职快照文件。

#### 场景 3：仅生成外包人员看板
只上传 Contingent Worker 文件，Skill 会在有 active 文件的基础上追加看板 5。

### 七、生成结果说明
Skill 会固定输出以下 **5 个标准看板**：
- **看板 1**：正式员工趋势图（ECharts 交互式同比 + 环比分组柱状图，支持 tooltip 悬停、图例、自适应窗口）
- **看板 2**：期末在离职分析（ECharts 交互式双饼图，支持 tooltip 悬停、富文本标题高亮、自适应窗口）
- **看板 3**：Active Regular & Intern 明细汇总表
- **看板 4**：Attrition Regular 离职分析表
- **看板 5**：Active Contractor & Partner（外包人员按 BG × Region × Country 分布表）

> 看板 5 仅在上传了 Contingent Worker 文件时生成。

#### 📧 一键生成邮件功能
看板页面的 Executive Summary 区域提供 **「✉️ 生成邮件」** 按钮，点击后：
1. 自动将完整看板（含图表图片）复制到系统剪贴板
2. 自动唤起系统/企微邮件客户端
3. 邮件主题自动填充为 `YYYYMMDD在职&累计离职人员数据统计看板 - 海外各区域及国内NHS试点`
4. 邮件正文预填 Executive Summary 纯文本摘要
5. 用户只需在邮件正文中 `Ctrl+V` / `Cmd+V` 即可粘贴带图表的富文本版完整看板

邮件格式优化说明：
- **标题处理**：复制时去掉 Executive Summary 标题，保留各看板标题和备注标题
- **图表排布**：看板 1&2 的 4 张图表使用 `<table>` 布局横向排列（邮件客户端不支持 CSS flex）
- **表格颜色**：保留表格原有的区域底色、表头背景色和文字颜色
- **表格居中**：看板 3/4/5 所有表格单元格内容居中显示（含 Region 列）
- **单元格合并**：「海外合计」和「海外合计（含试点国内）」行的 Region 和 Country 列合并为 `colspan=2`

### 八、常见问题
#### 1）能不能只传在职文件？
可以。Skill 仍会生成看板 1-3 和看板 4（降级提示数据不完整）。

#### 2）能不能用文件名区分 active 和 termination？
不建议。Skill 以**第 1 行报表名称**为准自动识别文件类型。

#### 3）可以上传多个在职文件吗？
可以，系统会按快照日期识别月份并自动组合。

#### 4）如果出现未知 BG 怎么办？
不会阻塞生成，但会在摘要中提示你有未识别 BG，方便你后续修正源数据。

#### 5）外包人员文件中的国家名是中文怎么办？
Skill 内置了 40+ 个常见国家的中英文映射表，会自动转换。如果出现未映射的国家名，会保留原始值。

### 九、给业务同学的最简操作建议
- 不要删除第 1 行元数据和第 2 行表头
- 日期统一写成 `YYYY-MM-DD`
- 在职、离职和外包人员文件分开上传
- 如果需要完整趋势，尽量一次上传多个历史月份在职快照
