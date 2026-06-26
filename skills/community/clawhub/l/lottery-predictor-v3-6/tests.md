# 测试用例

## 预测功能测试

```bash
# 测试 1：正常预测
python3 scripts/v2.15_prediction.py --issue 2026035

# 预期输出：
# {
#   "success": true,
#   "version": "V2.15",
#   "issue": "2026035",
#   "predictions": {
#     "red_top10": [...],
#     "blue_top4": [...],
#     ...
#   }
# }
```

## 验证功能测试

```bash
# 测试 2：验证准确率
python3 scripts/verify.py --issue 2026034 --actual 3,6,13,21,28,29,6

# 预期输出：
# {
#   "issue": "2026034",
#   "red_matches": X,
#   "blue_match": 0/1,
#   "prize_level": "..."
# }
```

## 错误处理测试

```bash
# 测试 3：已开奖期号
python3 scripts/v2.15_prediction.py --issue 2026033

# 预期输出：
# {
#   "success": false,
#   "error": "2026033 期已开奖..."
# }
```
