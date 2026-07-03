module.exports = {
  name: "kb_eval_repo",
  version: "1.0.0",
  description:
    "Evaluate GitHub/open-source repositories against the selected Research KB context and return query-compatible answers with citations.",
  entry: "SKILL.md",
  taskTypes: ["kb_query", "kb_eval_repo"],
  scripts: {
    runTask: "python3 scripts/run_task.py --stdin"
  }
};
