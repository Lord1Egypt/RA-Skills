---
name: huaweicloud-python-sdk-helper
description: 华为云 Python SDK 查询工具。自动发现已安装 SDK 的服务包、Client 类、API 方法列表、入参详情、SDK 类完整信息（__init__参数、属性、类型、描述），支持按关键字搜索。快速定位目标 API 的使用方法。
---

# 定位

本技能的核心目标是 **快速查询华为云 Python SDK 的方法与关键字**，帮助开发者在不查阅文档的情况下：

1. 发现某个服务有哪些 Client 类
2. 列出某个 Client 的所有 API 方法
3. 查看方法的入参类型和属性
4. 按关键字搜索匹配的 API

> 安装配置为前置条件，本技能不重点处理安装问题。

## 核心能力

- 🔍 **方法查询**：列出 SDK 包、Client 类、API 方法、入参详情
- 🔎 **关键词搜索**：在方法名和描述中搜索关键字
- 📋 **入参解析**：自动提取 Request 类的属性名、类型和描述
- 🏗️ **类详情查询**：查看 SDK 类（Request/Response）的 __init__ 参数、属性列表、类型定义和中文描述
- 📦 **JSON 输出**：支持结构化输出，便于程序化处理

## 查询工具

### 脚本位置

```
huaweicloud-python-sdk-helper/scripts/query_sdk_methods.py
```

### 功能清单

| 功能 | 命令行参数 | 示例 |
|------|-----------|------|
| 列出所有已安装 SDK 包 | 无参数 | `python query_sdk_methods.py` |
| 列出某服务的 Client 类 | `--service` | `python query_sdk_methods.py --service vpc` |
| 列出 Client 的所有方法 | `--service --client` | `python query_sdk_methods.py --service vpc --client VpcClient` |
| 查询方法入参详情 | `--service --client --method` | `python query_sdk_methods.py --service vpc --client VpcClient --method list_vpcs` |
| 按关键字搜索方法 | `--service --client --search` | `python query_sdk_methods.py --service vpc --client VpcClient --search firewall` |
| 查询 SDK 类详细信息 | `--service --class` | `python query_sdk_methods.py --service iam --v5 --class CreateUserReqBody` |
| 列出全部 SDK 的 Client | `--all-clients` | `python query_sdk_methods.py --all-clients` |
| JSON 格式输出 | `--json` | `python query_sdk_methods.py --service vpc --client VpcClient --json` |

### 工作流程

```
识别服务名 → python query_sdk_methods.py --service <服务> --client <Client> → 
列出方法列表 → --method <方法名> 查入参 → --search <关键字> 搜索 → --class <类名> 查类详情
```

## 使用方法

### 查找服务对应的 SDK 包

先确认服务名与 SDK 包的对应关系：

| 场景关键字 | 服务包 | Client 类 |
|-----------|--------|-----------|
| VPC、虚拟网络、子网 | `huaweicloudsdkvpc` | `VpcClient` |
| ECS、云服务器 | `huaweicloudsdkecs` | `EcsClient` |
| IAM、用户、权限 | `huaweicloudsdkiam` | `IamClient` |
| OBS、对象存储 | `huaweicloudsdkobs` | `ObsClient` |
| Config、合规 | `huaweicloudsdkconfig` | `ConfigClient` |
| LTS、日志 | `huaweicloudsdklts` | `LtsClient` |

如果不确定，运行 `python query_sdk_methods.py` 查看所有已安装的 SDK 包。

### 查询示例

```bash
# 1. 列出现有 Client
python query_sdk_methods.py --service vpc

# 2. 查看 VpcClient 所有方法
python query_sdk_methods.py --service vpc --client VpcClient

# 3. 查看 list_vpcs 方法的入参
python query_sdk_methods.py --service vpc --client VpcClient --method list_vpcs

# 4. 搜索包含 "firewall" 的方法
python query_sdk_methods.py --service vpc --client VpcClient --search firewall

# 5. 查询 Request/Response 类的详细信息（init参数、属性、类型、描述）
python query_sdk_methods.py --service iam --v5 --class CreateUserReqBody
```

### 查询输出示例

#### 示例1：查询方法入参详情

**命令**：`python query_sdk_methods.py --service vpc --client VpcClient --method list_vpcs`

**输出**：
```
================================================================================
方法入参详解: list_vpcs
================================================================================
  描述: 查询VPC列表
  Request 类型: huaweicloudsdkvpc.v3.ListVpcsRequest
  Response 类型: huaweicloudsdkvpc.v3.ListVpcsResponse

  入参列表 (7 个):
  ------------------------------------------------------------
    limit: int
    marker: str
    id: list[str]
    enterprise_project_id: str
    name: list[str]
    description: list[str]
    cidr: list[str]
```

