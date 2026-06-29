# 科创线索采集 Skill - 快速上手指南

## 安装 Skill

将 `kechuang-collection` 文件夹放到桌面后，在 Claude Code 中输入:

```
/kechuang-collection
```

Skill 自动加载。

## 常用命令速查

### 1️⃣ 一键扫描最新科创线索
```
/kechuang-collection scan 科技项目申报 2026 --days=7
```

### 2️⃣ 按KPI维度专项扫描
```
# 扫描资质认定类线索
/kechuang-collection scan 高新技术企业 认定

# 扫描资金补贴类线索
/kechuang-collection scan 补贴 资助

# 扫描科技奖项类线索
/kechuang-collection scan 科技奖 评选
```

### 3️⃣ 启动后台定时监控
```
# 启动监控（每2小时自动扫描一次）
/kechuang-collection monitor
```

### 4️⃣ 生成汇总报告
```
# 查看本周发现的所有线索汇总
/kechuang-collection report

# 只看高优先级线索
/kechuang-collection report --kpi=high
```

### 5️⃣ 管理监控源
```
# 查看当前监控的渠道列表
/kechuang-collection list-sources

# 添加自定义监控源（如公司所在园区官网）
/kechuang-collection add-source https://www.example-park.gov.cn
```

## 最佳实践

1. **首次使用**: 建议先运行 `scan` 进行一次全量扫描
2. **日常使用**: 启动 `monitor` 后台监控
3. **每周**: 运行一次 `report` 查看汇总
4. **月底**: 导出报告作为科创工作月报素材

## 定制指南

### 修改KPI权重

编辑 `references/kpi-criteria.md` 文件，根据公司实际考核标准调整权重百分比和匹配关键词。

### 修改监控源

编辑 `references/monitoring-sources.md` 文件，增删目标网站和栏目。

### 添加过滤词

在 `references/kpi-criteria.md` 的「无效信息过滤规则」部分添加或修改过滤词。