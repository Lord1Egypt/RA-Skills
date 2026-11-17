# 假失败示例：实际上已发布，但 Actions 仍然红灯

## 症状

- GitHub Actions 的 publish job 结束于 `exit code 1`
- 日志里出现 `pending-publication`
- 团队成员以为这次发布失败了

## 实际情况

- ClawHub 可能已经接受了这次发布
- 公开页或 inspect 结果可能已经能看到新版本
- 真正的问题在 workflow 对返回状态的兼容性，而不是 skill 内容本身

## 这类问题怎么判

1. 先看 registry 结果，而不是只看 Actions 红灯
2. 再确认返回的是 `pending-publication`、`published`、`unchanged` 还是 validation failed
3. 如果 registry 状态正常，优先修 workflow 对状态值的处理
