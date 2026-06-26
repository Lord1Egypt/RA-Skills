---
name: jyotish-full-reading-integration
description: 印度占星 full-reading 21步调用链集成方案（v4.4.0）
version: 4.4.0
author: 助手
tags: [jyotish, integration, full-reading, karaka-jh-mode, jyotish-engine]
related_skills: [jyotish-engine-modules, jyotish-vedic-astrology]
---

# 印度占星 Full-Reading 21步调用链集成方案

将 5 个新增模块（`special_lagnas` / `karaka_calculator` / `vimsopaka_calculator` / `avastha_calculator` / `divisional_charts_extended`）整合进 `jyotish_engine.py` 的 `full-reading` 调用链。

## 核心变化

### 版本升级
- **v4.1.0** → **v4.4.0**
- 调用步骤：**16步** → **21步**
- 新增 5 个插入点

### 21步调用链完整流程

```
Step 1   → chart (基础星盘)
Step 1.5 → special-lagnas (特殊上升点) ✨新增
Step 2   → dasha (行星时期)
Step 3   → yoga (组合配置)
Step 4   → varga-full (标准分盘)
Step 4.5 → vimsopaka (分盘力量) ✨新增
Step 4.6 → varga-extended (扩展分盘) ✨新增
Step 5   → aspects (相位)
Step 6   → jaimini (+karaka-jh) ✨JH兼容模式
Step 7   → nakshatra-adv (星宿高级)
Step 8   → argala (干预力量)
Step 9   → tajika (年运)
Step 10  → shadbala (六力)
Step 10.5 → avasthas (行星状态) ✨新增
Step 11  → ashtakavarga (八分法)
Step 12  → validate (验证)
Step 13  → audit (审计)
Step 14  → actionable-context (可执行上下文)
Step 15  → congregation (汇总)
Step 16  → vivah-saham (婚姻点)
```

## 5个新模块插入点详解

### 1. Step 1.5 - Special Lagnas（特殊上升点）
**位置**：Chart 之后，Dasha 之前  
**模块**：`special_lagnas.py`  
**功能**：
- Bhava Lagna（宫位上升）
- Hora Lagna（时辰上升）
- Ghati Lagna（Ghati上升）
- Vighati Lagna（Vighati上升）
- Varnada Lagna（Varnada上升）
- Sree Lagna（财富上升）

**调用示例**：
```python
from scripts.special_lagnas import SpecialLagnasCalculator

special_lagnas = SpecialLagnasCalculator.calculate(
    asc_degree=chart_data['ascendant'],
    sun_degree=chart_data['planets']['Sun'],
    moon_degree=chart_data['planets']['Moon'],
    birth_time_ghatis=chart_data['ghatis']
)
```

### 2. Step 4.5 - Vimsopaka（分盘力量）
**位置**：Varga 之后，Aspects 之前  
**模块**：`vimsopaka_calculator.py`  
**功能**：
- 16分盘权重系统（Shodasavarga）
- 10分盘权重系统（Dasavarga）
- Varga Dignity 尊严等级判定
- Vimsopaka Bala 总分计算

**调用示例**：
```python
from scripts.vimsopaka_calculator import VimsopakaCalculator

vimsopaka_16 = VimsopakaCalculator.calculate_shodasavarga(
    planet='Sun',
    varga_positions=varga_data
)

vimsopaka_10 = VimsopakaCalculator.calculate_dasavarga(
    planet='Sun',
    varga_positions=varga_data
)
```

### 3. Step 4.6 - Varga Extended（扩展分盘）
**位置**：Vimsopaka 之后，Aspects 之前  
**模块**：`divisional_charts_extended.py`  
**功能**：
- D5（Panchamsa）- 权力/名声
- D6（Shashthamsa）- 健康/疾病
- D8（Ashtamsa）- 突发事件/隐秘
- D11（Ekadasamsa）- 收益/成就

**调用示例**：
```python
from scripts.divisional_charts_extended import DivisionalChartsExtended

extended_vargas = DivisionalChartsExtended.calculate_extended(
    chart_data=chart_data,
    divisions=[5, 6, 8, 11]
)
```

