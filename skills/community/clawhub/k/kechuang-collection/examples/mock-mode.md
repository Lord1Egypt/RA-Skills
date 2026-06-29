# Mock 模式使用指南

> 无需网络即可体验 kechuang-collection 的全部功能。

## 使用方法

```bash
# 扫描模式（Mock）
/kechuang-collection scan 高新技术企业 认定 --mock

# 监控模式（Mock）
/kechuang-collection monitor --mock

# 报告模式（Mock）
/kechuang-collection report --mock
```

## Mock 数据说明

预置 5 条示例科创线索，覆盖：

| KPI维度 | 线索数 | 覆盖情况 |
|---------|--------|---------|
| 🏆 科技奖 | 1 | 省科技奖提名通知 |
| 🏭 资质认定 | 2 | 高企认定、专精特新 |
| 📋 项目立项 | 1 | 重点研发计划立项公示 |
| 📐 标准制定 | 1 | 团体标准征集 |

数据来源：`scripts/mock-data.js`

## 验证清单

- [ ] `scan --mock` 输出表格和线索卡片
- [ ] `report --mock` 输出汇总报告
- [ ] 所有数据为模拟数据，不涉及真实信息
- [ ] 输出格式与真实模式一致