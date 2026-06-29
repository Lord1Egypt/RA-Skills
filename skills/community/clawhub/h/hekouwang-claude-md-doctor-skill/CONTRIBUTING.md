# 贡献指南 / Contributing

感谢参与 **hekouwang-claude-md-doctor-skill**！欢迎新增检查项、降低误报、为其它语言/框架补启发式规则。

## 硬约束（不可破）

1. **零运行时依赖** —— `check.py` 只用 Python 3 标准库。不要引入第三方包。
2. **只读 + 安全** —— 检查器绝不读取 `.env` / `*.key` / `*.pem` 等密钥文件，不写用户文件。
3. **跨语言通用** —— 不绑定任何具体技术栈；新规则要对多数项目成立。

## 本地开发

```bash
git clone https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill
cd hekouwang-claude-md-doctor-skill

python3 check.py tests/fixtures/good     # 期望 exit 0
python3 check.py tests/fixtures/bad      # 期望 exit 1（有 FAIL 卡关）
python -m py_compile check.py            # 语法自检
```

## 加一条检查项

1. 在 `check.py` 的 `check()` 里用 `add(key, title, status, detail, fix)` 追加结果。
2. `status` 取 `PASS` / `WARN` / `FAIL` / `INFO`（INFO 不计分）。
3. 机检只做"机器能确定的"；需要读正文判断的，写进 `SKILL.md` 的「定性复核」与「机检盲区」。
4. 在 `tests/fixtures/` 增/改夹具，确保 `good` 仍 exit 0、`bad` 仍 exit 1。
5. 误报是头号大忌——宁可 `WARN` 不轻易 `FAIL`，并在 `detail` 里说清线索。

## 提交 PR

- 一个 PR 聚焦一件事；附上前后 `check.py` 输出对比。
- 通过 CI（`.github/workflows/ci.yml`：语法 + good/bad 夹具 + JSON 合法性）。
- commit 信息讲清「改了什么 + 为什么」。

## 范围说明

代码以 MIT 开源（见 [LICENSE](LICENSE)）。品牌名「会勇禾口王的AI笔记」与付费可视化报告卡为增值服务，不在本仓库开源范围内。