### 4. Step 6+ - Karaka JH Compatible（JH兼容模式）
**位置**：Jaimini 内部  
**模块**：`karaka_calculator.py`  
**功能**：
- **JH_COMPATIBLE 模式**：Rahu 强制降级到 MK（Marana Karaka）
- 输出三种 Karaka 分配：
  - `chara_karaka_7`：标准 BPHS 7星制
  - `chara_karaka_8`：标准 BPHS 8星制
  - `chara_karaka_jh`：**Jagannatha Hora 兼容模式**

**调用示例**：
```python
from scripts.karaka_calculator import KarakaCalculator, KarakaMode

# 标准 BPHS 8星制
karaka_8 = KarakaCalculator.calculate(
    planets=chart_data['planets'],
    mode=KarakaMode.BPHS_8
)

# JH 兼容模式（Rahu 限制在 MK）
karaka_jh = KarakaCalculator.calculate(
    planets=chart_data['planets'],
    mode=KarakaMode.JH_COMPATIBLE
)
```

**JH 模式核心逻辑**：
```python
# Rahu 在 JH 模式下强制降级
if mode == KarakaMode.JH_COMPATIBLE:
    if 'Rahu' in sorted_planets:
        rahu_index = sorted_planets.index('Rahu')
        # 确保 Rahu 只能是 MK（第8位）
        if rahu_index < 7:
            sorted_planets.remove('Rahu')
            sorted_planets.append('Rahu')
```

### 5. Step 10.5 - Avasthas（行星状态）
**位置**：Shadbala 之后，Ashtakavarga 之前  
**模块**：`avastha_calculator.py`  
**功能**：
- Bala Avastha（年龄状态）：婴儿/少年/青年/老年/死亡
- Jagrat Avastha（警觉状态）：清醒/梦境/深睡
- Deeptadi Avastha（情绪状态）：15种状态
- Lajjitadi Avastha（荣辱状态）：6种状态
- Shayanadi Avastha（姿态状态）：12种状态

**调用示例**：
```python
from scripts.avastha_calculator import AvasthaCalculator

avasthas = AvasthaCalculator.calculate_all(
    planet='Sun',
    degree=chart_data['planets']['Sun'],
    house=chart_data['houses']['Sun'],
    aspects=aspect_data
)
```

## jyotish_engine.py 修改要点

### 1. 导入新模块
```python
# 在文件顶部添加
from scripts.karaka_calculator import KarakaCalculator, KarakaMode
from scripts.special_lagnas import SpecialLagnasCalculator
from scripts.vimsopaka_calculator import VimsopakaCalculator
from scripts.avastha_calculator import AvasthaCalculator
from scripts.divisional_charts_extended import DivisionalChartsExtended
```

