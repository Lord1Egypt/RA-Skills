---
name: 多账号启动器
slug: multi-account-launcher
version: 1.0.0
description: |
  通过 HTTP API 控制「多账号矩阵管理工具」，实现浏览器账号的启动、关闭和信息查询。
  Python 模式，支持智能匹配、按名称启动。
author: @anonymous
files:
  - matrix_manager.py
  - config.yaml
  - last_result.txt
---

# 多账号启动器

多账号矩阵管理工具的技能，通过 HTTP API 控制账号的启动、关闭和信息查询。

---

## 执行流程（AI 必读）

**Windows 控制台会显示乱码，这是正常的。** 执行后必须读文件获取正确结果。

### 步骤

1. **执行 Python 命令**（替换 `<技能目录>` 为实际路径）：
   ```bash
   python <技能目录>/matrix_manager.py <命令> [参数]
   ```

2. **读取结果文件**：
   ```
   <技能目录>/last_result.txt
   ```
   - 此文件由 `matrix_manager.py` 脚本创建
   - UTF-8 编码，包含正确的中文内容

3. **将结果返回给用户**

**不要**根据控制台输出判断结果。

---

## 命令列表

| 命令 | 说明 | 完整 Python 调用 |
|------|------|------------------|
| `list` | 列出所有账号 | `python matrix_manager.py list` |
| `start <关键词>` | 按名称启动账号 | `python matrix_manager.py start 小红书` |
| `start-index <索引>` | 按索引启动账号 | `python matrix_manager.py start-index 1` |
| `stop <关键词>` | 按名称关闭账号 | `python matrix_manager.py stop 小红书` |
| `stop-index <索引>` | 按索引关闭账号 | `python matrix_manager.py stop-index 1` |

**匹配规则**：`start` 和 `stop` 命令先精准匹配账号名，失败则模糊匹配。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `matrix_manager.py` | 主脚本，执行命令并输出结果 |
| `config.yaml` | 配置文件（API 地址、超时时间） |
| `last_result.txt` | 执行结果输出文件，由 `matrix_manager.py` 创建 |

---

## 前置要求

### 1. Python 环境

需要 Python 3.8+，检测方法：

```bash
python --version
```

如未安装，访问 https://www.python.org/downloads/ 下载安装，**勾选「Add Python to PATH」**。

安装后需安装 `requests` 库：

```bash
pip install requests
```

### 2. 矩阵工具

必须安装「多账号矩阵管理工具」（官网：https://zmt.scys6688.com/）。

开启本地 HTTP 服务：软件设置 → 本地服务器 → 勾选「启动本地服务器」，确认端口为 1008。

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 「python 不是内部或外部命令」 | 未安装 Python 或未添加 PATH | 重装并勾选「Add Python to PATH」 |
| 「No module named 'requests'」 | 未安装 requests | `pip install requests` |
| 「无法连接到多账号矩阵管理工具」 | 软件未启动或本地服务未开启 | 打开软件，开启本地服务器（端口 1008） |
| 返回「无api」 | 编码问题 | 本脚本使用 UTF-8 编码，无需手动处理 |

---

## 索引说明

- **API 返回的下标**：从 0 开始
- **操作使用的索引**：从 1 开始

例如：API 下标 "0" 对应操作索引 "1"。

---

## 配置

`config.yaml` 默认内容：

```yaml
api_url: http://localhost:1008
timeout: 10
```

`api_url` 仅用于连接本地工具，请勿修改为外部地址。
