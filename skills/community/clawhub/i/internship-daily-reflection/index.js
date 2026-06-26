function today() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function toLines(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.map(String).map((s) => s.trim()).filter(Boolean);
  return String(value)
    .split(/\r?\n/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function pick(lines, keywords) {
  return lines.filter((line) => keywords.some((k) => line.includes(k)));
}

function renderFallbackReport(input = {}) {
  const date = input.date || today();
  const lines = toLines(input.notes || input.raw_notes || input.text);
  const done = pick(lines, ["完成", "已做", "实现", "学习", "搭建", "整理", "修复"]);
  const issues = pick(lines, ["问题", "阻塞", "卡点", "报错", "失败"]);
  const plan = pick(lines, ["明天", "计划", "下一步", "待做"]);
  const time = pick(lines, ["小时", "h", "min", "分钟"]);

  const safeDone = done.length ? done : ["待补充：今日完成事项"];
  const safeIssues = issues.length ? issues : ["暂无明确阻塞（或待补充）"];
  const safePlan = plan.length ? plan : ["待补充：明日计划"];
  const safeTime = time.length ? time : ["待补充：时间投入"];

  return [
    `# 实习日报（${date}）`,
    "",
    "## 1) 今日完成事项",
    ...safeDone.map((x) => `- ${x}`),
    "",
    "## 2) 项目进度",
    "- 当前所在阶段：待补充",
    "- 相比昨日的推进：待补充",
    "- 里程碑状态（按期/风险）：待补充",
    "",
    "## 3) 问题与阻塞",
    ...safeIssues.map((x) => `- ${x}`),
    "",
    "## 4) 解决方案与尝试",
    "- 已采取动作：待补充",
    "- 下一步验证：待补充",
    "",
    "## 5) 时间投入",
    ...safeTime.map((x) => `- ${x}`),
    "",
    "## 6) 明日计划",
    ...safePlan.map((x) => `- [ ] ${x.replace(/^[-\[\]\s]*/, "")}`),
    "- 需要协助：待补充",
  ].join("\n");
}

function buildPrompt(input = {}) {
  const date = input.date || today();
  const notes = input.notes || input.raw_notes || input.text || "";
  return `
你是一个中文实习日报整理助手。请把用户的零散记录整理成结构化日报，风格专业、可直接发给导师。

要求：
1) 不编造事实；缺失信息标注“待补充”
2) 必须包含以下模块：
- 1) 今日完成事项
- 2) 项目进度
- 3) 问题与阻塞
- 4) 解决方案与尝试
- 5) 时间投入
- 6) 明日计划
3) 如果内容涉及智能体/OpenClaw/Skill学习，补充“7) 学习复盘（智能体方向）”
4) 日期使用：${date}

用户原始记录：
${notes}
`.trim();
}

async function run(input = {}, context = {}) {
  // Try to use runtime model client first (for OpenClaw / qwen environments).
  const prompt = buildPrompt(input);
  const model = context.model || context.llm || null;

  if (model && typeof model.generate === "function") {
    const res = await model.generate({
      prompt,
      temperature: 0.2
    });
    if (res && typeof res.text === "string" && res.text.trim()) {
      return { output: res.text.trim() };
    }
  }

  if (model && typeof model.complete === "function") {
    const text = await model.complete(prompt, { temperature: 0.2 });
    if (typeof text === "string" && text.trim()) {
      return { output: text.trim() };
    }
  }

  // Fallback when runtime model API shape is unknown.
  return { output: renderFallbackReport(input) };
}

module.exports = {
  run
};

if (require.main === module) {
  const demo = {
    notes: [
      "今天完成了 OpenClaw skill 目录搭建和 SKILL.md 编写",
      "遇到路径问题，后来迁移到项目目录",
      "花费约2小时",
      "明天计划做首次发布并补充示例"
    ]
  };
  run(demo, {})
    .then((res) => console.log(res.output))
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
}
