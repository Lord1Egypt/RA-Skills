# Hopola 发布清单

## 发布前检查
- 目录完整：主技能、6 个子技能、脚本、资产、双语文档。
- 安全通过：无明文 key，`gateway.key_value` 为空。
- 映射通过：图片/视频/3D 的固定工具与回退策略有效。
- 版本通过：`VERSION.txt` 为 `x.y.z` 语义化版本格式。

## 执行命令
```bash
cd .trae/skills/Hopola
python3 scripts/check_tools_mapping.py
python3 scripts/validate_release.py
python3 scripts/build_release_zip.py
```

## 产物
- `Hopola-Skills/hopola-clawhub-v<version>-<timestamp>.zip`

## 当前版本
- 版本号：`1.0.9`
- 变更摘要：补充 ClawHub 审核说明模板，并强化“无 key 不执行生成调用”的声明一致性，降低 Suspicious 告警概率。
- 新增能力：README 增加可直接粘贴的审核说明（凭证、域名、本地文件用途、计费保护、日志策略）。
- 兼容性说明：不改变搜索→生成→上传→报告调用链路；仅增强声明与发布说明。
- 风险与回滚：如需回滚，可恢复 `README.zh-CN.md` 审核说明区与本版本文案更新。

## ClawHub 审查关注点
- 凭证字段统一：文档、模板、脚本均以 `MAAT_TOKEN_API` 为主，历史字段仅作兼容。
- 端点可控：自定义端点必须命中 `MAAT_TOKEN_API_ALLOWED_HOSTS`。
- 日志最小化：`OPENCLAW_REQUEST_LOG` 默认 `0`，仅在显式开启时输出调试日志。
- 敏感脱敏：token、policy、签名及凭证参数在日志中强制脱敏。

## 回归验证记录（1.0.9）
- 发布校验：`check_tools_mapping` 与 `validate_release` 均通过。
- 打包产物：见项目根目录最新 `hopola-clawhub-v1.0.9-<timestamp>.zip`。

## 回归验证记录（1.0.6）
- 公网 URL 回归：输入可访问的 `https` 商品图 URL，流程可直接通过前置校验并完成生成。
- 会话图回归：输入会话上传图片引用后，会先上传归一化为可访问 URL，再进入生成阶段并返回结果。
- 不可访问 URL 回归：输入不可访问 URL 会在前置校验阶段阻断，返回结构化错误与可执行重试建议。
- 发布校验：`check_tools_mapping` 与 `validate_release` 均通过。
- 打包产物：`/Users/youpengtu/Hopola-Skills/hopola-clawhub-v1.0.6-20260330-160116.zip`。

## 回归验证记录（1.0.3）
- 单图回归：本地单图路径输入可解析为上传候选，验证通过。
- 会话图回归：`openclaw://session_uploads//demo.png` 可归一化为 `/mnt/data/session_uploads/demo.png`，验证通过。
- 异常 URL 回归：`https://example.com//a///b.png?x=1` 可标准化为 `https://example.com/a/b.png?x=1`，验证通过。
- 发布校验：`check_tools_mapping` 与 `validate_release` 均通过。
- 打包产物：见项目根目录最新 `hopola-clawhub-v1.0.3-<timestamp>.zip`。

## 版本说明模板
- 版本号：`x.y.z`
- 变更摘要：
- 新增能力：
- 兼容性说明：
- 风险与回滚：
