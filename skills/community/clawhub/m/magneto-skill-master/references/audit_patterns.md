# 安全审计模式与命令

安装外部技能前的强制审计清单。本环境 `skills-security-check` 技能不可用时，改用下方 grep 手动扫描。

## 1. 高危模式扫描命令

在暂存区技能根目录执行（Bash 工具，Git Bash 环境）：

```bash
cd <技能暂存目录>
echo "===== scripts 高危模式 ====="
grep -rniE "os\.system|subprocess|eval\(|exec\(|shutil\.rmtree|os\.remove|os\.unlink|socket\.|requests\.(get|post)|urllib|pickle\.|__import__|input\(|webbrowser|os\.environ|getenv|api_key|secret|token|password|delete|rmtree" scripts/ 2>/dev/null

echo "===== SKILL.md / references 高危模式 ====="
grep -rniE "os\.system|subprocess|eval\(|exec\(|rm -rf|curl |wget |requests\.|urllib|api_key|secret|token|password|rmtree" SKILL.md references/ 2>/dev/null
```

## 2. 风险分级与判定

| 模式 | 风险 | 处理 |
|------|------|------|
| 外发网络到未知地址（`requests.post` 到外部 URL、`socket` -connect 到非本地、`urllib` 拉取远程脚本） | P0 | 强警告，必须用户确认 |
| 删除/移动工作区外文件（`shutil.rmtree` 绝对路径、无提示 `os.remove` 用户目录、`rm -rf ~`） | P0 | 强警告，必须用户确认 |
| 读取/外传凭据（`os.environ` 取 token、`api_key`、`secret`、`password` 并发送） | P0 | 强警告，必须用户确认 |
| `subprocess` / `os.system` 调本地脚本（如 `extract_text.py`） | 视情况 P1/P2 | 确认仅本地调用即可 |
| 交互式 `input()`、双击运行 `install.bat` 全局 pip 安装 | P1 | 告知并改为受管 venv |
| 纯提示词、模板、references 文档 | P2 | 安全，直接继续 |

注意：`token`、`delete` 等词可能是正则分词或"删除我公司…"之类正文，需人工判断是否为真实代码风险。

## 3. 中文乱码修复（Edit 工具偶发损坏）

现象：用 Edit 工具写中文 frontmatter 时，个别汉字被写成 U+FFFD 替换符（如"采购文件"→3 个替换符）。

安装后用 Python 复查并修复：

```python
p = r"<技能目录>/SKILL.md"
s = open(p, encoding="utf-8").read()
print("替换符数量:", s.count("\ufffd"))   # 必须为 0
# 精确修复（按实际损坏字符串调整）：
bad = "采购" + "\ufffd" * 3 + "件"
good = "采购文件"
if bad in s:
    open(p, "w", encoding="utf-8").write(s.replace(bad, good, 1))
```

要点：不要整体重写 frontmatter，只替换损坏片段，避免波及其它内容。