### 2. 修改 full_reading() 函数
```python
def full_reading(birth_data):
    """
    完整解盘（21步调用链）
    v4.4.0 - 整合 5 个新模块
    """
    result = {
        'version': '4.4.0-full-reading',
        'modules': {}
    }
    
    # Step 1: Chart
    result['modules']['chart'] = calculate_chart(birth_data)
    
    # Step 1.5: Special Lagnas ✨新增
    result['modules']['special_lagnas'] = SpecialLagnasCalculator.calculate(
        asc_degree=result['modules']['chart']['ascendant'],
        sun_degree=result['modules']['chart']['planets']['Sun'],
        moon_degree=result['modules']['chart']['planets']['Moon'],
        birth_time_ghatis=birth_data['ghatis']
    )
    
    # Step 2: Dasha
    result['modules']['dasha'] = calculate_dasha(birth_data)
    
    # Step 3: Yoga
    result['modules']['yoga'] = calculate_yoga(result['modules']['chart'])
    
    # Step 4: Varga Full
    result['modules']['varga_full'] = calculate_varga_full(result['modules']['chart'])
    
    # Step 4.5: Vimsopaka ✨新增
    result['modules']['vimsopaka'] = {}
    for planet in result['modules']['chart']['planets']:
        result['modules']['vimsopaka'][planet] = {
            'shodasavarga': VimsopakaCalculator.calculate_shodasavarga(
                planet=planet,
                varga_positions=result['modules']['varga_full']
            ),
            'dasavarga': VimsopakaCalculator.calculate_dasavarga(
                planet=planet,
                varga_positions=result['modules']['varga_full']
            )
        }
    
    # Step 4.6: Varga Extended ✨新增
    result['modules']['varga_extended'] = DivisionalChartsExtended.calculate_extended(
        chart_data=result['modules']['chart'],
        divisions=[5, 6, 8, 11]
    )
    
    # Step 5: Aspects
    result['modules']['aspects'] = calculate_aspects(result['modules']['chart'])
    
    # Step 6: Jaimini (含 JH 兼容模式) ✨修改
    result['modules']['jaimini'] = {
        'chara_karaka_7': KarakaCalculator.calculate(
            planets=result['modules']['chart']['planets'],
            mode=KarakaMode.BPHS_7
        ),
        'chara_karaka_8': KarakaCalculator.calculate(
            planets=result['modules']['chart']['planets'],
            mode=KarakaMode.BPHS_8
        ),
        'chara_karaka_jh': KarakaCalculator.calculate(
            planets=result['modules']['chart']['planets'],
            mode=KarakaMode.JH_COMPATIBLE
        )
    }
    
    # Step 7-9: 保持原有逻辑
    result['modules']['nakshatra_adv'] = calculate_nakshatra_advanced(result['modules']['chart'])
    result['modules']['argala'] = calculate_argala(result['modules']['chart'])
    result['modules']['tajika'] = calculate_tajika(birth_data)
    
    # Step 10: Shadbala
    result['modules']['shadbala'] = calculate_shadbala(result['modules']['chart'])
    
    # Step 10.5: Avasthas ✨新增
    result['modules']['avasthas'] = {}
    for planet in result['modules']['chart']['planets']:
        result['modules']['avasthas'][planet] = AvasthaCalculator.calculate_all(
            planet=planet,
            degree=result['modules']['chart']['planets'][planet],
            house=result['modules']['chart']['houses'][planet],
            aspects=result['modules']['aspects']
        )
    
    # Step 11-16: 保持原有逻辑
    result['modules']['ashtakavarga'] = calculate_ashtakavarga(result['modules']['chart'])
    result['modules']['validate'] = validate_chart(result['modules']['chart'])
    result['modules']['audit'] = audit_calculations(result)
    result['modules']['actionable_context'] = generate_actionable_context(result)
    result['modules']['congregation'] = congregate_results(result)
    result['modules']['vivah_saham'] = calculate_vivah_saham(result['modules']['chart'])
    
    # 添加版本说明
    result['summary'] = {
        'version': '4.4.0-full-reading',
        'total_steps': 21,
        'new_modules': [
            'special_lagnas (Step 1.5)',
            'vimsopaka (Step 4.5)',
            'varga_extended (Step 4.6)',
            'karaka_jh_compatible (Step 6+)',
            'avasthas (Step 10.5)'
        ],
        'next_step': '使用 karaka_jh 模式与 Jagannatha Hora 保持一致'
    }
    
    return result
```

## 使用方法

### 1. 复制修改后的 jyotish_engine.py
```bash
# 假设你已经有修改后的文件
cp jyotish_engine.py ~/Projects/yinduzhanxing/scripts/
```

### 2. 提交到 GitHub
```bash
cd ~/Projects/yinduzhanxing
git add scripts/jyotish_engine.py
git commit -m "feat: Integrate 5 new modules into full-reading chain (v4.4.0)

- Step 1.5: special_lagnas (特殊上升点)
- Step 4.5: vimsopaka (分盘力量)
- Step 4.6: varga_extended (扩展分盘)
- Step 6+: karaka_jh_compatible (JH兼容模式)
- Step 10.5: avasthas (行星状态)

调用链从 16 步扩展到 21 步
版本号：v4.1.0 → v4.4.0"

git push origin main
```

### 3. 测试完整调用链
```bash
cd ~/Projects/yinduzhanxing

# 运行 full-reading
python3 scripts/jyotish_engine.py --mode full-reading \
  --birth-date "1990-01-01" \
  --birth-time "12:00:00" \
  --latitude 28.6139 \
  --longitude 77.2090 \
  --timezone "Asia/Kolkata"
```

