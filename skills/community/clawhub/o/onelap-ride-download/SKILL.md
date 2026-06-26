---
name: onelap-ride-download
description: 从顽鹿竞技 (Onelap) 下载骑行记录 FIT 文件。用于批量导出用户的骑行数据。
metadata:
  openclaw:
    emoji: 🚴
    requires:
      bins: [curl]
      browser: true
---

# Onelap 骑行数据下载 Skill

从顽鹿竞技 (Onelap) 平台下载用户的骑行记录 FIT 文件。

## 使用场景

✅ **适用场景：**
- 备份骑行数据
- 导出数据到第三方平台（Strava、Garmin Connect 等）
- 本地分析骑行数据
- 批量导出指定时间段的骑行记录
- **按指定日期范围下载**（如"下载 3 月 16 号到 19 号的文件"）

❌ **不适用：**
- 实时骑行数据（需要骑行结束后才有记录）
- 非 FIT 格式需求（可后续转换）

## 前置条件

1. 用户已登录顽鹿竞技账号
2. 浏览器已打开并保持在登录状态
3. 知道用户的骑行记录页面 URL

## 操作步骤

### 1. 访问骑行记录页面

```bash
# 导航到分析页面
browser navigate https://u.onelap.cn/analysis
```

### 2. 获取页面内容

```bash
# 获取页面快照，找到 FIT 文件下载链接
browser snapshot --refs aria --depth 5
```

### 3. 解析下载链接

从页面中找到类似这样的 FIT 文件链接：
```
http://fits.rfsvr.net/MAGENE_C416_2026-03-19-09-34-33_1078400_1773886046761.fit?e=1773892823&token=xxx
```

### 4. 批量下载

```bash
# 创建保存目录
mkdir -p /home/ckboss/Downloads/onelap-rides-YYYYMMDD

# 下载单个文件
curl -s -o "2026-03-19_09-34.fit" "http://fits.rfsvr.net/xxx.fit?token=xxx"

# 批量下载示例（按日期范围）
cd /home/ckboss/Downloads/onelap-rides-0316-0319
curl -s -o "2026-03-16_09-24.fit" "URL_1" && echo "✓ 3/16 早"
curl -s -o "2026-03-16_21-37.fit" "URL_2" && echo "✓ 3/16 晚"
# ... 继续下载其他文件
```

### 5. 验证下载

```bash
# 检查下载的文件
ls -lh /home/ckboss/Downloads/onelap-rides-*/
```

## 快速命令模板

### 下载指定日期范围的骑行记录

```bash
# 用户指令示例：
# "下载 3 月 16 号到 19 号的骑行文件"
# "下载 2026-03-16 到 2026-03-19 的 fit 文件"
# "下载本周的骑行数据"

# 1. 解析用户指定的日期范围
# 格式支持：
#   - "3 月 16 号到 19 号" → 2026-03-16 ~ 2026-03-19
#   - "2026-03-16 到 2026-03-19"
#   - "本周" → 本周一到今日
#   - "上周" → 上周一到上周日

# 2. 创建工作目录
mkdir -p /home/ckboss/.openclaw/workspace/onelap-rides

# 3. 访问页面获取链接
browser navigate https://u.onelap.cn/analysis
browser snapshot --refs aria --depth 5

# 4. 从页面中筛选指定日期范围的 FIT 链接
# 页面数据结构示例：
#   - generic [ref=e26]: 2026-03-19 09:34
#   - link [ref=e32]: http://fits.rfsvr.net/xxx.fit?token=xxx

# 5. 批量下载（按日期范围过滤）
cd /home/ckboss/.openclaw/workspace/onelap-rides

# 示例：下载 3 月 16 日 -19 日 的文件
curl -s -o "2026-03-16_09-24.fit" "URL_1" && echo "✓ 3/16 早"
curl -s -o "2026-03-16_21-37.fit" "URL_2" && echo "✓ 3/16 晚"
curl -s -o "2026-03-17_09-28.fit" "URL_3" && echo "✓ 3/17 早"
# ... 继续下载范围内的其他文件

# 6. 复制到下载目录（以日期范围命名）
mkdir -p /home/ckboss/Downloads/onelap-rides-0316-0319
cp 2026-03-1{6,7,8,9}_*.fit /home/ckboss/Downloads/onelap-rides-0316-0319/
```

### 下载最近 7 天的骑行记录

```bash
# 1. 创建工作目录
mkdir -p /home/ckboss/.openclaw/workspace/onelap-rides

# 2. 访问页面获取链接
browser navigate https://u.onelap.cn/analysis
browser snapshot --refs aria --depth 5

# 3. 批量下载（替换为实际链接）
cd /home/ckboss/.openclaw/workspace/onelap-rides
curl -s -o "DATE_TIME.fit" "FIT_URL" && echo "✓ 下载完成"

# 4. 复制到下载目录
mkdir -p /home/ckboss/Downloads/onelap-rides-$(date +%m%d)
cp *.fit /home/ckboss/Downloads/onelap-rides-$(date +%m%d)/
```

## 注意事项

⚠️ **链接有效期：** FIT 文件下载链接有时效性（通常几小时），需尽快下载

⚠️ **登录状态：** 确保浏览器保持登录状态，否则无法获取有效链接

⚠️ **批量下载：** 建议分批下载，避免请求过于频繁

⚠️ **文件命名：** 建议按 `日期_时间.fit` 格式命名，便于管理

⚠️ **日期范围解析：** 
- 中文格式："3 月 16 号到 19 号" → `2026-03-16` ~ `2026-03-19`
- ISO 格式："2026-03-16 到 2026-03-19"
- 相对日期："本周"、"上周"、"最近 7 天"

## 数据用途

下载的 FIT 文件可以：
- 导入到 **Garmin Connect**、**Strava**、**TrainingPeaks** 等平台
- 使用 **GoldenCheetah**、**WKO5** 等软件分析
- 使用在线工具转换为 **TCX**、**GPX** 格式
- 本地备份和统计分析

## 相关文件

- 工作目录：`/home/ckboss/.openclaw/workspace/onelap-rides/`
- 输出目录：`/home/ckboss/Downloads/onelap-rides-*/`

## 用户指令示例

```
# 指定日期范围
"下载 3 月 16 号到 19 号的骑行文件"
"下载 2026-03-16 到 2026-03-19 的 fit 文件"
"下载 3 月 16 日到 3 月 19 日的所有骑行记录"

# 相对日期
"下载本周的骑行数据"
"下载上周的骑行记录"
"下载最近 7 天的骑行文件"

# 单日下载
"下载今天早上的骑行文件"
"下载 3 月 18 号的骑行数据"
```

## 输出示例

用户指令：`"下载 3 月 16 号到 19 号的骑行文件"`

预期输出：
```
✅ 完成！已下载 3 月 16 日 -19 日 的骑行记录

📁 文件位置：/home/ckboss/Downloads/onelap-rides-0316-0319/

📊 共 7 个文件：
| 日期 | 时间 | 文件 |
|------|------|------|
| 3/16 | 09:24 | 2026-03-16_09-24.fit |
| 3/16 | 21:37 | 2026-03-16_21-37.fit |
| 3/17 | 09:28 | 2026-03-17_09-28.fit |
| 3/17 | 20:48 | 2026-03-17_20-48.fit |
| 3/18 | 09:35 | 2026-03-18_09-35.fit |
| 3/18 | 21:27 | 2026-03-18_21-27.fit |
| 3/19 | 09:34 | 2026-03-19_09-34.fit |

总计：332KB，7 次骑行 🚴‍♂️
```

---

_最后更新：2026-03-19_
