# 📊 客服问题周报技能

**技能名称**: issue-analysis-agent  
**版本**: v2.0.0  
**作者**: 老六 🥷  
**创建时间**: 2026-03-23  
**更新时间**: 2026-03-23  

---

## 📋 技能描述

自动化分析客服问题收集表（Excel），生成可视化分析报告，支持每周数据更新和趋势对比。

**团队协作模式**：
- 🐛 **找茬** - 数据分析（读取 Excel、统计分析、未解问题人统计）
- 🎨 **画师** - 报告生成（HTML 可视化、图表绘制、COS 上传）

---

## 🎯 核心功能

1. **数据读取** - 自动解析 Excel 文件，识别字段
2. **统计分析** - 问题总数、解决率、趋势分析
3. **TOP5 排行** - 反馈人、解决人、未解问题人等
4. **可视化报告** - HTML 交互式报告（Chart.js，8 个图表）
5. **COS 上传** - 自动生成公网访问链接
6. **周报对比** - 与上周数据对比，分析趋势
7. **自动告警** - 解决率<80%、单周>50 个等阈值告警

---

## 📥 输入

- **文件格式**: `.xlsx` Excel 文件
- **必需字段**:
  - 问题描述
  - 提交日期/所属周
  - 所属平台
  - 问题模块
  - 反馈人
  - 解决者
  - 解决状态（已解决/待解决等）
  - 问题类型（Bug/咨询/需求等）

---

## 📤 输出

1. **结构化数据** - `analysis_data_latest.json`
2. **文字总结** - `analysis_summary.md`
3. **可视化报告** - `report_cn_latest.html`（HTML 交互式，8 个图表）
4. **COS 链接** - 公网访问地址

---

## 🚀 使用方法

### 方式 1：完整流程（推荐）
```bash
cd /Users/master.yu/.openclaw/workspace/skills/issue-analysis-agent
python3 weekly_report.py /path/to/issue_data.xlsx
```

### 方式 2：分步执行
```bash
# 步骤 1: 分析数据（找茬 🐛）
python3 analyze.py /path/to/issue_data.xlsx

# 步骤 2: 生成报告（画师 🎨）
python3 generate_report.py analysis_data_latest.json report_cn.html

# 步骤 3: 上传 COS（画师 🎨）
python3 upload_cos.py report_cn.html reports/issue_analysis/report_cn_latest.html
```

### 方式 3：Agent 调用
```
任务：分析本周客服问题数据
技能：issue-analysis-agent
输入：issue_data_week_12.xlsx
输出：可视化报告 + COS 链接
```

---

## 📊 报告内容

### 8 大图表
1. 📈 每周新增问题趋势（折线图）
2. 🏷️ 问题类型分布（饼图）
3. 💻 平台问题分布 TOP5（横向柱状图）
4. 👤 反馈人 TOP5（柱状图）
5. ✅ 解决人 TOP5（柱状图）
6. ⚠️ **未解问题人 TOP5**（柱状图）- 解决者中未解决问题最多的
7. ⚠️ 未解决问题模块 TOP10（表格）

### 核心指标
- 问题总数
- 已解决数/解决率
- 未解决数
- 环比变化

### 自动告警
- 🔴 解决率 <80%
- 🔴 单周新增 >50 个
- 🟡 Bug 占比 >60%
- 🟡 卖家端占比 >60%

---

## 🔄 每周更新流程

### 固定流程（每周一）

1. **接收数据** (10:00)
   - 用户上传最新 Excel 文件
   - 保存到 `issue_data_week_XX.xlsx`

2. **数据分析** (10:00-10:30) 🐛 找茬
   - 读取 Excel
   - 统计分析
   - 对比上周

3. **生成报告** (10:30-11:00) 🎨 画师
   - HTML 报告生成
   - 图表绘制
   - 数据验证

4. **上传 COS** (11:00-11:10) 🎨 画师
   - 上传文件
   - 设置权限
   - 生成链接

5. **推送通知** (11:10-11:20)
   - 发送报告链接
   - 关键发现摘要
   - 预警信息

6. **归档历史** (11:20-11:30)
   - 保存本周报告
   - 更新索引
   - 清理临时文件

---

## 📁 文件结构

```
issue-analysis-agent/
├── SKILL.md              # 技能说明
├── README.md             # 使用说明
├── config.json           # 配置项
├── weekly_report.py      # 主流程脚本
├── analyze.py            # 数据分析（找茬 🐛）
├── generate_report.py    # 报告生成（画师 🎨）
├── upload_cos.py         # COS 上传（画师 🎨）
├── output/               # 输出目录
│   ├── analysis_data.json
│   ├── analysis_summary.md
│   └── report_cn.html
└── reports/              # 历史报告归档
    ├── week_10/
    ├── week_11/
    └── week_12/
```

---

## 🛠️ 技术依赖

```bash
# Python 依赖
pip3 install openpyxl qcloud_cos

# Node.js 依赖（可选）
npm install chart.js
```

---

## 📝 更新日志

### v2.0.0 (2026-03-23)
- ✅ 团队协作模式（找茬 + 画师）
- ✅ 新增未解问题人 TOP5 统计
- ✅ 修复字段名不匹配问题
- ✅ 优化 COS 上传响应头
- ✅ 自动告警功能

### v1.0.0 (2026-03-23)
- ✅ 初始版本
- ✅ Excel 数据读取
- ✅ 统计分析
- ✅ HTML 报告生成
- ✅ COS 上传

---

## 📞 负责人

- **技能开发**: 老六 🥷
- **数据分析**: 找茬 🐛
- **报告制作**: 画师 🎨
- **技能维护**: 客服 📞

---

*最后更新：2026-03-23*
