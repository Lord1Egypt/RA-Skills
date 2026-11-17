# 搜索策略指南

## 四源搜索命令参考

```bash
# 全源搜索（推荐默认）
python3 ./scripts/search.py "关键词"

# 指定单源
python3 scripts/search.py "关键词" --source github
python3 scripts/search.py "关键词" --source clawhub
python3 scripts/search.py "关键词" --source skillhub
python3 scripts/search.py "关键词" --source skillssh

# 高级筛选（GitHub）
python3 scripts/search.py "关键词" --language python --min-stars 500 --updated-within 90

# JSON 输出（程序处理用）
python3 scripts/search.py "关键词" --json
```

## 关键词优化技巧

**按需求而非名称搜索：**
- 用户说"PDF表单填写" → 搜 `pdf form fill`
- 用户说"自动发邮件" → 搜 `email automation send`
- 用户说"分析Excel数据" → 搜 `excel data analysis`

**英文关键词效果更好**（GitHub/ClawHub 以英文为主）

**常用搜索组合：**
| 场景 | 关键词 |
|------|--------|
| AI Agent 工具 | `ai agent mcp` |
| 数据分析 | `data analysis pandas` |
| 网页抓取 | `web scraping browser` |
| 文件处理 | `file convert pdf docx` |
| 日历/日程 | `calendar schedule automation` |
| 代码审查 | `code review lint` |

## 结果评估优先级

1. **Stars 数量**：越高越受信任（>1000 为佳）
2. **最近更新**：30天内有更新 = 活跃维护
3. **描述清晰度**：README 是否完整
4. **许可证**：MIT/Apache 为友好开源协议

## SkillHub 搜索说明

SkillHub 是国内优先的 Skill 商店（腾讯出品），提供加速、合规的技能搜索与安装能力。

**CLI 安装**：
```bash
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash -s -- --cli-only
```

**搜索命令**：
```bash
# 通过 search.py 搜索
python3 scripts/search.py "关键词" --source skillhub

# 直接使用 skillhub CLI
skillhub search "关键词"
skillhub search "关键词" --json  # JSON 格式输出
```

**安装命令**：
```bash
# 安装到指定 skills 目录（必须用 --dir，否则默认装到 ./skills/）
skillhub install <slug> --dir ./
# 各 AI 客户端 skills 目录：
#   Claude Code: ~/.claude/skills/
#   Cursor: ~/.cursor/skills/
#   Windsurf: ~/.codeium/windsurf/skills/
#   Codex: ~/.codex/skills/
#   Gemini CLI: ~/.gemini/skills/
```

**优先策略**：涉及技能发现/安装/升级时优先 `skillhub`（CN 更快更合规），不可用/无匹配则回退 `clawhub` 并说明。

## 无结果时的处理

1. 换同义词重搜（如 `agent` → `assistant`）
2. 拆分关键词分别搜（如 `pdf excel` → `pdf` 和 `excel` 分两次）
3. 搜索更宽泛的分类词
4. 直接告知用户：该需求暂无现成 Skill，可考虑自建（mu-skill-creator）
