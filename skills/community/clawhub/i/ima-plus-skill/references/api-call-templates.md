# API 调用模板（跨平台 shell 写法 · 按需查阅）

> 由 SKILL.md 下沉，仅在**无脚本覆盖**的操作（笔记块编辑/移动/导出、自定义查询）时需要。
> 常用操作见 SKILL.md「高频操作快查表」。


> **先看「高频操作快查表」**：常用操作（上传/打包/标签/文件夹/笔记新建追加）已有封装脚本，直接调用脚本即可，无需手写 API。
> 以下模板仅用于**无脚本覆盖的操作**（笔记块编辑/移动/导出、自定义查询等）。

> **跨平台说明**：本 skill 的全部脚本（`.cjs`）为**单一 Node.js 实现**，Windows / Linux / macOS 命令本身完全一致；差异只在 shell 包装（捕获输出、检查退出码）与中文编码处理。**zip 打包为纯 Node 实现**（zlib + 手写 zip 结构），不依赖系统 `zip`/`tar` 命令，Windows 直接可用（含中文文件名 UTF-8）。下面分别给出两平台的规范写法。运行需 **Node 18+**（依赖全局 `fetch` 与 `node:` 前缀模块）。

所有请求统一为 **HTTP POST + JSON Body**，仅发往官方 Base URL `https://ima.qq.com`。

`ima_api` 已抽离到脚本：`./ima_api.cjs`

```bash
# ── Linux / macOS（bash / zsh）── 跨平台通用写法之一
# SKILL_DIR = this skill's root directory
# stdout = normal response JSON; stderr = structured error {"code":-100|-200,"msg":"..."}
resp=$(node "$SKILL_DIR/ima_api.cjs" "openapi/list_docs" '{"limit":10}' 2>&1)
if [ $? -ne 0 ]; then
  # Extract error code & msg using Node (cross-platform, no jq needed)
  err_info=$(node -e "try{const e=JSON.parse(process.argv[1]);process.stdout.write(e.code+':'+e.msg)}catch(_){process.stdout.write('-100:unknown error')}" "$resp")
  err_code="${err_info%%:*}"
  err_msg="${err_info#*:}"

  if [ "$err_code" = "-200" ]; then
    echo "[update] $err_msg" >&2
  else
    echo "[error] $err_msg" >&2
  fi
  exit 1
fi

echo "$resp"
```

> **Windows 版（PowerShell 5.1 / 7+）：**
>
> ```powershell
> # 用 & 调用避免别名/函数冲突；2>&1 合并错误流到 $resp
> $resp = & node "$env:SKILL_DIR/ima_api.cjs" 'openapi/list_docs' '{"limit":10}' 2>&1
> if ($LASTEXITCODE -ne 0) {
>     $err = $resp | ConvertFrom-Json
>     if ($err.code -eq -200) { Write-Host "[update] $($err.msg)" }
>     else { Write-Host "[error] $($err.msg)" }
>     exit 1
> }
> Write-Host $resp
> ```
>
> ⚠️ **PowerShell 5.1 中文乱码必读**：PS 5.1 会静默把请求 Body 转成系统 ANSI（中文 Windows 为 GBK），导致服务端收到乱码。必须改用 UTF-8 字节数组模式发送，详见 `references/platform-notes.md`。PowerShell 7+ 默认 UTF-8，无需额外处理。
>
> **Windows 版（命令提示符 cmd）：**
>
> ```cmd
> chcp 65001 >nul
> node "%SKILL_DIR%\ima_api.cjs" "openapi/list_docs" "{\"limit\":10}" 2>&1
> @REM 成功：stdout 为响应 JSON；失败：进程非 0 退出，错误信息在 stderr
> @REM 用 %ERRORLEVEL% 判断退出码；中文参数需先 chcp 65001 防止乱码
> ```
>
> **cmd 提示**：`SET SKILL_DIR=...` 后，路径用 `%SKILL_DIR%` 引用；Windows 上 `\` 与 `/` 均可作路径分隔符（Node 均接受）。若 `node` 不在 PATH，用完整路径（如 `"C:\Program Files\nodejs\node.exe"`）；脚本内部已用 `process.execPath` 调用 node 子进程，通常无需手动处理。

> **错误处理有两层，必须都检查：**
>
> **第一层 — 脚本执行错误**（进程非 0 退出，错误在 **stderr**）：
>
> - `-100`：程序错误（缺少凭证、参数非法、网络错误等），`msg` 可直接展示给用户
> - `-200`：skill 需要更新，原请求未发送，stdout 中有更新上下文 JSON
>
> **第二层 — 后端业务错误**（进程正常退出，响应在 **stdout**）：
>
> - stdout 返回 JSON `{"code": 0, "msg": "...", "data": {...}}`
> - `code=0` 表示成功，从 `data` 提取业务字段
> - `code≠0` 表示后端业务错误（如参数不合法、权限不足、资源不存在等），**直接将 `msg` 展示给用户**
> - 常见后端错误码见各子模块的「错误处理」章节


