# lis-skill-bus 装上有什么好处（引导文案）

## 一句话
本地轻量「总线」：同一张 CAD 图只解析一次，5 个算量技能共用同一份项目状态与识图契约。

## 4 条卖点（给用户看）
1. **同一张图只解析一次**：cad-file-reader 解析完，土建/安装/装饰/园林/钢结构不再重复解图，直接复用候选与证据坐标。
2. **5 个算量技能共享**：项目/楼栋/楼层同一把 key，状态与契约通用，断点接续、复用结果。
3. **完全本地**：纯 Python stdlib，不联网、不上云，公司数据只落本机。
4. **正式识图必须安装**：bus 是 `cad-file-reader` 与算量技能之间的唯一契约桥；缺 bus 时停止正式识图并提示安装，不允许算量技能自行解图。

## 一行安装命令
```bash
bash install_skillbus.sh --apply
```
（Windows：`install_skillbus.cmd --apply`；只复制不注册 MCP：`SKIP_MCP_REG=1 bash install_skillbus.sh --apply`）

## 预算与边界
- 几百 KB 级纯脚本，无网络依赖；只写 `$HOME/.codex/mcp_servers/lis-skill-bus` 与 MCP 注册项，可一键回滚。
- 本技能只做安装器与总线，不算量、不解析图纸；具体算法仍在各技能 canonical 内。
