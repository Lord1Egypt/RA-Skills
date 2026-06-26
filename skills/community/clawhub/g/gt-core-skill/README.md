# gumtree-skills

Gumtree 自动化 Skills，通过 Chrome 扩展 + Python 引擎，让 AI Agent 以真实用户身份访问 Gumtree。

当前支持十一类能力：

- 检查 Gumtree 当前登录状态
- 通过邮箱和密码登录 Gumtree
- 退出 Gumtree 当前登录状态
- 搜索 Gumtree 列表内容
- 提取 Gumtree 首页推荐内容
- 提取 Gumtree 收藏内容
- 提取 Gumtree 详情页内容
- 收藏 Gumtree 详情页
- 查看 Gumtree 站内交流页
- 从详情页点击 Message 进入站内交流并发送消息
- 发布二手物品（选择类目并跳转到发布详情页）

## 安装

### 前置条件

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) 包管理器
- Google Chrome 浏览器

### 第一步：安装项目

把整个 `gumtree-skills/` 目录放到你的 skills 目录中，或直接在本地仓库中使用。

安装 Python 依赖：

```bash
cd gumtree-skills
uv sync
```

### 第二步：安装浏览器扩展

1. 打开 Chrome，地址栏输入 `chrome://extensions/`
2. 右上角开启开发者模式
3. 点击加载已解压的扩展程序，选择本项目的 `extension/` 目录
4. 确认扩展 `Gumtree Bridge` 已启用

## 使用方式

### 作为 AI Agent 技能使用

安装到 skills 目录后，直接用自然语言与 Agent 对话即可。

示例：

> "在 Gumtree 搜索 iphone"

> "帮我看看 Gumtree 首页推荐"

> "抓一下这个 Gumtree 帖子详情"

> "检查一下我现在在 Gumtree 是不是登录状态"

### 作为 CLI 工具使用

所有功能也可以通过命令行直接调用，输出 JSON 格式。

```bash
# 检查当前登录状态
uv run python scripts/cli.py check-login

# 邮箱密码登录
uv run python scripts/cli.py login --username "you@example.com" --password "your-password"

# 退出当前登录状态
uv run python scripts/cli.py logout

# 搜索列表
uv run python scripts/cli.py search --keyword "iphone" --limit 10

# 带排序和筛选
uv run python scripts/cli.py search \
  --keyword "iphone" \
  --search-location "Sandwell" \
  --search-category "iphone" \
  --distance 3 \
  --sort date \
  --min-price 10 \
  --max-price 10000 \
  --condition as_good_as_new \
  --condition good \
  --seller-type trade \
  --seller-type private

# 首页推荐
uv run python scripts/cli.py home-recommend --limit 10

# 收藏列表
uv run python scripts/cli.py favourites --limit 10

# 详情页
uv run python scripts/cli.py detail --url "https://www.gumtree.com/p/..."

# 收藏详情页
uv run python scripts/cli.py detail-favourite --url "https://www.gumtree.com/p/..."

# 站内交流页
uv run python scripts/cli.py messages

# 指定会话并发送消息
uv run python scripts/cli.py messages --conversation-id "d842668c-0c94-3088-b19f-5f25bc423b17" --message "Hi, is this still available?"

# 从详情页点击 Message 并发送消息
uv run python scripts/cli.py detail-message --url "https://www.gumtree.com/p/..." --message "Hi, is this still available?"

# 发布二手物品 —— 查看建议类目
uv run python scripts/cli.py post-ad --keyword "iPhone"

# 发布二手物品 —— 按类目名称选择并跳转
uv run python scripts/cli.py post-ad --keyword "iPhone" --category-name "Apple iPhone"

# 发布二手物品 —— 按索引选择并跳转（选第一个建议类目）
uv run python scripts/cli.py post-ad --keyword "iPhone" --category-index 0
```

> 不要直接使用系统 `python` 或当前 shell 的 `conda` 环境运行脚本；推荐始终通过 `uv run` 启动。

> CLI 会自动检查并启动本地 bridge server；如果扩展未连接，会尝试打开 Chrome 并等待 `Gumtree Bridge` 扩展连接。首次使用前仍需要先在 Chrome 中加载扩展。

如果你希望使用安装后的命令入口，也可以运行：

```bash
uv run gumtree-skills check-login
uv run gumtree-skills login --username "you@example.com" --password "your-password"
uv run gumtree-skills logout
uv run gumtree-skills search --keyword "iphone" --limit 10
uv run gumtree-skills home-recommend --limit 10
uv run gumtree-skills favourites --limit 10
uv run gumtree-skills detail --url "https://www.gumtree.com/p/..."
uv run gumtree-skills detail-favourite --url "https://www.gumtree.com/p/..."
uv run gumtree-skills messages
uv run gumtree-skills messages --conversation-id "d842668c-0c94-3088-b19f-5f25bc423b17" --message "Hi, is this still available?"
uv run gumtree-skills detail-message --url "https://www.gumtree.com/p/..." --message "Hi, is this still available?"
uv run gumtree-skills post-ad --keyword "iPhone"
uv run gumtree-skills post-ad --keyword "iPhone" --category-name "Apple iPhone"
uv run gumtree-skills post-ad --keyword "iPhone" --category-index 0
```

