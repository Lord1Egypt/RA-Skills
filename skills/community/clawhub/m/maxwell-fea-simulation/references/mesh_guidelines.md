# Maxwell 网格设置规范

## 各区域网格尺寸参考

### 气隙（最关键）

气隙是电机仿真中精度最敏感区域。网格必须足够密。

| 气隙长度 | 最小网格尺寸 | 推荐网格尺寸 | 圆周方向分段 |
|---------|------------|------------|-------------|
| 0.3mm | 0.05mm | 0.05mm | ≥36 |
| 0.5mm | 0.08mm | 0.06mm | ≥36 |
| 0.8mm | 0.12mm | 0.08mm | ≥36 |
| 1.0mm | 0.15mm | 0.1mm | ≥36 |

### 永磁体

| 厚度方向尺寸 | 周向分段 | 径向分段 |
|------------|--------|--------|
| ≤3mm | ≥6 | ≥2 |
| 3~5mm | ≥8 | ≥3 |
| ≥5mm | ≥10 | ≥4 |

### 定子/转子轭部

| 区域 | 最大单元尺寸 |
|------|------------|
| 轭部 | ≤0.5mm |
| 齿部 | ≤0.3mm |
| 槽壁 | ≤0.2mm |

## 网格操作命令

### Maxwell 2D 网格操作

```
# 气隙内表面加密
Assign Mesh Operation:
  Type: Inside Selection / Surface Approximation
  Geometry: Inner Rotor Surface
  Maximum Length: 0.08mm

# 永磁体区域加密
Type: Inside Selection / Surface Approximation
Maximum Length: 0.15mm

# 轭部粗网格
Type: Inside Selection / Surface Approximation
Maximum Length: 0.5mm
```

### 空气包设置

```
内部求解域：到气隙外扩 20% → 正常网格
外部空气包：外扩模型尺寸 2倍 → 粗网格（0.5~2mm）
```

## 收敛性检查

1. **Resource Manager** → 查看网格数量：通常 8极36槽模型应有 5~15万单元
2. **能量误差**：静磁场 < 0.1%
3. **Solver Output** → 查看每步迭代收敛情况
