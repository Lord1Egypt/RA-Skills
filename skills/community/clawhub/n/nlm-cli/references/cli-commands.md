# `notebooklm-mcp-cli` 命令目录

统一命令前缀：

```bash
node {baseDir}/scripts/nlm.mjs
```

本技能面向 **Jacob Brown 的 `notebooklm-mcp-cli`**（`nlm` 命令）。

## Notebooks

```bash
node {baseDir}/scripts/nlm.mjs notebook list
node {baseDir}/scripts/nlm.mjs notebook list --json
node {baseDir}/scripts/nlm.mjs notebook list --quiet
node {baseDir}/scripts/nlm.mjs notebook list --title
node {baseDir}/scripts/nlm.mjs notebook list --full
node {baseDir}/scripts/nlm.mjs notebook create "Title"
node {baseDir}/scripts/nlm.mjs notebook get <id>
node {baseDir}/scripts/nlm.mjs notebook describe <id>
node {baseDir}/scripts/nlm.mjs notebook rename <id> "New Title"
node {baseDir}/scripts/nlm.mjs notebook delete <id> --confirm
node {baseDir}/scripts/nlm.mjs notebook query <id> "question"
```

## Sources

```bash
node {baseDir}/scripts/nlm.mjs source list <notebook>
node {baseDir}/scripts/nlm.mjs source list <notebook> --json
node {baseDir}/scripts/nlm.mjs source list <notebook> --url
node {baseDir}/scripts/nlm.mjs source add <notebook> --url "https://..."
node {baseDir}/scripts/nlm.mjs source add <notebook> --url "https://..." --wait
node {baseDir}/scripts/nlm.mjs source add <notebook> --text "content" --title "Notes"
node {baseDir}/scripts/nlm.mjs source add <notebook> --file document.pdf --wait
node {baseDir}/scripts/nlm.mjs source add <notebook> --youtube "https://..."
node {baseDir}/scripts/nlm.mjs source add <notebook> --drive <doc-id>
node {baseDir}/scripts/nlm.mjs source get <source-id>
node {baseDir}/scripts/nlm.mjs source describe <source-id>
node {baseDir}/scripts/nlm.mjs source stale <notebook>
node {baseDir}/scripts/nlm.mjs source sync <notebook> --confirm
node {baseDir}/scripts/nlm.mjs source delete <source-id> --confirm
```

## Studio 内容生成

优先规则：
- 当目标是**生成演示文稿 / PPT / 幻灯片 / 视频概览**，尤其需要指定语言、视觉风格、叙事风格、受众或内容约束时，优先使用 `notebook query` 触发生成
- `slides create`、`video create` 仍可作为底层回退命令，但不应再作为默认首选路径

推荐示例：

```bash
node {baseDir}/scripts/nlm.mjs notebook query <notebook> "请用中文回答。我希望生成PPT演示文稿，风格要求：使用黏土定格动画风格……"
node {baseDir}/scripts/nlm.mjs notebook query <notebook> "请用中文回答。我希望生成视频概览，风格要求：使用黏土定格动画风格……"
node {baseDir}/scripts/nlm.mjs studio status <notebook>
```

可用 create / revise 命令（回退或补充用）：

```bash
node {baseDir}/scripts/nlm.mjs audio create <notebook> --confirm
node {baseDir}/scripts/nlm.mjs audio create <notebook> --format deep_dive --length long --confirm
node {baseDir}/scripts/nlm.mjs video create <notebook> --confirm
node {baseDir}/scripts/nlm.mjs video create <notebook> --format explainer --style classic --confirm
node {baseDir}/scripts/nlm.mjs report create <notebook> --format "Briefing Doc" --confirm
node {baseDir}/scripts/nlm.mjs quiz create <notebook> --count 10 --difficulty medium --focus "key concepts" --confirm
node {baseDir}/scripts/nlm.mjs flashcards create <notebook> --difficulty hard --focus "definitions" --confirm
node {baseDir}/scripts/nlm.mjs mindmap create <notebook> --confirm
node {baseDir}/scripts/nlm.mjs slides create <notebook> --confirm
node {baseDir}/scripts/nlm.mjs slides revise <artifact-id> --slide '1 Fix title' --confirm
node {baseDir}/scripts/nlm.mjs infographic create <notebook> --orientation landscape --style professional --confirm
node {baseDir}/scripts/nlm.mjs data-table create <notebook> --description "Sales by region" --confirm
node {baseDir}/scripts/nlm.mjs studio status <notebook>
node {baseDir}/scripts/nlm.mjs studio delete <notebook> <artifact-id> --confirm
```

