/* Bundled report data for the offline XiaoHongShu mini-tool. */
(function (root) {
  root.HKW_SCORECARD_DATA = {
    schemaVersion: "1.0",
    generatedAt: "2026-08-17",
    target: "hekouwang-content-agent",
    targetLabel: "真实扫描示例 · 内容 Agent",
    score: {
      value: 86,
      max: 100,
      confidence: 71,
      decision: "CONDITIONAL",
      maturity: {
        id: "L4",
        name: "跨宿主治理",
        description: "多宿主、CI、恢复和失败闭环基本成形。"
      },
      caps: []
    },
    dimensions: [
      { id: "instruction_routing", name: "规则与路由", weight: 8, earned: 7, status: "partial", evidence: ["AGENTS.md", "README.md", ".harness/contracts/workflow-profiles.json:8"], description: "规则和路由入口已经存在，但部分信号仍来自文档与启发式判断。" },
      { id: "verification", name: "验证入口", weight: 12, earned: 12, status: "pass", evidence: [".harness/scripts/verify.sh", "bash .harness/scripts/verify.sh --working-tree"], description: "存在统一验证入口，并能保留真实退出码。" },
      { id: "ci_parity", name: "CI 可复现性", weight: 10, earned: 10, status: "pass", evidence: [".github/workflows/ci.yml", "bash .harness/scripts/verify.sh --ci"], description: "CI 模式与本地工作区模式被明确区分。" },
      { id: "host_adapters", name: "宿主适配", weight: 8, earned: 8, status: "pass", evidence: [".claude/settings.json", ".cursor/hooks.json", ".codebuddy/settings.json", ".codex/hooks.json"], description: "四类 Agent 宿主都能找到对应配置入口。" },
      { id: "safety_enforcement", name: "安全执行", weight: 12, earned: 10, status: "partial", evidence: [".harness/hooks/safety-gate.py", ".harness/tests/test-safety-gate.sh:8"], description: "危险动作有安全门和回归测试，但仍存在未覆盖的间接路径。" },
      { id: "evidence_contracts", name: "证据与完成门", weight: 12, earned: 10, status: "partial", evidence: [".harness/contracts/task-contract.json:12", ".harness/scripts/evaluate-task.py:108"], description: "完成证据契约已经建立，部分证据仍需要人工补充。" },
      { id: "recovery_state", name: "状态与恢复", weight: 8, earned: 6, status: "partial", evidence: [".harness/scripts/episode.py", ".harness/contracts/episode-state.json:5"], description: "任务状态和恢复路径存在，但跨环境恢复仍有边界。" },
      { id: "observability", name: "可观测性", weight: 8, earned: 5, status: "partial", evidence: [".harness/scripts/observability.py", ".harness/tests/test-observability.sh:9"], description: "有脱敏事件和失败趋势，但观测仍主要是本地状态。" },
      { id: "regression", name: "正反例回归", weight: 8, earned: 8, status: "pass", evidence: [".harness/tests/fixtures", ".harness/tests/test-runtime-governance.sh:19"], description: "关键规则同时有应命中和应放过的回归样例。" },
      { id: "lifecycle_drift", name: "生命周期与漂移", weight: 6, earned: 5, status: "partial", evidence: [".harness/contracts/component-registry.json", ".harness/scripts/sync-agent-adapters.sh:8"], description: "组件注册与适配同步存在，仍需持续防止宿主漂移。" },
      { id: "docs_portability", name: "文档与可移植性", weight: 4, earned: 3, status: "partial", evidence: ["README.md", ".harness/tests/test-safety-gate.sh:45"], description: "文档已说明接入方式和边界，但移植仍需项目化适配。" },
      { id: "human_boundary", name: "人工边界", weight: 4, earned: 2, status: "partial", evidence: ["README.md:124", ".harness/contracts/component-registry.json:38"], description: "人工验收边界被明确写出，但真实宿主烟测仍待补。" }
    ],
    executions: [
      { mode: "working-tree", label: "本地工作区", command: "bash .harness/scripts/verify.sh --working-tree", executed: true, exitCode: 0, passed: true, durationSeconds: 9.836, governanceCounts: 734, failureLabels: [] },
      { mode: "ci", label: "CI 可复现模式", command: "bash .harness/scripts/verify.sh --ci", executed: true, exitCode: 0, passed: true, durationSeconds: 9.386, governanceCounts: 177, failureLabels: [] }
    ],
    hosts: [
      { host: "Claude Code", short: "Claude", configured: true, smokeTest: "unknown", evidence: [".claude/settings.json", ".claude/hooks"] },
      { host: "Cursor", short: "Cursor", configured: true, smokeTest: "unknown", evidence: [".cursor/hooks.json", ".cursor/rules"] },
      { host: "CodeBuddy", short: "CodeBuddy", configured: true, smokeTest: "unknown", evidence: [".codebuddy/settings.json", ".codebuddy/skills"] },
      { host: "Codex", short: "Codex", configured: true, smokeTest: "unknown", evidence: [".codex/hooks.json", ".codex/config.toml"] }
    ],
    profile: {
      name: "内容 Agent 工作流",
      score: { value: 35, max: 35, confidence: 35, decision: "CONDITIONAL" },
      controls: [
        { name: "已发布状态门", earned: 5, weight: 5, evidenceKind: "policy" },
        { name: "来源与事实证据", earned: 5, weight: 5, evidenceKind: "policy" },
        { name: "渠道内容合同", earned: 5, weight: 5, evidenceKind: "policy" },
        { name: "生成物边界", earned: 4, weight: 4, evidenceKind: "policy" },
        { name: "视觉验收边界", earned: 4, weight: 4, evidenceKind: "policy" },
        { name: "人工内容审阅", earned: 4, weight: 4, evidenceKind: "policy" },
        { name: "外部副作用门", earned: 4, weight: 4, evidenceKind: "policy" },
        { name: "预检与交付门", earned: 4, weight: 4, evidenceKind: "policy" }
      ]
    }
  };
}(window));
