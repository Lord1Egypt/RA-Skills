# lgd-evo 使用示例

## 1. 列出 EVO 阶段演化节点

```bash
python lgd_evo.py --list
```

输出 1 个演化节点 `agent-evolution` 的 slug 与用途。

## 2. 探测真实可用性（诚实分级）

```bash
python lgd_evo.py --verify --json-out evidence.json
```

探测：有目录 + 脚本 `--help` 退出码 0 → `LIVE`；路由声明但活动工作集无目录 → `ECOSYSTEM`。

## 3. 查看节点调用说明

```bash
python lgd_evo.py --route agent-evolution
```
