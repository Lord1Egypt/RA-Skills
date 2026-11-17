# hegui-consult 合规咨询 skill · Claude 安装（两步）

## 1. 放置 skill
解压本包，把 `hegui-consult` 整个文件夹放到（任选其一）：
- 个人级（所有项目可用）：`~/.claude/skills/hegui-consult/`
- 项目级（仅当前项目）：`<你的项目>/.claude/skills/hegui-consult/`

放好后目录应是 `…/skills/hegui-consult/SKILL.md`（外层不要再多一层）。

## 2. 连上 hegui MCP（skill 依赖它取数据）
在 `~/.claude.json`（个人级）或项目根 `.mcp.json` 里加：

```json
{
  "mcpServers": {
    "hegui": {
      "type": "http",
      "url": "https://www.dxy-aiagent.com/mcp/hegui/mcp",
      "headers": { "Authorization": "Bearer <你的令牌>" }
    }
  }
}
```

令牌见《董小屿 · MCP 接口接入说明》（mcp-access-guide.txt / hub 页面），可能轮换、以那里为准。

## 3. 生效
重启 / 重连一次 Claude 会话。之后问到上市公司合规、信息披露、任职资格、交易所规则适用等问题，
会自动触发本 skill，按“先查法规→仅披露 required 才查公告”的两段式流程作答。

> 重 consult 可能 30–50 秒，客户端超时请给 ≥90s。