#### 示例2：关键字搜索方法

**命令**：`python query_sdk_methods.py --service vpc --client VpcClient --search firewall`

**输出**：
```
================================================================================
Client: VpcClient
Module: huaweicloudsdkvpc.v3
Total API Methods: 101
================================================================================

搜索关键字: 'firewall' - 找到 18 个匹配

  [1] add_firewall_rules:
      描述: 网络ACL插入规则
      Request: huaweicloudsdkvpc.v3.AddFirewallRulesRequest
      Response: huaweicloudsdkvpc.v3.AddFirewallRulesResponse

  [2] associate_subnet_firewall:
      描述: 网络ACL绑定子网
      Request: huaweicloudsdkvpc.v3.AssociateSubnetFirewallRequest
      Response: huaweicloudsdkvpc.v3.AssociateSubnetFirewallResponse
   ...
```

#### 示例3：查询 SDK 类详细信息

**命令**：`python query_sdk_methods.py --service iam --v5 --class CreateUserReqBody`

**输出**：
```
================================================================================
类详情: CreateUserReqBody
================================================================================
  完整路径: huaweicloudsdkiam.v5.CreateUserReqBody

  __init__ 参数 (3 个):
  ------------------------------------------------------------
    name = None
    description = None
    enabled = None

  属性列表 (3 个):
  ------------------------------------------------------------
    name: str - IAM用户名，长度为1到64个字符，只包含字母、数字、"_"、"-"、"."和空格的字符串，且首位不能为数字。
    description: str - IAM用户描述信息，长度为0到255个字符，不能包含特定字符"@"、"#"、"%"、"&"、"<"、">"、"\\"、"$"、"^"和"*"的字符串。
    enabled: bool - IAM用户是否启用。

  openapi_types (SDK 内部类型定义):
  ------------------------------------------------------------
    name: str
    description: str
    enabled: bool
```

## 安装说明

SDK 安装为前置步骤，确保已安装目标服务的 SDK 包：

```bash
pip install huaweicloudsdk<service> -i https://mirrors.tools.huawei.com/pypi/simple
# 或安装全部：pip install huaweicloudsdkall
```

## 输出说明

### 方法列表输出

每个方法包含以下信息：
- **方法名**：client 上的调用方法
- **描述**：API 的中文说明
- **Request 类型**：入参类的完整模块路径
- **Response 类型**：返回值类的完整模块路径

### 入参详情输出

使用 `--method <方法名>` 可获取方法的入参详情。脚本从 Request 类的 `openapi_types` 中提取：
- **属性名**：入参的属性名称
- **类型**：属性的数据类型（已简化完整类名）
- **描述**：属性的简要说明（如有 setter docstring）

**说明**：
- Request 类型的入参属性可直接通过 `request.<属性名>` 设置
- 若入参类型为嵌套对象（如 `CreateUserOption`），仅显示第一层属性名和类型。如需深入了解嵌套类的入参详情，可通过 Python 代码直接导入并查看 `openapi_types` 属性

### 类详情输出

使用 `--class <类名>` 可获取 SDK 类（如 Request Body、Response 等）的详细信息：
- **完整路径**：类的完整模块路径
- **__init__ 参数**：构造函数的参数列表及默认值，方便快速构建实例
- **属性列表**：所有可设置属性，包含属性名、类型、对应的 JSON 键名及中文描述
- **openapi_types**：SDK 内部的原始类型定义

**说明**：
- 类的属性均可通过 `instance.<属性名>` 直接设置
- 类支持直接通过 `__init__` 传入参数构造，如 `CreateUserReqBody(name="test", enabled=True)`
- 中文描述优先提取自 `__init__` 方法的 docstring 中的 `:param` 标签

## 常见问题排查

### 未找到 SDK 包

运行 `python query_sdk_methods.py` 查看可用的 SDK 包列表，确认服务名拼写。

### 未找到 Client 类

某些服务只有 v2 版本（如 ECS 为 `huaweicloudsdkecs.v2`），脚本会自动检测并回退到可用版本。

### 入参显示 "无法获取"

部分 Request 类的 `openapi_types` 属性可能未定义，此时脚本无法提取详细入参信息，建议查阅 [API Explorer](https://apiexplorer.developer.huaweicloud.com/apiexplorer/overview)。

## 参考资料

| 资源 | 链接 |
|------|------|
| SDK GitHub | https://github.com/huaweicloud/huaweicloud-sdk-python-v3 |
| API Explorer | https://apiexplorer.developer.huaweicloud.com/apiexplorer/overview |
