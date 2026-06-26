# TM Robot Unit Tests

## 运行测试

```bash
# 运行所有测试
python tests/test_svr_parser.py

# 运行特定测试类
python -m unittest tests.test_svr_parser.TestSVRParser

# 运行特定测试
python -m unittest tests.test_svr_parser.TestSVRParser.test_parse_joint_angle
```

## 测试结果

```
Ran 9 tests in 0.001s
OK
```

### 测试覆盖

| 测试项 | 状态 | 说明 |
|--------|------|------|
| `test_parse_joint_angle` | ✅ | 解析 6 关节角度 |
| `test_parse_error_code` | ✅ | 解析错误码 |
| `test_parse_error_code_zero` | ✅ | 解析零错误码 |
| `test_parse_project_run_true` | ✅ | 解析项目运行状态 (True) |
| `test_parse_project_run_false` | ✅ | 解析项目运行状态 (False) |
| `test_parse_multiple_variables` | ✅ | 解析多个变量 |
| `test_parse_variable_not_found` | ✅ | 处理不存在的变量 |
| `test_joint_angles` | ✅ | JointAngles 数据类 |
| `test_cartesian_pose` | ✅ | CartesianPose 数据类 |

## Mock 数据

测试使用 Mock 数据模拟 TMflow SVR 协议响应，不需要真实机器人。

**协议格式：**
```
[name][type][null][data][marker]
```

**示例：**
```python
body = b'Joint_Angle'      # 变量名
body += b'\x18\x00'        # 类型码 (0x18 = 24 bytes = 6 floats)
body += struct.pack('<6f', -1.0, 2.0, 1.5, 0.5, -0.5, -1.0)  # 数据
body += b'\x0b\x00'        # 标记
```

## 添加新测试

1. 在 `tests/` 目录创建新测试文件
2. 继承 `unittest.TestCase`
3. 使用 `MockSVRParser` 创建测试数据
4. 运行测试验证

## CI/CD 集成

```yaml
# GitHub Actions 示例
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: python tests/test_svr_parser.py
```
