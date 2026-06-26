# GI-ValueSider Superinvestor Data (Gravitech Innovations)

动态采集 [ValueSider](https://valuesider.com) 上 Superinvestors 的 13F 持仓与买卖活动，供 OpenClaw 调用。Gravitech Innovations 出品。

## 安装依赖

```bash
cd gi-valuesider-superinvestor-data
pip install -r requirements.txt
```

## 运行与测试

### 方式一：本地快速测试（不联网）

用自带的 sample 数据跑解析器，确认脚本正常：

```bash
cd gi-valuesider-superinvestor-data
bash scripts/run_test.sh
```

会输出解析后的 JSON（持仓 summary + 2 条 holdings，活动 3 条 activities），最后看到 `=== 测试通过：解析器工作正常 ===` 即表示解析流程 OK。

### 方式二：在 Cursor 里完整测试（实时抓网页）

1. 在 Cursor 中打开本项目（或至少让 Agent 能读到本 skill 的 `SKILL.md` 和 `scripts/`）。
2. 在对话里直接问，例如：
   - 「查一下 Mason Hawkins / Longleaf Partners 的持仓和最近买卖」
   - 「从 ValueSider 抓 Mason Hawkins 的 13F 持仓」
3. Agent 会按 SKILL 的流程：用 web_fetch 抓 portfolio 和 portfolio-activity 两个 URL → 把内容交给解析脚本 → 用得到的 JSON 汇总回答你。

无需你手动执行脚本，只要问题里包含「持仓 / 13F / ValueSider / 某基金经理」等关键词，Agent 会触发该 skill 并走完整个流程。

### 方式三：自己手动跑一遍实时流程

想自己体验「抓网页 → 解析」的每一步时：

1. **抓页面**（二选一）  
   - 在 Cursor 对话里让 Agent 用 web_fetch 抓下面两个 URL，把返回的**全文**保存成两个文件，例如 `portfolio.txt`、`activity.txt`；或  
   - 浏览器打开这两个链接，复制页面主要表格/文字内容到两个文件。
2. **解析**（在 skill 目录下执行）：

```bash
cd gi-valuesider-superinvestor-data
export GURU=mason-hawkins-longleaf-partners   # 或其他 slug

python scripts/parse_fetched_content.py --type portfolio --file portfolio.txt --guru-slug "$GURU" --source-url "https://valuesider.com/guru/$GURU/portfolio"
python scripts/parse_fetched_content.py --type activity --file activity.txt --guru-slug "$GURU" --source-url "https://valuesider.com/guru/$GURU/portfolio-activity"
```

输出即为该基金经理的持仓与交易 JSON，可再自己做展示或分析。

---

## 使用（实时爬取流程）

1. **获取页面**：用 MCP web_fetch 请求  
   - `https://valuesider.com/guru/{guru_slug}/portfolio`  
   - `https://valuesider.com/guru/{guru_slug}/portfolio-activity`
2. **解析为 JSON**：将返回内容保存为文件后执行  
   - `python scripts/parse_fetched_content.py --type portfolio --file <文件> --guru-slug <slug>`  
   - `python scripts/parse_fetched_content.py --type activity --file <文件> --guru-slug <slug>`
3. 用解析得到的 JSON 做汇总或展示。

若直接请求可用（无 403），也可用 `python scripts/fetch_valuesider.py <guru_slug>` 一次拉取。详见 [SKILL.md](SKILL.md)。

## 发布到 ClawHub

1. 安装 CLI：`npm i -g clawhub`
2. 登录：`clawhub login`（需 GitHub 账号，且账号至少一周历史）
3. 在仓库根目录执行发布：

```bash
clawhub publish ./gi-valuesider-superinvestor-data --slug gi-valuesider-superinvestor-data --name "GI ValueSider Superinvestor Data" --version 1.0.0 --tags latest
```

或从本 skill 目录：

```bash
cd gi-valuesider-superinvestor-data
clawhub publish . --slug gi-valuesider-superinvestor-data --name "GI ValueSider Superinvestor Data" --version 1.0.0 --tags latest
```

其他人可通过 `clawhub install gi-valuesider-superinvestor-data` 安装。
