# 试点：cad-file-reader → 土建算量 状态打通

目标：验证“cad 解析 → 土建算量取数”两端通过 lis-skill-bus 连接，
后续再扩展安装/装饰/园林，避免一次性改 5 个 skill。

## 接线顺序（每步完成再下一步）
1. cad-file-reader：解析完成后 `push_project_state(project=..., entry=cad-contract/v1)`
   - 契约 = `cad-contract/v1`（内含 project_key / producer / source / contract + 置信分层）
2. 土建算量（tujian-suanliang）：开工前 `get_project_state(project=...)`
   - 命中则直接复用候选，不重复读图；未命中表示当前没有可复用契约
3. bus 记录 `source_skill` 与 `pushed_at`，保证可追溯

## 接入方式
- 有 MCP：`mcp__lis_skill_bus__get_project_state`
- 无 MCP：`python3 skillbus.py get-project-state --project XXX`（同一 bus 包的 CLI，同样读写同一 state.json）
- 无 bus：正式识图链路停止并提示安装，不由算量技能自行解图

## 验收
- [x] cad 解析一次后，土建算量无需再次调用 CAD 解析（pilot_verify.sh 实测命中）
- [x] 项目 key（project/building/floor）一致时能取到同一份契约（实测）
- [x] state.json 原子写（os.replace；损坏时读侧降级为空库，已实现）
