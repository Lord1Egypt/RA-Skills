---
name: hk3-crm-installer
description: 一键安装 HK3 CRM 客户管理系统（Bursa Malaysia 保健品公司专用）
metadata:
  openclaw:
    requires:
      bins: []
      packages:
        - git
        - python3
---

# HK3 CRM 安装器

一键在本地安装并启动 HK3 CRM 客户管理系统。

## 触发词
- "安装 HK3 CRM"
- "下载 HK3 CRM"
- "hk3 crm setup"
- "装 CRM 系统"

## 工作流

1. 运行 `setup.sh` 脚本
2. 从 GitHub clone 代码
3. 安装 Python 依赖（flask, sqlalchemy）
4. 自动启动 CRM 服务（端口 5001）
5. 告知用户打开浏览器：http://127.0.0.1:5001

## 前置依赖

- git
- python3 + pip

## 数据安全

- 客户数据库（hk3_crm.db）在 .gitignore 中
- git pull 更新代码不会影响已有数据
- 数据库自动迁移系统，schema 升级无痛

## 演示数据

```bash
cd hk3-crm && python3 seed_demo.py
python3 seed_demo.py --clean  # 清空
```

## 更多信息

GitHub: https://github.com/jiangyisheng9-bot/hk3-crm