如果看到 `No module named 'websockets'`，通常说明当前命令不是通过 `uv run` 启动，或还没有在项目目录执行 `uv sync`。

搜索参数说明：

- `--sort` 支持 `relevance`、`date`、`price_lowest_first`、`price_highest_first`、`distance`。
- `--condition` 支持 `as_good_as_new`、`good`、`new`、`fair`，可重复传入。
- `--seller-type` 支持 `trade`、`private`，可重复传入。
- 价格、距离和类别筛选分别使用 `--min-price`、`--max-price`、`--distance`、`--search-category`。

登录态检查说明：

- `check-login` 优先使用页面内埋点对象判断登录态，包括 `window.__GUMTREE_ANALYTICS_CONFIG__`、`initialDataLayer.u.li`、`window.gumtreeDataLayer[0].user.loggedInStatus`、`legacy.loggedIn` 和 `window.clientData.userData`。
- DOM 中的 `Manage my Ads`、`My Orders`、`Favourites`、`My Alerts`、`My Details` 与 `Login`、`Sign up` 只作为辅助兜底信号。
- 输出会返回 `logged_in`；如果已登录，还会返回 `account` 和 `menu_links`。

登录说明：

- `login` 会自动打开 Gumtree 登录弹窗，切换到 `Continue with email`，填入邮箱和密码后提交。
- 当前命令参数会直接出现在 shell 历史里；如果是共享机器，建议用临时终端会话执行。
- `logout` 会自动展开用户菜单并提交 `logout-form`。

收藏页说明：

- `favourites` 会打开 `https://www.gumtree.com/my-account/favourites`，优先从 `window.clientData.favouriteAds.adverts` 提取收藏列表。
- 输出包含收藏总数、用户信息，以及每条收藏的标题、价格、位置、链接、图片、发布时间和商品属性。
- 如果当前未登录，Gumtree 可能会重定向到登录流程，此时命令会返回提取失败或空结果。

详情页收藏说明：

- `detail-favourite` 会打开指定详情页，定位详情区域的 `Favourite` 按钮并执行点击。
- 当前实现会先检查登录状态，再综合 `window.clientData.sellerActions.savedAds`、按钮 `is-saved` class、`data-q=full-heart`/`filled-heart` 和粉色心形图标状态判断点击前后收藏是否成功。
- 如果帖子已收藏，会返回 `already_favourited: true`；如果刚刚收藏成功，会返回 `just_favourited: true`。

站内交流说明：

- `messages` 会打开 `https://www.gumtree.com/manage/messages`，提取左侧会话列表、当前会话信息，以及当前会话中的消息文本和时间。
- 传 `--conversation-id` 时，会直接打开指定会话；传 `--message` 时，会在当前会话填写并发送消息。
- `detail-message` 会先打开详情页，点击卖家联系区域的 `Message` 按钮，等待进入站内交流页后再提取会话或发送消息。
- 这两个命令都需要用户已登录 Gumtree。

发布物品说明：

- `post-ad` 通过调用 Gumtree 类目建议 API（`https://my.gumtree.com/api/category/suggest?input=<keyword>`）获取建议类目。
- 仅传 `--keyword` 时，返回所有建议类目供用户选择；传 `--category-name` 或 `--category-index` 可自动选择类目并跳转到发布详情页（`/postad/create?categoryId=<id>`）。
- 需要用户已登录 Gumtree。

## 退出码

- `0` 成功
- `2` 错误

## 项目结构

```text
gumtree-skills/
├── extension/
│   ├── manifest.json
│   ├── background.js
│   └── content.js
├── gumtree_skills/
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py
├── scripts/
│   ├── bridge_server.py
│   ├── cli.py
│   └── gumtree/
│       ├── __init__.py
│       ├── bridge.py
│       ├── browser_detail.py
│       ├── browser_detail_favourite.py
│       ├── browser_favourites.py
│       ├── browser_home.py
│       ├── browser_messages.py
│       ├── browser_post_ad.py
│       ├── browser_search.py
│       ├── browser_urls.py
│       ├── errors.py
│       └── selectors.py
├── SKILL.md
├── CLAUDE.md
├── README.md
├── pyproject.toml
└── uv.lock
```

## 已知限制

- 当前不支持收藏同步、增删收藏或官方 API 模式；发布功能仅完成到类目选择和跳转，后续填写表单待实现
- 搜索、首页、收藏和详情页都依赖真实浏览器环境，不是纯 HTTP 抓取
- 主数据优先取结构化数据和页面内嵌数据，页面改版后可能需要更新脚本
