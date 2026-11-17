---
name: huaweicloud-rds-list
version: 1.0.0
description: |
  查询华为云账号下指定 Region 的关系型数据库服务（RDS）实例列表，输出精简的
  实例名称 + ID + 状态 + 引擎类型 + 规格清单。
  适合用于数据库资源盘点、运维巡检、故障排查与自动化脚本前置查询。
tags:
  - huaweicloud
  - rds
  - 资源查询
  - 云运维
tools:
  - python3
---

# 华为云 RDS 实例列表查询 Skill

## 能力

- 查询华为云账号下指定 Region 的 RDS 实例列表
- 输出精简结果：实例名称（name）、ID（id）、状态（status）、引擎类型（engine）、规格（spec）
- 默认查询北京4（cn-north-4）Region，Region 可在配置中修改
- 认证方式：AK/SK 从配置文件（config.json）读取，支持自动解析 project_id

## 前置条件

1. 本机已安装 Python 3.8+（仅使用标准库，无需安装第三方依赖）
2. 已创建配置文件 `config.json`（在 skill 目录内，已由 .gitignore 排除）：
   - 复制 `config.example.json` 为 `config.json`
   - 填入华为云 AK/SK（密钥不落盘到仓库，仅保存在本地 config.json）

```json
{
  "ak": "你的华为云 Access Key ID",
  "sk": "你的华为云 Secret Access Key",
  "region": "cn-north-4",
  "project_id": ""
}
```

- `region`：可选，默认 `cn-north-4`（北京4）；如需其他 Region 修改此字段
- `project_id`：可选，留空时脚本通过 IAM 接口按 region 自动解析

## 权限说明

本 Skill 仅发起只读查询请求，所需 IAM 权限见 [references/iam-policies.md](references/iam-policies.md)。

## 运行方式

```bash
# 默认读取 skill 目录下 config.json
python3 list_rds.py

# 指定配置文件
python3 list_rds.py -c /path/to/config.json

# 临时覆盖 Region（不改配置文件）
python3 list_rds.py -r cn-south-1
```

## 输出约定

成功时输出 Region 下的 RDS 实例精简列表，字段顺序为 name / id / status / engine / spec：

```
Region cn-north-4 的 RDS 实例列表（共 2 个）：
- name  id  status  engine  spec
- my-rds-01  7b9b0c8a-xxxx-xxxx-xxxx-xxxxxxxxxxxx  ACTIVE  MySQL  rds.mysql.c2.large.4
- my-rds-02  8c0d1e2f-xxxx-xxxx-xxxx-xxxxxxxxxxxx  ACTIVE  PostgreSQL  rds.pg.c2.large.4
```

字段说明：
- `status`：实例状态（ACTIVE/BUILD/FAILED/FROZEN/MODIFYING/REBOOTING 等）
- `engine`：数据库引擎类型（MySQL/PostgreSQL/SQLServer/MariaDB）
- `spec`：规格编码（flavor_ref，如 rds.mysql.c2.large.4）

无实例时输出：`Region cn-north-4 下暂无 RDS 实例。`

## 错误处理

| 场景 | 行为 |
|------|------|
| 配置文件缺失 | 明确提示复制 config.example.json 为 config.json |
| 配置缺少 AK/SK | 明确提示在 config.json 中填写 AK/SK |
| AK/SK 无效或无权限（HTTP 401/403） | 明确提示认证失败并检查配置 |
| 接口/网络异常 | 输出可读的接口错误信息（HTTP 状态码与详情） |
| 无实例 | 返回空提示，不报错 |

脚本以退出码 0（成功/无实例）或 1（配置/认证/接口错误）结束。

## 边界

- 仅支持查询（ListInstances），不支持实例的创建/删除/修改
- 单次仅查询一个 Region
- 凭证只从本地 config.json 读取，绝不写入仓库或日志

## 测试

```bash
python3 -m unittest discover -s tests -v
```
