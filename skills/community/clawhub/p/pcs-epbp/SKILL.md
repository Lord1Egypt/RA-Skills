---
name: pcs-epbp
description: 从pcs页面获取数据导入到epbp
author: Digital Employee Platform Team
category: productivity
tags:
  - pcs
  - epbp
  - RPA
  - excel

triggers:
  - pcs
  - epbp
  - RPA
  - 数据转储

config:
  pcs_url: "http://10.68.160.117:5173"
  pcs_page: "/#/vmodelDemo"
  epbp_page: "/#/home"
  fields:
    - 站库名称
    - 设备名称
    - 采集时间
    - 运行时长(小时)
    - 进口压力(MPa)
    - 泵压力(MPa)

requires:
  python: true
  playwright: true
---

# PCS数据自动转储录入技能

## 功能说明

自动从 PCS 页面抓取表格数据，导出 Excel 后导入到 EBP 系统。

## 安装依赖

```bash
pip install playwright openpyxl
playwright install chromium
```

## 使用方式

```bash
cd ~/.openclaw/skills/pcs-epbp/scripts
python main.py
```

## 工作流程

1. 打开 PCS 页面：http://10.68.160.117:5173/#/vmodelDemo
2. 抓取表格数据
3. 导出为 Excel (pcs_data.xlsx)
4. 打开 EBP 页面：http://10.68.160.117:5173/#/home
5. 自动上传 Excel 并导入

## 定时任务

可配合 cron 实现每日自动执行：

```bash
# 每天上午9点执行
0 9 * * * cd ~/.openclaw/skills/pcs-epbp/scripts && python main.py
```

## 注意事项

- 首次运行需要安装 Playwright 浏览器
- 如页面结构变化，需调整选择器
- EBP 导入按钮选择器可能需要根据实际页面调整
