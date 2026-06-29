/**
 * main.js — init_user Skill 入口
 *
 * 本 Skill 的行为完全由 SKILL.md 中的指令驱动：
 * OpenClaw 阅读 SKILL.md，按其中定义的流程调用 scripts/init_user.py。
 * 本文件仅提供元信息，不包含业务逻辑。
 */
module.exports = {
  name: "init_user",
  version: "1.0.0",
  description:
    "paper-kb 用户初始化：检查飞书用户注册状态，引导注册，创建 Gitea 知识库仓库与飞书多维表格",
  entry: "SKILL.md",
  scripts: {
    check: "python3 scripts/init_user.py --check --open_id <open_id>",
    register:
      "python3 scripts/init_user.py --register --open_id <open_id> --gitea_username <name> --research_direction <direction>",
    updateFeishu:
      "python3 scripts/init_user.py --update-feishu --open_id <open_id> --feishu_app_token <token> --feishu_table_id <id>",
  },
};
