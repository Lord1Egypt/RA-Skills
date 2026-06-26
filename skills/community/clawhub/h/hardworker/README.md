# Hardworker

Hardworker is a Claude skill designed to prevent AI agents from giving up early and encourage persistent problem solving.

Hardworker 是一个用于防止 AI 在复杂任务中提前放弃的技能,通过系统化排查和多路径攻坚机制持续推进问题解决。

---

## Features | 功能特点

**EN:**

- Prevents early "cannot solve" responses  
- Encourages systematic debugging  
- Forces multi-path reasoning  
- Promotes end-to-end verification  

**CN:**

- 防止 AI 过早放弃任务  
- 鼓励系统化问题排查  
- 强制多路径解决方案思考  
- 强调端到端验证与闭环  

---

## Installation | 安装

### Claude Code CLI

```bash
# Install from local path
cp -r hardworker ~/.claude/skills/

# Or install from ClawHub
clawhub install hardworker
```

### Usage | 使用

The skill triggers automatically when:
- A task fails multiple times or progress stalls
- The agent is about to give up or defer to the user
- Passive behavior appears (not searching, not reading context)
- The user expresses frustration or asks to try again

Or invoke manually:
```
/hardworker
```

---

## Repository Structure | 仓库结构

```
hardworker/
├── README.md
├── LICENSE
└── SKILL.md
```

---

## Version History | 版本历史

- **v1.0.6** - Converted to standard Claude skill format, added motivational reminders
- **v1.0.0** - Initial OpenClaw package release as `striver-mode`

---

## License

MIT
