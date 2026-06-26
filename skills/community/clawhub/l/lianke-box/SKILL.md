---
name: lianke-print-box
description: "链科云打印盒 - 通过 lk-print CLI 远程打印和扫描。当用户需要打印文件、查询打印机状态、提交打印任务、扫描文档时使用此 Skill。NOT for: 本地打印机直接操作、非链科设备。"
metadata: {"openclaw":{"emoji":"🖨️","requires":{"bins":["lk-print"]},"install":[{"id":"uv","kind":"uv","package":"git+https://github.com/liankenet/lk-print-box.git","bins":["lk-print"],"label":"Install lk-print (uv)"}]}}
---

# 链科云打印盒 Skill

通过 `lk-print` CLI 操作链科云打印盒，远程控制打印机和扫描仪。

## When to Use

✅ **USE this skill when:**

- 用户要打印文件（PDF、图片、Office文档）
- 查询打印机状态或打印任务状态
- 扫描文档
- 管理云打印盒设备

## When NOT to Use

❌ **DON'T use this skill when:**

- 操作本地直连打印机（非云打印盒）
- 非链科设备

## Setup

```bash
# 全局安装（注册 lk-print 到 PATH）
uv tool install git+https://github.com/liankenet/lk-print-box.git

# 一次性认证
lk-print auth --api-key <YOUR_API_KEY> --device-id <YOUR_DEVICE_ID> --device-key <YOUR_DEVICE_KEY>

# 验证
lk-print auth --status
```

> 凭据获取：ApiKey 从 https://open.liankenet.com 注册，DeviceId/DeviceKey 扫描设备二维码获取

## 打印流程

### 1. 确认设备在线

```bash
lk-print device
# 检查 data.info.online: 1=在线, 0=离线, null=从未开机
```

### 2. 获取打印机列表

```bash
# USB 打印机（推荐）
lk-print printers

# 全部打印机(含网络)
lk-print printers --type 3

# JSON 格式
lk-print printers --json
```

从输出中获取 `hash_id`（后续命令需要）。

### 3. 获取打印机参数（可选，用于了解打印机能力）

```bash
lk-print printer-params <hash_id>
# 返回支持的纸张、颜色、双面等能力
```

### 4. 提交打印任务

```bash
# 打印本地文件（默认 A4 黑白）
lk-print print /path/to/file.pdf

# 打印 URL 文件
lk-print print https://example.com/doc.pdf

# 指定参数
lk-print print file.pdf --paper-size 9 --color 2 --copies 3

# 双面打印
lk-print print file.pdf --duplex 2

# 横向打印
lk-print print file.pdf --orientation 2

# 指定页数范围
lk-print print file.pdf --page-range "1,3,5-10"

# 指定打印机
lk-print print file.pdf --printer <hash_id>
```

### 5. 查询任务状态

```bash
lk-print job-status <task_id>
# task_state: READY=排队, PARSING=解析, SENDING=发送, SUCCESS=完成, FAILURE=失败
```

### 取消打印

```bash
lk-print cancel-job <task_id>
```

## 扫描流程

```bash
# 1. 列出扫描仪
lk-print scanners

# 2. 查看扫描参数
lk-print scanner-params <scanner_id>

# 3. 创建扫描任务
lk-print scan <scanner_id>
lk-print scan <scanner_id> --color-mode RGB24 --format PDF --size A4

# 4. 查询扫描结果
lk-print scan-status <task_id>

# 5. 删除扫描任务
lk-print scan-delete <task_id>
```

## 参数速查

### 纸张 (--paper-size)

| 值 | 纸张 | 值 | 纸张 |
|----|------|----|------|
| 9 | **A4** | 11 | A5 |
| 70 | A6 | 1 | Letter |
| 5 | Legal | 13 | B5 |

### 缩放 (--scale)

| 值 | 说明 |
|----|------|
| `fit` | **自适应（默认）** |
| `fitw` | 宽度优先 |
| `fith` | 高度优先 |
| `fill` | 拉伸全图 |
| `cover` | 裁剪铺满 |
| `none` | 原始大小 |
| `90%` | 自定义百分比 |

## Notes

- 打印任务是**异步的**，`print` 命令返回 `task_id`，需用 `job-status` 查询结果
- 查询状态建议间隔 **10秒** 轮询
- 未指定打印机时默认使用第一台 USB 打印机
- JSON 格式输出便于程序解析（`--json`）
