#!/usr/bin/env python3
"""
Maxwell 仿真检查清单生成器
生成一个结构化的仿真前检查清单
"""

def generate_checklist(project_name, motor_spec):
    """生成仿真前检查清单"""
    
    p = motor_spec
    checklist = f"""
# Maxwell FEA 仿真检查清单
**项目：{project_name}**
**生成时间：自动生成**

## 1. 几何模型检查

- [ ] 定子外径 Dso = {p.get('Dso','___')} mm
- [ ] 定子内径 Dsi = {p.get('Dsi','___')} mm
- [ ] 转子外径 Dri = {p.get('Dri','___')} mm
- [ ] 气隙长度 g = {p.get('g','___')} mm
- [ ] 铁心长度 L = {p.get('L','___')} mm
- [ ] 1/4 对称模型：角度 = {360/p.get('poles',2)}°
- [ ] 空气包外扩 ≥ 20%

## 2. 材料设置

- [ ] 定子铁心：{p.get('stator_material','请选择')}，已导入 BH 曲线
- [ ] 转子铁心：{p.get('rotor_material','请选择')}
- [ ] 永磁体：{p.get('pm_grade','请选择')}，Br = {p.get('Br','___')} T
- [ ] 永磁体充磁方向：{p.get('mag_direction','Radial/Circumferential')}
- [ ] 铜线：电导率 = {p.get('sigma_cu','5.8e7')} S/m

## 3. 边界条件

- [ ] 对称边界：Vector Potential = 0
- [ ] 外空气包：Balloon 边界
- [ ] 周期边界：主从边界配对正确

## 4. 绕组设置

- [ ] 极数 2p = {p.get('poles','___')}
- [ ] 槽数 Q = {p.get('slots','___')}
- [ ] 每槽导体数 Ns = {p.get('Ns','___')}
- [ ] 并联支路数 a = {p.get('a','___')}
- [ ] 绕组类型：Stranded
- [ ] 电流密度 J = {p.get('J','___')} A/mm²（槽满率 ≤ 55%）

## 5. 网格设置

- [ ] 气隙内表面：最大单元 ≤ {p.get('gap_mesh','0.08')} mm
- [ ] 永磁体：最大单元 ≤ 0.15 mm
- [ ] 轭部：最大单元 ≤ 0.5 mm
- [ ] 总网格单元数：预计 {p.get('est_elements','请估算')} 万

## 6. 求解设置

- [ ] 静磁场：收敛标准 Energy Error < 0.1%
- [ ] 瞬态：时间步长 ≤ 1/(freq × 360 × p) / 20
- [ ] 瞬态：求解时间 ≥ 1 个电周期
- [ ] 参数化：变量范围已定义

## 7. 后处理计划

- [ ] 气隙磁密 Bg（路径积分）
- [ ] 反电动势 E（Voltage 探针）
- [ ] 电磁转矩 T（Torque 探针）
- [ ] 铁损密度分布（Core Loss）
- [ ] 磁力线/磁密云图

---
自动生成 by Maxwell FEA Simulation Skill
"""
    return checklist


if __name__ == "__main__":
    # 示例
    spec = {
        'Dso': 90, 'Dsi': 54, 'Dri': 53.2, 'g': 0.5,
        'L': 50, 'poles': 8, 'slots': 36,
        'Ns': 28, 'a': 2,
        'stator_material': '35YT310', 'pm_grade': 'N42SH',
        'Br': 1.25, 'gap_mesh': 0.06,
        'J': 4.5,
    }
    result = generate_checklist("8极36槽PMSM仿真", spec)
    print(result)
