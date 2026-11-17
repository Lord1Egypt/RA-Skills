# 头像资源（avatars）

本目录在 SkillHub 发布包中**不含 PNG 二进制**（平台禁止上传二进制文件）。

24 个部门头像 + team.png + 4 张通用头像统一托管在 user-level 资源目录：

    ~/.workbuddy/skills/ontology-agent-assets/avatars/

`scripts/avatars.py` 的查找顺序：user-level 资源目录 优先 -> 技能包自身 `assets/avatars/` 兜底。
只要 user-level 资源目录存在对应 PNG，onboarding 即可正常取图，与旧版行为一致。
