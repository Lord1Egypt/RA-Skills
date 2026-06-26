# OpenClaw Dual Cleanup 测试指南

## 测试场景 (v2.0.0)

### 1. Python版本测试
```bash
# 1.1 显示版本信息
python scripts/clean-sessions-dual.py --version

# 1.2 预览模式 (安全测试)
python scripts/clean-sessions-dual.py --mode dry-run

# 1.3 交互模式测试
python scripts/clean-sessions-dual.py

# 1.4 指定清理时长
python scripts/clean-sessions-dual.py --hours 24

# 1.5 强制模式测试
python scripts/clean-sessions-dual.py --mode force --hours 1
```

### 2. PowerShell版本测试
```powershell
# 2.1 预览模式
.\scripts\clean-sessions-dual.ps1 -Mode preview

# 2.2 测试向后兼容参数
.\scripts\clean-sessions-dual.ps1 -DryRun
.\scripts\clean-sessions-dual.ps1 -Force -Hours 72

# 2.3 交互模式
.\scripts\clean-sessions-dual.ps1

# 2.4 完整清理
.\scripts\clean-sessions-dual.ps1 -Mode force -Hours 168
```

### 3. 模拟实战场景
```bash
# 3.1 模拟HEARTBEAT触发 (智能清理)
# 当检测到会话文件数量 > 10时自动触发
python scripts/clean-sessions-dual.py --mode force

# 3.2 模拟周一深度清理
# 每周一自动执行72小时前的清理
python scripts/clean-sessions-dual.py --mode force --hours 72

# 3.3 模拟紧急磁盘空间清理
# 磁盘不足时清理7天前的所有文件
python scripts/clean-sessions-dual.py --mode force --hours 168
```

### 4. 测试验证
```bash
# 4.1 验证执行结果
# 查看工作区中的session文件数量
Get-ChildItem "~/.openclaw" -Recurse -Filter *.jsonl | Measure-Object | Select-Object -ExpandProperty Count

# 4.2 验证内存释放效果
# 通过报告查看释放的空间大小

# 4.3 验证索引一致性
# 使用OpenClaw命令验证会话状态
openclaw sessions list --limit 5
```

## 预期行为

### 交互式模式 (默认)
1. ✅ 显示清理计划和要操作的文件列表
2. ✅ 询问用户确认 (输入 y 继续)
3. ✅ 执行双重清理: 索引 + 物理文件
4. ✅ 生成详细报告 (文件数/大小/时间)

### 强制模式 (-Force / --mode force)
1. ✅ 跳过所有确认提示
2. ✅ 直接执行双重清理
3. ✅ 适用于定时任务和后台执行

### 预览模式 (-DryRun / --mode dry-run)
1. ✅ 显示要清理的内容但不实际删除
2. ✅ 适合安全检查和学习
3. ✅ 输出详细的清理计划

## 测试验证点

### ✅ 功能验证
- [ ] 编码问题已解决 (中文显示正常)
- [ ] 双重清理机制正常工作
- [ ] 清理报告信息完整
- [ ] 参数解析正确
- [ ] 错误处理友好

### ✅ 兼容性验证
- [ ] PowerShell 5.1+ 支持
- [ ] Python 3.6+ 支持  
- [ ] Windows 兼容性
- [ ] Linux/macOS 兼容性 (Python版本)

### ✅ 性能验证
- [ ] 清理响应速度 < 5秒 (无大规模文件)
- [ ] 清理报告生成 < 1秒
- [ ] 资源占用正常 (CPU/Memory)

## 问题诊断

如果测试失败，请检查：

1. **权限问题**: 是否以管理员身份运行
2. **路径问题**: OpenClaw是否已正确安装
3. **编码问题**: 终端是否支持UTF-8
4. **依赖问题**: Python/PowerShell版本是否满足要求
5. **文件锁定**: 是否有其他进程在使用会话文件

## 测试结果记录

```
测试日期: __________
测试者: __________
测试版本: 2.0.0
系统平台: Windows/Linux/macOS

测试项目         状态       备注
-----------    --------    --------------
Python版本     [✅/❌]     
PowerShell版本 [✅/❌]     
双重清理机制  [✅/❌]     
编码支持      [✅/❌]     
报告生成      [✅/❌]     
错误处理      [✅/❌]     
总体评价: __________
```

---

**重要**: 测试时建议先使用预览模式检查清理内容，确认无误后再执行实际清理。