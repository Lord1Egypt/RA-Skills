---
name: huaweicloud-vpc-subnet-list
version: 1.0.0
description: |
  查询华为云指定 Region 下某 VPC 的子网（Subnet）列表，输出精简的子网名称 + ID 清单。
  适合用于网络资源盘点、运维巡检、自动化脚本前置查询（下钻到 VPC 内子网级视图）。
tags:
  - huaweicloud
  - vpc
  - subnet
  - 资源查询
  - 云运维
tools:
  - python3
---

# 华为云 VPC 子网列表查询 Skill

## 能力

- 查询华为云指定 Region 下某 VPC 的子网列表
- 输出精简结果：仅包含子网名称（name）与 ID（id）
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
# 查询指定 VPC 下的子网（默认读取 skill 目录下 config.json）
python3 list_subnets.py -v <vpc_id>

# 指定配置文件
python3 list_subnets.py -v <vpc_id> -c /path/to/config.json

# 临时覆盖 Region（不改配置文件）
python3 list_subnets.py -v <vpc_id> -r cn-south-1
```

## 输出约定

成功时输出某 VPC 下的子网名称 + ID 精简列表：

```
Region cn-north-4 下 VPC 7b9b0c8a-xxxx-xxxx-xxxx-xxxxxxxxxxxx 的子网列表（共 2 个）：
- my-subnet-01  a3c43a27-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- my-subnet-02  b4d54b38-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

无子网时输出：`Region cn-north-4 下 VPC {vpc_id} 暂无子网。`

未指定 VPC ID 时输出用法提示并以退出码 1 结束。

## 错误处理

| 场景 | 行为 |
|------|------|
| 未指定 VPC ID | 提示用法 `python3 list_subnets.py -v <vpc_id> ...` |
| 配置文件缺失 | 明确提示复制 config.example.json 为 config.json |
| 配置缺少 AK/SK | 明确提示在 config.json 中填写 AK/SK |
| AK/SK 无效或无权限（HTTP 401/403） | 明确提示认证失败并检查配置 |
| 接口/网络异常 | 输出可读的接口错误信息（HTTP 状态码与详情） |
| 无子网 | 返回空提示，不报错 |

脚本以退出码 0（成功/无子网）或 1（配置/认证/接口错误/缺参）结束。

## 边界

- 仅支持查询（ListSubnets），不支持子网的创建/删除/修改
- 单次仅查询一个 Region 下单个 VPC 的子网
- 凭证只从本地 config.json 读取，绝不写入仓库或日志

## 测试

```bash
python3 -m unittest discover -s tests -v
```
