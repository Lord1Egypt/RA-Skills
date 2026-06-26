# govb-fetcher

地方政府采购商机抓取工具，openClaw CLI skill 插件。

## 安装

```bash
uv pip install -e .
```

## 常用命令

```bash
govb-fetcher --today                    # 抓取今日，含详情补全
govb-fetcher --today --no-detail        # 快速预览，只调列表接口
govb-fetcher --date 2026-03-28          # 指定日期
govb-fetcher --set-cookie --source bjzc \
  --bearer "Bearer xxx" \
  --session "YGCG_TBSESSION=xxx; JSESSIONID=xxx; jcloud_alb_route=xxx"
```

## 项目结构

```
govb_fetcher/
├── config.py     # 配置加载（.env 优先级、关键词、凭证读取）
└── fetcher.py    # 核心逻辑（抓取、过滤、详情补全、Excel 输出、CLI）
SKILL.md          # openClaw skill 定义（触发词、用法说明）
.env.example      # 配置模板
```

## 数据源

### 北京中建云智（bjzc）
- 列表接口：`POST /gt-jy-toubiao/api/cggg/gonggao/queryZBGongGaoList.do`
- 详情接口①：`GET /cggg/gonggao/queryGgBdList.do?ggGuid=xxx`（分包+时间）
- 详情接口②：`GET /cggg/gonggao/queryPurchaserInfo.do?gcGuid=xxx`（采购人+代理机构）
- **需要 Cookie + Bearer**，凭证通过 `--set-cookie` 写入 `~/.config/govb-fetcher/.env`
- 每次请求后服务器下发的新 `YGCG_TBSESSION` 自动写回 `.env`

### 湖南政府采购网（hnzc）
- 列表接口：`POST http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do`
- 详情接口：`GET /mvc/viewNoticeContent.do?noticeId=xxx`（返回 HTML，regex 解析）
- **免认证**，无需配置凭证

## 过滤体系

```
列表全量抓取
    ↓
排除关键词过滤（FETCHER_EXCLUDE_KEYWORDS）→ 丢弃
    ↓
核心关键词过滤（FETCHER_KEYWORDS）→ 不命中则丢弃
    ↓
仅对命中记录调详情接口（--no-detail 跳过此步）
    ↓
推荐评级 + 备注生成 → Excel
```

## 配置系统

变量命名规范：`FETCHER_{SOURCE}_{PARAM}`

- 通用参数：`FETCHER_KEYWORDS` / `FETCHER_EXCLUDE_KEYWORDS` / `FETCHER_HIGH_VALUE_KEYWORDS` / `FETCHER_OUTPUT_DIR`
- 代理：`FETCHER_USE_PROXY`（`true`/`false`，默认 `false`）/ `FETCHER_PROXY`（格式 `http://user:pass@host:port`）
- 北京政采凭证：`FETCHER_BJZC_BEARER_TOKEN` / `FETCHER_BJZC_TBSESSION` / `FETCHER_BJZC_JSESSIONID` / `FETCHER_BJZC_ALB_ROUTE`

优先级（高→低）：环境变量 > 当前目录 `.env` > `~/.config/govb-fetcher/.env` > 硬编码默认值（仅关键词）

## 新增数据源步骤

1. **`fetcher.py`**：新增 `_build_{src}_session()`、`_fetch_{src}_page()`、`_fetch_{src}_detail()`、`fetch_{src}_bidding()` 四个函数
2. **`fetch_all_bidding()`**：追加调用并加入返回 dict（key = Sheet 名）
3. **`SOURCE_COOKIE_MAP`**：若需认证，在注册表中添加一条（key = `--source` 标识）
4. **`config.py`**：新增 `get_{src}_xxx()` 凭证读取函数（若需认证）
5. **`.env.example`**：补充凭证变量示例

## Excel 输出

- 文件名：`政府采购商机汇总_{日期}.xlsx`
- 每个数据源一个 Sheet
- `--no-detail` 模式：自动去掉全为空的列，保持表格整洁
- 推荐等级高（黄色）/中（蓝色）行着色
