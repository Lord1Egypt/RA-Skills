# MCP API 参考

## 10 个 MCP Tool 完整参数

### create_session
- 参数: 无
- 返回: session_id（16位十六进制）
- 工作区: uploads/ scan_output/ design_output/ terraform_output/

### upload_file
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| filename | str | 是 | 文件名 |
| content_base64 | str | 是 | base64 编码内容 |

### list_workspace_files
| 参数 | 类型 | 必填 |
|------|------|------|
| session_id | str | 是 |

### download_file
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| file_path | str | 是 | 工作区内相对路径 |

文本文件（.md/.tf/.tfvars/.txt）直接返回内容。
二进制文件（.xlsx）返回格式: `[BASE64:path]\n<base64数据>`

### generate_survey
| 参数 | 类型 | 必填 |
|------|------|------|
| session_id | str | 否 |

输出: uploads/TencentCloud_LZ_Migration_Survey.xlsx

### scan_resources
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| excel_filename | str | 否 | 默认 TencentCloud_LZ_Migration_Survey.xlsx |

前置: Excel 凭据清单 Sheet 已填写
支持: AWS / 阿里云 / GCP / 华为云 / Azure
资源: VPC, Subnet, SecurityGroup, EIP, NAT, CLB, CVM, MySQL, PostgreSQL, Redis, COS, TKE, AutoScaling

### query_tc_specs
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | str | 是 | 如 ap-singapore, ap-jakarta |
| zone | str | 否 | 如 ap-jakarta-1 |
| products | str | 否 | 逗号分隔: zones,cvm,cbs,mysql,postgres,redis,tke,clb,nat,eip,cos |
| session_id | str | 否 | 提供时保存到工作区 |

### generate_design_doc
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| excel_filename | str | 否 | 问卷文件名 |
| resource_md_filename | str | 否 | 扫描结果 MD（默认 resources.md）|
| model | str | 否 | AI 模型（默认 minimax-m2.7:cloud）|

前置: uploads/ 有问卷，scan_output/resources.md 可选
输出:
- design_output/LZ_Design_Doc.md（完整 5 章）
- design_output/LZ_Design_Doc_products/（13 个产品 MD）

### generate_terraform
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| app_name | str | 否 | 应用名（留空自动检测）|
| app_names | str | 否 | 多应用逗号分隔 |
| env | str | 否 | nonprod（默认）/ prod |
| bu | str | 否 | 业务单元 |
| model | str | 否 | AI 模型 |
| git_base_url | str | 否 | 模块 Git 地址 |
| state_region | str | 否 | State Bucket 地域 |
| state_bucket_prefix | str | 否 | Bucket 前缀 |
| state_bucket_suffix | str | 否 | AppID 后缀 |
| state_key_prefix | str | 否 | State Key 前缀 |
| backend_role_name | str | 否 | AssumeRole 名称 |

前置: design_output/LZ_Design_Doc.md + LZ_Design_Doc_products/ 存在
输出: terraform_output/<app>/<app>-tfbaseline/<env>/ + <app>-tfworkload/<env>/

### complete_form
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| session_id | str | 是 | 会话 ID |
| excel_filename | str | 否 | Excel 文件名 |
| model | str | 否 | AI 模型（默认 qwen3.5:397b-cloud）|

前置: Excel 凭据清单至少一行有效 AK/SK
流程: 扫描 → AI 填充 26 题 → 写回 Excel
输出: uploads/FILLED_<原文件名>

## Session 管理

- 自动过期: 24 小时
- 数据路径: workspaces/<session_id>/
- 多客户端隔离
- 可通过 session_id 复用
