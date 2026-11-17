DSH Writing Plugin 0.3.2 bundles Human Writing core 0.17.2, writing modules and the approved logo.

## DSH Compatibility & Anti-AI Upgrades

- Fully compatible with official DSH 0.2.1-rc.2 and 0.2.2-rc.3+ packages with broadened semver ranges.
- Added robust Windows Python runtime probing (`probePython`) inspecting virtual environments, avoiding Windows Store execution alias stubs.
- Documented DSH 0.2.2+ subagent parameter support including `reasoning_effort` and `agent_preset` routing.
- Integrated enhanced anti-AI patterns: reasoning-bleed detection (`COT001`), melodramatic physiological kits (`BODY002`), pseudo-intellectual metaphors (`PSEUDO001`), manufactured hype (`MEDIA001`), and expanded English slop filters (`LEX001`).
- Fixed multi-threaded package lock contention on Windows NTFS.

## Agent Mode And Reliability

- On-demand caller-scoped delegation discovery and configurable `delegationToolName`.
- Full paged assignments, visible claim leases and explicit expired-claim status.
- Correct serious-document source-check schemas and consistent MCP/core result limits.
- Official DSH 0.2.1-rc.2 and 0.2.2-rc.3 Cordis/MCP integration tested; native live-model children
  still require a host provider, driver, permissions and available capacity.
- 按需检查智能体可见的委派工具，不代装驱动、不改变模型、不把启动当完成。

## 多 Agent 长篇写作

- 从大纲开始，依次完成大纲检查、分块规划、逐块写作、逐块独立审稿和全局衔接审核。
- 六万字符、每块五千字符规划为十二个写作任务及对应审稿任务；默认按依赖执行，显式独立契约允许受限并行。
- 交接累计事实状态和待承接事项，检查过渡证据、段落覆盖和相邻块；返修使受影响的后续结果失效。
- 详细编排协议按需加载，宿主缺少原生子代理执行器时明确说明角色轮次降级。

## Multi-Agent Long-Form Writing

The plugin adds outline checking, block planning, writers, independent per-block
editors, and final continuity review. Explicit state contracts govern parallel
blocks; sequential dependencies remain the default. Claims and versioned results
prevent stale workers or outdated approvals from entering final assembly.

Install:

```sh
dsh plugin --profile web add https://github.com/whh110112/human-writing-skills/releases/download/dsh-v0.3.2/dsh-advanced-human-writing.tgz
```

Use `desktop` for a desktop profile. Requires Python 3.9+ on PATH (or an explicit
pythonCommand) and Node ^22.19.0 or >=24. Tested with official DSH 0.2.1-rc.2
and 0.2.2-rc.3 Cordis/MCP packages. Actual native delegation requires the host's subagent service,
provider, tool and model driver. Live-model child execution has not been exercised.

Validation: 236 Python tests completed successfully with one environment-dependent
skip locally; eight DSH integration tests and isolated tarball verification passed.
