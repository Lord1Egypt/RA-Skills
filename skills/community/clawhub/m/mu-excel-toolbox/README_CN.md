<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-excel-toolbox" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 📊 mu-excel-toolbox · Excel全能工具箱

> 一个 Skill 搞定 Excel 全生命周期——**读写创建** · **合并拆分** · **清洗校验** · **透视图表** · **模板填充** · **加密保护**，对 Agent 说人话就行。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-excel-toolbox/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill%E9%9B%86%E5%90%88-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-excel-toolbox)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-excel-toolbox)](https://github.com/muippt/mu-excel-toolbox/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-excel-toolbox)](https://github.com/muippt/mu-excel-toolbox/stargazers)

## 💡 使用场景示例

- 📋 **快速预览**："帮我看看这个Excel有几个Sheet，每个Sheet有多少行、哪些列"
- 📎 **合并报表**："把这5个月度销售报表合并成一个年度汇总表"
- ✂️ **按部门拆分**："按'部门'列拆分花名册，每个部门一个独立Excel"
- 🧹 **数据清洗**："把空行删掉，手机号统一11位，日期格式统一成YYYY-MM-DD"
- 🔗 **VLOOKUP关联**："用工号把花名册和考勤表关联起来"
- 📊 **图表生成**："用这份销售数据生成一个柱状图+折线图组合"
- 📈 **数据透视**："按部门和月份交叉汇总销售额"
- 📄 **模板填充**："用员工数据批量生成offer letter"
- 🔍 **差异对比**："对比两版花名册，哪些人新增、离职、信息变更了"
- 🔒 **文件加密**："给薪酬表加密码保护"

## ✨ 核心亮点

### 🛠️ 22 项功能全覆盖

从"打开看看"到"加密交付"，Excel 工作流的每一步都有对应工具，无需切换多个软件：

| 类别 | 功能 | 说明 |
|------|------|------|
| 📖 读写 | 智能预览 / 读取 / 写入创建 | 自动识别 Sheet 结构、列名、数据类型 |
| 🔄 转换 | 格式互转 | xlsx ↔ csv ↔ json ↔ tsv，编码自适应 |
| 📎 整合 | 合并 / 拆分 / 按列值拆分 | 多文件合并、按 Sheet 或列值拆分 |
| 🔗 关联 | VLOOKUP 关联 / 去重 | 跨表关联、智能去重保留最新 |
| 🧹 清洗 | 数据清洗 / 数据校验 | 空行清理、格式统一、规则校验 |
| 📄 模板 | 模板填充 | 批量生成 offer letter 等标准化文档 |
| 💅 样式 | 条件格式 / 样式排版 | 自动标红标绿、表头美化、列宽自适应 |
| 📐 计算 | 函数公式 / 数据透视表 | 自动插入 SUM/AVERAGE 等公式、交叉汇总 |
| 📊 可视化 | 图表生成 / 数据分析 | 柱状图、折线图、饼图、组合图表 |
| 🔍 对比 | 差异对比 / 图片插入 | 两版文件逐行比对、批量插入图片 |
| 🔒 安全 | 密码保护 | 文件级加密/解密 |

### ⚡ 大文件无惧 — 10万+行流式处理

不是"先全部加载到内存再处理"，而是自动检测文件大小，超过10万行无缝切换流式读写模式：

- **读取**：自动启用 read_only 模式，内存占用降低 90%+
- **写入**：自动启用 write_only 模式，边生成边写入
- **容错**：遇到坏行/坏单元格跳过继续，最后汇总错误报告

### 🧹 8 大数据清洗规则

HR 和业务场景最常见的脏数据问题，一条命令搞定：

1. 删除空行/空列
2. 去除首尾空格
3. 手机号统一11位格式
4. 日期统一为 YYYY-MM-DD
5. 金额格式标准化
6. 身份证号格式校验
7. 邮箱格式校验
8. 重复数据标记

### 📐 5 种输出格式

所有脚本统一支持多格式输出，方便对接不同下游场景：

| 格式 | 用途 |
|------|------|
| json | 程序对接 / API 传输 |
| csv | 轻量交换 / 导入其他系统 |
| markdown | 文档嵌入 / 即时阅读 |
| table | 终端美观展示 |
| xlsx | 标准 Excel 输出 |

### 🔒 文件级加密保护

薪酬表、绩效数据这些敏感文件，一条命令加密码保护，也能一条命令解密打开：

- 支持设置/修改/移除密码
- 基于 msoffcrypto-tool 的标准 Office 加密
- 兼容 Microsoft Office / WPS / LibreOffice

## 📌 与同类工具对比

### mu-excel-toolbox vs 手动 Excel 操作

| 维度 | mu-excel-toolbox | 手动操作 |
|------|------------------|----------|
| 合并10个报表 | 1条命令，秒级完成 | 逐个复制粘贴，10-30分钟 |
| 按部门拆分 | 1条命令自动拆分 | 筛选→复制→新建→粘贴，循环N次 |
| 数据清洗 | 8种规则一键执行 | 手动查找替换，容易遗漏 |
| VLOOKUP关联 | 自动匹配+结果导出 | 写公式→拖拽→排错，易出错 |
| 差异对比 | 逐行比对+变更报告 | 肉眼比对，100行以上就崩溃 |
| 批量模板填充 | 数据+模板→批量生成 | 逐份修改，重复劳动 |
| 大文件处理 | 流式模式，不卡不崩 | Excel打开就转圈 |

### mu-excel-toolbox vs Python 脚本自己写

| 维度 | mu-excel-toolbox | 自己写脚本 |
|------|------------------|------------|
| 上手门槛 | 自然语言描述需求即可 | 需要会 Python + openpyxl/pandas |
| 功能覆盖 | 22项开箱即用 | 每个需求从零写起 |
| 大文件处理 | 自动切换流式模式 | 需要自己实现流式逻辑 |
| 错误处理 | 内置容错+错误报告 | 一个bug调半天 |
| 编码问题 | 自动识别 UTF-8/GBK/GB2312 | UnicodeDecodeError 经典噩梦 |
| 安全备份 | 写入自动备份原文件 | 覆盖了就没了 |
| 维护成本 | Skill 统一更新 | 散落脚本无人维护 |

## 🚀 22 项功能速查

| # | 功能 | 一句话说明 | 触发词示例 |
|---|------|-----------|-----------|
| 1 | 📋 智能预览 | 看文件有几个Sheet、列名、行数、数据类型 | "帮我看看这个Excel" |
| 2 | 📖 读取 | 按Sheet/列/行范围精确读取数据 | "读取Sheet2的A到D列" |
| 3 | ✏️ 写入/创建 | 把数据写入新Excel文件 | "把这份数据生成Excel" |
| 4 | 🔄 格式互转 | xlsx ↔ csv ↔ json ↔ tsv | "把csv转成xlsx" |
| 5 | 📎 合并 | 多文件/多Sheet合并 | "合并这5个月度报表" |
| 6 | ✂️ 拆分 | 按Sheet拆分为独立文件 | "把大表按Sheet拆开" |
| 7 | ✂️ 按列值拆分 | 按指定列的值分组拆分 | "按部门拆分" |
| 8 | 🔗 VLOOKUP | 跨表关联匹配 | "用工号关联两张表" |
| 9 | 🧹 去重 | 按指定列去重 | "按姓名+手机号去重" |
| 10 | 🧽 数据清洗 | 空行清理、格式统一 | "清理脏数据" |
| 11 | 📄 模板填充 | 数据+模板批量生成文档 | "批量生成offer letter" |
| 12 | ✅ 数据校验 | 邮箱/工号/身份证格式校验 | "检查哪些邮箱格式不对" |
| 13 | 🎨 条件格式 | 按规则自动标色 | "低于60标红，高于90标绿" |
| 14 | 💅 样式排版 | 表头美化、列宽自适应 | "给表头加粗加背景色" |
| 15 | 📐 函数公式 | 自动插入Excel公式 | "在E列加SUM汇总" |
| 16 | 📊 图表 | 柱状图/折线图/饼图/组合图 | "生成销售柱状图" |
| 17 | 📈 数据透视表 | 交叉汇总分析 | "按部门月份汇总销售额" |
| 18 | 🔬 数据分析 | 统计摘要：均值/中位数/分布 | "给我统计摘要" |
| 19 | 🔍 差异对比 | 两版文件逐行比对 | "对比两版花名册" |
| 20 | 🖼️ 图片插入 | 批量插入图片到对应行 | "在每行插入员工照片" |
| 21 | 🔒 密码保护 | 文件加密/解密 | "给薪酬表加密码" |
| 22 | ⚡ 大文件 | 10万+行自动流式处理 | 自动触发，无需手动 |

## ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 运行环境 | 任意支持 Skills/prompts 的 AI Agent 框架（如 Claude Code、Cursor、Windsurf） |
| Python 版本 | 3.9+ |
| 核心依赖 | openpyxl / pandas / xlsxwriter / xlrd / msoffcrypto-tool |
| 输入格式 | .xlsx / .xls / .csv / .tsv / .json |
| 输出格式 | .xlsx / .csv / .json / .tsv / markdown / table |
| 大文件阈值 | 10万行自动切换流式模式 |
| 编码支持 | UTF-8 / GBK / GB2312 / Latin-1 自动识别 |
| 脚本数量 | 20 个独立 Python 脚本 + 1 个公共模块 |
| 代码行数 | 5,636 行 |

## 🛠️ 快速开始

**第一步：安装**

```bash
# 解压到你的 Agent 的 skills 目录
unzip mu-excel-toolbox.zip -d ./mu-excel-toolbox

# 依赖会在首次运行时自动安装，也可手动安装
pip install -r ./mu-excel-toolbox/scripts/requirements.txt
```

**第二步：开始使用**

直接对 Agent 说你想做什么，Skill 会自动路由到对应工具：

```
# 看看文件长什么样
"帮我看看 sales.xlsx 有什么内容"

# 合并多个报表
"把 1月.xlsx 到 12月.xlsx 合并成年度汇总"

# 数据清洗 + 校验
"清理这份花名册的脏数据，检查手机号和邮箱格式"

# 生成图表
"用销售数据画一个按月份的柱状折线组合图"
```

> 💡 首次运行会自动安装依赖（约30秒），之后即装即用。

## 🔒 安全与隐私

- 所有脚本在本机执行，Skill 本身不会主动上传文件到任何第三方服务
- 通过 AI Agent 使用时，对话内容会经过大模型处理，请注意敏感数据
- 无遥测、无数据采集、无使用追踪
- 写入操作自动备份原文件，防止数据丢失
- MIT License 开源友好，可自由修改和分发

## ⭐ Star 趋势

如果这个项目对你有帮助，请给一个 ⭐！

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-excel-toolbox&type=date)

> 一句话总结：不用写代码、不用装插件，对 Agent 说人话就能搞定 Excel 的一切。

## 👤 作者简介

🎓 清华大学出版社签约作家 / 2026当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

## 📄 许可证与致谢

[MIT](LICENSE) © 2026 木先生iPPT

感谢 [openpyxl](https://openpyxl.readthedocs.io/) · [pandas](https://pandas.pydata.org/) · [xlsxwriter](https://xlsxwriter.readthedocs.io/) · [xlrd](https://github.com/python-excel/xlrd) · [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) 等优秀开源项目提供的技术基建。

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 Issue。
