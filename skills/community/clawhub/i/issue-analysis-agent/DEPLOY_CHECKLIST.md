# 📋 发布前检查清单

**技能名称**: issue-analysis-agent  
**版本**: v2.1.0  
**最后更新**: 2026-03-24

---

## ✅ 检查清单

### 1️⃣ 数据文件检查

- [ ] Excel 文件存在且可读
- [ ] 数据格式正确（包含必要列：问题 ID、状态、类型、平台、反馈人、解决人、模块等）
- [ ] 数据无异常（无空值、格式错误）

**自动检查命令**:
```bash
python3 check_before_deploy.py analysis_data_latest.json
```

---

### 2️⃣ JSON 字段名检查

确保 JSON 中包含以下字段（字段名必须完全一致）：

**必需字段**:
- [ ] `summary` - 汇总数据
  - [ ] `summary.total` - 问题总数
  - [ ] `summary.resolved` - 已解决数
  - [ ] `summary.unresolved` - 未解决数
  - [ ] `summary.rate` - 解决率（百分比字符串，如 "85%"）
  - [ ] `summary.week_num` - 周数（如 12）

- [ ] `weekly_trend` (或兼容字段 `weekly`) - 每周趋势数据
- [ ] `issue_types` (或兼容字段 `types`) - 问题类型分布
- [ ] `platforms` - 平台分布
- [ ] `reporters` - 反馈人统计
- [ ] `resolvers` - 解决人统计
- [ ] `unresolved_resolvers` - 未解问题人统计
- [ ] `unresolved_modules` - 未解决问题模块统计

**字段名统一规则**:
- 优先使用标准字段名（如 `weekly_trend`, `issue_types`）
- 支持旧字段名兼容（`weekly`, `types`）
- 所有字段从 JSON 动态读取，不硬编码

---

### 3️⃣ HTML 报告检查

**结构检查**:
- [ ] DOCTYPE 声明正确
- [ ] HTML 标签完整
- [ ] 字符集声明（UTF-8）
- [ ] Chart.js 库已引入

**图表检查**（6 个图表必须全部存在）:
- [ ] `weeklyChart` - 每周新增问题趋势图
- [ ] `typeChart` - 问题类型分布图
- [ ] `platformChart` - 平台问题分布图
- [ ] `reporterChart` - 反馈人 TOP5 图
- [ ] `resolverChart` - 解决人 TOP5 图
- [ ] `unresolvedResolverChart` - 未解问题人 TOP5 图

**图表标题检查**:
- [ ] 📈 每周新增问题趋势
- [ ] 🏷️ 问题类型分布
- [ ] 💻 平台问题分布 TOP5
- [ ] 👤 反馈人 TOP5
- [ ] ✅ 解决人 TOP5
- [ ] 📋 未解问题人 TOP5（解决者中未解决问题最多的）
- [ ] 📦 未解决问题模块 TOP10

**样式检查**:
- [ ] 移除不必要的红色警告样式
- [ ] 未解决数字使用蓝色（info）而非红色（warning）
- [ ] 中文显示正常（无乱码）

**自动检查命令**:
```bash
python3 check_before_deploy.py analysis_data_latest.json report_cn_latest.html
```

---

### 4️⃣ 响应头检查

上传到 COS 后，必须设置以下响应头：

- [ ] `Content-Type: text/html; charset=utf-8`
  - 确保浏览器正确解析 HTML
  - 确保中文正常显示

- [ ] `Content-Disposition: inline`
  - 确保在浏览器中打开，而不是下载

- [ ] `Cache-Control: public, max-age=0`
  - 确保不缓存，始终看到最新数据
  - 或 `no-cache` 也可接受

**验证方法**:
```bash
curl -I https://claw-1301484442.cos.ap-shanghai.myqcloud.com/reports/issue_analysis/report_cn_latest.html
```

**自动检查命令**:
```bash
python3 check_before_deploy.py analysis_data_latest.json report_cn_latest.html https://claw-1301484442.cos.ap-shanghai.myqcloud.com/reports/issue_analysis/report_cn_latest.html
```

---

### 5️⃣ 上传验证检查

上传到 COS 后，自动执行以下验证：

- [ ] HTTP 状态码 200
- [ ] 内容长度一致
- [ ] 内容完全一致（无篡改）
- [ ] 响应头正确

**重试机制**:
- 如果验证失败，自动重试（最多 3 次）
- 每次重试间隔递增（2 秒、4 秒、6 秒）

---

### 6️⃣ 数据质量检查

- [ ] 问题总数 > 0
- [ ] 解决率 >= 80%（良好）
- [ ] 解决率 >= 50%（需关注）
- [ ] 解决率 < 50%（过低，需告警）
- [ ] 数据一致性：已解决 + 未解决 = 总数
- [ ] 每周趋势数据存在

---

## 🚀 发布流程

### 完整流程（推荐）

```bash
# 步骤 1: 运行完整周报生成流程（包含所有检查）
python3 weekly_report.py issue_data_week_12.xlsx

# 步骤 2: 如果需要单独检查
python3 check_before_deploy.py analysis_data_latest.json report_cn_latest.html [COS 链接]
```

### 手动流程

```bash
# 步骤 1: 分析数据
python3 analyze.py issue_data_week_12.xlsx

# 步骤 2: 生成报告
python3 generate_report.py analysis_data_latest.json report_cn_latest.html

# 步骤 3: 检查报告
python3 check_before_deploy.py analysis_data_latest.json report_cn_latest.html

# 步骤 4: 上传到 COS
python3 upload_cos.py report_cn_latest.html reports/issue_analysis/report_cn_latest.html

# 步骤 5: 验证上传
curl -I https://claw-1301484442.cos.ap-shanghai.myqcloud.com/reports/issue_analysis/report_cn_latest.html
```

---

## ⚠️ 常见问题

### 1. 字段名不一致

**问题**: JSON 字段名与代码中使用的字段名不一致

**解决**: 
- 使用标准字段名（`weekly_trend`, `issue_types` 等）
- 或更新代码支持兼容字段

### 2. 图表不显示

**问题**: 图表区域空白

**可能原因**:
- Chart.js 库未正确引入
- 数据格式错误
- canvas 元素 ID 不匹配

**解决**: 运行 `check_before_deploy.py` 检查

### 3. 响应头不正确

**问题**: 浏览器下载文件而不是打开

**解决**: 
- 检查 `upload_cos.py` 中的 `ContentDisposition` 设置
- 重新上传文件

### 4. 中文乱码

**问题**: 报告中中文显示为乱码

**解决**:
- 确保文件保存为 UTF-8 编码
- 确保 HTML 中 `<meta charset="UTF-8">` 存在
- 确保 COS 响应头包含 `charset=utf-8`

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v2.1.0 | 2026-03-24 | 统一字段名、添加验证、移除红色警告样式 |
| v2.0.0 | 2026-03-23 | 初始版本 |

---

## 👥 团队分工

- **找茬 🐛**: 数据分析（读取 Excel、统计分析）
- **画师 🎨**: 报告生成（HTML 可视化、上传 COS、验证）

---

**最后更新**: 2026-03-24  
**维护者**: 画师 🎨
