# gumtree-skills

Gumtree 自动化 Claude Code Skills，通过用户真实浏览器访问 Gumtree。

## 开发命令

```bash
uv sync
uv run python scripts/cli.py --help
```

## 架构

双层结构：`scripts/` 是 Python 自动化引擎，`SKILL.md` 负责技能路由和调用约束。

- `scripts/gumtree/` - 核心浏览器桥接与页面提取逻辑
- `scripts/cli.py` - 统一 CLI 入口，JSON 结构化输出
- `scripts/bridge_server.py` - 本地通信服务
- `extension/` - Chrome 扩展
- `gumtree_skills/cli.py` - 包入口，复用同一套命令实现

### 调用方式

```bash
uv run python scripts/cli.py check-login
uv run python scripts/cli.py login --username "you@example.com" --password "your-password"
uv run python scripts/cli.py logout
uv run python scripts/cli.py search --keyword "iphone"
uv run python scripts/cli.py search --keyword "iphone" --search-location "Sandwell" --sort date --min-price 10 --max-price 10000
uv run python scripts/cli.py home-recommend
uv run python scripts/cli.py detail --url "https://www.gumtree.com/p/..."
uv run python scripts/cli.py post-ad --keyword "iPhone"
uv run python scripts/cli.py post-ad --keyword "iPhone" --category-name "Apple iPhone"
uv run python scripts/cli.py post-ad --keyword "iPhone" --category-index 0
```

- 不要假设当前 shell 的 `python` 就是项目环境；统一通过 `uv run` 调用。
- CLI 会自动检查并拉起 `scripts/bridge_server.py`，并在扩展未连接时尝试打开 Chrome。
- `check-login` 优先使用页面内数据对象判断登录态，DOM 只做兜底。
- `login` 通过页面弹窗执行邮箱密码登录，当前实现依赖 `hm-login`、`email-login` 和邮箱登录表单结构。
- `logout` 通过用户菜单中的 `logout-form` 执行退出。
- `post-ad` 通过 `https://my.gumtree.com/api/category/suggest` 获取建议类目，选中后导航到 `/postad/create?categoryId=<id>`。

## 代码规范

- 行长度上限 100 字符
- JSON 输出使用 `ensure_ascii=False`
- CLI exit code: `0=成功`, `2=错误`
