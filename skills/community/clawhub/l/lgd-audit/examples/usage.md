# lgd-audit 使用示例

## 1. 列出 AUDIT 阶段全部审计节点

```bash
python lgd_audit_dispatcher.py --list
```

输出 10 个审计节点的 slug 与一句话用途。

## 2. 探测真实可用性（诚实分级）

```bash
python lgd_audit_dispatcher.py --verify --json-out evidence.json
```

逐节点探测：有目录 + 脚本 `--help` 退出码 0 → `LIVE`；路由声明但活动工作集无目录 →
`ECOSYSTEM`；脚本异常 → `ERROR`。

## 3. 查看单个审计器调用说明

```bash
python lgd_audit_dispatcher.py --route lgd-three-laws-auditor
```

## 4. 跑三律全库审计（生态层 lgd-audit.py）

```bash
python D:/Workbuddy/发布总账/lgd-audit.py
```

退出码 0 = 全库三律 100% 达标；1 = 存在未达标包（发布前不放行）。
