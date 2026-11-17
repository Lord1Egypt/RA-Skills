# 虚假精确数字示例

这个示例故意混合“该弱化的数字”和“该保留的数字”，用于测试 `audit --profile numbers`。

她的手指沿着杯沿往上移动了三厘米，又停了七秒。老高看着她，觉得那段沉默大约有二点五秒那么长。

窗外那栋楼高 476 米，这是新闻里反复播过的数字。报告上写着，伤口长 2.3 厘米，边缘整齐，像被薄刃划开。

她又向后退了 1 厘米，其实没有人会在那时候量这个。她只是退了一点，刚好退到灯照不到的地方。

## 使用

```powershell
python -m humanwriting.cli audit `
  --draft examples/false-precision-draft.zh-CN.md `
  --profile numbers
```
