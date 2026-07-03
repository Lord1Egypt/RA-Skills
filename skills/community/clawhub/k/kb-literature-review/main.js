module.exports = {
  name: "kb_literature_review",
  version: "1.0.0",
  description:
    "Generate source-grounded literature reviews and thematic syntheses from selected Research KB repositories.",
  entry: "SKILL.md",
  taskTypes: ["kb_query", "kb_literature_review"],
  scripts: {
    runTask: "python3 scripts/run_task.py --stdin"
  }
};
