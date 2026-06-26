# 生成 Skill 模板

---

```yaml
---
name: {skill-name}
description: {一句话描述：从什么平台获取什么数据}
---
```

# {Skill 中文名}

## ⚡ 执行流程

> **执行顺序**：Step 0（Cookie/登录检查）→ Step 1（确认参数）→ Step 2（执行查询）→ Step 3（展示结果）

> 如果该平台使用 httpOnly session cookie（阶段0 curl 测试失败），需在此说明 API 调用通过 MCP `fetch_api` 完成，Python 脚本仅负责格式化和保存。

---

### Step 0：Cookie/登录检查

**Cookie 够用的平台**（document.cookie 可独立鉴权）：

```bash
if [ -f /tmp/{platform}_cookies.txt ] && [ -s /tmp/{platform}_cookies.txt ]; then echo "EXISTS"; else echo "MISSING"; fi
```
- EXISTS → 跳到 Step 1
- MISSING → 执行 [Cookie 刷新流程](#cookie-刷新流程)

**Cookie 不够的平台**（依赖 httpOnly cookie）：

调用 `mcp__data-saver__get_windows_and_tabs`，查找目标平台标签页。
- 找到 → 提取 URL 中的必要参数，进入 Step 1
- 未找到 → 打开平台页面提示用户登录

---

### Step 1：确认查询参数

为每个用户参数编写确认流程，支持路径分支：

**1.1 确认 {参数1}**

**路径 A：用户已明确指定** → 直接进入下一步

**路径 B：用户未指定，有列表 API**：
```bash
# Cookie 够用时调用脚本
python3 <SKILL_DIR>/scripts/fetch_{name}.py \
  --cookie-file /tmp/{platform}_cookies.txt \
  --list-{param1}
```
```
# Cookie 不够时调用 MCP
mcp__data-saver__fetch_api {
  url: "https://{domain}/{list_api}",
  method: "GET",
  cookieDomain: ".{domain}"
}
```
展示列表后询问用户选择。

**路径 C：无列表 API，需页面提取**：
1. MCP 导航到目标页面
2. `chrome_execute_script` 提取组件状态（React fiber / Vue instance）
3. 展示选项，等待选择

---

**1.N 确认时间范围**

| 用户表达 | 脚本参数 |
|---------|---------|
| 近7天 / 近30天 | `--period 7d` / `--period 30d` |
| 2026年2月 | `--period 2026-02` |
| 自定义日期 | `--start YYYY-MM-DD --end YYYY-MM-DD` |

> 如未提供时间 → 询问用户

---

### Step 2：执行查询

**Cookie 够用时**——一条 bash 命令调脚本：

```bash
python3 <SKILL_DIR>/scripts/fetch_{name}.py \
  --cookie-file /tmp/{platform}_cookies.txt \
  --{param1} "<value1>" \
  --{param2} "<value2>" \
  --period "<period>"
```

**脚本退出码处理**：

| 退出码 | 含义 | 处理方式 |
|-------|------|---------|
| `0` | 成功 | 进入 Step 3 |
| `2` + 确认信息 | 需用户确认 | 解析输出，询问用户，补加参数重跑 |
| `3` + `COOKIE_EXPIRED` | Cookie 失效 | 执行 Cookie 刷新流程，相同命令重跑 |
| 其他非0 | 错误 | 向用户报告错误信息 |

**Cookie 不够时**——MCP 并行调 API：

```
# 并行调用 N 个 fetch_api
mcp__data-saver__fetch_api {
  url: "https://{domain}/{api_path}?{query}",
  method: "POST",
  cookieDomain: ".{domain}",
  headers: {"Content-Type": "application/json"},
  body: "{请求体}"
}
```

响应上传到 OSS 后，curl 下载到临时文件：
```bash
curl -s "<oss_url_1>" -o /tmp/{name}_1.json && \
curl -s "<oss_url_2>" -o /tmp/{name}_2.json
```

然后调格式化脚本：
```bash
python3 <SKILL_DIR>/scripts/format_{name}.py \
  --data1-file /tmp/{name}_1.json \
  --data2-file /tmp/{name}_2.json \
  --{param1} "<value1>" \
  --start <START> --end <END>
```

---

### Step 3：展示结果

> ⚠️ **严禁幻觉**：所有内容必须来自脚本实际终端输出，不得凭记忆或推断补充。
> ⚠️ **严禁截断**：所有数据处理由脚本完成，Claude 只转述输出。

1. ✅ 列出 JSON 文件完整路径（`💾 结果已保存：` 后的路径）
2. 原样转述脚本输出的关键数据
3. 如需进一步分析 → 告知用户可读取 JSON 文件

---

## Cookie 刷新流程

**Cookie 够用的平台**：

R1. `mcp__data-saver__get_windows_and_tabs` 查找目标标签页
R2. `chrome_execute_script`（world: MAIN）执行 `() => document.cookie`
R3. 验证关键 token 是否存在；不存在则提示用户登录后重做 R2
R4. `echo "<cookie>" > /tmp/{platform}_cookies.txt`
R5. 回到 Step 1 或用相同命令重跑脚本

**Cookie 不够的平台**：

R1. `mcp__data-saver__get_windows_and_tabs` 查找目标标签页
R2. 若找不到 → 打开页面，提示用户登录
R3. 确认登录后直接用 MCP `fetch_api` 调 API（无需提取 cookie）

---

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| Cookie 文件不存在/为空 | 执行 Cookie 刷新流程 |
| 脚本退出码 3 | 清理旧 Cookie 文件，刷新后重跑 |
| 脚本退出码 2 | 解析输出的确认信息，询问用户后补加参数重跑 |
| API 鉴权失败 | 提示用户重新登录目标平台 |
| 参数找不到 | 引导用户用 `--list-xxx` 查看可选项 |

---

## 测试验证

### 问答对 1 - {场景描述}
**问题**：{自然语言}
**命令/参数**：{...}

### 问答对 2 - {场景描述}
{...}

### 问答对 3 - {场景描述}
{...}
