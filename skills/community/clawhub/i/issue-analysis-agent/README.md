# 📞 客服周报技能 - 使用说明

**技能位置**: `/Users/master.yu/.openclaw/workspace/skills/issue-analysis-agent/`
**版本**: v1.1.0（2026-03-23 更新）

---

## 🚀 快速开始

### 方式 1：一键生成（推荐）

```bash
cd /Users/master.yu/.openclaw/workspace/skills/issue-analysis-agent
python3 weekly_report.py /path/to/issue_data.xlsx
```

**输出**:
- ✅ 自动分析数据
- ✅ 生成 HTML 报告
- ✅ 上传到 COS
- ✅ 返回公网链接

### 方式 2：分步执行

```bash
# 1. 分析数据
python3 analyze.py issue_data.xlsx

# 2. 生成报告
python3 generate_report.py analysis_data_latest.json report_cn.html

# 3. 上传 COS
python3 upload_cos.py report_cn.html reports/issue_analysis/report_cn_latest.html
```

---

## 📥 输入要求

### Excel 文件格式

**必需列名**（支持中文）：
- 问题描述 / 问题内容
- 提交日期 / 周次
- 所属平台 / 平台
- 问题模块 / 模块
- 反馈人 / 提交人
- 解决人 / 处理人
- 状态 / 问题解决状态
- 问题类型 / 类型

**可选列名**：
- 优先级
- 创建时间
- 解决时间
- 备注

---

## 📤 输出内容

### 1. 结构化数据
`output/analysis_data.json`
```json
{
  "summary": {
    "total_issues": 237,
    "resolved": 194,
    "unresolved": 43
  },
  "weekly_counts": {...},
  "type_top5": [...],
  "platform_top5": [...],
  ...
}
```

### 2. 文字总结
`output/analysis_summary.md`
- 核心指标表格
- 趋势分析
- TOP5 排行
- 关键发现

### 3. 可视化报告
`output/report_cn.html`
- HTML 交互式报告
- Chart.js 图表
- 中文完美显示

### 4. COS 链接
```
https://claw-1301484442.cos.ap-shanghai.myqcloud.com/reports/issue_analysis/report_cn_latest.html
```

---

## 🔄 每周更新流程

### 固定流程（每周一）

1. **接收数据** (10:00)
   - 用户上传最新 Excel 文件
   - 保存到 `issue_data_week_XX.xlsx`

2. **数据分析** (10:00-10:30)
   - 读取 Excel
   - 统计分析
   - 对比上周

3. **生成报告** (10:30-11:00)
   - HTML 报告生成
   - 图表绘制
   - 文字总结

4. **上传 COS** (11:00-11:10)
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

## 📊 报告模板

### 核心指标
- 问题总数
- 已解决数/解决率
- 未解决数
- 环比变化

### 6 大图表
1. 每周新增趋势（折线图）
2. 问题类型分布（饼图）
3. 平台分布 TOP5（横向柱状图）
4. 反馈人 TOP5（柱状图）
5. 解决人 TOP5（柱状图 + 金银铜）
6. 未解决问题 TOP10（表格）

### 关键洞察
- 问题高发期
- 主要问题类型
- 重点优化平台
- 待优先处理模块

---

## ⚠️ 自动告警规则

触发以下情况立即通知：

| 指标 | 预警线 | 动作 |
|------|--------|------|
| 解决率 | <80% | 🔴 高优先级告警 |
| 单周新增 | >50 个 | 🔴 高优先级告警 |
| Bug 占比 | >60% | 🟡 中优先级告警 |
| 卖家端占比 | >60% | 🟡 中优先级告警 |
| 某模块未解决 | >5 个 | 🟡 中优先级告警 |

---

## 📁 文件归档

### 本地归档
```
/workspace/projects/issue_analysis/
├── issue_data_week_10.xlsx
├── issue_data_week_11.xlsx
├── issue_data_week_12.xlsx
└── report/
    ├── report_week_10.html
    ├── report_week_11.html
    └── report_week_12.html
```

### COS 归档
```
reports/issue_analysis/
├── report_cn_latest.html（最新，覆盖）
└── history/
    ├── report_week_10.html
    ├── report_week_11.html
    └── report_week_12.html
```

---

## 🛠️ 技术依赖

```bash
# Python 依赖
pip3 install openpyxl qcloud_cos

# Node.js 依赖（可选，用于 HTML 优化）
npm install chart.js
```

---

## 📝 常见问题

### Q: Excel 文件读取失败？
A: 检查列名是否匹配，支持中英文列名映射

### Q: 图表中文显示为方框？
A: 使用 Chart.js（浏览器渲染），避免 matplotlib

### Q: COS 上传失败？
A: 检查 AccessKey 权限，确保有写权限

### Q: 报告链接无法访问？
A: 检查文件 ACL 是否设置为 public-read

---

## 📞 负责人

- **技能开发**: 老六 🥷
- **数据提供**: 客服团队
- **报告接收**: 三疯

---

*最后更新：2026-03-23*
