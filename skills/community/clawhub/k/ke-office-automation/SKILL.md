---
name: ke-office-automation
description: 科特船长 - 办公自动化脚本，Excel/Word/文件批量处理
version: 1.0.0
metadata: {"openclaw": {"emoji": "🤖", "requires": {"bins": ["python3"]}}}
---

# 办公自动化脚本 - 科特船长版

## 功能说明

提供常用办公自动化脚本，包括：
- Excel 自动汇总
- Word 批量处理
- 文件批量重命名
- PDF 合并/拆分
- 邮件自动发送

## 使用场景

### 财务/会计
- 多表格自动汇总
- 发票数据提取
- 银行流水整理

### HR/行政
- 员工信息整理
- 考勤数据汇总
- 合同批量处理

### 销售/运营
- 客户信息整理
- 订单数据汇总
- 报表自动生成

### 通用场景
- 文件批量重命名
- 文件夹整理
- 数据格式转换

## 使用方法

```bash
# Excel 汇总
clawhub run ke-office-automation --action excel-merge --input ./data/ --output ./merged.xlsx

# Word 批量处理
clawhub run ke-office-automation --action word-batch --input ./docs/ --action-type replace --old "旧文本" --new "新文本"

# 文件批量重命名
clawhub run ke-office-automation --action rename --input ./files/ --pattern "{date}_{original}"

# PDF 合并
clawhub run ke-office-automation --action pdf-merge --input ./pdfs/ --output ./merged.pdf

# 邮件自动发送
clawhub run ke-office-automation --action email-send --config ./email-config.json --data ./recipients.xlsx
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--action` | 操作类型 | 是 |
| `--input` | 输入文件/文件夹路径 | 是 |
| `--output` | 输出文件路径 | 条件必填 |
| `--pattern` | 重命名模式 | 条件必填 |
| `--config` | 配置文件路径 | 条件必填 |

## 可用操作

| 操作 | 说明 | 适用场景 |
|------|------|----------|
| excel-merge | 合并多个 Excel 文件 | 多表格汇总 |
| excel-split | 拆分 Excel 文件 | 数据分发 |
| word-batch | Word 批量处理 | 合同/通知批量修改 |
| rename | 文件批量重命名 | 文件整理 |
| pdf-merge | PDF 合并 | 报告合并 |
| pdf-split | PDF 拆分 | 报告拆分 |
| email-send | 邮件批量发送 | 通知/营销 |

## 定制服务

需要定制自动化脚本？

### 服务类型
- **简单脚本**: ¥500-1000（单一功能）
- **中等复杂**: ¥1000-3000（多步骤）
- **系统级**: ¥3000+（完整流程）

### 典型案例
- 财务日报自动生成：¥1500
- 客户信息自动整理：¥1200
- 合同批量处理：¥2000
- 邮件营销自动化：¥1800

### 服务流程
1. 需求沟通（免费）
2. 方案确认
3. 开发测试（1-3 天）
4. 交付培训
5. 售后支持（30 天免费）

联系：私信获取报价

## 免费资源

提供以下免费脚本模板：
- Excel 汇总脚本
- 文件重命名脚本
- PDF 合并脚本

GitHub: 待开源

## 常见问题

**Q: 需要编程基础吗？**
A: 不需要，按说明使用即可。

**Q: 支持 Mac/Windows 吗？**
A: 都支持，需要安装 Python 3.8+

**Q: 数据安全吗？**
A: 所有处理在本地完成，数据不会上传。

---

**作者**: 科特船长
**更多技能**: https://clawhub.ai/@xiaoheizp
**定制咨询**: 私信获取报价
