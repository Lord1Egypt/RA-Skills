# 版式规范

## 通用风格

- 标题、备注、脚注：中文
- 国家、Region、BG 名称：英文
- 输出风格：中英混排
- 整体观感：接近管理汇报页，而非通用 BI 控件风格

## 颜色规范

- `Americas`：蓝色 `#1F6B8F`
- `APAC`：橙色 `#ED7D31`
- `EMEA`：绿色 `#2E7D32`
- 表格表头：浅蓝 `#B7D7E8`
- 海外合计 / 总计行：亮蓝 `#4FA9D5`
- Americas 区域底色：浅杏色 `#F5E1D6`
- APAC 区域底色：浅蓝灰 `#DCE8F4`
- EMEA 区域底色：米色 `#F3E0D4`
- Greater China 区域底色：浅灰蓝 `#D8E3EE`

## 看板 1

- 标题：看板1：正式员工趋势图
- **使用 ECharts 原生交互式分组柱状图**（取代静态 matplotlib PNG）
- 采用双图布局：左侧同比（flex:1）、右侧近三个月环比（flex:1.45）
- 柱子上直接显示人数（bar label）
- 最新月份虚线高亮（markArea）
- 右上角显示"最新月份: YYYY Mon"标注（graphic text）
- 图例（legend）居中展示 Americas / APAC / EMEA
- 鼠标悬停显示 tooltip 交互
- 窗口自适应 resize
- 若数据不完整，底部显示橙色注释
- ECharts CDN 引入：`echarts@5`（通过 jsDelivr）
- matplotlib PNG 渲染保留，供 Excel/PPT 导出使用

## 看板 2

- 标题：看板2：期末在离职分析
- **使用 ECharts 原生交互式饼图**（取代静态 matplotlib PNG）
- 使用双饼图布局：左侧在职人数（浅蓝灰背景 `#dfe8f1`）、右侧年内离职人数（暖杏色背景 `#eadccf`）
- 饼图内标签显示 `Region\nN人 X%`
- Rich text 标题："在职"用蓝色 `#1565C0` 高亮，"离职"用红色 `#C62828` 高亮
- 鼠标悬停显示 tooltip（人数 + 占比详情）
- 保持颜色与看板 1 一致（Americas 蓝、APAC 橙、EMEA 绿）
- 窗口自适应 resize

## 看板 3

- 输出宽表
- 第一列：`Region`（相同 Region 的国家合并单元格）
- 第二列：`Country/Territory`
- 后续为 `合计 / BG` 分组下的 `Regular / Intern`
- Region subtotal 行、海外合计、海外合计（含试点国内）必须高亮
- 所有表格单元格内容居中显示（含 Region 列）
- 「海外合计」和「海外合计（含试点国内）」行 Region+Country 合并为 `colspan=2`

## 看板 4

- 输出表格
- 建议列顺序：
  - `Region`
  - `Country/Territory`
  - `Start HC`
  - `End HC`
  - `No. of Attrition`
  - `Attrition %`
  - `Voluntary`
  - `Involuntary`
  - `Others`（No.、% of Involuntary；若数据为空不展示该列）
  - `Statutory`（No.、% of Involuntary；若数据为空不展示该列）
- Region subtotal 行高亮
- 百分比保留 1 位小数
- 所有表格单元格内容居中显示（含 Region 列）
- 「海外合计」行 Region+Country 合并为 `colspan=2`

## 看板 5

- 仅在上传了 Contingent Worker 文件时生成
- 输出宽表，样式与看板 3 一致
- 第一列：`Region`（相同 Region 的国家合并单元格）
- 第二列：`Country/Territory`（英文名，由中文映射而来）
- 后续为 `合计 / BG` 分组下的 `Contractor / Partner` 子列
- 使用 grouped header：上层为 BG 名称，下层为 Contractor / Partner
- 颜色与高亮规则与看板 3 相同（Americas / APAC / EMEA 区域底色 + 海外合计高亮）
- 所有表格单元格内容居中显示（含 Region 列）
- 「海外合计」行 Region+Country 合并为 `colspan=2`
- 表格下方有"复制"按钮

## HTML

- 使用单页交互式展示
- 引入 ECharts CDN（`echarts@5`，通过 jsDelivr）
- 顶部放置 Executive Summary（可编辑、可复制）
- 每个看板作为独立 section
- **看板 1 和看板 2 使用 ECharts 原生交互式图表**（分组柱状图 + 饼图），支持 tooltip、legend、responsive resize
- 看板 3-5 使用 HTML 表格
- CSS 内联到 HTML 中
- 交互功能：图表 tooltip 悬停、表格复制按钮、Executive Summary 编辑/保存/复制
- 一键生成邮件：复制时仅去掉 Executive Summary 标题，保留看板标题和备注标题；图表用 `<table>` 横排（邮件客户端不支持 flex）；保留表格行/单元格的原有背景颜色
- matplotlib PNG 渲染仍保留在脚本中，供 Excel/PPT 导出使用（HTML 不再使用）

## PowerPoint

- 4 页标准页，每页 1 个看板（看板 5 为表格形式仅在 HTML 中展示）
- 页面顶部放中文标题
- 图片尽量铺满内容区
- 页脚可带生成日期与数据完整性备注