### 4. 验证输出
检查输出 JSON 是否包含：
```json
{
  "version": "4.4.0-full-reading",
  "modules": {
    "chart": {...},
    "special_lagnas": {...},
    "dasha": {...},
    "yoga": {...},
    "varga_full": {...},
    "vimsopaka": {...},
    "varga_extended": {...},
    "aspects": {...},
    "jaimini": {
      "chara_karaka_7": {...},
      "chara_karaka_8": {...},
      "chara_karaka_jh": {...}
    },
    "nakshatra_adv": {...},
    "argala": {...},
    "tajika": {...},
    "shadbala": {...},
    "avasthas": {...},
    "ashtakavarga": {...},
    "validate": {...},
    "audit": {...},
    "actionable_context": {...},
    "congregation": {...},
    "vivah_saham": {...}
  },
  "summary": {
    "version": "4.4.0-full-reading",
    "total_steps": 21,
    "new_modules": [...]
  }
}
```

## JH 兼容模式使用指南

### 为什么需要 JH 兼容模式？

Jagannatha Hora（JH）软件在 Chara Karaka 计算中有特殊规则：
- **Rahu 强制降级到 MK（Marana Karaka，第8位）**
- 即使 Rahu 的星座内度数更高，也不会超过 MK

### 三种 Karaka 模式对比

| 模式 | Rahu 处理 | 适用场景 |
|------|-----------|----------|
| **BPHS_7** | 不包含 Rahu | 传统 BPHS 7星制 |
| **BPHS_8** | Rahu 按度数排序 | 标准 BPHS 8星制 |
| **JH_COMPATIBLE** | Rahu 限制在 MK | 与 JH 软件保持一致 |

### 如何选择模式？

```python
# 如果你的 PDF 星盘来自 Jagannatha Hora
karaka = result['modules']['jaimini']['chara_karaka_jh']

# 如果使用标准 BPHS 8星制
karaka = result['modules']['jaimini']['chara_karaka_8']

# 如果使用传统 7星制（不含 Rahu）
karaka = result['modules']['jaimini']['chara_karaka_7']
```

### 验证 JH 模式
```bash
# 单独测试 Karaka 计算器
python3 scripts/karaka_calculator.py \
  --mode jh \
  --planets "Sun:45.5,Moon:120.3,Mars:200.1,Mercury:50.8,Jupiter:180.5,Venus:90.2,Saturn:250.7,Rahu:150.4"

# 输出应该显示 Rahu 固定在 MK 位置
```

## 常见问题

### Q1: 如何确认新模块已正确集成？
```bash
# 检查 jyotish_engine.py 的导入
grep "from scripts" scripts/jyotish_engine.py

# 应该看到 5 个新模块的导入
```

### Q2: 如果某个模块报错怎么办？
```bash
# 单独测试每个模块
python3 scripts/special_lagnas.py --test
python3 scripts/karaka_calculator.py --test
python3 scripts/vimsopaka_calculator.py --test
python3 scripts/avastha_calculator.py --test
python3 scripts/divisional_charts_extended.py --test
```

### Q3: 如何回退到 v4.1.0？
```bash
cd ~/Projects/yinduzhanxing
git log --oneline  # 找到 v4.1.0 的 commit hash
git checkout <commit-hash> scripts/jyotish_engine.py
```

### Q4: JH 模式和 BPHS 模式结果差异大吗？
通常只有 Rahu 的 Karaka 位置不同，其他行星保持一致。如果你的 PDF 来自 JH 软件，务必使用 JH 模式。

## 性能优化建议

1. **缓存分盘计算**：Vimsopaka 和 Varga Extended 计算量大，建议缓存结果
2. **并行计算**：Avasthas 可以对每个行星并行计算
3. **按需加载**：如果不需要全部 21 步，可以传入 `steps` 参数选择性执行

```python
# 只执行特定步骤
result = full_reading(birth_data, steps=[1, 1.5, 2, 6])
```

## 下一步

1. ✅ 完成 5 个模块集成
2. ⏳ 添加单元测试覆盖
3. ⏳ 优化性能（缓存/并行）
4. ⏳ 生成 PDF 报告模板
5. ⏳ 添加 Web API 接口

## 相关 Skills

- `jyotish-engine-modules`：5个核心模块的完整代码
- `jyotish-vedic-astrology`：印度占星专业解盘系统

## 更新日志

### v4.4.0 (2026-05-03)
- 新增 5 个模块插入点
- 调用链从 16 步扩展到 21 步
- 支持 JH 兼容模式
- 版本号从 v4.1.0 升级到 v4.4.0
