# jyotish_engine.py v4.4.0 集成检查清单

## 前置准备

- [ ] 确认 5 个新模块已存在于 `scripts/` 目录
  - [ ] `karaka_calculator.py`
  - [ ] `special_lagnas.py`
  - [ ] `vimsopaka_calculator.py`
  - [ ] `avastha_calculator.py`
  - [ ] `divisional_charts_extended.py`

- [ ] 确认依赖已安装
  ```bash
  pip install swisseph numpy
  ```

## 代码修改

### 1. 导入模块
- [ ] 在 `jyotish_engine.py` 顶部添加导入语句
  ```python
  from scripts.karaka_calculator import KarakaCalculator, KarakaMode
  from scripts.special_lagnas import SpecialLagnasCalculator
  from scripts.vimsopaka_calculator import VimsopakaCalculator
  from scripts.avastha_calculator import AvasthaCalculator
  from scripts.divisional_charts_extended import DivisionalChartsExtended
  ```

### 2. 修改 full_reading() 函数

- [ ] **Step 1.5**: 在 Chart 之后添加 Special Lagnas
  ```python
  result['modules']['special_lagnas'] = SpecialLagnasCalculator.calculate(...)
  ```

- [ ] **Step 4.5**: 在 Varga Full 之后添加 Vimsopaka
  ```python
  result['modules']['vimsopaka'] = {}
  for planet in result['modules']['chart']['planets']:
      result['modules']['vimsopaka'][planet] = {...}
  ```

- [ ] **Step 4.6**: 在 Vimsopaka 之后添加 Varga Extended
  ```python
  result['modules']['varga_extended'] = DivisionalChartsExtended.calculate_extended(...)
  ```

- [ ] **Step 6+**: 修改 Jaimini 模块，添加三种 Karaka 模式
  ```python
  result['modules']['jaimini'] = {
      'chara_karaka_7': KarakaCalculator.calculate(..., mode=KarakaMode.BPHS_7),
      'chara_karaka_8': KarakaCalculator.calculate(..., mode=KarakaMode.BPHS_8),
      'chara_karaka_jh': KarakaCalculator.calculate(..., mode=KarakaMode.JH_COMPATIBLE)
  }
  ```

- [ ] **Step 10.5**: 在 Shadbala 之后添加 Avasthas
  ```python
  result['modules']['avasthas'] = {}
  for planet in result['modules']['chart']['planets']:
      result['modules']['avasthas'][planet] = AvasthaCalculator.calculate_all(...)
  ```

### 3. 更新版本信息

- [ ] 修改 `version` 字段
  ```python
  'version': '4.4.0-full-reading'
  ```

- [ ] 添加 `summary` 字段
  ```python
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
  ```

## 测试验证

### 单元测试（每个模块独立测试）

- [ ] 测试 Special Lagnas
  ```bash
  python3 scripts/special_lagnas.py --test
  ```

- [ ] 测试 Karaka Calculator
  ```bash
  python3 scripts/karaka_calculator.py --mode jh --test
  ```

- [ ] 测试 Vimsopaka
  ```bash
  python3 scripts/vimsopaka_calculator.py --test
  ```

- [ ] 测试 Avastha
  ```bash
  python3 scripts/avastha_calculator.py --test
  ```

- [ ] 测试 Divisional Charts Extended
  ```bash
  python3 scripts/divisional_charts_extended.py --test
  ```

### 集成测试（完整调用链）

- [ ] 运行 full-reading
  ```bash
  python3 scripts/jyotish_engine.py --mode full-reading \
    --birth-date "1990-01-01" \
    --birth-time "12:00:00" \
    --latitude 28.6139 \
    --longitude 77.2090 \
    --timezone "Asia/Kolkata"
  ```

- [ ] 检查输出 JSON 结构
  - [ ] `version` 为 `4.4.0-full-reading`
  - [ ] `modules` 包含 21 个步骤
  - [ ] `special_lagnas` 存在且有数据
  - [ ] `vimsopaka` 存在且有数据
  - [ ] `varga_extended` 存在且有数据
  - [ ] `jaimini.chara_karaka_jh` 存在且有数据
  - [ ] `avasthas` 存在且有数据

### JH 兼容模式验证

- [ ] 检查 `chara_karaka_jh` 输出
  - [ ] Rahu 是否固定在 MK（第8位）
  - [ ] 其他行星排序是否正确
  - [ ] 与你的 11 页 PDF 对比是否一致

### 性能测试

- [ ] 记录完整调用链执行时间
  ```bash
  time python3 scripts/jyotish_engine.py --mode full-reading ...
  ```
  - [ ] 执行时间 < 10 秒（可接受）
  - [ ] 执行时间 < 5 秒（优秀）

## Git 提交

- [ ] 添加修改文件
  ```bash
  git add scripts/jyotish_engine.py
  ```

- [ ] 提交
  ```bash
  git commit -m "feat: Integrate 5 new modules into full-reading chain (v4.4.0)

  - Step 1.5: special_lagnas (特殊上升点)
  - Step 4.5: vimsopaka (分盘力量)
  - Step 4.6: varga_extended (扩展分盘)
  - Step 6+: karaka_jh_compatible (JH兼容模式)
  - Step 10.5: avasthas (行星状态)

  调用链从 16 步扩展到 21 步
  版本号：v4.1.0 → v4.4.0"
  ```

- [ ] 推送到 GitHub
  ```bash
  git push origin main
  ```

## 文档更新

- [ ] 更新 README.md
  - [ ] 添加 v4.4.0 版本说明
  - [ ] 更新调用链流程图
  - [ ] 添加 JH 兼容模式说明

- [ ] 更新 CHANGELOG.md
  - [ ] 记录 v4.4.0 的所有变更

## 后续优化（可选）

- [ ] 添加缓存机制（减少重复计算）
- [ ] 添加并行计算（提升性能）
- [ ] 添加按需加载（只执行指定步骤）
- [ ] 生成 PDF 报告模板
- [ ] 添加 Web API 接口

---

**检查日期**: ___________
**检查人**: ___________
**状态**: [ ] 通过 / [ ] 未通过