## 下载 / 导出

```bash
node {baseDir}/scripts/nlm.mjs download audio <notebook> <artifact-id> --output podcast.mp3
node {baseDir}/scripts/nlm.mjs download video <notebook> <artifact-id> --output video.mp4
node {baseDir}/scripts/nlm.mjs download report <notebook> <artifact-id> --output report.md
node {baseDir}/scripts/nlm.mjs download mind-map <notebook> <artifact-id> --output mindmap.json
node {baseDir}/scripts/nlm.mjs download slide-deck <notebook> --id <artifact-id> --format pdf --output slides.pdf
node {baseDir}/scripts/nlm.mjs download slide-deck <notebook> --id <artifact-id> --format pptx --output slides.pptx
node {baseDir}/scripts/nlm.mjs download infographic <notebook> <artifact-id> --output infographic.png
node {baseDir}/scripts/nlm.mjs download data-table <notebook> <artifact-id> --output data.csv
node {baseDir}/scripts/nlm.mjs download quiz <notebook> <artifact-id> --format html --output quiz.html
node {baseDir}/scripts/nlm.mjs download flashcards <notebook> <artifact-id> --format markdown --output cards.md
```

## Research

```bash
node {baseDir}/scripts/nlm.mjs research start "query" --notebook-id <id> --mode fast
node {baseDir}/scripts/nlm.mjs research start "query" --notebook-id <id> --mode deep
node {baseDir}/scripts/nlm.mjs research start "query" --notebook-id <id> --source drive
node {baseDir}/scripts/nlm.mjs research status <notebook> --max-wait 300
node {baseDir}/scripts/nlm.mjs research import <notebook> <task-id>
```

## 分享

```bash
node {baseDir}/scripts/nlm.mjs share status <notebook>
node {baseDir}/scripts/nlm.mjs share public <notebook>
node {baseDir}/scripts/nlm.mjs share private <notebook>
node {baseDir}/scripts/nlm.mjs share invite <notebook> email@example.com
node {baseDir}/scripts/nlm.mjs share invite <notebook> email@example.com --role editor
```

## Chat 配置

```bash
node {baseDir}/scripts/nlm.mjs chat configure <notebook> --goal default --length default
node {baseDir}/scripts/nlm.mjs chat configure <notebook> --goal learning_guide --length longer
node {baseDir}/scripts/nlm.mjs chat configure <notebook> --goal custom --prompt "You are an expert..."
```

## Config / aliases / setup / doctor

```bash
node {baseDir}/scripts/nlm.mjs config show
node {baseDir}/scripts/nlm.mjs config get auth.default_profile
node {baseDir}/scripts/nlm.mjs config set auth.default_profile work
node {baseDir}/scripts/nlm.mjs alias set myproject <notebook-id>
node {baseDir}/scripts/nlm.mjs alias list
node {baseDir}/scripts/nlm.mjs alias get myproject
node {baseDir}/scripts/nlm.mjs alias delete myproject
node {baseDir}/scripts/nlm.mjs skill list
node {baseDir}/scripts/nlm.mjs skill install claude-code
node {baseDir}/scripts/nlm.mjs setup add claude-code
node {baseDir}/scripts/nlm.mjs setup list
node {baseDir}/scripts/nlm.mjs doctor
node {baseDir}/scripts/nlm.mjs doctor --verbose
```
