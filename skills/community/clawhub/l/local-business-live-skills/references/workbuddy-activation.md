# WorkBuddy 新会话激活指南

WorkBuddy 的 skill 系统设计决定：新会话不会自动加载用户自行安装的 skill。需要手动激活。

## 激活方法

新开会话时，复制下面这句话发送给 AI：

```
请读取 ~/.codebuddy/skills/local-business-live-cycle/SKILL.md
然后按里面的流程帮我诊断门店。
我说「写视频」转口播模式，说「复盘」转复盘模式。
```

## 触发词速查

| 你说 | 它做 |
|------|------|
| 诊断门店 | 逐题问20题 → 出诊断报告 |
| 写视频 | 选选题→选Hook→出稿→5铁律检查 |
| 复盘昨天的直播 | 按六部曲分析直播数据 |
| 复盘那条视频 | 按T+3d闭环对比预测 vs 实际 |
| 福袋怎么发 | 讲解福袋×放单循环法 |
| 不会用 / 卡住了 | 显示异常处理fallback |

## 安装路径确认

- WorkBuddy: `~/.codebuddy/skills/local-business-live-cycle/SKILL.md`
- Hermes: `~/.hermes/profiles/deepseek-v4/skills/consulting/local-business-live-cycle/SKILL.md`
- SkillHub 安装: `skillhub install local-business-live-cycle`
