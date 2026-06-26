# jwgl-query

面向教师侧教务系统（JWGL）的查询 skill。

## 功能

- 查本周课表
- 查考试相关信息（监考安排、课程考试安排、考试信息，支持聚合查询）
- 管理多位老师账号与学校 URL

## 初始化

可手动初始化：

```bash
bash scripts/setup.sh
```

也可以直接运行查询脚本；首次运行时会自动完成初始化：

```bash
bash scripts/run.sh --config config.json --teacher "某老师" --query-type course_schedule --headless
```

初始化会自动：

- 创建 `.venv`
- 安装依赖
- 在缺少 `config.json` 时从 `config.example.json` 复制一份
- 运行环境检查

## 配置学校与账号

`config.json` 不应提交到 Git。

用户首次使用时，由 agent 通过自然语言收集：

- 学校名称
- 学校教务系统 URL
- 老师姓名
- 登录账号
- 登录密码

如果用户没提供登录页 URL，默认按 `{学校 URL}/jsxsd/framework/jsMain.jsp` 生成。

然后调用底层脚本写入本地 `config.json`。

## 常用脚本

```bash
bash scripts/setup.sh
bash scripts/run.sh --config config.json --teacher "某老师" --query-type course_schedule --headless
python3 scripts/manage_accounts.py --config config.json list
python3 scripts/manage_accounts.py --config config.json school-list
python3 scripts/manage_accounts.py --config config.json add --teacher "某老师" --username "账号" --password "密码" --set-current
python3 scripts/manage_accounts.py --config config.json school-add --school "某学校" --base-url "https://jwgl.example.edu.cn" --set-current
```

兼容旧写法：

- 学校名：`--school` / `--name`
- 老师名：`--teacher` / `--name`
- 登录账号：`--username` / `--user` / `--account`
- 登录密码：`--password` / `--pass`

## 说明

- 主交互入口是自然语言，不是 CLI
- 如果还没有保存学校 URL，agent 应先追问学校教务系统 URL，再继续录入老师账号或执行查询
- 调 shell 脚本时优先使用 `bash scripts/...`，不要假设安装后的 skill 目录保留了可执行位
- `tools/` 下脚本仅用于诊断
- `out/` 为调试输出目录，不应提交到仓库
